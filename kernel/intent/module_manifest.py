#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""资产⑦ 模块清单生成器 → kernel/intent/module_manifest.json。

**手改 module_manifest.json 无效，只认本生成器。**
这句话不是口号，是有执行面的：`python3 -m kernel.intent.module_manifest --check` 会重新算一遍
（除 `generated_at` 外逐字段比对），手改过的 json 当场判 STALE。理由——清单里最有价值的字段是
`source_sha256`（模块每份源文件的内容指纹）与 `prompt_version`；这两样一旦允许手填，清单就从
「模块现在长什么样」退化成「有人曾经声称它长什么样」，跨轮回看时无法区分二者，属典型假绿。

为什么需要这份清单（C.3 资产⑦ 的用途，不是为了"整洁"）：
  一次 Intent 运行出问题时，第一个要回答的问题是「当时跑的是哪一版模块、哪一版 Prompt、
  对着哪一版输出契约」。运行产物 IntentExecutionPlan 里只带 artifact.schema_version 一个版本号，
  回答不了前两问。本清单把这三件事在同一时刻钉到一起，且全部由代码从真源现算，无人工转录环节。

真源指针（按小节名书写、不锁行号——同 tools/freeze_gate.py 与 config.py 的纪律，行号会漂移）：
  · 本文件产出的键集与 step_structure 取值 ← M1-EP02 kernel/intent 接口规格「module_manifest.py」行
  · module / module_version                 ← kernel/intent/config.py（MODULE_NAME / MODULE_VERSION，唯一落点）
  · prompt_version                          ← prompts/intent_v0.1.md 文件头 YAML，**经 runner.load_prompt 读**
                                              （同一份解析逻辑只许有一处，见 read_prompt_version 注释）
  · output_schema / input_schema            ← contracts/schemas/*.schema.json 的 $id

诚实边界（本清单**不**代表什么，别把它当合规图章）：
  ① `input_schema: context_snapshot.schema.json` 只是**声明本模块的入参契约是哪一份**，
     不代表运行时真的按它校验过——preprocess.load_snapshot 明确不做 Schema 校验（M0 扁平夹具与
     A.4.3 引用式结构存在形状差，属 OD 级裁决，见该函数文档串）。清单里出现这个文件名，
     绝不等于「快照已合规」。
  ② `source_sha256` 覆盖 kernel/intent/ 下**所有** `*.py`（含 `test_intent_offline.py`）与 `prompts/*.md`，
     `fixtures/` 的 .json/.txt 不在射程内。这里刻意**不设任何排除名单**——排除名单本身就是隐身通道
     （"这个文件不算数"是可以被人后补上去的）；夹具恰好不属这两类，所以不需要特判。
     由此产生两条可预期的行为：换一份 replay 夹具不改模块指纹；改自测口径会改模块指纹——
     后者是有意的，自测口径变了，「这个模块被验到什么程度」就跟着变了。
  ③ 清单不覆盖 contracts/ 与 acceptance/ 的内容指纹（那是冻结门 tools/freeze_gate.py 的职责，
     本文件不复制它、也不假装等价）；只在 output_schema 串里带一段输出契约的内容哈希，见 _schema_pin。

用法（不接受除下列以外的参数）：
  python3 -m kernel.intent.module_manifest                      # 生成并写盘（generated_at 取运行时钟）
  python3 -m kernel.intent.module_manifest --generated-at <ISO> # 生成并写盘（时间戳由调用方给定，可复现）
  python3 -m kernel.intent.module_manifest --check              # 只比对，不写盘
退出码：0 = 写成 / 已同步；1 = --check 判定与代码不同步（含 json 缺失）；2 = 用法或 I/O 错误
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

from kernel.intent.config import (
    KERNEL_INTENT_DIR,
    MODULE_MANIFEST_PATH,
    MODULE_NAME,
    MODULE_VERSION,
    SCHEMA_CONTEXT_SNAPSHOT,
    SCHEMA_INTENT_EXECUTION_PLAN,
)

# C.3 形态裁决的三段式，逐字照抄接口规格「module_manifest.py」行给的取值。
# 写成常量而不是在 generate() 里内联，是为了让"这个模块声称自己是几步"有一个可 grep 的落点：
# 将来若有人往 llm.py 里偷偷加第二次调用（那就是 2 步 LLM，形态变了），这里不改 = 清单与实现不符，
# 属可被人看见的矛盾；内联在函数里则连找都不好找。
STEP_STRUCTURE = (
    "deterministic_preprocess",
    "llm_single_step",
    "deterministic_postcheck_preflight",
)

# 纳入内容指纹的文件（相对 kernel/intent/）。用 glob 而不是写死文件清单：
# 写死清单时，新增一个 .py 若忘了登记，指纹照算不误、看着一切正常——那是"覆盖面静默缩水"。
# glob 的代价是顺序不稳定，故下面一律 sorted() 后再入表。
_SOURCE_GLOBS = ("*.py", "prompts/*.md")

# --check 比对时忽略的键：只有它一个。generated_at 记的是"这份清单什么时候生成的"，
# 每次重生成必然不同；把它算进比对，--check 会永远判 STALE，检查器随即失去意义。
_VOLATILE_KEYS = ("generated_at",)

# 结论标记串（只在真实结论那一行打印，绝不写进 argparse 的 help 文本——
# tools/validate_schema.py 踩过的坑：--help 把标记打出来，按子串判绿的调用方被骗过）。
_MARK_WRITTEN = "MODULE_MANIFEST_WRITTEN"
_MARK_IN_SYNC = "MODULE_MANIFEST_IN_SYNC"
_MARK_STALE = "MODULE_MANIFEST_STALE"


def _sha256_of_file(path):
    """一份文件的 sha256（十六进制全长）。

    按二进制读、不按文本读：文本模式会做换行转换，同一份文件在不同平台上算出两个哈希，
    指纹就不再是指纹了。
    """
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_source_sha256(base_dir=None):
    """逐文件算内容指纹，返回 {相对路径: sha256}（键按相对路径排序）。

    路径分隔符统一成 "/"：Windows 上 os.path.join 给的是反斜杠，落进 json 后与 Linux 上生成的
    同一份清单逐字节不同，--check 会误判 STALE——那是环境差异冒充内容差异。
    """
    base = base_dir or KERNEL_INTENT_DIR
    found = {}
    for pattern in _SOURCE_GLOBS:
        for path in glob.glob(os.path.join(base, *pattern.split("/"))):
            if not os.path.isfile(path):
                continue
            rel = os.path.relpath(path, base).replace(os.sep, "/")
            found[rel] = _sha256_of_file(path)
    if not found:
        # fail-loud：一个源文件都没扫到，多半是 base_dir 传错或模块被搬走。
        # 此时若照常写出一份 source_sha256 为空的清单，它看起来完全正常——那是最难查的一类假绿。
        raise RuntimeError(
            "kernel/intent 下没有扫到任何 %s，模块指纹无从生成（base_dir=%s）" % (list(_SOURCE_GLOBS), base)
        )
    return {k: found[k] for k in sorted(found)}


def read_prompt_version():
    """取 prompts/intent_v0.1.md 文件头的 prompt_version。

    **刻意复用 runner.load_prompt 而不是在这里再写一遍 YAML 文件头解析**：
    清单要回答的是「这次运行用的是哪版 Prompt」，那就必须与 runner 真正读到的那个值同源。
    自己另写一份解析，两处对同一份文件头的读法一旦分叉（比如一处认 `---` 分隔、一处认别的），
    清单就会记下一个运行时根本没用过的版本号，而且没有任何检测器会喊。
    代价是本模块因此依赖 runner 的 import 链（yaml / jsonschema），这在本仓已是既有依赖，不新增。
    """
    from kernel.intent import runner   # 局部 import：只有真要读版本时才拉起 runner 的依赖链
    _body, version = runner.load_prompt()
    return version


def _schema_pin(path):
    """把一份 JSON Schema 钉成 "<$id>@<版本>" 形式的字符串。

    接口规格写的是 `intent_execution_plan.schema.json@<其 $id/版本>`。实测（本轮）：
    contracts/schemas/intent_execution_plan.schema.json 只有 $schema / $id / title / $comment 四个顶层元键，
    **没有声明任何版本号**（该缺口已登记为 OQ-INT-D01-05，不是本文件能自决的事）。

    于是两条路：编一个版本号（比如照 20 份 Case Manifest 的 output_schema_version 写死 "v0.1"），
    或者如实说"没有声明版本"。这里选后者，并用内容哈希前 12 位代替版本位：
      · 编版本号的代价：契约文件被改而版本位不变时，清单仍显示 v0.1——它会主动说谎；
      · 内容哈希的代价：契约一改清单就变，重生成时会产生 diff——那正是应该被看见的 diff。
    版本位一旦在契约里正式声明，把这里改成读那个字段即可，形态不用动。
    """
    with open(path, encoding="utf-8") as fh:
        schema = json.load(fh)
    identifier = schema.get("$id") or os.path.basename(path)
    declared = schema.get("version")
    if declared:
        return "%s@%s" % (identifier, declared)
    return "%s@UNVERSIONED(sha256:%s)" % (identifier, _sha256_of_file(path)[:12])


def _now_utc_iso():
    """当前 UTC 时间的 ISO8601 串（秒级，带 Z）。只在调用方没给 generated_at 时用。"""
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def generate(generated_at=None, write=True, path=None):
    """生成 module_manifest 内容并（默认）写盘，返回该 dict。

    接口规格钉死的签名是 `generate()->dict`，故三个参数全部有默认值，`generate()` 直接可调。

    generated_at：规格写的是「调用方传入」。不传时取运行时钟，并向 stderr 说明——
      因为不传 = 这份清单的 generated_at 不可复现，两次重生成必然产生 diff。
      不静默取时钟，是为了让"为什么每次重生成都有 diff"这件事在日志里就能读到，
      而不是让人回来翻代码才发现。**不可复现的只有这一个字段**，其余全部由内容决定。

    write：自测（test_intent_offline.py）要在**不落盘**的前提下比对清单是否与代码同步，
      故留一个开关。默认 True 保持 CLI 行为不变。
    """
    if generated_at is None:
        generated_at = _now_utc_iso()
        print("[module_manifest] 未传入 generated_at，取运行时钟：%s（该字段因此不可复现，"
              "同步比对请用 --check，它按内容比、忽略本字段）" % generated_at, file=sys.stderr)
    if not isinstance(generated_at, str) or not generated_at.strip():
        raise ValueError("generated_at 必须是非空字符串（ISO8601），收到：%r" % (generated_at,))

    manifest = {
        "module": MODULE_NAME,
        "module_version": MODULE_VERSION,
        "prompt_version": read_prompt_version(),
        "output_schema": _schema_pin(SCHEMA_INTENT_EXECUTION_PLAN),
        # 入参契约按规格只写文件名（不钉版本）。诚实边界见本文件文档串第 ① 条：
        # 写在这里不代表运行时按它校验过。
        "input_schema": os.path.basename(SCHEMA_CONTEXT_SNAPSHOT),
        "step_structure": list(STEP_STRUCTURE),
        "generated_at": generated_at,
        "source_sha256": collect_source_sha256(),
    }
    if write:
        target = path or MODULE_MANIFEST_PATH
        with open(target, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    return manifest


def diff_against_disk(path=None):
    """把重新生成的清单与盘上那份逐键比对（忽略 generated_at），返回差异说明列表（空 = 同步）。

    这是"手改无效"的执行面。比对时**重新生成的那份不写盘**——检查器不该在检查过程中
    把被检查对象改成合格的样子（那等于自己给自己盖章）。
    """
    target = path or MODULE_MANIFEST_PATH
    if not os.path.exists(target):
        return ["module_manifest.json 不存在：%s（请先运行生成器）" % target]
    try:
        with open(target, encoding="utf-8") as fh:
            on_disk = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        return ["module_manifest.json 读取/解析失败（%s）：%s" % (type(e).__name__, e)]

    fresh = generate(generated_at=on_disk.get("generated_at") or "-", write=False)
    problems = []
    for key in sorted(set(fresh) | set(on_disk)):
        if key in _VOLATILE_KEYS:
            continue
        if key not in on_disk:
            problems.append("盘上缺键 %s（代码侧现值：%r）" % (key, fresh[key]))
        elif key not in fresh:
            problems.append("盘上多出键 %s（代码侧不产出此键，疑为手改）" % key)
        elif on_disk[key] != fresh[key]:
            # source_sha256 是个逐文件的映射，整体打印会刷屏且看不出到底哪份文件变了——
            # 而"哪份文件变了"正是使用者要的那一句话，所以这里下钻到文件级再报。
            if isinstance(fresh[key], dict) and isinstance(on_disk.get(key), dict):
                for name in sorted(set(fresh[key]) | set(on_disk[key])):
                    if name not in on_disk[key]:
                        problems.append("%s: 盘上未登记文件 %s（新增源文件后未重生成清单）" % (key, name))
                    elif name not in fresh[key]:
                        problems.append("%s: 盘上多出文件 %s（源文件已删除或被改名）" % (key, name))
                    elif on_disk[key][name] != fresh[key][name]:
                        problems.append("%s: %s 内容已变（盘上 %s… ≠ 现算 %s…）"
                                        % (key, name, on_disk[key][name][:12], fresh[key][name][:12]))
            else:
                problems.append("键 %s 不一致：盘上 %r ≠ 现算 %r" % (key, on_disk[key], fresh[key]))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python3 -m kernel.intent.module_manifest",
        description="生成 kernel/intent/module_manifest.json（资产⑦）。手改该 json 无效——只认本生成器。",
    )
    parser.add_argument("--generated-at", default=None,
                        help="ISO8601 时间戳；不给则取运行时钟（该字段将不可复现）")
    parser.add_argument("--check", action="store_true",
                        help="只比对盘上 json 与代码是否同步（忽略 generated_at），不写盘")
    args = parser.parse_args(argv)

    try:
        if args.check:
            problems = diff_against_disk()
            for line in problems:
                print("  " + line)
            print(_MARK_STALE if problems else _MARK_IN_SYNC)
            return 1 if problems else 0
        manifest = generate(generated_at=args.generated_at)
        print("module=%s module_version=%s prompt_version=%s files=%d"
              % (manifest["module"], manifest["module_version"],
                 manifest["prompt_version"], len(manifest["source_sha256"])))
        print(MODULE_MANIFEST_PATH)
        print(_MARK_WRITTEN)
        return 0
    except Exception as e:                      # noqa: BLE001 —— 没跑完 ≠ 通过，归到退出码 2
        print("[module_manifest] 运行失败（%s）：%s" % (type(e).__name__, e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
