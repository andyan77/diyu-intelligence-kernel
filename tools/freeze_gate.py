#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""冻结断言门（IA-0 送签前的物理拦截器）。

职责真源：IA-0_冻结签字包.md §四「B 类｜执行侧建设项」——「送签前脚本扫描全部 Manifest，任何 PENDING 残留 =
物理拒绝送签（堵"带着占位签字"的假绿）」；OPEN_QUESTIONS.md 文首执行侧自决项「PENDING 冻结断言门」
「hash=sha256 规范化 JSON」；OQ-INT-D01-06（SCHEMA_OK ≠ 可冻结）。
（指针按小节名书写，不锁行号——同 contracts/interaction/README.md §4 已采用的纪律。）

十三条红线（任一触发即 exit 1，且逐条列明，不汇总成一句"失败"）：
  R1 齐套数 ≠ EXPECTED_MANIFESTS，**或** 三份真源里书面声明的份数/案例数 ≠ 脚本常量
     （声明真源：IA-0 §五「齐套」句 / OPEN_QUESTIONS 文首预裁决① / OD-02 §三第 2 条。
      「改常量 = 改考卷」原本是纯散文纪律，零检测器；本条把它变成机器断言，常量与真源打架时门当场拦，
      不替任何一方拍板）
  R2 任一 Manifest 的**字段值**空白或命中占位模式（注释里的占位字样不算——注释是说明，不是考试条件）；
     **同一判据同样施加于 contracts/interaction/generation_parameters.json 的全部取值**——
     R8 只比对哈希一致性、从不看取值是不是占位，把 model_name 改成 "TBD" 再按门自己的算法重算指纹
     并同步 20 份 Manifest，旧实现照样判绿并宣称「零占位残留」，OD-02 模型定格就此被架空
  R3 Schema 不过（contracts/schemas/case_manifest.schema.json）
  R4 snapshot_hash 与按本文件算法实算的值不符 / 快照找不到 / 快照 ID 撞车 / 快照与 Manifest 不同案例目录
  R5 hard_rule_refs 解析不到 contracts/rules/ 的 RuleRecord 对象（含 version / brand_id / 非 ACTIVE），
     或 RuleRecord 字段集与 A.9.1 十项不全等
  R6 签字三件套失真：approved_at 不可解析为 ISO8601、approved_by 或 generation_parameters_hash 空白/占位
  R7 prd_version / data_contract_version / acceptance_contract_version 与三份真源文档控制块**实时解析**
     出来的版本号不一致
  R8 generation_parameters_hash ≠ 按本文件算法对 contracts/interaction/generation_parameters.json
     **实时重算**的规范化 sha256（R6 只查它非空，参数文件漂移不可察——那正是 M0 收口撞上的洞）
  R9 e2e_interaction_contract_version / e2e_output_contract_version / baseline_prompt_versions.* 声明的
     版本号，与 contracts/interaction/ 对应真源文件控制块**实时解析**出来的版本号不一致；
     或 E2E 案例把这四项写成 null（B:992「两阶段共同交互合同、输出合同和基线 Prompt 已冻结」）；
     或非 E2E 案例把这四项写成非 null（B.5 之外的案例不走两阶段共同合同）
  R10 冻结件的**正文字节 digest** 与 contracts/frozen_digests.json 登记值不符（防不升版偷改正文——
     R7 只看版本行，改正文不动版本行时 R7 判不出来），或登记的声明版本与文件实时解析不符，
     或 **version_history 链断**（同一 declared_version 二次登记出不同 digest / 顶层登记与末条对不上 /
     chain 与实算不符）。覆盖面 = PRD/A/B 三份冻结真源 + contracts/interaction/ 七份 CONTENT-FROZEN 冻结件。
     为什么要链：只登记一个 digest 拦不住「改正文 + 同步登记册 + 不升版」这条最自然的把门弄绿路径
     （横向比对两边都是新值、永远相等）。诚实边界见 frozen_digests.json 的 _chain_algorithm
  R11 待决标记扫描（三个面**同一扫描边界**：contracts/** + acceptance/cases/** 整棵 + 两份根级冻结声明；
     此前面一/面二只扫 contracts + 20 份 Manifest 而面三扫整棵 cases 树，同一条红线两套口径，
     实测可在 case.yaml 里塞 PENDING_IA0 而门仍绿）：
     PENDING_IA0 出现在扫描面任何位置（含注释）= 两模式均红；
     PENDING_RESIGN_P0-6 = 运行态红、送签态仅允许出现在白名单文件**且不超过该文件的条数上限**
     （白名单从「文件级豁免」收窄为「文件 + 上限」：只按文件名放行等于对该文件内容整体弃权）；
     ".draft.yaml" 字面出现在 acceptance/cases/**（含 fixtures）= 悬空指针复发，两模式均红。
     引述豁免只有一种形态：反引号整体包裹（`PENDING_IA0`）算引述历史状态，裸标记算活标记。
     读不出来的文件（解码/IO 失败）一律记红、按后缀跳过的文件计数打印——「跳过」不等于「干净」
  R12 运行身份唯一：case_id 与所在案例目录名不一致 / (case_id, Manifest 文件名变体) 全局撞车 /
     不同 case_id 数 ≠ EXPECTED_DISTINCT_CASE_IDS / approved_at 命中已撤回签字时间戳
     （撤回签字一项：运行态红，送签态放行并提示待重签）
  R13 需求映射完整性：PRD 全文提取的核心需求编号 ≠ 30 条或有重复 / B.7 表左列与之不全等 /
     B.7 右列解析后有案例目录零映射或有需求零映射

规范化 JSON hash 算法（本文件是唯一实现，Manifest 与 generation_parameters.json 的注释均指向此处；
函数名 canonical_snapshot_hash 保留不改——contracts/interaction/generation_parameters.json 按名引用它）：
  读 JSON → json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) → UTF-8 编码
  → sha256 → 字符串写作 "sha256:<hex>"。即：UTF-8、键排序、无多余空白的规范化 JSON 的 sha256。
  R4 用它算 snapshot_hash，R8 用它算 generation_parameters_hash——同一算法，两个落点。

版本行的锚定（R7/R9/R10 共用，P0-2 修复批次加固）：先剔除代码围栏与 HTML 注释，再只认**第一张**
表头为「| 项目 | 内容 |」的控制块表内的版本行，并把命中行号打印出来。旧实现对全文 findall，
实测可被「真控制块行改名 + 文末追加一个围栏放示例版本行」骗过——门宣称 v1.0 判绿，而真源自述未定稿。

边界（C.2 / C.4：脚本只汇总不推导，不建平台）：本门只做机械核验，不改任何文件、不猜测取值，
**不执行任何外部命令**（HEAD 提交号是直接读 .git 下的文件取的，不调 git）。
GATE_GREEN 只代表"占位清零且机械核验一致"，**不代表** Founder 已签字、更不代表案例质量合格——
签字动作定义见 B.2.1 与 IA-0_冻结签字包.md §五末条「签字动作定义（B.2.1）」。
GATE_GREEN 也只对**当前工作区目录树**成立，不等同于 HEAD 提交的内容（头部归属行已标明）；
干净 clone 的一致性由 P0-6 回执证明，不由本门证明。

用法: exit 0=全绿 1=有红线
  python3 tools/freeze_gate.py              运行态：十三条红线全查，不豁免任何字段。
  python3 tools/freeze_gate.py --mode=sign  送签态：仅豁免 4 个「运行前补填」的构建版本类字段
                                            （diyu_build_version、module_contract_versions.intent /
                                            .business_decision / .creative），且取值必须**恰为**
                                            声明性标记 PENDING_BUILD；任何其他占位或空值仍判红。
                                            该双模式为 Founder 2026-08-17 批准的正式口径（属改考卷），
                                            权威转录见 IA-0_冻结签字包.md §五「冻结门双模式真实口径」。
  除上述两种形态外不接受任何参数。齐套数等考试口径写死于脚本常量：改常量 = 改考卷，须随 Founder 预裁决
  一起改，不得由命令行开关在单次运行里临时放宽（旧 --expected 参数即为此洞，已删除；--mode=sign 不放宽
  齐套数，也不放宽 R3-R10、R13 任何一条）。--mode=sign 是本门唯一合法开关。
  送签态相对运行态的全部豁免只有三处，逐条可枚举：
    ① R2 的 4 个「运行前补填」字段且取值恰为 PENDING_BUILD；
    ② R11 的 PENDING_RESIGN_P0-6 白名单文件（P0-6 Founder 重签前，这些文件带此标记是设计内状态）；
    ③ R12 的已撤回签字时间戳（送签态改为提示「待重签」，不判红——送签本身就是去拿新签字）。
  除此之外送签态与运行态等严；R11 的 PENDING_IA0 与 .draft.yaml 两项**两模式同红**，不设送签豁免。
"""
import datetime
import glob
import hashlib
import io
import json
import os
import re
import sys

import yaml
from jsonschema import Draft7Validator, RefResolver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_GLOB = os.path.join(ROOT, "acceptance/cases/*/manifest*.yaml")
SNAPSHOT_GLOB = os.path.join(ROOT, "acceptance/cases/*/fixtures/*.json")
RULES_GLOB = os.path.join(ROOT, "contracts/rules/*.yaml")
SCHEMA_PATH = os.path.join(ROOT, "contracts/schemas/case_manifest.schema.json")

# 齐套口径 20 = Founder 2026-08-17 预裁决①「INT-D01 补 QUICK 分支变体，总 20 份」
# （acceptance/cases/OPEN_QUESTIONS.md 文首）+ contracts/OD-02_模型与参数定格记录.md §三「定格执行留痕」
# 第 2-3 条「实测版本串 / 参数哈希填入 **20 份** Case Manifest」；齐套定义另见 IA-0_冻结签字包.md §五「齐套」。
# 该口径变更 = 改考试条件，须随预裁决一起改，不得由本脚本静默跟随目录里数到几份就算几份，
# 也不得由命令行参数在单次运行里临时改写。
EXPECTED_MANIFESTS = 20

# 占位模式（R2/R6 共用）。空白（空串或纯空格）单独判，等价于政策里的 ^$ 分支。
PLACEHOLDER_RE = re.compile(r"PENDING|TBD|TODO|N/A|待定|XXX|\?\?\?")

# R6 签字三件套：这三个字段带着占位进签字流程 = "带着占位签字"的假绿本体。
SIGNATURE_FIELDS = ("approved_by", "approved_at", "generation_parameters_hash")

# R5：A.9.1 RuleRecord 的十项字段（A_模块接口与核心数据字典.md「## A.9.1 RuleRecord」yaml 块逐字）。
# 字段集必须全等——少一项 = 注册表残缺，多一项 = 私自扩合同，两者都不得被冻结案例引用。
RULE_RECORD_FIELDS_A91 = frozenset([
    "rule_id", "brand_id", "version", "scope", "effect",
    "target_path", "statement", "source_ref", "status", "effective_at",
])

# R4：跨案例共用快照的**唯一**合法例外。口径同 EXPECTED_MANIFESTS——改这里 = 改考卷。
# 依据：B.5.1/E2E-02「与 E2E-01 使用相同企业事实」+ B.2.2「同条件」定义之「相同 Context Snapshot」，
# 故 E2E-02 的 Manifest 指向 E2E-01/fixtures/ 下的 SNAP-E2E01-0001 属设计要求，不是错挂。
# 键 = Manifest 所在案例目录名，值 = 允许借用快照的案例目录名。
CROSS_CASE_SNAPSHOT_ALLOWED = {"E2E-02": "E2E-01"}

# R7：三个版本字段 ↔ 三份真源文档。版本号**每次运行实时解析**文档控制块，脚本内不留基线常量——
# 硬编码基线会在真源改版后继续判绿（B10 假绿洞的成因）。
VERSION_SOURCES = (
    ("prd_version", "PRD_笛语智能核_MVP_V3.0_v0.1.md"),
    ("data_contract_version", "A_模块接口与核心数据字典.md"),
    ("acceptance_contract_version", "B_三个核心模块智能验收合同.md"),
)
# 文档控制块里的版本行：`| 版本 | v0.2 |`
# ⚠ 本正则**只在锁定的控制块表内**逐行使用（见 parse_control_block_version），不再对全文 findall。
# 为什么（P0-2 修复批次实证的伪造路径）：全文匹配时，代码围栏里的「示例行」可以冒充权威版本——
# 把真控制块行改成 `| 文档版本 | v0.1-draft（禁止引用） |`，再在文末追加一个 ``` 围栏内含
# `| 版本 | v1.0 |`，门就会宣称该文件是 v1.0 并判绿。R7/R9/R10 三条红线共用本正则，一处被骗三处失守。
VERSION_ROW_RE = re.compile(r"^\|\s*版本\s*\|\s*([^|]+?)\s*\|\s*$")
# 文档控制块的表头行。本仓 7 份受控文档（PRD/A/B + contracts/interaction/ 五份 md）控制块表头一律是
# 「| 项目 | 内容 |」——版本行的**唯一**权威位置就是该表内。找不到表头 = 无从锚定 = 红线（fail-closed）。
CONTROL_BLOCK_HEADER_RE = re.compile(r"^\|\s*项目\s*\|\s*内容\s*\|\s*$")
# 控制块必须出现在文件开头附近；否则「第一张 项目|内容 表」这个锚点就不再是文档控制块。
CONTROL_BLOCK_MAX_START_LINE = 60
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

# ---- R8：生成参数指纹的唯一真源 ----
# generation_parameters.json 的 _hash_algorithm 字段明文指定「冻结门按本文件当前内容实时重算，
# 并与 Case Manifest 的 generation_parameters_hash 比对」——本常量即该比对的落点。
GENERATION_PARAMS_PATH = os.path.join(ROOT, "contracts/interaction/generation_parameters.json")

# ---- R9：Manifest 声明的合同版本 ↔ contracts/interaction/ 真源文件 ----
# 与 R7 同纪律：版本号每次运行**实时解析**真源文件的文档控制块，脚本内不留基线常量。
# 阶段 D = Business Decision（decision_stage），阶段 C = Creative（creative_stage）——
# 对应关系见 B.2.3（B:184-204）与 B.2.4（B:206-218），亦与 20 份 Manifest 的字段注释一致。
INTERACTION_VERSION_SOURCES = (
    ("e2e_interaction_contract_version", "contracts/interaction/e2e_interaction_contract.md"),
    ("e2e_output_contract_version", "contracts/interaction/e2e_output_contract.md"),
    ("baseline_prompt_versions.decision_stage", "contracts/interaction/baseline_prompt_stage_D.md"),
    ("baseline_prompt_versions.creative_stage", "contracts/interaction/baseline_prompt_stage_C.md"),
)
# 控制块版本行的取值可能带 Markdown 强调与括注（例：`**v1.0**（同时是 …）`）。
# 只认**行首的**版本号 token，避免"从一句话里随便捞一个 v 开头的串"。
VERSION_TOKEN_RE = re.compile(r"^v\d+(?:\.\d+)*")
# E2E 案例目录名前缀（B.5 端到端匿名 A/B）。只有这类案例走两阶段共同交互/输出合同与基线 Prompt。
E2E_CASE_PREFIX = "E2E-"

# ---- R10：真源正文 digest 登记册 ----
# R7 只核验「版本行」，改正文而不动版本行时 R7 判不出来（不升版偷改正文）。本登记册补上正文字节 digest。
FROZEN_DIGESTS_PATH = os.path.join(ROOT, "contracts/frozen_digests.json")
# contracts/interaction/ 七份文件的控制块都自述「CONTENT-FROZEN（内容定稿）」。P0-2 修复批次实证：
# R11 的送签白名单只是**文件级豁免**（按文件名放行，不看内容），frozen_digests 的旧 _scope 又只登记
# PRD/A/B——于是这七份冻结件的**正文**从头到尾没有任何红线覆盖：把 baseline_prompt_stage_D.md
# 整体替换成 8 行壳（只留版本行与一行 PENDING_RESIGN_P0-6），门照样 GATE_GREEN 并宣称「版本实时解析命中」。
# 故本清单纳入 R10 的同款校验（digest + 声明版本 + version_history 链）。少登记一份即红。
DIGEST_REQUIRED_FROZEN_FILES = (
    "contracts/interaction/README.md",
    "contracts/interaction/anonymity_procedure.md",
    "contracts/interaction/baseline_prompt_stage_C.md",
    "contracts/interaction/baseline_prompt_stage_D.md",
    "contracts/interaction/e2e_interaction_contract.md",
    "contracts/interaction/e2e_output_contract.md",
    "contracts/interaction/generation_parameters.json",
)

# ---- R11：待决标记扫描 ----
# PENDING_IA0：IA-0 冻结前置待办标记。IA-0 已定格后它不得残留在考试条件区（contracts/）
# 与答卷冻结件（Case Manifest）——**两模式同红**，不设送签豁免。
PENDING_IA0_MARK = "PENDING_IA0"
# PENDING_RESIGN_P0-6：M0 收口修复批次 P0-6「Founder 重签」的显式待办标记。
# 运行态一律红（带着未生效的合同跑正式案例 = 假绿）；送签态只允许出现在下列白名单文件——
# 送签的目的正是去拿 P0-6 那个签字，此时这些文件带标记是设计内状态。
PENDING_RESIGN_MARK = "PENDING_RESIGN_P0-6"
# 白名单从「文件级豁免」收窄为「文件 + 允许条数上限」（P0-2 修复批次）：
# 只按文件名放行等于对该文件的内容完全弃权——标记可以从 1 处膨胀到 100 处、从「状态」行扩散到正文任何
# 位置，门都不吭声。上限取 2026-08-17 落盘时的实测条数，**多一处即红**：新增待决点必须显式改这张表
# （= 显式承认「又多了一处没定的东西」），不能顺手混进去。P0-6 Founder 重签后应逐份清零并删表。
PENDING_RESIGN_SIGN_WHITELIST_MAX = {
    "contracts/interaction/README.md": 2,
    "contracts/interaction/anonymity_procedure.md": 2,
    "contracts/interaction/baseline_prompt_stage_C.md": 1,
    "contracts/interaction/baseline_prompt_stage_D.md": 1,
    "contracts/interaction/e2e_interaction_contract.md": 1,
    "contracts/interaction/e2e_output_contract.md": 1,
    "contracts/interaction/generation_parameters.json": 1,
    "contracts/OD-02_模型与参数定格记录.md": 1,
    "IA-0_冻结签字包.md": 3,
    "M0-EP01_文档版本一致性声明.md": 1,
}
# 引述约定（R11 三个面共用）：用反引号整体包住的标记（`PENDING_IA0`）是**引述历史状态**，不算活标记；
# 裸标记算。理由：登记册/说明文档需要引用「当时这里写的是 PENDING_IA0」这一历史事实，
# 靠「把该文件排除出扫描面」来放行等于给整份文件开后门（那正是面一/面二扫描面此前漏掉
# acceptance/cases/ 的成因）。约定是机器可判的，后门不是。
def bare_marker_count(text, mark):
    return text.count(mark) - text.count("`%s`" % mark)
# 20 份 Manifest 同样属白名单成员（路径由 MANIFEST_GLOB 实时枚举，不写死文件名清单），但**上限为 0**——
# 实测 20 份一处都没有该标记，按最紧的实测值封顶；真要新增须显式改上表。
# 扫描范围（明确边界，避免"扫全仓"把工作指令文档也当成考试条件）：
#   contracts/** 全部文件（考试条件区）+ acceptance/cases/** 整棵（答卷区：Manifest / case.yaml /
#   fixtures / 登记册——三个面同一边界，不再一条红线两套口径）+ 上述两份根级冻结声明文档。
#   M0收口修复批次_执行规格.md 是**工作指令文档**（描述 P0-1…P0-6 这批任务本身），不在扫描面内：
#   它提到 P0-6 是在派活，不是在声明某份合同待生效——把它纳入扫描等于禁止用任务编号写工作计划。
PENDING_RESIGN_SCAN_EXTRA_FILES = ("IA-0_冻结签字包.md", "M0-EP01_文档版本一致性声明.md")
# 悬空指针：P0-1 已把 20 份 Manifest 去掉 .draft 命名，答卷区任何 ".draft.yaml" 字面都是指向不存在文件的
# 旧指针（OPEN_QUESTIONS 的行号指针、Manifest 头注释的"草案性载体"句都属此类）。两模式同红，防复发。
DRAFT_POINTER_MARK = ".draft.yaml"
CASES_SCAN_ROOT = os.path.join(ROOT, "acceptance/cases")
# 扫描时跳过的二进制/派生后缀（本仓答卷区目前只有文本，此表是防御性的）
SCAN_SKIP_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".pyc")

# ---- R12：运行身份唯一 ----
# 14 = B 正文现数的锁定案例数（B.4 十一条诊断 + B.5 三条 E2E），与 tools/coverage.py 同源；
# 20 份 Manifest 是这 14 个案例按 Founder 08-17 预裁决①展开的运行变体。改这两个数 = 改考卷。
EXPECTED_DISTINCT_CASE_IDS = 14
# 已撤回的签字时间戳：IA-0 首签 2026-08-17T19:08:38+08:00 于同日随 M0 收口宣告撤回（《裁决台账》08-17）。
# 运行态拿它当有效签字 = 拿被撤回的签字跑正式案例；送签态放行（送签就是去换新签字）。
REVOKED_SIGNATURES = frozenset(["2026-08-17T19:08:38+08:00"])

# ---- R13：需求 × 案例映射完整性 ----
# 需求编号真源 = PRD 全文（⚠️ SYS 系列散落在 6.5 / 7 / 8.3 / 8.4 / 8.5 / 8.6 六处，不是一张连续表，
# 任何"只扫一张表"的实现会漏 5 条）。B.7 是引用侧，须与 PRD 全等。
PRD_DOC = "PRD_笛语智能核_MVP_V3.0_v0.1.md"
B_DOC = "B_三个核心模块智能验收合同.md"
REQ_ID_ROW_RE = re.compile(r"^\|\s*((?:INT|BD|CR|SYS)-\d{2})\s*\|", re.M)
EXPECTED_REQ_COUNT = 30
B7_HEADING = "# B.7 需求与案例映射"
# B.7 右列是中文自然语言：区间「X 至 Y」、集合「全部 E2E」、顿号/逗号分隔、以及非 14 案例的 PRE-xx 前置检查。
CASE_TOKEN_RE = re.compile(r"(?:INT|BD|CR|SYS)-D\d{2}|E2E-\d{2}")
PRE_TOKEN_RE = re.compile(r"PRE-\d{2}(?:-[A-Z])?")
RANGE_RE = re.compile(r"([A-Z0-9]+(?:-[A-Z])?-?\d{2})\s*至\s*([A-Z0-9]+(?:-[A-Z])?-?\d{2})")
ALL_E2E_RE = re.compile(r"全部\s*E2E")
SEGMENT_SPLIT_RE = re.compile(r"[、，,]")


def rel(p):
    return os.path.relpath(p, ROOT)


def case_dir_of(path):
    """acceptance/cases/<CASE>/... → <CASE>；不在该布局下返回 None。"""
    parts = rel(path).replace(os.sep, "/").split("/")
    if len(parts) >= 3 and parts[0] == "acceptance" and parts[1] == "cases":
        return parts[2]
    return None


def blank_or_placeholder(val):
    """R2/R6 共用判据：空白 或 命中占位模式。返回 None 表示通过，否则返回红线原因。"""
    if val is None:
        return "为 null（必填字段不得以 null 充当已填）"
    if not isinstance(val, str):
        return None
    if val.strip() == "":
        return "为空白值（空串/纯空格不算已填）"
    m = PLACEHOLDER_RE.search(val)
    if m:
        return "仍是占位值（命中占位模式 %s）→ %s" % (m.group(0), val.splitlines()[0][:80])
    return None


def parse_iso8601(val):
    """能解析返回 datetime，否则返回 None。Py3.10 的 fromisoformat 不吃 Z 后缀，先归一。"""
    if not isinstance(val, str):
        return None
    s = val.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.datetime.fromisoformat(s)
    except ValueError:
        return None


def canonical_snapshot_hash(path):
    """快照 JSON 的规范化 sha256。规范化 = UTF-8 + 键排序 + 紧凑分隔符（无多余空白）。"""
    with io.open(path, encoding="utf-8") as f:
        obj = json.load(f)
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def walk_values(node, path=""):
    """只遍历解析后的值——注释在此已被 YAML 解析器丢弃，故注释中的占位字样不会误报。"""
    if isinstance(node, dict):
        for k, v in node.items():
            for item in walk_values(v, "%s.%s" % (path, k) if path else str(k)):
                yield item
    elif isinstance(node, list):
        for i, v in enumerate(node):
            for item in walk_values(v, "%s[%d]" % (path, i)):
                yield item
    else:
        yield path, node


def index_snapshots(errors):
    """snapshot_id -> 文件路径。撞车（同一 ID 落在两个文件）直接算红线，不择一。"""
    idx = {}
    for p in sorted(glob.glob(SNAPSHOT_GLOB)):
        try:
            with io.open(p, encoding="utf-8") as f:
                obj = json.load(f)
        except ValueError as e:
            errors.append("R4 快照 JSON 解析失败: %s（%s）" % (rel(p), e))
            continue
        if isinstance(obj, dict) and isinstance(obj.get("snapshot_id"), str):
            sid = obj["snapshot_id"]
            if sid in idx:
                errors.append("R4 快照 ID 撞车: %s 同时出现在 %s 与 %s——无法确定该对哪一份算 hash"
                              % (sid, rel(idx[sid]), rel(p)))
            else:
                idx[sid] = p
    return idx


def index_rules(errors):
    """rule_id -> RuleRecord 对象。文件名与 rule_id 不一致、缺 rule_id、字段集不符 A.9.1 均算红线。"""
    idx = {}
    for p in sorted(glob.glob(RULES_GLOB)):
        try:
            with io.open(p, encoding="utf-8") as f:
                obj = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append("R5 规则文件 YAML 解析失败: %s（%s）" % (rel(p), e))
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("rule_id"), str):
            errors.append("R5 规则文件缺 rule_id，无法建索引: %s" % rel(p))
            continue
        rid = obj["rule_id"]
        if os.path.basename(p) != rid + ".yaml":
            errors.append("R5 规则文件名与 rule_id 不一致: %s 内是 %s" % (rel(p), rid))

        # 字段集必须与 A.9.1 十项全等（机械校验，不看值只看键）
        keys = set(obj.keys())
        missing = sorted(RULE_RECORD_FIELDS_A91 - keys)
        extra = sorted(keys - RULE_RECORD_FIELDS_A91)
        if missing or extra:
            errors.append("R5 %s 的字段集与 A.9.1 RuleRecord 十项不全等: 缺 %s / 多 %s"
                          % (rel(p), missing or "无", extra or "无"))

        if rid in idx:
            errors.append("R5 rule_id 重复登记: %s" % rid)
        else:
            idx[rid] = (obj, p)
    return idx


def mask_noise(text):
    """把代码围栏区段与 HTML 注释整体置空，返回**逐行列表**（行数不变，行号仍可直接引用）。

    围栏里的 `| 版本 | v1.0 |` 是**示例**不是权威版本行；HTML 注释同理。不剔除的话，在文末追加一个
    围栏就能伪造版本行——这是 P0-2 修复批次实测复现过的路径，不是设想。
    """
    text = _HTML_COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    out, in_fence = [], False
    for line in text.split("\n"):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def parse_control_block_version(path):
    """解析一份 Markdown 受控文档的**控制块**版本行。返回 (版本 token, 行号, 错误说明|None)。

    锚定三重（缺一即红，绝不退回默认值）：
      ① 剔除代码围栏与 HTML 注释后再匹配（防「示例行冒充权威行」）；
      ② 只认**第一张**表头为「| 项目 | 内容 |」的表——文档控制块的唯一形态；
      ③ 该表须出现在文件前 CONTROL_BLOCK_MAX_START_LINE 行内。
    行号一并返回并在门的头部打印，让「门读的到底是哪一行」可当场核对（绿灯自带可核验位置）。
    """
    with io.open(path, encoding="utf-8") as f:
        lines = mask_noise(f.read())
    head = None
    for i, line in enumerate(lines):
        if CONTROL_BLOCK_HEADER_RE.match(line.strip()):
            head = i
            break
    if head is None:
        return None, None, "找不到文档控制块表头「| 项目 | 内容 |」（版本行无从锚定；围栏内的示例表不算）"
    if head + 1 > CONTROL_BLOCK_MAX_START_LINE:
        return None, None, ("文档控制块表头出现在第 %d 行，超出前 %d 行的锚定范围"
                            % (head + 1, CONTROL_BLOCK_MAX_START_LINE))
    hits = []
    j = head
    while j < len(lines) and lines[j].strip().startswith("|"):
        m = VERSION_ROW_RE.match(lines[j].strip())
        if m:
            hits.append((m.group(1).strip(), j + 1))
        j += 1
    if len(hits) != 1:
        return None, None, ("控制块表（第 %d-%d 行）内「| 版本 | … |」行解析到 %d 处（应恰好 1 处）"
                            % (head + 1, j, len(hits)))
    cell, lineno = hits[0]
    return extract_version_token(cell) or cell, lineno, None


def resolve_doc_versions(errors, linenos=None):
    """实时解析三份真源文档控制块的版本号。解析不到 / 多于一处 = 红线，不退回默认值。"""
    versions = {}
    for field, docname in VERSION_SOURCES:
        path = os.path.join(ROOT, docname)
        if not os.path.exists(path):
            errors.append("R7 真源文档缺失: %s（%s 无从核验）" % (docname, field))
            continue
        token, lineno, err = parse_control_block_version(path)
        if err:
            errors.append("R7 %s 的%s，%s 无从核验" % (docname, err, field))
            continue
        versions[field] = token
        if linenos is not None:
            linenos[docname] = lineno
    return versions


# ============================================================================
# R8-R13 加固区（M0 收口修复批次 P0-2）
# 共同纪律：一律**实时重算/实时解析**真源，脚本内不留任何基线常量式的期望值——
# 硬编码期望值会在真源改动后继续判绿，这正是本批次要堵的假绿本体。
# ============================================================================

def schema_nullable_paths(schema):
    """从 Schema 反推「type 明示含 null」的字段路径（顶层 + 一层嵌套对象）。

    为什么需要：B.2.1（B:146-150）把 e2e_interaction_contract_version / e2e_output_contract_version /
    baseline_prompt_versions.decision_stage / .creative_stage / model_version 定义为 `string | null`
    ——键必须在，值允许为 null。P0-2 把前三项补进 Schema.required 后，R2 的「不得以 null 充当已填」
    会把 17 份非 E2E Manifest 的合法 null 判成红线。故 R2 的 null 判据要认 Schema 的显式可空声明。
    放宽的只是"null 本身合法"，不是"随便填什么都行"：E2E 必须非 null、非 E2E 必须为 null、
    非 null 时版本号必须在 contracts/interaction/ 真源里实际存在——三条全部由 R9 实时核验。
    """
    out = set()

    def is_nullable(sub):
        t = sub.get("type")
        return t == "null" or (isinstance(t, list) and "null" in t)

    for name, sub in (schema.get("properties") or {}).items():
        if not isinstance(sub, dict):
            continue
        if is_nullable(sub):
            out.add(name)
        for cname, csub in (sub.get("properties") or {}).items():
            if isinstance(csub, dict) and is_nullable(csub):
                out.add("%s.%s" % (name, cname))
    return out


def extract_version_token(cell):
    """从文档控制块版本行的单元格取版本号 token。

    控制块里的取值可能带 Markdown 强调与括注，例如 `**v1.0**（同时是 … 的取值）`。
    只认**行首**的 `vN[.N…]`，不从整句里随便捞一个 v 开头的串（那样容易把正文里的别的版本号当成本文件版本）。
    """
    s = cell.replace("*", "").replace("`", "").strip()
    m = VERSION_TOKEN_RE.match(s)
    return m.group(0) if m else None


def resolve_interaction_versions(errors, linenos=None):
    """R9：实时解析 contracts/interaction/ 四份真源文件控制块的版本号。

    返回 {manifest 字段路径: 版本号}；解析不到的字段不进字典（已记红，不退回默认值）。
    解析走 parse_control_block_version——剔围栏 + 锁控制块表 + 回报行号，与 R7/R10 同一实现。
    """
    out = {}
    for field, relpath in INTERACTION_VERSION_SOURCES:
        path = os.path.join(ROOT, relpath)
        if not os.path.exists(path):
            errors.append("R9 交互合同真源缺失: %s（%s 无从核验）" % (relpath, field))
            continue
        token, lineno, err = parse_control_block_version(path)
        if err:
            errors.append("R9 %s 的%s，%s 无从核验" % (relpath, err, field))
            continue
        if not VERSION_TOKEN_RE.match(token):
            errors.append("R9 %s 的版本行取值 %r 不是 vN.N 形态的版本号，%s 无从核验"
                          % (relpath, token, field))
            continue
        out[field] = token
        if linenos is not None:
            linenos[relpath] = lineno
    return out


def sha256_file_bytes(path):
    """真源正文的**字节** sha256（不做任何规范化——正文是 Markdown，改一个字就该变）。"""
    with io.open(path, "rb") as f:
        return "sha256:" + hashlib.sha256(f.read()).hexdigest()


def version_chain_link(prev_chain, declared_version, digest):
    """version_history 的链式指纹：chain_n = sha256(chain_{n-1} | declared_version | digest)。

    为什么要链而不是只存一张表（P0-2 修复批次实测的 R10 旁路本体）：
    「改正文 + 同步登记册 sha256 + 不升版」是最自然的『把门弄绿』反射动作，横向比对（登记值 == 实算值）
    对它完全无感——两边都是新值，永远相等。链把「同一个 declared_version 在历史上对应过哪个 digest」
    也变成机器可查的事实：不升版就改正文，必须同时改掉历史条目并重算整条链，
    而重算工具本仓不提供、链头一动全链皆变、且登记册进 git 后 diff 会把重写整条历史暴露在评审面前。
    诚实边界（不夸大）：这不是密码学不可伪造——知道算法的人能手工重算。它把「顺手弄绿」变成
    「显式重写冻结历史」，配合登记册纳入版本控制后的 diff 可见性构成拦截，**不是**单文件内的绝对防篡改。
    """
    base = "%s|%s|%s" % (prev_chain or "", declared_version, digest)
    return "sha256:" + hashlib.sha256(base.encode("utf-8")).hexdigest()


def registered_live_version(docname, path, entry, doc_versions_by_doc):
    """取一条登记项对应文件的**实时**版本号。返回 (版本, 错误说明|None)。

    version_from 支持两种（登记册里显式声明，不靠猜文件类型）：
      · doc_control_block（默认）：Markdown 文档控制块的版本行（parse_control_block_version）；
      · json_field:<字段名>：JSON 文件里某个字段的取值（generation_parameters.json 的 `_version`）。
    """
    if docname in doc_versions_by_doc and doc_versions_by_doc[docname] is not None:
        return doc_versions_by_doc[docname], None
    spec = entry.get("version_from") or "doc_control_block"
    if spec.startswith("json_field:"):
        field = spec.split(":", 1)[1]
        try:
            with io.open(path, encoding="utf-8") as f:
                obj = json.load(f)
        except ValueError as e:
            return None, "JSON 解析失败（%s）" % e
        if not isinstance(obj, dict) or not isinstance(obj.get(field), str):
            return None, "JSON 里取不到字符串字段 %r" % field
        return obj[field], None
    if spec != "doc_control_block":
        return None, "version_from=%r 不是受支持的取值（doc_control_block / json_field:<字段>）" % spec
    token, _lineno, err = parse_control_block_version(path)
    if err:
        return None, err
    return token, None


def check_frozen_digests(errors, doc_versions):
    """R10：冻结件的正文 digest、声明版本、以及**版本↔digest 的历史绑定**三者同时与登记册核对。

    R7 只核验版本行，改正文而不动版本行时 R7 判不出来（不升版偷改正文）；本条补上正文字节 digest。
    登记册本身也要自洽：登记的声明版本必须等于文件实时解析出来的版本；
    且 version_history 必须是**只增**的链——同一 declared_version 二次登记出不同 digest 即红。
    覆盖面：PRD/A/B 三份冻结真源 + contracts/interaction/ 全部自称 CONTENT-FROZEN 的冻结件
    （P0-2 修复批次实证：白名单是文件级豁免，那批合同的**正文**此前零红线覆盖，可被整体掏空而门仍绿）。
    """
    if not os.path.exists(FROZEN_DIGESTS_PATH):
        errors.append("R10 真源 digest 登记册缺失: %s（正文是否被偷改无从核验）" % rel(FROZEN_DIGESTS_PATH))
        return
    try:
        with io.open(FROZEN_DIGESTS_PATH, encoding="utf-8") as f:
            reg = json.load(f)
    except ValueError as e:
        errors.append("R10 真源 digest 登记册 JSON 解析失败: %s（%s）" % (rel(FROZEN_DIGESTS_PATH), e))
        return
    docs = reg.get("documents")
    if not isinstance(docs, dict):
        errors.append("R10 %s 缺 documents 映射，无从核验" % rel(FROZEN_DIGESTS_PATH))
        return

    # 登记册必须覆盖 R7 的三份真源 + 全部 CONTENT-FROZEN 冻结件——少登记一份 = 那份正文不受保护
    for field, docname in VERSION_SOURCES:
        if docname not in docs:
            errors.append("R10 真源 digest 登记册未登记 %s（%s 对应的正文不受 digest 保护）" % (docname, field))
    for relpath in DIGEST_REQUIRED_FROZEN_FILES:
        if relpath not in docs:
            errors.append("R10 真源 digest 登记册未登记冻结件 %s（该文件自称 CONTENT-FROZEN，"
                          "正文却不受任何红线保护——可被整体改写/掏空而门仍绿）" % relpath)

    version_by_doc = {docname: doc_versions.get(field) for field, docname in VERSION_SOURCES}
    for docname in sorted(docs):
        entry = docs[docname]
        path = os.path.join(ROOT, docname)
        if not isinstance(entry, dict):
            errors.append("R10 登记项 %s 不是对象" % docname)
            continue
        if not os.path.exists(path):
            errors.append("R10 登记册指向不存在的文件: %s" % docname)
            continue
        declared_digest = entry.get("sha256")
        actual_digest = sha256_file_bytes(path)
        if declared_digest != actual_digest:
            errors.append("R10 %s 正文 digest 与登记不符（不升版偷改正文 / 或改了正文未同步登记册）"
                          "\n      登记 %s\n      实算 %s" % (docname, declared_digest, actual_digest))
        declared_version = entry.get("declared_version")
        live_version, verr = registered_live_version(docname, path, entry, version_by_doc)
        if verr:
            errors.append("R10 %s 的%s，登记版本 %r 无从核验" % (docname, verr, declared_version))
        elif declared_version != live_version:
            errors.append("R10 %s 登记的 declared_version=%r ≠ 文件实时解析 %r"
                          % (docname, declared_version, live_version))

        # ---- 版本 ↔ digest 的单调绑定（append-only 链）----
        hist = entry.get("version_history")
        if not isinstance(hist, list) or not hist:
            errors.append("R10 %s 缺 version_history（非空列表）——没有历史绑定，"
                          "『改正文 + 同步 sha256 + 不升版』这条最自然的把门弄绿路径就无人拦" % docname)
            continue
        chain = None
        seen_by_version = {}
        broken = False
        for i, h in enumerate(hist):
            if not isinstance(h, dict):
                errors.append("R10 %s version_history[%d] 不是对象" % (docname, i)); broken = True; break
            hv, hd, hc = h.get("declared_version"), h.get("sha256"), h.get("chain")
            if not isinstance(hv, str) or not isinstance(hd, str):
                errors.append("R10 %s version_history[%d] 缺 declared_version / sha256"
                              % (docname, i)); broken = True; break
            if hv in seen_by_version and seen_by_version[hv] != hd:
                errors.append("R10 %s version_history 里 declared_version=%s 二次登记出不同 digest"
                              "（%s ≠ %s）——同一版本号对应两份正文 = 不升版偷改正文"
                              % (docname, hv, seen_by_version[hv], hd)); broken = True; break
            seen_by_version[hv] = hd
            want_chain = version_chain_link(chain, hv, hd)
            if hc != want_chain:
                errors.append("R10 %s version_history[%d]（%s）的 chain 与实算不符——"
                              "冻结历史被改写过\n      登记 %s\n      实算 %s"
                              % (docname, i, hv, hc, want_chain)); broken = True; break
            chain = want_chain
        if broken:
            continue
        last = hist[-1]
        if (last.get("declared_version"), last.get("sha256")) != (declared_version, declared_digest):
            errors.append("R10 %s 当前登记 (%s, %s) ≠ version_history 末条 (%s, %s)——"
                          "改了正文并同步了 sha256，却没有作为新版本追加进历史（不升版偷改正文的指纹）"
                          % (docname, declared_version, declared_digest,
                             last.get("declared_version"), last.get("sha256")))


def collect_scan_files(root_dir, skipped=None):
    """递归收集一棵目录下的文本文件（用于 R11 的字面扫描）。

    skipped：传入一个 list 时，按后缀跳过的文件路径会**逐条记入**并由门打印条数——
    「跳过」是一种未核验状态，不打印出来就等于悄悄缩小扫描面（同 read_text_or_failure 的三态纪律）。
    """
    out = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if fn.endswith(SCAN_SKIP_SUFFIXES):
                if skipped is not None:
                    skipped.append(rel(p))
                continue
            out.append(p)
    return sorted(out)


def read_text_or_failure(path, errors, rule):
    """读不出来 ≠ 干净：解码/IO 失败一律记红，禁止裸 continue（P0-2 修复批次实证的三态破口）。

    复现过的假绿：往 contracts/ 写一份 GBK 编码、内容含 PENDING_IA0 的文件 → 旧实现 return None →
    调用点 `if text is None: continue` → GATE_GREEN，末行照旧宣称「待决标记与悬空指针清零」。
    """
    try:
        with io.open(path, encoding="utf-8") as f:
            return f.read()
    except (UnicodeDecodeError, OSError) as e:
        errors.append("%s %s 无法按 UTF-8 读取（%s: %s）——待决标记/悬空指针无从核验，"
                      "读不出来不等于干净" % (rule, rel(path), type(e).__name__, e))
        return None


def check_pending_marks(errors, notes, mode, manifests):
    """R11：待决标记与悬空指针的字面扫描（含注释——注释里的待决标记同样会误导人）。

    与 R2 的分工：R2 只看 YAML 解析后的**值**（注释是说明不是考试条件）；R11 扫的是"这份文件整体
    还处在待决态"这一事实，注释里写着 PENDING_IA0 同样意味着该文件没定格，故按字面扫。
    扫描面（P0-2 修复批次对齐）：三个面统一为 contracts/** + acceptance/cases/**（整棵，含 case.yaml /
    fixtures / OPEN_QUESTIONS）+ 两份根级冻结声明。此前面一/面二只扫 contracts + 20 份 Manifest，
    而面三扫整棵 cases 树——同一条红线两套边界，实测可在 case.yaml 里塞 PENDING_IA0 而门仍绿
    （case.yaml 承载断言清单与 tag，是比 Manifest 更硬的考试条件）。
    引述豁免只有一种：`标记`（反引号整体包裹）。见 bare_marker_count。
    """
    skipped = []
    contracts_files = collect_scan_files(os.path.join(ROOT, "contracts"), skipped)
    cases_files = collect_scan_files(CASES_SCAN_ROOT, skipped)
    root_files = [os.path.join(ROOT, fn) for fn in PENDING_RESIGN_SCAN_EXTRA_FILES
                  if os.path.exists(os.path.join(ROOT, fn))]
    scan_targets = sorted(set(contracts_files + cases_files + [os.path.abspath(m) for m in manifests]
                              + root_files))
    if skipped:
        notes.append("R11 扫描面按后缀跳过 %d 个文件（%s）：%s——跳过 = 未核验，不等于干净"
                     % (len(skipped), "/".join(SCAN_SKIP_SUFFIXES), "、".join(sorted(skipped)[:8])))

    texts = {}
    for p in scan_targets:
        t = read_text_or_failure(p, errors, "R11")
        if t is not None:
            texts[p] = t

    # ---- 面一：PENDING_IA0（考试条件区 + 整棵答卷区），两模式同红 ----
    for p in scan_targets:
        text = texts.get(p)
        if text is None:
            continue
        n = bare_marker_count(text, PENDING_IA0_MARK)
        if n:
            errors.append("R11 %s: 残留裸 %s × %d 处——IA-0 已定格，考试条件区与答卷区不得再带 IA-0 冻结待办标记"
                          "（引述历史状态请用反引号包裹）" % (rel(p), PENDING_IA0_MARK, n))

    # ---- 面二：PENDING_RESIGN_P0-6（运行态红 / 送签态白名单，且受条数上限约束）----
    manifest_names = {rel(m) for m in manifests}
    whitelisted_hits = []
    for p in scan_targets:
        text = texts.get(p)
        if text is None:
            continue
        n = bare_marker_count(text, PENDING_RESIGN_MARK)
        if not n:
            continue
        name = rel(p)
        # 白名单成员 = 静态表里的 10 份 + 20 份 Manifest。Manifest 的上限取 0：实测当前 20 份一处都没有，
        # 「设计上允许标注行」在事实层面从未被用到，按最紧的实测值设上限——真要新增就显式改表。
        in_whitelist = name in PENDING_RESIGN_SIGN_WHITELIST_MAX or name in manifest_names
        cap = PENDING_RESIGN_SIGN_WHITELIST_MAX.get(name, 0)
        if mode == "sign" and in_whitelist:
            if n > cap:
                errors.append("R11 %s: 残留 %s × %d 处，超出白名单上限 %d 处——白名单是「文件 + 条数上限」，"
                              "不是对该文件内容的整体弃权；新增待决点必须显式改 "
                              "PENDING_RESIGN_SIGN_WHITELIST_MAX（= 显式承认又多了一处没定的东西）"
                              % (name, PENDING_RESIGN_MARK, n, cap))
            else:
                whitelisted_hits.append((name, n))
            continue
        errors.append("R11 %s: 残留 %s × %d 处（运行态：合同未生效即开跑 = 假绿；送签态：该文件不在白名单）"
                      % (name, PENDING_RESIGN_MARK, n))
    if whitelisted_hits:
        notes.append("R11 送签态放行 %s：%d 份白名单文件仍带该标记（逐份实测 %s；均未超上限）——"
                     "P0-6 Founder 重签后须逐份清零，运行态届时才可能转绿"
                     % (PENDING_RESIGN_MARK, len(whitelisted_hits),
                        "、".join("%s×%d" % (n, c) for n, c in sorted(whitelisted_hits))))

    # ---- 面三：答卷区的 .draft.yaml 悬空指针，两模式同红 ----
    for p in cases_files:
        text = texts.get(p)
        if text is None:
            continue
        n = bare_marker_count(text, DRAFT_POINTER_MARK)
        if n:
            errors.append("R11 %s: 出现裸 %r × %d 处——P0-1 后答卷区已无 .draft 命名文件，"
                          "该字面即指向不存在文件的悬空指针" % (rel(p), DRAFT_POINTER_MARK, n))


def check_identity(errors, notes, mode, identities):
    """R12：运行身份唯一 + 已撤回签字拦截。

    identities: [(manifest 相对路径, case_id, 文件名, 所在案例目录, approved_at)]

    为什么要把 case_id 焊到案例目录上：「不同 case_id 恰 14 个」这一条单独看是**可以被排列绕过**的
    ——把 BD-D01/manifest.yaml 的 case_id 改成任意新值、再把别处改回来，计数仍是 14，但每份 Manifest
    声明的身份已经和它所在的案例对不上，运行证据无法归属（本条即由 P0-2 的负向变异回归实测撞出来的洞）。
    目录是文件系统上的硬事实，case_id 是文件里的自述——两者必须一致，计数才有意义。
    """
    for name, case_id, _b, case_dir, _at in identities:
        if case_dir is not None and case_id != case_dir:
            errors.append("R12 %s: case_id=%r 与所在案例目录 %r 不一致——Manifest 自述的身份和它挂靠的案例对不上，"
                          "运行证据无法归属（『不同 case_id 恰 %d 个』若不焊死目录，任意排列都能凑够数）"
                          % (name, case_id, case_dir, EXPECTED_DISTINCT_CASE_IDS))

    seen = {}
    for name, case_id, basename, _case_dir, _at in identities:
        key = (case_id, basename)
        if key in seen:
            errors.append("R12 运行身份撞车: (case_id=%s, 文件名=%s) 同时出现在 %s 与 %s"
                          "——两份 Manifest 指向同一次运行，证据无法归属" % (case_id, basename, seen[key], name))
        else:
            seen[key] = name

    distinct = {case_id for _n, case_id, _b, _d, _a in identities if case_id is not None}
    if len(distinct) != EXPECTED_DISTINCT_CASE_IDS:
        errors.append("R12 不同 case_id 数 = %d ≠ 应有 %d（20 份运行 Manifest 必须恰好覆盖 %d 个锁定案例；"
                      "多了 = 私加案例，少了 = 有案例没考）：实际 %s"
                      % (len(distinct), EXPECTED_DISTINCT_CASE_IDS, EXPECTED_DISTINCT_CASE_IDS,
                         "、".join(sorted(distinct))))

    revoked = [name for name, _c, _b, _d, at in identities if at in REVOKED_SIGNATURES]
    if revoked:
        if mode == "sign":
            notes.append("R12 送签态放行已撤回签字：%d 份 Manifest 的 approved_at 仍是已撤回的首签时间戳 %s，"
                         "须由 P0-6 Founder 重签后同批更新（运行态对此判红）"
                         % (len(revoked), "、".join(sorted(REVOKED_SIGNATURES))))
        else:
            for name in revoked:
                errors.append("R12 %s: approved_at 命中已撤回的签字时间戳（《裁决台账》08-17 撤回 M0 收口宣告），"
                              "拿被撤回的签字跑正式案例 = 假绿" % name)


def check_generation_params_placeholders(errors):
    """R2（扫描面补齐）：contracts/interaction/generation_parameters.json 的取值不得是占位。

    P0-2 修复批次实证的假绿：R8 只比对哈希一致性、从不看取值是不是占位；R2 的占位判据只作用于
    **Manifest 解析后的值**，扫描面不含这个文件。于是把 model_name 改成 "TBD"、model_version 改成
    "待定"、seed 改成 "TODO"，再按门自己的算法重算指纹并同步 20 份 Manifest → GATE_GREEN、exit 0，
    收尾行照旧宣称「零占位残留」。OD-02「模型与参数定格」因此可被完全架空，
    而这正是 R2 要堵的「带着占位签字」，只是换了个文件承载。
    `_` 开头的元数据字段只豁免 PENDING_RESIGN_P0-6 这一枚举值（P0-6 待重签是设计内状态），其余一律红。
    """
    if not os.path.exists(GENERATION_PARAMS_PATH):
        return                                   # 文件缺失已由 R8 记红
    try:
        with io.open(GENERATION_PARAMS_PATH, encoding="utf-8") as f:
            obj = json.load(f)
    except ValueError:
        return                                   # JSON 解析失败已由 R8 记红
    name = rel(GENERATION_PARAMS_PATH)
    for fpath, val in walk_values(obj):
        top = fpath.split(".")[0].split("[")[0]
        probe = val
        if isinstance(val, str) and top.startswith("_"):
            probe = val.replace(PENDING_RESIGN_MARK, "")
        reason = blank_or_placeholder(probe)
        if reason is None:
            continue
        errors.append("R2 %s: 字段 %s %s（生成参数真源带着占位 = OD-02 模型与参数定格被架空，"
                      "指纹再一致也只是把占位的哈希对齐了）" % (name, fpath, reason))


# ---- R1：齐套份数的机器断言（不只比脚本常量）----
# IA-0_冻结签字包.md §五把「Manifest 实测份数 == 齐套口径**声明**份数」列为 P0-2 交付项，原文点名
# 「R1 比对的是脚本常量 EXPECTED_MANIFESTS、不是解析出的声明份数」。本表把三份真源里的声明份数
# 逐一解析出来与常量比对：常量与真源任一处对不上即红。这样「改常量 = 改考卷」这条纪律有了检测器，
# 不再只是散文——改常量而不改真源（或反之）会当场被拦。
DECLARED_COUNT_SOURCES = (
    ("IA-0_冻结签字包.md", "§五 齐套定义",
     re.compile(r"齐套[＝=](\d+)\s*案例\s*↔\s*(\d+)\s*份运行\s*Manifest"), ("cases", "manifests")),
    ("acceptance/cases/OPEN_QUESTIONS.md", "文首预裁决①",
     re.compile(r"INT-D01\s*补\s*QUICK\s*分支变体，总\s*(\d+)\s*份"), ("manifests",)),
    ("contracts/OD-02_模型与参数定格记录.md", "§三 定格执行留痕第 2 条",
     re.compile(r"实测版本串填入\s*(\d+)\s*份\s*Case\s*Manifest"), ("manifests",)),
)


def check_declared_counts(errors):
    """R1 自校验：脚本常量 == 三份真源里**书面声明**的份数/案例数。"""
    for relpath, where, pattern, kinds in DECLARED_COUNT_SOURCES:
        path = os.path.join(ROOT, relpath)
        if not os.path.exists(path):
            errors.append("R1 齐套口径真源缺失: %s（%s 的声明份数无从核验）" % (relpath, where))
            continue
        with io.open(path, encoding="utf-8") as f:
            text = f.read().replace("*", "")      # 去 Markdown 强调，声明句本身不变
        found = pattern.findall(text)
        if len(found) != 1:
            errors.append("R1 %s 的%s解析到 %d 处齐套声明（应恰好 1 处）——声明份数无从核验，"
                          "EXPECTED_MANIFESTS=%d 便成了无真源支撑的孤儿常量"
                          % (relpath, where, len(found), EXPECTED_MANIFESTS))
            continue
        values = found[0] if isinstance(found[0], tuple) else (found[0],)
        for kind, raw in zip(kinds, values):
            want = EXPECTED_DISTINCT_CASE_IDS if kind == "cases" else EXPECTED_MANIFESTS
            const = "EXPECTED_DISTINCT_CASE_IDS" if kind == "cases" else "EXPECTED_MANIFESTS"
            if int(raw) != want:
                errors.append("R1 %s 的%s声明 %s 数 = %s，但脚本常量 %s = %d——"
                              "改常量 = 改考卷，常量与真源必须同批改；两者打架时门不得替任何一方拍板"
                              % (relpath, where, kind, raw, const, want))


def read_head_commit():
    """只读 .git 目录取当前 HEAD 提交号（**不执行任何 git 命令**）。取不到返回 None。

    linked worktree（`git worktree add` 出来的树）口径（本批次实测修复）：
      .git 是一行 `gitdir: <path>`，指向 <main>/.git/worktrees/<name>/。该目录里**只有 HEAD**；
      分支引用 refs/ 与 packed-refs 住在 common dir（<main>/.git/，由同目录下的 `commondir`
      文件指出）。此前只在 per-worktree 目录里找 refs，导致 worktree 上恒返回 None——
      归属行会打成"非 git 工作区 / HEAD 取不到"，一段 GATE_GREEN 贴进签字包后无法绑定提交。
      现在：HEAD 读 per-worktree 目录；ref 解析按 [per-worktree, commondir] 顺序找。
    """
    gitdir = os.path.join(ROOT, ".git")
    try:
        if os.path.isfile(gitdir):               # worktree：.git 是一行 gitdir: <path>
            with io.open(gitdir, encoding="utf-8") as f:
                raw = f.read().split("gitdir:", 1)[1].strip()
            # 相对路径按 **ROOT** 解析，不按进程 cwd
            gitdir = raw if os.path.isabs(raw) else os.path.normpath(os.path.join(ROOT, raw))
        if not os.path.isdir(gitdir):
            return None
        search_dirs = [gitdir]
        cpath = os.path.join(gitdir, "commondir")
        if os.path.isfile(cpath):
            with io.open(cpath, encoding="utf-8") as f:
                c = f.read().strip()
            if c:
                common = c if os.path.isabs(c) else os.path.normpath(os.path.join(gitdir, c))
                if os.path.isdir(common) and os.path.realpath(common) != os.path.realpath(gitdir):
                    search_dirs.append(common)
        with io.open(os.path.join(gitdir, "HEAD"), encoding="utf-8") as f:
            head = f.read().strip()
        if not head.startswith("ref:"):
            return head
        ref = head.split(" ", 1)[1].strip()
        for d in search_dirs:
            refpath = os.path.join(d, ref)
            if os.path.exists(refpath):
                with io.open(refpath, encoding="utf-8") as f:
                    return f.read().strip()
        for d in search_dirs:
            packed = os.path.join(d, "packed-refs")
            if os.path.exists(packed):
                with io.open(packed, encoding="utf-8") as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) == 2 and parts[1] == ref:
                            return parts[0]
    except (OSError, UnicodeDecodeError, IndexError):
        return None
    return None


def attribution_block():
    """归属证据行：这段 GATE_GREEN/GATE_RED 到底扫的是**哪一棵树**、对应哪个提交。

    为什么必须打印（P0-2 修复批次实证）：ROOT 由 __file__ 推出，把脚本连同副本树放在任何位置执行都会
    静默改变扫描面（负向变异套件正是靠这个特性工作，说明这条路径真实可用）。不打印 ROOT 与提交号时，
    一段 GATE_GREEN 文本贴进签字包后**无法证明**它扫的是真仓那棵树的哪个版本。
    诚实边界：HEAD 是从 .git 文件直接读的（本门不执行任何外部命令），它只说明 ROOT 所在仓库的
    当前提交指针；**本门核验的是工作区目录树的实际内容，不是该提交的内容**——两者是否一致
    由干净 clone 回执证明（P0-6），不由本行证明。
    """
    head = read_head_commit()
    lines = ["扫描根 ROOT | %s" % os.path.realpath(ROOT),
             "仓库 HEAD  | %s（读自 .git，未执行 git 命令）" % (head or "非 git 工作区 / HEAD 取不到"),
             "归属口径   | 本门核验的是**上述目录树的当前工作区内容**，不等同于 HEAD 提交的内容；"
             "干净 clone 一致性由 P0-6 回执证明"]
    return "\n".join(lines)


def expand_case_range(lo_tok, hi_tok):
    """把「INT-D01 至 INT-D03」这类区间展开成 token 列表；端点不同族或倒序返回 None。"""
    m1 = re.match(r"^(.*?)(\d+)$", lo_tok)
    m2 = re.match(r"^(.*?)(\d+)$", hi_tok)
    if not m1 or not m2 or m1.group(1) != m2.group(1):
        return None
    width = len(m1.group(2))
    lo, hi = int(m1.group(2)), int(m2.group(2))
    if hi < lo:
        return None
    return ["%s%s" % (m1.group(1), str(i).zfill(width)) for i in range(lo, hi + 1)]


def parse_b7_cell(req, cell, case_dirs, errors):
    """解析 B.7 右列的中文自然语言，返回 (命中的案例目录集合, 命中的 PRE 前置检查集合)。

    支持：顿号/逗号分隔、区间「X 至 Y」、集合「全部 E2E」、PRE-xx 前置检查（合法但不是 14 案例之一）、
    以及「BD-D01 的两候选降级分支」这类带修饰语的写法。
    任何解析不出东西的片段一律记红——**宁可报错也不静默跳过**（静默跳过 = 少算一条映射的假绿）。
    """
    cases, pres = set(), set()
    for seg in SEGMENT_SPLIT_RE.split(cell):
        seg = seg.strip()
        if not seg:
            continue
        hit = False
        if ALL_E2E_RE.search(seg):
            e2e = {c for c in case_dirs if c.startswith(E2E_CASE_PREFIX)}
            if not e2e:
                errors.append("R13 B.7 %s 写了「全部 E2E」，但 acceptance/cases/ 下没有任何 E2E 案例目录" % req)
            cases |= e2e
            hit = True
        if "至" in seg:
            m = RANGE_RE.search(seg)
            if m is None:
                errors.append("R13 B.7 %s 右列出现区间写法但无法解析: %r" % (req, seg))
                continue
            expanded = expand_case_range(m.group(1), m.group(2))
            if expanded is None:
                errors.append("R13 B.7 %s 区间端点不同族或倒序: %r" % (req, seg))
                continue
            for tok in expanded:
                if tok in case_dirs:
                    cases.add(tok)
                else:
                    errors.append("R13 B.7 %s 区间 %r 展开出 acceptance/cases/ 下不存在的案例目录 %s"
                                  % (req, seg, tok))
            hit = True
        for tok in CASE_TOKEN_RE.findall(seg):
            if tok in case_dirs:
                cases.add(tok)
            else:
                errors.append("R13 B.7 %s 引用了 acceptance/cases/ 下不存在的案例目录 %s" % (req, tok))
            hit = True
        pre = PRE_TOKEN_RE.findall(seg)
        if pre:
            pres.update(pre)
            hit = True
        if not hit:
            errors.append("R13 B.7 %s 右列片段既解析不出案例也解析不出 PRE 前置检查: %r" % (req, seg))
    return cases, pres


def check_requirement_mapping(errors, case_dirs):
    """R13：30 条核心需求编号 × 14 个案例目录的映射完整性。

    真源分工：PRD 全文 = 需求编号的**定义处**（⚠️SYS 系列散落六处，不是一张连续表）；
    B.7 = 引用侧，左列须与 PRD 全等；B.7 尾注「每条核心需求至少有一个明确验收映射」是本条的判据来源。
    """
    prd_path = os.path.join(ROOT, PRD_DOC)
    b_path = os.path.join(ROOT, B_DOC)
    for p, label in ((prd_path, PRD_DOC), (b_path, B_DOC)):
        if not os.path.exists(p):
            errors.append("R13 真源文档缺失: %s（需求映射无从核验）" % label)
            return
    with io.open(prd_path, encoding="utf-8") as f:
        prd_text = f.read()
    with io.open(b_path, encoding="utf-8") as f:
        b_text = f.read()

    prd_ids = REQ_ID_ROW_RE.findall(prd_text)
    dups = sorted({i for i in prd_ids if prd_ids.count(i) > 1})
    if dups:
        errors.append("R13 PRD 的核心需求编号有重复: %s" % "、".join(dups))
    prd_set = set(prd_ids)
    if len(prd_set) != EXPECTED_REQ_COUNT:
        errors.append("R13 PRD 全文提取到 %d 条核心需求编号 ≠ 应有 %d 条（B:990「30 条核心需求编号一致」；"
                      "SYS 系列散落 6.5/7/8.3/8.4/8.5/8.6 六处，只扫一张表会漏 5 条）"
                      % (len(prd_set), EXPECTED_REQ_COUNT))

    start = b_text.find(B7_HEADING)
    if start < 0:
        errors.append("R13 B 文档找不到「%s」小节，需求映射无从核验" % B7_HEADING)
        return
    rest = b_text[start + len(B7_HEADING):]
    nxt = re.search(r"^# ", rest, re.M)
    section = rest[:nxt.start()] if nxt else rest

    rows = re.findall(r"^\|\s*((?:INT|BD|CR|SYS)-\d{2})\s*\|([^|]*)\|\s*$", section, re.M)
    b7_ids = [r[0] for r in rows]
    b7_dups = sorted({i for i in b7_ids if b7_ids.count(i) > 1})
    if b7_dups:
        errors.append("R13 B.7 表左列有重复需求编号: %s" % "、".join(b7_dups))
    b7_set = set(b7_ids)
    if b7_set != prd_set:
        only_prd = sorted(prd_set - b7_set)
        only_b7 = sorted(b7_set - prd_set)
        errors.append("R13 B.7 表左列与 PRD 需求编号不全等（B:989 要求主 PRD / 附录 A / 本合同互相引用一致）："
                      "PRD 有而 B.7 无 %s / B.7 有而 PRD 无 %s" % (only_prd or "无", only_b7 or "无"))

    mapped_cases = set()
    for req, cell in rows:
        cases, pres = parse_b7_cell(req, cell, case_dirs, errors)
        mapped_cases |= cases
        if not cases and not pres:
            errors.append("R13 B.7 %s 零映射（B.7 尾注：每条核心需求至少有一个明确验收映射）" % req)
    unmapped = sorted(case_dirs - mapped_cases)
    if unmapped:
        errors.append("R13 以下案例目录在 B.7 中零映射（有案例却没有任何需求指向它 = 考了没人要的题）: %s"
                      % "、".join(unmapped))


# 双模式（Founder 2026-08-17 IA-0 裁决批准，属改考卷）：
# run（默认）= 运行前全查；sign = IA-0 送签态，仅豁免下列 4 个"运行前补填"字段——
# 且豁免的前提是取值**恰为** PENDING_BUILD（声明性标记）；任何其他占位/空值仍判红。
RUN_TIME_FIELDS = frozenset([
    "diyu_build_version",
    "module_contract_versions.intent",
    "module_contract_versions.business_decision",
    "module_contract_versions.creative",
])


def main():
    args = sys.argv[1:]
    mode = "run"
    if args == ["--mode=sign"]:
        mode = "sign"
    elif args:
        print("冻结断言门只接受 --mode=sign（送签态）或无参数（运行态全查）。"
              "收到: %s" % " ".join(args), file=sys.stderr)
        return 1

    expected = EXPECTED_MANIFESTS
    errors = []
    notes = []          # 非红线的提示（送签态豁免留痕）——提示不参与退出码，但必须打印，不许静默
    identities = []     # R12 用：(相对路径, case_id, 文件名, approved_at)
    manifests = sorted(glob.glob(MANIFEST_GLOB))

    # ---- R1 齐套 ----
    if len(manifests) != expected:
        errors.append("R1 齐套数不符: 实际 %d 份 ≠ 应有 %d 份（缺任一变体不得计齐套）" % (len(manifests), expected))

    check_declared_counts(errors)

    snap_idx = index_snapshots(errors)
    rule_idx = index_rules(errors)
    version_linenos = {}
    doc_versions = resolve_doc_versions(errors, version_linenos)
    interaction_versions = resolve_interaction_versions(errors, version_linenos)

    # ---- R8 生成参数指纹：按真源文件当前内容实时重算（不留基线常量）----
    if os.path.exists(GENERATION_PARAMS_PATH):
        try:
            live_params_hash = canonical_snapshot_hash(GENERATION_PARAMS_PATH)
        except ValueError as e:
            live_params_hash = None
            errors.append("R8 生成参数真源 JSON 解析失败: %s（%s）" % (rel(GENERATION_PARAMS_PATH), e))
    else:
        live_params_hash = None
        errors.append("R8 生成参数真源缺失: %s（generation_parameters_hash 无从核验）"
                      % rel(GENERATION_PARAMS_PATH))
    check_generation_params_placeholders(errors)

    schema = json.load(io.open(SCHEMA_PATH, encoding="utf-8"))
    required_fields = set(schema.get("required") or [])
    nullable_paths = schema_nullable_paths(schema)
    resolver = RefResolver(base_uri="file://" + os.path.dirname(SCHEMA_PATH) + "/", referrer=schema)
    validator = Draft7Validator(schema, resolver=resolver)

    # R13 的案例目录口径 = 实际承载 Manifest 的案例目录（与 R12 的 case_id 口径互为反面）
    case_dirs = {c for c in (case_dir_of(m) for m in manifests) if c}

    for mf in manifests:
        name = rel(mf)
        try:
            with io.open(mf, encoding="utf-8") as f:
                doc = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append("R3 %s: YAML 解析失败（%s）" % (name, e))
            continue
        if not isinstance(doc, dict):
            errors.append("R3 %s: 顶层不是映射对象" % name)
            continue

        # ---- R2 空白 / 占位残留（只看值，不看注释）----
        # 覆盖面：占位模式对**所有**字符串值生效；空白/null 判据对必填字段（及其子字段）生效——
        # 可选字段留空是合法状态，必填字段留空是"填了个寂寞"的假绿。
        r2_flagged = set()
        for fpath, val in walk_values(doc):
            top = fpath.split(".")[0].split("[")[0]
            is_required_branch = top in required_fields
            reason = blank_or_placeholder(val)
            if reason is None:
                continue
            # Schema 明示 type 含 "null" 的字段：null 是 B.2.1 字面允许的合法取值（B:146-150 `string | null`），
            # 不算"以 null 充当已填"。这里放宽的只是"null 本身合法"——E2E 必须非 null、非 E2E 必须为 null、
            # 非 null 时版本号必须在 contracts/interaction/ 真源里实际存在，三条全部由 R9 实时核验，一条不少。
            if val is None and fpath in nullable_paths:
                continue
            # null / 空白只对必填分支判红；占位模式一律判红
            if not isinstance(val, str) and not is_required_branch:
                continue
            if isinstance(val, str) and val.strip() == "" and not is_required_branch:
                continue
            # sign 模式唯一豁免：运行前补填字段，且值必须恰为声明性标记 PENDING_BUILD
            if mode == "sign" and fpath in RUN_TIME_FIELDS and val == "PENDING_BUILD":
                continue
            errors.append("R2 %s: 字段 %s %s" % (name, fpath, reason))
            r2_flagged.add(fpath)

        # ---- R3 Schema ----
        for e in sorted(validator.iter_errors(doc), key=lambda x: list(x.absolute_path)):
            errors.append("R3 %s: /%s %s" % (name, "/".join(map(str, e.absolute_path)), e.message))

        # ---- R4 snapshot_hash + 归属 ----
        sid, declared = doc.get("context_snapshot_id"), doc.get("snapshot_hash")
        if not isinstance(sid, str) or sid not in snap_idx:
            errors.append("R4 %s: context_snapshot_id=%r 在 acceptance/cases/*/fixtures/ 里找不到对应快照，"
                          "snapshot_hash 无从核验" % (name, sid))
        else:
            spath = snap_idx[sid]
            mcase, scase = case_dir_of(mf), case_dir_of(spath)
            if mcase != scase and CROSS_CASE_SNAPSHOT_ALLOWED.get(mcase) != scase:
                errors.append("R4 %s: 快照归属越界——Manifest 在案例 %s，快照 %s 却在案例 %s；"
                              "跨案例共用快照只有 %s 一条合法例外（B.5.1/E2E-02 相同企业事实 + B.2.2 相同 Context Snapshot）"
                              % (name, mcase, sid, scase,
                                 "、".join("%s←%s" % kv for kv in sorted(CROSS_CASE_SNAPSHOT_ALLOWED.items()))))
            actual = canonical_snapshot_hash(spath)
            if declared != actual:
                errors.append("R4 %s: snapshot_hash 与实算不符\n      声明 %s\n      实算 %s（源 %s）"
                              % (name, declared, actual, rel(spath)))

        # ---- R5 hard_rule_refs ----
        for i, ref in enumerate(doc.get("hard_rule_refs") or []):
            loc = "%s: hard_rule_refs[%d]" % (name, i)
            if not isinstance(ref, dict):
                errors.append("R5 %s 不是 VersionedRef 对象" % loc)
                continue
            oid = ref.get("object_id")
            if ref.get("object_type") != "RuleRecord":
                errors.append("R5 %s object_type=%r，硬规则引用必须是 RuleRecord" % (loc, ref.get("object_type")))
            if oid not in rule_idx:
                errors.append("R5 %s object_id=%r 在 contracts/rules/ 无对应 RuleRecord 对象（解析不到）" % (loc, oid))
                continue
            rule, rpath = rule_idx[oid]
            if ref.get("version") != rule.get("version"):
                errors.append("R5 %s version=%r，但 %s 的 version=%r（版本对不上）"
                              % (loc, ref.get("version"), rel(rpath), rule.get("version")))
            if ref.get("brand_id") != rule.get("brand_id"):
                errors.append("R5 %s brand_id=%r，但 %s 的 brand_id=%r（品牌隔离 SYS-08）"
                              % (loc, ref.get("brand_id"), rel(rpath), rule.get("brand_id")))
            if rule.get("status") != "ACTIVE":
                errors.append("R5 %s 指向的 %s status=%r，非 ACTIVE 规则不得被冻结案例引用（A.9.2）"
                              % (loc, rel(rpath), rule.get("status")))

        # ---- R6 签字三件套 ----
        # R6 在 R2 之上补类型级断言。同一字段若已被 R2 判红，此处不重复计一条红线（同一事实只算一条）；
        # R2 放行的值 R6 仍会继续断言——例如 approved_at="签字日" 非空非占位，但不是 ISO8601，只有 R6 拦得住。
        for field in SIGNATURE_FIELDS:
            if field in r2_flagged:
                continue
            val = doc.get(field)
            reason = blank_or_placeholder(val)
            if reason is None and not isinstance(val, str):
                reason = "类型是 %s，签字字段必须是字符串" % type(val).__name__
            if reason is not None:
                errors.append("R6 %s: 签字字段 %s %s（带着占位/空值签字即假绿）" % (name, field, reason))
                continue
            if field == "approved_at" and parse_iso8601(val) is None:
                errors.append("R6 %s: approved_at=%r 不能解析为 ISO8601 datetime（B.2.1 该字段类型 datetime）"
                              % (name, val))

        # ---- R7 版本指针 ↔ 真源文档控制块 ----
        for field, docname in VERSION_SOURCES:
            if field not in doc_versions:
                continue  # 解析失败已在 resolve_doc_versions 记红
            declared_v = doc.get(field)
            if declared_v != doc_versions[field]:
                errors.append("R7 %s: %s=%r，但 %s 文档控制块实时解析为 %r（版本指针过期 = 把考卷冻结在被取代的合同上）"
                              % (name, field, declared_v, docname, doc_versions[field]))

        # ---- R8 生成参数指纹 ↔ 真源实时重算 ----
        if live_params_hash is not None:
            declared_hash = doc.get("generation_parameters_hash")
            if declared_hash != live_params_hash:
                errors.append("R8 %s: generation_parameters_hash 与真源实算不符（参数文件改了、指纹没跟着改，"
                              "= 案例声明的模型条件与实际条件已脱钩）\n      声明 %s\n      实算 %s（源 %s）"
                              % (name, declared_hash, live_params_hash, rel(GENERATION_PARAMS_PATH)))

        # ---- R9 两阶段共同合同 / 基线 Prompt 版本 ↔ contracts/interaction/ 实时解析 ----
        is_e2e = (case_dir_of(mf) or "").startswith(E2E_CASE_PREFIX)
        for field, relpath in INTERACTION_VERSION_SOURCES:
            parts = field.split(".")
            node, declared_v, reachable = doc, None, True
            for part in parts:
                if isinstance(node, dict) and part in node:
                    node = node[part]
                else:
                    reachable = False
                    break
            if reachable:
                declared_v = node
            else:
                # 键缺失由 R3（Schema.required）判红，这里不重复计一条
                continue
            if is_e2e:
                if declared_v is None:
                    errors.append("R9 %s: %s 为 null，但 B.5 端到端案例的两阶段共同交互合同/输出合同/基线 Prompt "
                                  "必须已冻结（B:992），null = 拿没冻结的合同跑 A/B" % (name, field))
                    continue
            else:
                if declared_v is not None:
                    errors.append("R9 %s: %s=%r，但本案例不是 B.5 端到端匿名 A/B（非 E2E 案例不走两阶段共同合同），"
                                  "该字段应为 null" % (name, field, declared_v))
                continue
            if field not in interaction_versions:
                continue  # 真源解析失败已在 resolve_interaction_versions 记红
            if declared_v != interaction_versions[field]:
                errors.append("R9 %s: %s=%r，但 %s 文档控制块实时解析为 %r"
                              "（版本号不存在或已过期 = 案例冻结在一份不存在/被取代的合同上）"
                              % (name, field, declared_v, relpath, interaction_versions[field]))

        # ---- R12 素材收集（判定在循环外统一做）----
        identities.append((name, doc.get("case_id"), os.path.basename(mf),
                           case_dir_of(mf), doc.get("approved_at")))

    # ---- R10 / R11 / R12 / R13：仓库级红线（不逐 Manifest 判）----
    check_frozen_digests(errors, doc_versions)
    check_pending_marks(errors, notes, mode, manifests)
    check_identity(errors, notes, mode, identities)
    check_requirement_mapping(errors, case_dirs)

    def _vfmt(label, field, docname, table):
        ln = version_linenos.get(docname)
        return "%s=%s@%s:%s" % (label, table.get(field, "解析失败"), os.path.basename(docname),
                                ("L%d" % ln) if ln else "行号未取到")

    ver_line = " / ".join(_vfmt(f, f, d, doc_versions) for f, d in VERSION_SOURCES)
    ix_line = " / ".join(_vfmt(f.split(".")[-1], f, d, interaction_versions)
                         for f, d in INTERACTION_VERSION_SOURCES)
    print(attribution_block())
    print("冻结断言门[%s 模式] | Manifest %d 份（应有 %d）| 案例目录 %d 个（应有 %d）| 快照索引 %d 条 | 规则对象 %d 条"
          % (mode, len(manifests), expected, len(case_dirs), EXPECTED_DISTINCT_CASE_IDS,
             len(snap_idx), len(rule_idx)))
    print("真源版本（实时解析，@文件:行号 = 门实际读到的控制块版本行）| %s" % ver_line)
    print("交互合同版本（实时解析）| %s" % ix_line)
    print("生成参数指纹（实时重算）| %s（源 %s）"
          % (live_params_hash or "重算失败", rel(GENERATION_PARAMS_PATH)))
    if notes:
        print("\n提示（非红线，仅留痕——送签态豁免不等于问题消失）：")
        for n, t in enumerate(notes, 1):
            print("  · %s" % t)
    if errors:
        print("\nGATE_RED —— 以下 %d 条红线未清，物理拒绝送签：\n" % len(errors))
        for n, e in enumerate(errors, 1):
            print("  %2d. %s" % (n, e))
        print("\n（占位未清或核验不一致时送签 = 带着占位签字的假绿，本门即为此而设）")
        return 1
    print("\nGATE_GREEN —— 十三条红线全清（齐套 / 零占位残留 / Schema 过 / snapshot_hash 实算一致且归属正确 /"
          " hard_rule_refs 全部解析到 A.9.1 全等的规则对象 / 签字三件套可解析 / 版本指针与真源实时一致 /"
          " 生成参数指纹实时重算一致 / 交互合同与基线 Prompt 版本实时解析命中 / 真源正文 digest 与登记一致 /"
          " 待决标记与悬空指针清零 / 运行身份唯一 / 30 需求 × 案例映射完整）")
    print("GATE_GREEN ≠ 已签字生效：本门只证明占位清零与机械核验一致，")
    print("  不代表 Founder 已签字（approved_by/approved_at 仍须真实签署），也不代表案例内容质量合格。")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # 被 | head / | less 截断时不抛栈；退出码仍标记异常
        os._exit(1)
