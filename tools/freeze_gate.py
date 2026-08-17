#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""冻结断言门（IA-0 送签前的物理拦截器）。

职责真源：IA-0_冻结签字包.md 三、B 类建设项——「送签前脚本扫描全部 Manifest，任何 PENDING 残留 =
物理拒绝送签（堵"带着占位签字"的假绿）」；OPEN_QUESTIONS.md 文首执行侧自决项「PENDING 冻结断言门」
「hash=sha256 规范化 JSON」；OQ-INT-D01-06（SCHEMA_OK ≠ 可冻结）。

七条红线（任一触发即 exit 1，且逐条列明，不汇总成一句"失败"）：
  R1 齐套数 ≠ EXPECTED_MANIFESTS
  R2 任一 Manifest 的**字段值**空白或命中占位模式（注释里的占位字样不算——注释是说明，不是考试条件）
  R3 Schema 不过（contracts/schemas/case_manifest.schema.json）
  R4 snapshot_hash 与按本文件算法实算的值不符 / 快照找不到 / 快照 ID 撞车 / 快照与 Manifest 不同案例目录
  R5 hard_rule_refs 解析不到 contracts/rules/ 的 RuleRecord 对象（含 version / brand_id / 非 ACTIVE），
     或 RuleRecord 字段集与 A.9.1 十项不全等
  R6 签字三件套失真：approved_at 不可解析为 ISO8601、approved_by 或 generation_parameters_hash 空白/占位
  R7 prd_version / data_contract_version / acceptance_contract_version 与三份真源文档控制块**实时解析**
     出来的版本号不一致

snapshot_hash 算法（本文件是唯一实现，Manifest 注释指向此处）：
  读快照 JSON → json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) → UTF-8 编码
  → sha256 → 字符串写作 "sha256:<hex>"。即：UTF-8、键排序、无多余空白的规范化 JSON 的 sha256。

边界（C.2 / C.4：脚本只汇总不推导，不建平台）：本门只做机械核验，不改任何文件、不猜测取值。
GATE_GREEN 只代表"占位清零且机械核验一致"，**不代表** Founder 已签字、更不代表案例质量合格——
签字动作定义见 B.2.1 与 IA-0_冻结签字包.md 附。

用法: python3 tools/freeze_gate.py   exit 0=全绿 1=有红线
  本门不接受任何参数。齐套数等考试口径写死于脚本常量：改常量 = 改考卷，须随 Founder 预裁决一起改，
  不得由命令行开关在单次运行里临时放宽（旧 --expected 参数即为此洞，已删除）。
"""
import datetime
import glob
import hashlib
import io
import json
import os
import re
import sys

import yaml
from jsonschema import Draft7Validator, RefResolver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_GLOB = os.path.join(ROOT, "acceptance/cases/*/manifest*.draft.yaml")
SNAPSHOT_GLOB = os.path.join(ROOT, "acceptance/cases/*/fixtures/*.json")
RULES_GLOB = os.path.join(ROOT, "contracts/rules/*.yaml")
SCHEMA_PATH = os.path.join(ROOT, "contracts/schemas/case_manifest.schema.json")

# 齐套口径 20 = Founder 2026-08-17 预裁决①「INT-D01 补 QUICK 分支变体，总 20 份」
# （acceptance/cases/OPEN_QUESTIONS.md 文首）+ IA-0_冻结签字包.md 四「版本串+参数哈希填入 20 份 Manifest」。
# 该口径变更 = 改考试条件，须随预裁决一起改，不得由本脚本静默跟随目录里数到几份就算几份，
# 也不得由命令行参数在单次运行里临时改写。
EXPECTED_MANIFESTS = 20

# 占位模式（R2/R6 共用）。空白（空串或纯空格）单独判，等价于政策里的 ^$ 分支。
PLACEHOLDER_RE = re.compile(r"PENDING|TBD|TODO|N/A|待定|XXX|\?\?\?")

# R6 签字三件套：这三个字段带着占位进签字流程 = "带着占位签字"的假绿本体。
SIGNATURE_FIELDS = ("approved_by", "approved_at", "generation_parameters_hash")

# R5：A.9.1 RuleRecord 的十项字段（A_模块接口与核心数据字典.md「## A.9.1 RuleRecord」yaml 块逐字）。
# 字段集必须全等——少一项 = 注册表残缺，多一项 = 私自扩合同，两者都不得被冻结案例引用。
RULE_RECORD_FIELDS_A91 = frozenset([
    "rule_id", "brand_id", "version", "scope", "effect",
    "target_path", "statement", "source_ref", "status", "effective_at",
])

# R4：跨案例共用快照的**唯一**合法例外。口径同 EXPECTED_MANIFESTS——改这里 = 改考卷。
# 依据：B.5.1/E2E-02「与 E2E-01 使用相同企业事实」+ B.2.2「同条件」定义之「相同 Context Snapshot」，
# 故 E2E-02 的 Manifest 指向 E2E-01/fixtures/ 下的 SNAP-E2E01-0001 属设计要求，不是错挂。
# 键 = Manifest 所在案例目录名，值 = 允许借用快照的案例目录名。
CROSS_CASE_SNAPSHOT_ALLOWED = {"E2E-02": "E2E-01"}

# R7：三个版本字段 ↔ 三份真源文档。版本号**每次运行实时解析**文档控制块，脚本内不留基线常量——
# 硬编码基线会在真源改版后继续判绿（B10 假绿洞的成因）。
VERSION_SOURCES = (
    ("prd_version", "PRD_笛语智能核_MVP_V3.0_v0.1.md"),
    ("data_contract_version", "A_模块接口与核心数据字典.md"),
    ("acceptance_contract_version", "B_三个核心模块智能验收合同.md"),
)
# 文档控制块里的版本行：`| 版本 | v0.2 |`
VERSION_ROW_RE = re.compile(r"^\|\s*版本\s*\|\s*([^|]+?)\s*\|\s*$", re.M)


def rel(p):
    return os.path.relpath(p, ROOT)


def case_dir_of(path):
    """acceptance/cases/<CASE>/... → <CASE>；不在该布局下返回 None。"""
    parts = rel(path).replace(os.sep, "/").split("/")
    if len(parts) >= 3 and parts[0] == "acceptance" and parts[1] == "cases":
        return parts[2]
    return None


def blank_or_placeholder(val):
    """R2/R6 共用判据：空白 或 命中占位模式。返回 None 表示通过，否则返回红线原因。"""
    if val is None:
        return "为 null（必填字段不得以 null 充当已填）"
    if not isinstance(val, str):
        return None
    if val.strip() == "":
        return "为空白值（空串/纯空格不算已填）"
    m = PLACEHOLDER_RE.search(val)
    if m:
        return "仍是占位值（命中占位模式 %s）→ %s" % (m.group(0), val.splitlines()[0][:80])
    return None


def parse_iso8601(val):
    """能解析返回 datetime，否则返回 None。Py3.10 的 fromisoformat 不吃 Z 后缀，先归一。"""
    if not isinstance(val, str):
        return None
    s = val.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.datetime.fromisoformat(s)
    except ValueError:
        return None


def canonical_snapshot_hash(path):
    """快照 JSON 的规范化 sha256。规范化 = UTF-8 + 键排序 + 紧凑分隔符（无多余空白）。"""
    with io.open(path, encoding="utf-8") as f:
        obj = json.load(f)
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def walk_values(node, path=""):
    """只遍历解析后的值——注释在此已被 YAML 解析器丢弃，故注释中的占位字样不会误报。"""
    if isinstance(node, dict):
        for k, v in node.items():
            for item in walk_values(v, "%s.%s" % (path, k) if path else str(k)):
                yield item
    elif isinstance(node, list):
        for i, v in enumerate(node):
            for item in walk_values(v, "%s[%d]" % (path, i)):
                yield item
    else:
        yield path, node


def index_snapshots(errors):
    """snapshot_id -> 文件路径。撞车（同一 ID 落在两个文件）直接算红线，不择一。"""
    idx = {}
    for p in sorted(glob.glob(SNAPSHOT_GLOB)):
        try:
            with io.open(p, encoding="utf-8") as f:
                obj = json.load(f)
        except ValueError as e:
            errors.append("R4 快照 JSON 解析失败: %s（%s）" % (rel(p), e))
            continue
        if isinstance(obj, dict) and isinstance(obj.get("snapshot_id"), str):
            sid = obj["snapshot_id"]
            if sid in idx:
                errors.append("R4 快照 ID 撞车: %s 同时出现在 %s 与 %s——无法确定该对哪一份算 hash"
                              % (sid, rel(idx[sid]), rel(p)))
            else:
                idx[sid] = p
    return idx


def index_rules(errors):
    """rule_id -> RuleRecord 对象。文件名与 rule_id 不一致、缺 rule_id、字段集不符 A.9.1 均算红线。"""
    idx = {}
    for p in sorted(glob.glob(RULES_GLOB)):
        try:
            with io.open(p, encoding="utf-8") as f:
                obj = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append("R5 规则文件 YAML 解析失败: %s（%s）" % (rel(p), e))
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("rule_id"), str):
            errors.append("R5 规则文件缺 rule_id，无法建索引: %s" % rel(p))
            continue
        rid = obj["rule_id"]
        if os.path.basename(p) != rid + ".yaml":
            errors.append("R5 规则文件名与 rule_id 不一致: %s 内是 %s" % (rel(p), rid))

        # 字段集必须与 A.9.1 十项全等（机械校验，不看值只看键）
        keys = set(obj.keys())
        missing = sorted(RULE_RECORD_FIELDS_A91 - keys)
        extra = sorted(keys - RULE_RECORD_FIELDS_A91)
        if missing or extra:
            errors.append("R5 %s 的字段集与 A.9.1 RuleRecord 十项不全等: 缺 %s / 多 %s"
                          % (rel(p), missing or "无", extra or "无"))

        if rid in idx:
            errors.append("R5 rule_id 重复登记: %s" % rid)
        else:
            idx[rid] = (obj, p)
    return idx


def resolve_doc_versions(errors):
    """实时解析三份真源文档控制块的版本号。解析不到 / 多于一处 = 红线，不退回默认值。"""
    versions = {}
    for field, docname in VERSION_SOURCES:
        path = os.path.join(ROOT, docname)
        if not os.path.exists(path):
            errors.append("R7 真源文档缺失: %s（%s 无从核验）" % (docname, field))
            continue
        with io.open(path, encoding="utf-8") as f:
            text = f.read()
        found = VERSION_ROW_RE.findall(text)
        if len(found) != 1:
            errors.append("R7 %s 的文档控制块「| 版本 | … |」行解析到 %d 处（应恰好 1 处），"
                          "%s 无从核验" % (docname, len(found), field))
            continue
        versions[field] = found[0]
    return versions


def main():
    if sys.argv[1:]:
        print("冻结断言门不接受参数（齐套数等考试口径写死于脚本常量：改口径 = 改考卷）。"
              "收到: %s" % " ".join(sys.argv[1:]), file=sys.stderr)
        return 1

    expected = EXPECTED_MANIFESTS
    errors = []
    manifests = sorted(glob.glob(MANIFEST_GLOB))

    # ---- R1 齐套 ----
    if len(manifests) != expected:
        errors.append("R1 齐套数不符: 实际 %d 份 ≠ 应有 %d 份（缺任一变体不得计齐套）" % (len(manifests), expected))

    snap_idx = index_snapshots(errors)
    rule_idx = index_rules(errors)
    doc_versions = resolve_doc_versions(errors)

    schema = json.load(io.open(SCHEMA_PATH, encoding="utf-8"))
    required_fields = set(schema.get("required") or [])
    resolver = RefResolver(base_uri="file://" + os.path.dirname(SCHEMA_PATH) + "/", referrer=schema)
    validator = Draft7Validator(schema, resolver=resolver)

    for mf in manifests:
        name = rel(mf)
        try:
            with io.open(mf, encoding="utf-8") as f:
                doc = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append("R3 %s: YAML 解析失败（%s）" % (name, e))
            continue
        if not isinstance(doc, dict):
            errors.append("R3 %s: 顶层不是映射对象" % name)
            continue

        # ---- R2 空白 / 占位残留（只看值，不看注释）----
        # 覆盖面：占位模式对**所有**字符串值生效；空白/null 判据对必填字段（及其子字段）生效——
        # 可选字段留空是合法状态，必填字段留空是"填了个寂寞"的假绿。
        r2_flagged = set()
        for fpath, val in walk_values(doc):
            top = fpath.split(".")[0].split("[")[0]
            is_required_branch = top in required_fields
            reason = blank_or_placeholder(val)
            if reason is None:
                continue
            # null / 空白只对必填分支判红；占位模式一律判红
            if not isinstance(val, str) and not is_required_branch:
                continue
            if isinstance(val, str) and val.strip() == "" and not is_required_branch:
                continue
            errors.append("R2 %s: 字段 %s %s" % (name, fpath, reason))
            r2_flagged.add(fpath)

        # ---- R3 Schema ----
        for e in sorted(validator.iter_errors(doc), key=lambda x: list(x.absolute_path)):
            errors.append("R3 %s: /%s %s" % (name, "/".join(map(str, e.absolute_path)), e.message))

        # ---- R4 snapshot_hash + 归属 ----
        sid, declared = doc.get("context_snapshot_id"), doc.get("snapshot_hash")
        if not isinstance(sid, str) or sid not in snap_idx:
            errors.append("R4 %s: context_snapshot_id=%r 在 acceptance/cases/*/fixtures/ 里找不到对应快照，"
                          "snapshot_hash 无从核验" % (name, sid))
        else:
            spath = snap_idx[sid]
            mcase, scase = case_dir_of(mf), case_dir_of(spath)
            if mcase != scase and CROSS_CASE_SNAPSHOT_ALLOWED.get(mcase) != scase:
                errors.append("R4 %s: 快照归属越界——Manifest 在案例 %s，快照 %s 却在案例 %s；"
                              "跨案例共用快照只有 %s 一条合法例外（B.5.1/E2E-02 相同企业事实 + B.2.2 相同 Context Snapshot）"
                              % (name, mcase, sid, scase,
                                 "、".join("%s←%s" % kv for kv in sorted(CROSS_CASE_SNAPSHOT_ALLOWED.items()))))
            actual = canonical_snapshot_hash(spath)
            if declared != actual:
                errors.append("R4 %s: snapshot_hash 与实算不符\n      声明 %s\n      实算 %s（源 %s）"
                              % (name, declared, actual, rel(spath)))

        # ---- R5 hard_rule_refs ----
        for i, ref in enumerate(doc.get("hard_rule_refs") or []):
            loc = "%s: hard_rule_refs[%d]" % (name, i)
            if not isinstance(ref, dict):
                errors.append("R5 %s 不是 VersionedRef 对象" % loc)
                continue
            oid = ref.get("object_id")
            if ref.get("object_type") != "RuleRecord":
                errors.append("R5 %s object_type=%r，硬规则引用必须是 RuleRecord" % (loc, ref.get("object_type")))
            if oid not in rule_idx:
                errors.append("R5 %s object_id=%r 在 contracts/rules/ 无对应 RuleRecord 对象（解析不到）" % (loc, oid))
                continue
            rule, rpath = rule_idx[oid]
            if ref.get("version") != rule.get("version"):
                errors.append("R5 %s version=%r，但 %s 的 version=%r（版本对不上）"
                              % (loc, ref.get("version"), rel(rpath), rule.get("version")))
            if ref.get("brand_id") != rule.get("brand_id"):
                errors.append("R5 %s brand_id=%r，但 %s 的 brand_id=%r（品牌隔离 SYS-08）"
                              % (loc, ref.get("brand_id"), rel(rpath), rule.get("brand_id")))
            if rule.get("status") != "ACTIVE":
                errors.append("R5 %s 指向的 %s status=%r，非 ACTIVE 规则不得被冻结案例引用（A.9.2）"
                              % (loc, rel(rpath), rule.get("status")))

        # ---- R6 签字三件套 ----
        # R6 在 R2 之上补类型级断言。同一字段若已被 R2 判红，此处不重复计一条红线（同一事实只算一条）；
        # R2 放行的值 R6 仍会继续断言——例如 approved_at="签字日" 非空非占位，但不是 ISO8601，只有 R6 拦得住。
        for field in SIGNATURE_FIELDS:
            if field in r2_flagged:
                continue
            val = doc.get(field)
            reason = blank_or_placeholder(val)
            if reason is None and not isinstance(val, str):
                reason = "类型是 %s，签字字段必须是字符串" % type(val).__name__
            if reason is not None:
                errors.append("R6 %s: 签字字段 %s %s（带着占位/空值签字即假绿）" % (name, field, reason))
                continue
            if field == "approved_at" and parse_iso8601(val) is None:
                errors.append("R6 %s: approved_at=%r 不能解析为 ISO8601 datetime（B.2.1 该字段类型 datetime）"
                              % (name, val))

        # ---- R7 版本指针 ↔ 真源文档控制块 ----
        for field, docname in VERSION_SOURCES:
            if field not in doc_versions:
                continue  # 解析失败已在 resolve_doc_versions 记红
            declared_v = doc.get(field)
            if declared_v != doc_versions[field]:
                errors.append("R7 %s: %s=%r，但 %s 文档控制块实时解析为 %r（版本指针过期 = 把考卷冻结在被取代的合同上）"
                              % (name, field, declared_v, docname, doc_versions[field]))

    ver_line = " / ".join("%s=%s" % (f, doc_versions.get(f, "解析失败")) for f, _ in VERSION_SOURCES)
    print("冻结断言门 | Manifest %d 份（应有 %d）| 快照索引 %d 条 | 规则对象 %d 条"
          % (len(manifests), expected, len(snap_idx), len(rule_idx)))
    print("真源版本（实时解析）| %s" % ver_line)
    if errors:
        print("\nGATE_RED —— 以下 %d 条红线未清，物理拒绝送签：\n" % len(errors))
        for n, e in enumerate(errors, 1):
            print("  %2d. %s" % (n, e))
        print("\n（占位未清或核验不一致时送签 = 带着占位签字的假绿，本门即为此而设）")
        return 1
    print("\nGATE_GREEN —— 七条红线全清（齐套 / 零占位残留 / Schema 过 / snapshot_hash 实算一致且归属正确 /"
          " hard_rule_refs 全部解析到 A.9.1 全等的规则对象 / 签字三件套可解析 / 版本指针与真源实时一致）")
    print("GATE_GREEN ≠ 已签字生效：本门只证明占位清零与机械核验一致，")
    print("  不代表 Founder 已签字（approved_by/approved_at 仍须真实签署），也不代表案例内容质量合格。")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # 被 | head / | less 截断时不抛栈；退出码仍标记异常
        os._exit(1)
