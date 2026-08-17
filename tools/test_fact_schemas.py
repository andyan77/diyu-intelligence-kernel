#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M1-EP01 事实层 Schema 正负例回归（check_m0 第 [6/6] 步的被测体；施工真源 D 索引 M1-EP01 + A.3/A.4.3）。

为什么必须有这个文件（M1-EP01 对抗核验 6/6 份 verify 一致点名）：contracts/schemas/examples/ 的
正负例若没有任何门禁跑它们，就是"死资产"——Schema 被改坏、$ref 断裂、负例失效，全链无人发现。
本文件把它们焊进回归：ok 例必须 VALID，bad 例必须 INVALID **且挂在声称的那条约束上**。

判绿口径（全部同时成立才 FACT_SCHEMAS_GREEN）：
  1. 七族 Schema 文件齐在且通过 Draft7 元校验（check_schema）；
  2. 每族至少 1 条 ok 例 + 2 条 bad 例（防样例被静默删光后"0 项全过"）；
  3. ok 例 0 违约；bad 例 ≥1 违约，且 _fixture_note.expected_error_substr 必须出现在实得报错里
     ——负例若因**别的**原因挂（如顺带缺了无关必填），期望子串对不上，当场红。
     没有 _fixture_note.expected_error_substr 的 bad 例一律红：不声明期望报错的负例无法防"负例污染"。

诚实边界（FACT_SCHEMAS_GREEN 不代表什么）：
  · 结构过 ≠ 内容正确 ≠ 事实为真——本回归只管 JSON Schema 结构层；
  · A.3/A.2.4 中 Schema 表达不了的语义约束（各 Schema description 已逐条注明"外包"），本回归一概未验。
    已知结构空洞清单（对抗核验实测，全部路由确定性谓词 C.3 资产④，落地纪律见裁决台账挂起项）：
      additionalProperties 开放（allOf 平铺的固有代价，拼错字段名静默通过）；空串 ID 可过（required
      拦不住 ""）；Range min>max 不拦；datetime 只落 string 无格式强制；Money.as_of 双层归属未收紧
      （A 行 180 与行 267 并存，不擅自加严）；fact_type 无归属检查（A 行 223 无枚举，不自造）；
      MODEL_EXTRACTION→只能 PROVISIONAL 属跨字段规则；CONFIRMED 的"非空"只判非 null。
  · acceptance/cases/*/fixtures/ 的既有考卷夹具**不是**本 Schema 形状（M0 期扁平自由结构）——
    对齐方向已定"改夹具不改 Schema"，但改夹具=改考卷（snapshot_hash 级联 20 份 Manifest），
    须 Founder 批准后单独施工，本回归不测它们、也不假装它们已对齐。

用法: python3 tools/test_fact_schemas.py     （不接受参数；改口径=改本文件，不设放宽开关）
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
MIN_OK, MIN_BAD = 1, 2

try:
    from jsonschema import Draft7Validator, RefResolver
except ImportError as e:
    sys.stderr.write("jsonschema 导入失败：%s（requirements.txt 钉版安装后再跑）\n" % e)
    sys.exit(1)


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


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
        validator = Draft7Validator(schema, resolver=resolver)

        try:
            names = sorted(f for f in os.listdir(EDIR)
                           if f.startswith(fam + ".") and f.endswith(".json"))
        except OSError as e:
            item("%s 样例目录" % fam, False, "examples/ 列不出来：%s（读不到 ≠ 没有样例）" % e)
            continue
        oks = [f for f in names if (".ok" in f)]
        bads = [f for f in names if (".bad" in f)]
        item("%s 样例下限" % fam, len(oks) >= MIN_OK and len(bads) >= MIN_BAD,
             "ok %d（需≥%d）/ bad %d（需≥%d）——样例被删光的族不算过，是没测"
             % (len(oks), MIN_OK, len(bads), MIN_BAD))

        for fn in oks:
            try:
                inst = load(os.path.join(EDIR, fn))
            except ValueError as e:
                item(fn, False, "不是合法 JSON：%s" % e)
                continue
            msgs = [err.message for err in validator.iter_errors(inst)]
            item(fn, not msgs, "正例竟有 %d 条违约，首条：%s" % (len(msgs), msgs[0] if msgs else ""))

        for fn in bads:
            try:
                inst = load(os.path.join(EDIR, fn))
            except ValueError as e:
                item(fn, False, "不是合法 JSON：%s" % e)
                continue
            msgs = [err.message for err in validator.iter_errors(inst)]
            note = inst.get("_fixture_note") or {}
            want = note.get("expected_error_substr") if isinstance(note, dict) else None
            if not msgs:
                item(fn, False, "负例竟然 VALID——它声称的约束没拦住它")
            elif not want:
                item(fn, False, "缺 _fixture_note.expected_error_substr——不声明期望报错的负例防不了负例污染")
            else:
                hit = any(want in m for m in msgs)
                item(fn, hit, "期望报错子串 %r 未出现在实得 %d 条报错里（首条：%s）——负例在因别的原因挂"
                     % (want, len(msgs), msgs[0]))

    print("fact_schemas 回归 | 七族 = A.3 五类事实 + VisualProfile + ContextSnapshot | 结构过 ≠ 内容正确")
    for f in fails:
        print("  ✗ " + f)
    failed = total - passed
    print("合计 %d 项：通过 %d，失败 %d" % (total, passed, failed))
    if failed == 0 and total > 0:
        print("FACT_SCHEMAS_GREEN | 语义空洞与考卷夹具漂移不在覆盖面内（见文件头诚实边界）")
        return 0
    print("FACT_SCHEMAS_RED | %d 项未过" % failed)
    return 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    sys.exit(main(sys.argv))
