#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/intent 离线自测（纯 replay，零网络，零写考卷区）。

它是什么：把 `kernel/intent/fixtures/` 里手写的模型回复喂进 runner，跑完整条编排
（确定性前处理 → 1 步 LLM（replay） → 确定性覆盖与硬闸 → Preflight），再对产出的
IntentExecutionPlan 与 Preflight 报告逐条断言。断言口径来自 A.5.2 七条约束 + contracts/OD-03
+ M1-EP02 修复批次的两条仲裁口径（见文末「规格偏离登记」），**不由本文件自造，也不为求绿放宽**。
期望值只取真源推导值：跑出来与期望不符时，正确动作是回去查真源或改实现，不是改这里的期望。

**正向对照组（本文件的自我拆台环节，务必保留）**：上面那类断言全是"跑通 + Preflight 九项全 OK"，
它们有一个共同弱点——**把某个检查项掏空成永远返回 OK，全部断言会更容易通过**，结论行照打 GREEN。
所以文件末尾另有一组反向用例：直接 `import postcheck`，喂手造的坏 plan，断言指定项**必须 FAIL**，
且每条都先核验"改坏之前该项是 OK"（否则断言 FAIL 什么都证明不了）。检查器被掏空时这一组立刻判红。

它**不是**什么（诚实边界，别把 GREEN 当合规图章）：
  · 不是 B 的验收判分。B.4.1 的「允许答案族 / 禁止结果 / 人工裁判问题」有大量语义判断，
    本文件一条都判不了；这里只验机器可判的结构与状态机行为。
  · 不是真实模型行为的证据。夹具是**手写**的（见 fixtures/README.md），它证明的是
    「模型这么答时系统会怎么处理」，不是「模型会这么答」。
  · 不覆盖 A.5.2 约束6（同一快照跨运行的目标迁移）的完整语义：本文件只能比对两次运行的
    required_context 差集非空 + 快照字节未变，判不了「下游重点是否真的变了」。

判绿口径（全部同时成立才 INTENT_OFFLINE_GREEN）：合计项数 > 0 且失败数 = 0。
话术与结论行格式对齐 tools/test_detectors.py / tools/test_fact_schemas.py
（`合计 N 项：通过 X，失败 Y`），便于将来接进 tools/check_m0.py 的同款门禁正则。

用法: python3 kernel/intent/test_intent_offline.py    （不接受参数；改口径 = 改本文件，不设放宽开关）
退出码: 0 = 全过；1 = 有失败；2 = 用法错误
"""
import contextlib
import copy
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import urllib.request

import yaml

# 允许直接 `python3 kernel/intent/test_intent_offline.py` 运行：本文件按 `kernel.intent.*` 包名 import
# 同批资产（runner 内部也用相对 import），所以仓库根必须在 sys.path 上。插到最前是为了避免
# 同名第三方包抢先（比如 site-packages 里恰好有个 kernel 包），那会让自测跑的根本不是本仓代码。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from kernel.intent import module_manifest, postcheck, preprocess, runner   # noqa: E402  （必须在 sys.path 就位之后）
from kernel.intent.config import (   # noqa: E402
    BUSINESS_GOAL_FIELD_PATH,
    FIXTURES_DIR,
    FORBIDDEN_LEXICON_PATH,
    SCHEMA_INTENT_EXECUTION_PLAN,
)

CASES_DIR = os.path.join(REPO_ROOT, "acceptance", "cases")

# Preflight 应当给出的九项。写成常量并做**集合相等**断言，是为了拦一类假绿：
# 把检查表删掉几项（比如去掉 P4），剩下的项全 OK，overall 照样是 OK——
# "少考了"和"全考过了"在结论行上长得一模一样，只有比对项数才分得开。
EXPECTED_CHECK_IDS = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9")

# ======================================================================================
# 零网络守卫
# ======================================================================================
# 本文件声称"零网络"。声称不算数——把 urlopen 换成会当场记账并抛错的桩，
# 任何一次意外的 live 调用都会留下痕迹（NETWORK_ATTEMPTS），最后由 G2 项断言它为空。
# 只拦 urlopen 而不拦整个 socket：llm.py 的 live 路径唯一出口就是 urllib.request.urlopen
# （实测该文件只 import urllib.request / urllib.error），拦到这一层足够，也不会误伤别的东西。
NETWORK_ATTEMPTS = []
_REAL_URLOPEN = urllib.request.urlopen


def _blocked_urlopen(*args, **kwargs):
    NETWORK_ATTEMPTS.append(str(args[0])[:120] if args else "<no-arg>")
    raise AssertionError("离线自测中出现网络调用——本文件零网络，任何 live 请求都是缺陷")


urllib.request.urlopen = _blocked_urlopen


# ======================================================================================
# 记账
# ======================================================================================
PASSED, FAILURES = [], []
# 「规格偏离登记」：既不是通过也不是失败的第三类事实——某条断言的**期望值本身**与冻结真源打架时，
# 在这里逐条登记并打印。为什么要单独一栏：这类事项的处置是"回去改真源或改规格"，
# 不是"改代码让它变绿"，混进失败列表里会被当成待修 bug，混进通过列表里则直接消失。
SPEC_DEVIATIONS = []


def item(label, ok, why=""):
    """记一项断言。why 只在失败时打印，所以要写清楚"实得什么、依据哪条真源"。"""
    if ok:
        PASSED.append(label)
    else:
        FAILURES.append((label, why))


def deviation(tag, text):
    SPEC_DEVIATIONS.append((tag, text))


# ======================================================================================
# 运行一个场景
# ======================================================================================

class Result(object):
    """一次 runner.main 调用的全部留痕：退出码 / plan / report / 标准输出与标准错误。

    stderr 一并留着，是因为硬闸的判定理由（"硬闸：存在阻断缺失 …，模型判 RESOLVED 被改判 NEEDS_INPUT"）
    只打在 stderr——断言"闸确实动了"而不只是"结果恰好对"，必须看得到这行。
    """

    def __init__(self, code, plan, report, out, err):
        self.code, self.plan, self.report, self.stdout, self.stderr = code, plan, report, out, err


def run_scenario(scn, work_dir):
    """按场景表跑一次 runner CLI（in-process，捕获输出），返回 Result。

    走 runner.main(argv) 而不是子进程：一是快，二是子进程的 exit code 会被 shell 截断成 0-255
    （本例用不到大值，但没必要给自己留坑），三是 in-process 才能让上面的零网络守卫真正生效——
    子进程有自己的解释器，桩打不进去。
    """
    out_path = os.path.join(work_dir, scn["name"] + ".plan.json")
    report_path = os.path.join(work_dir, scn["name"] + ".preflight.json")
    argv = [
        "--snapshot", os.path.join(CASES_DIR, scn["case"], "fixtures", "context_snapshot.json"),
        "--task", scn["task"],
        "--mode", scn["mode"],
        "--replay", os.path.join(FIXTURES_DIR, scn["fixture"]),
        "--out", out_path,
        "--report", report_path,
    ]
    if scn.get("stated_goal"):
        argv += ["--stated-goal", scn["stated_goal"]]

    buf_out, buf_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = runner.main(argv)

    def _load(path):
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    return Result(code, _load(out_path), _load(report_path), buf_out.getvalue(), buf_err.getvalue())


# ======================================================================================
# 断言用的小谓词
# ======================================================================================

def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def preflight_state(result):
    """返回 (九项是否齐, 非 OK 的项列表)。两件事一起返回，是因为"少了几项"和"有项没过"
    都会让「过 P1-P9」这句话不成立，但原因完全不同，报错时必须分得清。"""
    if result.report is None:
        return False, ["report 未落盘（本次运行没跑到 Preflight）"]
    checks = result.report.get("checks") or []
    ids = tuple(c.get("id") for c in checks)
    complete = sorted(ids) == sorted(EXPECTED_CHECK_IDS)
    bad = ["%s=%s（%s）" % (c.get("id"), c.get("verdict"), str(c.get("detail"))[:120])
           for c in checks if c.get("verdict") != "OK"]
    if not complete:
        bad.insert(0, "检查项不齐：实得 %s，期望 %s" % (list(ids), list(EXPECTED_CHECK_IDS)))
    return complete and not bad, bad


def field_paths(items):
    return [i.get("field_path") for i in (items or [])]


def assumption_targets(plan):
    """plan.assumptions 覆盖到的 field_path 集合（只认 target_paths，不认 statement 里提到字段名）。

    比 postcheck._assumption_covers 严一档：那里为了不误伤"只把字段名写进 statement"的合法写法
    留了兜底，本文件是自测，验的是 runner 有没有**结构化地**把假设挂到缺失项上——
    靠 statement 里出现字符串来配对，正是那种"看着过了、实则没绑定"的弱证据。
    """
    out = set()
    for entry in (plan.get("assumptions") or []):
        for path in (entry.get("target_paths") or []):
            out.add(path)
    return out


# ======================================================================================
# 场景表
# ======================================================================================
# task / mode / stated_goal 三项**同源读取自考卷区**，不在本文件手抄（M1-EP02 修复批次 K6）：
#   · task_statement / execution_mode ← acceptance/cases/<CASE>/manifest.<变体>.yaml
#   · stated_business_goal            ← acceptance/cases/INT-D02/fixtures/task_input.json
# 首轮是把这几句话手抄进本文件的常量。手抄的问题不是"抄错了"（当时逐字核过），而是**会漂移**：
# 考卷区哪天改了一个标点，自测照旧用旧句子跑，仍然全绿，而它验的已经不是那道考题了——
# 且没有任何检测器会喊。同源读取让这种漂移在物理上不可能发生。
# 只读：本文件对考卷区只做 open(...,"r")，收尾还会比对字节哈希（G2 项）。


def read_case_manifest(case, variant):
    """读一份运行 Manifest（考卷区，只读），返回 dict。

    读不到 / 缺关键键就抛异常让整次自测挂掉，不做默认值兜底：
    "manifest 少了 task_statement 就用一句默认任务原话继续跑"正是上面要堵的漂移，
    只不过换了个更隐蔽的形态。
    """
    path = os.path.join(CASES_DIR, case, "manifest.%s.yaml" % variant)
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise RuntimeError("Manifest 不是 YAML 映射：%s" % path)
    for key in ("task_statement", "execution_mode"):
        if not data.get(key):
            raise RuntimeError("Manifest 缺 %s：%s（自测不替考卷区补默认值）" % (key, path))
    return data


def read_stated_goal(case):
    """读某案例 fixtures/task_input.json 的 stated_business_goal（A.4.1 Task.stated_business_goal 的落盘位）。"""
    path = os.path.join(CASES_DIR, case, "fixtures", "task_input.json")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    goal = data.get("stated_business_goal")
    if not goal:
        raise RuntimeError("task_input.json 缺 stated_business_goal：%s" % path)
    return goal


def _scn(name, case, variant, fixture, with_stated_goal=False):
    """按 (案例, Manifest 变体) 组一条场景；任务原话与模式一律现读，不写死。"""
    manifest = read_case_manifest(case, variant)
    scenario = {
        "name": name,
        "case": case,
        "mode": manifest["execution_mode"],
        "task": manifest["task_statement"],
        "fixture": fixture,
    }
    if with_stated_goal:
        scenario["stated_goal"] = read_stated_goal(case)
    return scenario


# 负向三份共用 INT-D01 的快照与任务原话（它们考的是模型越权/幻觉引用时系统怎么办，
# 与"哪一道考题"无关），故同样从 INT-D01.quick 的 Manifest 现读，不另抄一句。
SCENARIOS = (
    _scn("INT-D01.quick", "INT-D01", "quick", "INT-D01.quick.model_reply.json"),
    _scn("INT-D01.enhanced", "INT-D01", "enhanced", "INT-D01.enhanced.model_reply.txt"),
    _scn("INT-D02.quick", "INT-D02", "quick", "INT-D02.quick.model_reply.json", with_stated_goal=True),
    _scn("INT-D03.input-a", "INT-D03", "input-a", "INT-D03.input-a.model_reply.json"),
    _scn("INT-D03.input-b", "INT-D03", "input-b", "INT-D03.input-b.model_reply.json"),
    _scn("NEG-01.forced_continue", "INT-D01", "quick", "NEG-01.forced_continue.model_reply.json"),
    _scn("NEG-02.out_of_pool_ref", "INT-D01", "quick", "NEG-02.out_of_pool_ref.model_reply.json"),
    _scn("NEG-03.candidate_ref_out_of_pool", "INT-D01", "quick",
         "NEG-03.candidate_ref_out_of_pool.model_reply.json"),
)

# 只读取证清单：跑之前算一遍 sha256，跑完再算一遍。考卷区（acceptance/）被本模块写过一个字节，
# 就等于考生改了考题——C.2 隔离门的机器面在这里。
READONLY_WITNESSES = tuple(
    [os.path.join(CASES_DIR, c, "fixtures", "context_snapshot.json") for c in ("INT-D01", "INT-D02", "INT-D03")]
    + [FORBIDDEN_LEXICON_PATH]
)


# ======================================================================================
# 主流程
# ======================================================================================

def main(argv):
    if argv[1:]:
        sys.stderr.write("用法错误：test_intent_offline.py 不接受参数。\n")
        return 2

    work_dir = tempfile.mkdtemp(prefix="intent-offline-")

    # ---- E 环境前置 --------------------------------------------------------------
    missing_fixtures = [s["fixture"] for s in SCENARIOS
                        if not os.path.exists(os.path.join(FIXTURES_DIR, s["fixture"]))]
    item("E1 %d 份 replay 夹具齐在" % len(SCENARIOS), not missing_fixtures, "缺失：%s" % missing_fixtures)

    missing_snapshots = [p for p in READONLY_WITNESSES if not os.path.exists(p)]
    item("E2 三份 INT 快照 + 禁用词表齐在（只读）", not missing_snapshots, "缺失：%s" % missing_snapshots)

    item("E3 零网络守卫已装载", urllib.request.urlopen is _blocked_urlopen,
         "urlopen 未被替换，本次运行不具备零网络保证")

    item("G1 运行产物不落在仓库内", not os.path.abspath(work_dir).startswith(REPO_ROOT + os.sep),
         "产物目录 %s 在仓库内——自测不得往仓库里写文件" % work_dir)

    manifest_problems = module_manifest.diff_against_disk()
    item("E4 module_manifest.json 与代码同步（手改无效的执行面）", not manifest_problems,
         "；".join(manifest_problems)[:400])

    before = {p: sha256_of(p) for p in READONLY_WITNESSES if os.path.exists(p)}

    # ---- 跑全部场景 --------------------------------------------------------------
    results = {}
    for scn in SCENARIOS:
        results[scn["name"]] = run_scenario(scn, work_dir)

    # ---- D01：模糊目标不得擅自确定（两种模式各一遍） -----------------------------
    for name in ("INT-D01.quick", "INT-D01.enhanced"):
        r = results[name]
        plan = r.plan or {}
        item("%s goal_resolution=AMBIGUOUS（承认目标没说清）" % name,
             plan.get("goal_resolution") == "AMBIGUOUS",
             "实得 %r（B.4.1/INT-D01 允许答案族：必须保留 AMBIGUOUS）" % plan.get("goal_resolution"))
        item("%s business_goal 为空（A.5.2 约束1）" % name,
             plan.get("business_goal") is None,
             "实得 %r——静默确定唯一目标是 B.4.1/INT-D01 的禁止结果" % plan.get("business_goal"))
        item("%s 候选 ≥ 2 且互不相同（A.5.2 约束1）" % name,
             len({c.get("goal") for c in (plan.get("goal_candidates") or [])}) >= 2,
             "实得候选 %s" % [c.get("goal") for c in (plan.get("goal_candidates") or [])])
        item("%s next_action=REQUEST_INPUT（A.5.2 约束1）" % name,
             plan.get("next_action") == "REQUEST_INPUT",
             "实得 %r——「已给出两个候选」不得成为 CONTINUE 的理由" % plan.get("next_action"))
        conf = (plan.get("confidence") or {}).get("level")
        item("%s confidence 非 HIGH（B.4.1/INT-D01 禁止结果）" % name, conf != "HIGH",
             "实得 %r——关键目标未知时不得给 HIGH" % conf)
        ok, bad = preflight_state(r)
        item("%s Preflight 九项全 OK" % name, ok, "非 OK 项：%s" % bad)

    # ---- D02：快速模式带已声明目标（期望值按仲裁2 = 真源推导，不按首轮规格 L80 的字面）----
    # 仲裁2（M1-EP02 修复批次）：kernel 行为按 OD-03 §二 原文——「品牌促销边界（最低折扣线 / 禁用表达）」
    # 是 INVENTORY_ACTIVATION 的**追加阻断项**；INT-D02 快照按 B.4.1/INT-D02「输入」刻意不带品牌事实。
    # 两者相乘，快速侧出现 BLOCKING 缺失 → NEEDS_INPUT，这是**正确行为**，不是缺陷。
    # B:320「非阻断信息缺失时允许继续」是条件句（前提是"非阻断"），不构成"快速模式可绕过阻断项"。
    r = results["INT-D02.quick"]
    plan = r.plan or {}
    missing = plan.get("missing_context") or []
    blocking_paths = [m.get("field_path") for m in missing if m.get("impact") == "BLOCKING"]
    d02_conditions = {
        "goal_resolution=NEEDS_INPUT": plan.get("goal_resolution") == "NEEDS_INPUT",
        "business_goal=null（A.5.2 约束2）": plan.get("business_goal") is None,
        "next_action=REQUEST_INPUT（A.5.2 约束2）": plan.get("next_action") == "REQUEST_INPUT",
        "BLOCKING 缺失含 brand.promotion_boundary（OD-03 §二 库存激活行）":
            "brand.promotion_boundary" in blocking_paths,
    }
    # 四个子条件合并成一项：它们同源于「D02 快速侧按 OD-03 必然被阻断项拦下」这一个期望，
    # 拆开会把同一个根因报成四次失败，读起来像四个 bug。
    item("INT-D02.quick 按 OD-03 被促销边界阻断（NEEDS_INPUT + 目标清空 + REQUEST_INPUT）",
         all(d02_conditions.values()),
         "未成立的子条件：%s；实得 goal_resolution=%r business_goal=%r next_action=%r，BLOCKING 缺失=%s"
         % ([k for k, v in d02_conditions.items() if not v], plan.get("goal_resolution"),
            plan.get("business_goal"), plan.get("next_action"), blocking_paths))
    ok, bad = preflight_state(r)
    item("INT-D02.quick Preflight 九项全 OK", ok, "非 OK 项：%s" % bad)
    conf = (plan.get("confidence") or {}).get("level")
    item("INT-D02.quick 模型自报 HIGH 被压低（置信度只降不升）", conf in ("MEDIUM", "LOW"),
         "夹具自报 confidence_level=HIGH，最终实得 %r——G6 只降不升未生效" % conf)
    # 闸留痕必须进产物（K2）：只打 stderr 的话，拿到 plan.json 的人分不清这个 NEEDS_INPUT
    # 是模型自己判的还是系统改判的——而这两件事的处置完全不同。
    basis_text = " ".join(str(b) for b in ((plan.get("confidence") or {}).get("basis") or []))
    item("INT-D02.quick 改判与目标出处写进 confidence.basis（可从产物追溯，不只在 stderr）",
         "系统改判" in basis_text and "--stated-goal" in basis_text,
         "basis 实得：%s" % basis_text[:300])
    item("INT-D02.quick 退出码与 Preflight 结论一致",
         r.code == (0 if (r.report or {}).get("overall") == "OK" else 1),
         "exit=%r overall=%r（overall!=OK 必须 exit 1，且 plan 照写盘便于取证）"
         % (r.code, (r.report or {}).get("overall")))

    # ---- D03：同一快照的目标迁移 --------------------------------------------------
    ra, rb = results["INT-D03.input-a"], results["INT-D03.input-b"]
    plan_a, plan_b = ra.plan or {}, rb.plan or {}
    item("INT-D03.input-a 解析为 INVENTORY_ACTIVATION 且继续（A.5.2 约束3）",
         plan_a.get("business_goal") == "INVENTORY_ACTIVATION"
         and plan_a.get("next_action") == "CONTINUE_TO_DECISION",
         "实得 business_goal=%r next_action=%r" % (plan_a.get("business_goal"), plan_a.get("next_action")))

    missing_a = plan_a.get("missing_context") or []
    non_qr_a = [m.get("field_path") for m in missing_a if m.get("impact") != "QUALITY_REDUCING"]
    covered_a = assumption_targets(plan_a)
    unpaired_a = [m.get("field_path") for m in missing_a if m.get("field_path") not in covered_a]
    item("INT-D03.input-a QUICK 跨过的缺失全为 QUALITY_REDUCING 且逐项有 ASSUMPTION（A.5.2 约束4）",
         bool(missing_a) and not non_qr_a and not unpaired_a,
         "缺失 %d 项；非 QUALITY_REDUCING=%s；无 ASSUMPTION 配对=%s"
         % (len(missing_a), non_qr_a, unpaired_a))

    # 标签如实（M1-EP02 修复批次 K6）：首轮这一项叫「目标确实迁移了」，但它实际断言的是
    # **两侧终态不同**——b 侧的 business_goal 是被 G2 硬闸清空成 null 的（人设阻断），
    # 不是"模型把目标解析成了另一个"。用"迁移"当标签会让读者以为这一项证明了后者。
    # 故拆成两项：一项如实描述终态，另一项去断言**闸前**解析出的目标确实不同（那才是"迁移"）。
    item("INT-D03 两侧 business_goal 终态不同（a=已解析目标；b=被人设阻断闸清空为 null）",
         plan_a.get("business_goal") != plan_b.get("business_goal"),
         "两侧同为 %r" % plan_a.get("business_goal"))

    # 闸前解析目标：直接读两份 replay 夹具里模型给出的 business_goal（那是硬闸动手之前的值）。
    # 读夹具而不是读 plan，正是因为 plan 里的 b 侧已经被闸清空了。
    def _fixture_goal(fixture_name):
        with open(os.path.join(FIXTURES_DIR, fixture_name), encoding="utf-8") as fh:
            return runner.llm.parse_model_json(fh.read()).get("business_goal")

    goal_a_raw = _fixture_goal("INT-D03.input-a.model_reply.json")
    goal_b_raw = _fixture_goal("INT-D03.input-b.model_reply.json")
    item("INT-D03 闸前解析目标两侧不同（同一快照、只换任务原话 → 目标确实迁移；A.5.2 约束6 的前半句）",
         goal_a_raw is not None and goal_b_raw is not None and goal_a_raw != goal_b_raw,
         "a 侧闸前目标=%r，b 侧闸前目标=%r" % (goal_a_raw, goal_b_raw))

    set_a, set_b = set(field_paths(plan_a.get("required_context"))), set(field_paths(plan_b.get("required_context")))
    item("INT-D03 两侧 required_context 双向差集非空（A.5.2 约束6 的机器可判部分）",
         bool(set_a - set_b) and bool(set_b - set_a),
         "a-b=%s，b-a=%s——目标变了但需要的上下文没变，说明 resolver 没按目标分岔"
         % (sorted(set_a - set_b), sorted(set_b - set_a)))

    ok_a, bad_a = preflight_state(ra)
    ok_b, bad_b = preflight_state(rb)
    item("INT-D03 两侧 Preflight 九项全 OK", ok_a and ok_b,
         "a 非 OK：%s；b 非 OK：%s" % (bad_a, bad_b))

    item("INT-D03.input-b 因人设阻断进入 NEEDS_INPUT（OD-03 §二 品牌故事行）",
         plan_b.get("goal_resolution") == "NEEDS_INPUT"
         and "persona" in [m.get("field_path") for m in (plan_b.get("missing_context") or [])
                           if m.get("impact") == "BLOCKING"],
         "实得 goal_resolution=%r，阻断缺失=%s"
         % (plan_b.get("goal_resolution"),
            [m.get("field_path") for m in (plan_b.get("missing_context") or []) if m.get("impact") == "BLOCKING"]))

    # ---- 确定性：同一份输入连跑两次必须逐字节一致 --------------------------------
    # 按名字取而不是按下标：场景表增删一条就会让下标指向另一个场景，而那时这一项仍然"通过"——
    # 它只是换了个对象在比"两次跑是否一致"，读结论行完全看不出来。
    scn_a = next(s for s in SCENARIOS if s["name"] == "INT-D03.input-a")
    repeat = run_scenario(dict(scn_a, name="INT-D03.input-a.repeat"), work_dir)
    plan_r = repeat.plan or {}
    same = (json.dumps(plan_a.get("required_context"), ensure_ascii=False, sort_keys=True)
            == json.dumps(plan_r.get("required_context"), ensure_ascii=False, sort_keys=True)
            and json.dumps(plan_a.get("missing_context"), ensure_ascii=False, sort_keys=True)
            == json.dumps(plan_r.get("missing_context"), ensure_ascii=False, sort_keys=True)
            and (plan_a.get("trace_bundle") or {}).get("trace_bundle_id")
            == (plan_r.get("trace_bundle") or {}).get("trace_bundle_id"))
    # 只比对确定性部分：artifact_id / created_at 含运行时钟，本来就该每次不同，拿它们比是自造假红。
    item("同一输入连跑两次：required/missing/trace_bundle_id 逐字节一致（replay 可复现）", same,
         "两次不一致——确定性前后处理里混进了时钟、随机或字典序不稳定的东西")

    # ---- 负向 ---------------------------------------------------------------------
    rn = results["NEG-01.forced_continue"]
    plan_n = rn.plan or {}
    item("NEG-01 硬闸把「RESOLVED + 阻断缺失」改判 NEEDS_INPUT（A.5.2 约束5）",
         plan_n.get("goal_resolution") == "NEEDS_INPUT" and plan_n.get("business_goal") is None
         and plan_n.get("next_action") == "REQUEST_INPUT",
         "实得 goal_resolution=%r business_goal=%r next_action=%r"
         % (plan_n.get("goal_resolution"), plan_n.get("business_goal"), plan_n.get("next_action")))
    # 留痕要两处都在：stderr（跑的人当场看得见）+ 产物 confidence.basis（拿到 plan.json 的人事后追得到）。
    neg1_basis = " ".join(str(b) for b in ((plan_n.get("confidence") or {}).get("basis") or []))
    item("NEG-01 模型越权写的 next_action=CONTINUE_TO_DECISION 未被采纳，且改判理由 stderr + 产物双留痕",
         plan_n.get("next_action") == "REQUEST_INPUT"
         and "系统改判" in rn.stderr and "系统改判" in neg1_basis,
         "实得 next_action=%r；stderr 含改判留痕=%s；confidence.basis 含改判留痕=%s"
         % (plan_n.get("next_action"), "系统改判" in rn.stderr, "系统改判" in neg1_basis))
    ok_n, bad_n = preflight_state(rn)
    item("NEG-01 改判后 Preflight 九项全 OK 且 exit 0", ok_n and rn.code == 0,
         "exit=%r；非 OK 项：%s" % (rn.code, bad_n))

    rp = results["NEG-02.out_of_pool_ref"]
    item("NEG-02 引用池外 FACT ID → 组装期硬失败，exit 2（C.3 资产⑤红线）", rp.code == 2,
         "实得 exit=%r——池外引用被静默清洗掉，比判红更危险" % rp.code)
    item("NEG-02 失败时不产出半成品 plan（没跑完 ≠ 通过）", rp.plan is None,
         "exit 2 却写出了 plan：%s" % (list((rp.plan or {}).keys())[:6]))

    # NEG-03：池外 ID **只**出现在 goal_candidates.supporting_trace_refs。
    # 这条路径与 NEG-02 不同——runner 只把 model_out.referenced_fact_ids 传给 trace.build_trace_bundle，
    # 候选的支撑引用不经过组装期校验，于是它不会 exit 2，而是一路走到 Preflight 由 P6 判红。
    # 两条路径必须各有一份夹具：只留 NEG-02 的话，"候选里的幻觉引用"这条通道无人把守，
    # 而它恰恰是 INT-D01 这类 AMBIGUOUS 运行最常见的形态（候选才是那次运行的主要输出）。
    rc = results["NEG-03.candidate_ref_out_of_pool"]
    p6 = next((c for c in ((rc.report or {}).get("checks") or []) if c.get("id") == "P6"), None)
    item("NEG-03 候选支撑引用指向池外 ID → P6 判 FAIL（不是静默放过，也不是组装期 exit 2）",
         p6 is not None and p6.get("verdict") == "FAIL",
         "P6 实得 %r（detail: %s）" % ((p6 or {}).get("verdict"), str((p6 or {}).get("detail"))[:200]))
    item("NEG-03 判红即 exit 1，且 plan 照写盘便于取证（失败的产物是证据，不许不落盘）",
         rc.code == 1 and isinstance(rc.plan, dict) and bool(rc.plan.get("goal_candidates")),
         "exit=%r；plan 是否落盘=%s；候选数=%d"
         % (rc.code, isinstance(rc.plan, dict), len((rc.plan or {}).get("goal_candidates") or [])))

    # ---- 正向对照组：把 postcheck 掏空会不会更绿 -----------------------------------
    # 为什么必须有这一组（它堵的是本文件自身最大的一个漏洞）：
    # 上面所有断言的形式都是「跑通 + Preflight 九项全 OK」。这类断言有一个致命的共同弱点——
    # **把某个检查项改成永远返回 OK，全部断言会更容易通过**。删掉 P4 的判定逻辑、让它 return "OK"，
    # 上面每一项都会变绿，结论行照打 INTENT_OFFLINE_GREEN。也就是说：光看正向用例，
    # 分不清"系统真的守住了"和"检查器被掏空了"。
    # 对照组的做法是反过来：直接 import postcheck，喂进**手造的坏 plan**，断言指定项必须 FAIL。
    # 检查器一旦被掏空，这一组立刻判红。每条都先核验"改坏之前该项是 OK"，再核验"改坏之后变 FAIL"——
    # 只断言后半句是不够的：若该项本来就一直 FAIL，断言 FAIL 也会通过，什么都没证明。
    def preflight_ctx(case, mode):
        """按某案例快照现搭一份 Preflight ctx（与 runner.run 里的组法一致，含 SYS-08 品牌过滤）。"""
        snap = preprocess.load_snapshot(os.path.join(CASES_DIR, case, "fixtures", "context_snapshot.json"))
        return {
            "schema_path": SCHEMA_INTENT_EXECUTION_PLAN,
            "fact_pool": preprocess.materialize_fact_pool(snap),
            "rule_pool": runner.filter_rule_pool_by_brand(preprocess.load_rule_pool(), snap.get("brand_id")),
            "snapshot": snap,
            "execution_mode": mode,
        }

    def verdict_of(plan_obj, ctx, check_id):
        report = postcheck.preflight(plan_obj, ctx)
        for c in report.get("checks") or []:
            if c.get("id") == check_id:
                return c.get("verdict"), str(c.get("detail"))[:220]
        return None, "报告里根本没有 %s 这一项（检查表被删过？）" % check_id

    def control(label, base_plan, ctx, check_id, mutate, extra_why=""):
        """一条对照：base 上该项应当 OK；按 mutate 改坏之后该项必须 FAIL。"""
        if not isinstance(base_plan, dict):
            item(label, False, "基线 plan 未落盘，对照无从做起")
            return
        before, before_detail = verdict_of(base_plan, ctx, check_id)
        broken = copy.deepcopy(base_plan)
        mutate(broken)
        after, after_detail = verdict_of(broken, ctx, check_id)
        item(label, before == "OK" and after == "FAIL",
             "改坏前 %s=%r（期望 OK，detail: %s）；改坏后 %s=%r（期望 FAIL，detail: %s）%s"
             % (check_id, before, before_detail, check_id, after, after_detail, extra_why))

    ctx_d01 = preflight_ctx("INT-D01", "QUICK")
    ctx_d03 = preflight_ctx("INT-D03", "QUICK")

    control(
        "对照① AMBIGUOUS 却不发 goal_candidates 键 → P1 必 FAIL（A.5.2 约束1「候选至少两个」）",
        results["INT-D01.quick"].plan, ctx_d01, "P1",
        lambda p: p.pop("goal_candidates", None),
        extra_why="｜本项依赖考卷侧 Schema 修复（AMBIGUOUS 分支补 required:[goal_candidates]）："
                  "JSON Schema 的 then.properties 对**缺席的键**是空操作，键不发就绕过 minItems:2。"
                  "Schema 未修时本项会红，属已知依赖，不得靠删断言消化。")
    control(
        "对照② QUICK 跨过 QR 缺失却给 confidence=HIGH → P3 必 FAIL（A:393 / OD-03 四-1「和 confidence 限制」）",
        results["INT-D03.input-a"].plan, ctx_d03, "P3",
        lambda p: p.setdefault("confidence", {}).__setitem__("level", "HIGH"))
    control(
        "对照③ RESOLVED 且存在 BLOCKING 缺失 → P4 必 FAIL（A.5.2 约束5；仲裁1 的 RESOLVED 分支）",
        results["NEG-01.forced_continue"].plan, ctx_d01, "P4",
        lambda p: p.update({"goal_resolution": "RESOLVED", "business_goal": "INVENTORY_ACTIVATION"}))

    def _empty_rule_object_refs(p):
        for entry in ((p.get("trace_bundle") or {}).get("entries") or []):
            if entry.get("trace_type") == "RULE":
                entry["object_refs"] = []

    control(
        "对照④ RULE 条目 object_refs 被清空 → P6 必 FAIL（A:68「RULE 必须引用规则版本」）",
        results["INT-D03.input-a"].plan, ctx_d03, "P6", _empty_rule_object_refs)

    def _disguise_fact_as_judgment(p):
        """把一条 FACT 条目的 trace_type 改成 MODEL_JUDGMENT，trace_id 的 `FACT:` 前缀原样留着。"""
        for entry in ((p.get("trace_bundle") or {}).get("entries") or []):
            if entry.get("trace_type") == "FACT":
                entry["trace_type"] = "MODEL_JUDGMENT"
                return

    # ⑤ 不在 M1-EP02 修复规格列的四条对照里，是本文件补的第五条：P6 本批新增的"前缀伪装"判定
    # （A:72）若没有对照，它就是一条没有任何测试守着的新规则——加了却没人验，与没加的差别只在
    # "看起来做了"。补一条，代价一个 lambda。
    control(
        "对照⑤ FACT: 前缀的条目被改成 MODEL_JUDGMENT → P6 必 FAIL"
        "（A:72「ASSUMPTION 和 MODEL_JUDGMENT 不得伪装为 FACT」）",
        results["INT-D03.input-a"].plan, ctx_d03, "P6", _disguise_fact_as_judgment)

    # ---- 回归护栏：修复批次三条新增行为（对抗核验的变异测试实证：掏空后原自测仍绿，故补） ----
    # 为什么补：K2-1 品牌过滤 / K1-2 枚举守卫 / K2-4 澄清问题落点 三项此前只有一次性脚本取证，
    # 常驻自测没有任何断言守着——掏空即静默退化。护栏各一条，直接调函数级行为，不再依赖场景侧影。
    _pool = [
        {"rule_id": "R-A", "statement": "s", "scope": "x", "effect": "PROHIBIT", "target_path": "t",
         "version": 1, "brand_id": "fixture-brand-01"},
        {"rule_id": "R-B", "statement": "s", "scope": "x", "effect": "PROHIBIT", "target_path": "t",
         "version": 1, "brand_id": "other-brand-99"},
        {"rule_id": "R-C", "statement": "s", "scope": "x", "effect": "PROHIBIT", "target_path": "t"},
    ]
    with contextlib.redirect_stderr(io.StringIO()):
        _kept = runner.filter_rule_pool_by_brand(_pool, "fixture-brand-01")
    item("护栏① SYS-08 品牌过滤：他牌规则与无 brand_id 规则被剔除，本牌保留",
         [r["rule_id"] for r in _kept] == ["R-A"],
         "实得 %s（期望仅 R-A）" % [r.get("rule_id") for r in _kept])

    def _bg_availability(value):
        snap = {"snapshot_id": "S-guard", "brand_id": "fixture-brand-01",
                "facts": {"business_goal": {"value": value}}}
        with contextlib.redirect_stderr(io.StringIO()):
            req, _missing = preprocess.resolve_requirements(None, snap, "随便一句")
        hits = [r for r in req if "business_goal" in r.get("field_path", "")]
        return hits[0]["availability"] if hits else None
    item("护栏② 快照侧 business_goal 枚举守卫：枚举外值判 MISSING、枚举内值判 AVAILABLE",
         _bg_availability("春节大促冲一波") == "MISSING" and _bg_availability("CONVERSION") == "AVAILABLE",
         "枚举外→%s，枚举内→%s" % (_bg_availability("春节大促冲一波"), _bg_availability("CONVERSION")))

    _d01_plan = results["INT-D01.quick"].plan
    _d01_fixture_q = json.load(open(os.path.join(FIXTURES_DIR, "INT-D01.quick.model_reply.json"),
                                    encoding="utf-8")).get("clarification_question")
    _bg_items = [r for r in (_d01_plan or {}).get("missing_context", [])
                 if "business_goal" in r.get("field_path", "")]
    item("护栏③ 澄清问题落点：模型定制问句替换 business_goal 项的模板 resolution_question（B:283）",
         bool(_d01_fixture_q) and bool(_bg_items)
         and _bg_items[0].get("resolution_question") == _d01_fixture_q,
         "夹具问句=%r，产物问句=%r" % (_d01_fixture_q,
                                       _bg_items[0].get("resolution_question") if _bg_items else None))

    _d01_raw = os.path.join(work_dir, "INT-D01.quick.plan.json.raw.txt")
    _d01_fixture_path = os.path.join(FIXTURES_DIR, "INT-D01.quick.model_reply.json")
    item("护栏④ 原始回复落盘：<out>.raw.txt 写出且与模型回复逐字一致（ATT-0004 刀①成功路径）",
         os.path.exists(_d01_raw)
         and open(_d01_raw, encoding="utf-8").read().strip()
             == open(_d01_fixture_path, encoding="utf-8").read().strip(),
         "raw 文件存在=%s" % os.path.exists(_d01_raw))

    # 失败路径才是 ATT-0004 观测缺口的真回归：解析炸掉时 plan 不得写、raw 必须已写
    _bad_fixture = os.path.join(work_dir, "bad_reply.txt")
    with open(_bad_fixture, "w", encoding="utf-8") as fh:
        fh.write("这不是 JSON{{{")
    _bad_out = os.path.join(work_dir, "bad.plan.json")
    _buf_o, _buf_e = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(_buf_o), contextlib.redirect_stderr(_buf_e):
        _bad_code = runner.main([
            "--snapshot", os.path.join(CASES_DIR, "INT-D01", "fixtures", "context_snapshot.json"),
            "--task", "帮我推广羊绒大衣。", "--mode", "QUICK",
            "--replay", _bad_fixture,
            "--out", _bad_out, "--report", os.path.join(work_dir, "bad.preflight.json"),
        ])
    item("护栏⑤ 失败路径 raw 仍落盘：坏 JSON 回放 exit 2、plan 未写、<out>.raw.txt 已写（ATT-0004 观测缺口回归）",
         _bad_code == 2 and not os.path.exists(_bad_out) and os.path.exists(_bad_out + ".raw.txt"),
         "code=%s plan存在=%s raw存在=%s" % (_bad_code, os.path.exists(_bad_out), os.path.exists(_bad_out + ".raw.txt")))

    # ---- 收尾：只读取证 + 零网络 ---------------------------------------------------
    changed = [p for p, h in before.items() if sha256_of(p) != h]
    item("G2 考卷区文件字节未变（三份 INT 快照 + 禁用词表）", not changed, "被改动：%s" % changed)
    item("G3 全程零网络（守卫未被触发）", not NETWORK_ATTEMPTS, "出现网络调用：%s" % NETWORK_ATTEMPTS)

    # ---- 规格偏离登记（不是通过也不是失败，处置动作是回真源裁决，不是改代码） -----
    deviation(
        "SPEC-DEV-01｜AMBIGUOUS 与约束5 的关系（**已仲裁 + 已登记台账**，本批不再阻塞）",
        "情形：OD-03 §一 #2 把 business_goal 列为通用阻断项，于是 INT-D01（目标未提供）只要保持 AMBIGUOUS，"
        "按约束5 的字面孤读（「有 BLOCKING 就必须 NEEDS_INPUT」）就永远过不了 P4；而 B:285-286 明写"
        "「必须保留 AMBIGUOUS」。M1-EP02 主循环仲裁1 给出的自洽解：**AMBIGUOUS 只承载「目标未明」**——"
        "AMBIGUOUS 且阻断缺失 ⊆ {business_goal} 时 P4 放行，阻断缺失里还有别的项则必须 NEEDS_INPUT。"
        "四条证据链（B:285-286 / A 约束1 把 AMBIGUOUS 定为合法终态且「Task 进入 NEEDS_INPUT」约束的是 Task 状态 /"
        " OD-03 §一 #2 引的是约束3 不是约束5 / 字面孤读会把 A 约束1 分支与 B:285 变成死条文）逐条写在"
        " postcheck._p4_constraint5 的文档串里。"
        "落地位置：postcheck P4 + runner.apply_hard_gates 的 G2 分支（口径同源于 config.BUSINESS_GOAL_FIELD_PATH）。"
        "状态：**执行侧对冻结真源的解释，非真源原文**，已登记裁决台账「待 Founder 裁决」表；Founder 可推翻。"
        "推翻时改的是上述两处代码，不改考卷。")
    deviation(
        "SPEC-DEV-02｜INT-D02 快速侧进 NEEDS_INPUT 是**正确行为**（已仲裁，非缺陷）",
        "OD-03 §二 把「品牌促销边界（最低折扣线 / 禁用表达）」列为 INVENTORY_ACTIVATION 的追加阻断项；"
        "INT-D02 快照按 B.4.1/INT-D02「输入」刻意不带品牌事实。两者相乘，快速侧出现 BLOCKING 缺失 → NEEDS_INPUT。"
        "仲裁2 钉定：kernel 行为按 OD-03 原文，B:320「非阻断信息缺失时允许继续」是**条件句**"
        "（前提是缺的那些是非阻断项），不构成「快速模式可绕过阻断项」——本文件因此把 D02 的期望值改成真源推导值，"
        "不是放宽断言。首轮写的「A 与 B 互斥」是不准确的归因（B 那句本就带前提），已删。"
        "遗留冲突（不阻塞本批，登记待裁）：Founder 2026-08-17 IA-0 裁决（OQ-BUILD-02）称补上 stated_business_goal 后"
        "「快速侧缺失项仅剩 QUALITY_REDUCING 类（人设 / 品牌信息）」，与 OD-03 §二 该行对「品牌信息」impact 归属的"
        "写法不一致，须回 OD-03 定夺；已登记台账。"
        "该目标下「QUICK 跨过 QR 并逐项产生 ASSUMPTION」这一考点，本文件由 INT-D03.input-a 承载（同为 INVENTORY_ACTIVATION，"
        "但其快照带品牌事实，实测 5 项 QR 缺失全部生成 ASSUMPTION），考点未落空。")
    deviation(
        "SPEC-DEV-03｜INT-D03 input-b 侧同样进 NEEDS_INPUT",
        "OD-03 §二 把「主理人人设事实」列为 BRAND_STORY 的追加阻断项，而 INT-D03 共用快照未带入 persona。"
        "故 b 侧 goal_resolution=NEEDS_INPUT、plan.business_goal=null。接口规格 L80 的「goal 不同」在字面上仍成立，"
        "但「目标迁移」的实证改由 required_context 双向差集承担（本文件已如此断言）。此项属真源推导的必然结果，"
        "非缺陷，登记以免被误读成「Intent 认不出品牌故事目标」。")

    # ---- 结论 ---------------------------------------------------------------------
    if SPEC_DEVIATIONS:
        print("\n规格偏离登记（须回真源裁决，不得靠改断言消化）：")
        for tag, text in SPEC_DEVIATIONS:
            print("  · %s\n      %s" % (tag, text))
    if FAILURES:
        print("\n失败明细：")
        for label, why in FAILURES:
            print("  ✗ %s\n      %s" % (label, why))

    total = len(PASSED) + len(FAILURES)
    print("\n合计 %d 项：通过 %d，失败 %d" % (total, len(PASSED), len(FAILURES)))
    green = total > 0 and not FAILURES
    if green:
        shutil.rmtree(work_dir, ignore_errors=True)
    else:
        # 判红时保留产物：失败的 plan / report 是取证材料，删掉就只剩一行"失败"可看
        print("产物保留在：%s" % work_dir)
    print("INTENT_OFFLINE_GREEN" if green else "INTENT_OFFLINE_RED")
    return 0 if green else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
