#!/usr/bin/env python3
"""资产⑤ Trace 组装（Intent 模块）——A.1.2 四类分离 + C.3「模型只许引用预物化 ID，不许自己新建」。

本模块唯一的产物是 common.defs.json#/definitions/TraceBundle 形状的 dict（字段与顺序照抄 A.9.2）。
它是 Intent 模块里**唯一**能把「模型编出来的 ID」挡在产物之外的位置：
  FACT / RULE 条目的 statement 只能从预物化的池里查出来——池里没有的 ID 根本查不到文本，
  想给它造一条 trace 就只能凭空编，所以这里选择**报错**而不是编（见 TraceAssemblyError 用法）。
红线原文（C_三个核心模块工程化落地与防死循环方案.md 资产⑤ 行）：
  「FACT/RULE/ASSUMPTION/MODEL_JUDGMENT 四类分离（A.1.2）；模型只许引用预物化的 FACT/RULE ID，不许自己新建」

零 I/O、零路径依赖：本模块不读文件、不 import config，因此可以被离线单测直接调用，
也保证 replay 与 live 两种模式下组装结果完全一致（同输入同产物，见 _derive_bundle_id）。

签名（M1-EP02 接口规格钉死，位置参数一个不改）：
  build_trace_bundle(fact_pool, rule_pool, referenced_fact_ids, assumption_entries, model_judgment_entries) -> dict
  assert_ids_in_pool(ids, pool) -> list[str]
**接口扩展（必读，与规格的差异点）**：common.defs 的 TraceBundle 把 brand_id 列为 required，
而钉死的五个位置参数里没有任何一个能提供它。在组装点臆造 brand_id 会直接违反 A.1.3 单品牌隔离，
因此新增 **keyword-only** 参数 `brand_id` / `trace_bundle_id` / `target_artifact_ref`，
其中 `brand_id` **必须由调用方（runner）从 ContextSnapshot 传入，不传即抛 TraceAssemblyError**——
宁可跑不起来，也不产出一个品牌归属不明的 Trace。
注意这是**与接口规格的实质偏离，不是"兼容"**：规格钉死的五位置参数调用
`build_trace_bundle(fp, rp, ids, asm, mj)` 在本实现下**必然抛错**（实测），
只有补上 `brand_id=` 才跑得通。首轮文档串写的「位置调用完全兼容规格」是错的，已删——
把一个必抛的调用形态说成"兼容"，会让按规格对接的调用方以为自己写对了。

诚实边界（本模块判不了的，绝不假装判了）：
  ① FACT 的 source_refs 是否真的指向该事实——只做「有没有」的透传，内容对不对判不了；
     池里 source_refs 为空时**不报错也不补造**（那是快照/前处理侧的事实层缺口，在这里补 = 造假来源），
     空数组会原样出现在产物里，下游肉眼与检测器都看得见。
  ② ASSUMPTION「必须指明缺失项」——只能机器判 target_paths 非空，判不了它指的是不是**那一条**缺失项。
  ③ MODEL_JUDGMENT「必须引用支撑 Trace」——只能判引用存在且在 bundle 内，判不了推理是否真的成立。
  ④ RULE「必须引用规则版本」——version 只能由 rule_pool 元素**透传**，本模块判不了这个版本号
     是不是该规则当前生效的那一版。缺口状态（2026-08-17 更新）：M1-EP02 修复批次 K1 已让
     preprocess.load_rule_pool 从 contracts/rules/*.yaml 真源透传 version / brand_id，
     故实测三条规则的 object_refs 现在都带得出 VersionedRef；真源某条缺 version 时这里仍留空数组、
     不编版本号，由 postcheck P6 判红（"引用了版本"不成立），不在本模块假装补齐。
"""

import hashlib
import json

# A.1.2 四类，顺序即 A.1.2 表格顺序；组装后的 entries 也按这个顺序分组排列（见 build_trace_bundle）
TRACE_TYPES = ("FACT", "RULE", "ASSUMPTION", "MODEL_JUDGMENT")

# TraceEntry 的键序照抄 A.9.2 的 YAML 声明顺序，所有条目统一发这一套键：
# 形状恒定才能做逐字段 diff 与稳定哈希；可选键时有时无会让两次运行的产物「看起来不一样」。
_ENTRY_KEYS = ("trace_id", "trace_type", "statement", "source_refs",
               "object_refs", "target_paths", "supporting_trace_refs", "confidence")

_CONFIDENCE_ENUM = ("HIGH", "MEDIUM", "LOW", None)   # common.defs TraceEntry.confidence 枚举，含 null


class TraceAssemblyError(ValueError):
    """组装期硬失败：引用了池外 ID、四类混写、缺 brand_id 等。

    为什么是抛异常而不是「跳过这条」：静默丢掉一条非法引用，下游看到的就是一份「干净」的 Trace——
    模型编过 ID 这件事被抹掉了，正是项目宪法里点名的假绿。调用方若要保留取证用的 plan，
    应当**先**用 assert_ids_in_pool 自查、按自己的策略处置，再调用本模块组装。
    继承 ValueError 是为了让只 except ValueError 的调用方也拦得住。
    """


# ---------------------------------------------------------------- 池索引与 ID 校验

def _pool_id(item):
    """取池元素的 ID：事实池用 fact_id，规则池用 rule_id。

    两个池共用一个取 ID 的口径，好处是调用方可以把两池直接相加传进 assert_ids_in_pool
    （`assert_ids_in_pool(refs, fact_pool + rule_pool)`），不必为「一次查两池」另开接口。
    """
    if not isinstance(item, dict):
        return None
    return item.get("fact_id") or item.get("rule_id")


def _index_pool(pool, id_key, label):
    """把池列表变成 {id: item} 索引；顺序保持池原序（dict 在 3.7+ 保序，产物顺序因此可复现）。

    重复 ID 直接报错：同一个 ID 指向两条不同事实时，「引用 X」到底指哪条无法判定——
    此时任何选择都是猜，按不猜原则交回上游修。
    """
    if pool is None:
        return {}
    if isinstance(pool, (str, bytes, dict)):
        raise TraceAssemblyError(f"{label} 必须是列表，实得 {type(pool).__name__}")
    idx = {}
    for i, item in enumerate(pool):
        if not isinstance(item, dict):
            raise TraceAssemblyError(f"{label}[{i}] 必须是 dict，实得 {type(item).__name__}")
        key = item.get(id_key)
        if not isinstance(key, str) or not key.strip():
            raise TraceAssemblyError(f"{label}[{i}] 缺少非空 {id_key}")
        if key in idx:
            raise TraceAssemblyError(f"{label} 存在重复 {id_key}={key}；引用会产生歧义，须由前处理去重")
        idx[key] = item
    return idx


def _as_id_list(ids, label):
    """把入参规整成 ID 列表，并挡住「字符串被当成可迭代」这个经典坑。

    LLM 回复里 referenced_fact_ids 偶尔会退化成单个字符串；若直接 for 循环会逐字符遍历，
    产出一堆单字符「池外 ID」——错得很难查。这里直接报错，让调用方在解析层修。
    """
    if ids is None:
        return []
    if isinstance(ids, (str, bytes)):
        raise TraceAssemblyError(f"{label} 必须是列表，实得字符串 {ids!r}（单个 ID 也要放进列表）")
    if isinstance(ids, dict):
        raise TraceAssemblyError(f"{label} 必须是列表，实得 dict")
    return list(ids)


def assert_ids_in_pool(ids, pool):
    """返回 ids 中**不在** pool 里的 ID 清单（空列表 = 全部合法）。

    规格钉死的签名。pool 可以是：事实池 / 规则池 / 两池相加的列表（按 _pool_id 逐元素取 ID），
    也可以是已经取好的 ID 字符串列表或集合（方便调用方复用同一份索引）。
    行为约定：
      - 保持首次出现顺序去重——同一个编出来的 ID 引用五次，报告里出现一次就够定位；
      - 非字符串 ID（None / 数字 / 嵌套结构）一律算池外，并以 str() 形式列出：
        它们本来就不可能命中池，静默放过等于给非法引用开口子；
      - 名字里的 assert 只表示「断言用」，本函数**不抛异常**——判定与处置分开，
        由调用方（runner / postcheck P6）决定是拦是记。
    """
    if isinstance(pool, (str, bytes, dict)):
        raise TraceAssemblyError(f"pool 必须是列表或集合，实得 {type(pool).__name__}")
    known = set()
    for item in (pool or []):
        if isinstance(item, str):
            known.add(item)
        else:
            pid = _pool_id(item)
            if isinstance(pid, str):
                known.add(pid)
    outside, seen = [], set()
    for raw in _as_id_list(ids, "ids"):
        key = raw if isinstance(raw, str) else str(raw)
        if key in known or key in seen:
            continue
        seen.add(key)
        outside.append(key)
    return outside


# ---------------------------------------------------------------- 各类条目的文本组装

def _dump(value):
    """把任意事实值序列化成可读文本：中文不转义、键排序（同值同文本，保证产物可复现）。"""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _fact_statement(item):
    """FACT 条目的 statement：照实转述快照，绝不把「没有的值」写成有值。

    为什么按 status 分岔而不是统一「字段=值」：MISSING / CONFLICTING 的事实若也写成
    「product.lining = None」，读起来与一条正常事实无异——A.2.4 约束3/4 明确要求
    缺失不得当值用、冲突不得静默择一。这里把状态写进句子，是让下游（含人）一眼看出它不是可用事实。
    """
    path = item.get("field_path") or item.get("fact_id")
    status = item.get("status")
    value = item.get("value")
    if status in ("MISSING", "NOT_APPLICABLE"):
        return f"{path}：快照标记为 {status}，无可用值"
    if status == "CONFLICTING":
        # 措辞不超陈述（M1-EP02 修复批次 K5）：首轮写「存在并列取值，未择一」，
        # 读起来像"并列的那几个取值都在这句话里、只是没挑"——事实上池的形状
        # {"fact_id","field_path","value","status","source_refs"} 只带**一个** value 字段，
        # 并列值的明细根本没被带进来。说成"未择一"等于暗示信息完整，属超陈述。
        return (f"{path}：快照标记为 CONFLICTING（存在并列取值；池形状未携带并列值明细）"
                f"｜池内取值={_dump(value)}（不代表这是全部并列值，也不得当作已择一的结果使用）")
    suffix = f"（status={status}）" if status else ""
    return f"{path} = {_dump(value)}{suffix}"


def _as_list(value):
    """把「标量或列表」统一成列表：None → []，标量 → [标量]，列表/元组 → list。

    前处理从 M0 扁平夹具带出的 source 可能是单个字符串（夹具里就是 "截图 IMG_0684" 这种），
    而 A.9.2 的 source_refs 是数组；这里只做形状适配，**不改内容**——原文什么样带出去什么样。
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _entry(trace_id, trace_type, statement, source_refs=None, object_refs=None,
           target_paths=None, supporting_trace_refs=None, confidence=None):
    """按 A.9.2 键序造一条 TraceEntry；八个键恒定发全，不做可选省略（见 _ENTRY_KEYS 注释）。"""
    if confidence not in _CONFIDENCE_ENUM:
        raise TraceAssemblyError(
            f"trace {trace_id} 的 confidence={confidence!r} 不在 common.defs 枚举 HIGH/MEDIUM/LOW/null 内")
    return {
        "trace_id": trace_id,
        "trace_type": trace_type,
        "statement": statement,
        "source_refs": _as_list(source_refs),
        "object_refs": _as_list(object_refs),
        "target_paths": [str(p) for p in _as_list(target_paths)],
        "supporting_trace_refs": [str(r) for r in _as_list(supporting_trace_refs)],
        "confidence": confidence,
    }


def _rule_object_refs(item, brand_id):
    """RULE 条目的 object_refs：只有 rule_pool 真给了 version 才拼 VersionedRef。

    A.1.2（A:68）要求 RULE「必须引用规则版本」。M1-EP02 修复批次 K1 之后，rule_pool 元素已从
    contracts/rules/*.yaml 真源透传 version / brand_id，正常情况下这里能拼出 VersionedRef。
    真源某条**确实没写** version 时这里仍留空数组：编一个 version=1 会让「引用了规则版本」
    这件事变成假的——宁可缺口可见（由 postcheck P6 判红），不可缺口被填平。
    brand_id 缺失时取 bundle 的 brand_id：A.1.3 要求同一次运行里所有对象同品牌，
    规则池本就是按本品牌加载的；但若规则**自带**了不同的 brand_id，说明跨品牌污染，直接报错。
    """
    version = item.get("version")
    if version is None:
        return []
    rule_brand = item.get("brand_id")
    if rule_brand is not None and rule_brand != brand_id:
        raise TraceAssemblyError(
            f"A.1.3 单品牌隔离：规则 {item.get('rule_id')} 的 brand_id={rule_brand!r} "
            f"与本次 TraceBundle 的 brand_id={brand_id!r} 不一致")
    return [{
        "object_type": "RuleRecord",
        "object_id": item["rule_id"],
        "version": version,
        "brand_id": brand_id,
    }]


def _normalize_authored(raw, trace_type, index, label):
    """把 runner / LLM 给的松散条目规整成 TraceEntry（ASSUMPTION 与 MODEL_JUDGMENT 共用）。

    容错读取的键（只做同义映射，不改语义）：
      statement ← statement | text          （LLM 输出契约里 model_judgments 用的是 text）
      supporting_trace_refs ← supporting_trace_refs | referenced_fact_ids
      target_paths ← target_paths | target_path | field_path
    若调用方自带 trace_type 且与本列表不符 → 报错：把一条 FACT 塞进 assumption_entries
    就是 A.1.2 点名的「ASSUMPTION 和 MODEL_JUDGMENT 不得伪装为 FACT」的镜像错误，必须当场拦。
    """
    if not isinstance(raw, dict):
        raise TraceAssemblyError(f"{label}[{index}] 必须是 dict，实得 {type(raw).__name__}")
    declared = raw.get("trace_type")
    if declared is not None and declared != trace_type:
        raise TraceAssemblyError(
            f"{label}[{index}] 声明 trace_type={declared!r}，但它出现在 {trace_type} 列表里（四类混写）")
    statement = raw.get("statement") or raw.get("text")
    if not isinstance(statement, str) or not statement.strip():
        raise TraceAssemblyError(f"{label}[{index}] 缺少非空 statement（或 text）")
    refs = raw.get("supporting_trace_refs")
    if refs is None:
        refs = raw.get("referenced_fact_ids")
    targets = raw.get("target_paths")
    if targets is None:
        targets = raw.get("target_path") if raw.get("target_path") is not None else raw.get("field_path")
    return {
        "trace_id": raw.get("trace_id"),
        "statement": statement.strip(),
        "source_refs": _as_list(raw.get("source_refs")),
        "object_refs": _as_list(raw.get("object_refs")),
        "target_paths": [str(p) for p in _as_list(targets)],
        "supporting_trace_refs": [str(r) for r in _as_list(_as_id_list(refs, f"{label}[{index}].supporting_trace_refs"))],
        "confidence": raw.get("confidence"),
    }


def _alloc_trace_id(preferred, fallback, used, label, index):
    """分配不冲突的 trace_id：优先用调用方给的；没给就用 fallback；已占用则追加 #2、#3…

    为什么不直接报错：一条缺失项理论上可能派生出多条假设，编号后缀比让整次运行挂掉更实用；
    但**调用方显式给的 ID 撞车必须报错**——那说明两条不同的 trace 会被同一个引用指到，属歧义。
    """
    if preferred is not None:
        if not isinstance(preferred, str) or not preferred.strip():
            raise TraceAssemblyError(f"{label}[{index}] 的 trace_id 必须是非空字符串")
        if preferred in used:
            raise TraceAssemblyError(f"{label}[{index}] 的 trace_id={preferred} 与已有条目重复（引用会产生歧义）")
        return preferred
    candidate, n = fallback, 1
    while candidate in used:
        n += 1
        candidate = f"{fallback}#{n}"
    return candidate


def _derive_bundle_id(brand_id, entries):
    """缺省 trace_bundle_id：对 brand_id + entries 做 sha256 取前 12 位，形如 TB-1a2b3c4d5e6f。

    不用 uuid4 / 时间戳的原因：Intent 模块要能 replay——同一份快照 + 同一份模型回复必须组装出
    逐字节相同的产物，才能做冻结比对与「改 prompt 前后 diff」。带随机数的 ID 会让每次运行都不同，
    比对全是噪音。含 brand_id 是为了让不同品牌的同形 Trace 不撞 ID。
    """
    payload = json.dumps({"brand_id": brand_id, "entries": entries},
                         ensure_ascii=False, sort_keys=True).encode("utf-8")
    return "TB-" + hashlib.sha256(payload).hexdigest()[:12]


# ---------------------------------------------------------------- 主入口

def build_trace_bundle(fact_pool, rule_pool, referenced_fact_ids,
                       assumption_entries, model_judgment_entries,
                       *, brand_id=None, trace_bundle_id=None, target_artifact_ref=None):
    """组装 TraceBundle（common.defs.json#/definitions/TraceBundle 形状）。

    参数：
      fact_pool              前处理物化的事实池，元素 {"fact_id","field_path","value","status","source_refs"}
      rule_pool              规则池，元素 {"rule_id","statement","scope","effect","target_path","version","brand_id"}
                             （后两键由 preprocess 从真源透传；真源没写就整个键不发，见 _rule_object_refs）
      referenced_fact_ids    模型声称引用的 FACT ID（`FACT:<field_path>`）；**池外一律报错，不代为新建**
      assumption_entries     runner 为每条被 QUICK 跨过的 missing 项生成的假设（松散 dict 即可，见 _normalize_authored）
      model_judgment_entries LLM 的 model_judgments（{"text","referenced_fact_ids"} 亦可）
      brand_id (kw, 必给)     本次运行的品牌，取自 ContextSnapshot；不给报错，绝不臆造（A.1.3）
      trace_bundle_id (kw)   不给则按内容确定性派生（见 _derive_bundle_id）
      target_artifact_ref(kw) VersionedRef；不给则**不发这个键**（A.9.2 里它非必填，发空壳等于编引用）

    entries 排序：FACT（按事实池原序）→ RULE（按规则池原序）→ ASSUMPTION → MODEL_JUDGMENT（均按入参原序）。
    按池序而不是按模型给出的顺序，是为了让「模型把引用顺序换一换」不产生 diff；分组排列则让四类分离肉眼可见。

    RULE 条目为什么是「整池物化」而不是按引用挑：签名里根本没有 referenced_rule_ids——
    A.1.2 对 RULE 的定义是「当前任务适用的已启用硬规则」，适用与否由前处理（规则加载）决定，
    不由模型挑选；模型漏引用一条硬规则不该让这条规则从 Trace 里消失。
    """
    if not isinstance(brand_id, str) or not brand_id.strip():
        raise TraceAssemblyError(
            "A.1.3 单品牌隔离：brand_id 必须由调用方从 ContextSnapshot 传入（build_trace_bundle(..., brand_id=...)），"
            "组装点不得臆造品牌归属")

    fact_idx = _index_pool(fact_pool, "fact_id", "fact_pool")
    rule_idx = _index_pool(rule_pool, "rule_id", "rule_pool")

    # ① 先规整作者型条目（假设 / 模型判断），因为它们的 supporting_trace_refs 会决定还要物化哪些 FACT
    assumptions = [_normalize_authored(r, "ASSUMPTION", i, "assumption_entries")
                   for i, r in enumerate(_as_id_list(assumption_entries, "assumption_entries"))]
    judgments = [_normalize_authored(r, "MODEL_JUDGMENT", i, "model_judgment_entries")
                 for i, r in enumerate(_as_id_list(model_judgment_entries, "model_judgment_entries"))]

    # ② 池外 FACT ID 一次报清（不是撞见一个就退出——让调用方一轮看到模型编了哪些 ID）
    wanted = _as_id_list(referenced_fact_ids, "referenced_fact_ids")
    outside = assert_ids_in_pool(wanted, fact_pool or [])
    if outside:
        raise TraceAssemblyError(
            "C.3 资产⑤红线：模型只许引用预物化的 FACT/RULE ID。以下 ID 不在事实池内，"
            f"无法在不编造的前提下生成 FACT 条目：{outside}")

    # ③ 需要物化的 FACT = 模型显式引用的 ∪ 被假设/判断当作支撑引用到的（后者若指向池内事实却没物化，
    #    产物里就会出现一条指向空气的 supporting_trace_ref——这里顺手补齐，补的仍然全部来自池，不是新建）
    needed = {i if isinstance(i, str) else str(i) for i in wanted}
    for e in assumptions + judgments:
        for ref in e["supporting_trace_refs"]:
            if ref in fact_idx:
                needed.add(ref)

    entries, used_ids = [], set()

    # FACT：按事实池原序物化。statement 由 _fact_statement 照实转述，source_refs 原样透传（空就是空）
    for fid, item in fact_idx.items():
        if fid not in needed:
            continue
        entries.append(_entry(
            trace_id=fid, trace_type="FACT", statement=_fact_statement(item),
            source_refs=item.get("source_refs"),
            target_paths=[item.get("field_path")] if item.get("field_path") else [],
            confidence=None,   # 事实不带模型置信度；快照自身的 FactValue.confidence 不在本池形状内
        ))
        used_ids.add(fid)

    # RULE：整池物化。statement 缺失即报错——一条没有文本的规则进了 Trace，读者无从判断它约束了什么
    for rid, item in rule_idx.items():
        statement = item.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            raise TraceAssemblyError(f"规则 {rid} 缺少非空 statement，无法生成 RULE 条目（不得以 rule_id 代替规则原文）")
        target_path = item.get("target_path")
        entries.append(_entry(
            trace_id=rid, trace_type="RULE", statement=statement.strip(),
            object_refs=_rule_object_refs(item, brand_id),
            target_paths=[target_path] if target_path else [],
            confidence=None,   # 硬规则是确定性的，标置信度反而误导
        ))
        used_ids.add(rid)

    # ASSUMPTION：A.1.2 要求「必须说明替代的缺失项和影响」——机器可判的部分只有 target_paths 非空
    for i, e in enumerate(assumptions):
        if not e["target_paths"]:
            raise TraceAssemblyError(
                f"assumption_entries[{i}] 没有 target_paths：A.1.2 要求假设必须指明它替代的缺失项"
                "（runner 应把该 missing 项的 field_path 带进来）")
        tid = _alloc_trace_id(e["trace_id"], f"ASSUMPTION:{e['target_paths'][0]}", used_ids, "assumption_entries", i)
        entries.append(_entry(tid, "ASSUMPTION", e["statement"], e["source_refs"], e["object_refs"],
                              e["target_paths"], e["supporting_trace_refs"], e["confidence"]))
        used_ids.add(tid)

    # MODEL_JUDGMENT：A.1.2 要求「必须引用支撑 Trace」——空引用直接报错，
    # 因为一条无支撑的模型判断混在 Trace 里，与有据判断长得一模一样，正是四类分离要防的伪装
    for i, e in enumerate(judgments):
        if not e["supporting_trace_refs"]:
            raise TraceAssemblyError(
                f"model_judgment_entries[{i}] 没有 supporting_trace_refs："
                "A.1.2 要求模型判断必须引用支撑 Trace（无支撑的判断不得进入 TraceBundle）")
        tid = _alloc_trace_id(e["trace_id"], f"MODEL_JUDGMENT:{i + 1}", used_ids, "model_judgment_entries", i)
        entries.append(_entry(tid, "MODEL_JUDGMENT", e["statement"], e["source_refs"], e["object_refs"],
                              e["target_paths"], e["supporting_trace_refs"], e["confidence"]))
        used_ids.add(tid)

    # ④ 支撑引用最终校验：必须指向本 bundle 内真实存在的条目。
    #    ③ 已把池内事实补齐，所以此刻还悬空的，只可能是模型/调用方编出来的 ID 或指向未加载的规则。
    dangling = {}
    for e in entries:
        if e["trace_type"] not in ("ASSUMPTION", "MODEL_JUDGMENT"):
            continue
        bad = [r for r in e["supporting_trace_refs"] if r not in used_ids]
        if bad:
            dangling[e["trace_id"]] = bad
    if dangling:
        raise TraceAssemblyError(
            "C.3 资产⑤红线：supporting_trace_refs 只能指向已物化的 FACT/RULE/ASSUMPTION/MODEL_JUDGMENT，"
            f"以下引用在本 bundle 内不存在：{dangling}")

    bundle = {
        "trace_bundle_id": trace_bundle_id or _derive_bundle_id(brand_id, entries),
        "brand_id": brand_id,
        "entries": entries,
    }
    if target_artifact_ref is not None:
        # 只有调用方真给了才发这个键：A.9.2 里它非必填，发一个空壳 VersionedRef = 编造引用
        if not isinstance(target_artifact_ref, dict):
            raise TraceAssemblyError("target_artifact_ref 必须是 VersionedRef 形状的 dict")
        bundle["target_artifact_ref"] = target_artifact_ref
    return bundle
