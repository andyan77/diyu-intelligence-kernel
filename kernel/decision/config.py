#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 模块的常量真源：路径 + 枚举，出现且只出现一次。

【M2-EP01 提前段·非正式证据】本模块全部产出属 D §十一「开发可乱序，闸门按序关闭」
授权的提前开发段（琥珀段）施工产物；IA-1 尚未 PASS，本模块不产生任何 IA-2 取证。

为什么要有这个文件（与 kernel/intent/config.py 同一条纪律，不是为了"整洁"）：
Decision 模块按 C.3 拆成 preprocess / trace / rules_engine / llm / postcheck / runner /
module_manifest 多个文件。任何一处把 contracts/ 路径或枚举再抄一遍，就出现"两份口径"——
真源改了只改其中一份时，跑出来仍然 exit 0，没有检测器会喊。**同一事实只许有一个落点。**

真源指针（按小节名书写、不锁行号——行号会随文档增删漂移，小节名不会）：
  · BUSINESS_GOALS / PRODUCT_ROLES / FIT_ASSESSMENTS / TRACE_TYPES / CONFIDENCE_LEVELS
        ← A_模块接口与核心数据字典.md「## A.2.6 核心枚举」
  · CANDIDATE_COUNT_STATUS_* / 候选数量约束（目标三、最低二）
        ← 同上 A「## A.6.2 输出」「## A.6.3 BusinessCandidate」约束清单
  · HardRuleResult 两值（PASS/BLOCK）
        ← 同上 A「## A.9.1 RuleRecord」
  · 三步 LLM 分步结构（冲突识别 → 候选生成 → 逐候选取舍评估 + 1 步确定性装配）
        ← C_三个核心模块工程化落地与防死循环方案.md「C.3」BD 分步裁决段
  · 确定性验证器四点纪律（逐规则 HardRuleResult 入证据 / 不造 DSL / 双阶段命名 /
    规则调度信息放实现层映射表不扩 A.9.1）
        ← G_后MVP愿景暂存与MVP边界裁决.md「G.2」第 4 条

本文件不做任何 I/O、不检查路径是否存在：缺文件应当由真正去读它的那个函数在现场报错。
"""

import os

# --- 仓库内路径（全部绝对化，避免调用方 cwd 不同导致读到别的文件） ---------------------

# kernel/decision/config.py → kernel/decision → kernel → 仓库根，故三层 dirname。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CONTRACTS_DIR = os.path.join(REPO_ROOT, "contracts")
SCHEMAS_DIR = os.path.join(CONTRACTS_DIR, "schemas")

# Decision 的入参形状（上游冻结产物）与出参形状（本模块输出合同）。
SCHEMA_INTENT_EXECUTION_PLAN = os.path.join(SCHEMAS_DIR, "intent_execution_plan.schema.json")
SCHEMA_BUSINESS_DECISION_BUNDLE = os.path.join(SCHEMAS_DIR, "business_decision_bundle.schema.json")
# 两份 schema 的 $ref 共同依赖（ArtifactEnvelope / HardRuleResult / TraceBundle 等定义在内）。
SCHEMA_COMMON_DEFS = os.path.join(SCHEMAS_DIR, "common.defs.json")

# 别名（不是第二份真源，指向同一个对象）：runner 用 getattr 按候选名探测本模块。
BUNDLE_SCHEMA_PATH = SCHEMA_BUSINESS_DECISION_BUNDLE
BUSINESS_DECISION_BUNDLE_SCHEMA = SCHEMA_BUSINESS_DECISION_BUNDLE

# 生成参数唯一真源（OD-02 定格）。llm.py 逐字段读它，不得在代码里写死温度/模型名。
GENERATION_PARAMETERS_PATH = os.path.join(CONTRACTS_DIR, "interaction", "generation_parameters.json")

# RuleRecord 注册表目录（A.9.1 十字段对象，每个 .yaml 一条）。合流适配后本模块**不再**直接
# 扫它组池——规则池唯一来源 = 快照视图 hard_rules（active_rule_refs 经 kernel/facts 解引用，
# 快照钉定规则集）；本常量保留给离线自测的只读见证面（READONLY_WITNESSES 哈希核验零写入）。
RULES_DIR = os.path.join(CONTRACTS_DIR, "rules")

# 禁用词表：唯一运营真源（Founder 2026-08-17 预裁决③）。属考卷区，本模块**只读不写**。
FORBIDDEN_LEXICON_PATH = os.path.join(REPO_ROOT, "acceptance", "detectors", "forbidden_lexicon.yaml")

# --- 模块自身的路径与身份（module_manifest.py / runner.py 消费） -----------------------

KERNEL_DECISION_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(KERNEL_DECISION_DIR, "prompts")
PROMPT_STEP1_PATH = os.path.join(PROMPTS_DIR, "decision_step1_conflicts_v0.1.md")
PROMPT_STEP2_PATH = os.path.join(PROMPTS_DIR, "decision_step2_candidates_v0.1.md")
PROMPT_STEP3_PATH = os.path.join(PROMPTS_DIR, "decision_step3_tradeoffs_v0.1.md")
FIXTURES_DIR = os.path.join(KERNEL_DECISION_DIR, "fixtures")
MODULE_MANIFEST_PATH = os.path.join(KERNEL_DECISION_DIR, "module_manifest.json")

MODULE_NAME = "decision"
MODULE_VERSION = "v0.1.0"

# --- 枚举：一律照抄 A「## A.2.6 核心枚举」，顺序也照抄，不重排 ---------------------------

BUSINESS_GOALS = (
    "BRAND_AWARENESS",
    "PRODUCT_LAUNCH",
    "CONVERSION",
    "INVENTORY_ACTIVATION",
    "BRAND_STORY",
    "CUSTOMER_EDUCATION",
)

# ProductRole 五值。**判定条件未裁决**（知识提取 S03 把「角色词表正式定义与迁移」路由到
# PCR-03 第 4 项，尚无 Founder 裁决）：本模块只做枚举合法性与结构校验，
# 角色归属本身是 MODEL_JUDGMENT（带 rationale 与 trace），不在代码里发明判定规则。
PRODUCT_ROLES = ("HERO", "SUPPORTING", "TRAFFIC", "PROFIT", "CLEARANCE")

# AlignmentAssessment 三值（A.6.3 四适配维度共用；只做定性判断，不计算加权总分）。
FIT_ASSESSMENTS = ("ALIGNED", "TENSION", "UNKNOWN")

TRACE_TYPES = ("FACT", "RULE", "ASSUMPTION", "MODEL_JUDGMENT")

CONFIDENCE_LEVELS = ("HIGH", "MEDIUM", "LOW")

# A.6.2 candidate_count_status 三态（顺序照抄 A.6.2 原文）。
COUNT_STATUS_TARGET_THREE = "TARGET_THREE"
COUNT_STATUS_DEGRADED_TWO = "DEGRADED_TWO"
COUNT_STATUS_BLOCKED = "BLOCKED_FEWER_THAN_TWO"
CANDIDATE_COUNT_STATUS_VALUES = (
    COUNT_STATUS_TARGET_THREE,
    COUNT_STATUS_DEGRADED_TWO,
    COUNT_STATUS_BLOCKED,
)

# A.6.3 候选数量约束的单点字面：目标三个、最低两个（改这两个数 = 改冻结合同，不许）。
CANDIDATE_TARGET_COUNT = 3
CANDIDATE_MIN_COUNT = 2

# A.9.1 HardRuleResult.result 两值。注意：**没有 UNKNOWN**——所以规则引擎凡机器词面
# 判不动的语义面，绝不硬发结果，而是把该语义面登记进「仅人可查」清单（G.2 第 4 条红线：
# 质检单逐条标注"机器可查/仅人可查"，禁止全局合规图章掩盖语义盲区）。
HARD_RULE_PASS = "PASS"
HARD_RULE_BLOCK = "BLOCK"

# A.9.3 ArtifactType 中本模块产物的取值 + 本批输出 schema_version。
ARTIFACT_TYPE = "BUSINESS_DECISION_BUNDLE"
OUTPUT_SCHEMA_VERSION = "v0.1"

# A.5.2 next_action 中"放行进 Decision"的唯一字面（输入闸 IG1 与测试同源引用，不得两套）。
NEXT_ACTION_CONTINUE = "CONTINUE_TO_DECISION"
GOAL_RESOLUTION_RESOLVED = "RESOLVED"

# A.4.2 ContextRequirement 枚举（输入闸 IG3 核验上游 plan 自洽性时消费）。
AVAILABILITY_AVAILABLE = "AVAILABLE"
IMPACT_BLOCKING = "BLOCKING"

# FACT ID 约定：与 kernel/intent 同一约定（FACT:<field_path>；RULE ID 直接取 RuleRecord.rule_id
# 原值不加前缀）。模型只许引用预物化池里的 ID，不许自建（C.3 资产⑤）。
FACT_ID_PREFIX = "FACT:"
ASSUMPTION_ID_PREFIX = "ASSUME-"
MODEL_JUDGMENT_ID_PREFIX = "MJ-"

# llm.py 取 API key 的环境变量名。只登记**变量名**，绝不登记值，也绝不读 .env 文件
# （用户级纪律：密钥必须走环境变量；指令内部矛盾先停先问）。
DASHSCOPE_API_KEY_ENV = "DASHSCOPE_API_KEY"
