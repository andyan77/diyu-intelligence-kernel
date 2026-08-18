#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 编排：确定性前处理与输入闸 → LLM 步1 冲突识别 → LLM 步2 候选生成
→ 确定性规则评估与 BLOCK 隔离 → LLM 步3 逐候选取舍（只见存活候选）→ 确定性装配
→ 确定性后校验（Preflight，G.2 第 4 条双阶段命名）。

【M2-EP01 提前段·非正式证据】IA-1 未 PASS，本 runner 的任何一次运行都不构成 IA-2 取证。

分步结构真源 = C.3 BD 分步裁决：三步拆分让 BD_CONFLICT_MISSED / BD_CANDIDATE_COLLAPSE /
BD_TRADEOFF_MISSING 三个失败标签各自能定位到具体一步；第四步是**确定性装配**——
human_selection_required 恒 true、candidate_count_status 按存活候选数计算、逐规则
HardRuleResult 由规则引擎生成，这三件事**都不问模型**（删掉代码只留 prompt 行为不变 =
已退化成 Prompt 套壳，C.3 红线测试）。

退出码：0 = Preflight 全过；1 = 后校验判 FAIL（bundle 仍写盘——失败的 bundle 是取证材料）；
2 = 没跑完（输入闸不过 / 模型输出不合形 / 组装不出合法产物；**不产出半成品 bundle**）。

确定性注入：--run-id / --created-at 两个可选参数供离线自测注入固定值（同一输入两次运行
逐字节一致的前提）；不给则取时钟并向 stderr 说明，不静默。
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

from . import llm, postcheck, preprocess, rules_engine, trace
from .config import (
    ARTIFACT_TYPE,
    ASSUMPTION_ID_PREFIX,
    CANDIDATE_TARGET_COUNT,
    COUNT_STATUS_BLOCKED,
    COUNT_STATUS_DEGRADED_TWO,
    COUNT_STATUS_TARGET_THREE,
    FIT_ASSESSMENTS,
    HARD_RULE_BLOCK,
    MODEL_JUDGMENT_ID_PREFIX,
    OUTPUT_SCHEMA_VERSION,
    PRODUCT_ROLES,
    PROMPT_STEP1_PATH,
    PROMPT_STEP2_PATH,
    PROMPT_STEP3_PATH,
    SCHEMA_BUSINESS_DECISION_BUNDLE,
)

SEGMENT_MARK = "M2-EP01 提前段·非正式证据"

PROMPT_BEGIN = "<<<PROMPT_BEGIN>>>"
PROMPT_END = "<<<PROMPT_END>>>"


# ============================ 一、Prompt 装载与渲染 ============================

def load_prompt(path):
    """读分步 prompt 文件：YAML 文件头给版本号，正文由 PROMPT_BEGIN/END 切出（标记不发给模型）。"""
    import yaml
    raw = Path(path).read_text(encoding="utf-8")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise RuntimeError(f"prompt 文件缺 YAML 文件头：{path}")
    front = yaml.safe_load(parts[1])
    if not isinstance(front, dict) or not front.get("prompt_version"):
        raise RuntimeError(f"prompt 文件头缺 prompt_version：{path}")
    body = parts[2]
    if PROMPT_BEGIN not in body or PROMPT_END not in body:
        raise RuntimeError(f"prompt 文件缺 {PROMPT_BEGIN}/{PROMPT_END} 标记：{path}")
    body = body.split(PROMPT_BEGIN, 1)[1].split(PROMPT_END, 1)[0].strip()
    return body, str(front["prompt_version"])


def render_prompt(template, mapping):
    """逐占位符替换；渲染完仍残留 {{ 占位符 = 模板与代码脱钩，当场报错不发残缺 prompt。"""
    text = template
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    if "{{" in text:
        leftover = text[text.index("{{"): text.index("{{") + 40]
        raise RuntimeError(f"prompt 渲染后仍有未解析占位符：{leftover!r}")
    return text


def format_fact_pool(fact_pool):
    lines = []
    for f in fact_pool:
        line = f"- {f['fact_id']}：值={json.dumps(f['value'], ensure_ascii=False)}"
        if f.get("unit"):
            line += f"，单位={f['unit']}"
        if f.get("status"):
            line += f"，状态={f['status']}"
        lines.append(line)
    return "\n".join(lines) if lines else "（事实池为空）"


def format_rule_pool(rule_pool):
    lines = []
    for r in rule_pool:
        lines.append(
            f"- {r.get('rule_id')}（v{r.get('version')}，{r.get('effect')}，scope={r.get('scope')}，"
            f"target={r.get('target_path')}）：{r.get('statement')}"
        )
    return "\n".join(lines) if lines else "（无 ACTIVE 规则）"


# ============================ 二、模型输出的确定性校验与装配 ============================

def _require_str(obj, key, where):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"{where} 缺少非空字符串字段 {key!r}（模型输出不合形，不兜底不补写）")
    return value


def collect_model_referenced_ids(step1_out, candidates_out, step3_out):
    """收齐模型三步引用的全部池 ID（FACT/RULE），供池内校验与 Trace 物化。"""
    fact_ids, rule_ids = [], []

    def _add(target, values):
        for v in values or []:
            if isinstance(v, str) and v not in target:
                target.append(v)

    for c in step1_out.get("conflicts") or []:
        _add(fact_ids, c.get("referenced_fact_ids"))
        _add(rule_ids, c.get("referenced_rule_ids"))
    for cand in candidates_out:
        _add(fact_ids, cand.get("referenced_fact_ids"))
        _add(rule_ids, cand.get("referenced_rule_ids"))
        for pr in cand.get("product_roles") or []:
            _add(fact_ids, pr.get("referenced_fact_ids"))
        for mj in cand.get("model_judgments") or []:
            _add_mixed(fact_ids, rule_ids, mj.get("supporting_ids"))
        for fit_key in ("brand_fit", "audience_fit", "business_alignment", "production_feasibility"):
            _add_mixed(fact_ids, rule_ids, (cand.get(fit_key) or {}).get("referenced_ids"))
        for risk in cand.get("risks") or []:
            _add_mixed(fact_ids, rule_ids, risk.get("referenced_ids"))
    for t in step3_out.get("comparative_tradeoffs") or []:
        _add_mixed(fact_ids, rule_ids, t.get("referenced_ids"))
    rec = step3_out.get("system_recommendation") or {}
    _add_mixed(fact_ids, rule_ids, rec.get("supporting_ids"))
    return fact_ids, rule_ids


def _add_mixed(fact_ids, rule_ids, values):
    """按前缀分流混合 ID 清单（FACT: 前缀进事实组，其余按规则 ID 处理；池内校验在 trace 层）。"""
    from .config import FACT_ID_PREFIX
    for v in values or []:
        if not isinstance(v, str):
            continue
        if v.startswith(FACT_ID_PREFIX):
            if v not in fact_ids:
                fact_ids.append(v)
        else:
            if v not in rule_ids:
                rule_ids.append(v)


def assert_candidate_ids_unique(candidates_out):
    """候选身份硬闸：candidate_id 非空且两两不同，违规当场报错（退出码 2，零半成品）。

    对抗审查抓获的 blocker：重号时按 id 建 dict 的索引后写覆盖前写——第一个候选会挂上
    别的候选的假设与判断（张冠李戴比缺失更危险），且 D1-D11 全绿。唯一性此前只由 prompt
    一句「顺序编号」维持，正是 C.3 红线说的 Prompt 套壳形态；此闸把它焊回代码。
    返回 id 清单（保持原序）。"""
    ids = []
    for cand in candidates_out:
        cid = cand.get("candidate_id")
        if not isinstance(cid, str) or not cid.strip():
            raise RuntimeError("存在 candidate_id 为空的候选（模型输出不合形，不兜底）")
        ids.append(cid)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise RuntimeError(f"candidate_id 重号 {dupes}：候选身份失去唯一落点，组不出合法候选集（不产半成品）")
    return ids


def build_assumption_entries(candidates_out):
    """把模型显式假设物化为 ASSUMPTION TraceEntry（A.9.2：必须指明缺失项）。

    返回 (entries, per_candidate_refs)——per_candidate_refs **按位置下标**对齐
    candidates_out（不按 candidate_id 建 dict：位置索引即使闸外重号也不会错配）。"""
    entries, per_candidate = [], []
    counter = 0
    for cand in candidates_out:
        refs = []
        for a in cand.get("assumptions") or []:
            statement = _require_str(a, "statement", f"候选 {cand.get('candidate_id')} 的 assumption")
            missing_field = _require_str(a, "missing_field", f"候选 {cand.get('candidate_id')} 的 assumption")
            counter += 1
            trace_id = f"{ASSUMPTION_ID_PREFIX}{counter}"
            entries.append({
                "trace_id": trace_id,
                "trace_type": "ASSUMPTION",
                "statement": f"{statement}（缺失项：{missing_field}）",
                "target_paths": ["candidate_options"],
            })
            refs.append(trace_id)
        per_candidate.append(refs)
    return entries, per_candidate


def build_model_judgment_entries(candidates_out, step3_out, surviving_ids):
    """把模型判断物化为 MODEL_JUDGMENT TraceEntry（A.9.2：必须有支撑 Trace）。

    只对**存活候选**建条目（本函数的输入即已按存活过滤）；推荐条目只在推荐指向存活候选时
    才建——被拦/不存在候选的推荐不建条目，防「背书被拦候选的判断」残留成孤儿 Trace
    （对抗审查抓获后收敛；孤儿另有 D4 判红兜底）。
    返回 (entries, per_candidate_refs 按位置下标, recommendation_trace_ref, dropped_note)。"""
    entries, per_candidate = [], []
    counter = 0
    for cand in candidates_out:
        refs = []
        for mj in cand.get("model_judgments") or []:
            statement = _require_str(mj, "statement", f"候选 {cand.get('candidate_id')} 的 model_judgment")
            supports = [s for s in (mj.get("supporting_ids") or []) if isinstance(s, str)]
            counter += 1
            trace_id = f"{MODEL_JUDGMENT_ID_PREFIX}{counter}"
            entries.append({
                "trace_id": trace_id,
                "trace_type": "MODEL_JUDGMENT",
                "statement": statement,
                "supporting_trace_refs": supports,
                "target_paths": ["candidate_options"],
            })
            refs.append(trace_id)
        per_candidate.append(refs)

    rec = step3_out.get("system_recommendation") or {}
    rec_trace_ref = None
    dropped_note = None
    if rec.get("candidate_id") is not None:
        if rec.get("candidate_id") in surviving_ids:
            statement = _require_str(rec, "judgment_statement", "system_recommendation")
            supports = [s for s in (rec.get("supporting_ids") or []) if isinstance(s, str)]
            counter += 1
            rec_trace_ref = f"{MODEL_JUDGMENT_ID_PREFIX}{counter}"
            entries.append({
                "trace_id": rec_trace_ref,
                "trace_type": "MODEL_JUDGMENT",
                "statement": statement,
                "supporting_trace_refs": supports,
                "target_paths": ["system_recommendation"],
            })
        else:
            dropped_note = (f"模型推荐 {rec.get('candidate_id')!r} 不在存活候选内，推荐清空且不建判断条目"
                            "（不背书被拦或不存在的候选）")
    return entries, per_candidate, rec_trace_ref, dropped_note


def _mode_limiting_line(llm_mode):
    """limiting_factors 兜底行按真实运行模式生成（对抗审查抓获：硬写「离线回放」在
    --live 下是产物内的假陈述）。"""
    if llm_mode == "live":
        return "无机器面缺口——但语义质量属 L2/L3 判分面，机器校验不背书（本次为 live 真实调用）"
    return "无机器面缺口——但本次为离线回放（replay），非真实模型行为证据"


def _candidate_confidence(cand, has_assumptions, products_in_pool, llm_mode):
    """候选级置信度：确定性只降不升（A.1.4）。模型不报级别——级别由装配侧按证据状态推。

    basis 只写**实际核验过**的事实（对抗审查抓获：无条件宣称「引用均来自快照物化池」在
    池外商品场景是产物内的假陈述）：FACT/RULE 引用由 trace 层 fail-loud 保证（池外引用
    根本组装不出产物，能出 bundle 即已核验）；商品引用在装配现场逐一比对商品池。"""
    level = "HIGH"
    basis = ["FACT/RULE 引用经 trace 层池内校验（fail-loud，池外引用组装不出产物）"]
    limiting = []
    if products_in_pool:
        basis.append("商品引用已在装配时逐一核验在快照商品池")
    else:
        level = "MEDIUM"
        basis.append("降级留痕：存在池外商品引用（postcheck D9 判定面详列）")
        limiting.append("商品引用未全部通过池内核验")
    unknown_fits = [k for k in ("brand_fit", "audience_fit", "business_alignment", "production_feasibility")
                    if (cand.get(k) or {}).get("assessment") == "UNKNOWN"]
    if unknown_fits:
        level = "MEDIUM"
        basis.append(f"降级留痕：适配维度 {unknown_fits} 为 UNKNOWN")
        limiting.extend(f"{k} 证据不足" for k in unknown_fits)
    if has_assumptions:
        level = "MEDIUM"
        basis.append("降级留痕：本候选含显式 ASSUMPTION")
        limiting.append("存在未验证工作假设")
    if not limiting:
        limiting.append(_mode_limiting_line(llm_mode))
    return {"level": level, "basis": basis, "limiting_factors": limiting}


def assemble_candidate(cand, brand_id, product_ids, engine_results,
                       assumption_refs, judgment_refs, llm_mode):
    """把模型候选装配成 A.6.3 BusinessCandidate（字段名逐字照抄，不增不减）。

    role 枚举违规当场报错（组不出合法候选）；product_id 池外**不在这层拦**——
    照装进 product_ref，由 postcheck D9 判红留取证材料（BD_FACT_FABRICATION 的结构面）；
    池外事实同步压低本候选置信度并留痕（不写无检测器的确定性表述）。
    """
    candidate_id = _require_str(cand, "candidate_id", "候选")
    roles = []
    for pr in cand.get("product_roles") or []:
        role = pr.get("role")
        if role not in PRODUCT_ROLES:
            raise RuntimeError(
                f"候选 {candidate_id} 的商品角色 {role!r} 不在 A.2.6 五值枚举内（模型不得自造角色）"
            )
        roles.append({
            "product_ref": {
                "object_type": "ProductFacts",
                "object_id": str(pr.get("product_id")),
                # M0 夹具商品无版本字段，缺省取 1（口径与 kernel/intent 对扁平夹具一致，已登记 UPSTREAM_GAPS）
                "version": 1,
                "brand_id": brand_id,
            },
            "role": role,
            "rationale": _require_str(pr, "rationale", f"候选 {candidate_id} 的 product_role"),
            "trace_refs": [s for s in (pr.get("referenced_fact_ids") or []) if isinstance(s, str)],
        })
    if not roles:
        raise RuntimeError(f"候选 {candidate_id} 无 product_roles（A.6.3 要求至少一个商品角色）")

    def _fit(key):
        fit = cand.get(key) or {}
        assessment = fit.get("assessment")
        if assessment not in FIT_ASSESSMENTS:
            raise RuntimeError(f"候选 {candidate_id} 的 {key}.assessment={assessment!r} 不在三值枚举内")
        return {
            "assessment": assessment,
            "rationale": _require_str(fit, "rationale", f"候选 {candidate_id} 的 {key}"),
            "trace_refs": [s for s in (fit.get("referenced_ids") or []) if isinstance(s, str)],
        }

    risks = []
    for r in cand.get("risks") or []:
        risks.append({
            "condition": _require_str(r, "condition", f"候选 {candidate_id} 的 risk"),
            "possible_impact": _require_str(r, "possible_impact", f"候选 {candidate_id} 的 risk"),
            "mitigation": r.get("mitigation") if isinstance(r.get("mitigation"), str) else None,
            "trace_refs": [s for s in (r.get("referenced_ids") or []) if isinstance(s, str)],
        })

    has_assumptions = bool(assumption_refs)
    products_in_pool = all(r["product_ref"]["object_id"] in product_ids for r in roles)
    return {
        "candidate_id": candidate_id,
        "title": _require_str(cand, "title", "候选"),
        "strategy": _require_str(cand, "strategy", "候选"),
        "product_roles": roles,
        "supporting_fact_refs": [s for s in (cand.get("referenced_fact_ids") or []) if isinstance(s, str)],
        "applied_rule_refs": [s for s in (cand.get("referenced_rule_ids") or []) if isinstance(s, str)],
        "assumption_refs": assumption_refs,
        "model_judgment_refs": judgment_refs,
        "brand_fit": _fit("brand_fit"),
        "audience_fit": _fit("audience_fit"),
        "business_alignment": _fit("business_alignment"),
        "production_feasibility": _fit("production_feasibility"),
        "risks": risks,
        "why_this_option": _require_str(cand, "why_this_option", "候选"),
        "why_not_primary_alternative": _require_str(cand, "why_not_primary_alternative", "候选"),
        "hard_rule_results": engine_results,
        "confidence": _candidate_confidence(cand, has_assumptions, products_in_pool, llm_mode),
    }


def compute_count_status(surviving_count, blocked_diagnostics, gate_notes):
    """按 A.6.2/A.6.3 三态确定性计算候选数量状态（不问模型）。>3 属上游步骤违约，当场报错。"""
    if surviving_count > CANDIDATE_TARGET_COUNT:
        raise RuntimeError(
            f"存活候选 {surviving_count} 个，超出 A.6.3 目标上限 {CANDIDATE_TARGET_COUNT}（模型违反 2-3 约束，不静默截断）"
        )
    if surviving_count == CANDIDATE_TARGET_COUNT:
        return COUNT_STATUS_TARGET_THREE, None
    blocked_notes = [
        f"被拦路径「{d['candidate_summary']}」：" + "；".join(
            f"{r['rule_ref']['object_id']}（{r['explanation']}）" for r in d["blocking_rule_results"]
        )
        for d in blocked_diagnostics
    ]
    if surviving_count == 2:
        if blocked_notes:
            explanation = "第三方向受规则限制：" + " ／ ".join(blocked_notes) + "；其余事实仅支撑两个实质差异方向"
        else:
            explanation = "模型仅提出两个实质差异候选，且无机器确认的被拦路径；受限原因属人工判分面，此处如实登记"
        gate_notes.append(f"候选数量降级 DEGRADED_TWO：{explanation}")
        return COUNT_STATUS_DEGRADED_TWO, explanation
    explanation = ("有效候选不足两个" + ("；" + " ／ ".join(blocked_notes) if blocked_notes else "")
                   + "。按 A.6.3 不补造候选，返回阻断诊断，不得进入 DECISION_READY")
    gate_notes.append(f"候选数量阻断 BLOCKED_FEWER_THAN_TWO：{explanation}")
    return COUNT_STATUS_BLOCKED, explanation


def bundle_confidence(candidates, count_status, unevaluated_rules, gate_notes, llm_mode):
    """bundle 级置信度：确定性只降不升（A.1.4），每次降级都留痕进 basis。
    basis 只写实际核验过的事实（同 _candidate_confidence 的口径收敛）。"""
    level = "HIGH"
    basis = ["FACT/RULE 引用经 trace 层池内校验；商品引用核验结果见各候选 basis 与 postcheck D9"]
    limiting = []
    if any(c["confidence"]["level"] != "HIGH" for c in candidates):
        level = "MEDIUM"
        basis.append("降级留痕：存在候选级置信度低于 HIGH（假设/UNKNOWN 适配）")
        limiting.append("候选级证据存在缺口（详见各候选 limiting_factors）")
    if count_status != COUNT_STATUS_TARGET_THREE:
        level = "MEDIUM" if level == "HIGH" else level
        basis.append(f"降级留痕：candidate_count_status={count_status}")
        limiting.append("候选空间受限")
    if unevaluated_rules:
        level = "LOW"
        basis.append(f"降级留痕：{len(unevaluated_rules)} 条规则无谓词可评（fail-closed）")
        limiting.append("存在未能机器评估的 ACTIVE 规则")
    basis.extend(f"闸留痕：{n}" for n in gate_notes)
    if not limiting:
        limiting.append(_mode_limiting_line(llm_mode))
    return {"level": level, "basis": basis, "limiting_factors": limiting}


def build_artifact_envelope(plan, snapshot, run_id, created_at):
    """按 common.defs.ArtifactEnvelope 逐字段组装（照抄形状，不臆造字段）。"""
    brand_id = snapshot.get("brand_id")
    snapshot_id = snapshot.get("snapshot_id")
    if not brand_id or not snapshot_id:
        raise RuntimeError("快照缺 brand_id 或 snapshot_id，无法组装 ArtifactEnvelope（A.1.3）")
    upstream = plan.get("artifact") or {}
    return {
        "artifact_id": f"BDB-{run_id}",
        "artifact_type": ARTIFACT_TYPE,
        "version": 1,
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "brand_id": brand_id,
        # 沿用上游 plan 的 task_id（同一 Task 链条）；上游没有时按运行号派生占位（待集成，不编真值）
        "task_id": upstream.get("task_id") or f"TASK-{run_id}",
        "context_snapshot_ref": {
            "object_type": "ContextSnapshot",
            "object_id": snapshot_id,
            "version": int(snapshot.get("version", 1)),
            "brand_id": brand_id,
        },
        "source_run_id": run_id,
        "parent_references": [{
            "object_ref": {
                "object_type": "IntentExecutionPlan",
                "object_id": upstream.get("artifact_id"),
                "version": int(upstream.get("version", 1)),
                "brand_id": brand_id,
            },
            "relation": "DERIVED_FROM",
        }],
        "review_status": "PENDING",   # 系统产出一律待人工复核（PASS 只能由人判，C.5）
        "created_at": created_at,
        "created_by": "SYSTEM",
    }


def artifact_self_ref(artifact):
    return {
        "object_type": "BusinessDecisionBundle",
        "object_id": artifact["artifact_id"],
        "version": artifact["version"],
        "brand_id": artifact["brand_id"],
    }


# ============================ 三、编排 ============================

def run(args):
    """一次完整编排。返回 (bundle, report)；异常一律向上抛（由 main 归到退出码 2）。"""
    plan = preprocess.load_plan(args.plan)
    snapshot = preprocess.load_snapshot(args.snapshot)   # A.4.3 引用式 → kernel/facts 内联兼容视图
    fact_pool = preprocess.materialize_fact_pool(snapshot)
    # 规则池唯一来源 = 快照视图 hard_rules（active_rule_refs 解引用产物，快照钉定规则集）。
    # 品牌过滤 + ACTIVE 过滤在**进 prompt 之前**、且只在此处过滤一次——prompt 渲染 /
    # 规则评估 / 请求装配 / D6 覆盖核验消费同一份池（非 ACTIVE 规则以「已启用」名义被模型
    # 读到，是对抗审查抓获后封死的口径分叉点；kernel/facts 谓词已保证引用规则 ACTIVE，
    # 此处双保险属幂等）
    rule_pool = preprocess.filter_active_rules(
        preprocess.filter_rule_pool_by_brand(preprocess.rule_pool_from_snapshot(snapshot), snapshot.get("brand_id"))
    )
    product_ids = preprocess.list_product_ids(snapshot)
    llm_mode = "live" if args.live else "replay"

    # --- 输入闸（生成前）：任何 FAIL 都不进入候选生成 ---
    input_gates = preprocess.check_input_gates(plan, snapshot, rule_pool)
    gate_failures = [g for g in input_gates if g["verdict"] != "OK"]
    if gate_failures:
        detail = "；".join(f"{g['id']} {g['detail']}" for g in gate_failures)
        raise RuntimeError(f"输入闸不过，不进入候选生成（A.5.2/A.1.3/OD-03）：{detail}")
    request = preprocess.build_request(plan, snapshot, rule_pool)

    # --- 三步 LLM（C.3 BD 分步裁决；replay 模式逐步各带各的夹具）---
    business_goal = str(plan.get("business_goal"))
    intent_summary = str(plan.get("intent_summary") or "")
    fact_pool_text = format_fact_pool(fact_pool)
    rule_pool_text = format_rule_pool(rule_pool)

    def _step(path_const, replay_path, mapping, label):
        template, version = load_prompt(path_const)
        prompt_text = render_prompt(template, mapping)
        mode = "live" if args.live else f"replay:{replay_path}"
        print(f"[decision.runner] {label} prompt_version={version} llm_mode={mode.split(':')[0]}", file=sys.stderr)
        return llm.parse_model_json(llm.call_llm(prompt_text, mode)), version

    step1_out, v1 = _step(PROMPT_STEP1_PATH, args.replay_step1, {
        "BUSINESS_GOAL": business_goal,
        "INTENT_SUMMARY": intent_summary,
        "FACT_POOL": fact_pool_text,
        "RULE_POOL": rule_pool_text,
    }, "step1")
    conflicts_text = json.dumps(step1_out.get("conflicts") or [], ensure_ascii=False, indent=2)

    step2_out, v2 = _step(PROMPT_STEP2_PATH, args.replay_step2, {
        "BUSINESS_GOAL": business_goal,
        "INTENT_SUMMARY": intent_summary,
        "FACT_POOL": fact_pool_text,
        "RULE_POOL": rule_pool_text,
        "CONFLICTS": conflicts_text,
        "PRODUCT_ROLE_ENUM": " / ".join(PRODUCT_ROLES),
        "FIT_ENUM": " / ".join(FIT_ASSESSMENTS),
    }, "step2")
    candidates_out = step2_out.get("candidates") or []
    if not isinstance(candidates_out, list) or not candidates_out:
        raise RuntimeError("step2 未产出候选清单（candidates 缺失或为空），不进入规则评估")
    assert_candidate_ids_unique(candidates_out)

    # --- 确定性规则评估与 BLOCK 隔离（G.2 第 4 条①：逐规则 HardRuleResult 进 Run 证据）。
    # 时序钉死在 step3 **之前**：step3 prompt 明写「候选清单……已过确定性规则评估」，被拦
    # 候选不得进入取舍步（否则其取舍引用/假设/判断全部要事后擦除——对抗审查抓获的
    # 「prompt 自述与代码时序相反」缺口，改代码顺序而不是改 prompt 陈述）---
    forbidden_groups, lexicon_note = rules_engine.load_forbidden_groups()
    gate_notes = [f"禁用词表装载：{lexicon_note}"]
    rule_evaluations = []
    surviving_raw, blocked_diagnostics = [], []
    all_unevaluated = []

    for cand in candidates_out:
        results, unevaluated = rules_engine.evaluate_candidate(cand, rule_pool, forbidden_groups)
        all_unevaluated.extend(unevaluated)
        rule_evaluations.append({"target": f"candidate:{cand.get('candidate_id')}", "results": results,
                                 "unevaluated": [{"rule_id": r, "note": n} for r, n in unevaluated]})
        blocks = [r for r in results if r["result"] == HARD_RULE_BLOCK]
        if blocks:
            # BLOCK 的候选不得进入下一人工节点（A.9.1）：不进取舍步、不建其假设/判断条目
            gate_notes.append(f"候选 {cand.get('candidate_id')} 被硬规则拦截，移入阻断诊断（不进入取舍步）")
            blocked_diagnostics.append({
                "candidate_summary": _require_str(cand, "title", "被拦候选"),
                "blocking_rule_results": blocks,
            })
        else:
            surviving_raw.append((cand, results))

    for path in step2_out.get("ruled_out_paths") or []:
        summary = _require_str(path, "summary", "ruled_out_path")
        pseudo = {"strategy": summary}
        results, unevaluated = rules_engine.evaluate_candidate(pseudo, rule_pool, forbidden_groups)
        all_unevaluated.extend(unevaluated)
        blocks = [r for r in results if r["result"] == HARD_RULE_BLOCK]
        rule_evaluations.append({"target": f"ruled_out_path:{summary}", "results": results,
                                 "unevaluated": [{"rule_id": r, "note": n} for r, n in unevaluated]})
        if blocks:
            blocked_diagnostics.append({"candidate_summary": summary, "blocking_rule_results": blocks})
        else:
            # 模型自称被规则排除但机器谓词未命中：不发 BLOCK（不编造确定性结论），如实留痕
            gate_notes.append(f"模型声称被排除的路径「{summary}」未获机器谓词确认，不入阻断诊断，只留痕")

    surviving_cands = [cand for cand, _results in surviving_raw]
    surviving_ids = [cand.get("candidate_id") for cand in surviving_cands]
    if not surviving_cands:
        # 全军覆没也要出诊断产物（A.6.3：不补造候选，返回阻断诊断）——但取舍步没有对象，跳过
        step3_out, v3 = {"comparative_tradeoffs": [], "system_recommendation": {"candidate_id": None}}, "（跳过）"
        gate_notes.append("存活候选为零，取舍步跳过（无对象可比），产出阻断诊断 bundle")
    else:
        step3_out, v3 = _step(PROMPT_STEP3_PATH, args.replay_step3, {
            "BUSINESS_GOAL": business_goal,
            "CONFLICTS": conflicts_text,
            "CANDIDATES": json.dumps(surviving_cands, ensure_ascii=False, indent=2),
        }, "step3")

    # --- 假设/判断物化（只对存活候选；推荐只在指向存活候选时建条目）---
    assumption_entries, assumption_refs_by_pos = build_assumption_entries(surviving_cands)
    judgment_entries, judgment_refs_by_pos, rec_trace_ref, rec_dropped_note = \
        build_model_judgment_entries(surviving_cands, step3_out, surviving_ids)
    if rec_dropped_note:
        gate_notes.append(rec_dropped_note)

    surviving = [
        assemble_candidate(cand, snapshot.get("brand_id"), product_ids, results,
                           assumption_refs_by_pos[i], judgment_refs_by_pos[i], llm_mode)
        for i, (cand, results) in enumerate(surviving_raw)
    ]

    count_status, count_explanation = compute_count_status(len(surviving), blocked_diagnostics, gate_notes)

    rec = step3_out.get("system_recommendation") or {}
    rec_candidate_id = rec.get("candidate_id") if rec_trace_ref is not None else None
    system_recommendation = {"candidate_id": rec_candidate_id, "judgment_trace_ref": rec_trace_ref}

    # --- Trace 物化（四类分离，池内校验在 trace 层 fail-loud；只物化存活候选的引用）---
    referenced_fact_ids, referenced_rule_ids = collect_model_referenced_ids(step1_out, surviving_cands, step3_out)
    run_id = args.run_id
    created_at = args.created_at
    if not run_id:
        run_id = "RUN-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        print(f"[decision.runner] 未注入 --run-id，取时钟生成 {run_id}", file=sys.stderr)
    if not created_at:
        created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print("[decision.runner] 未注入 --created-at，取当前时钟", file=sys.stderr)

    artifact = build_artifact_envelope(plan, snapshot, run_id, created_at)
    bundle_trace = trace.build_trace_bundle(
        fact_pool, rule_pool, referenced_fact_ids, referenced_rule_ids,
        assumption_entries, judgment_entries,
        brand_id=artifact["brand_id"], target_artifact_ref=artifact_self_ref(artifact),
    )

    # --- 按 A.6.2 字段顺序装配（字段名逐字照抄，不增不减）---
    recognized_conflicts = []
    for c in step1_out.get("conflicts") or []:
        recognized_conflicts.append({
            "conflict_id": _require_str(c, "conflict_id", "conflict"),
            "description": _require_str(c, "description", "conflict"),
            "side_a": _require_str(c, "side_a", "conflict"),
            "side_b": _require_str(c, "side_b", "conflict"),
            "trace_refs": [s for s in ((c.get("referenced_fact_ids") or []) + (c.get("referenced_rule_ids") or []))
                           if isinstance(s, str)],
        })
    comparative_tradeoffs = []
    for t in step3_out.get("comparative_tradeoffs") or []:
        comparative_tradeoffs.append({
            "candidate_refs": [s for s in (t.get("candidate_refs") or []) if isinstance(s, str)],
            "tradeoff": _require_str(t, "tradeoff", "comparative_tradeoff"),
            "trace_refs": [s for s in (t.get("referenced_ids") or []) if isinstance(s, str)],
        })

    confidence = bundle_confidence(surviving, count_status, all_unevaluated, gate_notes, llm_mode)
    for note in gate_notes:
        print(f"[decision.runner] 闸: {note}", file=sys.stderr)

    bundle = {
        "artifact": artifact,
        "business_problem": _require_str(step1_out, "business_problem", "step1 输出"),
        "recognized_conflicts": recognized_conflicts,
        "candidate_options": surviving,
        "comparative_tradeoffs": comparative_tradeoffs,
        "candidate_count_status": count_status,
        "candidate_count_explanation": count_explanation,
        "system_recommendation": system_recommendation,
        "human_selection_required": True,   # A.6.2 固定值：确定性装配，不问模型，机器不替 Founder 选方案
        "blocked_candidate_diagnostics": blocked_diagnostics,
        "confidence": confidence,
        "trace_bundle": bundle_trace,
    }

    # --- 确定性后校验（Preflight，G.2 第 4 条双阶段命名）---
    check_report = postcheck.preflight(bundle, {
        "schema_path": SCHEMA_BUSINESS_DECISION_BUNDLE,
        "fact_pool": fact_pool,
        "rule_pool": rule_pool,
        "snapshot": snapshot,
        "product_ids": product_ids,
    })

    report = {
        "segment": SEGMENT_MARK,
        "stage": check_report.get("stage"),
        "llm_mode": llm_mode,
        "prompt_versions": {"step1": v1, "step2": v2, "step3": v3},
        "request": request,
        "input_gates": input_gates,
        "rule_evaluations": rule_evaluations,
        "unevaluated_rules": [{"rule_id": r, "note": n} for r, n in all_unevaluated],
        "machine_human_register": rules_engine.machine_human_register(rule_pool),
        "gate_notes": gate_notes,
        "checks": check_report.get("checks"),
        "overall": check_report.get("overall"),
    }
    return bundle, report


# ============================ 四、CLI ============================

def parse_args(argv=None):
    # 说明文本里**不得出现**结论标记串（--help 也会打印，按子串判绿的调用方会被骗过）
    parser = argparse.ArgumentParser(
        prog="python3 -m kernel.decision.runner",
        description="Decision 模块编排：输入闸 → 三步 LLM → 确定性规则评估与装配 → 后校验。"
                    "退出码 0=全过 / 1=后校验判失败 / 2=没跑完",
    )
    parser.add_argument("--plan", required=True, help="冻结 IntentExecutionPlan JSON 路径（上游输入）")
    parser.add_argument("--snapshot", required=True, help="Context Snapshot JSON 路径")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--live", action="store_true",
                        help="调用 DashScope（key 只取环境变量 DASHSCOPE_API_KEY，零重试，三步各一次）")
    source.add_argument("--replay-step1", metavar="FIXTURE", help="离线：step1 的录制/手写模型回复")
    parser.add_argument("--replay-step2", metavar="FIXTURE", help="离线：step2 的录制/手写模型回复")
    parser.add_argument("--replay-step3", metavar="FIXTURE", help="离线：step3 的录制/手写模型回复")
    parser.add_argument("--out", required=True, help="BusinessDecisionBundle 输出路径")
    parser.add_argument("--report", default=None, help="运行证据报告输出路径（含逐规则评估与质检单）")
    parser.add_argument("--run-id", default=None, help="确定性注入运行号（离线自测用；不给则取时钟）")
    parser.add_argument("--created-at", default=None, help="确定性注入 created_at（离线自测用；不给则取时钟）")
    args = parser.parse_args(argv)
    if not args.live:
        missing = [n for n in ("replay_step1", "replay_step2", "replay_step3") if not getattr(args, n)]
        if missing:
            parser.error(f"replay 模式必须同时给出三步夹具，缺 {missing}")
    return args


def _write_json(path, payload):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    args = parse_args(argv)
    try:
        bundle, report = run(args)
    except Exception as e:   # 没跑完 ≠ 通过：exit 2，且不产出半成品 bundle
        print(f"[decision.runner] 运行失败（{type(e).__name__}）：{e}", file=sys.stderr)
        return 2
    _write_json(args.out, bundle)   # 判红也照写盘：失败的 bundle 是取证材料
    if args.report:
        _write_json(args.report, report)
    failed = [c for c in report.get("checks", []) if c.get("verdict") == "FAIL"]
    unknown = [c for c in report.get("checks", []) if c.get("verdict") == "UNKNOWN"]
    print(
        f"candidate_count_status={bundle['candidate_count_status']} "
        f"candidates={len(bundle['candidate_options'])} blocked={len(bundle['blocked_candidate_diagnostics'])} "
        f"conflicts={len(bundle['recognized_conflicts'])} confidence={bundle['confidence']['level']}"
    )
    for check in failed + unknown:
        print(f"  {check.get('verdict')} {check.get('id')} {check.get('item')}: {check.get('detail')}")
    # 结论标记串只出现在这一行真实结论里
    print("PREFLIGHT_OK" if report.get("overall") == "OK" else "PREFLIGHT_FAIL")
    return 0 if report.get("overall") == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
