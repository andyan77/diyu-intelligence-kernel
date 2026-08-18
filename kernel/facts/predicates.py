# -*- coding: utf-8 -*-
"""Facts 确定性谓词——结构层 P1-P3（自 tools/test_fact_schemas.py 抽出，测试与运行时共用同一入口，
E-08 关闭面）+ 运行时 R1-R5（块 E ③）。

约定：每个谓词返回「违规消息列表」，空列表 = 通过。全部确定性、零 LLM、零网络。
"""
import hashlib
import json
import re

from .store import FactStore, FactResolutionError

# ============================== 结构层 P1-P3 ==============================


def iter_fact_values(node, path="$"):
    """遍历实例中所有形如 FactValue 的节点（带 status 键的 dict）。`_` 前缀键跳过。"""
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
    """P2：顶层 brand_id 与全部嵌套 brand_id 全等（A.1.3 单品牌隔离，不一致必须阻断）。"""
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
    """P3：ContextSnapshot 各引用字段的 object_type 必须与字段语义族对应（A.4.3）。"""
    out = []
    for field, want in SNAPSHOT_REF_TYPES.items():
        node = inst.get(field)
        refs = node if isinstance(node, list) else ([node] if isinstance(node, dict) else [])
        for i, r in enumerate(refs):
            got = r.get("object_type") if isinstance(r, dict) else None
            if got != want:
                out.append("P3 $.%s[%d].object_type=%r ≠ %r（引用族错位）" % (field, i, got, want))
    return out


# ============================== 运行时 R1-R5（块 E ③） ==============================


def _canonical_obj_hash(obj):
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def runtime_snapshot_hash(snapshot):
    """R1：快照内 snapshot_hash 实算核验（口径=剔除 snapshot_hash 自身与全部 `_` 前缀键后
    canonical sha256，块 B 定、与 examples/context_snapshot.ok1 一致）。声明与实算不符即红。"""
    declared = snapshot.get("snapshot_hash")
    core = {k: v for k, v in snapshot.items() if k != "snapshot_hash" and not k.startswith("_")}
    actual = _canonical_obj_hash(core)
    if declared != actual:
        return ["R1 snapshot_hash 声明 %r ≠ 实算 %s（快照内容与指纹脱钩）" % (declared, actual)]
    return []


def runtime_refs_resolve(snapshot, store=None):
    """R2：全部引用可解析且状态合法——悬空引用 / 身份不符 / 引用非 ACTIVE 规则，逐条列出。"""
    store = store or FactStore()
    out = []
    for field in ("brand_facts_ref", "video_account_facts_ref"):
        ref = snapshot.get(field)
        if isinstance(ref, dict):
            try:
                store.load(ref)
            except FactResolutionError as e:
                out.append("R2 $.%s: %s" % (field, e))
    for field in ("product_facts_refs", "audience_facts_refs", "persona_facts_refs", "active_rule_refs"):
        for i, ref in enumerate(snapshot.get(field) or []):
            try:
                store.load(ref)
            except FactResolutionError as e:
                out.append("R2 $.%s[%d]: %s" % (field, i, e))
    return out


def runtime_brand_memory_first_round(snapshot):
    """R3：B.1.4 首轮关闭——approved_brand_memory_refs 必须为空数组；非空即红（未批准记忆禁入）。"""
    refs = snapshot.get("approved_brand_memory_refs")
    if refs != []:
        return ["R3 approved_brand_memory_refs=%r：B.1.4 首轮必须为空数组" % (refs,)]
    return []


# 明文凭证特征（fail-closed 词表：命中即红，宁误伤不漏放；locator 只该是文档/截图/表行定位符）
_CREDENTIAL_PATTERNS = [
    re.compile(p, re.I) for p in (
        r"password\s*[=:]", r"passwd\s*[=:]", r"secret\s*[=:]", r"token\s*[=:]",
        r"api[_-]?key\s*[=:]", r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"Bearer\s+[A-Za-z0-9\-_\.=]{16,}", r"ssh-rsa\s+AAAA", r"://[^/\s:@]+:[^/\s:@]+@",
    )
]


def runtime_locator_credentials(node, path="$"):
    """R4：任何 SourceRef.locator / 任意字符串字段不得含明文凭证特征（A.2.3 locator 是定位符不是载体）。"""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            out += runtime_locator_credentials(v, "%s.%s" % (path, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += runtime_locator_credentials(v, "%s[%d]" % (path, i))
    elif isinstance(node, str):
        for pat in _CREDENTIAL_PATTERNS:
            if pat.search(node):
                out.append("R4 %s: 字符串命中明文凭证特征 %r" % (path, pat.pattern))
                break
    return out


def runtime_no_duplicate_identity(store=None):
    """R5：同 (object_type, object_id, version) 禁重复定义——store 索引构建即查，本谓词把
    FactResolutionError 转为消息列表供统一报表。"""
    try:
        (store or FactStore()).index()
        (store or FactStore()).rules()
    except FactResolutionError as e:
        return ["R5 %s" % e]
    return []


def run_all_runtime(snapshot, store=None):
    """R1-R5 一次跑齐，返回违规消息列表（空=绿）。"""
    store = store or FactStore()
    out = []
    out += runtime_snapshot_hash(snapshot)
    out += runtime_refs_resolve(snapshot, store)
    out += runtime_brand_memory_first_round(snapshot)
    out += runtime_locator_credentials(snapshot)
    out += runtime_no_duplicate_identity(store)
    out += predicate_single_brand(snapshot)
    out += predicate_ref_object_type(snapshot)
    return out
