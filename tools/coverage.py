#!/usr/bin/env python3
"""检测覆盖率 v0.1（C.4 规格边界：四视图+知识卡池；只读元数据、只汇总不推导；不建 UI/库/趋势/通知）。
铁律2：禁止结果分母每次从 B 原文现数，禁止硬编码。用法: coverage.py [--init-registry]
P0-4 起报告附 provenance 块（见下）：四视图口径与统计逻辑一字未动，只加证据溯源。"""
import ast, datetime, hashlib, os, re, sys, json, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B_PATH = os.path.join(ROOT, "B_三个核心模块智能验收合同.md")
REG_PATH = os.path.join(ROOT, "acceptance/detectors/prohibited_registry.yaml")
CASE_RE = re.compile(r"^### ((?:INT|BD|CR|SYS)-D\d{2}|E2E-\d{2})｜(.+)$")
STATES = ["deterministic", "llm_assisted", "human_required", "not_detectable_declared"]

# ===================== P0-4 运行证据溯源（provenance）开始 =====================
# 为什么必须有（外部审查 BLOCK-03）：一份覆盖率报告不说明它读的是哪一版 B 原文、哪一版注册表、
# 在哪个提交上生成，「分母 58 / deterministic 3」就无法与考卷版本绑定，报告过期也看不出来。
# 取不到的一律留 null，**禁止编造版本号/哈希**。实现口径参照 tools/freeze_gate.py 的
# read_head_commit / attribution_block：只读 .git 文件，**不执行任何 git 命令**；
# tools/run_case.py 内有同源同口径的一份（小脚本各自自包含，见 tools/README.md）。
PROVENANCE_NOTE = "证据绑定生成时刻的工作区内容；与 HEAD 的一致性由干净 clone 回执核验"
DETECTORS_REL = "acceptance/detectors/checks.py"


def read_head_commit(repo_root):
    """只读 .git 取当前 HEAD 提交号（**不执行任何 git 命令**）。取不到返回 None，不得伪造。

    linked worktree（`git worktree add` 出来的树）口径（本批次实测修复）：
      .git 是一行 `gitdir: <path>`，指向 <main>/.git/worktrees/<name>/。该目录里**只有 HEAD**；
      分支引用 refs/ 与 packed-refs 住在 common dir（<main>/.git/，由同目录下的 `commondir`
      文件指出）。此前只在 per-worktree 目录里找 refs，导致 worktree 上恒返回 None——
      报告里的 commit_sha 会静默变 null，整份证据失去提交指针。
      现在：HEAD 读 per-worktree 目录；ref 解析按 [per-worktree, commondir] 顺序找。
    """
    gitdir = os.path.join(repo_root, ".git")
    try:
        if os.path.isfile(gitdir):               # worktree：.git 是一行 gitdir: <path>
            with open(gitdir, encoding="utf-8") as f:
                raw = f.read().split("gitdir:", 1)[1].strip()
            # 相对路径按 **repo_root** 解析，不按进程 cwd
            gitdir = raw if os.path.isabs(raw) else os.path.normpath(os.path.join(repo_root, raw))
        if not os.path.isdir(gitdir):
            return None
        search_dirs = [gitdir]
        cpath = os.path.join(gitdir, "commondir")
        if os.path.isfile(cpath):
            with open(cpath, encoding="utf-8") as f:
                c = f.read().strip()
            if c:
                common = c if os.path.isabs(c) else os.path.normpath(os.path.join(gitdir, c))
                if os.path.isdir(common) and os.path.realpath(common) != os.path.realpath(gitdir):
                    search_dirs.append(common)
        with open(os.path.join(gitdir, "HEAD"), encoding="utf-8") as f:
            head = f.read().strip()
        if not head.startswith("ref:"):
            return head
        ref = head.split(" ", 1)[1].strip()
        for d in search_dirs:
            refpath = os.path.join(d, ref)
            if os.path.exists(refpath):
                with open(refpath, encoding="utf-8") as f:
                    return f.read().strip()
        for d in search_dirs:
            packed = os.path.join(d, "packed-refs")
            if os.path.exists(packed):
                with open(packed, encoding="utf-8") as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) == 2 and parts[1] == ref:
                            return parts[0]
    except (OSError, UnicodeDecodeError, IndexError):
        return None
    return None


def dep_versions():
    """依赖实版：优先包元数据，其次已导入模块的 __version__；两条都取不到就留 null（禁编造）。"""
    out = {}
    for dist, mod in (("jsonschema", "jsonschema"), ("PyYAML", "yaml")):
        v = None
        try:
            from importlib import metadata
            v = metadata.version(dist)
        except Exception:
            v = None
        if v is None:
            m = sys.modules.get(mod)
            v = getattr(m, "__version__", None) if m is not None else None
        out[dist] = v
    return out


def sha256_file(path):
    """文件哈希。读不到（权限/IO 错误）返回 None——**留 null 是诚实，不得填 0 或空串充数**。

    provenance 只记录事实，绝不能成为让整轮统计崩掉的新故障源；此前它裸抛 OSError。
    """
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError:
        return None
    return h.hexdigest()


def detectors_version():
    """从 acceptance/detectors/checks.py 的模块 docstring 首行取版本 token（**不导入该模块**，
    只做 ast 解析——覆盖率脚本不跑检测器，不该因取版本而执行考卷区代码）。取不到返回 None。"""
    path = os.path.join(ROOT, DETECTORS_REL)
    if not os.path.exists(path):
        return None
    try:
        doc = ast.get_docstring(ast.parse(open(path, encoding="utf-8").read())) or ""
    except (OSError, SyntaxError, UnicodeDecodeError):
        return None
    first = doc.strip().splitlines()
    m = re.search(r"v\d+(?:\.\d+)+", first[0]) if first else None
    return m.group(0) if m else None


def docstring_version_of_self():
    """本脚本 docstring 首行里的版本 token（如 v0.1）。取不到返回 None，不得替它编一个。"""
    first = (__doc__ or "").strip().splitlines()
    m = re.search(r"v\d+(?:\.\d+)+", first[0]) if first else None
    return m.group(0) if m else None


def provenance_block():
    """报告的溯源块。诚实边界：commit_sha 只说明 ROOT 当前的提交指针，**本块描述的是工作区内容**，
    两者是否一致由干净 clone 回执（P0-6）证明，不由本块证明。"""
    detectors_path = os.path.join(ROOT, DETECTORS_REL)
    self_path = os.path.abspath(__file__)
    return {
        "commit_sha": read_head_commit(ROOT),
        # 生成器自身的版本与哈希（本批次补齐）：「分母 58 / deterministic 3」这些数字是**本脚本的
        # 解析口径**产出的——解析口径一变，同一份 B 原文可以得出不同分母，而此前报告里看不出脚本换过。
        # B 原文 / 注册表 / 检测器都记了 sha256，唯独漏了算它们的那把尺子（同源补齐见 tools/run_case.py）。
        "generator": {"path": os.path.relpath(self_path, ROOT),
                      "version": docstring_version_of_self(),
                      "sha256": sha256_file(self_path)},
        "commit_sha_source": ".git/HEAD + refs/packed-refs（读文件，未执行 git 命令）",
        "repo_root": os.path.realpath(ROOT),
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "python_version": sys.version.split()[0],
        "deps": dep_versions(),
        "argv": list(sys.argv),
        "sources": {
            "B_contract": {"path": os.path.relpath(B_PATH, ROOT),
                           "sha256": sha256_file(B_PATH) if os.path.exists(B_PATH) else None},
            "prohibited_registry": {"path": os.path.relpath(REG_PATH, ROOT),
                                    "sha256": sha256_file(REG_PATH) if os.path.exists(REG_PATH) else None},
        },
        "detectors_version": detectors_version(),
        "detectors_sha256": sha256_file(detectors_path) if os.path.exists(detectors_path) else None,
        "detectors_path": DETECTORS_REL,
        "note": PROVENANCE_NOTE,
    }
# ===================== P0-4 运行证据溯源（provenance）结束 =====================

def parse_b():
    cases, prohibited, cur = [], {}, "B-GENERAL"
    lines = open(B_PATH, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines):
        m = CASE_RE.match(lines[i])
        if m: cur = m.group(1); cases.append((cur, m.group(2).strip()))
        if lines[i].strip().startswith("**禁止结果"):
            i += 1; bullets = []
            while i < len(lines) and (lines[i].startswith("- ") or not lines[i].strip()):
                if lines[i].startswith("- "): bullets.append(lines[i][2:].strip("；。 "))
                i += 1
            prohibited.setdefault(cur, []).extend(bullets)
            continue
        i += 1
    return cases, prohibited

def live_keys(prohibited):
    return {f"{cid}#{n+1}": txt for cid, blts in prohibited.items() for n, txt in enumerate(blts)}

def main():
    cases, prohibited = parse_b()
    keys = live_keys(prohibited)
    denominator = len(keys)
    if "--init-registry" in sys.argv:
        if os.path.exists(REG_PATH): print(f"注册表已存在，拒绝覆盖: {REG_PATH}"); sys.exit(2)
        reg = {k: {"status": "human_required", "text": t} for k, t in keys.items()}
        with open(REG_PATH, "w", encoding="utf-8") as f:
            f.write("# 禁止结果检测注册表（C.4 铁律1：每条挂 deterministic:<ID>/llm_assisted:<ID>/human_required/not_detectable_declared）\n")
            f.write("# 后两种状态下该项结果只能是 PENDING_HUMAN。本文件属考卷区，改状态=改考卷。\n")
            yaml.safe_dump(reg, f, allow_unicode=True, sort_keys=True)
        print(f"注册表初始化：{denominator} 条，全部 human_required（诚实基线）"); return
    reg = yaml.safe_load(open(REG_PATH, encoding="utf-8")) if os.path.exists(REG_PATH) else {}
    drift = sorted(set(keys) ^ set(reg))
    dist = {s: sum(1 for v in reg.values() if v.get("status") == s) for s in STATES}
    exec_cases = {}
    for cid, _ in cases:
        cy = os.path.join(ROOT, "acceptance/cases", cid, "case.yaml")
        if os.path.exists(cy):
            c = yaml.safe_load(open(cy, encoding="utf-8"))
            exec_cases[cid] = {"must_hold": len(c.get("must_hold", [])), "judge_probes": len(c.get("judge_probes", [])), "human_questions": len(c.get("human_questions", [])), "dimensions": c.get("dimensions")}
    card_pool = [f for f in os.listdir(os.path.join(ROOT, "acceptance/candidates/elicitation")) if not f.startswith(".")]
    gates_path = os.path.join(ROOT, "acceptance/gates.yaml")
    L = []
    L.append("# 检测覆盖率报告（诚实基线——完整性仪表，不是能力证明；能力成立只由 B.8 闸门判定）\n")
    L.append(f"分母（脚本自 B 原文现数，禁止硬编码）：**{denominator} 条禁止结果**，分布于 {len(prohibited)} 个案例段\n")
    L.append("## 运行证据溯源（provenance，P0-4）\n")
    L.append("本报告的全部数字来自下述提交指针所在工作区的**当时内容**；取不到的字段留 `null`（不编造）。\n")
    L.append("```json\n" + json.dumps(provenance_block(), ensure_ascii=False, indent=2) + "\n```\n")
    L.append(f"## 视图1｜案例视角（{len(cases)} 条锁定案例 × 执行文件落地）\n")
    L.append("| 案例 | 执行文件 | 断言 | 探针 | 人工问题引用 |")
    L.append("|---|---|---|---|---|")
    for cid, title in cases:
        e = exec_cases.get(cid)
        L.append(f"| {cid}｜{title} | {'✅' if e else '未落地'} | {e['must_hold'] if e else '—'} | {e['judge_probes'] if e else '—'} | {e['human_questions'] if e else '—'} |")
    L.append(f"\n执行文件落地：{len(exec_cases)}/{len(cases)}\n")
    L.append("## 视图2｜禁止结果视角（检测器四态）\n")
    L.append("| 状态 | 条数 | 占比 |")
    L.append("|---|---|---|")
    for s in STATES:
        L.append(f"| {s} | {dist.get(s,0)} | {dist.get(s,0)*100//denominator if denominator else 0}% |")
    L.append(f"\n确定性/探针覆盖合计：{dist.get('deterministic',0)+dist.get('llm_assisted',0)}/{denominator}（其余全部 PENDING_HUMAN，绝不自动 PASS）\n")
    if drift: L.append(f"⚠️ 注册表漂移（live 分母与注册表键不一致，需人工对账）：{drift}\n")
    L.append("## 视图3｜维度视角（案例声明制，脚本不推导）\n")
    dims = {cid: e["dimensions"] for cid, e in exec_cases.items() if e.get("dimensions")}
    L.append(f"{len(dims)} 条案例声明了维度" + (f"：{dims}" if dims else "（暂无；案例落地时自行声明）") + "\n")
    L.append("## 视图4｜闸门视角（Gate 声明制）\n")
    if os.path.exists(gates_path):
        L.append("```\n" + open(gates_path, encoding="utf-8").read() + "```\n")
    else:
        L.append("IA-0 ~ IA-4：前置案例清单未声明（gates.yaml 待 IA 准备时落，真源 B.8）\n")
    L.append("## 附加指标｜知识卡池长度（E.3）\n")
    L.append(f"acceptance/candidates/elicitation/：**{len(card_pool)} 张**（持续增长不清空 = 第四个经验库早期信号）\n")
    report = "\n".join(L)
    out = os.path.join(ROOT, "acceptance/runs/coverage_report.md")
    open(out, "w", encoding="utf-8").write(report)
    print(report.split("## 视图1")[0])
    print(f"[视图2] " + ", ".join(f"{s}={dist.get(s,0)}" for s in STATES) + f" / 分母 {denominator}")
    print(f"[视图1] 执行文件 {len(exec_cases)}/{len(cases)}  [知识卡池] {len(card_pool)}  [漂移] {len(drift)}")
    print(f"报告已存: {os.path.relpath(out, ROOT)}")

if __name__ == "__main__": main()
