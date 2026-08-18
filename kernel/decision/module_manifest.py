#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 资产⑦：模块清单生成器。

【M2-EP01 提前段·非正式证据】

手改 module_manifest.json 无效，只认本生成器：`--check` 会重新生成一份（不写盘）逐键比对，
不一致即报 STALE——检查器不该在检查过程中把被检查对象改成合格的样子。

诚实边界（本清单**不**代表什么，别把它当合规图章）：
  ① input_schema 只声明入参契约是哪份文件，不代表运行时对上游 plan 做过全量校验
     （输入闸只查放行信号与自洽性，见 preprocess 诚实边界③）；
  ② source_sha256 覆盖 kernel/decision 的 *.py 与 prompts/*.md（glob，不写死清单、不设排除名单——
     排除名单本身就是隐身通道）；换 fixtures 回放夹具**不会**改指纹，改自测口径**会**改指纹；
  ③ 不覆盖 contracts/ 与 acceptance/ 的指纹——那是 tools/freeze_gate.py 的职责，
     本文件不复制它、也不假装等价。

用法：
  python3 -m kernel.decision.module_manifest                     # 生成并写盘（取时钟，stderr 留痕）
  python3 -m kernel.decision.module_manifest --generated-at ISO  # 确定性注入时间
  python3 -m kernel.decision.module_manifest --check             # 与盘上清单比对，0=同步 1=STALE 2=错误
"""

import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

from .config import (
    KERNEL_DECISION_DIR,
    MODULE_MANIFEST_PATH,
    MODULE_NAME,
    MODULE_VERSION,
    PROMPT_STEP1_PATH,
    PROMPT_STEP2_PATH,
    PROMPT_STEP3_PATH,
    SCHEMA_BUSINESS_DECISION_BUNDLE,
    SCHEMA_INTENT_EXECUTION_PLAN,
)

# 分步结构如实声明：三步 LLM + 确定性段（C.3 BD 分步裁决）。可 grep 的落点。
# 规则评估与 BLOCK 隔离在 step3 **之前**（step3 只见存活候选——step3 prompt 的
# 「已过确定性规则评估」陈述以此为真），顺序按 runner 实际时序逐段照抄。
STEP_STRUCTURE = (
    "deterministic_preprocess_and_input_gates",
    "llm_step1_conflict_recognition",
    "llm_step2_candidate_generation",
    "deterministic_rules_evaluation_and_block_isolation",
    "llm_step3_tradeoff_evaluation",
    "deterministic_assembly",
    "deterministic_postcheck_preflight",
)

_VOLATILE_KEYS = ("generated_at",)
# 结论标记串：绝不写进 argparse 的 help 文本（--help 会把它打出来，按子串判绿的调用方被骗过）
_MARK_WRITTEN = "DECISION_MANIFEST_WRITTEN"
_MARK_IN_SYNC = "DECISION_MANIFEST_IN_SYNC"
_MARK_STALE = "DECISION_MANIFEST_STALE"


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:   # 按二进制读：文本模式的换行归一会让指纹依赖平台
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _source_fingerprints():
    patterns = (os.path.join(KERNEL_DECISION_DIR, "*.py"),
                os.path.join(KERNEL_DECISION_DIR, "prompts", "*.md"))
    files = sorted(p for pattern in patterns for p in glob.glob(pattern))
    if not files:
        raise RuntimeError("指纹扫描 0 个文件——glob 与目录结构脱节，拒绝生成空清单")
    out = {}
    for path in files:
        rel = os.path.relpath(path, KERNEL_DECISION_DIR).replace(os.sep, "/")
        out[rel] = _sha256_file(path)
    return out


def _prompt_version(path):
    """复用 runner.load_prompt 而不是自己再写一遍解析（同一事实只许有一个落点）。"""
    from . import runner   # 局部 import：避免生成器把整条依赖链拉起
    return runner.load_prompt(path)[1]


def _schema_tag(path):
    with open(path, encoding="utf-8") as f:
        schema = json.load(f)
    schema_id = schema.get("$id") or os.path.basename(path)
    version = schema.get("version")
    if version:
        return f"{schema_id}@{version}"
    return f"{schema_id}@UNVERSIONED(sha256:{_sha256_file(path)[:12]})"


def generate(generated_at=None, write=True, path=None):
    if generated_at is None:
        generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(f"[decision.manifest] 未注入 --generated-at，取当前时钟 {generated_at}", file=sys.stderr)
    manifest = {
        "module": MODULE_NAME,
        "module_version": MODULE_VERSION,
        "segment": "M2-EP01 提前段·非正式证据",
        "prompt_versions": {
            "step1": _prompt_version(PROMPT_STEP1_PATH),
            "step2": _prompt_version(PROMPT_STEP2_PATH),
            "step3": _prompt_version(PROMPT_STEP3_PATH),
        },
        "output_schema": _schema_tag(SCHEMA_BUSINESS_DECISION_BUNDLE),
        "input_schema": os.path.basename(SCHEMA_INTENT_EXECUTION_PLAN),
        "step_structure": list(STEP_STRUCTURE),
        "generated_at": generated_at,
        "source_sha256": _source_fingerprints(),
    }
    if write:
        target = path or MODULE_MANIFEST_PATH
        with open(target, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return manifest


def diff_against_disk(path=None):
    """重新生成（不写盘）并与盘上清单逐键比对（忽略 generated_at）。返回差异键清单。"""
    target = path or MODULE_MANIFEST_PATH
    with open(target, encoding="utf-8") as f:
        on_disk = json.load(f)
    fresh = generate(generated_at="__check__", write=False)
    diffs = []
    for key in set(on_disk) | set(fresh):
        if key in _VOLATILE_KEYS:
            continue
        if on_disk.get(key) != fresh.get(key):
            diffs.append(key)
    return sorted(diffs)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python3 -m kernel.decision.module_manifest",
        description="生成/校验 kernel/decision 模块清单。--check 只比对不写盘。",
    )
    parser.add_argument("--generated-at", default=None, help="确定性注入生成时间（ISO8601）")
    parser.add_argument("--check", action="store_true", help="与盘上清单比对，不写盘")
    args = parser.parse_args(argv)
    try:
        if args.check:
            diffs = diff_against_disk()
            if diffs:
                print(f"{_MARK_STALE} 差异键：{diffs}")
                return 1
            print(_MARK_IN_SYNC)
            return 0
        generate(generated_at=args.generated_at)
        print(_MARK_WRITTEN)
        return 0
    except Exception as e:
        print(f"[decision.manifest] 失败（{type(e).__name__}）：{e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
