#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 资产④（规则判定面）：确定性硬规则引擎。

【M2-EP01 提前段·非正式证据】

落地依据 = G.2 第 4 条「确定性约束验证器落地纪律」四点（Founder 已裁决吸收，本模块照办）：
  ① 逐规则 HardRuleResult 清单存进每次 Run 证据（runner 落 report.rule_evaluations）；
  ② **不自造约束 DSL**：只用 JSON Schema + 词表/正则 + Python 谓词三件套；
  ③ 双阶段报告命名沿用 Preflight（生成前，落 A.6.2 既有语义）；
  ④ 规则调度信息（谓词映射 / 词表分组归属 / 机器可查面 / 仅人可查面）放**本实现层映射表**
     `RULE_CHECK_TABLE`，**不扩 A.9.1 RuleRecord 冻结字段**。

红线（G.2 第 4 条原文）：质检单逐条标注"机器可查/仅人可查"，禁止全局合规图章掩盖语义盲区。
A.9.1 HardRuleResult 只有 PASS/BLOCK 两值、没有 UNKNOWN——所以：
  · PASS 的语义**只是**"机器谓词在声明的词面范围内零命中"，explanation 逐条写明这一点；
  · 谓词覆盖不到的语义面登记在 `machine_human_register()` 的 human_scope 列，属 L3 人工
    判分面（C.5），**不发结果不算过**；
  · 以下三种情形一律**不发结果**（fail-closed，由 postcheck D6 的覆盖核验判红——想让规则
    过闸必须先补齐机器判定条件，堵"引擎默认全过"的假绿通道）：
      a) 注册表里有规则但本映射表无谓词；
      b) 词表分组解析出 0 词条（空词表 ≠ 零命中，对齐 checks.py 三态口径）；
      c) 规则 target_path 在被测对象上解析不到字段、或解析出的文本面为空
         （空文本 ≠ 零命中——对抗审查抓获的 fail-open 通道，runtime_verified 后封死）。

**词表分组归属**（对抗审查抓获「全量词表 = 全局图章」后收敛）：
  forbidden_lexicon.yaml 分组即语义归属——low_price_selling / false_scarcity 两组源自
  BD-D01 冻结 forbidden_expression=LOW_PRICE_SELLING（词表头注 verbatim「低价/甩卖/虚假稀缺」），
  归 R-BDD01-001；brand_tone 组源自 OQ-BUILD-03 品牌调性禁词，归品牌禁语规则 R-FB01-001
  （该规则本就以整份词表为运营真源，全组）。`高级感` 只会以 R-FB01-001 名义 BLOCK，
  不再冒充「低价叫卖」证据——总拦截面不变，证据归属变准。

**BLOCK explanation 不回写命中词原文**（对抗审查抓获两条连锁缺陷后收敛）：
  回写原词会让取证文本自带禁用表达——postcheck D7 扫全产物必假红（正确拦截的运行反而
  PREFLIGHT_FAIL），送考卷时 A7 全文本扫描同样命中。改写为「组名 + 命中处数 + 目标字段」，
  可复核（组与字段定位到词表与产物位置）但不复述；词条原文不落盘。

词表边界：唯一运营真源仍是 acceptance/detectors/forbidden_lexicon.yaml（只读，**对齐而非
复用** checks.py，不 import 考卷区代码）。促销机制词表 `PROMO_PATH_TERMS` 是 R-BDD01-002
的实现层检测辅助（纪律④允许的调度信息），不判品牌禁语、不是第二份运营词表。
"""

import os

try:
    import yaml
except ImportError as e:
    raise RuntimeError("需要 PyYAML（requirements.txt 已登记）") from e

from .config import FORBIDDEN_LEXICON_PATH, HARD_RULE_BLOCK, HARD_RULE_PASS

# R-BDD01-002「促销让利路径」的词面谓词表（实现层调度信息，G.2 第 4 条④）。
PROMO_PATH_TERMS = (
    "促销", "折扣", "打折", "让利", "降价", "特价", "满减", "买赠", "限时优惠", "限时折扣", "低价",
)

# 实现层映射表：rule_id → 谓词、词表分组归属与两栏质检单（机器可查 / 仅人可查）。
# lexicon_groups=None 表示全组。新增 RuleRecord 而不登记本表 = 该规则不产生结果
# （fail-closed，postcheck D6 判红）。
RULE_CHECK_TABLE = {
    "R-BDD01-001": {
        "predicate": "forbidden_lexicon",
        "lexicon_groups": ("low_price_selling", "false_scarcity"),
        "machine_scope": "禁用词表 low_price_selling + false_scarcity 两组词面扫描零命中",
        "human_scope": "非词面的低价叫卖语义变体（改写、暗示、比价话术）——L3 人工判分面",
    },
    "R-FB01-001": {
        "predicate": "forbidden_lexicon",
        "lexicon_groups": None,
        "machine_scope": "禁用词表（forbidden_lexicon.yaml 全组）词面扫描零命中",
        "human_scope": "词表外的品牌禁语语义变体——L3 人工判分面",
    },
    "R-BDD01-002": {
        "predicate": "promo_path_lexicon",
        "lexicon_groups": None,
        "machine_scope": "促销机制词面扫描（PROMO_PATH_TERMS）零命中",
        "human_scope": "非词面表达的促销让利路径判定——L3 人工判分面",
    },
}


def load_forbidden_groups(path=None):
    """读禁用词表并**保留分组结构**。返回 ({group: [terms]}, note)；顶层不是映射或
    全部组为空时返回空 dict + 原因——与 checks.py::forbidden_expression 的三态口径对齐。"""
    target = path or FORBIDDEN_LEXICON_PATH
    if not os.path.exists(target):
        return {}, f"词表不存在：{target}"
    with open(target, encoding="utf-8") as f:
        lex = yaml.safe_load(f)
    if not isinstance(lex, dict):
        return {}, f"词表顶层不是映射对象（实得 {type(lex).__name__}）"
    groups = {}
    malformed = []
    for key, value in lex.items():
        if isinstance(value, list):
            terms = [t for t in value if isinstance(t, str) and t.strip()]
            if terms:
                groups[str(key)] = terms
        else:
            malformed.append(str(key))
    total = sum(len(v) for v in groups.values())
    note = f"{len(groups)} 组 {total} 词" + (f"；结构异常键 {malformed} 未参与" if malformed else "")
    return groups, note


def load_forbidden_terms(path=None):
    """全组扁平词表（postcheck D7 的全文本扫描面消费——D7 判的是"产物含任何禁用表达"，
    与规则归属无关，全组正确）。返回 (terms, note)。"""
    groups, note = load_forbidden_groups(path)
    terms = [t for group_terms in groups.values() for t in group_terms]
    return terms, note


def collect_text_fields(node, out=None):
    """深度收集一个结构里的全部字符串叶子（`_` 前缀键为注释约定，跳过）。"""
    if out is None:
        out = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str) and key.startswith("_"):
                continue
            collect_text_fields(value, out)
    elif isinstance(node, list):
        for item in node:
            collect_text_fields(item, out)
    return out


def _scan(texts, terms):
    """词面扫描：返回命中词的有序去重清单（只在引擎内部流转，不落盘原词）。"""
    return sorted({t for txt in texts for t in terms if t in txt})


def hard_rule_result(rule, result, explanation):
    """按 A.9.1 HardRuleResult 形状组装（字段照抄，不增不减；target_ref 非必填不发）。"""
    return {
        "rule_ref": {
            "object_type": "RuleRecord",
            "object_id": rule["rule_id"],
            "version": int(rule.get("version", 1)),
            "brand_id": rule.get("brand_id"),
        },
        "target_path": rule.get("target_path"),
        "result": result,
        "explanation": explanation,
    }


def _forbidden_hits_by_group(texts, groups, wanted):
    """按组扫描。wanted=None 取全组。返回 {group: hit_count}（只计处数，不外传原词）。"""
    out = {}
    for group, terms in groups.items():
        if wanted is not None and group not in wanted:
            continue
        hits = _scan(texts, terms)
        if hits:
            out[group] = len(hits)
    return out


def evaluate_rule_on_texts(rule, texts, forbidden_groups, scope_note="被测对象"):
    """用映射表谓词对一组文本判一条规则。

    返回 (hard_rule_result | None, note)：
      · 命中 → BLOCK（explanation 写组名+处数+扫描面，不回写词条原文）；
      · 零命中 → PASS（explanation 明写"仅词面扫描"，不冒充语义级合规）；
      · 无谓词映射 / 词表组空 / 文本面为空 → None + note（不发结果，无检测器不得判过）。
    """
    entry = RULE_CHECK_TABLE.get(rule.get("rule_id"))
    if entry is None:
        return None, f"规则 {rule.get('rule_id')} 未登记实现层谓词映射，无检测器不发结果（fail-closed）"
    if not texts:
        return None, (f"规则 {rule.get('rule_id')} 在{scope_note}上无可扫描文本"
                      "（target_path 解析不到字段或文本面为空），无从核验，不发结果")
    if entry["predicate"] == "forbidden_lexicon":
        wanted = entry.get("lexicon_groups")
        available = set(forbidden_groups) if wanted is None else set(forbidden_groups) & set(wanted)
        if not available:
            return None, f"禁用词表相关分组为空，规则 {rule.get('rule_id')} 无从核验，不发结果"
        hit_groups = _forbidden_hits_by_group(texts, forbidden_groups, wanted)
        if hit_groups:
            detail = "；".join(f"{g} 组命中 {n} 处" for g, n in sorted(hit_groups.items()))
            return hard_rule_result(
                rule, HARD_RULE_BLOCK,
                f"禁用词表词面命中：{detail}（扫描面：{scope_note}；词条原文不落盘，防取证文本自带禁用表达）",
            ), "命中"
        return hard_rule_result(
            rule, HARD_RULE_PASS,
            f"机器词面扫描零命中（{entry['machine_scope']}；扫描面：{scope_note}）；语义变体属人工判分面",
        ), "零命中"
    if entry["predicate"] == "promo_path_lexicon":
        hits = _scan(texts, PROMO_PATH_TERMS)
        if hits:
            return hard_rule_result(
                rule, HARD_RULE_BLOCK,
                f"促销机制词面命中 {len(hits)} 处（扫描面：{scope_note}；词条原文不落盘）",
            ), "命中"
        return hard_rule_result(
            rule, HARD_RULE_PASS,
            f"机器词面扫描零命中（{entry['machine_scope']}；扫描面：{scope_note}）；非词面促销路径属人工判分面",
        ), "零命中"
    return None, f"谓词 {entry['predicate']!r} 未实现（映射表与引擎脱节，属实现缺陷）"


def evaluate_candidate(candidate, rule_pool, forbidden_groups):
    """对一个候选逐条评估 ACTIVE 规则。

    返回 (results, unevaluated)：results = HardRuleResult 清单；unevaluated = 未能发结果的
    [(rule_id, note)] 清单（进 Run 证据 + postcheck D6 覆盖核验）。
    扫描面：规则 target_path="*" 扫候选全部文本叶子；否则只扫该字段——字段在被测对象上
    **不存在或为空时不发 PASS**（见文件头 fail-closed 口径 c）。
    """
    results, unevaluated = [], []
    for rule in rule_pool:
        if rule.get("status") != "ACTIVE":
            continue
        target = rule.get("target_path")
        if target and target != "*":
            texts = collect_text_fields(candidate.get(target))
            scope_note = f"字段 {target}"
        else:
            texts = collect_text_fields(candidate)
            scope_note = "候选全文本面"
        result, note = evaluate_rule_on_texts(rule, texts, forbidden_groups, scope_note)
        if result is None:
            unevaluated.append((rule.get("rule_id"), note))
        else:
            results.append(result)
    return results, unevaluated


def machine_human_register(rule_pool):
    """质检单（G.2 第 4 条红线）：逐规则两栏——机器可查面 / 仅人可查面。进 Run 证据。"""
    rows = []
    for rule in rule_pool:
        entry = RULE_CHECK_TABLE.get(rule.get("rule_id"))
        if entry is None:
            rows.append({
                "rule_id": rule.get("rule_id"),
                "machine_checkable": "（无谓词映射——本引擎不发结果，见 fail-closed 口径）",
                "human_only": "全部语义面",
            })
        else:
            rows.append({
                "rule_id": rule.get("rule_id"),
                "machine_checkable": entry["machine_scope"],
                "human_only": entry["human_scope"],
            })
    return rows
