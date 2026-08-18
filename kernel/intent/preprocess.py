#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""资产③ Intent 确定性前处理：事实物化 / 规则池装载 / 上下文需求解析。

形态裁决（C.3 冻结，接口规格「形态裁决」段）：Intent = 1 步 LLM + 确定性前后处理。
**required_context / missing_context 由本文件按 OD-03 算出，绝不交给 LLM。**
红线测试：删掉本文件只留 prompt，行为基本不变 = 违规套壳。所以这里的每一条判定都必须是
"同一份输入必得同一份输出"的纯函数——不读时钟、不读随机、不读网络、不看模型说了什么。

真源（按小节名 + 行号双写；行号锚定 contracts/OD-03_阻断性最小上下文字段清单.md 当前 **37 行**版本，
该文件改版须同步本文件行号注释——仓库通例是只写小节名，这里额外写行号是本任务的明确要求）：
  · contracts/OD-03_阻断性最小上下文字段清单.md   全文 37 行（`wc -l` 实测 2026-08-17，runtime_verified；
    首轮写的「38 行」是错值，已更正），逐行对映见下方 _UNIVERSAL / _GOAL_* / _QR_* 三张表
  · A_模块接口与核心数据字典.md「## A.4.2 ContextRequirement」  六字段结构与两条 QUICK 规则
  · A_模块接口与核心数据字典.md「## A.2.6 核心枚举」            六目标 / 平台 / 可用性 / 影响度枚举
  · M1-EP02 kernel/intent 接口规格「各文件公共函数签名」「快照事实→OD-03 字段映射」

OD-03 L8 语义行「本清单不新增 A 之外的字段与状态」——因此本文件产出的 ContextRequirement
严格只有 A.4.2 的六个键，一个不多；availability / impact 只取 A.4.2 的三值 / 两值。

诚实边界（写在最前面，免得被当成"已覆盖"）：
  ① 快照形状：M0 的 12 份案例夹具是"扁平事实内联"形状（顶层 snapshot_id / brand_id / facts / hard_rules），
     与 contracts/schemas/context_snapshot.schema.json（照抄 A.4.3 的十四字段引用式结构）不是同一形状。
     本文件按夹具实际形状容错读取，**不在此做 Schema 校验**（理由见 load_snapshot 文档串）。
  ② 材质证明的"涉功效声明升阻断"条款（OD-03 L32 括号）：v1 只落谓词桩，未实现判据，
     缺口如实登记在 _material_proof_impact() 里，不假装覆盖。
  ③ 本文件不做品牌隔离过滤（SYS-08）：load_rule_pool 的签名（接口规格钉死）不带 brand 参数，
     **过滤职责在 runner**（M1-EP02 修复批次 K2 已落地 runner.filter_rule_pool_by_brand），
     本函数只负责把真源里的 brand_id / version 如实透传出去，让 runner 有得可判。
"""

import glob
import json
import os
import re
import sys

import yaml

from kernel.intent.config import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_CONFLICTING,
    AVAILABILITY_MISSING,
    BUSINESS_GOAL_FIELD_PATH,
    BUSINESS_GOALS,
    FACT_ID_PREFIX,
    FACT_STATUS_VALUES,
    IMPACT_BLOCKING,
    IMPACT_QUALITY_REDUCING,
    RULES_DIR,
)

# ======================================================================================
# 一、快照装载
# ======================================================================================


def load_snapshot(path):
    """读一份 Context Snapshot JSON → R1-R5 运行时谓词 → 解引用，返回内联兼容视图 dict。

    历史注（原「诚实边界」已随块 E ① 关闭）：M0 冻结夹具曾是"事实内联"扁平形状，与
    contracts/schemas/context_snapshot.schema.json（A.4.3 引用式）存在形状差，本函数当时
    只做最小结构断言、不卡 Schema。该形状差经 Founder 2026-08-18 批准迁移方案后已消除——
    15 份正式快照全部迁为 A.4.3 十四字段引用式（tools/migrate_snapshots.py，值级对账
    acceptance/runs/migration_reconciliation.md）。据此本函数改为（块 E ②，删旧容错）：
      1. kernel/facts.predicates.run_all_runtime：snapshot_hash 实算 / 引用可解析且 ACTIVE /
         BrandMemory 首轮必空 / locator 无明文凭证 / 同 ID 同版本禁覆盖 / P2 / P3，任何红即抛错；
      2. kernel/facts.resolve.materialize_legacy_view：解引用产出与旧内联同构的视图，
         下游 materialize_fact_pool / resolve_requirements 的消费面不变；
      3. 旧内联形状**直接拒绝**（fail-closed）——两套形状并行 = E-05 假闭环温床。

    `_fixture_note` 泄题纪律不变：视图不含任何 `_` 前缀键（解引用层已剔除，含迁移注解），
    runner 侧仍只许注入 fact 池行，不得注入原始快照全文。
    """
    with open(path, "r", encoding="utf-8") as fh:
        snapshot = json.load(fh)
    if not isinstance(snapshot, dict):
        raise ValueError("快照根节点必须是 JSON 对象，实际是 %s：%s" % (type(snapshot).__name__, path))
    from kernel.facts import FactStore, materialize_legacy_view, predicates as _fact_predicates
    store = FactStore()
    red = _fact_predicates.run_all_runtime(snapshot, store)
    if red:
        raise ValueError("快照未过 kernel/facts 运行时谓词（R1-R5/P2/P3），拒绝装载：\n  " + "\n  ".join(red))
    return materialize_legacy_view(snapshot, store)


# ======================================================================================
# 二、事实物化（FACT 池）
# ======================================================================================

# 池内 status 的取值域说明（重要，别当成笔误）：
# 接口规格「materialize_fact_pool」行钉定的口径是「有 status 用之，无 status 视为 AVAILABLE，
# 值为 null/"MISSING" 视为 MISSING」。于是池里会同时出现两套词汇：
#   · 夹具**显式写出**的 A.2.4 FactValue.status（CONFIRMED / PROVISIONAL / MISSING / CONFLICTING /
#     NOT_APPLICABLE）——原样透传，不翻译；
#   · 夹具**没写** status 时派生的 AVAILABLE——这是 A.4.2 availability 的词汇。
# 为什么不统一：两边各自是各自真源的原话，谁翻译谁就得替真源做映射决定（比如 PROVISIONAL 到底算
# 在场还是不在场），那属于合同解释，不是前处理该干的事。需要"在不在场"这一层判断的只有
# resolve_requirements，它用 _availability_from_status() 显式做一次映射，映射规则写在那里、只写一处。
_STATUS_AVAILABLE = AVAILABILITY_AVAILABLE
_STATUS_MISSING = AVAILABILITY_MISSING


def _is_fact_leaf(node):
    """判断一个节点是不是 FactValue 叶子。

    判据只有一条：dict 且含 "value" 键。理由是 M0 夹具的书写惯例——
    事实值一律写成 {"value": …, "source": …[, "status": …]}，而 product / brand 这种分组节点
    只有子键、没有 value。用"有没有 value 键"做判据是可机器判定的，不靠字段名猜层级。
    """
    return isinstance(node, dict) and "value" in node


def _fact_status(node):
    """按接口规格口径推 status。

    优先级：夹具显式 status > 值为空派生 MISSING > 其余 AVAILABLE。
    显式 status 优先是关键——夹具写 {"value": null, "status": "MISSING"} 与写 {"value": null} 语义相同，
    但夹具若写了不认识的状态字符串，这里 fail-closed 判 MISSING：把没见过的状态当"在场"是编造事实的第一步。

    **认不出来的 status 会往 stderr 打一行告警**（M1-EP02 修复批次 K1）：
    只降级不出声，等于把「快照写了个 A.2.4 五枚举之外的状态」这件事悄悄吞掉——
    降级后的行为（判缺失）与「这个字段本来就没有」长得一模一样，排查时无从区分是夹具写错了状态词
    还是真的缺值。告警只写到 stderr、不改变返回值，既不影响确定性（同输入同输出），也不静默。
    """
    declared = node.get("status")
    if declared is not None:
        if declared in FACT_STATUS_VALUES:
            return declared
        # 认不出来的状态：如实降级为缺失，并把原文塞进 status 供人工排查会丢失信息，
        # 故这里只降级、原文保留在 value 侧，由上层打印时自行呈现。
        sys.stderr.write(
            "[intent.preprocess] 告警：快照事实的 status=%r 不在 A.2.4 五枚举 %s 内，"
            "已 fail-closed 降级为 MISSING（不是「这个字段没有」，是「状态词认不出来」）\n"
            % (declared, list(FACT_STATUS_VALUES))
        )
        return _STATUS_MISSING
    value = node.get("value")
    # 值为 null 或字面 "MISSING"（夹具里出现过的两种"没有"写法）→ 缺失
    if value is None or value == "MISSING":
        return _STATUS_MISSING
    return _STATUS_AVAILABLE


def _source_refs_of(node):
    """取一条事实的来源引用列表。

    M0 夹具的来源是**自由文本**（如 "截图 IMG_0684"、"故意缺失（夹具设计）"），不是 A.2.3 SourceRef 对象。
    这里原样透传成单元素列表，**绝不**补造 source_id / brand_id / captured_at / checksum 把它包装成
    "看起来合规"的 SourceRef——那是伪造溯源，比没有溯源更危险（下游会以为它可核验）。
    夹具将来若改成真 SourceRef 对象（写在 source_refs 数组里），本函数直接透传该数组。
    """
    refs = node.get("source_refs")
    if isinstance(refs, list):
        return list(refs)
    source = node.get("source")
    if source is not None:
        return [source]
    return []


def _walk_facts(node, prefix, out):
    """深度优先遍历 facts 子树，把叶子铺平成 FACT 条目。"""
    if _is_fact_leaf(node):
        out.append(
            {
                "fact_id": FACT_ID_PREFIX + prefix,
                "field_path": prefix,
                "value": node.get("value"),
                "status": _fact_status(node),
                "source_refs": _source_refs_of(node),
            }
        )
        return
    if isinstance(node, dict):
        # 不排序：按夹具书写顺序输出。为什么——池的顺序会决定 prompt 里事实行的顺序，
        # 排序规则一变，同一份快照两次运行的 prompt 就不再逐字节相同，B.2.2「同条件」被悄悄破坏。
        # Python 3.7+ dict 保序，json.load 也保序，所以"照原样"本身就是确定性的。
        for key, child in node.items():
            if key.startswith("_"):
                # 下划线开头 = 夹具元数据（_fixture_note / _context_snapshot_ref_note 等），
                # 里面写着案例编号与考点，不是事实，进池即泄题。
                continue
            _walk_facts(child, "%s.%s" % (prefix, key) if prefix else key, out)
        return
    # 标量 / 数组叶子：夹具里直接写裸值的字段（如 product.product_id = "P13"、brand.brand_id）。
    # 没有 status 包装，按口径视为 AVAILABLE（值为 null 时由 _fact_status 判 MISSING）。
    out.append(
        {
            "fact_id": FACT_ID_PREFIX + prefix,
            "field_path": prefix,
            "value": node,
            "status": _fact_status({"value": node}),
            "source_refs": [],
        }
    )


def materialize_fact_pool(snapshot):
    """把快照 facts 子树物化成 FACT 池：[{fact_id, field_path, value, status, source_refs}]。

    池 = 模型**唯一**被允许引用的事实集合（接口规格「FACT ID 约定」：池外 ID 一律 postcheck FAIL）。
    因此缺失事实也必须进池并带 status=MISSING——把缺失项从池里删掉，模型引用不到它，
    postcheck 也就无从判断"模型是不是把缺失当成了事实"，反而少了一道拦截。
    """
    facts = snapshot.get("facts")
    if facts is None:
        return []
    if not isinstance(facts, dict):
        raise ValueError("快照 facts 必须是 JSON 对象，实际是 %s" % type(facts).__name__)
    pool = []
    _walk_facts(facts, "", pool)
    return pool


# ======================================================================================
# 三、规则池装载（RULE 池）
# ======================================================================================

# A.9.1 RuleRecord 的 status 语义：只有 ACTIVE 的规则参与运行。
_RULE_STATUS_ACTIVE = "ACTIVE"


# 规则池条目的键集（M1-EP02 修复批次 K1：五键 → 七键）。
# 前五个是接口规格钉死的必给键（缺一即 fail-loud）；后两个是**真源里有就透传、没有就如实缺键**的键。
_RULE_REQUIRED_KEYS = ("rule_id", "statement", "scope", "effect", "target_path")
_RULE_PASSTHROUGH_KEYS = ("version", "brand_id")


def load_rule_pool():
    """装载 contracts/rules/*.yaml 里的 RuleRecord，返回
    [{rule_id, statement, scope, effect, target_path, version, brand_id}]（七键）。

    RULE ID = rule_id 原值（接口规格「FACT ID 约定」），不加前缀、不改写——它是注册表主键，
    改写等于制造第二套 ID 体系，postcheck 的池成员校验立刻失去意义。

    **为什么从五键扩到七键**（M1-EP02 修复批次 K1，堵两个下游缺口）：
      · `version`  ← A.1.2「RULE：必须引用规则版本」（A:68）。首轮池形状不带 version，
                     trace.py 只能把 RULE 条目的 object_refs 留成空数组，于是「引用了规则版本」
                     这件事在产物里根本无从核验；postcheck P6 也就判不了。真源
                     contracts/rules/*.yaml 本来就有 version 字段，是前处理没带出来。
      · `brand_id` ← A.1.3 / SYS-08 单品牌隔离。见下条。

    **透传，不编造**：这两个键只有在 YAML 真源里存在时才出现在返回的 dict 里；真源没写就
    **整个键都不发**（而不是发一个 None 或补一个默认值）。理由是下游要区分三件事——
    「这条规则声明了自己属于 X 品牌」「这条规则声明了版本 N」「这条规则什么都没声明」。
    补 None 会让第三种情形看起来像「声明了空值」，补默认值则直接是编造。
    实测（2026-08-17，runtime_verified）：contracts/rules/ 三份 RuleRecord
    （R-BDD01-001 / R-BDD01-002 / R-FB01-001）version 与 brand_id 均齐备，故当前无缺键情形。

    ⚠ 品牌隔离（SYS-08 / OD-03 §一 #3）**仍不在本函数内发生**，但职责已经明确：
    接口规格把签名钉死为无参 `load_rule_pool()`，拿不到 brand_id，本函数因此**如实透传全仓所有
    ACTIVE 规则**（可能跨品牌）；**过滤职责归 runner**——见 runner.filter_rule_pool_by_brand()，
    它按 snapshot["brand_id"] 过滤，并把没有 brand_id 键的规则 fail-closed 剔除 + stderr 告警。
    这里不"顺手"过滤，是因为过滤所需的 brand_id 根本没进签名，偷偷读全局快照来过滤会造出隐藏依赖。

    非 ACTIVE 的规则被排除，且**不静默**：跳过的条目数与 rule_id 由调用方需要时自行比对
    （目录里现有三份全部 ACTIVE，实测无跳过）。
    """
    pool = []
    # 排序：按文件名。规则池顺序会进 prompt，排序必须稳定；glob 的返回顺序依赖文件系统，不稳定。
    for path in sorted(glob.glob(os.path.join(RULES_DIR, "*.yaml"))):
        with open(path, "r", encoding="utf-8") as fh:
            record = yaml.safe_load(fh)
        if not isinstance(record, dict):
            raise ValueError("RuleRecord 必须是 YAML 映射：%s" % path)
        if record.get("status") != _RULE_STATUS_ACTIVE:
            continue
        missing_keys = [k for k in _RULE_REQUIRED_KEYS if k not in record]
        if missing_keys:
            # fail-loud：A.9.1 十字段是冻结结构，缺字段说明注册表坏了，不能当"这条规则不存在"糊过去。
            raise ValueError("RuleRecord 缺字段 %s：%s" % (missing_keys, path))
        item = {k: record[k] for k in _RULE_REQUIRED_KEYS}
        for key in _RULE_PASSTHROUGH_KEYS:
            if key in record:
                item[key] = record[key]
            else:
                # 不 raise、不补值：A.9.1 里这两个字段是必填，但「注册表某条缺了它」属数据缺陷，
                # 由下游（runner 的品牌过滤 / postcheck P6 的 version 判定）在各自射程内判红，
                # 前处理只如实反映真源现状。缺键这件事在这里出一声告警，免得只在下游看到后果。
                sys.stderr.write(
                    "[intent.preprocess] 告警：RuleRecord %s 缺 %s 字段（A.9.1 必填），"
                    "池条目按真源如实缺键，不补默认值；下游按 fail-closed 处理\n"
                    % (os.path.basename(path), key)
                )
        pool.append(item)
    return pool


# ======================================================================================
# 四、快照探针：把 OD-03 的一行字段，落到快照里的具体键
# ======================================================================================


def _get_by_path(snapshot, dotted):
    """按点号路径取快照节点；取不到返回哨兵 _ABSENT。

    路径写法统一以 "facts." 开头（如 "facts.product.inventory"），与 FACT 池的 field_path
    差一个前缀——池的 field_path 是 facts 内部相对路径，这里的候选路径是从快照根算起，
    两者刻意不混用，避免"到底带不带 facts."的口径分裂。
    """
    node = snapshot
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return _ABSENT
        node = node[part]
    return node


class _Absent(object):
    """'键根本不存在' 的哨兵。用哨兵而不是 None，因为 None 在夹具里是合法的'值为空'。"""

    def __repr__(self):
        return "<ABSENT>"


_ABSENT = _Absent()


def _availability_from_status(status):
    """FACT 池 status → A.4.2 availability 三枚举。整份模块只有这一处做这个映射。

    · AVAILABLE / CONFIRMED / PROVISIONAL → AVAILABLE
      PROVISIONAL 也算在场：A.2.4 允许它带 confidence 使用，只是"不得被描述为确定事实"——
      那是表述层约束（Creative/postcheck 管），不是"这个字段没有"。在这里把它判缺失会让系统
      对着一个明明有值的字段反复追问 Founder，直接违反北极星②降低认知负担。
    · MISSING / NOT_APPLICABLE → MISSING
      NOT_APPLICABLE 归入缺失是 fail-closed 的口径选择，如实登记：A.4.2 的 availability 三枚举里
      没有"不适用"这一格，OD-03 也未规定；M0 全部 12 份快照夹具实测零处使用 NOT_APPLICABLE
      （grep 实证），所以这个选择当前不影响任何案例判定。若将来真出现，需回 OD-03 定口径。
    · CONFLICTING → CONFLICTING
      OD-03 L37「字段 availability=CONFLICTING（如双价）视同缺失处理，且内容不得使用该字段值」——
      "视同缺失"落在 missing_context 的**成员判定**上（见 resolve_requirements），
      availability 字段本身按 L37 原文保留 CONFLICTING，不改写成 MISSING：改写会抹掉
      "这里有冲突要人工裁决"和"这里啥都没有"的区别，而这两者的处理动作完全不同。
    """
    if status == AVAILABILITY_CONFLICTING:
        return AVAILABILITY_CONFLICTING
    if status in (AVAILABILITY_AVAILABLE, "CONFIRMED", "PROVISIONAL"):
        return AVAILABILITY_AVAILABLE
    return AVAILABILITY_MISSING


def _availability_of_node(node):
    """一个快照节点的可用性。"""
    if node is _ABSENT:
        return AVAILABILITY_MISSING
    if _is_fact_leaf(node):
        return _availability_from_status(_fact_status(node))
    if isinstance(node, dict):
        # 分组节点（如 facts.product）：至少有一个非下划线子键才算在场。
        # 空对象 {} 视为缺失——OD-03 L14「至少选定一个」，空壳不算"选定"。
        return AVAILABILITY_AVAILABLE if any(not k.startswith("_") for k in node) else AVAILABILITY_MISSING
    if node is None:
        return AVAILABILITY_MISSING
    if isinstance(node, (list, tuple)) and len(node) == 0:
        return AVAILABILITY_MISSING
    return AVAILABILITY_AVAILABLE


def _worse(a, b):
    """两个 availability 取"更差"的一个：CONFLICTING > MISSING > AVAILABLE（越靠前越差）。

    用于 OD-03 里一行写了多个并列字段的情况（如 L23「品牌促销边界（最低折扣线 / 禁用表达）」
    = 商业硬约束 + 禁用表达清单，两者都在才算这项上下文齐备）。
    CONFLICTING 排在最差：有冲突比单纯没有更需要人介入（L37 明令"内容不得使用该字段值"）。
    """
    order = {AVAILABILITY_CONFLICTING: 2, AVAILABILITY_MISSING: 1, AVAILABILITY_AVAILABLE: 0}
    return a if order[a] >= order[b] else b


def _probe(snapshot, candidate_groups):
    """按候选路径探快照，返回 (availability, related_source_refs)。

    candidate_groups 是"组"的元组，组与组之间是**且**（全部齐备才 AVAILABLE）。
    组内的多个候选路径**不是"哪个可用就用哪个"的或**，而是「**第一个存在的键定音**」：
    按候选表顺序找到第一个在快照里**存在**（不是 _ABSENT）的键，就用它的可用性作为本组结论，
    **后面的候选一概不再看**——哪怕它存在且可用。举例：候选表 ("facts.brand.x", "facts.brand_facts.x")，
    若快照里 facts.brand.x 写着 {"value": null, "status": "MISSING"}、facts.brand_facts.x 有值，
    本组结论是 MISSING（前者存在，定音），不是 AVAILABLE。
    这是有意的 fail-closed 口径：候选表按可信度排序（先案例专用键、后同义键），
    "换个键名再试一次"等于允许系统在第一处明说缺失之后去别处找一个能用的值顶上，
    那正是编造上下文的入口。首轮文档串把它写成"命中第一个存在的就算数"，字面容易被读成
    "哪个可用取哪个"，与实现不符，已按实现更正（M1-EP02 修复批次 K1）。
    为什么需要多候选：同一语义的字段在不同案例夹具里键名不同——实测 INT 家族写 facts.persona /
    facts.brand，E2E-01 与 SYS-D01 家族写 facts.persona_facts / facts.brand_facts，
    库存则一份写 facts.product.inventory、一份写 facts.inventory（接口规格「快照事实→OD-03 字段映射」
    亦明写"facts.product.inventory 或 facts.inventory"）。候选表是**按实测夹具枚举**出来的，
    不是猜出来的；新增候选前须先在夹具里 grep 到该键确实存在。
    """
    overall = AVAILABILITY_AVAILABLE
    refs = []
    for group in candidate_groups:
        group_availability = AVAILABILITY_MISSING
        for dotted in group:
            node = _get_by_path(snapshot, dotted)
            if node is _ABSENT:
                continue
            group_availability = _availability_of_node(node)
            if _is_fact_leaf(node):
                refs.extend(_source_refs_of(node))
            # 第一个**存在的键**定音：存在但标为缺失/冲突时，**不再看后位候选**（口径理由见文档串）。
            break
        overall = _worse(overall, group_availability)
    return overall, refs


# ======================================================================================
# 五、OD-03 三张表：通用四项 / 分目标追加 / 非阻断白名单
# ======================================================================================
#
# 表结构说明（每条 = 一个 ContextRequirement 的模板）：
#   field_path            → A.4.2 field_path。用**规范名**，不用"这次匹配上的那个快照键"，
#                           否则同一语义在不同案例里 field_path 不同，跨案例比对（如 INT-D03
#                           两侧 required_context 差集）就没法做。
#   purpose               → A.4.2 purpose。照抄 OD-03 原文大白话，不改写。
#   impact                → A.4.2 impact，只有 BLOCKING | QUALITY_REDUCING（OD-03 L8：不新增状态）。
#   od03                  → 出处行号（本任务要求逐行注明；锚定 OD-03 当前 38 行版本）。
#   candidates            → 快照探针候选组（见 _probe）。
#   question              → A.4.2 resolution_question，人话中文；AVAILABLE 时置 None。

_UNIVERSAL_REQUIREMENTS = (
    {
        # OD-03 L14｜#1 做哪个商品：至少选定一个且在库（A.4.1：至少一个）
        "field_path": "selected_product_refs",
        "purpose": "做哪个商品：至少选定一个且在库",
        "impact": IMPACT_BLOCKING,
        "od03": "OD-03 §一 L14",
        # 接口规格「快照事实→OD-03 字段映射」：selected_product_refs ← facts.product 在场即 AVAILABLE。
        "candidates": (("facts.product",),),
        "question": "这条视频要做哪件商品？请至少选定一件在库商品。",
    },
    {
        # OD-03 L15｜#2 为什么做：商业目标六选一已解析；听不出来必须问，不许猜
        #           （A.5.2：goal_resolution=RESOLVED 才可继续）
        # field_path 取 config.BUSINESS_GOAL_FIELD_PATH 而不是就地写字面："business_goal" 这个字面
        # 同时是 runner G2 硬闸与 postcheck P4 的分岔判据（仲裁1），三处必须同源，见 config 里的说明。
        "field_path": BUSINESS_GOAL_FIELD_PATH,
        "purpose": "为什么做：商业目标六选一已解析；听不出来必须问，不许猜",
        "impact": IMPACT_BLOCKING,
        "od03": "OD-03 §一 L15",
        # 特判：优先看 stated_goal 入参（A.4.1 Task.stated_business_goal 承载），
        # 其次才读 facts.business_goal。逻辑在 _resolve_business_goal()，不走通用探针。
        "candidates": (("facts.business_goal",),),
        "question": "这条视频想达成什么？六选一：品牌认知 / 新品推广 / 转化 / 库存激活 / 品牌故事 / 用户教育。",
    },
    {
        # OD-03 L16｜#3 哪个品牌：品牌身份明确（防串牌）（SYS-08 单品牌隔离）
        "field_path": "brand_id",
        "purpose": "哪个品牌：品牌身份明确（防串牌）",
        "impact": IMPACT_BLOCKING,
        "od03": "OD-03 §一 L16",
        # 接口规格：brand_id ← 快照顶层 brand_id（不在 facts 里）。
        "candidates": (("brand_id",),),
        "question": "这条视频是哪个品牌的？请指明品牌，避免跨品牌串用事实。",
    },
    {
        # OD-03 L17｜#4 发到哪：本期仅视频号；其他平台不得静默适配（A.4.1 规则）
        "field_path": "platform",
        "purpose": "发到哪：本期仅视频号；其他平台不得静默适配",
        "impact": IMPACT_BLOCKING,
        "od03": "OD-03 §一 L17",
        # 接口规格：platform ← 常量 WECHAT_VIDEO（恒 AVAILABLE）。
        # 诚实说明：本项在 M0 结构上恒可用，因为 A.2.6 Platform 枚举只有 WECHAT_VIDEO 一个值。
        # OD-03 L17 真正要拦的"其他平台不得静默适配"是对**非 WECHAT_VIDEO 输入**的拒绝，
        # 落在 postcheck 的常量校验（接口规格 P5），不在这里假装判过。
        "candidates": (),
        "question": None,
    },
)

# 分目标追加阻断项（OD-03 §二 L19「在通用四件之上」，L23-L28 六行逐行对映）。
_GOAL_REQUIREMENTS = {
    "INVENTORY_ACTIVATION": (
        {
            # OD-03 L23｜库存数量与有效性
            "field_path": "product.inventory",
            "purpose": "库存数量与有效性",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L23",
            # 两种键名都实测存在：INT-D02/D03 写 facts.product.inventory，E2E-01/SYS-D01 写 facts.inventory。
            "candidates": (("facts.product.inventory", "facts.inventory"),),
            "question": "这件商品现在还有多少库存、这个数是什么时候的？",
        },
        {
            # OD-03 L23｜时间窗口（多久内消化）
            "field_path": "task.time_window",
            "purpose": "时间窗口（多久内消化）",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L23",
            # facts.time_window 是 E2E-01 / SYS-D01 夹具的实际键（Founder 2026-08-17 IA-0 裁决
            # OQ-BUILD-07 定值"六周"后回填）；INT 家族快照没有这个键，改由 task_statement 兜底，
            # 逻辑见 _time_window_in_statement()。
            "candidates": (("facts.time_window",),),
            "question": "这批货希望多久内消化完？（例如「春节前」「六周内」）",
        },
        {
            # OD-03 L23｜品牌促销边界（最低折扣线 / 禁用表达）
            "field_path": "brand.promotion_boundary",
            "purpose": "品牌促销边界（最低折扣线 / 禁用表达）",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L23",
            # 一行两件事 → 两个"且"组：商业硬约束（含最低折扣线）+ 禁用表达清单，缺一即不齐备。
            "candidates": (
                ("facts.brand.commercial_constraints", "facts.brand_facts.commercial_constraints"),
                ("facts.brand.forbidden_expressions", "facts.brand_facts.forbidden_expressions"),
            ),
            "question": "促销可以做到什么程度？最低折扣线是多少、哪些说法是禁止的？",
        },
    ),
    "PRODUCT_LAUNCH": (
        {
            # OD-03 L24｜商品已确认卖点或可验证事实（成分 / 版型）
            "field_path": "product.verified_selling_point",
            "purpose": "商品已确认卖点或可验证事实（成分 / 版型）",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L24",
            # 原文是"或"：卖点、成分、版型任一在场即可 → 单组多候选（组内或）。
            "candidates": (
                (
                    "facts.product.selling_points",
                    "facts.product.material",
                    "facts.product.style_attributes",
                ),
            ),
            "question": "这件新品最值得说的、且有据可查的点是什么？（卖点 / 成分 / 版型任一）",
        },
        {
            # OD-03 L24｜在售状态
            "field_path": "product.availability_status",
            "purpose": "在售状态",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L24",
            # 诚实登记：M0 十二份快照夹具里**没有任何"在售状态"键**（实测），故本项在 M0 恒判 MISSING。
            # 刻意**不**拿 product.lifecycle_stage（值如"库存消化期"）冒充——生命周期阶段不等于在不在售，
            # 拿它顶替就是为了让考卷变绿而做的语义拉伸，属假绿。
            "candidates": (("facts.product.availability_status", "facts.product.sales_status"),),
            "question": "这件商品现在是在售、预售还是已下架？",
        },
    ),
    "CONVERSION": (
        {
            # OD-03 L25｜价格（无价或价格冲突未解决即停）
            "field_path": "product.price",
            "purpose": "价格（无价或价格冲突未解决即停）",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L25",
            # "价格冲突未解决即停"由 CONFLICTING 传导自动实现：探针返回 CONFLICTING，
            # 而 CONFLICTING 按 L37 计入 missing_context → BLOCKING 缺失 → 停。不需要另写分支。
            "candidates": (("facts.product.price",),),
            "question": "这件商品卖多少钱？如果同款有两个价格，请指明以哪个为准。",
        },
        {
            # OD-03 L25｜在售 / 购买渠道
            "field_path": "product.purchase_channel",
            "purpose": "在售 / 购买渠道",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L25",
            # 同 PRODUCT_LAUNCH 的在售状态：M0 夹具无此键，恒 MISSING，如实标缺。
            "candidates": (
                (
                    "facts.product.purchase_channel",
                    "facts.product.availability_status",
                    "facts.product.sales_channel",
                ),
            ),
            "question": "顾客在哪里能买到？（门店 / 小程序 / 直播间…）现在是否可下单？",
        },
    ),
    "BRAND_STORY": (
        {
            # OD-03 L26｜品牌定位与价值主张
            "field_path": "brand.positioning_and_values",
            "purpose": "品牌定位与价值主张",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L26",
            # "与" → 两个且组。定位键名两族：INT-D03 写 facts.brand.positioning，
            # E2E-01/SYS-D01 写 facts.brand_facts.positioning_statement 与顶层 facts.brand_positioning。
            "candidates": (
                (
                    "facts.brand.positioning",
                    "facts.brand_facts.positioning_statement",
                    "facts.brand_positioning",
                ),
                ("facts.brand.values", "facts.brand_facts.values"),
            ),
            "question": "这个品牌是做什么的、坚持什么？（定位一句话 + 价值主张）",
        },
        {
            # OD-03 L26｜主理人人设事实（G.1 窄门：必须有品牌锚）
            "field_path": "persona",
            "purpose": "主理人人设事实（G.1 窄门：必须有品牌锚）",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L26",
            # ⚠ 与 OD-03 §三 L32「人设 / 账号事实」属 QUALITY_REDUCING 的**表面冲突**，此处按
            # "特殊优先于一般"解：L19 标题明写分目标追加项是"在通用四件之上"的追加阻断项，
            # L26 又把"主理人人设事实"单独点名并附 G.1 窄门理由（品牌故事没有品牌锚就只能编）。
            # 若反过来让 L32 覆盖 L26，那 L26 这一格就永远不生效——一条清单不会写一格死条款。
            # 因此：BRAND_STORY 下 persona 是 BLOCKING，且不再重复出现在 QUALITY_REDUCING 白名单里
            # （去重逻辑见 resolve_requirements）。
            "candidates": (("facts.persona", "facts.persona_facts"),),
            "question": "出镜/讲述的主理人是谁？有哪些可核实的真实经历可以用？（没有就不能编）",
        },
    ),
    "CUSTOMER_EDUCATION": (
        {
            # OD-03 L27｜教育点对应的可验证商品事实（如成分 / 护理）；无真源事实不得编功效
            "field_path": "product.verifiable_education_fact",
            "purpose": "教育点对应的可验证商品事实（如成分 / 护理）；无真源事实不得编功效",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L27",
            # 注意 purpose 后半句"无真源事实不得编功效"是**禁令**不是字段：它没有对应的快照键，
            # 因此不为它单造一条 ContextRequirement（那等于把禁令伪装成"缺一个字段"）。
            # 它照抄进 purpose 作为本项的理由，真正的执行落在 postcheck / 检测器侧。
            "candidates": (
                (
                    "facts.product.material",
                    "facts.product.care",
                    "facts.product.care_instructions",
                ),
            ),
            "question": "这次想教顾客什么？对应的商品事实（成分 / 护理方式）有据可查吗？",
        },
    ),
    "BRAND_AWARENESS": (
        {
            # OD-03 L28｜品牌定位
            "field_path": "brand.positioning",
            "purpose": "品牌定位",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L28",
            "candidates": (
                (
                    "facts.brand.positioning",
                    "facts.brand_facts.positioning_statement",
                    "facts.brand_positioning",
                ),
            ),
            "question": "这个品牌怎么定位自己？（服务谁、做什么品类、什么档次）",
        },
        {
            # OD-03 L28｜说话调性
            "field_path": "brand.tone",
            "purpose": "说话调性",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L28",
            "candidates": (("facts.brand.tone", "facts.brand_facts.tone"),),
            "question": "品牌说话是什么调子？（例如稳、具体、不喊口号）",
        },
        {
            # OD-03 L28｜禁用表达清单
            "field_path": "brand.forbidden_expressions",
            "purpose": "禁用表达清单",
            "impact": IMPACT_BLOCKING,
            "od03": "OD-03 §二 L28",
            "candidates": (
                ("facts.brand.forbidden_expressions", "facts.brand_facts.forbidden_expressions"),
            ),
            "question": "哪些说法是这个品牌明令不许用的？",
        },
    ),
}

# 非阻断白名单（OD-03 §三 L30-L32）。L32 一整行四类，逐类对映如下。
# 只在目标已解析时才评估（接口规格：goal=None 时只出通用四项）——目标都还没定，
# 讨论"人设缺了要不要降 confidence"没有意义，只会给 Founder 增加噪音。
_QUALITY_REDUCING_REQUIREMENTS = (
    {
        # OD-03 L32｜人设 / 账号事实（缺 → 暂定人设标 ASSUMPTION、降 confidence、不得编造创始人背景——INT-D02）
        "field_path": "persona",
        "purpose": "人设事实（缺 → 暂定人设标 ASSUMPTION、降 confidence、不得编造创始人背景）",
        "impact": IMPACT_QUALITY_REDUCING,
        "od03": "OD-03 §三 L32",
        # L32 把"人设 / 账号"并列写成一项，这里拆成两条 ContextRequirement：
        # 两者在快照里是两个独立键（facts.persona / facts.video_account，实测），且 A.4.2 要求
        # "QUICK 跨过的每项缺失必须产生 ASSUMPTION"——拆开才能一缺一假设、假设文本各自贴切。
        # 拆分不改变 impact（两条都是 QUALITY_REDUCING），不构成对 OD-03 的加严或放宽。
        "candidates": (("facts.persona", "facts.persona_facts"),),
        "question": "出镜或讲述的人设是谁？（缺了会用暂定人设，且不会编创始人经历）",
    },
    {
        # OD-03 L32｜人设 / 账号事实（账号侧）
        "field_path": "video_account",
        "purpose": "账号事实（缺 → 账号关系只能暂定，不得编造）",
        "impact": IMPACT_QUALITY_REDUCING,
        "od03": "OD-03 §三 L32",
        "candidates": (("facts.video_account", "facts.video_account_facts"),),
        "question": "发在哪个视频号上？这个号平时讲什么、和顾客什么关系？",
    },
    {
        # OD-03 L32｜受众调研
        "field_path": "audience",
        "purpose": "受众调研",
        "impact": IMPACT_QUALITY_REDUCING,
        "od03": "OD-03 §三 L32",
        "candidates": (("facts.audience", "facts.audience_facts"),),
        "question": "这条视频主要说给谁听？有没有做过受众了解？",
    },
    {
        # OD-03 L32｜材质证明（除非涉及功效声明，届时升为对应目标的阻断项）
        "field_path": "product.material_proof",
        "purpose": "材质证明",
        "impact": IMPACT_QUALITY_REDUCING,  # 动态升级见 _material_proof_impact()
        "od03": "OD-03 §三 L32",
        # 诚实登记：M0 夹具无"材质证明"类键（有的是 material 成分本身，那是另一回事——
        # 成分是商品事实，证明是第三方检测/证书）。故本项在 M0 恒 MISSING 且 QUALITY_REDUCING。
        "candidates": (
            ("facts.product.material_proof", "facts.product.material_certification"),
        ),
        "question": "面料成分有没有检测报告或吊牌照片一类的凭证？",
    },
    {
        # OD-03 L32｜次要商品字段（如里料）
        "field_path": "product.lining",
        "purpose": "次要商品字段（如里料）",
        "impact": IMPACT_QUALITY_REDUCING,
        "od03": "OD-03 §三 L32",
        # OD-03 只举了"里料"一个例子，这里就只实现里料。想扩到别的次要字段 = 改口径，
        # 须回 OD-03 走版本升级 + Founder 签字（该文件「落位说明」行），执行侧不自行扩表。
        "candidates": (("facts.product.lining",),),
        "question": "里料是什么材质？（缺了不影响能不能做，只影响能说多细）",
    },
)


# ======================================================================================
# 六、两条特判：时间窗口正则 / 材质证明动态升级
# ======================================================================================

# 时间窗口的确定性识别口径（接口规格「快照事实→OD-03 字段映射」：
# 「时间窗口←task_statement 含"春节前/N周内"即 AVAILABLE（确定性正则，注明口径）否则 MISSING」）。
# **闭列表**，只认两种写法：
_TIME_WINDOW_PATTERNS = (
    re.compile(r"春节前"),                                   # 实测命中：INT-D02 与 INT-D03-a 的 task_statement
    re.compile(r"\d+\s*(?:天|周|个月|月|季度)内"),           # "N周内"族，阿拉伯数字
)
# 为什么闭得这么窄（这是有意的，不是没想到别的写法）：
#   OD-03 L23 把时间窗口列为 INVENTORY_ACTIVATION 的**阻断项**。判错的两个方向代价不对称——
#   多认一种写法 = 系统自以为知道期限、不再追问，直接产出一个可能踩错节奏的方案（编造上下文）；
#   少认一种写法 = 多问 Founder 一句。前者违反北极星①防幻觉，后者只是轻微增加认知负担。
#   故 fail-closed：没在闭列表里的写法一律判缺失。
# 已知缺口（如实登记，不假装覆盖）：中文数字写法（"六周内"）本正则识别不了。
#   目前不影响任何案例——E2E-01 / SYS-D01 的"六周"是走 facts.time_window 键进来的（Founder IA-0
#   OQ-BUILD-07 定值后回填），不依赖本正则。若将来出现只在 task_statement 里写中文数字期限的案例，
#   这里会判缺失并追问；扩正则 = 改口径，须回 OD-03 / IA-0。


def _time_window_in_statement(task_statement):
    """task_statement 里是否出现闭列表内的时间窗口写法。纯正则，无 NLP、无模型。"""
    if not task_statement:
        return False
    return any(p.search(task_statement) for p in _TIME_WINDOW_PATTERNS)


def _material_proof_impact(goal):
    """材质证明这一项的 impact（OD-03 L32 括号里的动态升级条款）。

    条款原文：「材质证明（除非涉及功效声明，届时升为对应目标的阻断项）」。
    v1 口径由接口规格「动态升级条款」行钉定，落地如下：

      · goal == CUSTOMER_EDUCATION：**结构上已经升级完毕**，本函数不重复升级。
        因为 OD-03 L27 已把"教育点对应的可验证商品事实（如成分 / 护理）；无真源事实不得编功效"
        列为该目标的阻断项——用户教育正是最典型的"涉功效声明"场景，L27 那一格就是 L32 括号
        在该目标下的落地形态。此时 _GOAL_REQUIREMENTS["CUSTOMER_EDUCATION"] 会给出一条 BLOCKING，
        材质证明本身仍留在白名单里做 QUALITY_REDUCING。

      · 其余五个目标：**不升级**。这是一个**如实登记的覆盖缺口，不是"已覆盖"**，理由两条：
        ① "涉及功效声明"没有判据。A / B / OD-03 三份真源里都没定义什么算功效声明。
           靠关键词猜（"保暖""抗菌""修护"…）就是拍脑袋造一个没人批准的检测器，
           与项目宪法「无检测器不得判 PASS」同侧的纪律相冲突——无判据也不得擅自加阻断，
           那会在没有依据的情况下把 Founder 拦在门外。
        ② 时序上也判不了。功效声明是 Creative 阶段**输出文本**里的表述，Intent 阶段还没有任何输出，
           这里能看到的只有 task_statement；用它反推"将来会不会写功效"属于预测，不是确定性前处理。
        因此本函数在其余目标下恒返回 QUALITY_REDUCING，该缺口由考卷侧 / 人工承接
        （同接口规格对 A.5.2 约束6「目标迁移跨运行」的处理方式：说明白，不假装覆盖）。

    参数只收 goal 而不收 task_statement，正是为了让"这里没有在猜关键词"这件事在签名上就可验证。
    """
    return IMPACT_QUALITY_REDUCING


# ======================================================================================
# 七、resolve_requirements：本文件的核心
# ======================================================================================


def _make_requirement(template, availability, source_refs, impact_override=None):
    """按模板产出一条 ContextRequirement（A.4.2 六字段，一个不多一个不少）。

    OD-03 L8「本清单不新增 A 之外的字段与状态」——所以这里硬编六个键，
    想加"匹配到的快照路径""od03 行号"之类的调试字段都不行：那会让产物不再是 A.4.2 对象，
    下游 Schema 校验（postcheck P1）能不能拦看 additionalProperties 的设置，拦不住就是私自扩合同。
    """
    resolvable = availability != AVAILABILITY_AVAILABLE
    return {
        "field_path": template["field_path"],
        "purpose": template["purpose"],
        "availability": availability,
        "impact": impact_override or template["impact"],
        # A.4.2 resolution_question 允许 null。字段齐备时置 None：给一个"已经有了还要问"的问题
        # 会直接变成 Founder 的噪音（北极星②）。
        "resolution_question": template["question"] if resolvable else None,
        # related_source_refs：把探针路上摸到的来源原样带上。
        # M0 夹具的 source 是自由文本字符串而非 A.2.3 SourceRef 对象——照原样放进去，
        # 不补造 SourceRef 结构（伪造溯源比没有溯源更危险）。
        # 结构上合法：common.defs.json 的 ContextRequirement.related_source_refs 只声明 {"type":"array"}，
        # 未约束 items（实测），所以字符串数组不会撞 Schema。
        "related_source_refs": list(source_refs),
    }


def _resolve_business_goal(goal, snapshot):
    """通用项 #2 business_goal 的可用性（OD-03 L15）。

    口径（接口规格「快照事实→OD-03 字段映射」）：business_goal ← stated_goal 参数 **或** facts.business_goal。
    参数优先：A.4.1 Task.stated_business_goal 是目标的正式承载位（INT-D02 的 IA-0 裁决就是这样落的，
    见 acceptance/cases/INT-D02/fixtures/task_input.json）；快照里的 facts.business_goal 是次选。
    两者都没有 → MISSING → BLOCKING → 上层强制 NEEDS_INPUT（A.4.2「BLOCKING 缺失在任何模式都进入
    NEEDS_INPUT」＋ OD-03 L15「听不出来必须问，不许猜」）。

    **快照侧枚举守卫**（M1-EP02 修复批次 K1）：facts.business_goal 有值但**不在 A.2.6 六枚举内**时，
    本函数判 MISSING，而不是把这个值当成"目标已在场"。
    理由是 OD-03 L15 原文「商业目标六选一已解析；听不出来必须问，不许猜」——快照里写着
    "春节大促" / "冲一波销量" 这类自由文本，落不到六选一，就是**没解析**；
    把它当在场会让 business_goal 这一阻断项被一句没人认识的字符串糊过去，系统从此不再追问（fail-open）。
    这里选 fail-closed：认不出来就是缺，多问 Founder 一句，绝不放行一个不在枚举里的"目标"。
    注意与 goal 入参侧的区别：goal 入参走 resolve_requirements 入口的 fail-loud 校验（枚举外直接 raise，
    因为那说明 runner 没做枚举校验，是代码缺陷）；快照侧是数据问题，判缺失并追问才是正确处置。
    """
    if goal is not None:
        # goal 已经在 resolve_requirements 入口校验过属于六枚举，这里不再重复校验。
        return AVAILABILITY_AVAILABLE, []
    node = _get_by_path(snapshot, "facts.business_goal")
    availability = _availability_of_node(node)
    refs = _source_refs_of(node) if _is_fact_leaf(node) else []
    if availability == AVAILABILITY_AVAILABLE:
        raw = node.get("value") if _is_fact_leaf(node) else node
        if raw not in BUSINESS_GOALS:
            sys.stderr.write(
                "[intent.preprocess] 枚举守卫：快照 facts.business_goal=%r 不在 A.2.6 六枚举内，"
                "按 OD-03 L15「听不出来必须问，不许猜」判 MISSING（fail-closed，不当作目标已在场）\n"
                % (raw,)
            )
            availability = AVAILABILITY_MISSING
    return availability, refs


def resolve_requirements(goal, snapshot, task_statement):
    """按 OD-03 算出 (required_context, missing_context)，两者元素均为 A.4.2 六字段 dict。

    这是 Intent"不套壳"的核心证据：目标一变，required_context 就变；事实一缺，missing_context 就有；
    全过程零模型参与——模型只负责把用户那句话解析成六个目标之一（或说不出来），剩下的都是查表。

    参数：
      goal            六枚举之一，或 None。None = 目标未解析（AMBIGUOUS / NEEDS_INPUT）。
                      按接口规格，goal=None 时**只出通用四项**——目标都没定，谈分目标追加项没有意义，
                      列一堆"库存激活才需要的字段"只会误导 Founder 以为系统已经认定了目标。
      snapshot        load_snapshot() 的返回值（M0 扁平夹具形状，容错读取）。
      task_statement  任务原话。只有一个用途：时间窗口的确定性识别（见 _time_window_in_statement）。

    返回：
      (required_context, missing_context)
      missing_context 是 required_context 的**子集且共享同一批 dict 对象**（不复制）。
      为什么不复制：两份最终会一起进同一个 ArtifactEnvelope，复制出来的两份一旦被上层各改一次
      就会出现"同一字段两种状态"的自相矛盾产物。共享对象让这种矛盾在物理上不可能发生。

    成员判定：availability != AVAILABLE 即计入 missing_context——
    即 MISSING 与 CONFLICTING 都算缺（OD-03 L37「字段 availability=CONFLICTING（如双价）视同缺失处理」），
    但 availability 字段本身保留 CONFLICTING 原值，不改写成 MISSING（改写会抹掉"有冲突"与"没有"的区别）。
    """
    if goal is not None and goal not in BUSINESS_GOALS:
        # fail-loud：目标值不在六枚举内说明调用方（runner）没做枚举校验就把模型输出直接透传进来了。
        # 悄悄当成 None 处理会掩盖这个 bug，而且 A.4.2「目标不明确时不得填入唯一 business_goal」
        # 要求的是显式走"未解析"分支，不是猜。
        raise ValueError(
            "goal 必须是 A.2.6 BusinessGoal 六枚举之一或 None，收到：%r。"
            "模型给出枚举外目标时，runner 应传 None 走未解析分支。" % (goal,)
        )

    required = []

    # --- 通用四项（OD-03 §一 L10-L17），任何任务都要，顺序照 OD-03 表 -------------------
    for template in _UNIVERSAL_REQUIREMENTS:
        field_path = template["field_path"]
        if field_path == BUSINESS_GOAL_FIELD_PATH:
            availability, refs = _resolve_business_goal(goal, snapshot)
        elif field_path == "platform":
            # OD-03 L17 + 接口规格：常量 WECHAT_VIDEO，恒 AVAILABLE。
            # 不去快照里找 platform 键：A.2.6 Platform 枚举只有这一个值，它是运行常量不是事实。
            availability, refs = AVAILABILITY_AVAILABLE, []
        else:
            availability, refs = _probe(snapshot, template["candidates"])
        required.append(_make_requirement(template, availability, refs))

    if goal is not None:
        # --- 分目标追加阻断项（OD-03 §二 L19-L28） -------------------------------------
        for template in _GOAL_REQUIREMENTS[goal]:
            if template["field_path"] == "task.time_window":
                # 时间窗口两条来源：快照 facts.time_window 键（E2E/SYS 家族），
                # 或 task_statement 里的闭列表写法（INT 家族）。任一命中即在场。
                availability, refs = _probe(snapshot, template["candidates"])
                if availability != AVAILABILITY_AVAILABLE and _time_window_in_statement(task_statement):
                    availability, refs = AVAILABILITY_AVAILABLE, []
            else:
                availability, refs = _probe(snapshot, template["candidates"])
            required.append(_make_requirement(template, availability, refs))

        # --- 非阻断白名单（OD-03 §三 L30-L32） -----------------------------------------
        # 去重：分目标阻断项已经点名的 field_path（如 BRAND_STORY 下的 persona）不再以
        # QUALITY_REDUCING 的身份出现第二次。"特殊优先于一般"的理由写在 _GOAL_REQUIREMENTS
        # ["BRAND_STORY"] 的 persona 条目注释里。同一个字段出现两条状态不同的 ContextRequirement，
        # 会让下游"是不是阻断"变成看谁排在前面，那是纯粹的口径事故。
        claimed = {item["field_path"] for item in required}
        for template in _QUALITY_REDUCING_REQUIREMENTS:
            if template["field_path"] in claimed:
                continue
            availability, refs = _probe(snapshot, template["candidates"])
            impact = None
            if template["field_path"] == "product.material_proof":
                impact = _material_proof_impact(goal)
            required.append(_make_requirement(template, availability, refs, impact_override=impact))

    missing = [item for item in required if item["availability"] != AVAILABILITY_AVAILABLE]
    return required, missing
