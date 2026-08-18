#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 离线自测：纯 replay、零网络、零写考卷区。

【M2-EP01 提前段·非正式证据】

它**不是**什么（诚实边界，别把 GREEN 当合规图章）：
  · 不是 B 的验收判分——B 的 PASS 只能由 L3 人工判（C.5）；本测试全部属 L1 考生自查；
  · 不是真实模型行为的证据——模型回复全部是手写夹具（fixtures/README.md）；
    live 真实调用未执行，llm 层只在协议面被回放覆盖 = 结构层达标（协作契约第 4 条口径）；
  · 不是 IA-2 取证——IA-1 未 PASS，闸门按序关闭（D §十一），本测试绿不改变任何 Gate 状态。

组织方式（与 kernel/intent/test_intent_offline.py 同源）：
  独立脚本非 pytest；`python3 kernel/decision/test_decision_offline.py` 不接受任何参数
  （改口径 = 改本文件，不设放宽开关）。in-process 调 runner.main(argv) 不起子进程——
  子进程有自己的解释器，零网络桩打不进去。
  正向对照组存在的理由：正向断言全是"跑通 + 全 OK"，把某个检查项掏空成永远返回 OK，
  全部正向断言反而更容易通过；对照组反向喂坏产物，断言指定项必 FAIL，且**先核验改坏之前
  该项是 OK**——若该项本来就一直 FAIL，断言 FAIL 也会通过，什么都没证明。
"""

import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)

from kernel.decision import config, module_manifest, postcheck, preprocess, rules_engine, runner, trace  # noqa: E402

FIXTURES = config.FIXTURES_DIR
BD_CASE_DIR = os.path.join(REPO_ROOT, "acceptance", "cases", "BD-D01", "fixtures")
FROZEN_PLAN = os.path.join(BD_CASE_DIR, "intent_execution_plan.frozen.json")
SNAPSHOT = os.path.join(BD_CASE_DIR, "context_snapshot.json")

# 考卷区只读见证：跑前跑后 sha256 必须一致（G2）
READONLY_WITNESSES = [
    FROZEN_PLAN,
    SNAPSHOT,
    config.FORBIDDEN_LEXICON_PATH,
    os.path.join(config.RULES_DIR, "R-BDD01-001.yaml"),
    os.path.join(config.RULES_DIR, "R-BDD01-002.yaml"),
    os.path.join(config.RULES_DIR, "R-FB01-001.yaml"),
]

EXPECTED_CHECK_IDS = ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11")
# 输入闸集合同样钉死（对抗审查抓获：只断言「全 OK」时 all([]) 恒真，整条闸被删仍绿）
EXPECTED_GATE_IDS = ("IG1", "IG2", "IG3", "IG4", "IG5", "IG6")

# ---- 记账器 ----
PASSED, FAILURES = [], []
SPEC_DEVIATIONS = []   # 第三类事实：期望值本身与真源打架——处置是回去改真源或改规格，不是改代码变绿
NETWORK_ATTEMPTS = []


def item(label, ok, why=""):
    (PASSED if ok else FAILURES).append((label, why))
    if not ok:
        print(f"  FAIL {label}" + (f"：{why}" if why else ""))


def deviation(tag, text):
    SPEC_DEVIATIONS.append((tag, text))


# ---- 零网络守卫（第二道防线；第一道是 replay mode 本身不碰网络）----
_real_urlopen = urllib.request.urlopen


def _blocked_urlopen(*args, **kwargs):
    NETWORK_ATTEMPTS.append(args[0] if args else "?")
    raise AssertionError("离线自测出现网络调用（守卫拦截）")


urllib.request.urlopen = _blocked_urlopen

# ---- 产物目录：不落仓库内 ----
WORKDIR = tempfile.mkdtemp(prefix="decision-offline-")


def _sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


WITNESS_BEFORE = {p: _sha256(p) for p in READONLY_WITNESSES if os.path.exists(p)}


def run_case(name, step1, step2, step3, plan=FROZEN_PLAN, extra=None):
    """in-process 跑一次 runner；返回 (exit_code, bundle_path, report_path)。"""
    out = os.path.join(WORKDIR, f"{name}.bundle.json")
    report = os.path.join(WORKDIR, f"{name}.report.json")
    argv = [
        "--plan", plan, "--snapshot", SNAPSHOT,
        "--replay-step1", step1, "--replay-step2", step2, "--replay-step3", step3,
        "--out", out, "--report", report,
        "--run-id", "RUN-OFFLINE-FIXED", "--created-at", "2026-08-18T00:00:00+00:00",
    ] + (extra or [])
    code = runner.main(argv)
    return code, out, report


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fx(name):
    return os.path.join(FIXTURES, name)


# ============================ E 环境前置 ============================

for f in ("BD-D01.step1.model_reply.json", "BD-D01.step2.model_reply.json", "BD-D01.step3.model_reply.json",
          "BD-D01.step2.blocked_candidate.model_reply.json",
          "NEG-01.out_of_pool_product.step2.model_reply.json", "NEG-02.not_json.step1.model_reply.txt",
          "NEG-03.judgment_no_support.step3.model_reply.json",
          "NEG-04.duplicate_candidate_id.step2.model_reply.json"):
    item(f"E1 夹具在位：{f}", os.path.exists(fx(f)))
item("E2 冻结上游 plan 在位（C.3 资产⑥ / B.4 模块隔离）", os.path.exists(FROZEN_PLAN))
item("E2 冻结快照在位", os.path.exists(SNAPSHOT))
item("E2 禁用词表在位（只读）", os.path.exists(config.FORBIDDEN_LEXICON_PATH))
item("E3 零网络守卫已装载", urllib.request.urlopen is _blocked_urlopen)
try:
    diffs = module_manifest.diff_against_disk()
    item("E4 module_manifest 与代码同步（--check 口径）", diffs == [], f"差异键：{diffs}")
except FileNotFoundError:
    item("E4 module_manifest 与代码同步（--check 口径）", False, "module_manifest.json 不存在——先跑生成器")

# ============================ 正向：BD-D01 两候选降级分支回放 ============================

code, out, report_path = run_case(
    "bdd01",
    fx("BD-D01.step1.model_reply.json"), fx("BD-D01.step2.model_reply.json"), fx("BD-D01.step3.model_reply.json"),
)
item("BD-D01 replay 退出码 0（Preflight 全过）", code == 0, f"exit={code}")
bundle = load_json(out) if os.path.exists(out) else None
report = load_json(report_path) if os.path.exists(report_path) else None
item("BD-D01 bundle 已写盘", bundle is not None)
item("BD-D01 report 已写盘", report is not None)

if bundle and report:
    item("报告 overall=OK", report.get("overall") == "OK")
    item("报告检查表 ID 集合恰为 D1..D11（少考了和全考过了在结论行上长得一样，必须集合相等）",
         tuple(c["id"] for c in report.get("checks", [])) == EXPECTED_CHECK_IDS,
         f"实得 {[c['id'] for c in report.get('checks', [])]}")
    item("报告带提前段标记（铁律④：全部产出标注非正式证据）",
         report.get("segment") == "M2-EP01 提前段·非正式证据")
    item("输入闸集合恰为 IG1..IG6 且全 OK（集合断言防整闸被删）",
         tuple(g["id"] for g in report.get("input_gates", [])) == EXPECTED_GATE_IDS
         and all(g["verdict"] == "OK" for g in report.get("input_gates", [])))
    item("candidate_count_status=DEGRADED_TWO（B.4.2/BD-D01 两候选降级分支）",
         bundle.get("candidate_count_status") == "DEGRADED_TWO")
    item("降级说明引用限制规则 R-BDD01-002（A.6.3：必须说明受何限制）",
         bool(bundle.get("candidate_count_explanation")) and "R-BDD01-002" in bundle["candidate_count_explanation"])
    item("候选恰两个（C1/C2）",
         [c["candidate_id"] for c in bundle.get("candidate_options", [])] == ["C1", "C2"])
    item("human_selection_required 恒真（A.6.2：机器不替 Founder 选方案）",
         bundle.get("human_selection_required") is True)
    item("阻断诊断恰一条且为 R-BDD01-002 BLOCK",
         len(bundle.get("blocked_candidate_diagnostics", [])) == 1
         and all(r["result"] == "BLOCK" and r["rule_ref"]["object_id"] == "R-BDD01-002"
                 for r in bundle["blocked_candidate_diagnostics"][0]["blocking_rule_results"]))
    active_rule_ids = {"R-BDD01-001", "R-BDD01-002"}   # 快照钉定的规则集（A.4.3 active_rule_refs）
    item("每候选对快照钉定的 2 条 ACTIVE 规则各有一条 HardRuleResult 且全 PASS（G.2 第 4 条①）",
         all({r["rule_ref"]["object_id"] for r in c["hard_rule_results"]} == active_rule_ids
             and all(r["result"] == "PASS" for r in c["hard_rule_results"])
             for c in bundle["candidate_options"]))
    tmap = {e["trace_id"]: e["trace_type"] for e in bundle["trace_bundle"]["entries"]}
    rec = bundle.get("system_recommendation") or {}
    item("推荐指向存活候选 C1 且 judgment_trace_ref 挂 MODEL_JUDGMENT（A.6.3）",
         rec.get("candidate_id") == "C1" and tmap.get(rec.get("judgment_trace_ref")) == "MODEL_JUDGMENT")
    item("冲突显式识别非空且 trace_refs 全可溯（BD_CONFLICT_MISSED 结构面）",
         len(bundle.get("recognized_conflicts", [])) >= 1
         and all(ref in tmap for c in bundle["recognized_conflicts"] for ref in c["trace_refs"]))
    item("Trace 含全部四类（A.1.2 四类分离的存在性）",
         {"FACT", "RULE", "ASSUMPTION", "MODEL_JUDGMENT"} <= set(tmap.values()))
    item("质检单逐规则带机器可查/仅人可查两栏（G.2 第 4 条红线；快照钉定 2 条规则）",
         len(report.get("machine_human_register", [])) == 2
         and all(r.get("machine_checkable") and r.get("human_only") for r in report["machine_human_register"]))
    item("报告含逐规则评估证据（评估目标 3 个：候选 C1、C2 + 被拦路径×1）",
         len(report.get("rule_evaluations", [])) == 3)
    item("报告如实登记 llm_mode=replay（live 时该字段与 limiting 陈述随之翻转）",
         report.get("llm_mode") == "replay")

# ============================ 确定性：同一输入两次运行逐字节一致 ============================

code2, out2, _ = run_case(
    "bdd01-again",
    fx("BD-D01.step1.model_reply.json"), fx("BD-D01.step2.model_reply.json"), fx("BD-D01.step3.model_reply.json"),
)
if code2 == 0 and os.path.exists(out) and os.path.exists(out2):
    item("确定性：同一输入（含注入的 run-id/created-at）两次运行 bundle 逐字节一致",
         _sha256(out) == _sha256(out2))
else:
    item("确定性：第二次运行可复跑", False, f"exit={code2}")

# ============================ 变体：候选级拦截与隔离（对抗审查修复的端到端复测）============================

code, out_b, report_b = run_case(
    "bdd01-blocked",
    fx("BD-D01.step1.model_reply.json"), fx("BD-D01.step2.blocked_candidate.model_reply.json"),
    fx("BD-D01.step3.model_reply.json"),
)
item("变体（含禁用词候选 C3）：正确拦截后整跑仍绿（此前 D7 自扫自红，修复后必须 exit 0）", code == 0, f"exit={code}")
if code == 0 and os.path.exists(out_b):
    bundle_b = load_json(out_b)
    report_b_obj = load_json(report_b)
    item("变体：C3 被拦、存活恰 C1/C2、DEGRADED_TWO",
         [c["candidate_id"] for c in bundle_b["candidate_options"]] == ["C1", "C2"]
         and bundle_b["candidate_count_status"] == "DEGRADED_TWO")
    item("变体：阻断诊断两条（被拦候选 C3 + 促销路线），全部 BLOCK",
         len(bundle_b["blocked_candidate_diagnostics"]) == 2
         and all(r["result"] == "BLOCK" for d in bundle_b["blocked_candidate_diagnostics"]
                 for r in d["blocking_rule_results"]))
    _all_expl = [r["explanation"] for d in bundle_b["blocked_candidate_diagnostics"]
                 for r in d["blocking_rule_results"]]
    item("变体：BLOCK explanation 不回写命中原词（取证文本不得自带禁用表达）",
         all("清仓" not in e for e in _all_expl) and any("low_price_selling" in e for e in _all_expl))
    item("变体：D7 全产物扫描仍零命中（正确拦截不再自红）",
         {c["id"]: c["verdict"] for c in report_b_obj["checks"]}.get("D7") == "OK")
    _stmts_b = [e.get("statement") or "" for e in bundle_b["trace_bundle"]["entries"]]
    item("变体：被拦候选的假设/判断不建条目（C3 的『季末仍有清货窗口』『价格动作可以最快回笼资金』零残留，无孤儿）",
         all("季末仍有清货窗口" not in s and "价格动作可以最快回笼资金" not in s for s in _stmts_b))
    item("变体：评估目标 4 个（候选×3 + 被拦路径×1）", len(report_b_obj.get("rule_evaluations", [])) == 4)

# ============================ 负向 ============================

code, out_neg1, report_neg1 = run_case(
    "neg01",
    fx("BD-D01.step1.model_reply.json"), fx("NEG-01.out_of_pool_product.step2.model_reply.json"),
    fx("BD-D01.step3.model_reply.json"),
)
item("NEG-01 池外商品：退出码 1（后校验判红，bundle 留取证）", code == 1, f"exit={code}")
if os.path.exists(report_neg1):
    neg1_checks = {c["id"]: c["verdict"] for c in load_json(report_neg1).get("checks", [])}
    item("NEG-01 D9 判 FAIL（BD_FACT_FABRICATION 结构面：池外商品即补写）", neg1_checks.get("D9") == "FAIL")
item("NEG-01 bundle 仍写盘（失败产物是取证材料）", os.path.exists(out_neg1))

code, out_neg2, _ = run_case(
    "neg02",
    fx("NEG-02.not_json.step1.model_reply.txt"), fx("BD-D01.step2.model_reply.json"),
    fx("BD-D01.step3.model_reply.json"),
)
item("NEG-02 非 JSON 输出：退出码 2（没跑完）", code == 2, f"exit={code}")
item("NEG-02 不产出半成品 bundle", not os.path.exists(out_neg2))

code, out_neg3, _ = run_case(
    "neg03",
    fx("BD-D01.step1.model_reply.json"), fx("BD-D01.step2.model_reply.json"),
    fx("NEG-03.judgment_no_support.step3.model_reply.json"),
)
item("NEG-03 判断无支撑：退出码 2（A.9.2 在 trace 层 fail-loud）", code == 2, f"exit={code}")
item("NEG-03 不产出半成品 bundle", not os.path.exists(out_neg3))

code, out_neg4, _ = run_case(
    "neg04",
    fx("BD-D01.step1.model_reply.json"), fx("NEG-04.duplicate_candidate_id.step2.model_reply.json"),
    fx("BD-D01.step3.model_reply.json"),
)
item("NEG-04 candidate_id 重号：退出码 2（唯一性硬闸，身份失去唯一落点不产半成品）", code == 2, f"exit={code}")
item("NEG-04 不产出半成品 bundle", not os.path.exists(out_neg4))

# 输入闸：上游未放行（next_action=REQUEST_INPUT）不得进入候选生成
_gate_plan = load_json(FROZEN_PLAN)
_gate_plan["next_action"] = "REQUEST_INPUT"
_gate_plan_path = os.path.join(WORKDIR, "plan.request_input.json")
with open(_gate_plan_path, "w", encoding="utf-8") as f:
    json.dump(_gate_plan, f, ensure_ascii=False)
code, out_gate, _ = run_case(
    "neg-gate",
    fx("BD-D01.step1.model_reply.json"), fx("BD-D01.step2.model_reply.json"),
    fx("BD-D01.step3.model_reply.json"), plan=_gate_plan_path,
)
item("输入闸 IG1：上游 REQUEST_INPUT → 退出码 2（A.5.2 约束3，不进入候选生成）", code == 2, f"exit={code}")
item("输入闸拦截时不产出 bundle", not os.path.exists(out_gate))

# ============================ 正向对照组（掏空防线检测）============================

def preflight_ctx():
    snapshot = preprocess.load_snapshot(SNAPSHOT)
    fact_pool = preprocess.materialize_fact_pool(snapshot)
    rule_pool = preprocess.filter_active_rules(
        preprocess.filter_rule_pool_by_brand(preprocess.rule_pool_from_snapshot(snapshot), snapshot.get("brand_id")))
    return {
        "schema_path": config.SCHEMA_BUSINESS_DECISION_BUNDLE,
        "fact_pool": fact_pool,
        "rule_pool": rule_pool,
        "snapshot": snapshot,
        "product_ids": preprocess.list_product_ids(snapshot),
    }


def verdict_of(bundle_obj, ctx, check_id):
    for c in postcheck.preflight(bundle_obj, ctx).get("checks", []):
        if c["id"] == check_id:
            return c["verdict"], c["detail"]
    return None, "检查项不存在"


def control(label, base_bundle, ctx, check_id, mutate, extra_why=""):
    before, why_before = verdict_of(base_bundle, ctx, check_id)
    if before != "OK":
        item(f"对照 {label}", False, f"改坏之前 {check_id} 就不是 OK（{before}：{why_before}）——对照无效")
        return
    mutated = copy.deepcopy(base_bundle)
    mutate(mutated)
    after, why_after = verdict_of(mutated, ctx, check_id)
    item(f"对照 {label}", after == "FAIL", f"改坏后 {check_id}={after}（{why_after}）{extra_why}")


if bundle:
    CTX = preflight_ctx()

    control("① D2：两候选硬标 TARGET_THREE 必红", bundle, CTX, "D2",
            lambda b: b.update(candidate_count_status="TARGET_THREE"))
    control("② D5：human_selection_required=false 必红（人工门绕过）", bundle, CTX, "D5",
            lambda b: b.update(human_selection_required=False))
    control("③ D4：判断引用指向 FACT 必红（四类混写）", bundle, CTX, "D4",
            lambda b: b["candidate_options"][0].update(model_judgment_refs=["FACT:facts.inventory"]))
    control("④ D6：BLOCK 结果混入存活候选必红（A.9.1）", bundle, CTX, "D6",
            lambda b: b["candidate_options"][0]["hard_rule_results"].__setitem__(
                0, dict(b["candidate_options"][0]["hard_rule_results"][0], result="BLOCK")))
    control("⑤ D7：注入禁用词必红", bundle, CTX, "D7",
            lambda b: b["candidate_options"][0].update(strategy=b["candidate_options"][0]["strategy"] + "清仓"))
    control("⑥ D8：注入池外数字必红", bundle, CTX, "D8",
            lambda b: b.update(business_problem=b["business_problem"] + "预计售出 9999 件"))
    control("⑦ D9：商品引用换池外 P99 必红", bundle, CTX, "D9",
            lambda b: b["candidate_options"][0]["product_roles"][0]["product_ref"].update(object_id="P99"))
    control("⑧ D3：清空取舍必红（BD_TRADEOFF_MISSING 结构面）", bundle, CTX, "D3",
            lambda b: b.update(comparative_tradeoffs=[]))
    control("⑨ D11：候选降级而 bundle 硬标 HIGH 必红（只降不升）", bundle, CTX, "D11",
            lambda b: b["confidence"].update(level="HIGH"))
    control("⑩ D10：review_status=APPROVED 必红（系统产出必须 PENDING）", bundle, CTX, "D10",
            lambda b: b["artifact"].update(review_status="APPROVED"))
    # 对照⑪ 超出既有 D 面自补：D1 是唯一挡"字段整个缺席"的防线，必须证明它真的在挡
    control("⑪ D1：删除必填字段 recognized_conflicts 必红（schema 键缺席假绿洞）", bundle, CTX, "D1",
            lambda b: b.pop("recognized_conflicts"))
    # 对照⑫-⑮：对抗审查修复批次的回归护栏（每条都是被抓获后补的防线，先证 OK 再证必红）
    control("⑫ D1：created_at 写非法时间串必红（FormatChecker 生效，此前任意字符串照过）", bundle, CTX, "D1",
            lambda b: b["artifact"].update(created_at="不是时间"))
    control("⑬ D2：candidate_id 重号必红（张冠李戴场景的 postcheck 侧兜底）", bundle, CTX, "D2",
            lambda b: b["candidate_options"][1].update(candidate_id=b["candidate_options"][0]["candidate_id"]))
    control("⑭ D4：孤儿 MODEL_JUDGMENT 必红（无人引用的判断条目 = 证据挂空）", bundle, CTX, "D4",
            lambda b: b["trace_bundle"]["entries"].append(
                {"trace_id": "MJ-ORPHAN", "trace_type": "MODEL_JUDGMENT", "statement": "无人引用的判断",
                 "supporting_trace_refs": ["FACT:facts.inventory"], "target_paths": []}))
    control("⑮ D8：借位数字 39 必红（'39'⊂'3980' 的子串洞已封，整值口径）", bundle, CTX, "D8",
            lambda b: b.update(business_problem=b["business_problem"] + "预计首周售出 39 件"))

# ============================ 回归护栏（函数级直调，不依赖场景侧影）============================

_snapshot = preprocess.load_snapshot(SNAPSHOT)   # A.4.3 引用式 → kernel/facts 内联兼容视图
_pool = preprocess.materialize_fact_pool(_snapshot)
_by_id = {f["fact_id"]: f for f in _pool}
item("护栏① 事实池物化：库存 800 在池且路径正确（视图坐标 facts.product.inventory，Quantity 内层 value）",
     (_by_id.get("FACT:facts.product.inventory", {}).get("value") or {}).get("value") == 800)
item("护栏② 事实池物化：价格 3980 在池（Money 内层 amount）",
     (_by_id.get("FACT:facts.product.price", {}).get("value") or {}).get("amount") == 3980)
item("护栏③ 商品池识别 = [P13]", preprocess.list_product_ids(_snapshot) == ["P13"])
_rules = preprocess.filter_active_rules(
    preprocess.filter_rule_pool_by_brand(preprocess.rule_pool_from_snapshot(_snapshot), _snapshot.get("brand_id")))
item("护栏④ 规则池 = 快照钉定 2 条 ACTIVE（R-BDD01-001/002）且品牌全等",
     [r["rule_id"] for r in _rules] == ["R-BDD01-001", "R-BDD01-002"]
     and all(r["status"] == "ACTIVE" for r in _rules))
_gates = preprocess.check_input_gates(load_json(FROZEN_PLAN), _snapshot, _rules)
item("护栏⑤ 输入闸集合恰为 IG1..IG6 且对冻结输入全 OK（集合断言防整闸被删）",
     tuple(g["id"] for g in _gates) == EXPECTED_GATE_IDS and all(g["verdict"] == "OK" for g in _gates))
_groups, _note = rules_engine.load_forbidden_groups()
item("护栏⑥ 禁用词表分组非空可核验（含 low_price_selling 组）",
     len(_groups) > 0 and "low_price_selling" in _groups, _note)
_unmapped_result, _unmapped_note = rules_engine.evaluate_rule_on_texts(
    {"rule_id": "R-NOT-REGISTERED", "status": "ACTIVE"}, ["任意文本"], _groups)
item("护栏⑦ 无谓词映射的规则不发结果（fail-closed，无检测器不得判过）",
     _unmapped_result is None and "不发结果" in _unmapped_note)
_rules_by_id = {r["rule_id"]: r for r in _rules}
# R-FB01-001 不在 BD-D01 快照钉定集内（active_rule_refs 只含 R-BDD01-001/002）；
# 分组归属护栏用注册表同形合成 dict 做函数级验证（引擎按 rule_id 查映射表，形状即可）
_fb_rule = {"rule_id": "R-FB01-001", "status": "ACTIVE", "version": 1,
            "brand_id": "fixture-brand-01", "target_path": "*"}
_r1_pass, _ = rules_engine.evaluate_rule_on_texts(_rules_by_id["R-BDD01-001"], ["高级感的呈现"], _groups)
_fb_block, _ = rules_engine.evaluate_rule_on_texts(_fb_rule, ["高级感的呈现"], _groups)
item("护栏⑩ 词表分组归属：『高级感』只以 R-FB01-001（brand_tone）名义 BLOCK，不冒充低价叫卖证据",
     _r1_pass is not None and _r1_pass["result"] == "PASS"
     and _fb_block is not None and _fb_block["result"] == "BLOCK")
item("护栏⑪ BLOCK explanation 不回写命中原词、带组名可复核",
     _fb_block is not None and "高级感" not in _fb_block["explanation"] and "brand_tone" in _fb_block["explanation"])
_no_field_results, _no_field_unev = rules_engine.evaluate_candidate({"title": "只有标题没有策略字段"}, _rules, _groups)
item("护栏⑫ target_path 解析不到字段不发 PASS（空文本 ≠ 零命中，进 unevaluated）",
     any(rid == "R-BDD01-002" for rid, _n in _no_field_unev))
item("护栏⑬ filter_active_rules 丢弃非 ACTIVE（单点过滤，防非 ACTIVE 进 prompt）",
     preprocess.filter_active_rules([{"status": "ACTIVE", "rule_id": "a"}, {"status": "INACTIVE", "rule_id": "b"}])
     == [{"status": "ACTIVE", "rule_id": "a"}])
try:
    trace.build_trace_bundle(_pool, _rules, ["FACT:facts.不存在的字段"], [], [], [], brand_id="fixture-brand-01")
    item("护栏⑧ 池外 FACT 引用在 trace 层报错（幻觉引用组装不出合法 Trace）", False, "未抛错")
except trace.TraceAssemblyError:
    item("护栏⑧ 池外 FACT 引用在 trace 层报错（幻觉引用组装不出合法 Trace）", True)
try:
    trace.build_trace_bundle(_pool, _rules, [], [], [], [{"trace_id": "MJ-X", "trace_type": "MODEL_JUDGMENT",
                                                          "statement": "无支撑判断", "supporting_trace_refs": []}],
                             brand_id="fixture-brand-01")
    item("护栏⑨ MODEL_JUDGMENT 无支撑在 trace 层报错（A.9.2）", False, "未抛错")
except trace.TraceAssemblyError:
    item("护栏⑨ MODEL_JUDGMENT 无支撑在 trace 层报错（A.9.2）", True)

# ============================ 收尾守卫 ============================

item("G1 产物目录不在仓库内", not os.path.abspath(WORKDIR).startswith(os.path.abspath(REPO_ROOT)))
_witness_after = {p: _sha256(p) for p in WITNESS_BEFORE}
item("G2 考卷区/合同区只读见证：跑前跑后 sha256 逐一相等（零写考卷）", _witness_after == WITNESS_BEFORE)
item("G3 全程零网络调用", NETWORK_ATTEMPTS == [], f"出现 {len(NETWORK_ATTEMPTS)} 次")

# ============================ 规格偏离登记 ============================

deviation(
    "GAP-BD-UPSTREAM｜BD-D02/03 无冻结 IntentExecutionPlan 夹具（已登记 UPSTREAM_GAPS.md，本批不阻塞）",
    "C.3 资产⑥与 B.4 模块隔离要求 BD 测试用冻结上游输入；考卷区当前只有 BD-D01 备有该夹具。"
    "本车道不代上游定义（开工令②），故场景面只覆盖 BD-D01；BD-D02/03 的回放待上游夹具落盘后追加。",
)
deviation(
    "GAP-SNAPSHOT-SHAPE｜✅ 已随块 E 关闭（合流适配完成，留痕防复读旧口径）",
    "原登记：考卷快照内联形状 ≠ A.4.3 引用式。块 E（PR #15）已把 15 份快照迁为引用式并落"
    "kernel/facts 官方消费通道；本模块按预案只改 preprocess（运行时谓词 + materialize_legacy_view），"
    "规则池改为快照钉定（active_rule_refs）。UPSTREAM_GAPS.md 第 2/4/5 条随之更新。",
)

# ============================ 结论 ============================

total, passed_n, failed_n = len(PASSED) + len(FAILURES), len(PASSED), len(FAILURES)
print()
if SPEC_DEVIATIONS:
    print("规格偏离登记（处置=改真源或改规格，不是改代码变绿）：")
    for tag, text in SPEC_DEVIATIONS:
        print(f"  · {tag}\n    {text}")
print(f"合计 {total} 项：通过 {passed_n}，失败 {failed_n}")
if failed_n:
    print("DECISION_OFFLINE_RED")
    print(f"产物保留供取证：{WORKDIR}")
    sys.exit(1)
shutil.rmtree(WORKDIR, ignore_errors=True)
print("DECISION_OFFLINE_GREEN")
sys.exit(0)
