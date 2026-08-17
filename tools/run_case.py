#!/usr/bin/env python3
"""L1 案例 runner v0.1（C.4 三带 / C.5 判分三层）。
用法: run_case.py <case_dir> <output.json> --run-id RUN-XXXX
纪律：L1 只判 FAIL；judge_probes 只出 CLEAN/SUSPECT/UNCLEAR（未启用则 NOT_RUN）；
终态只有 FAIL / PENDING_HUMAN——PASS 只能由 L3 人工判（B.1.5 / C.5）。
P0-4 起每份回执附 provenance 块（见下）：判分逻辑与既有 11 键一字未动，只加证据溯源。"""
import argparse, datetime, hashlib, importlib.util, json, os, re, sys, yaml

# ===================== P0-4 运行证据溯源（provenance）开始 =====================
# 为什么必须有（外部审查 BLOCK-03）：一份只有 11 键的 RUN JSON 无法回答「这段 PENDING_HUMAN 是拿
# 哪一版考卷、哪一版词表、哪一版检测器、在哪个提交上跑出来的」——证据与考卷版本脱钩，词表 13→16 改了
# 也看不出回执已过期。本块只描述生成时刻的事实，取不到的一律留 null，**禁止编造版本号/哈希/词数**。
# 实现口径参照 tools/freeze_gate.py 的 read_head_commit / attribution_block：只读 .git 文件，
# **不执行任何 git 命令**；tools/coverage.py 内有同源同口径的一份（小脚本各自自包含，见 tools/README.md）。
PROVENANCE_NOTE = "证据绑定生成时刻的工作区内容；与 HEAD 的一致性由干净 clone 回执核验"
DEFAULT_LEXICON = "acceptance/detectors/forbidden_lexicon.yaml"
DETECTORS_REL = "acceptance/detectors/checks.py"


def read_head_commit(repo_root):
    """只读 .git 取当前 HEAD 提交号（**不执行任何 git 命令**）。取不到返回 None，不得伪造。

    linked worktree（`git worktree add` 出来的树）口径（本批次实测修复）：
      .git 是一行 `gitdir: <path>`，指向 <main>/.git/worktrees/<name>/。该目录里**只有 HEAD**；
      分支引用 refs/ 与 packed-refs 住在 common dir（<main>/.git/，由同目录下的 `commondir`
      文件指出）。此前只在 per-worktree 目录里找 refs，导致 worktree 上恒返回 None——
      回执里的 commit_sha 会静默变 null，整份证据失去提交指针。
      现在：HEAD 读 per-worktree 目录；ref 解析按 [per-worktree, commondir] 顺序找
      （per-worktree 优先，因为 refs/bisect 等确实是每树一份）。
    """
    gitdir = os.path.join(repo_root, ".git")
    try:
        if os.path.isfile(gitdir):               # worktree：.git 是一行 gitdir: <path>
            with open(gitdir, encoding="utf-8") as f:
                raw = f.read().split("gitdir:", 1)[1].strip()
            # 相对路径按 **repo_root** 解析，不按进程 cwd——cwd 是调用方的事，不该改变归属结论
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

    为什么必须吞掉 OSError：本函数只服务 provenance，而 provenance 只记录事实，
    绝不能成为让整轮判分崩掉的新故障源。此前它裸抛 OSError，会在 L1 判分已跑完、
    回执尚未写盘的位置炸掉整轮——判分结果连同 acceptance/runs/ 回执一起丢失。
    """
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError:
        return None
    return h.hexdigest()


def lexicon_provenance(repo_root, case):
    """词表证据：路径取案例 must_hold 里**实际引用**的那份（无引用则回落默认路径并标注 referenced_by_case=false）。
    term_count 与 acceptance/detectors/checks.py::forbidden_expression 同口径——只数 list 值键下的非空
    字符串词条，**实读实算**，不硬编码；文件缺失 / 结构异常时留 null 并写明原因（0 词与「数不出来」不是一回事）。"""
    refs = sorted({(i.get("args") or {}).get("lexicon")
                   for i in (case.get("must_hold") or []) if (i.get("args") or {}).get("lexicon")})
    rel_path = refs[0] if refs else DEFAULT_LEXICON
    blk = {"path": rel_path, "referenced_by_case": bool(refs), "sha256": None, "term_count": None}
    if len(refs) > 1:
        blk["all_referenced"] = refs
    path = os.path.join(repo_root, rel_path)
    if not os.path.exists(path):
        blk["note"] = "词表文件不存在，哈希与词数无从实算（不得填 0 充数）"
        return blk
    blk["sha256"] = sha256_file(path)
    if blk["sha256"] is None:
        blk["note"] = "词表文件存在但读取失败（权限/IO），哈希无从实算（留 null，不得填 0 充数）"
    try:                                     # provenance 只记录事实，绝不能成为让整轮判分崩掉的新故障源
        with open(path, encoding="utf-8") as f:
            lex = yaml.safe_load(f)
    except (yaml.YAMLError, OSError, UnicodeDecodeError) as e:
        blk["note"] = "词表 YAML 解析失败（%s），词数无从实算" % type(e).__name__
        return blk
    if not isinstance(lex, dict):
        blk["note"] = "词表顶层不是映射对象（实得 %s），词数无从实算" % type(lex).__name__
        return blk
    terms = [t for v in lex.values() if isinstance(v, list) for t in v if isinstance(t, str) and t.strip()]
    blk["term_count"] = len(terms)
    blk["term_count_basis"] = "实读词表现数（与 checks.forbidden_expression 同口径：只计 list 值键下的非空字符串）"
    malformed = sorted(str(k) for k, v in lex.items() if not isinstance(v, list))
    if malformed:
        blk["malformed_keys"] = malformed
    return blk


def docstring_version(doc):
    """从模块 docstring 首行取版本 token（v0.1 / v1.2.3）。取不到返回 None，不得替它编一个。"""
    first = (doc or "").strip().splitlines()
    m = re.search(r"v\d+(?:\.\d+)+", first[0]) if first else None
    return m.group(0) if m else None


def provenance_block(repo_root, checks_mod, case):
    """一份运行回执的溯源块。诚实边界：commit_sha 只说明 repo_root 当前的提交指针，
    **本块描述的是工作区内容**，两者是否一致由干净 clone 回执（P0-6）证明，不由本块证明。"""
    detectors_path = os.path.join(repo_root, DETECTORS_REL)
    self_path = os.path.abspath(__file__)
    return {
        "commit_sha": read_head_commit(repo_root),
        # 生成器自身的版本与哈希：判分结果是**这份脚本**的解析/判分逻辑产出的，
        # 脚本换了而 B 原文/词表/检测器都没换时，回执里若看不出生成器变过，
        # 同一批输入得出不同结论就无从解释（同源补齐见 tools/coverage.py）。
        "generator": {"path": os.path.relpath(self_path, repo_root),
                      "sha256": sha256_file(self_path)},
        "commit_sha_source": ".git/HEAD + refs/packed-refs（读文件，未执行 git 命令）",
        "repo_root": os.path.realpath(repo_root),
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "python_version": sys.version.split()[0],
        "deps": dep_versions(),
        "argv": list(sys.argv),
        "lexicon": lexicon_provenance(repo_root, case),
        "detectors_version": docstring_version(getattr(checks_mod, "__doc__", "")),
        "detectors_sha256": sha256_file(detectors_path) if os.path.exists(detectors_path) else None,
        "detectors_path": DETECTORS_REL,
        "note": PROVENANCE_NOTE,
    }
# ===================== P0-4 运行证据溯源（provenance）结束 =====================


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
        # tag 一律落进回执（此前只在 FAIL 时落）。判分语义一字未动——tag 仍只在 FAIL 时进
        # l1_fail_tags、仍只有 FAIL 改终态。加它是为了让回执**自证本轮跑了哪几条断言、
        # 各自绑定哪个失败标签**：考卷里删掉几条 must_hold 时，终态与标签都可以纹丝不动，
        # 只有 (id, check, tag) 有序集合进了回执，下游回归（tools/check_m0.py [4/5]）才拦得住。
        tag = item.get("tag")
        rec = {"id": item["id"], "check": item["check"], "tag": tag,
               "verdict": verdict, "detail": detail}
        if verdict == "FAIL":
            if tag is None:                  # 判 FAIL 却无标签：考卷格式错误，不静默放过
                print(f"REJECT [考卷格式] must_hold {item['id']} 判 FAIL 但 case.yaml 未给 tag——"
                      f"无标签的失败结果无法进 l1_fail_tags，判分留痕不成立"); sys.exit(2)
            fails.append(rec)
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
    report["provenance"] = provenance_block(repo_root, checks, case)   # P0-4：只加证据，不参与判分
    out_path = os.path.join(repo_root, "acceptance/runs", a.run_id + ".json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: report[k] for k in ["run_id", "case_id", "l1_fail_tags", "l1_unknown_count", "final_status"]}, ensure_ascii=False))
    sys.exit(1 if fails else 0)

if __name__ == "__main__": main()
