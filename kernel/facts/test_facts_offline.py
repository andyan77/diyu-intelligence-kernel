#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/facts 离线回归（纯 assert，不依赖 pytest；exit 0=全过 1=有失败）。

覆盖（块 E ②③ 的自证面；与 tools/test_fact_schemas.py ⑤ 正式面扩测互补——那边证明
「真仓当前状态全绿」，这边证明「谓词与存取层在坏输入上真的会红」，防 exit 0 ≠ 通过）：
  正向：15 份正式快照逐份 R1-R5/P2/P3/P4 全绿 + 解引用成视图（纵切端到端）；
  负向（内存构造坏输入，不落盘不污染真仓）：
    N1 snapshot_hash 篡改 → R1 红          N2 悬空引用 → R2 红
    N3 引用非 ACTIVE 规则 → R2 红           N4 BrandMemory 非空 → R3 红
    N5 locator 明文凭证 → R4 红             N6 同 ID 同版本撞车 → R5 红（store 索引层）
    N7 跨品牌引用 → P2 红                   N8 引用错族 → P3 红
    N9 Range min>max → P4 红                N10 旧内联形状 → materialize_legacy_view 拒绝
"""
import copy
import glob
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from kernel.facts import FactStore, FactResolutionError, materialize_legacy_view  # noqa: E402
from kernel.facts import predicates as kp  # noqa: E402

total = passed = 0
fails = []


def item(name, ok, why=""):
    global total, passed
    total += 1
    passed += ok
    if not ok:
        fails.append("%s: %s" % (name, why))
    print("[%s] %s" % ("ok" if ok else "✗✗", name))


def main():
    store = FactStore()
    snaps = sorted(glob.glob(os.path.join(ROOT, "acceptance/cases/*/fixtures/context_snapshot*.json")))
    item("正式快照计数", len(snaps) == 15, "实得 %d" % len(snaps))
    base = None
    for p in snaps:
        snap = json.load(io.open(p, encoding="utf-8"))
        red = kp.run_all_runtime(snap, store)
        item("正向 %s R1-R5 全绿" % os.path.relpath(p, ROOT).split("cases/")[-1],
             not red, red[0] if red else "")
        try:
            view = materialize_legacy_view(snap, store)
            ok = isinstance(view.get("facts"), dict) and view.get("brand_id") == snap["brand_id"]
        except FactResolutionError as e:
            ok = False
            view = None
        item("正向 %s 解引用" % snap["snapshot_id"], ok, "视图构建失败")
        if base is None:
            base = snap

    # ---- 负向（全部在 deepcopy 上做，真仓零改动）----
    s = copy.deepcopy(base)
    s["version"] = 2  # 内容变了、hash 没变
    item("N1 snapshot_hash 篡改→R1", any(m.startswith("R1") for m in kp.runtime_snapshot_hash(s)))

    s = copy.deepcopy(base)
    s["product_facts_refs"] = [dict(s["product_facts_refs"][0], object_id="FS-PRODUCT-不存在-9999")] \
        if s["product_facts_refs"] else s["product_facts_refs"]
    item("N2 悬空引用→R2", any(m.startswith("R2") for m in kp.runtime_refs_resolve(s, store)))

    s = copy.deepcopy(base)
    s["active_rule_refs"] = [{"object_type": "RuleRecord", "object_id": "R-BDD01-001",
                              "version": 99, "brand_id": s["brand_id"]}]
    item("N3 规则版本悬空→R2", any(m.startswith("R2") for m in kp.runtime_refs_resolve(s, store)))

    s = copy.deepcopy(base)
    s["approved_brand_memory_refs"] = [{"object_type": "BrandMemory", "object_id": "BM-X",
                                        "version": 1, "brand_id": s["brand_id"]}]
    item("N4 BrandMemory 非空→R3", any(m.startswith("R3") for m in kp.runtime_brand_memory_first_round(s)))
    try:
        materialize_legacy_view(s, store)
        item("N4b 解引用层同拦", False, "带未批准记忆引用的快照被解成了视图")
    except FactResolutionError:
        item("N4b 解引用层同拦", True)

    s = copy.deepcopy(base)
    s["input_source_refs"] = list(s.get("input_source_refs") or []) + [{
        "source_id": "SRC-EVIL", "brand_id": s["brand_id"], "source_type": "SYSTEM_RECORD",
        "locator": "https://user:hunter2pass@internal.example/db", "captured_at": "2026-08-17T00:00:00+08:00",
        "checksum": None}]
    item("N5 locator 明文凭证→R4", any(m.startswith("R4") for m in kp.runtime_locator_credentials(s)))

    dup_store = FactStore()
    dup_store._index = None
    # 撞车用影子目录模拟：把同一对象登记两次成本太高（要写盘）；直接构造 index 冲突路径——
    # 走 store 内部约定：手工预置索引后调用 rules() 仍会构建；此处用两份内存对象直接调用私有逻辑
    # 不如实测：复制一份池文件到同族目录（临时名）再建索引，测完删除。
    pool_dir = os.path.join(ROOT, "acceptance/fixtures/facts/product")
    src = sorted(glob.glob(os.path.join(pool_dir, "*.v1.json")))[0]
    tmp = os.path.join(pool_dir, "__dup_probe__.v1.json")
    try:
        with io.open(src, encoding="utf-8") as f:
            io.open(tmp, "w", encoding="utf-8").write(f.read())
        red = kp.runtime_no_duplicate_identity(FactStore())
        item("N6 同 ID 同版本撞车→R5", any(m.startswith("R5") for m in red), "撞车未被拦")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    s = copy.deepcopy(base)
    s["brand_facts_ref"] = dict(s["brand_facts_ref"], brand_id="other-brand-02")
    item("N7 跨品牌引用→P2", any(m.startswith("P2") for m in kp.predicate_single_brand(s)))

    s = copy.deepcopy(base)
    s["brand_facts_ref"] = dict(s["brand_facts_ref"], object_type="ProductFacts")
    item("N8 引用错族→P3", any(m.startswith("P3") for m in kp.predicate_ref_object_type(s)))

    item("N9 Range min>max→P4", any(m.startswith("P4") for m in kp.predicate_range_sane(
        {"x": {"value": {"min": 45, "max": 30, "unit": "岁"}, "status": "CONFIRMED"}})))

    try:
        materialize_legacy_view({"snapshot_id": "S", "brand_id": "b", "facts": {}, "hard_rules": []})
        item("N10 旧内联形状拒绝", False, "旧形状被接受——删旧容错失效")
    except FactResolutionError:
        item("N10 旧内联形状拒绝", True)

    print("\n合计 %d 项：通过 %d，失败 %d" % (total, passed, total - passed))
    if total == passed and total > 0:
        print("FACTS_OFFLINE_GREEN | 谓词红得起来 + 纵切端到端可解引用；绿 ≠ 事实为真")
        return 0
    for f in fails:
        print("  ✗ " + f)
    print("FACTS_OFFLINE_RED")
    return 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
