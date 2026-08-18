# -*- coding: utf-8 -*-
"""事实对象存取（文件级）。

存储布局（块 E ① 迁移落成的共享池）：
  acceptance/fixtures/facts/<family>/<object_id>.v<version>.json   五族事实对象
  contracts/rules/<rule_id>.yaml                                   RuleRecord（A.9.1）

同 ID 同版本禁覆盖（块 E ③ R5 的存取层执行面）：索引构建时同一
(object_type, object_id, version) 出现两个文件即抛错，不择一。
BrandMemory：B.1.4 首轮关闭，无存储目录；任何 BrandMemory 引用在 store 层直接判无法解析。
"""
import glob
import io
import json
import os

OBJECT_TYPE_DIRS = {
    "BrandFacts": "brand",
    "ProductFacts": "product",
    "AudienceFacts": "audience",
    "PersonaFacts": "persona",
    "VideoAccountFacts": "video_account",
}
FACT_TYPE_BY_OBJECT_TYPE = {
    "BrandFacts": "BRAND_FACTS", "ProductFacts": "PRODUCT_FACTS",
    "AudienceFacts": "AUDIENCE_FACTS", "PersonaFacts": "PERSONA_FACTS",
    "VideoAccountFacts": "VIDEO_ACCOUNT_FACTS",
}


class FactResolutionError(Exception):
    """引用解析失败（悬空引用 / 身份不符 / 撞车 / 非法状态）——fail-closed，不降级。"""


def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FactStore(object):
    def __init__(self, facts_root=None, rules_root=None):
        root = _repo_root()
        self.facts_root = facts_root or os.path.join(root, "acceptance", "fixtures", "facts")
        self.rules_root = rules_root or os.path.join(root, "contracts", "rules")
        self._index = None
        self._rules = None

    # ---------- 索引 ----------
    def index(self):
        if self._index is None:
            idx = {}
            for otype, sub in OBJECT_TYPE_DIRS.items():
                for p in sorted(glob.glob(os.path.join(self.facts_root, sub, "*.json"))):
                    obj = json.load(io.open(p, encoding="utf-8"))
                    oid = obj.get("fact_set_id")
                    ver = obj.get("version")
                    if obj.get("fact_type") != FACT_TYPE_BY_OBJECT_TYPE[otype]:
                        raise FactResolutionError(
                            "对象 fact_type=%r 与所在族目录 %s 不符：%s" % (obj.get("fact_type"), sub, p))
                    key = (otype, oid, ver)
                    if key in idx:
                        raise FactResolutionError(
                            "同 ID 同版本撞车（禁覆盖）：%r 同时落在 %s 与 %s" % (key, idx[key][0], p))
                    idx[key] = (p, obj)
            self._index = idx
        return self._index

    def rules(self):
        if self._rules is None:
            import yaml
            rules = {}
            for p in sorted(glob.glob(os.path.join(self.rules_root, "*.yaml"))):
                d = yaml.safe_load(io.open(p, encoding="utf-8"))
                key = (d.get("rule_id"), int(d.get("version", 1)))
                if key in rules:
                    raise FactResolutionError("RuleRecord 同 ID 同版本撞车：%r" % (key,))
                rules[key] = d
            self._rules = rules
        return self._rules

    # ---------- 解析 ----------
    def load(self, ref):
        """VersionedRef → 对象。身份四字段逐项核对，任何不符即 FactResolutionError。"""
        for f in ("object_type", "object_id", "version", "brand_id"):
            if f not in ref:
                raise FactResolutionError("VersionedRef 缺 %s：%r" % (f, ref))
        otype = ref["object_type"]
        if otype == "RuleRecord":
            rec = self.rules().get((ref["object_id"], int(ref["version"])))
            if rec is None:
                raise FactResolutionError("悬空规则引用：%r（contracts/rules/ 无此 rule_id+version）" % (ref,))
            if rec.get("brand_id") != ref["brand_id"]:
                raise FactResolutionError("规则 brand_id 不符：%r vs %r" % (rec.get("brand_id"), ref["brand_id"]))
            if rec.get("status") != "ACTIVE":
                raise FactResolutionError(
                    "active_rule_refs 引用了非 ACTIVE 规则：%s status=%r（A.4.3 active 语义）"
                    % (ref["object_id"], rec.get("status")))
            return rec
        if otype == "BrandMemory":
            raise FactResolutionError(
                "BrandMemory 引用无法解析：B.1.4 首轮关闭、无已批准记忆存储（approved_brand_memory_refs 必须为空）")
        if otype not in OBJECT_TYPE_DIRS:
            raise FactResolutionError("未知 object_type：%r" % otype)
        hit = self.index().get((otype, ref["object_id"], ref["version"]))
        if hit is None:
            raise FactResolutionError("悬空引用：%r（facts 池无此对象）" % (ref,))
        path, obj = hit
        if obj.get("brand_id") != ref["brand_id"]:
            raise FactResolutionError(
                "对象 brand_id=%r 与引用 brand_id=%r 不符（A.1.3 单品牌隔离）：%s"
                % (obj.get("brand_id"), ref["brand_id"], path))
        return obj
