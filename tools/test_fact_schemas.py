#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M1-EP01 事实层 Schema 正负例回归 v2（check_m0 第 [6/6] 步的被测体；施工真源 D 索引 M1-EP01 + A.3/A.4.3）。

v1→v2（块 B 语义补强，2026-08-18；外部审查 M1-EP01 两票判「需返工」的直接修复）：
  ① 三级计数钉死：族数 / 每族 ok·bad·predbad 份数 / 断言总数三层全等断言——删任何一个样例必须红
     （外部审查实测：删 visual_profile.bad3 后 46/46 照样 GREEN，覆盖集可被静默缩水）；
  ② FormatChecker 启用 + fail-closed 自检：datetime 字段的 format 校验先用已知非法值自证「真的拦」，
     环境缺 rfc3339 库时 format 静默放行 → 本回归直接 RED（不许"看起来启用了"）；
  ③ 新负例三元组：_fixture_note 里 expected_validator + expected_path 存在即强校验（绑定 validator
     类型与实例路径，不再只匹配消息子串）；存量负例仍走子串（计数钉死防其静默退化），增补时逐步升级；
  ④ 最小确定性谓词三条（C.3 资产④首批，接入本步）：
     P1 MODEL_EXTRACTION 来源 → 该 FactValue 不得 CONFIRMED（A.2.3「只能产生 PROVISIONAL」；
        本谓词只拦 CONFIRMED——MISSING/CONFLICTING 等状态不涉「把模型输出当确认事实」）；
     P2 ContextSnapshot 内全部嵌套 brand_id 与顶层全等（A.1.3 单品牌隔离）；
     P3 VersionedRef.object_type 与引用字段的目标族一致（A.4.3 引用不得错族）。
     ok 例必须 0 谓词违规；predbad 例必须恰命中其声明的谓词。
     其余谓词（snapshot_hash 核验 / RuleRecord ACTIVE / BrandMemory APPROVED / 版本追加）本轮不做，
     触发点 = 运行时对象落地（台账挂起表登记）。
  ⑤ $ref 断裂 / Schema 加载异常一律走标准 FACT_SCHEMAS_RED 收尾（不裸 traceback）。

判绿口径（全部同时成立才 FACT_SCHEMAS_GREEN）：
  1. 七族 Schema 齐在且过 Draft7 元校验；2. 三级计数与 EXPECTED 全等；3. ok 例 0 违约且 0 谓词违规；
  4. bad 例必须违约且命中声明子串（有三元组则加验 validator+path）；5. predbad 例 Schema 层合法
     但必须恰命中声明谓词；6. FormatChecker 自检通过。

诚实边界（FACT_SCHEMAS_GREEN 不代表什么）：
  · 结构过 + 三谓词过 ≠ 内容正确 ≠ 事实为真；
  · 未覆盖语义（外包清单更新版）：空串 ID 可过（required 拦不住 ""，A 未规定 minLength 不自行加严）；
    Range min>max 不拦；fact_type 无归属检查（A 无枚举不自造）；snapshot_hash 值核验 / 规则状态 /
    记忆状态 / Fact 更新触发新 Snapshot——运行时对象落地时随谓词批次补；
  · acceptance/cases/*/fixtures/ 的既有考卷夹具**不是**本 Schema 形状——对齐属改考卷，
    已登记台账挂起表（触发点 = 下次动 acceptance/ 考卷时），本回归不测它们、也不宣称已对齐。

用法: python3 tools/test_fact_schemas.py     （不接受参数；改口径=改本文件与 EXPECTED，不设放宽开关）
退出码: 0=全过 1=有失败 2=用法错误
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDIR = os.path.join(ROOT, "contracts", "schemas")
EDIR = os.path.join(SDIR, "examples")

# 七族 = A.3 五类事实 + A.3.3 VisualProfile + A.4.3 ContextSnapshot。
# 收缩这个元组 = 缩小回归覆盖面 = 改口径，须说明依据，不得为了让门变绿而删族。
FAMILIES = (
    "brand_facts", "product_facts", "visual_profile",
    "audience_facts", "persona_facts", "video_account_facts",
    "context_snapshot",
)

# ---- 三级计数第 2 级：每族 (ok, bad, predbad) 份数（块 B 施工后的样例集；改动 = 改覆盖面，须留痕）----
EXPECTED_COUNTS = {
    "brand_facts":         (2, 11, 1),
    "product_facts":       (2, 5, 0),
    "visual_profile":      (1, 4, 0),
    "audience_facts":      (1, 4, 0),
    "persona_facts":       (1, 4, 0),
    "video_account_facts": (1, 4, 0),
    "context_snapshot":    (1, 2, 2),
}
# ---- 三级计数第 3 级：断言总数（实测钉死；任何样例/断言增删必须同步本值并留痕）----
EXPECTED_TOTAL_ITEMS = 72

try:
    from jsonschema import Draft7Validator, RefResolver, FormatChecker
except ImportError as e:
    sys.stderr.write("jsonschema 导入失败：%s（requirements.txt 钉版安装后再跑）\n" % e)
    sys.exit(1)


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- 确定性谓词（C.3 资产④ 首批三条）

def iter_fact_values(node, path="$"):
    """遍历实例中所有形如 FactValue 的节点（带 status 键的 dict）。"""
    if isinstance(node, dict):
        if isinstance(node.get("status"), str):
            yield path, node
        for k, v in node.items():
            if k.startswith("_"):
                continue
            for r in iter_fact_values(v, path + "." + k):
                yield r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            for r in iter_fact_values(v, "%s[%d]" % (path, i)):
                yield r


def predicate_model_extraction(inst):
    """P1：任一 source_ref.source_type=MODEL_EXTRACTION 的 FactValue，status 不得为 CONFIRMED（A.2.3）。"""
    out = []
    for path, fv in iter_fact_values(inst):
        refs = fv.get("source_refs") or []
        if fv.get("status") == "CONFIRMED" and any(
                isinstance(r, dict) and r.get("source_type") == "MODEL_EXTRACTION" for r in refs):
            out.append("P1 %s: MODEL_EXTRACTION 来源被标 CONFIRMED——模型抽取只能产生 PROVISIONAL（A.2.3）" % path)
    return out


def collect_brand_ids(node, path="$"):
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("_"):
                continue
            if k == "brand_id" and isinstance(v, str):
                yield path + ".brand_id", v
            else:
                for r in collect_brand_ids(v, path + "." + k):
                    yield r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            for r in collect_brand_ids(v, "%s[%d]" % (path, i)):
                yield r


def predicate_single_brand(inst):
    """P2：ContextSnapshot 顶层 brand_id 与全部嵌套 brand_id 全等（A.1.3 单品牌隔离，不一致必须阻断）。"""
    top = inst.get("brand_id")
    if not isinstance(top, str):
        return ["P2 $.brand_id: 顶层 brand_id 缺失或非字符串，单品牌隔离无从核验"]
    return ["P2 %s: brand_id=%r ≠ 顶层 %r（跨品牌引用，A.1.3 阻断）" % (p, v, top)
            for p, v in collect_brand_ids(inst) if p != "$.brand_id" and v != top]


# ContextSnapshot 引用字段 → 期望 object_type（A.4.3 字段语义逐字对应）
SNAPSHOT_REF_TYPES = {
    "brand_facts_ref": "BrandFacts",
    "product_facts_refs": "ProductFacts",
    "audience_facts_refs": "AudienceFacts",
    "persona_facts_refs": "PersonaFacts",
    "video_account_facts_ref": "VideoAccountFacts",
    "active_rule_refs": "RuleRecord",
    "approved_brand_memory_refs": "BrandMemory",
}


def predicate_ref_object_type(inst):
    """P3：VersionedRef.object_type 与其所在引用字段的目标族一致（A.4.3）。只对 ContextSnapshot 生效。"""
    out = []
    for field, want in SNAPSHOT_REF_TYPES.items():
        v = inst.get(field)
        refs = v if isinstance(v, list) else ([v] if isinstance(v, dict) else [])
        for i, r in enumerate(refs):
            if isinstance(r, dict) and r.get("object_type") != want:
                out.append("P3 $.%s[%d].object_type=%r ≠ %r（引用错族）" % (field, i, r.get("object_type"), want))
    return out


def run_predicates(fam, inst):
    out = predicate_model_extraction(inst)
    if fam == "context_snapshot":
        out += predicate_single_brand(inst)
        out += predicate_ref_object_type(inst)
    return out


# ---------------------------------------------------------------- 主流程

def main(argv):
    if argv[1:]:
        sys.stderr.write("用法错误：test_fact_schemas.py 不接受参数。\n")
        return 2
    total = passed = 0
    fails = []

    def item(label, ok, why=""):
        nonlocal total, passed
        total += 1
        if ok:
            passed += 1
        else:
            fails.append("%s: %s" % (label, why))

    # ---- FormatChecker fail-closed 自检：环境缺 rfc3339 库时 format 会静默放行，必须先自证「真的拦」----
    fmt = FormatChecker()
    probe = Draft7Validator({"type": "string", "format": "date-time"}, format_checker=fmt)
    item("FormatChecker 自检（非法 datetime 必须拦）", bool(list(probe.iter_errors("不是时间"))),
         "format=date-time 没拦住已知非法值——环境缺 rfc3339 校验库（requirements.txt 的 "
         "rfc3339-validator），format 正在静默放行，绿了也是假绿")

    # ---- 三级计数第 1 级：族集合全等 ----
    item("七族口径", tuple(sorted(FAMILIES)) == tuple(sorted(EXPECTED_COUNTS)),
         "FAMILIES 与 EXPECTED_COUNTS 键集不一致——改口径必须两处同改")

    for fam in FAMILIES:
        spath = os.path.join(SDIR, fam + ".schema.json")
        if not os.path.exists(spath):
            item("%s.schema" % fam, False, "Schema 文件不存在——族被删除或未落盘")
            continue
        try:
            schema = load(spath)
            Draft7Validator.check_schema(schema)
            item("%s.schema 元校验" % fam, True)
        except Exception as e:
            item("%s.schema 元校验" % fam, False, "check_schema 失败：%s" % e)
            continue
        resolver = RefResolver(base_uri="file://" + SDIR + "/", referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver, format_checker=fmt)

        try:
            names = sorted(f for f in os.listdir(EDIR)
                           if f.startswith(fam + ".") and f.endswith(".json"))
        except OSError as e:
            item("%s 样例目录" % fam, False, "examples/ 列不出来：%s（读不到 ≠ 没有样例）" % e)
            continue
        oks = [f for f in names if ".ok" in f]
        predbads = [f for f in names if ".predbad" in f]
        bads = [f for f in names if ".bad" in f and f not in predbads]

        want_ok, want_bad, want_pred = EXPECTED_COUNTS[fam]
        item("%s 计数钉死" % fam,
             (len(oks), len(bads), len(predbads)) == (want_ok, want_bad, want_pred),
             "实际 ok/bad/predbad = %d/%d/%d ≠ 钉死 %d/%d/%d——样例被增删而计数未同步 = 覆盖面漂移"
             % (len(oks), len(bads), len(predbads), want_ok, want_bad, want_pred))

        for fn in oks:
            try:
                inst = load(os.path.join(EDIR, fn))
            except ValueError as e:
                item(fn, False, "不是合法 JSON：%s" % e)
                continue
            try:
                msgs = [err.message for err in validator.iter_errors(inst)]
            except Exception as e:
                item(fn, False, "校验器异常（$ref 断裂或 Schema 坏）：%s" % e)
                continue
            item(fn, not msgs, "正例竟有 %d 条违约，首条：%s" % (len(msgs), msgs[0] if msgs else ""))
            pv = run_predicates(fam, inst)
            item(fn + " 谓词", not pv, "正例竟有 %d 条谓词违规，首条：%s" % (len(pv), pv[0] if pv else ""))

        for fn in bads:
            try:
                inst = load(os.path.join(EDIR, fn))
            except ValueError as e:
                item(fn, False, "不是合法 JSON：%s" % e)
                continue
            try:
                errors = list(validator.iter_errors(inst))
            except Exception as e:
                item(fn, False, "校验器异常（$ref 断裂或 Schema 坏）：%s" % e)
                continue
            note = inst.get("_fixture_note") or {}
            want = note.get("expected_error_substr") if isinstance(note, dict) else None
            want_validator = note.get("expected_validator") if isinstance(note, dict) else None
            want_path = note.get("expected_path") if isinstance(note, dict) else None
            if not errors:
                item(fn, False, "负例竟然 VALID——它声称的约束没拦住它")
                continue
            if not want:
                item(fn, False, "缺 _fixture_note.expected_error_substr——不声明期望报错的负例防不了负例污染")
                continue
            hit = [e for e in errors if want in e.message]
            if not hit:
                item(fn, False, "期望报错子串 %r 未出现在实得 %d 条报错里（首条：%s）——负例在因别的原因挂"
                     % (want, len(errors), errors[0].message))
                continue
            if want_validator or want_path:
                # 三元组强校验（v2 新负例协议）：同一条报错须同时命中 validator 与实例路径
                def epath(e):
                    return "$" + "".join("[%d]" % p if isinstance(p, int) else "." + str(p)
                                         for p in e.absolute_path)
                bound = [e for e in hit
                         if (not want_validator or e.validator == want_validator)
                         and (not want_path or epath(e) == want_path)]
                item(fn, bool(bound),
                     "子串命中但未绑定住：期望 validator=%r path=%r，实得命中条 [%s]——错误挂错了位置"
                     % (want_validator, want_path,
                        "; ".join("%s@%s" % (e.validator, epath(e)) for e in hit[:3])))
            else:
                item(fn, True)

        for fn in predbads:
            try:
                inst = load(os.path.join(EDIR, fn))
            except ValueError as e:
                item(fn, False, "不是合法 JSON：%s" % e)
                continue
            try:
                msgs = [err.message for err in validator.iter_errors(inst)]
            except Exception as e:
                item(fn, False, "校验器异常（$ref 断裂或 Schema 坏）：%s" % e)
                continue
            note = inst.get("_fixture_note") or {}
            want_pred_tag = note.get("expected_predicate") if isinstance(note, dict) else None
            if msgs:
                item(fn, False, "谓词负例在 Schema 层就挂了（首条：%s）——它必须结构合法、只由谓词拦" % msgs[0])
                continue
            if not want_pred_tag:
                item(fn, False, "缺 _fixture_note.expected_predicate——不声明期望谓词的谓词负例防不了污染")
                continue
            pv = run_predicates(fam, inst)
            item(fn, any(v.startswith(want_pred_tag + " ") for v in pv),
                 "期望谓词 %r 未命中（实得 %d 条：%s）" % (want_pred_tag, len(pv), "; ".join(pv[:2]) or "无"))

    # ---- 三级计数第 3 级：断言总数 ----
    item("断言总数钉死", total + 1 == EXPECTED_TOTAL_ITEMS,
         "实际 %d ≠ 钉死 %d——覆盖面变了而总数未同步留痕" % (total + 1, EXPECTED_TOTAL_ITEMS))

    print("fact_schemas 回归 v2 | 七族 + 三谓词(P1/P2/P3) + FormatChecker | 结构过+谓词过 ≠ 内容正确")
    for f in fails:
        print("  ✗ " + f)
    failed = total - passed
    print("合计 %d 项：通过 %d，失败 %d" % (total, passed, failed))
    if failed == 0 and total > 0:
        print("FACT_SCHEMAS_GREEN | 未覆盖语义见文件头诚实边界（空串 ID / Range min>max / "
              "snapshot_hash 值核验等运行时谓词批次）")
        return 0
    print("FACT_SCHEMAS_RED | %d 项未过" % failed)
    return 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    sys.exit(main(sys.argv))
