#!/usr/bin/env python3
"""检测覆盖率 v0.1（C.4 规格边界：四视图+知识卡池；只读元数据、只汇总不推导；不建 UI/库/趋势/通知）。
铁律2：禁止结果分母每次从 B 原文现数，禁止硬编码。用法: coverage.py [--init-registry]"""
import os, re, sys, json, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B_PATH = os.path.join(ROOT, "B_三个核心模块智能验收合同.md")
REG_PATH = os.path.join(ROOT, "acceptance/detectors/prohibited_registry.yaml")
CASE_RE = re.compile(r"^### ((?:INT|BD|CR|SYS)-D\d{2}|E2E-\d{2})｜(.+)$")
STATES = ["deterministic", "llm_assisted", "human_required", "not_detectable_declared"]

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
    L.append("## 视图1｜案例视角（14 条锁定案例 × 执行文件落地）\n")
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
