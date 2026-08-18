#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/intent 资产：编排 CLI（确定性前处理 → 1 步 LLM → 确定性覆盖与硬闸 → Preflight）。

用法：
  python3 -m kernel.intent.runner --snapshot <path> --task "<task_statement>" --mode QUICK|ENHANCED \\
      [--stated-goal <BusinessGoal>] (--live | --replay <fixture>) --out <plan.json> [--report <preflight.json>]

退出码（对齐 tools/validate_schema.py 口径：跑完 ≠ 通过）：
  0 = Preflight 全过；1 = Preflight 判 FAIL（plan 仍写盘，便于取证）；2 = 没跑完（LLM/IO/参数/契约错误，plan 未生成）

本文件的形态红线（C.3 冻结）：Intent = 1 步 LLM + 确定性前后处理。
  模型只负责"目标说清楚了没有、可能是哪几个、给一个最关键的澄清问题"；
  required_context / missing_context 由 preprocess 按 OD-03 算，next_action 与 confidence 由本文件按
  A.5.2 七条约束确定性裁定。**删掉本文件只留 prompt，行为必须显著变差**——否则就退化成 Prompt 套壳。

硬闸顺序（钉死，改顺序 = 改判定语义，须走规格升级）：
  G1 目标裁定（--stated-goal 优先；模型给出冲突目标即反证）
  G2 BLOCKING 闸：模型说 RESOLVED 但存在阻断缺失 → 强制 NEEDS_INPUT（A.5.2 约束5 / A.4.2）；
     模型说 AMBIGUOUS 且阻断缺失里**除 business_goal 之外还有别的** → 同样强制 NEEDS_INPUT（仲裁1）
  G3 A.5.2 约束1/2：非 RESOLVED → business_goal=null + REQUEST_INPUT；AMBIGUOUS 候选不足两个 → 降为 NEEDS_INPUT
  G4 next_action 裁定（A.5.2 约束3：RESOLVED + goal 非空 + 无 BLOCKING 才可 CONTINUE_TO_DECISION）
  G5 QUICK 跨过的 QUALITY_REDUCING 缺失逐项生成 ASSUMPTION（A.5.2 约束4 / A.4.2）
  G6 置信度只降不升（模型自报只作上限输入）

闸决定的留痕（M1-EP02 修复批次 K2，堵「改判只打 stderr、产物里查不到」的取证缺口）：
  G1-G6 每一次改判、每一处目标出处、每一次置信度下调，都会写进产物的
  `confidence.basis`（common.defs ConfidenceStatement 的 string[] 字段，不新增字段）。
  stderr 照旧打印，但 stderr 不落盘——只看 plan.json 的人必须也能读到「这个 NEEDS_INPUT 是模型判的
  还是系统改的」「这个 business_goal 是模型解析的还是 CLI 声明的」。

与同批其它资产的对接约定（接口规格未逐字钉死、按落盘真件对齐，实跑核过）：
  - `trace.build_trace_bundle(...)` 的 assumption_entries / model_judgment_entries 均传 **TraceEntry 形状 dict**
    （assumptions 由本文件按 A.4.2 生成，model_judgments 由本文件从模型输出改名而来）；
  - 同函数在接口规格的五个位置参数之外，要求调用方以关键字给出 `brand_id`（A.1.3 单品牌隔离，组装点不得
    臆造品牌归属），并可给 `target_artifact_ref`——本文件传本次产物的自引用（TraceBundle 指向的是产物，
    不是快照），trace_bundle_id 由 trace.py 按内容确定性派生，本文件**不补写、只核验**；
  - 模型引用了事实池之外的 FACT ID 时，trace.py 直接报错（幻觉引用组装不出合法 Trace）→ 本次运行 exit 2；
    只出现在 goal_candidates.supporting_trace_refs 里的池外 ID 不经过该函数，会走到 postcheck P6 判红 → exit 1。
    两条路径都不在本文件做"删掉了事"的清洗；
  - config.py 的常量名未被接口规格钉死，本文件按候选名取、取不到用本地默认（见 `_from_config`）。
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

import yaml

from . import llm
from . import postcheck
from . import preprocess
from . import trace
# 「目标这一项」的 field_path 字面：硬 import 而不是走下面的 _from_config 探测。
# 理由——G2 的 AMBIGUOUS 分岔（仲裁1）与 postcheck P4 的判据必须**逐字同源**，
# 规格明令「判据用同一字面，不得两套」；探测失败时退回本地默认，恰恰会造出第二套字面。
# 探不到就应该当场报错，而不是安静地用另一个值继续跑。
from .config import BUSINESS_GOAL_FIELD_PATH as GOAL_FIELD_PATH

# 仓库根：kernel/intent/runner.py → parents[2]
REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "intent_v0.4.md"
_DEFAULT_PLAN_SCHEMA_PATH = REPO_ROOT / "contracts" / "schemas" / "intent_execution_plan.schema.json"

# A:204 逐字七枚举（BusinessGoal，A v0.4 判分批新增 DAILY_CONTENT_OPERATION）。落在本文件是为了
# 让 CLI 在 config.py 未就绪时也能自校，且启动时会与 contracts/schemas/intent_execution_plan.schema.json
# 的 enum 实时比对（见 _load_plan_schema）——常量与冻结契约打架时当场报错，不替任何一方拍板。
BUSINESS_GOALS = (
    "DAILY_CONTENT_OPERATION",
    "BRAND_AWARENESS", "PRODUCT_LAUNCH", "CONVERSION",
    "INVENTORY_ACTIVATION", "BRAND_STORY", "CUSTOMER_EDUCATION",
)
EXECUTION_MODES = ("QUICK", "ENHANCED")          # A:203 ExecutionMode
GOAL_RESOLUTIONS = ("RESOLVED", "AMBIGUOUS", "NEEDS_INPUT")
TASK_TYPE = "VIDEO_CONTENT_CREATION"             # A.5.2 常量（Intent 只输出视频号内容任务计划，约束7）
PLATFORM = "WECHAT_VIDEO"                        # A.5.2 常量
ARTIFACT_TYPE = "IntentExecutionPlan"            # A.5.2 输出对象名
# 输出合同版本：intent_execution_plan.schema.json 自身未声明版本号（OQ-INT-D01-05 登记在案），
# 20 份 Manifest 的 output_schema_version 现值为 "v0.1"，此处与之对齐；契约声明版本后改这里。
OUTPUT_SCHEMA_VERSION = "v0.1"
_LEVEL_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
# 缺失项达到该条数即把置信度压到 LOW。阈值来自 M1-EP02 接口规格（A/B 未规定条数），属执行侧口径；
# 改阈值 = 改判定口径，须同步规格，不得在这里随手调。
MISSING_COUNT_LOW_THRESHOLD = 3
# Prompt 文件里界定"冻结对象"的两个标记（沿用 contracts/interaction 基线 Prompt 的写法），不发给模型
PROMPT_BEGIN_MARK = "<<<PROMPT_BEGIN>>>"
PROMPT_END_MARK = "<<<PROMPT_END>>>"


def _from_config(default, *names):
    """优先取 kernel/intent/config.py 的同名常量，取不到用本文件默认值（理由同 llm.py 内同名函数）。"""
    try:
        from . import config
    except ImportError:
        return default
    for name in names:
        value = getattr(config, name, None)
        if value:
            return value
    return default


# ============================ 一、Prompt 渲染（确定性） ============================

def load_prompt(path=None):
    """读 config.PROMPT_INTENT_PATH 指到的 prompt 文件（当前 prompts/intent_v0.2.md），返回 (正文模板, prompt_version)。

    文件头 YAML 用 `---` 包起来；prompt_version 是 module_manifest.py 的取值来源，
    这里同样按它取值并打到 stderr——一次运行用的是哪版 Prompt 必须能从日志里读出来。
    """
    target = Path(path or PROMPT_PATH)
    raw = target.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise RuntimeError(f"Prompt 文件缺少 YAML 文件头：{target}")
    _, front, body = raw.split("---", 2)
    meta = yaml.safe_load(front) or {}
    version = meta.get("prompt_version")
    if not version:
        raise RuntimeError(f"Prompt 文件头缺 prompt_version：{target}")
    if PROMPT_BEGIN_MARK in body:
        body = body.split(PROMPT_BEGIN_MARK, 1)[1]
    if PROMPT_END_MARK in body:
        body = body.split(PROMPT_END_MARK, 1)[0]
    return body.strip(), version


def format_fact_pool(fact_pool):
    """事实池 → Prompt 注入行。每行行首是模型唯一允许引用的 FACT ID。

    **不截断取值**：截断会让模型看见半截事实并据此判断，等于人为制造缺失。
    池为空时也要明说"本次无可引用事实"，否则模型会以为注入失败而自行脑补。
    """
    if not fact_pool:
        return "（本次无可引用事实：事实池为空。缺就是缺，不得据此推断任何取值。）"
    lines = []
    for item in fact_pool:
        value = item.get("value")
        rendered = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        lines.append(f"- {item['fact_id']} | status={item.get('status')} | value={rendered}")
    return "\n".join(lines)


def filter_rule_pool_by_brand(rule_pool, brand_id):
    """SYS-08 / A.1.3 单品牌隔离：只保留 brand_id 与本次快照一致的规则。

    为什么这一步必须在 runner 而不是 preprocess：`load_rule_pool()` 的签名（接口规格钉死）无参，
    拿不到 brand_id，它只能如实返回**全仓所有 ACTIVE 规则**。若 runner 不过滤，别的品牌的硬规则
    就会一路进 prompt 的规则池行、再进 TraceBundle 的 RULE 条目——那是实打实的跨品牌事实泄漏
    （B 侧 SYS-08 的禁止结果），而且因为"规则看起来都很合理"，肉眼极难发现。

    **没有 brand_id 键的规则一律剔除（fail-closed）**，不是保留：
    A.9.1 把 brand_id 列为必填，缺了说明这条 RuleRecord 本身有缺陷；此时"保留"等于让一条
    归属不明的规则参与本品牌的判定，方向上就是放行未知。剔除并 stderr 告警，让缺陷可见。

    返回过滤后的新列表（不原地改入参）。规则池顺序不变——顺序会进 prompt，必须稳定。
    """
    if not isinstance(brand_id, str) or not brand_id.strip():
        # 快照没有 brand_id 就无从隔离。宁可当场停，也不要"没法比对就全放过"。
        raise RuntimeError("快照缺 brand_id，无法执行 SYS-08 单品牌隔离过滤（不得在无法比对时放行全部规则）")
    kept, cross_brand, unlabeled = [], [], []
    for rule in rule_pool:
        if "brand_id" not in rule:
            unlabeled.append(rule.get("rule_id"))
            continue
        if rule.get("brand_id") != brand_id:
            cross_brand.append("%s(brand_id=%r)" % (rule.get("rule_id"), rule.get("brand_id")))
            continue
        kept.append(rule)
    if cross_brand:
        print("[intent.runner] SYS-08 单品牌隔离：剔除非本品牌规则 %s（本次 brand_id=%s）"
              % ("、".join(cross_brand), brand_id), file=sys.stderr)
    if unlabeled:
        print("[intent.runner] SYS-08 单品牌隔离：剔除无 brand_id 键的规则 %s"
              "（A.9.1 必填；归属不明一律 fail-closed 剔除，不得放行）"
              % ("、".join(str(r) for r in unlabeled)), file=sys.stderr)
    return kept


def format_rule_pool(rule_pool):
    """硬规则池 → Prompt 注入行（rule_id 为 contracts/rules/*.yaml 的原值，不改写）。"""
    if not rule_pool:
        return "（本次无适用硬规则。无规则 ≠ 可以随便写：禁止虚构一条仍然成立。）"
    lines = []
    for rule in rule_pool:
        lines.append(
            f"- {rule.get('rule_id')} | scope={rule.get('scope')} | effect={rule.get('effect')}"
            f" | target_path={rule.get('target_path')} | {rule.get('statement')}"
        )
    return "\n".join(lines)


def render_prompt(template, task_statement, execution_mode, stated_goal, fact_pool, rule_pool):
    """逐字替换占位符（不改写、不摘要、不补写——对齐 contracts/interaction 的替换纪律）。"""
    stated_text = (
        f"用户已显式声明商业目标：{stated_goal}。"
        "注意：显式声明只是输入，不自动等于已解析（A.4.1「用户陈述不自动等同于已解析商业目标」）；"
        "若你在任务原话里看到与之冲突的目标，照实说出来。"
        if stated_goal else
        "用户**没有**显式声明商业目标。只能从任务原话本身判断；判断不出来就承认判断不出来。"
    )
    rendered = template
    for placeholder, value in (
        ("{{TASK_STATEMENT}}", task_statement),
        ("{{EXECUTION_MODE}}", execution_mode),
        ("{{STATED_BUSINESS_GOAL}}", stated_text),
        ("{{BUSINESS_GOAL_ENUM}}", "\n".join(f"- {g}" for g in BUSINESS_GOALS)),
        ("{{FACT_POOL}}", format_fact_pool(fact_pool)),
        ("{{RULE_POOL}}", format_rule_pool(rule_pool)),
    ):
        rendered = rendered.replace(placeholder, value)
    if "{{" in rendered:
        # 漏替换的占位符会被原样发给模型（模型会看见 "{{XXX}}" 并自行发挥）——当场拦，不放行
        raise RuntimeError(f"Prompt 仍有未替换占位符：{rendered[rendered.index('{{'):][:60]}")
    return rendered


# ============================ 二、模型输出 → 确定性覆盖 ============================

def normalize_candidates(model_out):
    """模型候选 → A.5.2 v0.4 goal_candidates 形状（goal / rationale / focus / tradeoffs /
    expected_outcome / supporting_trace_refs）。

    只做三件确定性的事：丢弃不在枚举里的 goal（枚举外就不是合法候选）、字段改名、按 goal 去重
    （同一个目标写两遍不构成"两个候选"）。
    **绝不补候选、绝不补三要素**：凑不够两个就让约束1 走不通，由 G3 降级成 NEEDS_INPUT——凑候选
    就是在编目标；三要素缺就让它空着，交给 Schema 与 P 闸判红（A v0.4：光秃标签选择题=INT_TASK_ESCALATED），
    替模型补一句"侧重点"同样是编。
    supporting_trace_refs 逐字保留模型给的 ID（含池外 ID），删掉就等于把幻觉引用擦干净，postcheck P6 再也看不见。
    """
    seen, candidates = set(), []
    for raw in model_out.get("goal_candidates") or []:
        if not isinstance(raw, dict):
            continue
        goal = raw.get("goal")
        if goal not in BUSINESS_GOALS or goal in seen:
            continue
        seen.add(goal)
        candidates.append({
            "goal": goal,
            "rationale": str(raw.get("rationale") or ""),
            "focus": str(raw.get("focus") or ""),
            "tradeoffs": str(raw.get("tradeoffs") or ""),
            "expected_outcome": str(raw.get("expected_outcome") or ""),
            "supporting_trace_refs": list(raw.get("referenced_fact_ids") or []),
        })
    return candidates


def resolve_goal(model_out, stated_goal):
    """G1 目标裁定。返回 (goal_resolution, business_goal, notes)。

    --stated-goal 的口径：接口规格要求"作为已声明目标直接用、强制 RESOLVED，除非模型给出反证"；
    A.4.1 同时写着"用户陈述不自动等同于已解析商业目标"。两句话在本实现里的合成口径是——
    声明的目标**直接采用**，但仍要过 G2 阻断闸、且模型给出冲突目标即视为反证（降为 NEEDS_INPUT，
    不在两个目标之间替人挑一个）。"不自动等同"因此落在"仍须过全部确定性闸 + 在 confidence 里如实登记"上，
    而不是"声明了也不算"。
    """
    notes = []
    model_resolution = model_out.get("goal_resolution")
    if model_resolution not in GOAL_RESOLUTIONS:
        notes.append(
            f"系统改判：模型 goal_resolution={model_resolution!r} 不在三枚举内，按最保守方向改为 NEEDS_INPUT"
        )
        model_resolution = "NEEDS_INPUT"
    model_goal = model_out.get("business_goal")
    if model_goal not in BUSINESS_GOALS:
        model_goal = None

    if stated_goal:
        if model_goal and model_goal != stated_goal:
            notes.append(
                f"系统改判：用户声明 {stated_goal}，模型判为 {model_goal}——两者冲突（A.4.1 反证），"
                "不替人二选一，改为 NEEDS_INPUT"
            )
            return "NEEDS_INPUT", None, notes
        notes.append(
            f"business_goal 来源：--stated-goal CLI 声明（{stated_goal}）"
            "；A.4.1「用户陈述不自动等同于已解析商业目标」落在「仍须过全部确定性闸」上"
        )
        return "RESOLVED", stated_goal, notes

    if model_resolution == "RESOLVED" and model_goal is None:
        notes.append(
            "系统改判：模型自称 RESOLVED 却没给出六枚举之一的 business_goal——不代它挑一个，改为 NEEDS_INPUT"
        )
        return "NEEDS_INPUT", None, notes
    if model_resolution != "RESOLVED":
        notes.append(f"business_goal 来源：模型解析结果 goal_resolution={model_resolution}（目标未落到六选一）")
        return model_resolution, None, notes
    notes.append(f"business_goal 来源：模型解析结果（{model_goal}），未使用 --stated-goal")
    return "RESOLVED", model_goal, notes


def apply_hard_gates(goal_resolution, business_goal, candidates, missing, execution_mode):
    """G2-G4：把 A.5.2 约束 1/2/3/5 写成代码，模型说什么都拦得住。返回状态 dict。"""
    notes = []
    blocking = [m for m in missing if m.get("impact") == "BLOCKING"]

    # ---- G2 BLOCKING 闸（A.5.2 约束5 / A.4.2「BLOCKING 缺失在任何模式都进入 NEEDS_INPUT」）----
    # 分两支，口径与 postcheck._p4_constraint5 逐条对齐（M1-EP02 修复批次仲裁1，证据链写在 P4 注释里）：
    #   ① 模型判 RESOLVED + 任意阻断缺失 → 改判 NEEDS_INPUT。模型说材料够了而实际不够，一律拦。
    #   ② 模型判 AMBIGUOUS + 阻断缺失里**除 business_goal 之外还有别的** → 同样改判 NEEDS_INPUT。
    #      AMBIGUOUS 这个标签只承载「目标未明」这一件事（仲裁1）；它不是"什么都缺也照样挂着候选"的通行证。
    #      商品没选、品牌不明这类缺失与目标解析无关，挂着两个候选让人挑目标解决不了它们，必须直接要人补输入。
    #   ③ 模型判 AMBIGUOUS 且阻断缺失 ⊆ {business_goal}（含空集）→ **不改判**，保留 AMBIGUOUS。
    #      依据 B:285-286「用户明确选择快速模式时…但必须保留 AMBIGUOUS、missing_context、assumptions
    #      和非高置信度」——INT-D01 正是这一格。改判会抹掉候选与澄清问题，把 B 那句写成死条文。
    if blocking and goal_resolution == "RESOLVED":
        notes.append(
            "系统改判：模型判 RESOLVED，存在阻断缺失 "
            + "、".join(m["field_path"] for m in blocking)
            + "，改为 NEEDS_INPUT（A.5.2 约束5 / A.4.2）"
        )
        goal_resolution, business_goal = "NEEDS_INPUT", None
    elif blocking and goal_resolution == "AMBIGUOUS":
        non_goal_blocking = [m for m in blocking if m.get("field_path") != GOAL_FIELD_PATH]
        if non_goal_blocking:
            notes.append(
                "系统改判：模型判 AMBIGUOUS，存在非 %s 的阻断缺失 %s，改为 NEEDS_INPUT"
                "（AMBIGUOUS 只承载「目标未明」，不覆盖其它阻断缺失——M1-EP02 仲裁1）"
                % (GOAL_FIELD_PATH, "、".join(m["field_path"] for m in non_goal_blocking))
            )
            goal_resolution, business_goal = "NEEDS_INPUT", None

    # ---- G3 约束1/2：非 RESOLVED 一律清空目标并要人补输入 ----
    if goal_resolution == "AMBIGUOUS" and len(candidates) < 2:
        # 约束1 要求候选至少两个。凑不出来时**降级**（NEEDS_INPUT 不要求候选），绝不编第二个候选。
        notes.append(
            f"系统改判：模型判 AMBIGUOUS 但合法候选不足两个（实得 {len(candidates)} 个），"
            "改为 NEEDS_INPUT，不补候选（A.5.2 约束1）"
        )
        goal_resolution = "NEEDS_INPUT"
    if goal_resolution != "RESOLVED":
        business_goal = None
        next_action = "REQUEST_INPUT"
    else:
        # ---- G4 约束3：只有 RESOLVED + goal 非空 + 无 BLOCKING 才可能继续 ----
        if blocking:
            # 走不到这里（G2 已改判），留作显式防线：约束3 是"必要条件"，任何路径都不得绕过
            next_action = "REQUEST_INPUT"
        elif execution_mode == "QUICK":
            next_action = "CONTINUE_TO_DECISION"
        else:
            # ENHANCED（B v0.6 / OD-03 v1.1，Founder 2026-08-18 判分批标准③⑤）：可选信息不作
            # 执行前障碍——非阻断缺失不再触发追问（v1「有缺失就先问」的保守侧被判分批明确判死：
            # 把可执行任务解释成缺条件无法继续＝INT_TASK_ESCALATED）。「高价值追问」的判定是语义
            # 判断，确定性层不猜，取「零个追问」默认；诚实面不降：跨过的缺失照样逐项 ASSUMPTION
            # + 降置信（G5/G6），且交付后提示补充。
            next_action = "CONTINUE_TO_DECISION"
            if missing:
                notes.append("增强模式（B v0.6）：剩余缺失均为非阻断可选信息（%d 项），不作执行前障碍，"
                             "逐项留假设并降置信，交付后提示补充" % len(missing))

    # 候选只在 AMBIGUOUS 下保留：目标已解析还挂着候选，会诱导下游把候选当"可选方案"接着跑
    # （B.4.1 INT-D01 禁止结果：以"已给出两个目标候选"为由设置 CONTINUE_TO_DECISION）。
    kept_candidates = candidates if goal_resolution == "AMBIGUOUS" else []
    return {
        "goal_resolution": goal_resolution,
        "business_goal": business_goal,
        "goal_candidates": kept_candidates,
        "next_action": next_action,
        "blocking": blocking,
        "gate_notes": notes,
    }


def build_assumption_entries(missing, execution_mode, next_action):
    """G5：继续执行时跨过的每一项 QUALITY_REDUCING 缺失 → 一条 ASSUMPTION（A.4.2 / A.5.2 约束4）。

    v2（判分批）：不再限 QUICK——增强模式在 B v0.6 下同样会跨过非阻断缺失继续（可选信息不作
    执行前障碍），跨过就必须留假设，两种模式同一诚实口径。
    statement 里**不写任何替代取值**：假设的内容是"在缺这项的情况下继续"，不是"这项大概是 X"——
    后者就是 B.4.1 INT-D02 禁止结果里的编造。
    """
    if next_action != "CONTINUE_TO_DECISION":
        return []
    entries = []
    for item in missing:
        if item.get("impact") != "QUALITY_REDUCING":
            continue                      # 阻断项不可能走到这里（G2 已拦），保留判断作为第二道防线
        field_path = item.get("field_path")
        mode_word = "快速" if execution_mode == "QUICK" else "增强"
        entries.append({
            "trace_id": f"ASSUMPTION:{field_path}",
            "trace_type": "ASSUMPTION",
            "statement": (
                f"缺少「{field_path}」（用途：{item.get('purpose')}）。{mode_word}模式下跨过该缺失继续，"
                "本次不对其取值做任何假定，也不得据此写出确定表述；补齐后须重新运行 Intent。"
            ),
            "target_paths": [field_path] if field_path else [],
            "confidence": None,           # 无检测器可判这条假设的可信度，留 null；硬写档位就是假绿
        })
    return entries


def build_model_judgment_entries(model_out):
    """模型判断 → MODEL_JUDGMENT TraceEntry。引用 ID 逐字保留（含池外 ID，交给 postcheck P6 判）。"""
    entries = []
    for index, raw in enumerate(model_out.get("model_judgments") or [], start=1):
        if not isinstance(raw, dict) or not raw.get("text"):
            continue
        entries.append({
            "trace_id": f"MODEL_JUDGMENT:MJ-{index}",
            "trace_type": "MODEL_JUDGMENT",
            "statement": str(raw["text"]),
            "supporting_trace_refs": list(raw.get("referenced_fact_ids") or []),
        })
    return entries


def cap_confidence(model_level, state, missing, out_of_pool_refs):
    """G6：置信度只降不升。返回 (level, limiting_factors, notes)。

    模型自报只是**上限的输入之一**：最终档位 = min(模型自报, 各条确定性上限)。
    这样"模型说 HIGH"永远不能把系统抬上去（B.4.1 INT-D01 禁止结果：关键目标未知时给 HIGH confidence）。

    第三个返回值 notes 是**下调留痕**（M1-EP02 修复批次 K2）：格式
    「模型自报 confidence=HIGH，按缺失规则下调为 LOW」。它会进 confidence.basis——
    只有 limiting_factors 的话，读产物的人看到的是"为什么档位低"，看不到"模型原本报的是几档"，
    也就无从判断 G6 到底动没动过。没有下调时不发这条（不制造"看起来做了什么"的噪音）。
    """
    limiting, notes = [], []
    level = model_level if model_level in _LEVEL_ORDER else "LOW"
    if model_level not in _LEVEL_ORDER:
        limiting.append(f"模型自报置信度 {model_level!r} 不是三级枚举，按最低档处理")

    caps = []
    if state["goal_resolution"] != "RESOLVED":
        caps.append(("LOW", "商业目标尚未解析为六选一，任何结论都建立在未定目标上"))
    if missing:
        # 比接口规格更保守的一处：规格只说 QUICK 跨过时降档，这里对两种模式都降。
        # 理由：增强模式同样可能带着缺失出计划，"有缺失却 HIGH"正是 INT_CONFIDENCE_OVERSTATED。
        # 方向仍是只降不升，故取保守侧。
        caps.append(("MEDIUM", "存在缺失上下文项，输出质量受限"))
    if len(missing) >= MISSING_COUNT_LOW_THRESHOLD:
        caps.append(("LOW", "缺失上下文项达到降档阈值"))
    if out_of_pool_refs:
        caps.append(("LOW", "模型引用了事实池之外的 ID：" + "、".join(sorted(out_of_pool_refs))))
    for cap_level, reason in caps:
        if _LEVEL_ORDER[cap_level] < _LEVEL_ORDER[level]:
            level = cap_level
        limiting.append(reason)
    if model_level in _LEVEL_ORDER and _LEVEL_ORDER[level] < _LEVEL_ORDER[model_level]:
        notes.append(f"模型自报 confidence={model_level}，按缺失规则下调为 {level}（G6 只降不升）")
    return level, limiting, notes


def apply_clarification_question(missing, model_out, state):
    """把模型给出的澄清问题落到 missing_context 里 business_goal 那一项的 resolution_question 上。

    出处：B:285-286 允许 INT-D01 保留 AMBIGUOUS，B 的允许答案族第一条是「提出一个最关键澄清问题」。
    这个问题必须有落点——A.4.2 里唯一承载"要问什么"的字段就是 ContextRequirement.resolution_question。
    不落进去的话，模型精心提的那句问题只留在模型原始回复里（那份不进产物），产物里剩下的是
    preprocess 的模板句「这条视频想达成什么？六选一：…」。模板句不是错的，但它不针对这次任务；
    模型定制问题优先，正是为了减少 Founder 的认知负担（北极星②）。

    只在 AMBIGUOUS 下替换：其它状态下模型按 Prompt 契约本就该给 null，若给了也不采纳
    （RESOLVED 还问"你到底要什么"是自相矛盾的产物）。

    **原地改 missing 里的那个 dict**——它与 required_context 里的同一条是同一个对象（见
    preprocess.resolve_requirements 文档串"共享同一批 dict 对象"），所以两处会同步变，
    不会出现"required 里问模板句、missing 里问定制句"的自相矛盾。
    返回一条留痕字符串（无替换发生时返回 None）。
    """
    if state["goal_resolution"] != "AMBIGUOUS":
        return None
    question = model_out.get("clarification_question")
    if not isinstance(question, str) or not question.strip():
        return None
    for item in missing:
        if item.get("field_path") != GOAL_FIELD_PATH:
            continue
        template = item.get("resolution_question")
        item["resolution_question"] = question.strip()
        return (
            "clarification_question 落点：AMBIGUOUS，已用模型给出的澄清问题替换 %s 项的模板问句"
            "（B:285-286「提出一个最关键澄清问题」；被替换的模板句：%r）" % (GOAL_FIELD_PATH, template)
        )
    return None


def build_confidence(level, limiting_factors, model_out, state, missing, gate_notes=()):
    """组装 ConfidenceStatement（common.defs：level / basis / limiting_factors 三字段，不加字段）。

    basis 的第一段是 **G1-G6 的闸决定留痕**（M1-EP02 修复批次 K2）：每一次系统改判、
    business_goal 的出处、置信度下调、澄清问题替换，逐条进这里。
    为什么放 basis 而不是新开一个字段：common.defs 的 ConfidenceStatement 只有三个字段，
    加第四个就是私自扩冻结合同；而 basis 的语义（"这个档位是凭什么给的"）本来就该包含
    "系统在这次运行里做了哪些确定性裁定"。前缀「闸留痕：」让它与模型自述、确定性核对分得开。
    """
    basis = [f"闸留痕：{note}" for note in gate_notes]
    reason = model_out.get("confidence_reason")
    if isinstance(reason, str) and reason.strip():
        basis.append(f"模型自述：{reason.strip()}")
    basis.append(f"确定性核对：goal_resolution={state['goal_resolution']}，next_action={state['next_action']}")
    basis.append("required_context / missing_context 由 OD-03 冻结清单逐项算出，非模型判断")
    factors = list(limiting_factors)
    for item in missing:
        question = item.get("resolution_question") or item.get("purpose")
        factors.append(f"缺 {item.get('field_path')}（{item.get('impact')}）：{question}")
    return {"level": level, "basis": basis, "limiting_factors": factors}


# ============================ 三、Artifact 组装 ============================

def build_artifact_envelope(snapshot, run_id, created_at):
    """按 common.defs.ArtifactEnvelope 逐字段组装（照抄形状，不臆造字段）。"""
    brand_id = snapshot.get("brand_id")
    snapshot_id = snapshot.get("snapshot_id")
    if not brand_id or not snapshot_id:
        # 没有 brand_id 就组不出合法 Artifact（SYS-08 单品牌隔离）；宁可不出，也不填占位品牌
        raise RuntimeError("快照缺 brand_id 或 snapshot_id，无法组装 ArtifactEnvelope")
    return {
        "artifact_id": f"IEP-{run_id}",
        "artifact_type": ARTIFACT_TYPE,
        "version": 1,                              # 本次运行产出的第一版；返工重跑另起版本由上层版本机制负责（A.1.5 不可覆盖）
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "brand_id": brand_id,
        # Task 对象层（A.4.1）尚未落盘，runner 只拿到 task_statement 字符串；此处按运行号派生占位 task_id，
        # 待 Task 层就绪后由调用方传入（待集成）。不编一个看起来像真 task_id 的值。
        "task_id": f"TASK-{run_id}",
        "context_snapshot_ref": {
            "object_type": "ContextSnapshot",
            "object_id": snapshot_id,
            # M0 扁平夹具没有 version 字段（A.4.3 形状尚未落地），缺省取 1 并在此写明来源，不静默当作"已知版本"
            "version": int(snapshot.get("version", 1)),
            "brand_id": brand_id,
        },
        "source_run_id": run_id,
        "parent_references": [],                   # Intent 是链条起点，没有父 Artifact
        "review_status": "PENDING",                # 系统产出一律待人工复核（PASS 只能由人判，C.5）
        "created_at": created_at,
        "created_by": "SYSTEM",
    }


def artifact_self_ref(artifact):
    """本次产出 Artifact 自身的 VersionedRef（TraceBundle.target_artifact_ref 指向的是**产物**，不是快照）。"""
    return {
        "object_type": ARTIFACT_TYPE,
        "object_id": artifact["artifact_id"],
        "version": artifact["version"],
        "brand_id": artifact["brand_id"],
    }


def check_trace_bundle(bundle):
    """只核验、不补写：TraceBundle 三个必填键必须由 trace.py 给全（common.defs.TraceBundle）。

    为什么不在这里"缺什么补什么"：trace.py 已经拿到 brand_id 并按内容确定性派生 bundle_id，
    runner 再补一份等于同一字段两个来源；真缺了就是组装出了不合规产物，应当当场失败而不是被 runner 掩盖。
    """
    if not isinstance(bundle, dict):
        raise RuntimeError(f"build_trace_bundle 返回了 {type(bundle).__name__}，期望 dict")
    missing_keys = [k for k in ("trace_bundle_id", "brand_id", "entries") if not bundle.get(k) and bundle.get(k) != []]
    if missing_keys:
        raise RuntimeError(f"TraceBundle 缺必填键 {missing_keys}（common.defs.TraceBundle），不在 runner 侧补写")
    return bundle


def assemble_plan(artifact, state, model_out, required, missing, assumptions, confidence, bundle):
    """按 A.5.2 字段顺序组装 IntentExecutionPlan（字段名逐字照抄，不增不减）。"""
    return {
        "artifact": artifact,
        "task_type": TASK_TYPE,
        "platform": PLATFORM,
        "goal_resolution": state["goal_resolution"],
        "business_goal": state["business_goal"],
        "goal_candidates": state["goal_candidates"],
        # intent_summary 逐字取模型原文：**不做词表/数字清洗**——清洗等于把违规擦干净，
        # 该由 postcheck P8（词表）/ P9（数字溯源）当场判红。
        "intent_summary": str(model_out.get("intent_summary") or ""),
        # 受众引用需要 VersionedRef，M0 扁平夹具里没有带版本的受众对象（事实层 M1-EP01 在建）——
        # 留空数组，不用 snapshot 里的自由文本硬凑一个 ref（待集成）。
        "target_audience_refs": [],
        "required_context": required,
        "missing_context": missing,
        "assumptions": assumptions,
        "confidence": confidence,
        "next_action": state["next_action"],
        "trace_bundle": bundle,
    }


# ============================ 四、CLI ============================

def _load_plan_schema(schema_path):
    """读输出契约，并把本文件的六枚举与契约里的 enum 实时比对（常量漂移当场报错，不替谁拍板）。"""
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    contract_goals = [g for g in schema["properties"]["business_goal"]["enum"] if g is not None]
    if sorted(contract_goals) != sorted(BUSINESS_GOALS):
        raise RuntimeError(
            f"BusinessGoal 六枚举与冻结契约不一致：代码 {sorted(BUSINESS_GOALS)} vs 契约 {sorted(contract_goals)}"
        )
    return schema


def parse_args(argv=None):
    # 说明文本里**不得出现** PREFLIGHT_OK / PREFLIGHT_FAIL 这两个结论标记串
    # （tools/validate_schema.py 踩过的坑：--help 也会把它打出来，按标记子串判绿的调用方会被骗过）
    parser = argparse.ArgumentParser(
        prog="python3 -m kernel.intent.runner",
        description="Intent 模块编排：确定性前处理 → 1 步 LLM → 确定性覆盖与硬闸 → Preflight。退出码 0=全过 / 1=后校验判失败 / 2=没跑完",
    )
    parser.add_argument("--snapshot", required=True, help="Context Snapshot JSON 路径")
    parser.add_argument("--task", required=True, help="业务任务原话（task_statement），逐字传入")
    parser.add_argument("--mode", required=True, choices=EXECUTION_MODES, help="执行模式")
    parser.add_argument("--stated-goal", choices=BUSINESS_GOALS, default=None, help="用户已显式声明的商业目标")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--live", action="store_true", help="调用 DashScope（key 只取环境变量 DASHSCOPE_API_KEY，零重试）")
    source.add_argument("--replay", metavar="FIXTURE", help="离线：读一份录制/手写的模型原始回复")
    parser.add_argument("--out", required=True, help="IntentExecutionPlan 输出路径")
    parser.add_argument("--report", default=None, help="Preflight 报告输出路径（不给则只打摘要）")
    return parser.parse_args(argv)


def run(args):
    """一次完整编排。返回 (plan, report)；异常一律向上抛（由 main 归到退出码 2）。"""
    schema_path = str(_from_config(_DEFAULT_PLAN_SCHEMA_PATH, "INTENT_PLAN_SCHEMA_PATH", "INTENT_EXECUTION_PLAN_SCHEMA"))
    _load_plan_schema(schema_path)                       # 启动即比对六枚举，别等组装完才发现契约对不上

    # --- 前处理（确定性）---
    snapshot = preprocess.load_snapshot(args.snapshot)
    fact_pool = preprocess.materialize_fact_pool(snapshot)
    # 规则池按本次快照的 brand_id 过滤（SYS-08 单品牌隔离）。过滤发生在**进 prompt 之前**：
    # 过滤晚一步，别的品牌的规则就已经被模型读过了，产物里删干净也没用。
    rule_pool = filter_rule_pool_by_brand(preprocess.load_rule_pool(), snapshot.get("brand_id"))

    # --- 1 步 LLM ---
    template, prompt_version = load_prompt()
    prompt_text = render_prompt(template, args.task, args.mode, args.stated_goal, fact_pool, rule_pool)
    mode = "live" if args.live else f"replay:{args.replay}"
    print(f"[intent.runner] prompt_version={prompt_version} mode={args.mode} llm_mode={mode.split(':')[0]}", file=sys.stderr)
    raw_reply = llm.call_llm(prompt_text, mode)
    _persist_raw_reply(args.out, raw_reply)
    model_out = llm.parse_model_json(raw_reply)

    # --- 确定性覆盖 + 硬闸 ---
    goal_resolution, business_goal, goal_notes = resolve_goal(model_out, args.stated_goal)
    # resolver 拿到的 goal 是**闸前**的目标：目标解析出来了就按该目标算分目标追加项，
    # 这样"因为这个目标才缺这几项"才有证据；G2 事后改判 NEEDS_INPUT 时**不重算**——
    # 重算成通用四项会把"到底为什么被拦"的那几条缺失抹掉。
    required, missing = preprocess.resolve_requirements(business_goal, snapshot, args.task)
    state = apply_hard_gates(goal_resolution, business_goal, normalize_candidates(model_out), missing, args.mode)
    state["gate_notes"] = goal_notes + state["gate_notes"]

    # 澄清问题落点：必须在硬闸之后（要先知道最终是不是 AMBIGUOUS），且在组装 plan 之前
    # （它改的是 missing/required 里同一个 dict 的 resolution_question）。
    clarification_note = apply_clarification_question(missing, model_out, state)
    if clarification_note:
        state["gate_notes"].append(clarification_note)

    assumptions = build_assumption_entries(missing, args.mode, state["next_action"])
    model_judgments = build_model_judgment_entries(model_out)

    # 池外引用不在这层丢弃（丢了 postcheck P6 就看不见幻觉引用），只用来压置信度并如实登记
    referenced_fact_ids = list(model_out.get("referenced_fact_ids") or [])
    checked_ids = referenced_fact_ids + [r for c in state["goal_candidates"] for r in c["supporting_trace_refs"]]
    out_of_pool = set(trace.assert_ids_in_pool(checked_ids, fact_pool))

    level, limiting, conf_notes = cap_confidence(model_out.get("confidence_level"), state, missing, out_of_pool)
    state["gate_notes"] += conf_notes
    # stderr 打印挪到全部闸跑完之后：留痕清单与产物 confidence.basis 里的那一份必须是同一份，
    # 否则日志与产物会各说各话（先打印一半再追加，正是这种分叉的来源）。
    for note in state["gate_notes"]:
        print(f"[intent.runner] 闸: {note}", file=sys.stderr)
    confidence = build_confidence(level, limiting, model_out, state, missing, state["gate_notes"])

    run_id = "RUN-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    artifact = build_artifact_envelope(snapshot, run_id, created_at)
    # brand_id / target_artifact_ref 走关键字入参：trace.py 在接口规格的五个位置参数之外要求由调用方给出
    # brand_id（A.1.3 单品牌隔离，组装点不得臆造品牌归属），并按内容确定性派生 trace_bundle_id。
    # 池外 FACT 引用由 trace.py 直接报错（幻觉引用 = 组装不出合法 Trace），本层不兜、不删、不改写。
    bundle = check_trace_bundle(trace.build_trace_bundle(
        fact_pool, rule_pool, referenced_fact_ids, assumptions, model_judgments,
        brand_id=artifact["brand_id"], target_artifact_ref=artifact_self_ref(artifact),
    ))

    plan = assemble_plan(artifact, state, model_out, required, missing, assumptions, confidence, bundle)

    # --- 确定性后校验（Preflight）---
    report = postcheck.preflight(plan, {
        "schema_path": schema_path,
        "fact_pool": fact_pool,
        "rule_pool": rule_pool,
        "snapshot": snapshot,
        "execution_mode": args.mode,
    })
    return plan, report


def _write_json(path, payload):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _persist_raw_reply(out_path, raw_text):
    """模型原始回复落盘（<out>.raw.txt）：在解析之前写、无论后续成败都留。

    零重试纪律（B.2.4）下失败 run 的唯一一手证据就是原始回复；ATT-0004 的失败 run
    （TraceAssemblyError 早于任何写盘）事后连模型说了什么都无从取证，此处即堵该观测缺口。
    """
    target = Path(str(out_path) + ".raw.txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(raw_text if raw_text.endswith("\n") else raw_text + "\n", encoding="utf-8")
    print(f"[intent.runner] 原始回复已落盘：{target}", file=sys.stderr)


def main(argv=None):
    args = parse_args(argv)
    try:
        plan, report = run(args)
    except Exception as e:                       # 没跑完 ≠ 通过：exit 2，且不产出半成品 plan（A.5 降级纪律）
        print(f"[intent.runner] 运行失败（{type(e).__name__}）：{e}", file=sys.stderr)
        return 2
    _write_json(args.out, plan)                  # 判红也照写盘：失败的 plan 是取证材料
    if args.report:
        _write_json(args.report, report)
    failed = [c for c in report.get("checks", []) if c.get("verdict") == "FAIL"]
    unknown = [c for c in report.get("checks", []) if c.get("verdict") == "UNKNOWN"]
    print(
        f"goal_resolution={plan['goal_resolution']} business_goal={plan['business_goal']} "
        f"next_action={plan['next_action']} confidence={plan['confidence']['level']} "
        f"missing={len(plan['missing_context'])} assumptions={len(plan['assumptions'])}"
    )
    for check in failed + unknown:
        print(f"  {check.get('verdict')} {check.get('id')} {check.get('item')}: {check.get('detail')}")
    # 结论标记串只出现在这一行真实结论里（同 tools/validate_schema.py 的纪律）
    print("PREFLIGHT_OK" if report.get("overall") == "OK" else "PREFLIGHT_FAIL")
    return 0 if report.get("overall") == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
