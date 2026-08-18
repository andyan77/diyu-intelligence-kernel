#!/usr/bin/env python3
"""资产④ 确定性后校验 · Preflight（Intent 侧）。

定位（G.2 第 4 条纪律，逐条对齐）：
  ① 三件套，**不造约束 DSL**——本文件只用 JSON Schema（P1）+ 词表/正则（P8/P9）+ Python 谓词（P2-P7）；
  ② **双阶段命名**：本文件是 Preflight（生成前，落 A.5.2 既有语义），Delivery（生成后，A.7.2 validation）不在此；
  ③ **逐条标注 machine_checkable**——首批 P1-P9 全部 true；不得用一个全局合规图章掩盖语义盲区；
  ④ 首批规则按既有合同落点实现，不新增 Gate、不新增模块、不扩 A.9.1 冻结字段。

三态契约（对齐 acceptance/detectors/checks.py 的 L1 口径，C.4 铁律1）：
  每项 check 返回 verdict ∈ {"OK","FAIL","UNKNOWN"}；**证据不足一律 UNKNOWN 向上冒泡**，
  既不判 OK（那是假绿）也不判 FAIL（那是假红——把"没核验成"说成"违约"，同样是编造结论）。

overall 只有两值（接口规格钉死 {"OK","FAIL"}），因此 UNKNOWN 必须归到哪一侧要说清楚：
  **overall = OK 当且仅当九项全 OK**；任一 FAIL **或** 任一 UNKNOWN → overall = FAIL。
  理由：北极星 1「无检测器不得判 PASS」——"没核验成"不得被吸收成"通过"。
  但每项 verdict 原值保留（UNKNOWN 不会被改写成 FAIL），人读 report 时能区分"违约"与"没核验成"。

约束覆盖对照（A.5.2 七条约束，A:561-569）：
  约束1/2（AMBIGUOUS/NEEDS_INPUT → business_goal 空 + REQUEST_INPUT + 候选≥2）→ **P1 承担**
      （写在 intent_execution_plan.schema.json 的 allOf 条件式里，这里不重复实现第二套判定，
        两套判定会漂移；P1 一旦 FAIL/UNKNOWN，约束1/2 即视为未通过）。
      **诚实登记（M1-EP02 修复批次 K4，改掉首轮的超陈述）**：约束1 的「候选≥2」这一半，
      在本批次之前**并未被真正覆盖**——首轮的 Schema 只在 AMBIGUOUS 分支的 `then.properties`
      里给 goal_candidates 写了 minItems:2，而 JSON Schema 的 `properties` 对**缺席的键**是空操作：
      产物干脆不发 goal_candidates 键时，该分支照样判过。这个洞由同批次考卷侧（Agent A）
      给该分支补 `"required": ["goal_candidates"]` 堵上。本模块 docstring 因此不再声称
      「schema 修复前 P1 已覆盖约束1」；修复后的覆盖情况由 test_intent_offline.py 的
      正向对照组①（AMBIGUOUS 且无 goal_candidates 键 → P1 必 FAIL）实跑证明，不靠声明。
  约束3 → P2；约束4 → P3；约束5 → P4（**判据按 M1-EP02 仲裁1 的自洽解**，见 _p4_constraint5
      文档串的四条证据链与台账登记句）；约束7 → P5（只覆盖两个常量，见 P5 诚实边界）；
  约束6（同一快照只改目标时 business_goal / required_context 应变、未改事实必须保持）
      → **不在单次 Preflight 射程**：它要求比对同一快照下的两次运行产物，本函数只看单份 plan，
        看不见另一次运行。故此处**不设 P 项、不假装覆盖**；该约束由考卷侧 INT-D03（input-a/input-b
        双输入对照）与人工判分承担。任何"Preflight 全 OK"都**不代表**约束6 已被机器验证。

ctx 键（接口规格钉死五键 + 一个可选键）：
  schema_path      IntentExecutionPlan Schema 路径；P1 的 RefResolver base_uri 取其所在目录
                   （必须是 contracts/schemas/，否则 common.defs.json#/definitions/* 解析不到）
  fact_pool        preprocess.materialize_fact_pool 的产物（元素含 fact_id）
  rule_pool        preprocess.load_rule_pool 的产物（元素含 rule_id）
  snapshot         ContextSnapshot 原始 dict（P9 溯源底本）
  execution_mode   "QUICK" | "ENHANCED"（P3 只在 QUICK 且继续时才触发）
  lexicon_path     [可选] 禁用表达词表路径；缺省用仓库内 acceptance/detectors/forbidden_lexicon.yaml
                   （只读，词表属考卷区，本模块**绝不写**它）
  为什么加可选第六键：P8 需要词表路径，而规格给的五键里没有；不从 config.py 硬 import 是为了
  不与同批次其他代理的建档顺序耦合（config.py 由另一资产落盘）——runner 传就用传的，不传走仓库默认。
"""
import json
import os
import re

import yaml
from jsonschema import Draft7Validator, RefResolver
from jsonschema.exceptions import RefResolutionError

# 「目标这一项」的 field_path 字面。硬 import 自 config（唯一落点）——
# 仲裁1 的判据要按「阻断缺失集合减去 business_goal 还剩不剩」分岔，runner 的 G2 与本模块的 P4
# 必须逐字同源；在这里再写一遍字面，就是规格明令禁止的"两套判据"。
from kernel.intent.config import BUSINESS_GOAL_FIELD_PATH, FACT_ID_PREFIX

STAGE = "PREFLIGHT"

# 仓库根：本文件在 <repo>/kernel/intent/postcheck.py，向上三层即仓库根。
# 用 __file__ 推而不写死绝对路径，是为了 clone 到任何目录都能跑（P0-6 干净 clone 回执口径）。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_LEXICON_PATH = os.path.join(_REPO_ROOT, "acceptance", "detectors", "forbidden_lexicon.yaml")

_IMPACT_VALUES = ("BLOCKING", "QUALITY_REDUCING")          # A.4.2 ContextRequirement.impact 只有两值
_MISSING_AVAILABILITY = ("MISSING", "CONFLICTING")          # OD-03 四-2：CONFLICTING 视同缺失
_TASK_TYPE_CONST = "VIDEO_CONTENT_CREATION"                 # A:543
_PLATFORM_CONST = "WECHAT_VIDEO"                            # A:544
# FACT trace_id 的前缀（接口规格「FACT ID 约定」：FACT:<field_path>）。P6 的前缀伪装判定用它。
# 取自 config 而不是在这里重写一遍字面：前缀一旦在 config 改掉而这里没跟着改，
# P6 会安静地判不出任何伪装（判据用的前缀根本不存在了），属"检测器静默失效"型假绿。
_FACT_ID_PREFIX = FACT_ID_PREFIX


# ============================ 通用小工具 ============================

def _strings(obj, out):
    """递归收集对象里的所有字符串（与 acceptance/detectors/checks.py::_texts 同形，
    刻意复制而非 import：kernel 不得依赖考卷区代码，否则改考卷会静默改考生行为（C.2 隔离门）。"""
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _strings(v, out)
    return out


def _collect_missing(plan):
    """归集"缺失集合"，返回 (items, 无从核验原因)；items 为 None 表示该结构不可核验（调用方判 UNKNOWN）。

    口径（**并集**，不是只看 missing_context）：
      missing_context 全体 ∪ required_context 中 availability ∈ {MISSING, CONFLICTING} 的条目。
    为什么要并集：只看 missing_context 会留一条假绿通道——把一条 availability=MISSING、impact=BLOCKING
      的需求只写进 required_context、missing_context 留空，约束3/5 就都"过"了，而事实上它就是缺的。
      A.4.2 的 availability 字段本身就是权威判据，OD-03 四-2 又明确 CONFLICTING 视同缺失，
      故两处都算数。按 field_path 去重。
    去重冲突取严（BLOCKING 优先）：同一 field_path 在两个数组里 impact 写得不一样（required_context
      写 BLOCKING、missing_context 写 QUALITY_REDUCING）是自相矛盾的 plan；若按"先入为准"就留下一条
      旁路——把阻断项在 missing_context 里降级成 QR，约束3/4/5 全部绕过。故取更严的那个，
      并在 origin 上留痕（impact_conflict），让 report 的 detail 能指出矛盾本身。
    """
    mc, rc = plan.get("missing_context"), plan.get("required_context")
    if not isinstance(mc, list) or not isinstance(rc, list):
        return None, "missing_context / required_context 不是数组，缺失集合无从核验"
    out, index = [], {}
    for origin, arr in (("missing_context", mc), ("required_context", rc)):
        for it in arr:
            if not isinstance(it, dict):
                return None, f"{origin} 含非对象条目，缺失集合无从核验"
            fp, av = it.get("field_path"), it.get("availability")
            if not isinstance(fp, str) or not fp.strip():
                return None, f"{origin} 有条目缺 field_path（或非字符串），缺失集合无从核验"
            if origin == "required_context" and av not in _MISSING_AVAILABILITY:
                continue                      # required_context 里 AVAILABLE 的项不是缺失，跳过
            if fp in index:
                prev = index[fp]
                if it.get("impact") == "BLOCKING" and prev["impact"] != "BLOCKING":
                    prev["impact"], prev["origin"] = "BLOCKING", f"{prev['origin']}+{origin}(impact_conflict)"
                continue
            rec = {"field_path": fp, "impact": it.get("impact"), "availability": av, "origin": origin}
            index[fp] = rec
            out.append(rec)
    return out, ""


def _bad_impacts(items):
    """impact 不是 A.4.2 两枚举之一的条目 → 无法判定它是不是 BLOCKING → 调用方必须 UNKNOWN。"""
    return [i["field_path"] for i in items if i["impact"] not in _IMPACT_VALUES]


def _assumption_entries(plan):
    """取全部 ASSUMPTION TraceEntry，返回 (entries, 无从核验原因)。

    为什么取两处并集：A.5.2 把 assumptions 单列为顶层字段（A:555），同时 TraceBundle 也收 ASSUMPTION
    条目（A.9.2）；两处都是合同承认的落点，只认一处会把另一处的合法写法误判成"没产生 ASSUMPTION"。
    按 trace_id 去重；没有 trace_id 的条目照收（它的结构问题归 P1 的 schema 判定，不在这里重判）。
    """
    top = plan.get("assumptions")
    if not isinstance(top, list):
        return None, "assumptions 不是数组，ASSUMPTION 配对无从核验"
    tb = plan.get("trace_bundle")
    tb_entries = tb.get("entries") if isinstance(tb, dict) else None
    if tb_entries is None:
        tb_entries = []                        # TraceBundle 缺失由 P1（required）与 P6 各自表态，这里不重复判红
    elif not isinstance(tb_entries, list):
        return None, "trace_bundle.entries 不是数组，ASSUMPTION 配对无从核验"
    out, seen = [], set()
    for e in list(top) + list(tb_entries):
        if not isinstance(e, dict):
            return None, "assumptions / trace_bundle.entries 含非对象条目，ASSUMPTION 配对无从核验"
        if e.get("trace_type") not in (None, "ASSUMPTION"):
            continue                           # TraceBundle 里的 FACT/RULE/MODEL_JUDGMENT 不参与配对；
                                               # trace_type 缺失的条目按 assumptions 字段的位置语义收下（其结构问题归 P1）
        tid = e.get("trace_id")
        if isinstance(tid, str) and tid in seen:
            continue
        if isinstance(tid, str):
            seen.add(tid)
        out.append(e)
    return out, ""


# _assumption_covers 的三态返回值（M1-EP02 修复批次 K4）。
_COVER_EXACT = "EXACT"              # target_paths 精确含该 field_path
_COVER_STATEMENT_ONLY = "STATEMENT" # 只有 statement 文本里出现该串
_COVER_NONE = "NONE"                # 两处都没有


def _assumption_covers(entry, field_path):
    """一条 ASSUMPTION 对某缺失项的覆盖强度，三态返回（不再是 True/False）。

    口径（M1-EP02 修复批次 K4 改，与考卷侧 acceptance/detectors/checks.py::intent_assumption_coverage
    **同批同改、逐字一致**——两侧口径分叉就等于两把尺子量同一件事）：
      · _COVER_EXACT           ← target_paths 里精确出现该 field_path。
        这是唯一算"配上了"的形态：A.9.2 的 TraceEntry.target_paths 就是干这个的，
        它是结构化绑定，机器可判、不受文本写法影响。
      · _COVER_STATEMENT_ONLY  ← 只在 statement 原文里出现该 field_path 串。
        **首轮把它当 OK，是一条假绿通道**：statement 是自由文本，"缺 product.lining" 这句话里
        出现 `product.lining` 会命中，但"本次不涉及 product.lining 之外的字段"这种**反向叙述**、
        或一条把所有缺失项名字列一遍的总述句，同样会命中——一条泛泛的总述就能把 N 个缺失项
        全部"配对"掉。子串命中证明不了"这条假设是针对这一项做的"，因此降为 UNKNOWN
        （证据不足向上冒泡），**不判 OK 也不判 FAIL**：它确实提到了这一项，判红是假红。
      · _COVER_NONE            ← 两处都没有 → 真的没有对应假设 → 调用方判 FAIL。

    这条配对规则是本模块自定的**实现层约定**，不是合同字段，故写在这里而不是扩 A 的冻结字段。
    """
    paths = entry.get("target_paths")
    if isinstance(paths, list) and any(isinstance(p, str) and p == field_path for p in paths):
        return _COVER_EXACT
    stmt = entry.get("statement")
    if isinstance(stmt, str) and field_path in stmt:
        return _COVER_STATEMENT_ONLY
    return _COVER_NONE


# ============================ P1 ~ P9 ============================

def _p1_schema(plan, ctx):
    """P1 结构校验。约束1/2 的条件式就写在这份 Schema 的 allOf 里，故 P1 同时是约束1/2 的判定口。"""
    path = ctx.get("schema_path")
    if not path or not os.path.exists(path):
        return "UNKNOWN", f"schema_path 未配置或不存在: {path!r}——结构无从核验（≠通过）"
    try:
        with open(path, encoding="utf-8") as f:
            schema = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return "UNKNOWN", f"Schema 读取/解析失败，结构无从核验: {type(e).__name__}: {e}"
    # base_uri 必须指向 Schema 所在目录（contracts/schemas/），否则 "common.defs.json#/definitions/…"
    # 这类相对 $ref 解析不到——与 tools/validate_schema.py 同一口径，两处不得分叉。
    base = "file://" + os.path.abspath(os.path.dirname(path)) + "/"
    resolver = RefResolver(base_uri=base, referrer=schema)
    try:
        errors = sorted(Draft7Validator(schema, resolver=resolver).iter_errors(plan),
                        key=lambda e: list(e.absolute_path))
    except RefResolutionError as e:
        # $ref 解析失败 = 没核验成，**不是**实例违约：绝不能报 FAIL 让人以为是 plan 的错
        return "UNKNOWN", f"$ref 解析失败（base_uri={base}），结构无从核验: {e}"
    if errors:
        head = "; ".join(f"/{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in errors[:5])
        return "FAIL", f"{len(errors)} 处结构违约: {head}"[:800]
    return "OK", f"结构合规（含约束1/2 条件式）；schema={os.path.basename(path)}"


def _p2_constraint3(plan, ctx):
    """P2 = A.5.2 约束3：只有 RESOLVED + business_goal 非空 + 无 BLOCKING 缺失，才准 CONTINUE_TO_DECISION。"""
    na = plan.get("next_action")
    if na not in ("CONTINUE_TO_DECISION", "REQUEST_INPUT"):
        return "UNKNOWN", f"next_action 缺失或非法（{na!r}），约束3 无从核验"
    if na != "CONTINUE_TO_DECISION":
        return "OK", "next_action=REQUEST_INPUT，约束3 是对「继续」的必要条件，本次不触发"
    items, why = _collect_missing(plan)
    if items is None:
        return "UNKNOWN", why
    bad = _bad_impacts(items)
    if bad:
        return "UNKNOWN", f"缺失项 impact 非法/缺失（{bad}），是否有 BLOCKING 缺失无从核验"
    problems = []
    gr, bg = plan.get("goal_resolution"), plan.get("business_goal")
    if gr != "RESOLVED":
        problems.append(f"goal_resolution={gr!r}≠RESOLVED")
    if not (isinstance(bg, str) and bg.strip()):
        problems.append(f"business_goal 为空（{bg!r}）")
    blocking = [i["field_path"] for i in items if i["impact"] == "BLOCKING"]
    if blocking:
        problems.append(f"存在 BLOCKING 缺失 {blocking}")
    if problems:
        return "FAIL", "CONTINUE_TO_DECISION 但 " + "；".join(problems)
    return "OK", f"CONTINUE 三条件齐备（RESOLVED / goal={bg} / 无 BLOCKING 缺失，共 {len(items)} 项缺失）"


def _p3_constraint4(plan, ctx):
    """P3 = A.5.2 约束4（A:566）+ A:393 + OD-03 四-1。

    三件事一起判（前两件是约束4 原文，第三件是 A:393 / OD-03 四-1 的后半句，首轮漏了）：
      ① QUICK 继续时跨过的缺失必须**全为** QUALITY_REDUCING；
      ② 每一项跨过的缺失都要有**对应的** ASSUMPTION（配对强度见 _assumption_covers 三态口径）；
      ③ 跨过了缺失还给 confidence.level=HIGH → FAIL。
         出处 A:393「QUICK 跨过的每项缺失必须产生 ASSUMPTION **和 confidence 限制**」、
         OD-03 四-1「每跨一项必须产生 ASSUMPTION 和 confidence 限制」。
         首轮只判了 ASSUMPTION 那一半，"限制"那一半没人判——于是一份"跨过五项缺失、
         逐项挂了假设、置信度照给 HIGH"的产物可以全绿通过，那正是 INT_CONFIDENCE_OVERSTATED 的形态。
         这里只把 HIGH 判红（"限制"的最低含义就是不得停留在最高档）；MEDIUM 与 LOW 之间该怎么分档
         A 与 OD-03 都没规定，本项**不假装能判**，不自造阈值。

    **QUICK 前置的口径来源与已知分叉（如实登记，不合并）**：
      本项只在 `execution_mode == "QUICK"` 且 `next_action == "CONTINUE_TO_DECISION"` 时触发，
      依据是 A:566 原文「**QUICK 继续时**，跨过的缺失项必须为 QUALITY_REDUCING，并产生对应 ASSUMPTION」——
      真源写了模式前置，本模块照写（真源 > 规格）。
      而考卷侧 acceptance/detectors/checks.py::intent_assumption_coverage **不分模式**判同一件事。
      两侧因此存在一处口径分叉：ENHANCED 模式下带缺失继续时，考卷侧会判、本模块不判。
      这不是谁写错了——考卷侧是"验收判分"（可以比合同更严），本模块是"合同执行面"（不得超出合同射程）；
      但分叉本身必须被看见，故在此登记，不靠"两边都改成一样"来消化。
    """
    mode = ctx.get("execution_mode")
    if mode not in ("QUICK", "ENHANCED"):
        return "UNKNOWN", f"ctx.execution_mode 缺失或非法（{mode!r}），约束4 是否触发无从判定"
    na = plan.get("next_action")
    if na not in ("CONTINUE_TO_DECISION", "REQUEST_INPUT"):
        return "UNKNOWN", f"next_action 缺失或非法（{na!r}），约束4 无从核验"
    if not (mode == "QUICK" and na == "CONTINUE_TO_DECISION"):
        return "OK", f"约束4 只约束「QUICK 继续」（当前 mode={mode} / next_action={na}），本次不触发"
    items, why = _collect_missing(plan)
    if items is None:
        return "UNKNOWN", why
    bad = _bad_impacts(items)
    if bad:
        return "UNKNOWN", f"缺失项 impact 非法/缺失（{bad}），跨过项性质无从核验"
    non_qr = [i["field_path"] for i in items if i["impact"] != "QUALITY_REDUCING"]
    if non_qr:
        return "FAIL", f"QUICK 继续却跨过了非 QUALITY_REDUCING 缺失: {non_qr}"
    entries, why2 = _assumption_entries(plan)
    if entries is None:
        return "UNKNOWN", why2
    unpaired, weak = [], []
    for i in items:
        strengths = {_assumption_covers(e, i["field_path"]) for e in entries}
        if _COVER_EXACT in strengths:
            continue
        (weak if _COVER_STATEMENT_ONLY in strengths else unpaired).append(i["field_path"])
    if unpaired:
        return "FAIL", f"这些跨过的缺失项没有对应 ASSUMPTION（target_paths 或 statement 均未提及）: {unpaired}"
    # ③ confidence 限制（A:393 / OD-03 四-1 的后半句）。放在 weak 之前判：HIGH 是硬证据，
    #    "配对强度不足"是证据不足；有硬证据时不该被 UNKNOWN 盖过去。
    conf = plan.get("confidence")
    if not isinstance(conf, dict) or conf.get("level") not in ("HIGH", "MEDIUM", "LOW"):
        return "UNKNOWN", "confidence.level 缺失或非三级枚举，「每跨一项必须产生 confidence 限制」无从核验"
    if items and conf["level"] == "HIGH":
        return "FAIL", (f"QUICK 跨过 {len(items)} 项 QUALITY_REDUCING 缺失 "
                        f"{[i['field_path'] for i in items]}，却仍给 confidence.level=HIGH"
                        "（A:393 / OD-03 四-1：每跨一项必须产生 ASSUMPTION **和 confidence 限制**）")
    if weak:
        return "UNKNOWN", (f"这些跨过的缺失项只在 ASSUMPTION 的 statement 文本里被提到、"
                           f"target_paths 未精确绑定，配对强度不足以判过: {weak}"
                           "（子串命中证明不了假设是针对该项做的——见 _assumption_covers 口径）")
    return "OK", (f"{len(items)} 项跨过的缺失全为 QUALITY_REDUCING、逐项有 target_paths 精确绑定的 ASSUMPTION"
                  f"（共 {len(entries)} 条），且 confidence.level={conf['level']}（非 HIGH）")


def _p4_constraint5(plan, ctx):
    """P4 = A.5.2 约束5（A:567「BLOCKING 缺失时 goal_resolution 为 NEEDS_INPUT」）。

    ============================ 判据（M1-EP02 修复批次仲裁1 钉定） ============================
    首轮把约束5 逐字实现成「有 BLOCKING 就必须 NEEDS_INPUT」，结果是 INT-D01 这类"目标没说清、
    除目标外什么都不缺"的运行永远过不了 Preflight——而 B 恰恰明写这种情形必须保留 AMBIGUOUS。
    仲裁1 的自洽解是：**AMBIGUOUS 这个标签只承载「目标未明」这一件事**，于是四条分支：

      · goal_resolution == RESOLVED   且存在 BLOCKING 缺失                        → FAIL
      · goal_resolution == AMBIGUOUS  且 BLOCKING 缺失集合 − {business_goal} 非空 → FAIL（必须 NEEDS_INPUT）
      · goal_resolution == AMBIGUOUS  且 BLOCKING 缺失 ⊆ {business_goal}（含空集）→ OK
      · goal_resolution == NEEDS_INPUT                                            → OK

    ============================ 证据链（逐条带出处） ============================
    ① B:285-286（M1-EP02 修复规格记作 B:283-286，实测行号为 285-286，以真源为准）明文：
       「用户明确选择快速模式时，可以返回暂定目标候选，**但必须保留 AMBIGUOUS**、missing_context、
       assumptions 和非高置信度」——INT-D01 的 business_goal 按 OD-03 §一 #2 是必然阻断缺失，
       若 P4 一律要求 NEEDS_INPUT，B 这一句在该案例上永远不可能成立。
    ② A 约束1（A:563）本身把 AMBIGUOUS 定为合法终态：它规定 AMBIGUOUS 时 business_goal 为空、
       候选≥2、next_action=REQUEST_INPUT、**Task 必须进入 NEEDS_INPUT**。那句约束的是
       **Task 的状态**，不是 goal_resolution 这个标签——两者是不同的字段，不能互相顶替。
    ③ OD-03 §一 #2 的「A 对应」列写的是 `business_goal（A.5.2：goal_resolution=RESOLVED 才可继续）`，
       引的是**约束3**（继续的必要条件），不是约束5。OD-03 并未要求"目标缺失即 NEEDS_INPUT"。
    ④ 字面孤读（"有 BLOCKING 就必须 NEEDS_INPUT"，不看是哪一项）会同时把 A 约束1 的 AMBIGUOUS
       分支与 B:285 变成死条文——一条冻结合同不会写一格自己永远走不到的分支。

    ============================ 台账登记 ============================
    本判据是执行侧对两条冻结真源的**自洽解释**，不是真源原文。已获 Founder 认可
    （2026-08-17 裁决，台账 SPEC-DEV-01 行）；日后若推翻，改的是本函数与 runner.apply_hard_gates 的
    G2 分支两处（口径同源，见 config.BUSINESS_GOAL_FIELD_PATH 注释），不改考卷。

    诚实边界：AMBIGUOUS 分支判 OK **不代表**"目标已解析"或"这次运行可以继续"——
    继续与否由 P2（约束3）判，那里 goal_resolution != RESOLVED 一律拦。
    """
    items, why = _collect_missing(plan)
    if items is None:
        return "UNKNOWN", why
    bad = _bad_impacts(items)
    if bad:
        return "UNKNOWN", f"缺失项 impact 非法/缺失（{bad}），是否有 BLOCKING 缺失无从核验"
    gr = plan.get("goal_resolution")
    if gr not in ("RESOLVED", "AMBIGUOUS", "NEEDS_INPUT"):
        # 先判 goal_resolution 合法性再谈分支：标签认不出来时，"有没有 BLOCKING"这件事再清楚
        # 也推不出结论，只能 UNKNOWN（不是 OK 也不是 FAIL）。
        return "UNKNOWN", f"goal_resolution 缺失或非法（{gr!r}），约束5 无从核验"
    blocking = [i["field_path"] for i in items if i["impact"] == "BLOCKING"]
    if not blocking:
        return "OK", f"无 BLOCKING 缺失（缺失共 {len(items)} 项），约束5 不触发"
    if gr == "NEEDS_INPUT":
        return "OK", f"BLOCKING 缺失 {blocking} 已进入 NEEDS_INPUT"
    if gr == "RESOLVED":
        return "FAIL", (f"存在 BLOCKING 缺失 {blocking}，但 goal_resolution=RESOLVED"
                        "（约束5：任何模式都必须进入 NEEDS_INPUT）")
    # 剩下只有 AMBIGUOUS：按仲裁1，只有当阻断缺失全部落在 business_goal 这一项上时才放行。
    others = [fp for fp in blocking if fp != BUSINESS_GOAL_FIELD_PATH]
    if others:
        return "FAIL", (f"goal_resolution=AMBIGUOUS，但阻断缺失里还有非 {BUSINESS_GOAL_FIELD_PATH} 的项 {others}"
                        "——AMBIGUOUS 只承载「目标未明」，其余阻断缺失必须进 NEEDS_INPUT（仲裁1）")
    return "OK", (f"goal_resolution=AMBIGUOUS 且阻断缺失仅 {blocking}"
                  f"（⊆ {{{BUSINESS_GOAL_FIELD_PATH}}}），按仲裁1 放行；"
                  "「能否继续」另由 P2/约束3 判定，本项放行不等于可继续")


def _p5_scope_constants(plan, ctx):
    """P5 = A.5.2 约束7 + 两个常量（A:543-544）：Intent 只输出视频号内容任务计划。

    诚实边界：本项只覆盖**常量面**（task_type / platform 两个字段值）。
    "intent_summary 描述的是否真是一条视频号内容任务"属语义面，无检测器 → **不在本项射程**，
    不得因 P5=OK 就宣称约束7 已被完整机器验证（OD-03 一-4「其他平台不得静默适配」的语义部分同理）。
    """
    tt, pf = plan.get("task_type"), plan.get("platform")
    if tt is None or pf is None:
        return "UNKNOWN", f"task_type/platform 缺失（{tt!r}/{pf!r}），常量面无从核验"
    wrong = []
    if tt != _TASK_TYPE_CONST:
        wrong.append(f"task_type={tt!r}≠{_TASK_TYPE_CONST}")
    if pf != _PLATFORM_CONST:
        wrong.append(f"platform={pf!r}≠{_PLATFORM_CONST}（本期只出视频号）")
    if wrong:
        return "FAIL", "；".join(wrong)
    return "OK", f"常量面合规（{tt}/{pf}）；语义面（摘要是否真为视频号内容任务）不在本项射程"


def _p6_trace_pool(plan, ctx):
    """P6 = A.1.2 + A.9.2 + 本模块 ID 池约定：FACT/RULE trace 只能引用预物化池；候选的支撑引用不得悬空。

    池外 ID 一律 FAIL——这是"模型只许引用预物化 FACT/RULE ID"这条形态红线的机器执行面：
    模型编一个 FACT:xxx 出来，若不判红，编造事实就直通下游。
    ASSUMPTION / MODEL_JUDGMENT 的 trace_id 由 runner 生成、不在池中，故不做池成员判定（否则必然假红）。

    本批次新增两条（M1-EP02 修复批次 K4）：
      ① **RULE 条目必须真的引用了规则版本**：object_refs 非空，且其中至少一条带 version。
         出处 A:68「RULE｜当前任务适用的已启用硬规则｜**必须引用规则版本**」。
         首轮判不了这条，是因为规则池形状不带 version，trace.py 只能把 object_refs 留空——
         "缺口在上游"不等于"这条约束不该判"。K1 已把 version 从 contracts/rules/*.yaml 真源透传出来，
         现在判得了，就必须判：否则一份 object_refs 全空的产物照样全绿，A:68 形同虚设。
      ② **trace_id 前缀与 trace_type 必须自洽**：`FACT:` 前缀的条目 trace_type 只能是 FACT；
         trace_id 落在规则池 rule_id 集合里的条目 trace_type 只能是 RULE。
         出处 A:72「ASSUMPTION 和 MODEL_JUDGMENT 不得伪装为 FACT」。
         没有这条时，一条 `{"trace_id": "FACT:product.price", "trace_type": "MODEL_JUDGMENT"}`
         能同时躲过池成员判定（ID 确实在池里）和四类分离检查——读产物的人按 ID 前缀认它是事实，
         而它其实是模型判断，这正是 A:72 点名要防的伪装。

    诚实边界：本项**不查** TraceEntry 自身的 supporting_trace_refs（首批只按规格覆盖
    goal_candidates.supporting_trace_refs）；那部分悬空引用目前无检测器。
    ①只判"引用里带没带版本号"，判不了"引用的版本号是不是规则当前的那一版"——
    池里的 version 与 object_refs 里的 version 是否一致，本项不比对，不得据此宣称版本已核对。
    """
    fact_pool, rule_pool = ctx.get("fact_pool"), ctx.get("rule_pool")
    if not isinstance(fact_pool, list) or not isinstance(rule_pool, list):
        return "UNKNOWN", "ctx.fact_pool / ctx.rule_pool 缺失或不是数组，池成员无从核验"
    fact_ids = {f.get("fact_id") for f in fact_pool if isinstance(f, dict)}
    rule_ids = {r.get("rule_id") for r in rule_pool if isinstance(r, dict)}
    tb = plan.get("trace_bundle")
    entries = tb.get("entries") if isinstance(tb, dict) else None
    if not isinstance(entries, list):
        return "UNKNOWN", "trace_bundle.entries 缺失或不是数组，池成员无从核验"
    offenders, trace_ids = [], set()
    for e in entries:
        if not isinstance(e, dict):
            return "UNKNOWN", "trace_bundle.entries 含非对象条目，池成员无从核验"
        tid, ttype = e.get("trace_id"), e.get("trace_type")
        if isinstance(tid, str):
            trace_ids.add(tid)
        if ttype == "FACT" and tid not in fact_ids:
            offenders.append(f"FACT 条目 {tid!r} 不在事实池（{len(fact_ids)} 项）")
        elif ttype == "RULE":
            if tid not in rule_ids:
                offenders.append(f"RULE 条目 {tid!r} 不在规则池（{len(rule_ids)} 项）")
            else:
                # ① A:68「RULE 必须引用规则版本」
                refs = e.get("object_refs")
                if not isinstance(refs, list) or not refs:
                    offenders.append(
                        f"RULE 条目 {tid!r} 的 object_refs 为空，未引用规则版本（A:68）")
                elif not any(isinstance(r, dict) and r.get("version") is not None for r in refs):
                    offenders.append(
                        f"RULE 条目 {tid!r} 的 object_refs 里没有一条带 version，"
                        "「引用了规则版本」不成立（A:68）")
        # ② A:72 前缀伪装：ID 长得像事实/规则，类型却不是
        if isinstance(tid, str):
            if tid.startswith(_FACT_ID_PREFIX) and ttype != "FACT":
                offenders.append(
                    f"trace_id {tid!r} 用了 {_FACT_ID_PREFIX} 前缀却 trace_type={ttype!r}"
                    "（A:72 ASSUMPTION / MODEL_JUDGMENT 不得伪装为 FACT）")
            if tid in rule_ids and ttype != "RULE":
                offenders.append(
                    f"trace_id {tid!r} 是规则池里的 rule_id 却 trace_type={ttype!r}"
                    "（同 A:72：非规则条目不得占用规则 ID）")
    cands = plan.get("goal_candidates")
    if cands is None:
        cands = []                              # 可选字段，RESOLVED 时通常没有候选
    elif not isinstance(cands, list):
        return "UNKNOWN", "goal_candidates 不是数组，候选支撑引用无从核验"
    for idx, c in enumerate(cands):
        if not isinstance(c, dict):
            return "UNKNOWN", f"goal_candidates[{idx}] 不是对象，候选支撑引用无从核验"
        refs = c.get("supporting_trace_refs") or []
        if not isinstance(refs, list):
            return "UNKNOWN", f"goal_candidates[{idx}].supporting_trace_refs 不是数组，无从核验"
        for r in refs:
            # 合法落点三选一：bundle 内已有的 trace_id / 事实池 / 规则池；都不是即悬空引用
            if r not in trace_ids and r not in fact_ids and r not in rule_ids:
                offenders.append(f"goal_candidates[{idx}].supporting_trace_refs 悬空引用 {r!r}")
    if offenders:
        return "FAIL", "；".join(offenders)[:800]
    return "OK", f"{len(entries)} 条 trace 的 FACT/RULE ID 全部在池内，候选支撑引用无悬空"


def _p7_confidence_ceiling(plan, ctx):
    """P7：goal_resolution ≠ RESOLVED 时 confidence.level 不得 HIGH。

    字段名照 contracts/schemas/common.defs.json 的 ConfidenceStatement（level / basis / limiting_factors），
    不臆造 confidence_level 之类的别名。语义依据：目标都没解析清楚还自称高置信 = 伪确定性表述（北极星1）。
    """
    gr = plan.get("goal_resolution")
    if gr not in ("RESOLVED", "AMBIGUOUS", "NEEDS_INPUT"):
        return "UNKNOWN", f"goal_resolution 缺失或非法（{gr!r}），置信上限无从核验"
    conf = plan.get("confidence")
    if not isinstance(conf, dict) or conf.get("level") not in ("HIGH", "MEDIUM", "LOW"):
        return "UNKNOWN", "confidence.level 缺失或非三级枚举，置信上限无从核验"
    if gr == "RESOLVED":
        return "OK", f"goal_resolution=RESOLVED，本项不设上限（当前 level={conf['level']}）"
    if conf["level"] == "HIGH":
        return "FAIL", f"goal_resolution={gr} 却自报 confidence.level=HIGH（未解析目标不得高置信）"
    return "OK", f"goal_resolution={gr} 且 confidence.level={conf['level']}（未越上限）"


def _p8_forbidden_lexicon(plan, ctx):
    """P8：intent_summary + assumptions 文本过禁用表达词表（只读考卷区词表，绝不写）。

    三态口径与 acceptance/detectors/checks.py::forbidden_expression 对齐（**空词表必须 UNKNOWN**）：
    词表若解析出 0 个词条，hits 必然为空，"清仓甩卖"也会返回 OK——那是词表一漂移检测就整体失效的假绿形态。
    出处：OD-03 二（INVENTORY_ACTIVATION 促销边界含禁用表达；BRAND_AWARENESS 禁用表达清单）；
    词表本体来自 BD-D01 冻结的 forbidden_expression + 衡叙集夹具包·包1。
    诚实边界：B 的 PRE-02 只有 -B/-C（Decision/Creative）两条，**没有 Intent 侧**；本项是 Preflight 提前拦截，
    不替代 PRE-02-B/PRE-02-C；且只扫 intent_summary 与 assumptions 两处文本（规格首批口径），
    goal_candidates.rationale 等其他文本不在本项射程。
    """
    path = ctx.get("lexicon_path") or DEFAULT_LEXICON_PATH
    if not os.path.exists(path):
        return "UNKNOWN", f"词表不存在: {path}——禁用表达无从核验"
    try:
        with open(path, encoding="utf-8") as f:
            lex = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as e:
        return "UNKNOWN", f"词表读取/解析失败: {type(e).__name__}: {e}"
    if not isinstance(lex, dict):
        return "UNKNOWN", f"词表顶层不是映射对象（实得 {type(lex).__name__}），禁用表达无从核验"
    terms, malformed = [], []
    for k, v in lex.items():
        if isinstance(v, list):
            terms.extend(t for t in v if isinstance(t, str) and t.strip())
        else:
            malformed.append(str(k))
    if not terms:
        return "UNKNOWN", (f"词表解析出 0 个词条，禁用表达无从核验"
                           + (f"（结构异常键: {malformed}）" if malformed else ""))
    texts, gaps = [], []
    summary = plan.get("intent_summary")
    if isinstance(summary, str):
        texts.append(summary)
    else:
        gaps.append("intent_summary 缺失或非字符串")
    assumptions = plan.get("assumptions")
    if isinstance(assumptions, list):
        _strings(assumptions, texts)
    else:
        gaps.append("assumptions 不是数组")
    hits = sorted({t for txt in texts for t in terms if t in txt})
    if hits:                                    # 先判命中：即使覆盖面残缺，命中就是硬证据
        return "FAIL", f"命中禁用表达 {hits}（词表 {len(terms)} 词）"
    if gaps:                                    # 没命中但没扫全 → 不能说"零命中"，只能说没核验成
        return "UNKNOWN", f"已扫文本零命中，但覆盖面残缺: {'；'.join(gaps)}"
    if malformed:
        return "UNKNOWN", (f"词表有 {len(malformed)} 个键的值不是列表（{malformed}），这部分词条未参与核验"
                           f"——已核验的 {len(terms)} 词零命中，但覆盖面残缺")
    return "OK", f"词表 {len(terms)} 词，intent_summary + assumptions 零命中"


# 数字抽取：支持千分位与小数（与考卷侧 numeric_grounding 的 _NUM_V2 同形，口径不分叉）
_NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
# 全角数字定点归一（只做数字，不用 NFKC——NFKC 会连带重写兼容汉字，在中文文案里放大误伤面）
_FW_DIGITS = {ord(a): b for a, b in zip("０１２３４５６７８９", "0123456789")}


def _p9_numeric_grounding(plan, ctx):
    """P9：intent_summary 里的阿拉伯数字必须能在 ContextSnapshot 的序列化文本中找到；无数字则 OK。

    出处：北极星1「数字必须溯源到快照」；A.1.2「FACT 来自当前 Context Snapshot，必须引用来源」。
    诚实边界（**必须读到**，别把本项当成考卷侧 numeric_grounding 的等价物）：
      本项是**文本级弱溯源**——只问"这个数字串在快照文本里出现过吗"，不绑定字段路径、不校单位、
      不认中文数字。因此：把 A 款的价格安到 B 款上、把 as_of 日期当价格背书、"3980 件"配"3980 元"，
      本项一律看不见。字段/单位级的绑定判定在 acceptance/detectors/checks.py::numeric_grounding v0.3
      （考卷区，L1），本模块不复制它、也不假装等价——Preflight 全 OK ≠ 数字已被字段级溯源。
    命中口径（ATT-0005 收紧）：**独立数字串**才算命中——命中位置两侧不得紧贴字母或数字，
      否则"7天内"的 7 会借 SKU `1G9971081` 内部的 7 过溯源（修复前实测判 OK，假绿）。
      仍在盲区：千分位串内部借位（快照散文里的 "3,980" 之于摘要 token "3"）等文本级歧义，不假装覆盖。
    找不到即 FAIL 而不是 UNKNOWN：快照在手、数字在手，比对是做得成的，"比对不上"就是实打实的违约证据。
    """
    snap = ctx.get("snapshot")
    if not isinstance(snap, dict):
        return "UNKNOWN", "ctx.snapshot 缺失或不是对象，数字溯源无从核验"
    summary = plan.get("intent_summary")
    if not isinstance(summary, str):
        return "UNKNOWN", "intent_summary 缺失或非字符串，数字溯源无从核验"
    try:
        hay = json.dumps(snap, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as e:
        return "UNKNOWN", f"快照无法序列化，数字溯源无从核验: {type(e).__name__}: {e}"
    tokens = _NUM.findall(summary.translate(_FW_DIGITS))
    if not tokens:
        # 措辞不清场（M1-EP02 修复批次 K4）：首轮写「无阿拉伯数字，无需溯源」，读起来像
        # "这段摘要里没有需要溯源的数字"——而中文数字（"三千九百八"）本项根本扫不到，
        # 它不是"没有数字"，是"本项看不见这种数字"。两者的处置完全不同，不能用同一句话盖过去。
        return "OK", "intent_summary 未发现阿拉伯数字；中文数字不在本项射程（本项看不见，≠ 摘要里没有数字）"
    def _independent_hit(needle):
        # 独立数字串命中（ATT-0005）：两侧不得紧贴字母或数字——"7" 不得借 "1G9971081" 内部的 7。
        return re.search(r"(?<![0-9A-Za-z])" + re.escape(needle) + r"(?![0-9A-Za-z])", hay) is not None

    ungrounded = []
    for t in sorted(set(tokens)):
        # 两种写法都试：原串（"3,980"）与去千分位（"3980"）——快照 JSON 里数值不带千分位，
        # 只归一"待查串"而**不**改造快照文本：把快照里的逗号删掉会让 [1,2] 变成 12，凭空造出可命中的数字（假绿）。
        if _independent_hit(t) or _independent_hit(t.replace(",", "")):
            continue
        ungrounded.append(t)
    if ungrounded:
        return "FAIL", f"这些数字在快照中找不到独立出处: {ungrounded}（文本级独立串比对，快照序列化 {len(hay)} 字符）"
    return "OK", f"{len(set(tokens))} 个数字均有独立出处（文本级独立串命中，非字段级溯源）"


# ============================ 检查表与入口 ============================
# item 文本里内嵌出处（A 行号 / OD-03 章节）——接口规格把 checks 条目键钉死为五个，
# 不另加 source 键，所以出处随 item 一起走，report 落盘后仍能逐条追到合同原文。
_CHECK_TABLE = (
    ("P1", "结构校验：IntentExecutionPlan Schema（内含 A.5.2 约束1/2 条件式）"
           "｜出处 A.5.2 A:540-564 + contracts/schemas/intent_execution_plan.schema.json + B PRE-01-I", _p1_schema),
    ("P2", "A.5.2 约束3（A:565）：CONTINUE_TO_DECISION 需 RESOLVED + business_goal 非空 + 无 BLOCKING 缺失"
           "｜缺失口径 OD-03 四-2（CONFLICTING 视同缺失）", _p2_constraint3),
    ("P3", "A.5.2 约束4（A:566）：QUICK 继续时跨过的缺失必须全为 QUALITY_REDUCING、逐项有 target_paths 绑定的"
           " ASSUMPTION，且 confidence 不得停在 HIGH｜出处 A:393 + OD-03 四-1 + OD-03 三（非阻断项白名单）",
     _p3_constraint4),
    ("P4", "A.5.2 约束5（A:567）：存在 BLOCKING 缺失 → goal_resolution=NEEDS_INPUT；"
           "AMBIGUOUS 且阻断缺失仅 business_goal 时放行（M1-EP02 仲裁1 自洽解，Founder 2026-08-17 已认可，台账 SPEC-DEV-01 行）"
           "｜阻断项清单 OD-03 一（通用四项）+ OD-03 二（分目标追加）", _p4_constraint5),
    ("P5", "A.5.2 约束7（A:569）+ 常量（A:543-544）：task_type=VIDEO_CONTENT_CREATION、platform=WECHAT_VIDEO"
           "｜出处 OD-03 一-4（本期仅视频号，其他平台不得静默适配）", _p5_scope_constants),
    ("P6", "Trace ID 池成员与四类分离：FACT/RULE trace_id 必须来自预物化池、RULE 条目须引用规则版本（A:68）、"
           "trace_id 前缀不得与 trace_type 打架（A:72）、goal_candidates.supporting_trace_refs 不得悬空"
           "｜出处 A.1.2 四类依据分离（A:63-73）+ A.9.2 TraceBundle + A.5.2（A:547-550,558）", _p6_trace_pool),
    ("P7", "置信上限：goal_resolution≠RESOLVED 时 confidence.level 不得 HIGH"
           "｜出处 A.5.2 约束1/2（A:563-564）+ common.defs ConfidenceStatement + OD-03 四-1（降 confidence）", _p7_confidence_ceiling),
    ("P8", "禁用表达词表：intent_summary + assumptions 文本零命中（只读 acceptance/detectors/forbidden_lexicon.yaml）"
           "｜出处 OD-03 二（促销边界/禁用表达清单）+ 词表源 BD-D01 冻结 forbidden_expression", _p8_forbidden_lexicon),
    ("P9", "数字溯源：intent_summary 中的阿拉伯数字须在 ContextSnapshot 序列化文本中出现"
           "｜出处 A.1.2 FACT 必须来自当前 Snapshot（A:63-73）+ 项目宪法北极星1（数字必须溯源到快照）", _p9_numeric_grounding),
)


def preflight(plan, ctx):
    """确定性后校验入口。返回 {"stage","checks":[{id,item,verdict,machine_checkable,detail}],"overall"}。

    verdict 三态、overall 二值（UNKNOWN 归 FAIL 侧，不得吸收成 OK）——理由见模块 docstring。
    调用方（runner）口径：overall != "OK" → exit 1，plan 仍照写盘便于取证。
    """
    ctx = ctx if isinstance(ctx, dict) else {}
    checks = []
    for cid, item, fn in _CHECK_TABLE:
        if not isinstance(plan, dict):
            # plan 根本不是 JSON 对象：九项全部"没核验成"，绝不能因为"没跑出 FAIL"就算过
            verdict, detail = "UNKNOWN", f"plan 不是 JSON 对象（实得 {type(plan).__name__}），本项无从核验"
        else:
            try:
                verdict, detail = fn(plan, ctx)
            except Exception as e:                # noqa: BLE001 —— 检查器自身崩了 = 没核验成
                # 兜底成 UNKNOWN 而不是 FAIL：崩溃说明的是检测器状态，不是 plan 违约；
                # 但因 UNKNOWN 归 FAIL 侧，overall 照样不放行，不存在"崩了就当过"的通道。
                verdict, detail = "UNKNOWN", f"检查器异常（未完成核验，≠通过）: {type(e).__name__}: {e}"
        checks.append({"id": cid, "item": item, "verdict": verdict,
                       "machine_checkable": True, "detail": detail})
    overall = "OK" if all(c["verdict"] == "OK" for c in checks) else "FAIL"
    return {"stage": STAGE, "checks": checks, "overall": overall}
