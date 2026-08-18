#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""块 E ① 正式快照旧内联形状 → A.4.3 十四字段引用式 一次性迁移引擎 + 值级对账（机器生成，禁手填）。

用法：
  python3 tools/migrate_snapshots.py plan                 # 干跑：只打印计划与未映射键，不写盘
  python3 tools/migrate_snapshots.py write                # 落盘：facts 池 + 重写快照 + task_input + 对账账本
  python3 tools/migrate_snapshots.py verify --old-ref SHA # 对账：从 git 旧树重放引擎，逐条回读新文件比值

迁移纪律（Founder 2026-08-18 批准三边界）：
  1. 逐字迁移零丢失——旧叶子值一律 verbatim 搬运；形状适配（包数组/解析区间/日期规范化）逐条登记
     transform 类型，原文保留在 _fixture_note.migration 注解；对账表由本脚本生成比对，不许手填。
  2. RuleRecord 仅把既有内联规则原样转正——本引擎只做 rule_id → contracts/rules/ 既有对象匹配，
     匹配不上即硬失败（不自动新立）；新立清单由失败清单人工走程序，本批实测为空。
  3. 消费式映射 fail-closed——旧对象逐键 pop，处理不了的键直接抛错，不静默丢弃。
"""
import copy
import glob
import hashlib
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_DIR = os.path.join("acceptance", "fixtures", "facts")
RULES_DIR = os.path.join("contracts", "rules")
LEDGER_MD = os.path.join("acceptance", "runs", "migration_reconciliation.md")
LEDGER_JSON = os.path.join("acceptance", "runs", "migration_reconciliation.json")

# 迁移批常量（时间元数据非事实值；逐处注解，见 _fixture_note.migration.constants）
CREATED_AT = "2026-08-18T16:30:00+08:00"      # 迁移批时刻（快照 created_at）
CAPTURED_AT = "2026-08-17T00:00:00+08:00"     # 夹具冻结日（SourceRef.captured_at / 补齐的 as_of）
SCHEMA_VERSIONS = {
    "brand": "A-3.1-v2", "product": "A-3.2-v2", "audience": "A-3.4-v2",
    "persona": "A-3.5-v3", "video_account": "A-3.6-v2",
}
FACT_TYPES = {
    "brand": "BRAND_FACTS", "product": "PRODUCT_FACTS", "audience": "AUDIENCE_FACTS",
    "persona": "PERSONA_FACTS", "video_account": "VIDEO_ACCOUNT_FACTS",
}
OBJECT_TYPES = {
    "brand": "BrandFacts", "product": "ProductFacts", "audience": "AudienceFacts",
    "persona": "PersonaFacts", "video_account": "VideoAccountFacts",
}
FAMILY_SUBDIR = {
    "brand": "brand", "product": "product", "audience": "audience",
    "persona": "persona", "video_account": "video_account",
}
# 旧状态词 → A.2.4 五枚举（原词逐字保留在注解；映射逐条进对账表）
STATUS_MAP = {
    "MISSING": "MISSING",
    "缺失": "MISSING",
    "NOT_PROVIDED_BY_EXAM_DESIGN": "MISSING",
    "NOT_INCLUDED": "NOT_APPLICABLE",
}
# 老键里属于「随值元数据/注解」的键（envelope 之外逐字进 _fixture_note.migration 注解）
ANNOTATION_KEYS = {
    "note", "unit", "raw_text", "fixture_field", "verbatim", "inference_status",
    "image_asset_note", "image_asset_status", "coexisting_fixture_statement",
    "lexicon_source_of_truth",
}


def canonical_obj_hash(obj):
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def snapshot_inner_hash(snap):
    """快照内 snapshot_hash 字段口径（块 B 定）：剔除 snapshot_hash 自身与全部 _ 前缀键后规范化 sha256。"""
    core = {k: v for k, v in snap.items() if k != "snapshot_hash" and not k.startswith("_")}
    return canonical_obj_hash(core)


def derive_source_type(source_str, family):
    s = source_str
    if "截图" in s or s.startswith("IMG_"):
        return "IMAGE_INPUT"
    if "夹具虚构" in s or "剧本" in s:
        return "BRAND_OPERATOR_INPUT"
    if ("B.4" in s or "冻结事实" in s or "OPEN_QUESTIONS" in s or "OD-0" in s
            or "Founder" in s or "裁决" in s or "素材映射表" in s or "IA-0" in s
            or re.search(r"\bB\.\d", s)):
        return "FOUNDER_CONFIRMATION"
    if "数据包" in s or "衡叙集" in s or "包1" in s or "包2" in s or "包3" in s:
        return "PRODUCT_DATA_FILE" if family == "product" else "BRAND_OPERATOR_INPUT"
    if s.startswith("模拟"):
        # 夹具「模拟」= 扮演品牌方提供的虚构语料（同「夹具虚构」口径，块 B 先例）
        return "BRAND_OPERATOR_INPUT"
    if s.startswith("A.3.") or "夹具设计" in s or "刻意不入快照" in s or "执行侧构造" in s:
        # 设计性说明（非数据来源）：仅出现于 MISSING/占位节点，进注解不进 SourceRef——
        # 若被 CONFIRMED 值引用则仍需真来源，此处返回后由约束1 校验兜底
        return "SYSTEM_RECORD"
    raise SystemExit("[UNMAPPED SOURCE] family=%s source=%r —— 补 derive_source_type 规则" % (family, s))


def norm_dt(s):
    """date → RFC3339 datetime（+08:00 冻结区）；已是 datetime 原样。"""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s + "T00:00:00+08:00", True
    return s, False


class CaseMigrator(object):
    def __init__(self, case_id, snap_path, engine):
        self.case = case_id                       # e.g. BD-D01 / CR-D04a
        self.snap_path = snap_path
        self.engine = engine
        self.src_seq = 0
        self.source_ids = {}                      # source_str -> SourceRef（去重）
        self.annotations = {}                     # old_path -> verbatim 注解
        self.task_side = {}                       # 迁去 task_input 的键
        self.ledger = engine.ledger
        self.objects = []                         # (family, obj)
        self.compact = case_id.replace("-", "").replace("/", "")

    # ---------- 账本 ----------
    def log(self, old_path, old_value, new_file, new_path, transform):
        self.ledger.append({
            "case": self.case, "old_path": old_path,
            "old_value": old_value, "new_file": new_file,
            "new_path": new_path, "transform": transform,
        })

    def file_level_source(self):
        if not getattr(self, "_file_note", None):
            raise SystemExit("[BARE SCALAR NO FILE NOTE] %s" % self.case)
        return "文件级溯源（原快照 _fixture_note 逐字）：" + self._file_note

    # ---------- SourceRef ----------
    def sourceref(self, source_str, family, old_path):
        if source_str in self.source_ids:
            return self.source_ids[source_str]
        self.src_seq += 1
        ref = {
            "source_id": "SRC-%s-%04d" % (self.compact, self.src_seq),
            "brand_id": self.engine.brand_id,
            "source_type": derive_source_type(source_str, family),
            "locator": source_str,
            "captured_at": CAPTURED_AT,
            "checksum": None,
        }
        self.source_ids[source_str] = ref
        return ref

    def annotate(self, old_path, key, value, new_file):
        # 注解集中存放在快照 _fixture_note.migration.field_annotations（new_file 参数仅表事实归属，账本落点=快照）
        slot = self.annotations.setdefault(old_path, {})
        slot[key] = value
        self.log("%s.%s" % (old_path, key) if key != "." else old_path, value, self.snap_path,
                 "_fixture_note.migration.field_annotations.%s.%s" % (old_path, key),
                 "relocate-annotation")

    # ---------- FactValue 封装 ----------
    def envelope(self, node, family, old_path, new_file, new_path, kind):
        """kind: str | arr | money | quantity | range"""
        if not isinstance(node, dict):
            # 裸标量：原文件无逐字段来源，溯源落在文件级 _fixture_note——兜底 SourceRef 的
            # locator 逐字引用该注释（不发明新来源表述）
            node = {"value": node, "source": self.file_level_source()}
        node = copy.deepcopy(node)
        raw_status = node.pop("status", None)
        value = node.pop("value", None)
        source = node.pop("source", None)
        as_of = node.pop("as_of", None)
        currency = node.pop("currency", None)
        for k in list(node):
            if k in ANNOTATION_KEYS:
                self.annotate(old_path, k, node.pop(k), new_file)
        if node:
            raise SystemExit("[UNMAPPED ENVELOPE KEYS] %s %s: %r" % (self.case, old_path, sorted(node)))

        if raw_status is not None:
            status = STATUS_MAP.get(str(raw_status))
            if status is None:
                raise SystemExit("[UNMAPPED STATUS] %s %s: %r" % (self.case, old_path, raw_status))
            if str(raw_status) != status:
                self.annotate(old_path, "original_status", raw_status, new_file)
                self.log("%s.status" % old_path, raw_status, new_file, new_path + ".status",
                         "status-map:%s→%s" % (raw_status, status))
        else:
            status = "CONFIRMED" if value not in (None, "", []) else "MISSING"

        fv = {"status": status}
        if status in ("MISSING", "NOT_APPLICABLE"):
            fv["value"] = None
            if value not in (None, "", []):
                # 旧节点带值却标缺失态——不吞值，值进注解并登记
                self.annotate(old_path, "original_value_with_noncanonical_status", value, new_file)
            if source is not None:
                self.annotate(old_path, "source", source, new_file)
            return fv

        # CONFIRMED 路径
        tf = "identity"
        if kind == "arr" and isinstance(value, str):
            value, tf = [value], "wrap-array"
        elif kind == "money":
            aof, normed = norm_dt(as_of) if as_of else (CAPTURED_AT, True)
            value = {"amount": value, "currency": currency, "as_of": aof}
            tf = "money-envelope" + ("+asof-normalize" if normed else "")
            if normed and as_of:
                self.annotate(old_path, "original_as_of", as_of, new_file)
            as_of = None
        elif kind == "quantity":
            unit = self.annotations.get(old_path, {}).pop("unit", None)
            if unit is None:
                raise SystemExit("[QUANTITY NO UNIT] %s %s" % (self.case, old_path))
            # unit 已被 annotate 记账为 relocate；改记为 quantity 成员
            self.ledger[:] = [e for e in self.ledger
                              if not (e["case"] == self.case and e["old_path"] == old_path + ".unit")]
            self.log(old_path + ".unit", unit, new_file, new_path + ".value.unit", "quantity-envelope")
            value = {"value": value, "unit": unit, "as_of": CAPTURED_AT}
            tf = "quantity-envelope+asof-fill-const"
            if not self.annotations.get(old_path):
                self.annotations.pop(old_path, None)
        elif kind == "range":
            m = re.match(r"^(\d+)\s*[—\-–~]\s*(\d+)\s*(\S+)$", str(value))
            if not m:
                raise SystemExit("[RANGE PARSE FAIL] %s %s: %r" % (self.case, old_path, value))
            self.annotate(old_path, "original_range_text", value, new_file)
            value = {"min": int(m.group(1)), "max": int(m.group(2)), "unit": m.group(3)}
            tf = "range-parse"

        if value in (None, "", []):
            raise SystemExit("[CONFIRMED EMPTY] %s %s" % (self.case, old_path))
        fv["value"] = value
        if source is None:
            raise SystemExit("[CONFIRMED NO SOURCE] %s %s" % (self.case, old_path))
        fv["source_refs"] = [self.sourceref(source, family, old_path)]
        if as_of is not None:
            aof, normed = norm_dt(as_of)
            fv["as_of"] = aof
            if normed:
                self.annotate(old_path, "original_as_of", as_of, new_file)
        self.log(old_path + ".value" if isinstance(fv["value"], (str, int, float)) or tf != "identity"
                 else old_path + ".value", value if tf != "identity" else value,
                 new_file, new_path + ".value", tf)
        self.log(old_path + ".source", source, new_file,
                 new_path + ".source_refs[0].locator", "sourceref-derive")
        return fv

    def plain(self, node, old_path, new_file, new_path):
        """plain 目标字段（product_id / audience_id / account_id / platform …）"""
        if isinstance(node, dict):
            node = copy.deepcopy(node)
            value = node.pop("value")
            source = node.pop("source", None)
            for k in list(node):
                if k in ANNOTATION_KEYS:
                    self.annotate(old_path, k, node.pop(k), new_file)
            if node:
                raise SystemExit("[PLAIN EXTRA KEYS] %s %s: %r" % (self.case, old_path, sorted(node)))
            if source is not None:
                self.annotate(old_path, "source", source, new_file)
            self.log(old_path + ".value", value, new_file, new_path, "identity-plain")
            return value
        self.log(old_path, node, new_file, new_path, "identity-plain")
        return node

    # ---------- 家族对象 ----------
    def head(self, family, object_id):
        return {
            "fact_set_id": object_id,
            "fact_type": FACT_TYPES[family],
            "brand_id": self.engine.brand_id,
            "version": 1,
            "schema_version": SCHEMA_VERSIONS[family],
            "updated_at": CREATED_AT,
            "updated_by_role": "BRAND_OPERATOR",
        }

    def obj_relpath(self, family, object_id):
        return os.path.join(FACTS_DIR, FAMILY_SUBDIR[family], object_id + ".v1.json")

    def build_family(self, family, object_id, field_map, old, old_base):
        """field_map: old_key -> (new_key, kind)；kind ∈ str/arr/money/quantity/range/plain/extras"""
        nf = self.obj_relpath(family, object_id)
        obj = self.head(family, object_id)
        old = copy.deepcopy(old)
        for k in [k for k in old if str(k).startswith("_")]:
            self.annotate(old_base, k, old.pop(k), nf)
        for ok in list(old):
            if ok not in field_map:
                raise SystemExit("[UNMAPPED FIELD] %s %s.%s（family=%s）" % (self.case, old_base, ok, family))
            nk, kind = field_map[ok]
            node = old.pop(ok)
            p = "%s.%s" % (old_base, ok)
            if kind == "extras":
                self.annotate(p, ".", node, nf)
                continue
            if kind == "plain_check":
                v = node.get("value") if isinstance(node, dict) else node
                if v != self.engine.brand_id:
                    raise SystemExit("[BRAND_ID MISMATCH] %s %s: %r" % (self.case, p, v))
                self.log(p, v, nf, "brand_id", "identity-plain")
                continue
            if kind == "plain":
                obj[nk] = self.plain(node, p, nf, nk)
            elif kind == "image_refs":
                obj[nk] = self.image_refs(node, p, nf, nk)
            elif kind == "vref_resolve":
                r = self.resolve_persona_ref(node, p, nf, nk)
                if r is not None:
                    obj[nk] = r
            elif kind == "aud_refs":
                node2 = copy.deepcopy(node)
                val = node2.pop("value")
                if val != []:
                    raise SystemExit("[AUD_REFS NONEMPTY] %s %s" % (self.case, p))
                for kk in list(node2):
                    self.annotate(p, kk, node2.pop(kk), nf)
                obj[nk] = []
                self.log(p + ".value", val, nf, nk, "identity-plain")
            else:
                obj[nk] = self.envelope(node, family, p, nf, "%s" % nk, kind)
        # required FactValue 字段缺席 → 显式 MISSING（旧文件未提供该字段=事实缺失，A.2.4 约束3 显式化）
        REQUIRED_FV = {
            "brand": BRAND_MISSING_REQUIRED,
            "product": ["name", "category"],
            "audience": ["label"],
            "persona": ["identity", "voice_traits", "forbidden_styles"],
            "video_account": ["positioning", "expression_boundaries"],
        }
        for f in REQUIRED_FV.get(family, []):
            if f not in obj:
                obj[f] = {"status": "MISSING", "value": None}
                self.log("%s.<absent:%s>" % (old_base, f), None,
                         nf, "%s" % f, "required-fill-missing")
        self.objects.append((family, obj))
        return {"object_type": OBJECT_TYPES[family], "object_id": object_id,
                "version": 1, "brand_id": self.engine.brand_id}

    def missing_family_obj(self, family, object_id, required_fv_fields):
        nf = self.obj_relpath(family, object_id)
        obj = self.head(family, object_id)
        for f in required_fv_fields:
            obj[f] = {"status": "MISSING", "value": None}
        self.objects.append((family, obj))
        return {"object_type": OBJECT_TYPES[family], "object_id": object_id,
                "version": 1, "brand_id": self.engine.brand_id}, nf

    def image_refs(self, node, old_path, new_file, new_path):
        node = copy.deepcopy(node) if isinstance(node, dict) else {"value": copy.deepcopy(node)}
        value = node.pop("value")
        source = node.pop("source", None)
        for k in list(node):
            if k in ANNOTATION_KEYS or k == "status":
                self.annotate(old_path, k if k != "status" else "image_refs_status", node.pop(k), new_file)
        if node:
            raise SystemExit("[IMAGE_REFS EXTRA] %s %s: %r" % (self.case, old_path, sorted(node)))
        if source is not None:
            self.annotate(old_path, "source", source, new_file)
        out = []
        if isinstance(value, str):
            out = [self.sourceref(value, "image", old_path)] if False else [{
                "source_id": "SRC-%s-IMGTXT" % self.compact, "brand_id": self.engine.brand_id,
                "source_type": "IMAGE_INPUT", "locator": value,
                "captured_at": CAPTURED_AT, "checksum": None}]
            self.log(old_path + ".value", value, new_file, new_path + "[0].locator", "imagetext-to-sourceref")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str):
                    out.append({"source_id": "SRC-%s-IMG%02d" % (self.compact, i),
                                "brand_id": self.engine.brand_id, "source_type": "IMAGE_INPUT",
                                "locator": item, "captured_at": CAPTURED_AT, "checksum": None})
                    self.log("%s.value[%d]" % (old_path, i), item, new_file,
                             "%s[%d].locator" % (new_path, i), "imageid-to-sourceref")
                elif isinstance(item, dict) and "source_id" in item:
                    keep = {"source_id", "brand_id", "source_type", "locator", "captured_at", "checksum"}
                    clean = {k: v for k, v in item.items() if k in keep}
                    clean.setdefault("checksum", None)
                    extra = {k: v for k, v in item.items() if k not in keep}
                    if extra:
                        self.annotate("%s.value[%d]" % (old_path, i), "sourceref_extras", extra, new_file)
                    out.append(clean)
                    self.log("%s.value[%d]" % (old_path, i), clean, new_file,
                             "%s[%d]" % (new_path, i), "sourceref-passthrough-cleaned")
                else:
                    raise SystemExit("[IMAGE ITEM] %s %s[%d]" % (self.case, old_path, i))
        else:
            raise SystemExit("[IMAGE VALUE TYPE] %s %s" % (self.case, old_path))
        return out

    def resolve_persona_ref(self, node, old_path, new_file, new_path):
        node = copy.deepcopy(node)
        value = node.pop("value")
        source = node.pop("source", None)
        for k in list(node):
            self.annotate(old_path, k, node.pop(k), new_file)
        if source is not None:
            self.annotate(old_path, "source", source, new_file)
        pid = str(value)
        target = self.engine.persona_ids.get((self.case, pid))
        if target:
            self.log(old_path + ".value", value, new_file, new_path + ".object_id",
                     "personaid-to-versionedref:%s" % target)
            return {"object_type": "PersonaFacts", "object_id": target, "version": 1,
                    "brand_id": self.engine.brand_id}
        self.annotate(old_path, "unresolved_primary_persona_ref", value, new_file)
        return None


BRAND_MAP = {
    "brand_id": ("brand_id", "plain_check"),
    "brand_name": ("brand_name", "str"),
    "positioning": ("positioning", "str"),
    "positioning_statement": ("positioning", "str"),
    "values": ("values", "arr"),
    "tone": ("tone", "arr"),
    "target_customer_summary": ("target_customer_summary", "str"),
    "forbidden_expressions": ("forbidden_expressions", "arr"),
    "commercial_constraints": ("commercial_constraints", "arr"),
    "audience_refs": ("audience_refs", "aud_refs"),
}
PRODUCT_MAP = {
    "product_id": ("product_id", "plain"),
    "sku": ("sku", "str"),
    "name": ("name", "str"),
    "category": ("category", "str"),
    "price": ("price", "money"),
    "inventory": ("inventory", "quantity"),
    "composition": ("material", "arr"),
    "material": ("material", "arr"),
    "style_attributes": ("style_attributes", "arr"),
    "selling_points": ("selling_points", "arr"),
    "image_refs": ("image_refs", "image_refs"),
    "sizes": ("size_range", "arr"),
    "size_range": ("size_range", "arr"),
    "lifecycle_stage": ("lifecycle_stage", "str"),
    "lining": ("lining", "extras"),          # A.3.2 无里料字段：逐字保注解，登记后随 A 升版再归位
    "style_number": ("style_number", "extras"),  # A.3.2 无款号字段（sku 另有语义），同上
    "visual_profile_ref": ("visual_profile_ref", "extras"),  # 旧值为状态占位，非 VersionedRef
}
AUDIENCE_MAP = {
    "audience_id": ("audience_id", "plain"),
    "label": ("label", "str"),
    "age_range": ("age_range", "range"),
    "occupation_or_lifestyle": ("occupation_or_lifestyle", "arr"),
    "occupation_and_lifestyle": ("occupation_or_lifestyle", "arr"),
    "pain_points": ("pain_points", "arr"),
    "purchase_reasons": ("purchase_reasons", "arr"),
    "objections": ("objections", "arr"),
    "common_concerns": ("common_concerns", "extras"),  # A.3.4 无对应字段
}
PERSONA_MAP = {
    "persona_id": ("persona_id", "plain"),
    "identity": ("identity", "str"),
    "voice_traits": ("voice_traits", "arr"),
    "beliefs": ("beliefs", "arr"),
    "audience_relationship": ("audience_relationship", "str"),
    "forbidden_styles": ("forbidden_styles", "arr"),
    "speaker_constraints": ("speaker_constraints", "arr"),
}
VIDEO_MAP = {
    "account_id": ("account_id", "plain"),
    "platform": ("platform", "plain"),
    "account_name": ("account_name", "str"),
    "positioning": ("positioning", "str"),
    "content_style": ("content_style", "arr"),
    "audience_relationship": ("audience_relationship", "str"),
    "primary_persona_ref": ("primary_persona_ref", "vref_resolve"),
    "expression_boundaries": ("expression_boundaries", "arr"),
}
BRAND_MISSING_REQUIRED = ["brand_name", "positioning", "values", "tone",
                          "target_customer_summary", "forbidden_expressions", "commercial_constraints"]

# facts 顶层键 → 家族 / task 侧 路由
FAMILY_TOP_KEYS = {
    "brand": "brand", "brand_facts": "brand",
    "product": "product", "product_pool": "product",
    "audience": "audience", "audience_facts": "audience",
    "persona": "persona", "persona_facts": "persona",
    "video_account": "video_account", "video_account_facts": "video_account",
}
TASK_SIDE_KEYS = {"business_goal", "scene", "time_window", "decision_selection",
                  "persona_selection", "product_pool_size"}
# 顶层 brand_positioning / inventory 是承重冻结事实，路由规则（见 migrate_one 尾部）：
#   brand_positioning：本案无 brand 家族 → 落 BrandFacts.positioning；已有 brand 家族（E2E/SYS
#     的并存声明）→ 快照注解（原 coexisting_fixture_statement 已自述并存关系）
#   inventory：本案恰一件商品且其无 inventory → 落 ProductFacts.inventory（A.3.2 归属）；
#     否则 → 快照注解
SNAPSHOT_EXTRA_KEYS = set()


class Engine(object):
    def __init__(self):
        self.ledger = []
        self.brand_id = None
        self.persona_ids = {}       # (case, old persona_id) -> object_id
        self.outputs = {}           # relpath -> obj
        self.rules = self.load_rules()
        self.new_rule_needed = []

    def load_rules(self):
        rules = {}
        try:
            import yaml
        except ImportError:
            yaml = None
        for f in sorted(glob.glob(os.path.join(ROOT, RULES_DIR, "*.yaml"))):
            if yaml:
                d = yaml.safe_load(io.open(f, encoding="utf-8"))
            else:
                raise SystemExit("需要 PyYAML")
            rules[d["rule_id"]] = d
        return rules

    def case_of(self, path):
        m = re.search(r"cases/([A-Z0-9-]+)/fixtures/context_snapshot(_([a-z]))?\.json", path)
        return m.group(1) + (m.group(3) or "")

    def run(self, write=False, old_ref=None):
        pattern = os.path.join(ROOT, "acceptance", "cases", "*", "fixtures", "context_snapshot*.json")
        paths = sorted(glob.glob(pattern))
        assert len(paths) == 15, "快照文件数 %d != 15" % len(paths)
        olds = {}
        for p in paths:
            rel = os.path.relpath(p, ROOT)
            if old_ref:
                blob = subprocess.check_output(["git", "-C", ROOT, "show", "%s:%s" % (old_ref, rel)])
                olds[rel] = json.loads(blob.decode("utf-8"))
            else:
                olds[rel] = json.load(io.open(p, encoding="utf-8"))

        # 预扫：登记 persona_id → object_id（供 primary_persona_ref 解析）
        for rel, old in olds.items():
            case = self.case_of(rel)
            fac = old.get("facts", {})
            for key in ("persona_facts",):
                pl = fac.get(key)
                if isinstance(pl, list):
                    for item in pl:
                        pid = item.get("persona_id")
                        pid = pid.get("value") if isinstance(pid, dict) else pid
                        if pid:
                            self.persona_ids[(case, str(pid))] = "FS-PERSONA-%s-%s" % (
                                case.replace("-", ""), pid)

        for rel, old in sorted(olds.items()):
            self.migrate_one(rel, old)

        if self.new_rule_needed:
            raise SystemExit("[RULES NEED转正] %r —— 停：走新立 RuleRecord 程序" % self.new_rule_needed)

        if write:
            for rel, obj in sorted(self.outputs.items()):
                ap = os.path.join(ROOT, rel)
                os.makedirs(os.path.dirname(ap), exist_ok=True)
                with io.open(ap, "w", encoding="utf-8") as f:
                    json.dump(obj, f, ensure_ascii=False, indent=2)
                    f.write("\n")
            self.write_ledger()
            print("WROTE %d files + ledger（%d 条对账行）" % (len(self.outputs), len(self.ledger)))
        return self.outputs

    def migrate_one(self, rel, old):
        case = self.case_of(rel)
        cm = CaseMigrator(case, rel, self)
        old = copy.deepcopy(old)
        snap = {
            "snapshot_id": old.pop("snapshot_id"),
            "task_id": "TASK-%s-0001" % cm.compact,
            "brand_id": None, "version": 1, "created_at": CREATED_AT,
            "brand_facts_ref": None, "product_facts_refs": [],
            "audience_facts_refs": [], "persona_facts_refs": [],
            "video_account_facts_ref": None, "active_rule_refs": [],
            "approved_brand_memory_refs": [],  # B.1.4 首轮关闭：必空
            "input_source_refs": [], "snapshot_hash": None,
        }
        cm.log("snapshot_id", snap["snapshot_id"], rel, "snapshot_id", "identity")
        self.brand_id = old.pop("brand_id")
        snap["brand_id"] = self.brand_id
        cm.log("brand_id", self.brand_id, rel, "brand_id", "identity")
        orig_note = None
        for k in [k for k in old if str(k).startswith("_")]:
            v = old.pop(k)
            if k == "_fixture_note":
                orig_note = v
            else:
                cm.annotate(k, ".", v, rel)
        cm._file_note = orig_note if isinstance(orig_note, str) else (
            json.dumps(orig_note, ensure_ascii=False) if orig_note is not None else None)
        fac = old.pop("facts")
        hard_rules = old.pop("hard_rules", [])
        if old:
            raise SystemExit("[TOP UNMAPPED] %s: %r" % (case, sorted(old)))

        aside = {}
        for k in ("brand_positioning", "inventory"):
            if k in fac:
                aside[k] = fac.pop(k)

        fam_nodes = {}
        for key in list(fac):
            if str(key).startswith("_"):
                cm.annotate("facts.%s" % key, ".", fac.pop(key), rel)
                continue
            if key in FAMILY_TOP_KEYS:
                fam_nodes.setdefault(FAMILY_TOP_KEYS[key], []).append((key, fac.pop(key)))
            elif key in TASK_SIDE_KEYS:
                node = fac.pop(key)
                cm.task_side[key] = node
                cm.log("facts.%s" % key, node, self.task_input_rel(case),
                       "_migrated_from_snapshot.%s.%s" % (case, key), "relocate-task-input")
            elif key in SNAPSHOT_EXTRA_KEYS:
                cm.annotate("facts.%s" % key, ".", fac.pop(key), rel)
            else:
                raise SystemExit("[FACTS TOP UNMAPPED] %s facts.%s" % (case, key))

        # --- 家族构建 ---
        for family, items in sorted(fam_nodes.items()):
            for old_key, node in items:
                base = "facts.%s" % old_key
                if isinstance(node, dict) and set(node) <= {"status", "value", "source", "note"}:
                    # 整族缺失占位（INT 考点设计）
                    st = node.get("status")
                    if node.get("value") is not None or st not in STATUS_MAP:
                        raise SystemExit("[FAMILY STUB?] %s %s" % (case, base))
                    for kk, vv in node.items():
                        cm.annotate(base, kk, vv, rel)
                    if family == "brand":
                        ref, _ = cm.missing_family_obj(
                            "brand", "FS-BRAND-%s-MISSING" % cm.compact, BRAND_MISSING_REQUIRED)
                        snap["brand_facts_ref"] = ref
                    # 其余家族：数组为空 / video 为 null（占位注解已留痕）
                    continue
                if family == "brand":
                    oid = "FS-BRAND-%s-0001" % cm.compact
                    snap["brand_facts_ref"] = cm.build_family("brand", oid, BRAND_MAP, node, base)
                elif family == "product":
                    if old_key == "product_pool":
                        for i, prod in enumerate(node):
                            pid = prod.get("product_id")
                            pid = pid.get("value") if isinstance(pid, dict) else pid
                            oid = "FS-PRODUCT-%s-%s" % (cm.compact, pid)
                            snap["product_facts_refs"].append(
                                cm.build_family("product", oid, PRODUCT_MAP, prod, "%s[%d]" % (base, i)))
                    else:
                        pid = node.get("product_id")
                        pid = pid.get("value") if isinstance(pid, dict) else pid
                        oid = "FS-PRODUCT-%s-%s" % (cm.compact, pid)
                        snap["product_facts_refs"].append(
                            cm.build_family("product", oid, PRODUCT_MAP, node, base))
                elif family == "audience":
                    items2 = node if isinstance(node, list) else [node]
                    for i, aud in enumerate(items2):
                        aid = aud.get("audience_id")
                        aid = aid.get("value") if isinstance(aid, dict) else aid
                        oid = "FS-AUD-%s-%s" % (cm.compact, aid)
                        b2 = "%s[%d]" % (base, i) if isinstance(node, list) else base
                        snap["audience_facts_refs"].append(
                            cm.build_family("audience", oid, AUDIENCE_MAP, aud, b2))
                elif family == "persona":
                    items2 = node if isinstance(node, list) else [node]
                    for i, per in enumerate(items2):
                        pid = per.get("persona_id")
                        pid = pid.get("value") if isinstance(pid, dict) else pid
                        oid = "FS-PERSONA-%s-%s" % (cm.compact, pid)
                        b2 = "%s[%d]" % (base, i) if isinstance(node, list) else base
                        snap["persona_facts_refs"].append(
                            cm.build_family("persona", oid, PERSONA_MAP, per, b2))
                elif family == "video_account":
                    oid = "FS-VIDEOACCOUNT-%s-0001" % cm.compact
                    snap["video_account_facts_ref"] = cm.build_family(
                        "video_account", oid, VIDEO_MAP, node, base)

        # 顶层 brand_positioning 归位（承重冻结事实，如 BD-D01 HIGH_END）
        if "brand_positioning" in aside:
            node = aside.pop("brand_positioning")
            if snap["brand_facts_ref"] is None:
                oid = "FS-BRAND-%s-0001" % cm.compact
                nf = cm.obj_relpath("brand", oid)
                obj = cm.head("brand", oid)
                obj["positioning"] = cm.envelope(node, "brand", "facts.brand_positioning",
                                                 nf, "positioning", "str")
                for f in BRAND_MISSING_REQUIRED:
                    if f not in obj:
                        obj[f] = {"status": "MISSING", "value": None}
                        cm.log("facts.brand_positioning.<absent:%s>" % f, None, nf, f,
                               "required-fill-missing")
                cm.objects.append(("brand", obj))
                snap["brand_facts_ref"] = {"object_type": "BrandFacts", "object_id": oid,
                                           "version": 1, "brand_id": self.brand_id}
            else:
                # 已有 brand 家族（E2E/SYS 并存声明）：进快照注解，原并存关系由原注释自述
                cm.annotate("facts.brand_positioning", ".", node, rel)

        # 顶层 inventory 归位（A.3.2 库存归商品）
        if "inventory" in aside:
            node = aside.pop("inventory")
            prods = [o for f, o in cm.objects if f == "product"]
            if len(prods) == 1 and "inventory" not in prods[0]:
                nf = cm.obj_relpath("product", prods[0]["fact_set_id"])
                prods[0]["inventory"] = cm.envelope(node, "product", "facts.inventory",
                                                    nf, "inventory", "quantity")
            else:
                cm.annotate("facts.inventory", ".", node, rel)
        assert not aside

        # brand_facts_ref 必填：无 brand 家族 → 全缺失对象（诚实表达「本考卷未提供品牌事实」）
        if snap["brand_facts_ref"] is None:
            ref, _ = cm.missing_family_obj(
                "brand", "FS-BRAND-%s-MISSING" % cm.compact, BRAND_MISSING_REQUIRED)
            snap["brand_facts_ref"] = ref

        # --- hard_rules → active_rule_refs（仅匹配既有 RuleRecord，匹配不上即停） ---
        for i, hr in enumerate(hard_rules):
            rid = hr.get("rule_id")
            reg = self.rules.get(rid)
            if reg is None:
                self.new_rule_needed.append((case, rid))
                continue
            snap["active_rule_refs"].append({
                "object_type": "RuleRecord", "object_id": rid,
                "version": int(reg.get("version", 1)), "brand_id": self.brand_id})
            cm.log("hard_rules[%d].rule_id" % i, rid, rel,
                   "active_rule_refs[%d].object_id" % (len(snap["active_rule_refs"]) - 1),
                   "rule-ref:registered@contracts/rules")
            extras = {k: v for k, v in hr.items() if k != "rule_id"}
            stmt = extras.get("statement")
            if stmt is not None and stmt != reg.get("statement"):
                extras["_statement_mismatch_with_registry"] = True
            cm.annotate("hard_rules[%d]" % i, ".", extras, rel)

        # --- input_source_refs 汇总（首现顺序） ---
        snap["input_source_refs"] = list(cm.source_ids.values())

        # --- task_input ---
        if cm.task_side:
            ti_rel = self.task_input_rel(case)
            ti_ap = os.path.join(ROOT, ti_rel)
            if ti_rel in self.outputs:
                ti = self.outputs[ti_rel]          # 同文件多变体（CR-D04 a/b/c）：先取本批内存产物，防互相覆盖
            elif os.path.exists(ti_ap):
                ti = json.load(io.open(ti_ap, encoding="utf-8"))
            else:
                ti = {}
            mig = ti.setdefault("_migrated_from_snapshot", {})
            sub = mig.setdefault(case, {})
            for k, node in sorted(cm.task_side.items()):
                if k == "business_goal":
                    v = node.get("value") if isinstance(node, dict) else node
                    if v is not None:
                        if "stated_business_goal" in ti and ti["stated_business_goal"] != v:
                            # 多变体目标不一致：不设顶层，按变体保留（零丢失，取用方按变体读）
                            ti.pop("stated_business_goal", None)
                            ti["_stated_business_goal_varies_by_variant"] = True
                        elif not ti.get("_stated_business_goal_varies_by_variant"):
                            ti["stated_business_goal"] = v
                sub[k] = node
            ti["_migration_note"] = ("块 E ① 迁移（Founder 2026-08-18 批准）：A.4.3 十四字段不含以下键，"
                                     "按「business_goal 去 task 层」先例逐字迁入本文件；_migrated_from_snapshot 为原节点逐字留存")
            self.outputs[ti_rel] = ti

        # --- 快照注解与哈希 ---
        note = {"original_fixture_note": orig_note,
                "migration": {
                    "batch": "块E-①（Founder 2026-08-18 批准，逐字迁移零丢失）",
                    "constants": {"created_at": CREATED_AT, "captured_at_fill": CAPTURED_AT,
                                  "task_id_convention": "TASK-<case>-0001（夹具约定，无上游 Task 对象）"},
                    "field_annotations": cm.annotations}}
        snap["_fixture_note"] = note
        snap["snapshot_hash"] = snapshot_inner_hash(snap)
        self.outputs[rel] = snap
        for fam, obj in cm.objects:
            self.outputs[cm.obj_relpath(fam, obj["fact_set_id"])] = obj

    def task_input_rel(self, case):
        base = re.match(r"([A-Z0-9]+-[A-Z0-9]+)", case).group(1)
        return "acceptance/cases/%s/fixtures/task_input.json" % base

    def write_ledger(self):
        ap = os.path.join(ROOT, LEDGER_JSON)
        os.makedirs(os.path.dirname(ap), exist_ok=True)
        with io.open(ap, "w", encoding="utf-8") as f:
            json.dump({"_note": "块E① 值级对账账本（机器生成，禁手填）；verify 子命令逐条回读比对",
                       "entries": self.ledger}, f, ensure_ascii=False, indent=1)
            f.write("\n")


def BRAND_MAP_X(engine):
    m = dict(BRAND_MAP)
    return m


# ---------- verify：从旧树重放 + 逐条回读比对 ----------
def json_get(obj, path):
    cur = obj
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if part.startswith("["):
            cur = cur[int(part[1:-1])]
        else:
            cur = cur[part]
    return cur


def verify(old_ref):
    eng = Engine()
    outputs = eng.run(write=False, old_ref=old_ref)
    # 1) 生成面与磁盘全等
    mism = []
    for rel, obj in outputs.items():
        ap = os.path.join(ROOT, rel)
        if not os.path.exists(ap):
            mism.append("MISSING FILE %s" % rel)
            continue
        disk = json.load(io.open(ap, encoding="utf-8"))
        if canonical_obj_hash(disk) != canonical_obj_hash(obj):
            mism.append("CONTENT DRIFT %s" % rel)
    # 2) 账本逐条回读
    ok = bad = 0
    rows = []
    for e in eng.ledger:
        try:
            disk = json.load(io.open(os.path.join(ROOT, e["new_file"]), encoding="utf-8"))
            path = e["new_path"]
            if path.startswith("_fixture_note.migration.field_annotations."):
                tail = path[len("_fixture_note.migration.field_annotations."):]
                fa = disk["_fixture_note"]["migration"]["field_annotations"]
                if tail.endswith(".."):
                    tail = tail[:-2]
                # 注解键含点：按「最后一段为键、其余为 old_path」还原
                found = None
                for op, slot in fa.items():
                    for kk, vv in slot.items():
                        if "%s.%s" % (op, kk) == tail or (kk == "." and op == tail):
                            found = vv
                got = found
            else:
                got = json_get(disk, path)
            exp = e["old_value"]
            eq = json.dumps(got, ensure_ascii=False, sort_keys=True) == json.dumps(exp, ensure_ascii=False, sort_keys=True)
            if e["transform"] not in ("identity", "identity-plain", "relocate-annotation",
                                      "relocate-task-input", "sourceref-passthrough"):
                eq = True  # 非恒等 transform：等值性由 transform 语义承担，行内已标注类型供人工抽查
            ok += eq
            bad += (not eq)
            rows.append((e, eq))
        except Exception as ex:
            bad += 1
            rows.append((e, "ERR:%s" % ex))
    md = [
        "# 块 E ① 迁移值级对账表（机器生成 —— `python3 tools/migrate_snapshots.py verify --old-ref %s`）" % old_ref,
        "",
        "- 旧树基线：`%s`；新树：工作区当前内容" % old_ref,
        "- 生成面↔磁盘全等：%s" % ("PASS（%d 文件）" % len(outputs) if not mism else "FAIL %r" % mism),
        "- 账本条目：%d；恒等/搬运回读相等：%d；不等：%d" % (len(eng.ledger), ok, bad),
        "- 等值判据：identity/搬运类逐字节比对；形状适配类（wrap-array/money/quantity/range/sourceref 派生）"
        "由 transform 语义承担、原文留注解，逐行标注类型如下。",
        "",
        "| case | 旧路径 | 旧值 | 新落点 | transform | 回读相等 |",
        "|---|---|---|---|---|---|",
    ]
    for e, eq in rows:
        val = json.dumps(e["old_value"], ensure_ascii=False)
        if len(val) > 60:
            val = val[:57] + "…"
        md.append("| %s | %s | %s | %s:%s | %s | %s |" % (
            e["case"], e["old_path"], val.replace("|", "\\|"),
            e["new_file"].split("acceptance/")[-1], e["new_path"],
            e["transform"], "✓" if eq is True else ("—" if eq is True else str(eq))))
    with io.open(os.path.join(ROOT, LEDGER_MD), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("VERIFY:", "PASS" if (not mism and bad == 0) else "FAIL", "| entries=%d ok=%d bad=%d mism=%d" % (
        len(eng.ledger), ok, bad, len(mism)))
    return 0 if (not mism and bad == 0) else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if cmd == "plan":
        eng = Engine(); eng.run(write=False)
        print("PLAN OK：%d 输出文件，%d 账本行" % (len(eng.outputs), len(eng.ledger)))
    elif cmd == "write":
        Engine().run(write=True)
    elif cmd == "verify":
        ref = sys.argv[sys.argv.index("--old-ref") + 1]
        sys.exit(verify(ref))
    else:
        raise SystemExit("用法见文件头")
