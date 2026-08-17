#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""冻结断言门的负向变异回归套件（轨道A 第二步 · P0-2 属主件）。

为什么要有本文件（宪法铁律「exit 0 ≠ 通过」的直接落点）：
  tools/freeze_gate.py 现在对真仓判 GATE_GREEN。但「门在当前仓库判绿」**不能证明**「门拦得住东西」——
  一个 `return 0` 的空壳脚本同样会判绿。要证明门是活的，唯一办法是**故意把仓库弄坏，看门红不红**。
  本套件对 R1/R2/R3/R4/R8/R9/R10/R11/R12/R13 各注入至少一处已知缺陷，逐条断言门必须转红，
  并用 M0 基线（未变异副本送签态必须判绿）堵住「套件自己一直红 = 假红」这条反向假绿。
  M11-M20（P0-2 修复批次增补）注入的是**对抗核验实测复现过的假绿路径**，不是设想出来的缺陷：
  改正文+同步登记册不升版 / 围栏伪造版本行 / GBK 不可读件藏待决标记 / 参数真源写占位 /
  冻结件正文被掏空 / 白名单标记条数膨胀 / case.yaml 待决标记 / 声明份数与常量打架 / 两条豁免边界。

隔离纪律（不得污染真仓）：
  每个变异都在**独立的副本树**上做，真仓一个字节都不改。副本树自带 tools/freeze_gate.py，
  freeze_gate 的 ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))，
  故直接执行副本里的那份脚本，根目录**自动**指向副本树——
  因此**不需要**给 freeze_gate.py 加 DIYU_FREEZE_GATE_ROOT 之类的根目录覆盖环境变量（北极星 6「不加建」：
  能用现有机制做到就不加开关；少一个环境变量 = 少一条能在生产运行里被误设、把门的扫描面挪走的放宽路径）。
  副本里的 freeze_gate.py 与真仓的字节 sha256 相等这一点由 make_copy() 的断言② 当场核验——
  否则本套件测的就不是出厂那份门（自欺）。
  收尾另有「真仓零改动」核验：变异前后对真仓做一次全量文件 digest 快照比对，路径集合与内容必须完全一致。
  该核验的**排除面**见 snapshot_tree 的 docstring（点开头路径 + *.pyc/__pycache__）——措辞不得超出它证明的范围。

副本范围（为什么不是「git ls-files 的追踪文件」）：
  ① 仓库根存在 `.env`（mode 600，密钥文件）。任何「整树复制」都会把它复制进临时目录 = 扩散密钥面。
     本套件的复制规则是**排除一切以 "." 开头的文件与目录**（含 .env / .git / .claude / .githooks），
     并在复制后断言副本树里不存在任何点开头的路径分量。
  ② 反过来，「只复制 git 追踪文件」会漏掉 acceptance/cases/*/fixtures/ 与 contracts/rules/*.yaml 等
     **门必须读、但当前尚未提交**的资产，M0 基线会因此假红——那会把套件本身变成噪音。
  ③ 故取「整树减点开头路径」：既不含密钥，又与门实际读到的工作区状态一字不差。
     若将来门新读了某个点开头的文件，M0 基线会当场转红把这件事喊出来（不静默）。

用法（纯 assert 脚本，不依赖 pytest）：
  python3 tools/test_freeze_gate_mutations.py      逐项打印 PASS/FAIL；任一项 FAIL → exit 1
  环境变量 KEEP_MUTATION_TREES=1 保留副本树不删（排障用；默认跑完即删）

判定口径（与任务规格一致）：
  · 变异可能同时命中多条红线，故断言是「**非绿** 且 **命中集合包含期望红线**」，不要求「只红这一条」。
  · 「非绿」= 退出码非 0 且 stdout 含 GATE_RED 且不含 GATE_GREEN——三者同时成立才算门真的拒绝，
    单看退出码会被 import 期异常之类的非门失败冒充（那属于「门坏了」，不是「门拦住了」）。
  · M10 / M14 / M16 额外断言某条红线 **未**命中：它们在副本上先把 frozen_digests 同步到改后的内容，
    目的是逼被测红线独立命中；若 R10 抢先触发，本条就退化成又一次 R10 测试，证明不了被测红线活着。
  · **模式维度**（P0-2 修复批次增补）：CHECKS 每项带 mode。M0-run 断言「未变异副本在 run 模式下
    命中集合**恰为** {R2,R11,R12}」——多一条 = 冒出计划外缺陷，少一条 = 送签豁免泄漏进了运行态；
    M19/M20 则从反向证明送签豁免是「字段 + 取值」「逐份文件名」双重限定，不是取值/目录级通行证。
"""
import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE_REL = os.path.join("tools", "freeze_gate.py")
GATE_ABS = os.path.join(REPO, GATE_REL)

# 复制副本树时跳过的名字：一切点开头（含 .env 密钥与 .git）+ Python 派生物
SKIP_EXACT = frozenset(["__pycache__"])


def _ignore(_dirpath, names):
    out = set()
    for n in names:
        if n.startswith(".") or n in SKIP_EXACT or n.endswith(".pyc"):
            out.add(n)
    return out


# freeze_gate 的正文字节 digest 算法（M10 同步 frozen_digests 要用）——
# 直接**导入出厂那份实现**，不在本文件里另写一遍：算法一旦分叉，M10 就会用错算法造出假的「已同步」。
def _load_gate_module():
    # 导入真仓的门会在真仓写出 tools/__pycache__/*.pyc。虽被 .gitignore 忽略，
    # 但「真仓零改动」那句断言会因此与事实不符（snapshot_tree 恰好跳过 *.pyc，对自己造的这个污染是瞎子）。
    # 关掉字节码写入，让断言说的和做的一致。
    prev = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("freeze_gate_under_test", GATE_ABS)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)      # 模块级只算路径/编译正则，无副作用；main() 有 __main__ 守卫
        return mod
    finally:
        sys.dont_write_bytecode = prev


GATE = _load_gate_module()


# ---------------------------------------------------------------- 基础设施

def sha256_bytes_of(path):
    with io.open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def snapshot_tree(root):
    """{相对路径: 内容 sha256}，范围与副本规则同口径（不读任何点开头文件，故不碰 .env）。

    ⚠ 排除清单（收尾那句「真仓零改动」只在此范围内成立，措辞不得超出它证明的东西）：
      · 一切以 "." 开头的文件与目录（含 .env / .git / .githooks）——为不扩散密钥面；
      · __pycache__ 与 *.pyc（Python 派生物）。
    即：本断言证明的是「非点开头、非字节码缓存的文件路径集合与内容不变」，
    **不**证明「真仓一个字节都没动」。字节码写入已由 _load_gate_module 关掉，但排除面本身仍在。
    """
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if not d.startswith(".") and d not in SKIP_EXACT)
        for fn in sorted(filenames):
            if fn.startswith(".") or fn.endswith(".pyc"):
                continue
            p = os.path.join(dirpath, fn)
            out[os.path.relpath(p, root)] = sha256_bytes_of(p)
    return out


def make_copy(dest):
    shutil.copytree(REPO, dest, ignore=_ignore, symlinks=False)
    # 断言①：副本树里不得有任何点开头的路径分量（密钥/`.git` 确实没被带进来）
    for dirpath, dirnames, filenames in os.walk(dest):
        for n in list(dirnames) + list(filenames):
            if n.startswith("."):
                raise AssertionError("副本树混入点开头路径 %s（复制规则失效，可能扩散 .env 等密钥）"
                                     % os.path.relpath(os.path.join(dirpath, n), dest))
    # 断言②：副本里的门与出厂那份字节相同——否则测的不是出厂门
    copied = os.path.join(dest, GATE_REL)
    if sha256_bytes_of(copied) != sha256_bytes_of(GATE_ABS):
        raise AssertionError("副本里的 %s 与真仓不一致，本套件测的不是出厂那份门" % GATE_REL)
    return dest


RED_RULE_RE = re.compile(r"^\s*\d+\.\s+(R\d{1,2})\b")


def run_gate(tree, mode="sign"):
    """在副本树上执行副本里的门。返回 (rc, stdout+stderr, 命中的红线编号集合)。"""
    argv = [sys.executable, os.path.join(tree, GATE_REL)]
    if mode == "sign":
        argv.append("--mode=sign")
    proc = subprocess.run(argv, cwd=tree, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.stdout.decode("utf-8", "replace")
    rules = set()
    if "GATE_RED" in out:
        tail = out[out.index("GATE_RED"):]
        for line in tail.splitlines():
            m = RED_RULE_RE.match(line)
            if m:
                rules.add(m.group(1))
    return proc.returncode, out, rules


def is_green(rc, out):
    return rc == 0 and "GATE_GREEN" in out and "GATE_RED" not in out


def is_red(rc, out):
    return rc != 0 and "GATE_RED" in out and "GATE_GREEN" not in out


# ---------------------------------------------------------------- 变异原语

def read(tree, relpath):
    with io.open(os.path.join(tree, relpath), encoding="utf-8") as f:
        return f.read()


def write(tree, relpath, text):
    with io.open(os.path.join(tree, relpath), "w", encoding="utf-8") as f:
        f.write(text)


def replace_once(tree, relpath, old, new):
    """把锚点串恰好替换一次。锚点不唯一即抛错——变异必须是**确定**的一处改动，
    否则「门红了」可能红在别的地方，测不出想测的那条红线。"""
    text = read(tree, relpath)
    n = text.count(old)
    if n != 1:
        raise AssertionError("变异锚点在 %s 中出现 %d 次（应恰好 1 次）: %r" % (relpath, n, old))
    write(tree, relpath, text.replace(old, new, 1))


def sub_once(tree, relpath, pattern, repl):
    text = read(tree, relpath)
    new, n = re.subn(pattern, repl, text, flags=re.M)
    if n != 1:
        raise AssertionError("变异正则在 %s 上匹配 %d 处（应恰好 1 处）: %r" % (relpath, n, pattern))
    write(tree, relpath, new)


E2E01_MF = "acceptance/cases/E2E-01/manifest.yaml"
E2E01_SNAP = "acceptance/cases/E2E-01/fixtures/context_snapshot.json"
GEN_PARAMS = "contracts/interaction/generation_parameters.json"
ANON_DOC = "contracts/interaction/anonymity_procedure.md"
INTERACTION_README = "contracts/interaction/README.md"
E2E_CONTRACT = "contracts/interaction/e2e_interaction_contract.md"
BASELINE_D = "contracts/interaction/baseline_prompt_stage_D.md"
BD_D01_CASE = "acceptance/cases/BD-D01/case.yaml"
RULE_FILE = "contracts/rules/R-FB01-001.yaml"
SIGN_PACKAGE = "IA-0_冻结签字包.md"
B_DOC = "B_三个核心模块智能验收合同.md"
DIGESTS = "contracts/frozen_digests.json"


def sync_digest_registry(tree, docrel):
    """在副本树上把某份文件的 frozen_digests 登记项**完整**同步到改后的内容。

    「完整」= 顶层 sha256 + version_history 末条的 sha256 与 chain 一并改写。
    用途只有一个：在需要**隔离**某条红线的变异里让 R10 闭嘴（M10 逼 R13 独立命中、M14 逼 R2、M16 逼 R11）。
    ⚠ 这个动作本身就是 `contracts/frozen_digests.json` 的 `_chain_algorithm` 里如实交代的那条残余路径：
      知道算法的人可以重写整条冻结历史。本套件用它，正是为了不假装该路径不存在——
      M11 测的是「只同步顶层 sha256、不动历史」这条**顺手**路径必须红；本函数走的是「显式重写历史」那条更重的路径。
    """
    reg_path = os.path.join(tree, DIGESTS)
    with io.open(reg_path, encoding="utf-8") as f:
        reg = json.load(f)
    entry = reg["documents"][docrel]
    new_digest = GATE.sha256_file_bytes(os.path.join(tree, docrel))
    if new_digest == entry["sha256"]:
        raise AssertionError("sync_digest_registry: %s 的 digest 没变，变异没生效" % docrel)
    entry["sha256"] = new_digest
    hist = entry["version_history"]
    hist[-1]["sha256"] = new_digest
    chain = None
    for h in hist:
        chain = GATE.version_chain_link(chain, h["declared_version"], h["sha256"])
        h["chain"] = chain
    with io.open(reg_path, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def m0_baseline(_tree):
    """基线：不做任何变异。防「套件自身假红」——若这条不绿，后面十条的『红』毫无意义。"""


def m1_drop_contract_version_key(tree):
    """M1 删除 E2E-01 Manifest 的 e2e_interaction_contract_version 键。
    期望：R3（Schema.required 缺键）；R9 因取不到键而按设计让位给 R3，故两者取其一即算命中。"""
    sub_once(tree, E2E01_MF, r"^e2e_interaction_contract_version:.*\n", "")


def m2_drift_generation_parameter(tree):
    """M2 改生成参数取值、**不动** Manifest 的 generation_parameters_hash。
    期望：R8（实时重算 ≠ 声明指纹）。这正是 M0 收口撞上的洞：R6 只查非空，参数漂移看不见。"""
    replace_once(tree, GEN_PARAMS, '"temperature": 0.3,', '"temperature": 0.35,')


def m3_bogus_contract_version(tree):
    """M3 把交互合同版本号改成真源里不存在的 v999.0。期望：R9（版本号实时解析比对）。"""
    replace_once(tree, E2E01_MF,
                 'e2e_interaction_contract_version: "v1.0"',
                 'e2e_interaction_contract_version: "v999.0"')


def m4_reintroduce_pending_ia0(tree):
    """M4 在匿名流程文件里插一行 PENDING_IA0。期望：R11（考试条件区的待决标记，两模式同红）。"""
    write(tree, ANON_DOC, read(tree, ANON_DOC) + "\n<!-- MUTATION M4：PENDING_IA0 残留复发 -->\n")


def m5_edit_b_body_without_version_bump(tree):
    """M5 改 B 合同正文一个字符、**不升版**、**不同步** frozen_digests。
    期望：R10（正文字节 digest 与登记不符）。R7 只看版本行，对这种改法是瞎子——本条即证明 R10 补上了那半边。
    锚点选在 B 尾部结语句，既不在 B.0 文档控制块（不影响 R7），也不在 B.7 表内（不影响 R13）。"""
    replace_once(tree, B_DOC, "才能对终极问题给出：", "才能对终极问题给出:")


def m6_duplicate_case_id(tree):
    """M6 把 BD-D02 的 case_id 改成与 BD-D01 重复。
    期望：R12（case_id 与所在案例目录不一致 / 运行身份撞车 / 不同 case_id 数 ≠ 14）。"""
    sub_once(tree, "acceptance/cases/BD-D02/manifest.yaml", r"^case_id: BD-D02\b", "case_id: BD-D01")


def m7_delete_one_manifest(tree):
    """M7 删掉一份 Manifest。期望：R1（齐套数 ≠ 20）。"""
    os.remove(os.path.join(tree, "acceptance/cases/SYS-D01/manifest.yaml"))


def m8_tamper_snapshot(tree):
    """M8 改快照内容（企业事实 facts.inventory.value 库存 800 → 801）。期望：R4（snapshot_hash 与实算不符）。

    走**结构路径**改而不是文本串替换：`"value": 800` 在本快照里出现两次（顶层 facts.inventory 与
    facts.product.inventory），文本锚点不唯一，改错一处会让「门为什么红」变得不可归因。
    改完当场用出厂门自己的 canonical_snapshot_hash 断言哈希确实变了——门算的是**规范化** JSON sha256
    （键排序 + 紧凑分隔符），纯格式改动本就不该变哈希（设计如此，不是漏判），
    这一句断言保证本条测的是真的内容篡改，而不是一次格式级 no-op 骗出来的红。"""
    p = os.path.join(tree, E2E01_SNAP)
    before = GATE.canonical_snapshot_hash(p)
    with io.open(p, encoding="utf-8") as f:
        obj = json.load(f)
    node = obj["facts"]["inventory"]
    if node.get("value") != 800:
        raise AssertionError("M8 前置不成立：facts.inventory.value=%r（应为 800）" % node.get("value"))
    node["value"] = 801
    with io.open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    if GATE.canonical_snapshot_hash(p) == before:
        raise AssertionError("M8 改后规范化 hash 未变，变异没生效（成了格式级 no-op）")


def m9_blank_required_field(tree):
    """M9 把一个必填字段置成空串。期望：R2（空白值不算已填）。"""
    sub_once(tree, "acceptance/cases/BD-D03/manifest.yaml",
             r'^task_statement: .*$', 'task_statement: ""')


def m10_drop_b7_mapping_row(tree):
    """M10 删 B.7 一行需求映射，并在副本上**先把 frozen_digests 完整同步到改后的 B 正文**。
    期望：R13 命中，且 R10 **不**命中。
    为什么要先同步：不同步的话 R10 会抢先报「正文 digest 不符」，这条就退化成第二次 R10 测试，
    证明不了「R13 能独立发现需求映射被削掉」。同步动作只发生在一次性副本树里，真仓不受影响。"""
    replace_once(tree, B_DOC, "| SYS-10 | SYS-D01 |\n", "")
    sync_digest_registry(tree, B_DOC)


# ============================ P0-2 修复批次新增变异（M11-M20 + 双模式）============================
# 每一条都对应一处**已在副本树上复现过的假绿**，不是设想。

def m11_edit_b_body_and_sync_digest_without_bump(tree):
    """M11 改 B 正文 + **同步 frozen_digests 顶层 sha256** + 不升版 + 不动 version_history。

    这是最自然的「把门弄绿」反射动作：门报 digest 不符 → 顺手把登记值改成实算值 → 绿。
    修复前实测：`--mode=sign` 输出 GATE_GREEN、exit 0，收尾行照旧宣称「真源正文 digest 与登记一致」
    （M5 只测了「不同步」那一种，对本条完全无感；M10 则先同步 digest 让 R10 闭嘴——旁路配方就写在套件自己里）。
    期望：R10 必须红——顶层 (declared_version, sha256) 与 version_history 末条对不上。"""
    replace_once(tree, B_DOC,
                 "目标三个且最低两个 candidate_options",
                 "目标三个且最低一个 candidate_options")
    reg_path = os.path.join(tree, DIGESTS)
    with io.open(reg_path, encoding="utf-8") as f:
        reg = json.load(f)
    new_digest = GATE.sha256_file_bytes(os.path.join(tree, B_DOC))
    if new_digest == reg["documents"][B_DOC]["sha256"]:
        raise AssertionError("M11 改后 B 正文 digest 未变，变异没生效")
    reg["documents"][B_DOC]["sha256"] = new_digest      # 只同步顶层，历史一字不动
    with io.open(reg_path, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def m12_forge_version_row_in_code_fence(tree):
    """M12 伪造版本行：把真控制块的「版本」行改名成「文档版本」，并在文末追加一个代码围栏，
    围栏里放一行 `| 版本 | v1.0 |`。

    修复前实测：门打印「e2e_interaction_contract_version=v1.0」并判 GATE_GREEN、exit 0，
    而真源自述 v0.1-draft 未定稿——正好是 R9 声称要拦的「案例冻结在一份不存在/被取代的合同上」。
    期望：R9 必须红（控制块内已无版本行，围栏里的示例不算权威）。"""
    replace_once(tree, E2E_CONTRACT, "| 版本 | **v1.0** |",
                 "| 文档版本 | **v0.1-draft（尚未定稿，禁止引用）** |")
    write(tree, E2E_CONTRACT, read(tree, E2E_CONTRACT)
          + "\n\n```\n| 项目 | 内容 |\n|---|---|\n| 版本 | v1.0 |\n```\n")


def m13_unreadable_file_with_pending_mark(tree):
    """M13 往 contracts/ 写一份 **GBK 编码**、内容含 PENDING_IA0 的文件。

    修复前实测：read_text_or_none 吞掉 UnicodeDecodeError 返回 None，调用点 `if text is None: continue`
    → GATE_GREEN、exit 0，末行仍宣称「待决标记与悬空指针清零」；同一文件 iconv 回 UTF-8 后 grep 得 1 处。
    期望：R11 必须红——读不出来 ≠ 干净。"""
    p = os.path.join(tree, "contracts", "OD-99_变异用不可读件.md")
    with open(p, "wb") as f:
        f.write("# 变异件\n\n本行含待决标记 PENDING_IA0，编码为 GBK。\n".encode("gbk"))


def m14_placeholder_in_generation_parameters(tree):
    """M14 把 generation_parameters.json 的 model_name 改成占位 "TBD"，并按门自己的算法重算指纹、
    同步 20 份 Manifest 的 generation_parameters_hash，再完整同步 digest 登记册。

    修复前实测：`--mode=sign` 判 GATE_GREEN、exit 0，收尾行仍宣称「零占位残留」——R8 只比对哈希
    一致性、从不看取值是不是占位；R2 的扫描面又不含这个文件。OD-02「模型与参数定格」因此可被完全架空。
    期望：R2 必须红，且 R8 / R10 **不**得抢先命中（否则证明不了 R2 的扫描面真的覆盖到了这个文件）。"""
    replace_once(tree, GEN_PARAMS, '"model_name": "qwen-max-0107",', '"model_name": "TBD",')
    new_hash = GATE.canonical_snapshot_hash(os.path.join(tree, GEN_PARAMS))
    old_hash = None
    mfs = sorted(glob.glob(os.path.join(tree, "acceptance/cases/*/manifest*.yaml")))
    if len(mfs) != 20:
        raise AssertionError("M14 前置不成立：副本树里 Manifest %d 份（应 20）" % len(mfs))
    for mf in mfs:
        with io.open(mf, encoding="utf-8") as f:
            text = f.read()
        m = re.search(r'generation_parameters_hash:\s*"?(sha256:[0-9a-f]{64})"?', text)
        if not m:
            raise AssertionError("M14 在 %s 里找不到 generation_parameters_hash" % mf)
        old_hash = old_hash or m.group(1)
        with io.open(mf, "w", encoding="utf-8") as f:
            f.write(text.replace(m.group(1), new_hash))
    if old_hash == new_hash:
        raise AssertionError("M14 改后指纹未变，变异没生效")
    sync_digest_registry(tree, GEN_PARAMS)


def m15_hollow_out_frozen_contract(tree):
    """M15 把 baseline_prompt_stage_D.md 整体替换成一个 8 行壳（只留控制块版本行与一行待决标记）。

    修复前实测：`--mode=sign` 判 GATE_GREEN、exit 0，提示行照旧输出「10 份白名单文件仍带该标记」，
    门宣称「交互合同与基线 Prompt 版本实时解析命中」——IA-0 送签三件套的**内容**从未被任何红线覆盖，
    只有一行版本号被读过。
    期望：R10 必须红（该文件已纳入 digest 登记册）。"""
    write(tree, BASELINE_D,
          "# 基线 Prompt｜阶段 D\n\n## 0. 元信息\n\n| 项目 | 内容 |\n|---|---|\n"
          "| 版本 | **v1.0** |\n| 状态 | PENDING_RESIGN_P0-6 |\n")


def m16_exceed_whitelist_marker_cap(tree):
    """M16 往 contracts/interaction/README.md 注入一处 PENDING_RESIGN_P0-6（重签后 0→1），并同步 digest。

    历史：白名单曾是文件级豁免（P0-2 收窄为条数上限，当时 README 上限 2）；2026-08-18 P0-6 重签完成后
    白名单整体退役——该标记无合法复活场景，出现一处即红。期望：R11 必须红，且 R10 不得抢先命中。"""
    write(tree, INTERACTION_README, read(tree, INTERACTION_README)
          + "\n> 变异追加：又一处 PENDING_RESIGN_P0-6。\n")
    sync_digest_registry(tree, INTERACTION_README)


def m17_pending_mark_in_case_yaml(tree):
    """M17 往 acceptance/cases/BD-D01/case.yaml 追加一行含 PENDING_IA0 的注释。

    修复前实测：面一/面二只扫 contracts/** + 20 份 Manifest，面三却扫整棵 cases 树——同一条红线两套边界，
    于是 case.yaml（承载断言清单与 tag，比 Manifest 更硬的考试条件）带着待决标记仍判 GATE_GREEN。
    期望：R11 必须红。"""
    write(tree, BD_D01_CASE, read(tree, BD_D01_CASE) + "\n# 判定阈值待 IA-0 定：PENDING_IA0\n")


def m18_declared_count_drift(tree):
    """M18 把 IA-0 签字包 §五 的齐套声明从「20 份」改成「21 份」，脚本常量不动。

    修复前：R1 只比对脚本常量 EXPECTED_MANIFESTS，从不解析真源里的**声明**份数——
    「改常量 = 改考卷」是纯散文纪律，零检测器；常量与真源各说各话时门不会吭声。
    期望：R1 必须红（常量与真源声明打架，门不替任何一方拍板）。"""
    replace_once(tree, SIGN_PACKAGE,
                 "**齐套**＝14 案例 ↔ **20 份**运行 Manifest",
                 "**齐套**＝14 案例 ↔ **21 份**运行 Manifest")


def m19_pending_build_in_wrong_field(tree):
    """M19 把送签豁免值 PENDING_BUILD 写进**非** RUN_TIME_FIELDS 的字段（task_statement）。
    期望：即使 --mode=sign 也必须 R2 红——豁免是「字段 + 取值」双重限定，不是「取值」通行证。"""
    sub_once(tree, "acceptance/cases/BD-D03/manifest.yaml",
             r'^task_statement: .*$', 'task_statement: "PENDING_BUILD"')


def m20_resign_mark_outside_whitelist(tree):
    """M20 把 PENDING_RESIGN_P0-6 写进**非**白名单文件（contracts/rules/ 下的 RuleRecord）。
    期望：即使 --mode=sign 也必须 R11 红——白名单是逐份枚举的，不是「contracts/ 下都放行」。"""
    write(tree, RULE_FILE, read(tree, RULE_FILE) + "\n# 变异：PENDING_RESIGN_P0-6\n")


# 每项：(编号, 说明, 变异函数, 模式, 期望结果, 期望命中的红线之一, 禁止命中的红线, 期望的**完整**命中集合|None)
CHECKS = [
    ("M0", "基线：未变异副本 --mode=sign 必须 GATE_GREEN（防套件自身假红）",
     m0_baseline, "sign", "GREEN", (), (), None),
    # 运行态基线：证明 run 模式的红**恰为设计内类别**（重签后仅 R2），不是「运行态红得莫名其妙」。
    # 命中集合断言为**全等**：多一条 = 冒出计划外缺陷，少一条 = 送签豁免泄漏进了运行态。
    ("M0-run", "基线：未变异副本 **run 模式** 必须 RED 且命中集合恰为 {R2}（P0-6 重签后 R11/R12 已清零）",
     m0_baseline, "run", "RED", ("R2",), (), {"R2"}),
    ("M1", "删除 E2E-01 Manifest 的 e2e_interaction_contract_version 键",
     m1_drop_contract_version_key, "sign", "RED", ("R3", "R9"), (), None),
    ("M2", "改 generation_parameters.json 参数值、不动 Manifest 指纹",
     m2_drift_generation_parameter, "sign", "RED", ("R8",), (), None),
    ("M3", "e2e_interaction_contract_version 改成真源不存在的 v999.0",
     m3_bogus_contract_version, "sign", "RED", ("R9",), (), None),
    ("M4", "anonymity_procedure.md 插入一行 PENDING_IA0",
     m4_reintroduce_pending_ia0, "sign", "RED", ("R11",), (), None),
    ("M5", "B 合同正文改一字、不升版、不同步 digest 登记册",
     m5_edit_b_body_without_version_bump, "sign", "RED", ("R10",), (), None),
    ("M6", "两份 Manifest 的 case_id 改成重复",
     m6_duplicate_case_id, "sign", "RED", ("R12",), (), None),
    ("M7", "删除一份 Manifest（齐套被破坏）",
     m7_delete_one_manifest, "sign", "RED", ("R1",), (), None),
    ("M8", "快照内容改一处取值（库存 800→801）",
     m8_tamper_snapshot, "sign", "RED", ("R4",), (), None),
    ("M9", "Manifest 必填字段 task_statement 置空串",
     m9_blank_required_field, "sign", "RED", ("R2",), (), None),
    ("M10", "删 B.7 一行需求映射并同步 digest（逼 R13 独立命中）",
     m10_drop_b7_mapping_row, "sign", "RED", ("R13",), ("R10",), None),
    ("M11", "改 B 正文 + 只同步登记册 sha256 + 不升版（最自然的「把门弄绿」路径）",
     m11_edit_b_body_and_sync_digest_without_bump, "sign", "RED", ("R10",), (), None),
    ("M12", "伪造版本行：真控制块行改名 + 代码围栏里塞示例版本行",
     m12_forge_version_row_in_code_fence, "sign", "RED", ("R9",), (), None),
    ("M13", "往 contracts/ 写一份 GBK 编码、含 PENDING_IA0 的不可读文件",
     m13_unreadable_file_with_pending_mark, "sign", "RED", ("R11",), (), None),
    ("M14", "generation_parameters.json 取值改成占位 TBD + 同步指纹与登记册（逼 R2 独立命中）",
     m14_placeholder_in_generation_parameters, "sign", "RED", ("R2",), ("R8", "R10"), None),
    ("M15", "把 baseline_prompt_stage_D.md 掏空成 8 行壳（冻结件正文被整体改写）",
     m15_hollow_out_frozen_contract, "sign", "RED", ("R10",), (), None),
    ("M16", "重签后注入一处 PENDING_RESIGN（README 0→1）并同步登记册（逼 R11 独立命中，白名单已退役）",
     m16_exceed_whitelist_marker_cap, "sign", "RED", ("R11",), ("R10",), None),
    ("M17", "往 acceptance/cases/BD-D01/case.yaml 塞一行 PENDING_IA0（扫描面此前漏掉的面）",
     m17_pending_mark_in_case_yaml, "sign", "RED", ("R11",), (), None),
    ("M18", "IA-0 §五 齐套声明改成 21 份、脚本常量不动（常量与真源打架）",
     m18_declared_count_drift, "sign", "RED", ("R1",), (), None),
    ("M19", "送签豁免值 PENDING_BUILD 写进非豁免字段 task_statement（豁免边界）",
     m19_pending_build_in_wrong_field, "sign", "RED", ("R2",), (), None),
    ("M20", "PENDING_RESIGN_P0-6 写进非白名单文件 contracts/rules/（豁免边界）",
     m20_resign_mark_outside_whitelist, "sign", "RED", ("R11",), (), None),
]


def main():
    print("冻结断言门 · 负向变异回归套件")
    print("真仓 %s" % REPO)
    print("门   %s（sha256 %s…）" % (GATE_REL, sha256_bytes_of(GATE_ABS)[:16]))
    print("口径：每个变异在独立副本树上做；断言「非绿 + 命中期望红线」；M0 反向断言「未变异必须绿」。")
    print("根目录覆盖：不需要环境变量——副本树自带 tools/freeze_gate.py，门的 ROOT 由 __file__ 自动指向副本根。")
    print("")

    before = snapshot_tree(REPO)
    work = tempfile.mkdtemp(prefix="freeze_gate_mut_")
    failures = []
    try:
        for cid, desc, mutate, mode, expect, want_rules, forbid_rules, exact_rules in CHECKS:
            tree = os.path.join(work, cid)
            detail = ""
            try:
                make_copy(tree)
                mutate(tree)
                rc, out, rules = run_gate(tree, mode=mode)
                got = "GREEN" if is_green(rc, out) else ("RED" if is_red(rc, out) else "不确定")
                fired = "、".join(sorted(rules, key=lambda r: int(r[1:]))) or "无"
                ok = True
                reasons = []
                if expect == "GREEN":
                    if not is_green(rc, out):
                        ok = False
                        reasons.append("期望 GATE_GREEN，实得 %s（exit=%d）" % (got, rc))
                else:
                    if not is_red(rc, out):
                        ok = False
                        reasons.append("期望 GATE_RED，实得 %s（exit=%d）——门没拦住这个缺陷" % (got, rc))
                    if want_rules and not (set(want_rules) & rules):
                        ok = False
                        reasons.append("期望命中 %s 之一，实际命中 {%s}"
                                       % ("/".join(want_rules), fired))
                    hit_forbidden = set(forbid_rules) & rules
                    if hit_forbidden:
                        ok = False
                        reasons.append("不应命中 %s（该条抢先触发会掩盖被测红线）"
                                       % "、".join(sorted(hit_forbidden)))
                    if exact_rules is not None and rules != set(exact_rules):
                        ok = False
                        reasons.append("命中集合应**恰为** {%s}，实得 {%s}（多一条=计划外缺陷，"
                                       "少一条=豁免泄漏或红线失效）"
                                       % ("、".join(sorted(exact_rules)), fired))
                detail = "[%s 模式] 实得 %s，命中红线 {%s}" % (mode, got, fired)
                if not ok:
                    failures.append((cid, "；".join(reasons), out))
            except Exception as e:                                   # noqa: BLE001
                ok = False
                detail = "变异或执行阶段异常"
                failures.append((cid, "%s: %s" % (type(e).__name__, e), ""))
            print("[%-3s] %-6s %s" % (cid, "PASS" if ok else "FAIL", desc))
            print("        期望 %s%s | %s"
                  % (expect,
                     ("（含 %s）" % "/".join(want_rules)) if want_rules else "",
                     detail))
    finally:
        if os.environ.get("KEEP_MUTATION_TREES") == "1":
            print("\n副本树保留于 %s（KEEP_MUTATION_TREES=1）" % work)
        else:
            shutil.rmtree(work, ignore_errors=True)

    # ---- 真仓零改动核验（变异只能发生在副本树上）----
    after = snapshot_tree(REPO)
    if before != after:
        added = sorted(set(after) - set(before))
        removed = sorted(set(before) - set(after))
        changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
        failures.append(("ISOLATION",
                         "真仓被改动：新增 %s / 删除 %s / 内容变 %s" % (added, removed, changed), ""))
        print("\n[隔离] FAIL   真仓在套件运行中被改动——变异泄漏出副本树")
    else:
        print("\n[隔离] PASS   真仓 %d 个文件路径与内容 digest 前后完全一致（变异未泄漏）" % len(before))

    print("")
    if failures:
        print("FAIL —— %d 项未通过：" % len(failures))
        for cid, why, out in failures:
            print("  · %s: %s" % (cid, why))
            if out:
                for line in out.splitlines()[-12:]:
                    print("      | %s" % line)
        print("\n（任一项 FAIL = 冻结门在该缺陷面上判不出红，或套件自身失真——两者都不得放行）")
        return 1
    injected = [c for c in CHECKS if c[4] == "RED"]
    print("PASS —— %d 项全过：门在 %d 个缺陷面上逐一转红，且未变异副本在送签态判绿、"
          "运行态只红设计内类别（重签后仅 R2）。" % (len(CHECKS), len(injected)))
    print("本结论只覆盖上列注入点，**不等于**门无漏判。如实披露三点：")
    print("  ① 未被变异覆盖的红线（R5 / R6 / R7）本次仍无活体证据，不得据此宣称『十三条红线全部已验证』；")
    print("  ② 双模式已取证的只有 M0-run 这一条运行态基线 + M19/M20 两条豁免边界；"
          "其余变异只在送签态取证，运行态表现按同一实现推断、未逐条实测；")
    print("  ③ M10/M14/M16 用 sync_digest_registry **显式重写了冻结历史**来隔离被测红线——"
          "这条路径本身是 frozen_digests.json `_chain_algorithm` 里如实交代的残余面："
          "链把「顺手弄绿」抬成「显式重写历史」，不等于正文不可篡改。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
