#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M0 门禁统一入口（P0-5「可传播门禁」；施工真源 M0收口修复批次_执行规格.md §二 P0-5）。

为什么必须有这个文件（外部审查 BLOCK-05）：M0 的门禁此前散在四个脚本里，靠人**记住**"跑哪几条、
看输出的哪几行才算过"。干净 clone 上没人记得住，CI 上更没人替你记——门禁不可传播 = 等于没有门禁。
本文件把那条链焊成一条命令，并把"怎样才算过"从人的记忆里搬进断言。

判绿条件（五步，顺序执行，五步全过才 CHECK_M0_GREEN）：
  [1/5] python3 tools/freeze_gate.py --mode=sign     必须 GATE_GREEN 且 exit 0（十三条红线）
  [2/5] python3 tools/test_freeze_gate_mutations.py  冻结门负向变异回归 + 真仓零改动隔离核验
  [3/5] python3 tools/test_detectors.py              检测器负向测试
  [4/5] BD-D01 三夹具回归                            good→PENDING_HUMAN /
                                                     collapse→FAIL 标签集全等 {BD_CANDIDATE_COLLAPSE} /
                                                     fabricated→FAIL 标签集全等 {BD_FACT_FABRICATION}；
                                                     三轮均断言 case_version 与 (id,check,tag) 有序集合全等
  [5/5] tools/validate_schema.py 四例烟测             两条正例（结构过 + exit 0）
                                                     + 一条负例（结构违约 + exit 1）
                                                     + 一条不可核验（路径不存在 + exit 2）

铁律「exit 0 ≠ 通过」的落地方式（宪法 · 对 AI 执行侧的三条铁律 ②）：
  每一步都**同时**核验退出码与输出标记，两者缺一即红。理由是实测可复现的假绿路径——
  一个被截断/改坏的子脚本可以在什么都没测的情况下 exit 0；只看退出码的入口会把它读成"全绿"。
  第 3 步还额外断言"合计项数 > 0 且 通过数 == 合计数"：跑了 0 项测试同样 exit 0，
  而"0 项全过"不是通过，是没测。

冻结门**运行态**（不带 --mode=sign）**不计入判绿条件**，只多打一行类别统计供人读。
  依据：M0 阶段 20 份 Manifest 的 4 个构建版本字段按设计就是 PENDING_BUILD，运行态必然红
  （M0收口修复批次_执行规格.md §〇「默认运行态 80 条红线……设计内行为，非阻断」）。
  把设计内红线算进判绿条件会逼出"为了让门变绿去填未裁决版本号"——那正是 P0-6 明令禁止的动作。
  但**不计入判绿 ≠ 不许人看**：统计行照打，红线类别与条数一目了然，运行态哪天多出一类新红线，
  看的人当场能发现。

诚实边界（CHECK_M0_GREEN 不代表什么）：
  · 不代表 Founder 已签字——签字动作定义见 B.2.1 与 IA-0_冻结签字包.md §五；
  · 不代表案例内容质量合格——L1 只判 FAIL，终态 PENDING_HUMAN ≠ 通过，PASS 只属 L3 人工（C.5 / B.1.5）；
  · 不代表 HEAD 提交内容合格——本入口核验的是**当前工作区目录树**（末行转发 freeze_gate 归属块的
    ROOT/HEAD 即为此而设），干净 clone 一致性由 P0-6 回执证明；
  · 五步覆盖面之外的一切（未被变异覆盖的红线、L2/L3 判分面）本入口一概未验，不得据此宣称"M0 已验证"。

边界（C.2 / C.4：脚本只汇总不推导，不建平台）：本入口**不改任何被测文件**、不推导结论、
  不执行任何 git 写命令；纯 stdlib，不引入新依赖（统一入口不该比它调用的脚本更难装）。
  唯一的写动作是第 4 步产生的临时 RUN 回执，跑完即删（try/finally 保证异常路径也删），
  且只删本进程创建的那几个路径——预存的 RUN-000x 不碰。

用法: exit 0=五步全绿 1=有步骤红 2=用法错误
  python3 tools/check_m0.py           跑全部五步
  python3 tools/check_m0.py --help    打印简用法并 exit 0
  除此之外不接受任何参数：判绿口径写死在本文件里，**不设放宽开关**——
  同 tools/freeze_gate.py 的既定纪律（"改口径 = 改考卷"，须随修复批次一起改，
  不得由命令行开关在单次运行里临时放宽）。
"""
import io
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable or "python3"
STEP_TIMEOUT = 1800          # 单步上限（秒）：超时按红处理，避免 CI 挂死到平台超时才报错
DUMP_LIMIT = 400             # 失败时回显子进程输出的行数上限（超出只截尾并明示已截断）

# USAGE **不得包含结论标记串**（CHECK_M0_GREEN / CHECK_M0_RED）。
# 此前 USAGE = __doc__，而 docstring 里两处写了 CHECK_M0_GREEN——`--help` 一次空跑就能打出两次该串
# 并 exit 0。任何按"输出里有 CHECK_M0_GREEN"判绿的包装脚本、日志巡检或人工肉眼扫读都会被骗过。
# 现在 --help 与用法错误都只打印下面这段短用法；完整判绿口径与诚实边界留在本文件头注释里给读源码的人看。
# （同类修复见 tools/validate_schema.py 的 USAGE。）
USAGE = """用法: check_m0.py            跑 M0 门禁全部五步（顺序执行，五步全过才算过）
      check_m0.py --help     打印本说明并 exit 0
退出码: 0=五步全过 | 1=有步骤未过 | 2=用法错误
五步: [1/5] 冻结断言门送签态  [2/5] 冻结门负向变异回归  [3/5] 检测器负向测试
      [4/5] BD-D01 三夹具回归  [5/5] Schema 四例烟测（两正 + 一违约 + 一不可核验）
口径: 每步同时核验退出码与输出标记（exit 0 ≠ 通过）；不接受任何参数，判绿口径不设放宽开关。
边界: 本入口核验的是**当前工作区目录树**，不代表 Founder 已签字 / 案例质量合格 / HEAD 提交内容合格。
      完整判绿条件与诚实边界见本文件头注释（源码），不在本短用法里复述。
"""

# ---- 第 1 步：freeze_gate 归属块的转发锚点（末行 CHECK_M0_GREEN 的 ROOT/HEAD 由此而来）----
# 只**转发**门自己打印的归属行，不由本入口另算一遍：另算一遍等于两套口径，
# 一旦两边不一致，末行会替真实扫描面背书。
ATTR_ROOT_RE = re.compile(r"^扫描根\s+ROOT\s*\|\s*(.+?)\s*$", re.M)
ATTR_HEAD_RE = re.compile(r"^仓库\s+HEAD\s*\|\s*(.+?)\s*$", re.M)

# ---- 第 2 步：变异套件的结论行 ----
MUT_PASS_RE = re.compile(r"PASS\s*——\s*(\d+)\s*项全过")
MUT_ISOLATION_RE = re.compile(r"^\[隔离\]\s+PASS", re.M)

# ---- 第 3 步：检测器套件的合计行 ----
DET_TOTAL_RE = re.compile(r"合计\s*(\d+)\s*项：通过\s*(\d+)，失败\s*(\d+)")

# ---- 运行态统计（不计入判绿）----
RUN_RED_ITEM_RE = re.compile(r"^\s*\d+\.\s+(R\d+)\b", re.M)
RUN_RED_TOTAL_RE = re.compile(r"GATE_RED\s*——\s*以下\s*(\d+)\s*条红线未清")

# ---- 第 4 步：BD-D01 三夹具的期望终态与**断言集合**（三带案例真源 B.4.2/BD-D01；口径见 case.yaml）----
# 下面三个常量整体 = 回归基线。改其中任何一行 = 改回归基线，须说明依据，不得为了让门变绿而改。
#
# 为什么必须连"断言集合"一起钉（本批次实测缺陷，runtime_verified）：
#   此前本步只钉「终态 + 单个期望标签 + unknown=0」。在副本树上从 case.yaml 删掉 7 条 must_hold
#   里的 4 条（A3 tradeoff_nonempty / A4 trace_types_separated / A6 human_gate_flag /
#   A7 forbidden_expression），三夹具的终态与标签纹丝不动，本入口五步照样全绿——考卷被削掉一大半，
#   全链无人发现（冻结门只把 case.yaml 纳入占位残留扫描面，不算哈希、不核断言数）。
#   终态与标签只描述"剩下的断言判了什么"，描述不了"本轮到底跑了哪几条"；后者必须单独钉死。
# 三元组取自回执 l1_assertions 的 (id, check, tag)——tag 由 run_case.py 一律落盘（不只 FAIL 时），
#   顺序敏感：断言顺序变了也算考卷变了，同样要在这里同批改。
CASE_DIR = "acceptance/cases/BD-D01"
BD_D01_EXPECT_CASE_VERSION = "v0.1"
BD_D01_EXPECT_ASSERTIONS = (
    ("A1", "schema_valid", "SYS_SCHEMA_INVALID"),
    ("A2", "candidate_count", "BD_CANDIDATE_COLLAPSE"),
    ("A3", "tradeoff_nonempty", "BD_TRADEOFF_MISSING"),
    ("A4", "trace_types_separated", "BD_TRACE_MIXED"),
    ("A5", "numeric_grounding", "BD_FACT_FABRICATION"),
    ("A6", "human_gate_flag", "BD_HUMAN_GATE_BYPASSED"),
    ("A7", "forbidden_expression", "SYS_RULE_VIOLATION"),
)
# 第五列是**标签集合全等**的期望值（不是"包含"）：一个误伤扩大到负样例上的检测器，
# 只要不同时误伤 good 夹具，"包含"式断言就发现不了它多冒出来的标签。
BD_D01_EXPECT = (
    ("good", "fixtures/output_good.json", 0, "PENDING_HUMAN", ()),
    ("collapse", "fixtures/output_bad_candidate_collapse.json", 1, "FAIL", ("BD_CANDIDATE_COLLAPSE",)),
    ("fabricated", "fixtures/output_bad_fabricated_inventory.json", 1, "FAIL", ("BD_FACT_FABRICATION",)),
)

# ---- 第 5 步：Schema 烟测（实例与 schema 均为现有资产，**不新建夹具**）----
# 四条：两正 + 一违约 + 一不可核验。每条 = (标签, 实例路径, schema 路径, 期望退出码, 期望出现的标记, 禁止出现的标记)
#
# 为什么必须有负例（本批次实测缺陷，runtime_verified）：此前两条实例都是合规实例，断言只有
#   「SCHEMA_OK 且 exit 0」——把 tools/validate_schema.py 换成 7 行桩（无条件 print SCHEMA_OK;
#   sys.exit(0)），本入口五步依旧全绿，且 [4/5] 的 A1 schema_valid 同样被骗过
#   （checks.schema_valid 只按 returncode == 0 分岔）。一个"永远放行"的校验器完全满足只有正例的烟测，
#   「无检测器不得判 PASS」在这一步就是空文：校验器停止校验，门看不见。
#   加负例后，桩化校验器会在 invalid / unverifiable 两条上当场判红。
# 负例怎么选：不造新夹具，用**现有资产错配**——context_snapshot.json 拿 business_decision_bundle
#   的 schema 去校验，必然缺一堆 required 字段（实测 9 条 VIOLATION、exit 1）。
# 不可核验例：一条**故意不存在**的路径（不落任何文件），期望 exit 2 + SCHEMA_UNVERIFIABLE——
#   顺带把 P0-5 新加的退出码 2 纳入回归（此前它在整套门禁里零覆盖）。
SCHEMA_NX_INSTANCE = "acceptance/cases/BD-D01/fixtures/__no_such_instance_for_smoke__.json"
SCHEMA_SMOKE = (
    ("正例1", "acceptance/cases/BD-D01/fixtures/output_good.json",
     "contracts/schemas/business_decision_bundle.schema.json", 0, "SCHEMA_OK", None),
    ("正例2", "acceptance/cases/BD-D01/fixtures/intent_execution_plan.frozen.json",
     "contracts/schemas/intent_execution_plan.schema.json", 0, "SCHEMA_OK", None),
    ("负例·结构违约", "acceptance/cases/BD-D01/fixtures/context_snapshot.json",
     "contracts/schemas/business_decision_bundle.schema.json", 1, "SCHEMA_INVALID", "SCHEMA_OK"),
    ("负例·不可核验", SCHEMA_NX_INSTANCE,
     "contracts/schemas/business_decision_bundle.schema.json", 2, "SCHEMA_UNVERIFIABLE", "SCHEMA_OK"),
)

# ---- 运行态红线的**类别基线**（不计入判绿，仅供人读）----
# 为什么按类别写实：此前统计行的括注写「M0 阶段 PENDING_BUILD 类红线为设计内」，而实际输出是
#   110 条里只有 80 条属 PENDING_BUILD，另外 30 条是别的类别——读者会把 110 整体读成设计内的那一类，
#   "运行态哪天多出一类新红线，看的人当场能发现"这条设计意图就落空了。
# 数值是**说明性基线**，不参与判绿：对不上只加 ⚠ 提示，不改绿/红（判绿由五步定义，见文件头）。
RUNMODE_BASELINE = {
    "R2": (80, "PENDING_BUILD：20 份 Manifest × 4 个构建版本字段，M0 设计内（执行规格 §〇）；R11/R12 已随 P0-6 重签清零（2026-08-17）"),
}


class Step(object):
    """一步的结果。ok 由 reasons 是否为空推出——没有"手动置绿"的通道。"""

    def __init__(self, label, name):
        self.label = label
        self.name = name
        self.reasons = []
        self.summary = ""
        self.output = ""
        self.seconds = 0.0

    @property
    def ok(self):
        return not self.reasons


def run(cmd, timeout=STEP_TIMEOUT):
    """跑子进程，返回 (退出码, 合并后的输出)。stderr 并进 stdout——诊断信息不该因为流不同而丢失。

    PYTHONIOENCODING=utf-8：本仓输出全是中文，CI 容器上若落到 ascii 流编码会让子脚本
    在**打印结论行时**炸掉，看起来像"门失败了"，实则是编码问题——把它钉死，省掉这类假红。
    """
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        p = subprocess.run(cmd, cwd=ROOT, env=env, timeout=timeout,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           encoding="utf-8", errors="replace")
        return p.returncode, p.stdout or ""
    except subprocess.TimeoutExpired as e:
        out = e.output or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return 124, out + "\n[check_m0] 该步超过 %d 秒上限被终止（超时按红处理，不按未知处理）" % timeout
    except OSError as e:
        return 127, "[check_m0] 无法启动子进程 %r: %s" % (cmd, e)


def rel(path):
    return os.path.relpath(path, ROOT)


# ============================ 五个判绿步骤 ============================

def step_freeze_gate_sign():
    """[1/5] 冻结断言门 送签态：必须 GATE_GREEN 且 exit 0；顺带取出归属块供末行转发。"""
    s = Step("[1/5]", "冻结断言门 送签态")
    t0 = time.monotonic()
    rc, out = run([PY, "tools/freeze_gate.py", "--mode=sign"])
    s.seconds = time.monotonic() - t0
    s.output = out
    if rc != 0:
        s.reasons.append("退出码 %d ≠ 0" % rc)
    if "GATE_GREEN" not in out:
        s.reasons.append("输出无 GATE_GREEN 标记（exit 0 ≠ 通过：退出码与标记必须同时成立）")
    if "GATE_RED" in out:
        s.reasons.append("输出含 GATE_RED——有红线未清")

    m_root = ATTR_ROOT_RE.search(out)
    m_head = ATTR_HEAD_RE.search(out)
    s.root = m_root.group(1).strip() if m_root else None
    # 归属行形如 "仓库 HEAD  | <sha>（读自 .git，未执行 git 命令）"；括号里是口径说明，转发时去掉。
    # 门取不到 HEAD 时该字段是"非 git 工作区 / HEAD 取不到"——这句照样原样转发：
    # 门自己承认取不到 ≠ 门没打印归属块，前者不判红（非 git 工作区是合法用法），后者判红。
    s.head = m_head.group(1).split("（")[0].strip() if m_head else None
    if s.root is None or s.head is None:
        # 这条 reason 会在红路径被打印，故同样不含结论标记串（否则 RED 输出里带着"绿"标记）
        s.reasons.append("freeze_gate 归属块解析失败（扫描根 ROOT / 仓库 HEAD 行取不到）"
                         "——末行结论将无法说明它扫的是哪一棵树，不可追溯的绿不算绿")

    s.summary = ("GATE_GREEN、exit 0（十三条红线全清）" if s.ok
                 else "未达 GATE_GREEN（exit %d）" % rc)
    return s


def step_mutations():
    """[2/5] 冻结门负向变异回归：套件自身必须 PASS，且真仓零改动隔离核验必须在场。"""
    s = Step("[2/5]", "冻结门负向变异回归")
    t0 = time.monotonic()
    rc, out = run([PY, "tools/test_freeze_gate_mutations.py"])
    s.seconds = time.monotonic() - t0
    s.output = out
    if rc != 0:
        s.reasons.append("退出码 %d ≠ 0（有变异未让门转红，或套件自身失真）" % rc)
    m = MUT_PASS_RE.search(out)
    if not m:
        s.reasons.append("输出无「PASS —— N 项全过」结论行（exit 0 ≠ 通过）")
        n = None
    else:
        n = int(m.group(1))
        if n <= 0:
            s.reasons.append("变异项数为 %d——跑了 0 项变异不是通过，是没测" % n)
    if not MUT_ISOLATION_RE.search(out):
        s.reasons.append("输出无「[隔离] PASS」行——真仓零改动核验未执行或未通过；"
                         "变异一旦泄漏出副本树，后续所有步骤都在被污染的树上跑")
    s.summary = ("%d 项全过、真仓零改动隔离 PASS、exit 0" % n) if s.ok else "变异回归未全过"
    return s


def step_detectors():
    """[3/5] 检测器负向测试：失败为 0 之外，还断言项数 > 0 且通过数 == 合计数（防"0 项全过"）。"""
    s = Step("[3/5]", "检测器负向测试")
    t0 = time.monotonic()
    rc, out = run([PY, "tools/test_detectors.py"])
    s.seconds = time.monotonic() - t0
    s.output = out
    if rc != 0:
        s.reasons.append("退出码 %d ≠ 0" % rc)
    m = DET_TOTAL_RE.search(out)
    total = passed = failed = None
    if not m:
        s.reasons.append("输出无「合计 N 项：通过 X，失败 Y」结论行（exit 0 ≠ 通过）")
    else:
        total, passed, failed = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if failed != 0:
            s.reasons.append("失败 %d 项" % failed)
        if total <= 0:
            s.reasons.append("合计项数为 0——跑了 0 项测试不是通过，是没测")
        if passed != total:
            s.reasons.append("通过 %d ≠ 合计 %d（有项目既不算通过也不算失败）" % (passed, total))
    s.summary = ("合计 %d 项：通过 %d、失败 0、exit 0" % (total, passed)) if s.ok else "检测器测试未全过"
    return s


def _parse_run_case_json(out):
    """run_case.py 末尾打印一行 JSON 摘要；取最后一个以 { 开头的行。解析不出来返回 None。"""
    for line in reversed(out.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except ValueError:
                return None
    return None


def step_bd_d01():
    """[4/5] BD-D01 三夹具回归：三带案例的正/负样例终态与标签必须与基线一致。

    临时 run-id + 跑完删产物：回归产物不该混进 acceptance/runs/ 的正式证据里
    （RUN-000x 是 P0-4 按 HEAD 重跑的留痕，被一个随手跑的回归覆盖掉就等于证据被污染）。
    删除只针对**本进程创建**的路径：跑之前先记录该路径是否已存在，已存在的一律不碰、且判红
    （撞名说明有别的东西占着，宁可报错也不静默覆盖别人的文件）。
    """
    s = Step("[4/5]", "BD-D01 三夹具回归")
    t0 = time.monotonic()
    created = []
    parts = []
    # 上一轮被 SIGKILL / CI job timeout 砍掉时 try/finally 覆盖不到，临时回执会留在证据目录里。
    # 下一轮 run-id 带的是新 pid，撞不上"路径已存在"那条红线——不主动扫一遍，证据目录会静默积垃圾，
    # 而残留本身说明上一轮是被打断的，本轮结论的清洁性存疑，必须让人看见。
    try:
        stale = sorted(f for f in os.listdir(os.path.join(ROOT, "acceptance/runs"))
                       if f.startswith("TMP-CHECKM0-") and f.endswith(".json"))
    except OSError as e:                     # 证据目录读不到本身就是问题，判红而不是当成"没有残留"
        stale = []
        s.reasons.append("acceptance/runs/ 列不出来（%s）——残留扫描没跑成，"
                         "本步的清洁性无从判断（读不到 ≠ 干净）" % e)
    if stale:
        s.reasons.append("acceptance/runs/ 里有上一轮遗留的临时回执 %d 份：%s——"
                         "残留说明上一轮 check_m0 被信号/超时打断（try/finally 覆盖不到），"
                         "请人工确认后删除再跑；本轮不代删他人产物" % (len(stale), "、".join(stale)))
    try:
        for tag, fixture, want_rc, want_status, want_tags in BD_D01_EXPECT:
            run_id = "TMP-CHECKM0-%d-%s" % (os.getpid(), tag)
            report_path = os.path.join(ROOT, "acceptance/runs", run_id + ".json")
            if os.path.exists(report_path):
                s.reasons.append("%s: 临时回执路径 %s 已存在，拒绝覆盖他人产物" % (tag, rel(report_path)))
                continue
            rc, out = run([PY, "tools/run_case.py", CASE_DIR,
                           os.path.join(CASE_DIR, fixture), "--run-id", run_id])
            s.output += "\n$ run_case.py %s (%s)\n%s" % (fixture, tag, out)
            if os.path.exists(report_path):
                created.append(report_path)

            data = _parse_run_case_json(out)
            if data is None:
                s.reasons.append("%s: run_case 未输出可解析的 JSON 摘要行（退出码 %d）" % (tag, rc))
                parts.append("%s=解析失败" % tag)
                continue
            got_status = data.get("final_status")
            got_tags = data.get("l1_fail_tags") or []
            got_unknown = data.get("l1_unknown_count")
            if rc != want_rc:
                s.reasons.append("%s: 退出码 %s ≠ 期望 %d" % (tag, rc, want_rc))
            if data.get("case_id") != "BD-D01":
                s.reasons.append("%s: case_id 实得 %r ≠ BD-D01（跑错案例）" % (tag, data.get("case_id")))
            if got_status != want_status:
                s.reasons.append("%s: 终态 %r ≠ 期望 %r" % (tag, got_status, want_status))
            # 标签集合**全等**（不是"包含"）：多冒出来的标签同样是考卷行为变了
            if sorted(got_tags) != sorted(want_tags):
                s.reasons.append("%s: FAIL 标签集实得 %s ≠ 期望 %s（全等断言，不是包含）"
                                 % (tag, sorted(got_tags), sorted(want_tags)))
            # 考卷版本与断言集合：只有把这两样钉死，"从 case.yaml 删掉几条 must_hold"
            # 才会在本步当场转红（终态与标签对此完全无感，见 BD_D01_EXPECT_ASSERTIONS 上方说明）。
            if not os.path.exists(report_path):
                s.reasons.append("%s: 回执 %s 未写盘，断言集合无从核验" % (tag, rel(report_path)))
            else:
                try:
                    with io.open(report_path, encoding="utf-8") as f:
                        full = json.load(f)
                except (OSError, ValueError) as e:
                    full = None
                    s.reasons.append("%s: 回执 %s 读不出/不是合法 JSON（%s），断言集合无从核验"
                                     % (tag, rel(report_path), e))
                if full is not None:
                    got_ver = full.get("case_version")
                    if got_ver != BD_D01_EXPECT_CASE_VERSION:
                        s.reasons.append("%s: case_version 实得 %r ≠ 基线 %r（改考卷版本 = 改回归基线，"
                                         "须与本文件常量同批改）" % (tag, got_ver, BD_D01_EXPECT_CASE_VERSION))
                    got_asserts = tuple((a.get("id"), a.get("check"), a.get("tag"))
                                        for a in (full.get("l1_assertions") or []))
                    if got_asserts != BD_D01_EXPECT_ASSERTIONS:
                        s.reasons.append(
                            "%s: 断言集合与基线不全等（顺序敏感）——实得 %d 条 %s；基线 %d 条 %s。"
                            "考卷被增删/改序时终态与标签可以纹丝不动，只有这条断言拦得住"
                            % (tag, len(got_asserts), list(got_asserts),
                               len(BD_D01_EXPECT_ASSERTIONS), list(BD_D01_EXPECT_ASSERTIONS)))
            # UNKNOWN = 检测器缺失/证据不足，按 C.4 铁律向上冒泡。它不进 l1_fail_tags，
            # 因而**不影响终态**——一个检测器被删掉，三夹具照样"终态如期"。这里单独断言 0，
            # 否则"无检测器不得判 PASS"这条铁律在本步就是空文。
            if got_unknown != 0:
                s.reasons.append("%s: l1_unknown_count=%r ≠ 0（有断言因缺检测器/证据不足冒泡为 UNKNOWN，"
                                 "而 UNKNOWN 不进 fail_tags、不改终态——不单独断言就会被终态掩盖）"
                                 % (tag, got_unknown))
            parts.append("%s=%s%s" % (tag, got_status, ("[%s]" % "、".join(got_tags)) if got_tags else ""))
    finally:
        for p in created:
            try:
                os.remove(p)
            except OSError as e:
                s.reasons.append("临时回执 %s 删除失败: %s（产物残留即污染 acceptance/runs/）" % (rel(p), e))
    s.seconds = time.monotonic() - t0
    s.summary = " / ".join(parts) + ("（PENDING_HUMAN ≠ 通过，PASS 只属 L3 人工）" if s.ok else "")
    return s


def step_schema_smoke():
    """[5/5] Schema 四例烟测：两正 + 一结构违约 + 一不可核验，逐条核验退出码与标记。

    只跑正例的烟测测不出"校验器被掏空"——一个无条件 print SCHEMA_OK / exit 0 的桩完全满足它
    （实测可复现）。负例是这一步的全部意义所在：桩化的校验器在 invalid / unverifiable 两条上必红。
    """
    s = Step("[5/5]", "Schema 四例烟测")
    t0 = time.monotonic()
    okc = 0
    # 不可核验例靠"路径不存在"成立——先确认它确实不存在，否则这一条测的就不是它该测的东西
    nx = os.path.join(ROOT, SCHEMA_NX_INSTANCE)
    if os.path.exists(nx):
        s.reasons.append("不可核验例依赖的路径 %s 竟然存在——该条断言的前提不成立，"
                         "请改用另一条确实不存在的路径（本入口不删任何文件）" % SCHEMA_NX_INSTANCE)
    for label, inst, schema, want_rc, want_mark, forbid_mark in SCHEMA_SMOKE:
        rc, out = run([PY, "tools/validate_schema.py",
                       os.path.join(ROOT, inst), os.path.join(ROOT, schema)])
        s.output += "\n$ validate_schema.py %s %s  → rc=%d\n%s" % (inst, schema, rc, out)
        bad = []
        if rc != want_rc:
            bad.append("退出码 %d ≠ 期望 %d" % (rc, want_rc))
        if want_mark not in out:
            bad.append("输出无 %s 标记（exit 码与标记必须同时成立）" % want_mark)
        if forbid_mark and forbid_mark in out:
            bad.append("输出**不应**出现 %s 标记却出现了——一个永远放行的校验器正是这样骗过烟测的"
                       % forbid_mark)
        if bad:
            s.reasons.append("%s（%s）: %s" % (label, inst, "；".join(bad)))
        else:
            okc += 1
    s.seconds = time.monotonic() - t0
    s.summary = ("%d/%d 如期（2 正 + 1 结构违约 + 1 不可核验；结构过 ≠ 内容正确）"
                 % (okc, len(SCHEMA_SMOKE)) if s.ok else "%d/%d 通过" % (okc, len(SCHEMA_SMOKE)))
    return s


# ============================ 运行态统计（不计入判绿）============================

def runmode_line():
    """冻结门运行态的红线类别统计。**只汇总不判分**：本行的任何取值都不改变 check_m0 的绿/红。"""
    rc, out = run([PY, "tools/freeze_gate.py"])
    head = "运行态红线（不计入判绿条件，仅供人读）| "
    if rc == 1:
        cats = {}
        for m in RUN_RED_ITEM_RE.finditer(out):
            cats[m.group(1)] = cats.get(m.group(1), 0) + 1
        counted = sum(cats.values())
        m = RUN_RED_TOTAL_RE.search(out)
        declared = int(m.group(1)) if m else None
        # 逐类别写实：把 110 整体标成"PENDING_BUILD 类为设计内"会让读者把另外 30 条也读成同一类，
        # "多出一类新红线当场能发现"的设计意图就落空了。基线只做说明与提示，不改判绿。
        bits, notes = [], []
        for k in sorted(cats, key=lambda x: int(x[1:])):
            n = cats[k]
            base = RUNMODE_BASELINE.get(k)
            if base is None:
                bits.append("%s×%d ⚠新类别" % (k, n))
                notes.append("%s 不在本文件 RUNMODE_BASELINE 里——运行态冒出了一类此前没有的红线，"
                             "请人工判断它是不是设计内" % k)
            elif n != base[0]:
                bits.append("%s×%d ⚠基线 %d" % (k, n, base[0]))
                notes.append("%s 实得 %d ≠ 基线 %d（%s）" % (k, n, base[0], base[1]))
            else:
                bits.append("%s×%d" % (k, n))
        line = head + "exit 1、GATE_RED %s 条：%s" % (
            declared if declared is not None else "?", "、".join(bits) or "无法归类")
        if declared is not None and declared != counted:
            line += "（⚠ 逐条计数 %d ≠ 声明 %d，统计口径对不上，按人工查看处理）" % (counted, declared)
        expl = "；".join("%s=%s" % (k, RUNMODE_BASELINE[k][1]) for k in sorted(
            RUNMODE_BASELINE, key=lambda x: int(x[1:])) if k in cats)
        if expl:
            line += "\n   类别口径 | " + expl
        for n in notes:
            line += "\n   ⚠ " + n
        return line
    if rc == 0:
        return head + ("exit 0、GATE_GREEN 0 条红线——与 M0 设计内预期不符"
                       "（20 份 Manifest 的 4 个构建版本字段本应为 PENDING_BUILD 并判红），请人工确认是谁把它填了")
    return head + "统计不可得（退出码 %d，非 0/1）——不计入判绿，但请人工查看子进程输出" % rc


# ============================ 环境证据（不计入判绿）============================

def env_lines():
    """打印本次实际使用的解释器与依赖实版，并与 requirements.txt 的钉版对照。

    为什么对照只出提示、不判红：判绿口径由五个步骤定义，依赖版本漂移会不会导致问题，
    由那五步的实跑结果回答。把版本相等本身写成红线，等于用"版本号看着对"替代"门实际跑过"。
    但**不打印就更糟**——钉版没人核对时就只是一行装饰。
    """
    code = ("import json,sys\n"
            "d={'python': sys.version.split()[0], 'exe': sys.executable}\n"
            "for mod,key in (('jsonschema','jsonschema'),('yaml','PyYAML')):\n"
            "    try:\n"
            "        d[key]=getattr(__import__(mod),'__version__','未知（模块无 __version__）')\n"
            "    except Exception as e:\n"
            "        d[key]='导入失败: %s' % e\n"
            "print(json.dumps(d, ensure_ascii=False))\n")
    rc, out = run([PY, "-c", code], timeout=120)
    try:
        d = json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return ["环境 | 探针失败（退出码 %d）：%s" % (rc, out.strip()[:200])]

    pins = {}
    try:
        with io.open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as f:
            for raw in f:
                line = raw.split("#")[0].strip()
                if "==" in line:
                    k, v = line.split("==", 1)
                    pins[k.strip().lower()] = v.strip()
    except OSError:
        pins = {}

    bits, drift = ["Python %s (%s)" % (d.get("python"), d.get("exe"))], []
    for key in ("jsonschema", "PyYAML"):
        got, pin = d.get(key), pins.get(key.lower())
        bits.append("%s %s%s" % (key, got, ("（钉 %s）" % pin) if pin else "（requirements.txt 未钉）"))
        if pin and got != pin:
            drift.append("%s 实装 %s ≠ 钉版 %s" % (key, got, pin))
    lines = ["环境 | " + " | ".join(bits)]
    if drift:
        lines.append("     ⚠ 与 requirements.txt 不一致（仅提示，不改判绿）："
                     + "；".join(drift) + "——M0 的运行证据是在钉版下取得的，换版须重跑并重出证据")
    return lines


# ============================ 主流程 ============================

def main(argv):
    args = argv[1:]
    if args in (["--help"], ["-h"]):
        sys.stdout.write(USAGE)
        return 0
    if args:
        sys.stderr.write("用法错误：check_m0.py 不接受参数（实得 %s）；判绿口径不设放宽开关。\n\n"
                         % " ".join(repr(a) for a in args))
        sys.stderr.write(USAGE)
        return 2

    print("check_m0 · M0 门禁统一入口 —— 五步顺序执行；每步同时核验退出码与输出标记（exit 0 ≠ 通过）")
    # 这行**不得**出现结论标记串：它每轮都打印，一旦含 CHECK_M0_GREEN，
    # 连一次 CHECK_M0_RED 的运行输出里都带着"绿"标记，按子串判绿的巡检会读反。
    print("诚实边界 | 五步全绿 ≠ Founder 已签字 ≠ 案例质量合格 ≠ HEAD 提交内容合格；"
          "本入口核验的是当前工作区目录树，干净 clone 一致性由 P0-6 回执证明")
    for line in env_lines():
        print(line)
    print("")

    steps = []
    for fn in (step_freeze_gate_sign, step_mutations, step_detectors, step_bd_d01, step_schema_smoke):
        s = fn()
        steps.append(s)
        print("· %s %s …… %s  %.1fs" % (s.label, s.name, "通过" if s.ok else "未通过 ← 本步红", s.seconds))
        sys.stdout.flush()

    reds = [s for s in steps if not s.ok]
    for s in reds:
        print("\n———— %s %s 未通过，逐条原因 ————" % (s.label, s.name))
        for i, r in enumerate(s.reasons, 1):
            print("  %d. %s" % (i, r))
        lines = s.output.splitlines()
        print("———— %s 子进程输出%s ————" % (s.label,
              ("（末 %d 行，共 %d 行）" % (DUMP_LIMIT, len(lines))) if len(lines) > DUMP_LIMIT else ""))
        for line in lines[-DUMP_LIMIT:]:
            print("  | %s" % line)

    print("")
    print(runmode_line())
    print("")

    gate = steps[0]
    root = getattr(gate, "root", None) or "未取到"
    head = getattr(gate, "head", None) or "未取到"
    for s in steps:
        print("%s %-4s %s | %s" % (s.label, "PASS" if s.ok else "RED", s.name, s.summary))
    attr = "ROOT=%s | HEAD=%s（转发自 freeze_gate 归属块，读自 .git，未执行 git 命令）" % (root, head)
    if reds:
        print("CHECK_M0_RED | 未通过：%s | %s" % ("、".join("%s %s" % (s.label, s.name) for s in reds), attr))
        return 1
    # 「不可追溯的绿不算绿」：HEAD 必须是 40 位 sha 才配叫 CHECK_M0_GREEN。
    # 取不到 HEAD 的情形是真实存在且合法的（非 git 工作区 / tar 出来的副本 / 早先 linked worktree
    # 解析缺陷），但那样的一行绿贴进签字包或 P0-6 回执后**无法绑定到任何提交**——它是绿，却是
    # 没有归属的绿，必须与正常绿区分开，否则贴的人看不出差别。
    # 标记串刻意不含 "CHECK_M0_GREEN" 子串：否则按子串判绿的巡检脚本照样把它读成正常绿。
    if not re.match(r"^[0-9a-f]{40}$", head or ""):
        print("CHECK_M0_UNATTRIBUTED_GREEN | 五步全绿，但 HEAD 不是 40 位 sha（实得 %r）——"
              "本行不可作为绑定提交的证据；P0-6 回执要求 HEAD 为 40 位 sha | %s" % (head, attr))
        return 0
    print("CHECK_M0_GREEN | 五步全绿 | %s" % attr)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # CI 容器落到 ascii 流编码时不炸
    except (AttributeError, ValueError):
        pass
    sys.exit(main(sys.argv))
