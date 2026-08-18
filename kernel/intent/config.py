#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/intent 模块的常量真源：路径 + 枚举，出现且只出现一次。

为什么要有这个文件（不是为了"整洁"，是为了堵一类假绿）：
Intent 模块按 C.3 拆成 preprocess / trace / postcheck / llm / runner / module_manifest 六个文件、
由多方分头施工。任何一处把 contracts/ 路径或六个 BusinessGoal 再抄一遍，就出现"两份口径"——
真源改了只改动其中一份时，跑出来仍然 exit 0，没有任何检测器会喊。这与 tools/freeze_gate.py
不留版本基线常量、坚持"每次实时解析真源"是同一条纪律：**同一事实只许有一个落点**。

真源指针（按小节名书写、不锁行号——同 tools/freeze_gate.py 与 contracts/interaction/README.md §4 的纪律，
行号会随文档增删漂移，小节名不会）：
  · BUSINESS_GOALS / EXECUTION_MODES / PLATFORM / TASK_TYPE
        ← A_模块接口与核心数据字典.md「## A.2.6 核心枚举」
  · AVAILABILITY_* / IMPACT_*
        ← 同上 A「## A.4.2 ContextRequirement」
  · 阻断性最小上下文口径
        ← contracts/OD-03_阻断性最小上下文字段清单.md（EFFECTIVE，Founder 2026-08-17 批准生效）
  · 文件布局与各常量的消费方
        ← M1-EP02 kernel/intent 接口规格「文件布局」「各文件公共函数签名」

本文件不做任何 I/O、不检查路径是否存在：缺文件应当由真正去读它的那个函数在现场报错，
在这里预先 assert 只会把报错点推离案发地点，排查时反而更慢。
"""

import os

# --- 仓库内路径（全部绝对化，避免调用方 cwd 不同导致读到别的文件） ---------------------

# kernel/intent/config.py → kernel/intent → kernel → 仓库根，故三层 dirname。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CONTRACTS_DIR = os.path.join(REPO_ROOT, "contracts")
SCHEMAS_DIR = os.path.join(CONTRACTS_DIR, "schemas")

# 接口规格「config.py：路径常量：contracts schema 两份」——两份 = Intent 的入参形状与出参形状。
SCHEMA_CONTEXT_SNAPSHOT = os.path.join(SCHEMAS_DIR, "context_snapshot.schema.json")
SCHEMA_INTENT_EXECUTION_PLAN = os.path.join(SCHEMAS_DIR, "intent_execution_plan.schema.json")
# 上面两份都以 $ref 指向 common.defs.json（ArtifactEnvelope / TraceEntry / ContextRequirement 等
# 共用定义都在里面），jsonschema 的 RefResolver 需要它的实际路径才能解析，故一并登记——
# 它不是"第三份 schema"，是那两份的依赖。
SCHEMA_COMMON_DEFS = os.path.join(SCHEMAS_DIR, "common.defs.json")

# 别名（不是第二份真源，指向同一个对象）：runner.py 用 getattr 按候选名 "INTENT_PLAN_SCHEMA_PATH" /
# "INTENT_EXECUTION_PLAN_SCHEMA" 探本模块，探不到就退回它自己文件内的默认路径常量。
# 两条路径今天指向同一个文件，所以行为一致；但真源目录一旦搬家，"退回本地默认"就会静默用旧路径继续跑——
# 那正是本文件想堵的"两份口径"。补上别名后，runner 的探测必然命中这里，config 重新成为唯一权威。
INTENT_PLAN_SCHEMA_PATH = SCHEMA_INTENT_EXECUTION_PLAN
INTENT_EXECUTION_PLAN_SCHEMA = SCHEMA_INTENT_EXECUTION_PLAN

# 生成参数唯一真源（OD-02 定格；其内容哈希是 20 份 Case Manifest 的 generation_parameters_hash 来源，
# 算法见 tools/freeze_gate.py canonical_snapshot_hash）。llm.py 逐字段读它，不得在代码里写死温度/模型名。
GENERATION_PARAMETERS_PATH = os.path.join(CONTRACTS_DIR, "interaction", "generation_parameters.json")

# RuleRecord 注册表目录（A.9.1 十字段对象，每个 .yaml 一条）。preprocess.load_rule_pool 读它。
RULES_DIR = os.path.join(CONTRACTS_DIR, "rules")

# 禁用词表：**唯一运营真源**（Founder 2026-08-17 预裁决③，见 contracts/rules/R-FB01-001.yaml 头注）。
# 它属考卷区（acceptance/），本模块**只读不写**——改词表 = 改考卷，走 C.6.3 审批。
FORBIDDEN_LEXICON_PATH = os.path.join(REPO_ROOT, "acceptance", "detectors", "forbidden_lexicon.yaml")

# --- 模块自身的路径与身份（module_manifest.py / runner.py 消费） -----------------------

KERNEL_INTENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(KERNEL_INTENT_DIR, "prompts")
PROMPT_INTENT_PATH = os.path.join(PROMPTS_DIR, "intent_v0.4.md")
FIXTURES_DIR = os.path.join(KERNEL_INTENT_DIR, "fixtures")
MODULE_MANIFEST_PATH = os.path.join(KERNEL_INTENT_DIR, "module_manifest.json")

MODULE_NAME = "intent"
MODULE_VERSION = "v0.1.0"

# --- 枚举：一律照抄 A「## A.2.6 核心枚举」，顺序也照抄，不重排 ---------------------------

# 七个商业目标。顺序 = A.2.6 v0.4 表内原顺序；prompt 渲染与 postcheck 都按本元组，
# 顺序稳定才保证同一快照两次运行的 prompt 逐字节相同（B.2.2「同条件」的隐形前提）。
# DAILY_CONTENT_OPERATION（日常内容经营，Founder 2026-08-18 判分批正面定义）：让商品被看见、
# 被理解——日常经营本身就是目标；「推广／做内容」类表述解析到它属正常目标识别，不算脑补。
BUSINESS_GOALS = (
    "DAILY_CONTENT_OPERATION",
    "BRAND_AWARENESS",
    "PRODUCT_LAUNCH",
    "CONVERSION",
    "INVENTORY_ACTIVATION",
    "BRAND_STORY",
    "CUSTOMER_EDUCATION",
)

EXECUTION_MODES = ("QUICK", "ENHANCED")

# 单值枚举：A.2.6 Platform / TaskType 各只有一个允许值。
# 写成常量而不是"反正只有一个就硬编在字符串里"，是为了让 postcheck 的常量校验有个可比对的落点
# （OD-03 §一 #4「本期仅视频号；其他平台不得静默适配」——静默适配正是"没人比对常量"的产物）。
PLATFORM = "WECHAT_VIDEO"
TASK_TYPE = "VIDEO_CONTENT_CREATION"

# A.4.2 ContextRequirement 的两组枚举。availability 三值、impact 两值，
# 与 contracts/schemas/common.defs.json definitions.ContextRequirement 的 enum 逐字一致。
AVAILABILITY_AVAILABLE = "AVAILABLE"
AVAILABILITY_MISSING = "MISSING"
AVAILABILITY_CONFLICTING = "CONFLICTING"
AVAILABILITY_VALUES = (AVAILABILITY_AVAILABLE, AVAILABILITY_MISSING, AVAILABILITY_CONFLICTING)

IMPACT_BLOCKING = "BLOCKING"
IMPACT_QUALITY_REDUCING = "QUALITY_REDUCING"
IMPACT_VALUES = (IMPACT_BLOCKING, IMPACT_QUALITY_REDUCING)

# A.2.4 FactValue.status 五枚举（common.defs.json definitions.FactValueBase.status）。
# 这里登记是为了 preprocess 判"夹具写的 status 认不认识"，不认识的一律 fail-closed 当缺失，
# 而不是当可用——把没见过的状态当"在场"，正是编造事实的第一步。
FACT_STATUS_VALUES = ("CONFIRMED", "PROVISIONAL", "MISSING", "CONFLICTING", "NOT_APPLICABLE")

# A.2.6 TraceType 四枚举（trace.py 消费；放这里同样是为了只有一份）。
TRACE_TYPES = ("FACT", "RULE", "ASSUMPTION", "MODEL_JUDGMENT")

# ConfidenceStatement.level 三级（common.defs.json definitions.ConfidenceStatement）。
# A 明文「只三级置信度，不输出伪精确百分比」。
CONFIDENCE_LEVELS = ("HIGH", "MEDIUM", "LOW")

# FACT ID 前缀（接口规格「FACT ID 约定」：FACT:<field_path>）。RULE ID 直接取 RuleRecord.rule_id 原值，
# 不加前缀——那是注册表里的主键，改写它等于制造第二套 ID 体系。
FACT_ID_PREFIX = "FACT:"

# OD-03 §一 #2「为什么做：商业目标六选一已解析」这一条 ContextRequirement 的 A.4.2 field_path 规范名。
# 为什么要有这个常量（M1-EP02 修复批次仲裁1 的直接要求「判据用同一字面，不得两套」）：
# 仲裁1 后，runner 的 G2 硬闸与 postcheck 的 P4 都要按「阻断缺失里除掉 business_goal 之后还剩不剩」分岔。
# 这个字面若在 preprocess 的模板、runner 的闸、postcheck 的判据里各写一遍，改一处漏两处时
# 三方各判各的、跑出来仍然 exit 0——正是 config.py 文档串开头说的那类假绿。
# 现值 "business_goal"（不是 "facts.business_goal"）：实测取自 preprocess._UNIVERSAL_REQUIREMENTS 第二条
# 的 field_path，也是 Preflight P4 判红时打印出来的那个字面（runtime_verified，2026-08-17）。
BUSINESS_GOAL_FIELD_PATH = "business_goal"

# llm.py 取 API key 的环境变量名。此处只登记**变量名**，绝不登记值，也绝不读 .env 文件
# （用户级纪律：密钥必须走环境变量；指令内部矛盾先停先问）。
DASHSCOPE_API_KEY_ENV = "DASHSCOPE_API_KEY"
