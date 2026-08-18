#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 资产⑤：Trace 组装（FACT / RULE / ASSUMPTION / MODEL_JUDGMENT 四类分离，A.1.2）。

【M2-EP01 提前段·非正式证据】

纪律（与 kernel/intent/trace.py 同源）：
  · 零 I/O、零路径依赖、不 import config——保证可被单测直接调、replay/live 组装结果一致；
  · 模型只许引用**预物化**的 FACT/RULE ID（C.3 资产⑤），池外引用组装不出合法 Trace，当场报错；
  · ASSUMPTION 必须指明缺失项，MODEL_JUDGMENT 必须有支撑 Trace（A.9.2 规则句）；
  · trace_bundle_id 由内容确定性派生（sha256 前 16 位），同一输入两次组装逐字节一致；
  · 判定与处置分开：`assert_ids_in_pool` 只返回池外 ID 清单，不抛异常——要不要当错误由调用方定。

诚实边界（本模块判不了的，绝不假装判了）：
  ① FACT 条目的 source_refs 透传夹具 source 字符串包装成的说明——M0 夹具没有 A.2.3 全字段
     SourceRef 对象，本层**不硬凑**七字段对象（凑出来的 captured_at/checksum 全是编的），
     而是留空数组并把来源说明并进 statement。事实层 v2 对齐后由块 E 侧收敛（UPSTREAM_GAPS 第 2 条）。
  ② 「FACT 陈述与事实值是否相符」属语义面，本层只保证 ID 在池、类型不混写。
"""

import hashlib
import json


class TraceAssemblyError(ValueError):
    """组装不出合法 Trace（池外引用 / 缺品牌 / 类型混写）。继承 ValueError：
    只 `except ValueError` 的调用方也拦得住。"""


def assert_ids_in_pool(ids, fact_pool, rule_pool):
    """返回既不在事实池也不在规则池的 ID 清单（名字里的 assert 只表示"断言用"，不抛异常）。"""
    known = {f["fact_id"] for f in fact_pool} | {r.get("rule_id") for r in rule_pool}
    out = []
    for i in ids:
        if i not in known and i not in out:
            out.append(i)
    return out


def _fact_entry(fact):
    statement = f"{fact['field_path']} = {json.dumps(fact['value'], ensure_ascii=False)}"
    if fact.get("unit"):
        statement += f"（单位：{fact['unit']}）"
    if fact.get("source"):
        # 诚实边界①：来源说明并进 statement，不硬凑 SourceRef 七字段对象
        statement += f"［夹具来源：{fact['source']}］"
    return {
        "trace_id": fact["fact_id"],
        "trace_type": "FACT",
        "statement": statement,
        "source_refs": [],
        "target_paths": [],
    }


def _rule_entry(rule):
    status = rule.get("status")
    if status != "ACTIVE":
        # A.9.2：RULE 必须引用 ACTIVE 版本。非 ACTIVE 规则被引用 = 组装违规，当场报错
        raise TraceAssemblyError(f"规则 {rule.get('rule_id')} status={status!r}，非 ACTIVE 不得入 Trace（A.9.2）")
    return {
        "trace_id": rule["rule_id"],
        "trace_type": "RULE",
        "statement": f"{rule.get('statement')}（{rule['rule_id']} v{rule.get('version')}，ACTIVE）",
        "source_refs": [],
        "target_paths": [],
    }


def build_trace_bundle(fact_pool, rule_pool, referenced_fact_ids, referenced_rule_ids,
                       assumption_entries, model_judgment_entries, *,
                       brand_id=None, target_artifact_ref=None):
    """组装 TraceBundle（common.defs.TraceBundle 形状）。

    位置参数：物化池两份 + 模型引用的 FACT/RULE ID 两组 + 已建好的 ASSUMPTION / MODEL_JUDGMENT
    条目两组（由 runner 确定性生成，形状 = common.defs.TraceEntry）。
    关键字参数 brand_id / target_artifact_ref 必给（A.1.3：组装点不得臆造品牌归属）。

    池外 FACT/RULE 引用直接报错——幻觉引用 = 组装不出合法 Trace，本层不兜、不删、不改写。
    """
    if not brand_id:
        raise TraceAssemblyError("build_trace_bundle 需要 brand_id（A.1.3 单品牌隔离，不得缺省）")

    facts_by_id = {f["fact_id"]: f for f in fact_pool}
    rules_by_id = {r.get("rule_id"): r for r in rule_pool}

    entries = []
    seen = set()
    for fid in referenced_fact_ids:
        if fid in seen:
            continue
        if fid not in facts_by_id:
            raise TraceAssemblyError(f"FACT 引用 {fid!r} 不在预物化事实池（模型不得自建事实 ID，C.3 资产⑤）")
        entries.append(_fact_entry(facts_by_id[fid]))
        seen.add(fid)
    for rid in referenced_rule_ids:
        if rid in seen:
            continue
        if rid not in rules_by_id:
            raise TraceAssemblyError(f"RULE 引用 {rid!r} 不在规则注册表池（A.9.1 之外不存在规则）")
        entries.append(_rule_entry(rules_by_id[rid]))
        seen.add(rid)

    for entry in assumption_entries:
        if entry.get("trace_type") != "ASSUMPTION":
            raise TraceAssemblyError(f"assumption_entries 混入 {entry.get('trace_type')!r}（A.1.2 四类不得混写）")
        entries.append(entry)
    for entry in model_judgment_entries:
        if entry.get("trace_type") != "MODEL_JUDGMENT":
            raise TraceAssemblyError(f"model_judgment_entries 混入 {entry.get('trace_type')!r}（A.1.2 四类不得混写）")
        if not entry.get("supporting_trace_refs"):
            raise TraceAssemblyError(
                f"MODEL_JUDGMENT {entry.get('trace_id')!r} 无 supporting_trace_refs（A.9.2：判断必须有支撑 Trace）"
            )
        entries.append(entry)

    # bundle_id 由内容确定性派生：同一输入两次组装逐字节一致（离线自测「确定性」组的前提）
    digest = hashlib.sha256(
        json.dumps(entries, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]

    bundle = {
        "trace_bundle_id": f"TB-{digest}",
        "brand_id": brand_id,
        "entries": entries,
    }
    if target_artifact_ref is not None:
        bundle["target_artifact_ref"] = target_artifact_ref
    return bundle
