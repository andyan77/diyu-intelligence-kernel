#!/usr/bin/env python3
"""L1 案例 runner v0.1（C.4 三带 / C.5 判分三层）。
用法: run_case.py <case_dir> <output.json> --run-id RUN-XXXX
纪律：L1 只判 FAIL；judge_probes 只出 CLEAN/SUSPECT/UNCLEAR（未启用则 NOT_RUN）；
终态只有 FAIL / PENDING_HUMAN——PASS 只能由 L3 人工判（B.1.5 / C.5）。"""
import argparse, importlib.util, json, os, sys, yaml

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("case_dir"); ap.add_argument("output"); ap.add_argument("--run-id", required=True)
    a = ap.parse_args()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case = yaml.safe_load(open(os.path.join(a.case_dir, "case.yaml"), encoding="utf-8"))
    lock = os.path.join(repo_root, "acceptance/locks", case["case_id"] + ".lock")
    if os.path.exists(lock):
        print(f"REJECT [C.6 熔断锁] {lock} 存在，解锁走 B.8.1 三条路"); sys.exit(2)
    output = json.load(open(a.output, encoding="utf-8"))
    snap_path = os.path.join(a.case_dir, case.get("fixtures", {}).get("context_snapshot", ""))
    ctx = {"repo_root": repo_root, "output_path": os.path.abspath(a.output),
           "output_schema": os.path.join(repo_root, case["output_schema"]) if case.get("output_schema") else None,
           "snapshot": json.load(open(snap_path, encoding="utf-8")) if os.path.exists(snap_path) else None}
    spec = importlib.util.spec_from_file_location("checks", os.path.join(repo_root, "acceptance/detectors/checks.py"))
    checks = importlib.util.module_from_spec(spec); spec.loader.exec_module(checks)
    results, fails, unknowns = [], [], []
    for item in case["must_hold"]:
        fn = getattr(checks, item["check"], None)
        if fn is None:
            verdict, detail = "UNKNOWN", f"检测器 {item['check']} 不存在（无检测器不得判过）"
        else:
            verdict, detail = fn(output, ctx, **(item.get("args") or {}))
        rec = {"id": item["id"], "check": item["check"], "verdict": verdict, "detail": detail}
        if verdict == "FAIL": rec["tag"] = item["tag"]; fails.append(rec)
        if verdict == "UNKNOWN": unknowns.append(rec)
        results.append(rec)
    final = "FAIL" if fails else "PENDING_HUMAN"
    report = {"run_id": a.run_id, "case_id": case["case_id"], "case_version": case["case_version"],
              "contract_ref": case["contract_ref"], "output_file": os.path.relpath(a.output, repo_root),
              "l1_assertions": results, "l1_fail_tags": sorted({f["tag"] for f in fails}),
              "l1_unknown_count": len(unknowns),
              "judge_probes": [{"id": p["id"], "verdict": "NOT_RUN", "status": p.get("status", "wired_not_run")} for p in case.get("judge_probes", [])],
              "final_status": final,
              "note": "L1 只判 FAIL；PENDING_HUMAN ≠ 通过；PASS 只能由 L3 人工判（C.5 / B.1.5）"}
    out_path = os.path.join(repo_root, "acceptance/runs", a.run_id + ".json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: report[k] for k in ["run_id", "case_id", "l1_fail_tags", "l1_unknown_count", "final_status"]}, ensure_ascii=False))
    sys.exit(1 if fails else 0)

if __name__ == "__main__": main()
