#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 资产④（校验面）：确定性后校验（Preflight——G.2 第 4 条双阶段命名，
生成前阶段落 A.6.2 既有语义；A.7.2 的 Delivery 属 M3）。

【M2-EP01 提前段·非正式证据】

三条铁律（与 kernel/intent/postcheck.py 同源）：
  1. 每项 check ∈ {OK, FAIL, UNKNOWN}；证据不足一律 UNKNOWN 向上冒泡——既不判 OK（假绿）
     也不判 FAIL（把没核验说成违约同样是编造结论）；
  2. overall = OK 当且仅当全部项 OK；任一 FAIL **或** 任一 UNKNOWN → overall = FAIL；
     每项 verdict 原值保留，UNKNOWN 不被改写成 FAIL；
  3. 检查器自身崩了 → 兜底成 UNKNOWN 而不是 FAIL（崩溃说明的是检测器状态，不是 bundle 违约；
     但 UNKNOWN 归 FAIL 侧，不存在崩了就当过的通道）。

本模块与 acceptance/detectors/checks.py 是**对齐而非复用**：不 import 考卷区代码、不假装等价；
考卷区那套是独立判分层（L1），本模块是考生自查——两边同红才可信，考生自查绿不等于考卷绿。

约束覆盖对照（诚实声明——本表列**不在射程**的语义面，不设 D 项、不假装覆盖）：
  · 冲突识别是否**漏了真实冲突**（BD_CONFLICT_MISSED 语义面）——只有 L2 judge / L3 人工可判；
    本模块只核验已写出的冲突结构合法、引用可溯。
  · 候选是否**实质差异**（BD_CANDIDATE_COLLAPSE 语义面）——同上，L2 探针（J1）/ L3 人工；
    本模块只判数量与状态一致性。
  · 取舍陈述**质量**（BD_TRADEOFF_MISSING 语义面）——本模块只判结构非空与引用合法。
  · BLOCKED_FEWER_THAN_TWO **不得进入 DECISION_READY** 的状态机执行面——属 Runtime
    （M3-EP02，A.4.4 七状态机），本模块管不到状态迁移，已登记 UPSTREAM_GAPS。
  · 数字溯源（D8）为**整值 token 口径**：输出中的独立数字必须与快照中出现过的某个数字
    **整值相等**（不做字段路径与单位绑定）——**弱于**考卷 numeric_grounding v0.3 的
    字段类+单位语义绑定；两者同为类级、非实例级（跨实体同类同值借位两侧都看不见，
    属 L3 人工判分面）。首版子串包含口径被对抗审查抓获借位洞（'39'⊂'3980' 判过，
    runtime_verified）后收敛为整值比对。

ctx 必给键：schema_path / fact_pool / rule_pool / snapshot / product_ids。
"""

import json
import os
import re

from .config import (
    CANDIDATE_COUNT_STATUS_VALUES,
    CANDIDATE_TARGET_COUNT,
    CONFIDENCE_LEVELS,
    COUNT_STATUS_BLOCKED,
    COUNT_STATUS_DEGRADED_TWO,
    COUNT_STATUS_TARGET_THREE,
    FACT_ID_PREFIX,
    HARD_RULE_BLOCK,
    PRODUCT_ROLES,
)
from .rules_engine import RULE_CHECK_TABLE, load_forbidden_terms

STAGE = "PREFLIGHT"


# ============================ 文本收集（D7/D8 共用） ============================

_TEXT_FIELDS_NOTE = (
    "内容承载字段：business_problem / conflicts 三段 / 候选文本面（title、strategy、"
    "rationale、risks、why_*）/ tradeoff / 诊断 summary / Trace statement。ID、引用数组、"
    "时间戳、confidence 不扫——不是面向人的内容面。机器生成的取证文本（hard_rule_results "
    "与 blocking_rule_results 的 explanation、candidate_count_explanation）只进 D7 词表面"
    "（防其携带禁用表达），**不进 D8 数字面**——取证计数（如『命中 N 处』）是审计元数据，"
    "不是模型的商业事实断言，混进数字溯源会制造机器自红。"
)


def _content_texts(bundle, include_machine_evidence=True):
    out = [bundle.get("business_problem") or ""]
    for c in bundle.get("recognized_conflicts") or []:
        out += [c.get("description") or "", c.get("side_a") or "", c.get("side_b") or ""]
    for cand in bundle.get("candidate_options") or []:
        out += [cand.get("title") or "", cand.get("strategy") or "",
                cand.get("why_this_option") or "", cand.get("why_not_primary_alternative") or ""]
        for pr in cand.get("product_roles") or []:
            out.append(pr.get("rationale") or "")
        for key in ("brand_fit", "audience_fit", "business_alignment", "production_feasibility"):
            out.append((cand.get(key) or {}).get("rationale") or "")
        for r in cand.get("risks") or []:
            out += [r.get("condition") or "", r.get("possible_impact") or "", r.get("mitigation") or ""]
        if include_machine_evidence:
            for hr in cand.get("hard_rule_results") or []:
                out.append(hr.get("explanation") or "")
    for t in bundle.get("comparative_tradeoffs") or []:
        out.append(t.get("tradeoff") or "")
    if include_machine_evidence and bundle.get("candidate_count_explanation"):
        out.append(bundle["candidate_count_explanation"])
    for d in bundle.get("blocked_candidate_diagnostics") or []:
        out.append(d.get("candidate_summary") or "")
        if include_machine_evidence:
            for hr in d.get("blocking_rule_results") or []:
                out.append(hr.get("explanation") or "")
    for entry in (bundle.get("trace_bundle") or {}).get("entries") or []:
        out.append(entry.get("statement") or "")
    return [t for t in out if t]


def _trace_type_map(bundle):
    return {
        e.get("trace_id"): e.get("trace_type")
        for e in (bundle.get("trace_bundle") or {}).get("entries") or []
        if e.get("trace_id")
    }


# ============================ 各检查项 ============================

def _d1_schema(bundle, ctx):
    schema_path = ctx.get("schema_path")
    if not schema_path or not os.path.exists(schema_path):
        return "UNKNOWN", f"输出契约不存在：{schema_path}"
    try:
        from jsonschema import Draft7Validator, FormatChecker, RefResolver
    except ImportError:
        return "UNKNOWN", "jsonschema 未安装，结构校验无从执行"
    # FormatChecker 自检（对齐 tools/test_fact_schemas.py 的 fail-closed 写法）：环境缺
    # rfc3339 校验库时 format 会**静默放行**——先喂一个非法 datetime 证明它真的在拦，
    # 拦不住就 UNKNOWN，不带着失效的 format 面宣告「结构校验通过」。
    format_checker = FormatChecker()
    probe = Draft7Validator({"type": "string", "format": "date-time"}, format_checker=format_checker)
    if not list(probe.iter_errors("不是时间")):
        return "UNKNOWN", "FormatChecker 对非法 datetime 未报错（rfc3339 校验库缺失？），format 面失效，不发 OK"
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    # base_uri 指向 contracts/schemas/ 才能解析 common.defs.json#/definitions/*
    # （解析结果与 tools/validate_schema.py 同一口径，两处不得分叉）。
    # common.defs.json **预载进 store**：RefResolver 对未缓存 $ref 会走 urlopen（file:// 也走），
    # 这与"离线自测零网络"的守卫相撞（首跑实测 RefResolutionError，runtime_verified 2026-08-18）；
    # 预载后解析零 I/O，行为不变。
    base_uri = "file://" + os.path.abspath(os.path.dirname(schema_path)) + "/"
    common_path = os.path.join(os.path.dirname(schema_path), "common.defs.json")
    if not os.path.exists(common_path):
        return "UNKNOWN", f"共用定义不存在：{common_path}（$ref 无从解析）"
    with open(common_path, encoding="utf-8") as f:
        common_defs = json.load(f)
    # 主 schema 自身也要进 store：它的 $id 会把解析作用域推成 base_uri+$id，内部
    # `#/definitions/*` 引用随之落在该 URL 下——store 里没有它就又回到 urlopen（实测确认）。
    schema_name = os.path.basename(schema_path)
    store = {
        base_uri + "common.defs.json": common_defs,
        "common.defs.json": common_defs,
        common_defs.get("$id") or "common.defs.json": common_defs,
        base_uri + schema_name: schema,
        schema_name: schema,
        schema.get("$id") or schema_name: schema,
    }
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    errors = sorted(
        Draft7Validator(schema, resolver=resolver, format_checker=format_checker).iter_errors(bundle),
        key=lambda e: list(e.path),
    )
    if errors:
        first = errors[0]
        return "FAIL", f"{len(errors)} 处违反输出契约；首处 /{'/'.join(map(str, first.path))}: {first.message[:160]}"
    return "OK", "BusinessDecisionBundle 结构校验通过（含 A.6.3 数量条件式）"


def _d2_count_status(bundle, ctx):
    status = bundle.get("candidate_count_status")
    if status not in CANDIDATE_COUNT_STATUS_VALUES:
        return "FAIL", f"candidate_count_status={status!r} 不在三态枚举内"
    ids = [c.get("candidate_id") for c in bundle.get("candidate_options") or []]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        # 重号让假设/判断引用与人工选择（A.6.4 selected_candidate_id）失去唯一落点——
        # 对抗审查抓获的 blocker（张冠李戴 + 孤儿 Trace 仍全绿），装配闸之外这里再补一道
        return "FAIL", f"candidate_id 重号 {dupes}（候选身份必须两两不同，重号使引用与人工选择失去唯一落点）"
    n = len(ids)
    explanation = bundle.get("candidate_count_explanation")
    if n > CANDIDATE_TARGET_COUNT:
        return "FAIL", f"候选 {n} 个，超出 A.6.3 目标上限 {CANDIDATE_TARGET_COUNT}"
    if status == COUNT_STATUS_TARGET_THREE and n != 3:
        return "FAIL", f"TARGET_THREE 但候选 {n} 个"
    if status == COUNT_STATUS_DEGRADED_TWO:
        if n != 2:
            return "FAIL", f"DEGRADED_TWO 但候选 {n} 个"
        if not (isinstance(explanation, str) and explanation.strip()):
            return "FAIL", "DEGRADED_TWO 但 candidate_count_explanation 为空（A.6.3：必须说明受何限制）"
    if status == COUNT_STATUS_BLOCKED and n >= 2:
        return "FAIL", f"BLOCKED_FEWER_THAN_TWO 但候选 {n} 个"
    return "OK", f"候选 {n} 个与状态 {status} 一致"


def _d3_tradeoffs(bundle, ctx):
    candidates = bundle.get("candidate_options") or []
    tradeoffs = bundle.get("comparative_tradeoffs") or []
    if len(candidates) >= 2 and not tradeoffs:
        return "FAIL", "两个及以上候选但 comparative_tradeoffs 为空（BD_TRADEOFF_MISSING 结构面）"
    ids = {c.get("candidate_id") for c in candidates}
    for t in tradeoffs:
        if not (isinstance(t.get("tradeoff"), str) and t["tradeoff"].strip()):
            return "FAIL", "存在空 tradeoff 陈述"
        dangling = [r for r in (t.get("candidate_refs") or []) if r not in ids]
        if dangling:
            return "FAIL", f"tradeoff 引用了不存在的候选 {dangling}"
    return "OK", f"{len(tradeoffs)} 条取舍结构合法（质量属 L2/L3 判分面）"


def _d4_trace_separation(bundle, ctx):
    tmap = _trace_type_map(bundle)
    if not tmap:
        return "FAIL", "trace_bundle 无条目（四类分离无从成立）"
    problems = []

    def _expect(refs, expected, where):
        for ref in refs or []:
            actual = tmap.get(ref)
            if actual is None:
                problems.append(f"{where} 引用 {ref!r} 在 trace_bundle 中不存在")
            elif actual != expected:
                problems.append(f"{where} 引用 {ref!r} 类型是 {actual}，应为 {expected}（混写）")

    for cand in bundle.get("candidate_options") or []:
        cid = cand.get("candidate_id")
        _expect(cand.get("supporting_fact_refs"), "FACT", f"候选 {cid} supporting_fact_refs")
        _expect(cand.get("applied_rule_refs"), "RULE", f"候选 {cid} applied_rule_refs")
        _expect(cand.get("assumption_refs"), "ASSUMPTION", f"候选 {cid} assumption_refs")
        _expect(cand.get("model_judgment_refs"), "MODEL_JUDGMENT", f"候选 {cid} model_judgment_refs")
    for c in bundle.get("recognized_conflicts") or []:
        for ref in c.get("trace_refs") or []:
            if ref not in tmap:
                problems.append(f"冲突 {c.get('conflict_id')} 引用 {ref!r} 不在 trace_bundle")
            elif tmap[ref] not in ("FACT", "RULE"):
                problems.append(f"冲突 {c.get('conflict_id')} 引用 {ref!r} 类型 {tmap[ref]}（冲突两面只认事实与规则）")
    for entry in (bundle.get("trace_bundle") or {}).get("entries") or []:
        if entry.get("trace_type") == "MODEL_JUDGMENT":
            supports = entry.get("supporting_trace_refs") or []
            if not supports:
                problems.append(f"MODEL_JUDGMENT {entry.get('trace_id')} 无支撑引用（A.9.2）")
            for s in supports:
                if s not in tmap:
                    problems.append(f"MODEL_JUDGMENT {entry.get('trace_id')} 支撑引用 {s!r} 不在 trace_bundle")
        tid = entry.get("trace_id") or ""
        if tid.startswith(FACT_ID_PREFIX) and entry.get("trace_type") != "FACT":
            problems.append(f"trace_id {tid!r} 带 FACT 前缀但类型是 {entry.get('trace_type')}")
    # 孤儿判红（对抗审查抓获：被拦候选/被清推荐的 ASSUMPTION/MODEL_JUDGMENT 条目残留在
    # trace_bundle 却无人引用——证据挂空比缺失更误导）：每条 ASSUMPTION/MODEL_JUDGMENT
    # 必须被某候选的 refs 或 system_recommendation.judgment_trace_ref 引用
    referenced = set()
    for cand in bundle.get("candidate_options") or []:
        referenced.update(cand.get("assumption_refs") or [])
        referenced.update(cand.get("model_judgment_refs") or [])
    rec_ref = (bundle.get("system_recommendation") or {}).get("judgment_trace_ref")
    if rec_ref:
        referenced.add(rec_ref)
    orphans = [e.get("trace_id") for e in (bundle.get("trace_bundle") or {}).get("entries") or []
               if e.get("trace_type") in ("ASSUMPTION", "MODEL_JUDGMENT") and e.get("trace_id") not in referenced]
    if orphans:
        problems.append(f"孤儿 ASSUMPTION/MODEL_JUDGMENT 条目 {orphans}（无任何候选或推荐引用）")
    if problems:
        return "FAIL", "；".join(problems[:5]) + (f"（共 {len(problems)} 处）" if len(problems) > 5 else "")
    return "OK", f"{len(tmap)} 条 trace 四类分离且引用可溯（陈述内容真实性属 L2/L3）"


def _d5_human_gate(bundle, ctx):
    if bundle.get("human_selection_required") is not True:
        return "FAIL", f"human_selection_required={bundle.get('human_selection_required')!r}（人工门绕过）"
    rec = bundle.get("system_recommendation") or {}
    cid = rec.get("candidate_id")
    if cid is None:
        return "OK", "human_selection_required=true；无系统推荐（允许为空）"
    ids = {c.get("candidate_id") for c in bundle.get("candidate_options") or []}
    if cid not in ids:
        return "FAIL", f"system_recommendation 指向不存在的候选 {cid!r}"
    ref = rec.get("judgment_trace_ref")
    tmap = _trace_type_map(bundle)
    if not ref or tmap.get(ref) != "MODEL_JUDGMENT":
        return "FAIL", f"推荐的 judgment_trace_ref={ref!r} 未指向 MODEL_JUDGMENT（A.6.3：推荐必须属模型判断）"
    return "OK", "human_selection_required=true；推荐指向存活候选且挂 MODEL_JUDGMENT"


def _d6_hard_rule_coverage(bundle, ctx):
    rule_pool = ctx.get("rule_pool")
    if rule_pool is None:
        return "UNKNOWN", "ctx 缺 rule_pool，覆盖核验无从执行"
    active = [r for r in rule_pool if r.get("status") == "ACTIVE"]
    unmapped = [r.get("rule_id") for r in active if r.get("rule_id") not in RULE_CHECK_TABLE]
    if unmapped:
        return "FAIL", f"ACTIVE 规则 {unmapped} 无实现层谓词映射——无检测器不得视为已过（fail-closed）"
    pool_versions = {r.get("rule_id"): int(r.get("version", 1)) for r in active}
    problems = []
    for cand in bundle.get("candidate_options") or []:
        cid = cand.get("candidate_id")
        results = cand.get("hard_rule_results") or []
        seen = {}
        for hr in results:
            ref = hr.get("rule_ref") or {}
            seen[ref.get("object_id")] = hr
            if ref.get("object_id") in pool_versions and int(ref.get("version", -1)) != pool_versions[ref.get("object_id")]:
                problems.append(f"候选 {cid} 规则 {ref.get('object_id')} 版本 {ref.get('version')} 与注册表不一致")
        missing = [rid for rid in pool_versions if rid not in seen]
        if missing:
            problems.append(f"候选 {cid} 缺规则评估结果 {missing}（每条 ACTIVE 规则都必须有 HardRuleResult）")
        blocks = [rid for rid, hr in seen.items() if hr.get("result") == HARD_RULE_BLOCK]
        if blocks:
            problems.append(f"候选 {cid} 带 BLOCK 结果 {blocks} 却仍在 candidate_options（A.9.1：BLOCK 不得进入下一人工节点）")
    for d in bundle.get("blocked_candidate_diagnostics") or []:
        for hr in d.get("blocking_rule_results") or []:
            if hr.get("result") != HARD_RULE_BLOCK:
                problems.append(f"阻断诊断「{d.get('candidate_summary')}」混入非 BLOCK 结果")
    if problems:
        return "FAIL", "；".join(problems[:4]) + (f"（共 {len(problems)} 处）" if len(problems) > 4 else "")
    return "OK", (f"{len(active)} 条 ACTIVE 规则逐候选有果、BLOCK 全部隔离"
                  "（PASS 仅代表词面扫描，语义面见质检单 human_only 列）")


def _d7_forbidden_lexicon(bundle, ctx):
    terms, note = load_forbidden_terms(ctx.get("lexicon_path"))
    if not terms:
        return "UNKNOWN", f"禁用词表无从核验（{note}）——空词表不等于零命中"
    texts = _content_texts(bundle)
    hits = sorted({t for txt in texts for t in terms if t in txt})
    if hits:
        return "FAIL", f"命中禁用表达：{hits}"
    return "OK", f"词表 {note} 零命中（全取证文本面，含机器生成 explanation；扫描面定义见 _TEXT_FIELDS_NOTE）"


# 独立数字抽取：排除字母数字标识符内部的数字段（C1 / P99 / R-BDD01-001 的 '1'/'99'/'001'
# 是身份字符不是事实数字——身份合法性由 D4/D9 判，混进数字溯源只会双向误伤）
_STANDALONE_NUMBER = re.compile(r"(?<![A-Za-z0-9])\d+(?![A-Za-z0-9])")


def _d8_numeric_grounding(bundle, ctx):
    snapshot = ctx.get("snapshot")
    if snapshot is None:
        return "UNKNOWN", "ctx 缺 snapshot，数字溯源无从执行"
    # 整值 token 比对（文件头「约束覆盖对照」注明的口径收敛）：快照侧取全部数字 run 作
    # token 池（宽），输出侧只取独立数字（严）；判定是**整值相等**，不是子串包含——
    # 子串口径下 '39'⊂'3980'、'80'⊂'800' 全部漏网（对抗审查 runtime_verified）。
    snap_numbers = set(re.findall(r"\d+", json.dumps(snapshot, ensure_ascii=False)))
    numbers = set()
    for txt in _content_texts(bundle, include_machine_evidence=False):
        numbers.update(_STANDALONE_NUMBER.findall(txt))
    orphans = sorted(n for n in numbers if n not in snap_numbers)
    if orphans:
        return "FAIL", f"数字 {orphans} 与快照中出现过的任何数字都不整值相等（整值 token 口径；实例级借位属 L3 人工判分面）"
    if not numbers:
        return "OK", "内容面无独立阿拉伯数字，无需溯源"
    return "OK", (f"{len(numbers)} 个独立数字均与快照数字整值相等"
                  "（整值 token 口径，弱于考卷字段级绑定；不代表实例级正确）")


def _d9_roles_and_products(bundle, ctx):
    product_ids = ctx.get("product_ids")
    if product_ids is None:
        return "UNKNOWN", "ctx 缺 product_ids，商品池核验无从执行"
    snapshot = ctx.get("snapshot") or {}
    brand = snapshot.get("brand_id")
    problems = []
    for cand in bundle.get("candidate_options") or []:
        cid = cand.get("candidate_id")
        for pr in cand.get("product_roles") or []:
            if pr.get("role") not in PRODUCT_ROLES:
                problems.append(f"候选 {cid} 角色 {pr.get('role')!r} 不在五值枚举")
            ref = pr.get("product_ref") or {}
            if ref.get("object_id") not in product_ids:
                problems.append(
                    f"候选 {cid} 引用商品 {ref.get('object_id')!r} 不在快照商品池 {product_ids}"
                    "（BD_FACT_FABRICATION 结构面：池外商品即补写）"
                )
            if ref.get("brand_id") != brand:
                problems.append(f"候选 {cid} 商品引用 brand_id={ref.get('brand_id')!r} 与快照 {brand!r} 不一致（A.1.3）")
    if problems:
        return "FAIL", "；".join(problems[:4]) + (f"（共 {len(problems)} 处）" if len(problems) > 4 else "")
    return "OK", f"角色枚举合法、商品引用均在池（池={product_ids}）"


def _d10_envelope(bundle, ctx):
    snapshot = ctx.get("snapshot")
    if snapshot is None:
        return "UNKNOWN", "ctx 缺 snapshot，封套绑定无从核验"
    artifact = bundle.get("artifact") or {}
    problems = []
    if artifact.get("artifact_type") != "BUSINESS_DECISION_BUNDLE":
        problems.append(f"artifact_type={artifact.get('artifact_type')!r}")
    if artifact.get("review_status") != "PENDING":
        problems.append(f"review_status={artifact.get('review_status')!r}（系统产出必须待人工复核，PASS 只能由人判）")
    ref = artifact.get("context_snapshot_ref") or {}
    if ref.get("object_id") != snapshot.get("snapshot_id"):
        problems.append(f"context_snapshot_ref 指向 {ref.get('object_id')!r}，非本次快照 {snapshot.get('snapshot_id')!r}")
    brands = {artifact.get("brand_id"), snapshot.get("brand_id"), (bundle.get("trace_bundle") or {}).get("brand_id")}
    if len(brands) != 1 or None in brands:
        problems.append(f"brand_id 不全等：{brands}（A.1.3）")
    if problems:
        return "FAIL", "；".join(problems)
    return "OK", "封套类型/复核态/快照绑定/品牌全等核验通过"


def _d11_confidence(bundle, ctx):
    conf = bundle.get("confidence") or {}
    if conf.get("level") not in CONFIDENCE_LEVELS:
        return "FAIL", f"bundle confidence.level={conf.get('level')!r} 不在三级枚举"
    cand_levels = [(c.get("candidate_id"), (c.get("confidence") or {}).get("level"))
                   for c in bundle.get("candidate_options") or []]
    bad = [(cid, lv) for cid, lv in cand_levels if lv not in CONFIDENCE_LEVELS]
    if bad:
        return "FAIL", f"候选置信度枚举非法：{bad}"
    if conf.get("level") == "HIGH" and any(lv != "HIGH" for _, lv in cand_levels):
        return "FAIL", "bundle 置信度 HIGH 但存在非 HIGH 候选（确定性只降不升被违反）"
    return "OK", "置信度三级枚举合法且降级方向一致"


# ============================ 入口 ============================

# item 文本内嵌出处：checks 条目键钉死为五个，不另加 source 键，出处随 item 一起走
_CHECK_TABLE = (
    ("D1", "输出契约结构校验（contracts/schemas/business_decision_bundle.schema.json，A.6.2/A.6.3）", _d1_schema),
    ("D2", "候选数量与三态一致（A.6.3 约束：目标三最低二；DEGRADED_TWO 必须带受限说明）", _d2_count_status),
    ("D3", "取舍结构非空且引用合法（A.6.2 comparative_tradeoffs；质量属 L2/L3）", _d3_tradeoffs),
    ("D4", "Trace 四类分离与引用可溯（A.1.2 / A.9.2 / B.4.2 总则）", _d4_trace_separation),
    ("D5", "人工门永真与推荐合法（A.6.2 human_selection_required 固定 true；推荐必须属 MODEL_JUDGMENT）", _d5_human_gate),
    ("D6", "硬规则逐条有果且 BLOCK 隔离（A.9.1；G.2 第 4 条①；无谓词映射的 ACTIVE 规则 fail-closed）", _d6_hard_rule_coverage),
    ("D7", "禁用表达词表零命中（唯一运营真源 acceptance/detectors/forbidden_lexicon.yaml，只读对齐）", _d7_forbidden_lexicon),
    ("D8", "数字整值溯源（输出独立数字必须与快照数字整值相等；弱于考卷字段级绑定，实例级借位属 L3）", _d8_numeric_grounding),
    ("D9", "商品角色枚举与商品池核验（A.2.6 五值；池外商品 = 补写，BD-D02 禁止结果结构面）", _d9_roles_and_products),
    ("D10", "Artifact 封套与品牌绑定（A.9.3 / A.1.3；review_status 必须 PENDING）", _d10_envelope),
    ("D11", "置信度三级枚举与降级方向（A.2.5：只三级，不合成综合分）", _d11_confidence),
)


def preflight(bundle, ctx):
    """跑全部 D 项。返回 {"stage", "segment", "checks": [...], "overall"}。"""
    checks = []
    if not isinstance(bundle, dict):
        for check_id, item, _fn in _CHECK_TABLE:
            checks.append({"id": check_id, "item": item, "verdict": "UNKNOWN",
                           "machine_checkable": True, "detail": f"bundle 不是 dict（{type(bundle).__name__}）"})
        return {"stage": STAGE, "segment": "M2-EP01 提前段·非正式证据", "checks": checks, "overall": "FAIL"}
    for check_id, item, fn in _CHECK_TABLE:
        try:
            verdict, detail = fn(bundle, ctx)
        except Exception as e:   # 检查器崩溃 → UNKNOWN（不是 FAIL 也绝不是 OK）
            verdict, detail = "UNKNOWN", f"检查器异常（{type(e).__name__}）：{e}"
        checks.append({"id": check_id, "item": item, "verdict": verdict,
                       "machine_checkable": True, "detail": detail})
    overall = "OK" if all(c["verdict"] == "OK" for c in checks) else "FAIL"
    return {"stage": STAGE, "segment": "M2-EP01 提前段·非正式证据", "checks": checks, "overall": overall}
