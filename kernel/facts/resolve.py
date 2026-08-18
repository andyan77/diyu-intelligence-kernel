# -*- coding: utf-8 -*-
"""Snapshot 解引用与消费端兼容视图。

新形状（A.4.3 十四字段引用式）→ 消费端「内联兼容视图」：
detectors（tools/run_case.py 的 ctx["snapshot"]）与 intent 前处理（materialize_fact_pool）
此前消费的是 M0 旧内联形状；块 E ① 迁移后快照只剩引用。本模块把引用解开、
产出与旧形状同构的视图，让两个消费端接同一入口（E-05/E-08 的关闭面）。

视图纪律：
  · 全部 `_` 前缀键剔除——迁移注解里逐字保留着旧数值（如库存 800），进视图即给
    numeric_grounding 提供过期溯源面，属假绿通道，一律不进；
  · 事实对象剥头（fact_set_id / fact_type / version / schema_version / updated_at /
    updated_by_role / brand_id），只保留领域字段；
  · 全缺失家族对象 / 空引用数组 / null 引用 → 单叶 MISSING 占位（与 M0 INT 夹具写法同构，
    preflight 的缺失判定路径不变）；
  · 单成员数组 → 单数键（product / audience / persona）；多成员 → 旧惯例复数键
    （product_pool / audience_facts / persona_facts）。
"""
import copy

from .store import FactStore, FactResolutionError

_HEAD_KEYS = ("fact_set_id", "fact_type", "version", "schema_version",
              "updated_at", "updated_by_role", "brand_id")
_MISSING_STUB = {"value": None, "status": "MISSING", "source_refs": []}

_REF_FIELDS = ("brand_facts_ref", "product_facts_refs", "audience_facts_refs",
               "persona_facts_refs", "video_account_facts_ref", "active_rule_refs",
               "approved_brand_memory_refs")


def is_reference_shape(snapshot):
    """判据：十四字段引用式必有 brand_facts_ref 键；旧内联形状必有 facts 键、无引用键。"""
    return isinstance(snapshot, dict) and "brand_facts_ref" in snapshot


def _strip(obj):
    out = {}
    for k, v in obj.items():
        if k.startswith("_") or k in _HEAD_KEYS:
            continue
        out[k] = copy.deepcopy(v)
    return out


def _all_missing(obj):
    body = _strip(obj)
    fvs = [v for v in body.values() if isinstance(v, dict) and "status" in v]
    return bool(fvs) and all(v.get("status") == "MISSING" for v in fvs) and \
        all(isinstance(v, dict) and "status" in v for v in body.values()
            if not isinstance(v, str))


def materialize_legacy_view(snapshot, store=None):
    """引用式快照 → 旧内联同构视图。旧形状输入直接拒绝（E-05：删旧容错，两套形状不再并行）。

    返回 dict：{snapshot_id, brand_id, facts: {...}, hard_rules: [RuleRecord dict…]}。
    任何引用解析失败原样抛 FactResolutionError（fail-closed，不产出残缺视图）。
    """
    if not is_reference_shape(snapshot):
        raise FactResolutionError(
            "快照不是 A.4.3 引用式形状（缺 brand_facts_ref）——旧内联形状已随块 E ① 迁移退役，"
            "本入口不再容错；请先迁移或检查文件")
    store = store or FactStore()
    facts = {}

    brand = store.load(snapshot["brand_facts_ref"])
    facts["brand"] = copy.deepcopy(_MISSING_STUB) if _all_missing(brand) else _strip(brand)

    prods = [store.load(r) for r in snapshot["product_facts_refs"]]
    if len(prods) == 1:
        facts["product"] = _strip(prods[0])
    elif len(prods) > 1:
        facts["product_pool"] = [_strip(p) for p in prods]

    auds = [store.load(r) for r in snapshot["audience_facts_refs"]]
    if len(auds) == 1:
        facts["audience"] = _strip(auds[0])
    elif len(auds) > 1:
        facts["audience_facts"] = [_strip(a) for a in auds]
    else:
        facts["audience"] = copy.deepcopy(_MISSING_STUB)

    pers = [store.load(r) for r in snapshot["persona_facts_refs"]]
    if len(pers) == 1:
        facts["persona"] = _strip(pers[0])
    elif len(pers) > 1:
        facts["persona_facts"] = [_strip(p) for p in pers]
    else:
        facts["persona"] = copy.deepcopy(_MISSING_STUB)

    vref = snapshot.get("video_account_facts_ref")
    facts["video_account"] = _strip(store.load(vref)) if vref else copy.deepcopy(_MISSING_STUB)

    if snapshot.get("approved_brand_memory_refs"):
        # B.1.4 首轮关闭：非空即错（运行时谓词 R3 同判；这里提前拦，视图不掺未批准记忆）
        raise FactResolutionError("approved_brand_memory_refs 非空，B.1.4 首轮必须为空")

    hard_rules = [store.load(r) for r in snapshot["active_rule_refs"]]

    return {
        "snapshot_id": snapshot.get("snapshot_id"),
        "task_id": snapshot.get("task_id"),
        "brand_id": snapshot.get("brand_id"),
        "version": snapshot.get("version"),
        "facts": facts,
        "hard_rules": hard_rules,
    }
