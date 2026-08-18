# A｜模块接口与核心数据字典

## A.0 文档控制

| 项目 | 内容 |
|---|---|
| 文档编号 | DIYU-MVP-V3-A |
| 版本 | v0.5 |
| 状态 | **EFFECTIVE（已批准生效）** |
| 批准 | Founder（Faye）2026-08-17 批准；2026-08-18 内容真实性三层边界修订批次（Founder R1-R7 裁决，台账 08-18 块 C 行）三份同批升版；2026-08-18 校准修订批（Founder L3 判分裁决 + 四点批复，台账 08-18 判分行）A v0.4 + B v0.6 + OD-03 v1.1 同批升版；2026-08-18 校准批二（Founder 复判裁定 + 第⑥条产品标准 + 三分叉批复，台账 08-18 复判行/三分叉行）A v0.5 + B v0.7 + OD-03 v1.2 同批升版；历次修订均经 Founder 批准 |
| v0.4→v0.5 修订 | Founder 2026-08-18 复判批裁决（**第⑥条产品标准**＋分叉 B「乙」＋分叉 C「窄」，原文见 acceptance/runs/L3-判分记录-INT-20260818.md 复判节）：① A.5.2 goal_resolution 新增第四取值 **RESOLVED_WITH_ALTERNATIVE**（已解析＋另有情境备选）——用户原话已解析出主目标、系统又据企业事实发现用户未提及的重大经营情境时的合法终态，Founder 批复原文「账本必须如实，听懂了就是听懂了」（不把已听懂降级成没听懂）；② 新增约束 8（该状态的完整判据与触发面）；③ 约束 3 措辞明确 CONTINUE_TO_DECISION 不含该新状态。其余条款不变 |
| v0.3→v0.4 修订 | Founder 2026-08-18 判分批裁决（五条统一产品标准 + 四点批复 1/3）：① A.2.6 BusinessGoal 新增第七枚举 DAILY_CONTENT_OPERATION（日常内容经营，正面定义见枚举表后注）；② A.5.2 goal_candidates 新增三个机器可判字段 focus / tradeoffs / expected_outcome（候选必须是方案骨架）；③ 约束1 同步（AMBIGUOUS 时候选三要素非空）。裁决记录见《裁决台账》08-18 判分行 + acceptance/runs/L3-判分记录-INT-20260818.md |
| v0.1→v0.2 修订 | Founder 2026-08-17 裁决：VoicePackage 补「emotion（情绪）」字段，对齐主 PRD 7.2 Voice Package 最小内容（完整口播、停顿、强调、语速和情绪）；其余条款不变。裁决记录见《裁决台账》 |
| v0.2→v0.3 修订 | Founder 2026-08-18 裁决（内容真实性三层边界 R3）：A.3.5 PersonaFacts 新增 real_anchors「真实锚点清单」字段（完全选填）——人设＝真人成份与角色演绎的混合体，不设真人/虚构二分字段；锚点列出该人设必须如实的身份要素，锚点之外默认演绎自由；其余条款不变。裁决记录见《裁决台账》08-18 块 C 行 |
| 文档属性 | 主 PRD 的规范性接口与数据附录 |
| 上位文档 | PRD_笛语智能核_MVP_V3.0_v0.1.md |
| 配套验收合同 | B_三个核心模块智能验收合同.md |
| 适用范围 | 单品牌、微信视频号、服装内容商业决策与制作交付 |

本附录定义当前 MVP 能够执行、引用和验证核心能力所需的最小逻辑接口。实现可以把这些合同转换为 JSON Schema、数据库对象或工作流变量，但不得改变语义。

Schema 通过只证明结构合法，不证明智能能力成立。附录 B 对相应里程碑拥有阻断权。

本附录不试图：

- 枚举服装行业全部任务、字段和异常；
- 建设完整行业本体或经验知识库；
- 定义多租户 SaaS、企业 IAM、RLS 或复杂审计模型；
- 用临时自由文本替代必须结构化的状态、来源、引用和不确定性；
- 用字段数量、综合分数或 LLM Judge 代替人工商业验收。

完整性的判断标准是：

> 当前 MVP 用户旅程、模块诊断案例和端到端匿名 A/B，可以通过明确字段、枚举、引用与异常合同执行，不需要临时增加无来源的自由文本字段补洞。

---

# A.1 数据与接口硬原则

## A.1.1 先事实，后经验

MVP Day 1 只建设：

- BrandFacts；
- ProductFacts；
- AudienceFacts；
- PersonaFacts；
- VideoAccountFacts。

三个智能模块首先使用：

~~~text
企业事实
+
当前任务合同
+
已批准硬规则
+
通用基础模型的内化能力
~~~

模型生成的候选、创意文本和判断不得反向写成企业事实。

人工选择、人工修改和品牌明确偏好可以形成 BrandMemoryCandidate，但只有 Founder / Reviewer 批准后才能形成 ApprovedBrandMemory。

## A.1.2 四类依据必须分离

| 类型 | 定义 | 来源要求 |
|---|---|---|
| FACT | 来自当前 Context Snapshot 的企业事实或用户明确陈述 | 必须引用来源 |
| RULE | 当前任务适用的已启用硬规则 | 必须引用规则版本 |
| ASSUMPTION | 因资料不足而显式采用的工作假设 | 必须说明替代的缺失项和影响 |
| MODEL_JUDGMENT | 模型基于事实、规则与假设形成的判断 | 必须引用支撑 Trace |

ASSUMPTION 和 MODEL_JUDGMENT 不得伪装为 FACT。

## A.1.3 单品牌隔离

每个 Task、ContextSnapshot、Run、Artifact、Review 和 BrandMemory 记录必须携带同一个 brand_id。

模块执行前必须满足：

~~~text
task.brand_id
= context_snapshot.brand_id
= all_fact_refs.brand_id
= all_artifact_refs.brand_id
~~~

不一致时必须阻断运行，不能自动跨品牌检索或补全。

## A.1.4 不确定性必须显式

资料不足时只能：

- 进入 NEEDS_INPUT；
- 在快速模式中显式记录 missing_context、assumptions 和降低后的 confidence；
- 输出受限候选；
- 返回 FAILED 或等待人工决定。

不得通过生成一个看似完整的值来消除缺失。

## A.1.5 版本不可覆盖

事实、Snapshot、模块输出和审核后的 Artifact 均采用追加版本。已经被下游引用的版本不得原地覆盖。

---

# A.2 通用类型与枚举

## A.2.1 必填性

| 标记 | 含义 |
|---|---|
| R | 结构必填；字段必须存在 |
| C | 条件必填；由当前任务、规则或输出类型决定 |
| O | 可选；缺失时不得临时虚构 |

## A.2.2 VersionedRef

~~~yaml
VersionedRef:
  object_type: string
  object_id: string
  version: integer
  brand_id: string
~~~

模块之间不允许只传递可变对象 ID。

## A.2.3 SourceRef

~~~yaml
SourceRef:
  source_id: string
  brand_id: string
  source_type: enum
  locator: string
  captured_at: datetime
  checksum: string | null
~~~

source_type 当前允许：

~~~text
BRAND_OPERATOR_INPUT
FOUNDER_CONFIRMATION
UPLOADED_DOCUMENT
PRODUCT_DATA_FILE
IMAGE_INPUT
MODEL_EXTRACTION
SYSTEM_RECORD
~~~

规则：

- locator 可以是消息、文件、页码、段落、表格行或图片引用；
- locator 不得包含明文凭证、临时访问令牌或无关系统路径；
- MODEL_EXTRACTION 只能产生 PROVISIONAL 值；
- 普通创意输出不能成为企业事实来源。

## A.2.4 FactValue

~~~yaml
FactValue:
  value: any | null
  status: CONFIRMED | PROVISIONAL | MISSING | CONFLICTING | NOT_APPLICABLE
  source_refs: SourceRef[]
  as_of: datetime | null
  confidence: HIGH | MEDIUM | LOW | null
  uncertainty_reason: string | null
  alternatives:
    - value: any
      source_ref: SourceRef
~~~

约束：

- CONFIRMED：value 非空，至少有一个 source_ref；
- PROVISIONAL：必须有 confidence、来源和不确定原因；
- MISSING、NOT_APPLICABLE：value 为空；
- CONFLICTING：必须列出 alternatives，不能静默选值；
- 库存、价格等时效性事实必须有单位和 as_of；
- PROVISIONAL 或 CONFLICTING 不得被描述为确定事实。

## A.2.5 ConfidenceStatement

~~~yaml
ConfidenceStatement:
  level: HIGH | MEDIUM | LOW
  basis:
    - string
  limiting_factors:
    - string
~~~

只使用三级置信度，不输出伪精确百分比，不合成为综合分数。

## A.2.6 核心枚举

| 枚举 | 允许值 |
|---|---|
| UserRole | BRAND_OPERATOR, FOUNDER_REVIEWER |
| Platform | WECHAT_VIDEO |
| TaskType | VIDEO_CONTENT_CREATION |
| ExecutionMode | QUICK, ENHANCED |
| BusinessGoal | DAILY_CONTENT_OPERATION, BRAND_AWARENESS, PRODUCT_LAUNCH, CONVERSION, INVENTORY_ACTIVATION, BRAND_STORY, CUSTOMER_EDUCATION |
| ProductRole | HERO, SUPPORTING, TRAFFIC, PROFIT, CLEARANCE |
| TraceType | FACT, RULE, ASSUMPTION, MODEL_JUDGMENT |
| AlignmentAssessment | ALIGNED, TENSION, UNKNOWN |
| ReviewAction | SELECT_CANDIDATE, APPROVE_PACKAGE, REQUEST_LOCAL_REWORK, REQUEST_STRATEGY_REWORK, REJECT, TERMINATE |
| ReworkReason | FACT_ERROR, RULE_CONFLICT, PRODUCTION_ISSUE, BRAND_MISMATCH, USER_OBJECTIVE_CHANGED |
| ReworkScope | LOCAL, STRATEGY |

节日、季节、活动和时间窗口属于任务上下文，不新增为 BusinessGoal。

DAILY_CONTENT_OPERATION（日常内容经营）定义（Founder 2026-08-18 判分批裁决，正面定义）：让商品被看见、被理解——日常经营本身就是目标，不是「未指定目标」。「推广／做内容」类表述解析到它属正常目标识别，不算脑补；脑补禁令的管辖范围＝其余六个特殊经营目标不得擅自选定（与 S01 知识卡 ELI-0101 口径同步）。

---

# A.3 企业语义事实层

五类事实对象共享：

~~~yaml
FactSetEnvelope:
  fact_set_id: string
  fact_type: string
  brand_id: string
  version: integer
  schema_version: string
  updated_at: datetime
  updated_by_role: BRAND_OPERATOR | FOUNDER_REVIEWER
~~~

## A.3.1 BrandFacts

| 字段 | 类型 | 必填 | 默认来源 | 缺失处理 |
|---|---|---:|---|---|
| brand_id | string | R | 系统 | 阻断 |
| brand_name | FactValue<string> | R | 人工、品牌资料 | 显式缺失 |
| positioning | FactValue<string> | R | 人工、品牌资料 | 降低品牌适配置信度 |
| values | FactValue<string[]> | R | 人工、品牌资料 | 不得由模型代写为事实 |
| tone | FactValue<string[]> | R | 人工、资料抽取 | 缺失时标记表达不确定 |
| target_customer_summary | FactValue<string> | O | 人工、品牌资料 | AudienceFacts 为权威对象 |
| forbidden_expressions | FactValue<string[]> | R | 人工、品牌规范 | 可确认空数组；未知不等于无 |
| commercial_constraints | FactValue<string[]> | R | 人工、商业要求 | 影响规则与候选有效性 |
| audience_refs | VersionedRef[] | C | 系统引用 | 目标受众任务需要 |

## A.3.2 ProductFacts

| 字段 | 类型 | 必填 | 默认来源 | 缺失处理 |
|---|---|---:|---|---|
| product_id | string | R | 系统或商品文件 | 阻断 |
| sku | FactValue<string> | C | 商品文件、人工 | 可无 SKU，但必须有 product_id |
| name | FactValue<string> | R | 商品文件、人工 | 不得自动命名为事实 |
| category | FactValue<string> | R | 商品文件、人工 | 影响表达与视觉判断 |
| price | FactValue<Money> | C | 商品文件、人工 | 价格相关任务需要 |
| inventory | FactValue<Quantity> | C | 商品文件、人工 | 库存激活任务需要 |
| material | FactValue<string[]> | C | 吊牌、文件、人工 | 未确认时禁止材质功效表达 |
| style_attributes | FactValue<string[]> | C | 人工、资料抽取 | 可在快速模式缺失 |
| selling_points | FactValue<string[]> | C | 人工、商品资料 | 只使用已确认卖点 |
| image_refs | SourceRef[] | C | 商品图片 | 视觉理解时需要 |
| size_range | FactValue<string[]> | O | 商品文件、人工 | 非尺码任务可缺失 |
| lifecycle_stage | FactValue<string> | O | 人工、商品文件 | 新品或库存任务建议提供 |
| visual_profile_ref | VersionedRef | O | 视觉理解输出 | 缺失时不得虚构视觉细节 |

~~~yaml
Money:
  amount: number
  currency: string
  as_of: datetime | null

Quantity:
  value: number
  unit: string
  as_of: datetime
~~~

## A.3.3 VisualProfile

VisualProfile 是基于商品图片的模型观察，不自动成为确认事实。

~~~yaml
VisualProfile:
  visual_profile_id: string
  brand_id: string
  product_ref: VersionedRef
  image_source_refs: SourceRef[]
  version: integer
  silhouette: FactValue<string>
  colors: FactValue<string[]>
  texture_observation: FactValue<string>
  visual_focus: FactValue<string[]>
  shooting_attention: FactValue<string[]>
~~~

规则：

- 模型识别字段初始为 PROVISIONAL；
- 无图片时为 MISSING，不依据商品名称补写颜色、版型或纹理；
- Creative 引用时必须保留图片来源和不确定性；
- MVP 不生成图片或视频。

## A.3.4 AudienceFacts

| 字段 | 类型 | 必填 | 默认来源 | 缺失处理 |
|---|---|---:|---|---|
| audience_id | string | R | 系统 | 阻断引用错误 |
| label | FactValue<string> | R | 人工、品牌资料 | 显式缺失 |
| age_range | FactValue<Range> | O | 人工、品牌资料 | 不得由价格自动推断 |
| occupation_or_lifestyle | FactValue<string[]> | O | 人工、品牌资料 | 可缺失 |
| pain_points | FactValue<string[]> | C | 人工、研究资料 | 缺失时张力只能是模型判断 |
| purchase_reasons | FactValue<string[]> | C | 人工、研究资料 | 不伪装成已验证洞察 |
| objections | FactValue<string[]> | O | 人工、研究资料 | 可缺失 |

~~~yaml
Range:
  min: number | null
  max: number | null
  unit: string
~~~

## A.3.5 PersonaFacts

| 字段 | 类型 | 必填 | 默认来源 | 缺失处理 |
|---|---|---:|---|---|
| persona_id | string | R | 系统 | 阻断引用错误 |
| identity | FactValue<string> | R | 人工 | 缺失时需要补充或显式假设 |
| voice_traits | FactValue<string[]> | R | 人工、资料抽取 | 降低一致性置信度 |
| beliefs | FactValue<string[]> | C | 人工 | 不得写成创始人虚构信念 |
| audience_relationship | FactValue<string> | C | 人工、账号资料 | 如朋友型专家 |
| forbidden_styles | FactValue<string[]> | R | 人工 | 可确认空数组 |
| speaker_constraints | FactValue<string[]> | O | 人工 | 可缺失 |
| real_anchors | FactValue<string[]> | O | 人工 | 可缺失（完全选填，Founder 2026-08-18 R3 裁决）；真实锚点清单：列出该人设必须如实的身份要素（如真名/真职业/真店主身份），锚点之外默认演绎自由 |

## A.3.6 VideoAccountFacts

| 字段 | 类型 | 必填 | 默认来源 | 缺失处理 |
|---|---|---:|---|---|
| account_id | string | R | 系统 | 阻断引用错误 |
| platform | WECHAT_VIDEO | R | 系统固定 | 非视频号任务拒绝编译 |
| account_name | FactValue<string> | O | 人工 | 可缺失 |
| positioning | FactValue<string> | R | 人工、账号资料 | 降低平台适配置信度 |
| content_style | FactValue<string[]> | C | 人工、资料抽取 | 单次生成不能写为账号事实 |
| audience_relationship | FactValue<string> | C | 人工 | 与 Persona 冲突时标记 CONFLICTING |
| primary_persona_ref | VersionedRef | C | 系统引用 | 人物出镜型方案需要 |
| expression_boundaries | FactValue<string[]> | R | 人工 | 可确认空数组 |

---

# A.4 Task、Context 与 Runtime

## A.4.1 Task

~~~yaml
Task:
  task_id: string
  version: integer
  brand_id: string
  created_by_role: BRAND_OPERATOR
  task_statement: string
  task_statement_source_ref: SourceRef
  task_type: VIDEO_CONTENT_CREATION
  platform: WECHAT_VIDEO
  execution_mode: QUICK | ENHANCED
  selected_product_refs: VersionedRef[]
  stated_business_goal: BusinessGoal | null
  occasion: string | null
  deadline: datetime | null
  runtime_state: RuntimeState
  human_decision_required: boolean
  created_at: datetime
  updated_at: datetime
~~~

规则：

- 至少一个 selected_product_ref；
- 用户陈述不自动等同于已解析商业目标；
- 非 WECHAT_VIDEO 任务不得被静默适配；
- 商业目标改变时返回 DRAFT，重新运行 Intent。

## A.4.2 ContextRequirement

~~~yaml
ContextRequirement:
  field_path: string
  purpose: string
  availability: AVAILABLE | MISSING | CONFLICTING
  impact: BLOCKING | QUALITY_REDUCING
  resolution_question: string | null
  related_source_refs: SourceRef[]
~~~

规则：

- QUICK 只能跨过 QUALITY_REDUCING 缺失；
- QUICK 跨过的每项缺失必须产生 ASSUMPTION 和 confidence 限制；
- BLOCKING 缺失在任何模式都进入 NEEDS_INPUT；
- 目标不明确时不得填入唯一 business_goal。

## A.4.3 ContextSnapshot

~~~yaml
ContextSnapshot:
  snapshot_id: string
  task_id: string
  brand_id: string
  version: integer
  created_at: datetime
  brand_facts_ref: VersionedRef
  product_facts_refs: VersionedRef[]
  audience_facts_refs: VersionedRef[]
  persona_facts_refs: VersionedRef[]
  video_account_facts_ref: VersionedRef | null
  active_rule_refs: VersionedRef[]
  approved_brand_memory_refs: VersionedRef[]
  input_source_refs: SourceRef[]
  snapshot_hash: string
~~~

规则：

- 每次模块运行固定引用一个 Snapshot；
- 同条件 A/B 使用同一个 snapshot_id 或相同 snapshot_hash；
- Fact 更新后创建新 Snapshot；
- 旧 Artifact 继续引用旧 Snapshot；
- 首轮 MVP 验收或 Brand Memory 禁用时 approved_brand_memory_refs 必须为空；启用时只能引用 APPROVED 且未 REVOKED 的版本。

## A.4.4 RuntimeState

~~~text
DRAFT
NEEDS_INPUT
DECISION_READY
CREATIVE_READY
REVIEW_REQUIRED
COMPLETED
FAILED
~~~

| 当前状态 | 允许的下一状态 |
|---|---|
| DRAFT | NEEDS_INPUT, DECISION_READY, FAILED |
| NEEDS_INPUT | DRAFT, FAILED |
| DECISION_READY | DRAFT, CREATIVE_READY, FAILED |
| CREATIVE_READY | REVIEW_REQUIRED, FAILED |
| REVIEW_REQUIRED | CREATIVE_READY, DRAFT, COMPLETED, FAILED |
| COMPLETED | 无 |
| FAILED | DRAFT |

HUMAN_DECISION_REQUIRED 是 REVIEW_REQUIRED 下的 human_decision_required 标记，不是第八状态。

事件—状态合同：

| 事件 | 前态 | 后态 | 约束 |
|---|---|---|---|
| Intent 发现目标未明确或阻断项 | DRAFT | NEEDS_INPUT | 不得继续 Business Decision |
| 用户补齐资料或明确目标 | NEEDS_INPUT | DRAFT | 必须生成新 Task 或 Snapshot 版本后重跑 Intent |
| 合法商业候选生成 | DRAFT | DECISION_READY | 目标已 RESOLVED，候选满足数量合同 |
| 人工选定候选且 Creative 生成成功 | DECISION_READY | CREATIVE_READY | 必须存在成对且关联一致的 DecisionSelection 与 ReviewRecord |
| 包完整性与硬规则通过并提交审核 | CREATIVE_READY | REVIEW_REQUIRED | 九项资产与引用均有效 |
| 请求局部返工并生成受影响新版本 | REVIEW_REQUIRED | CREATIVE_READY | 随后校验通过再回 REVIEW_REQUIRED |
| 拒绝全部候选或请求策略重做 | DECISION_READY 或 REVIEW_REQUIRED | DRAFT | 复用或更新 Intent 后重跑 Business Decision，再进入 DECISION_READY |
| 商业目标变化 | DECISION_READY 或 REVIEW_REQUIRED | DRAFT | 必须重跑 Intent |
| 批准制作包 | REVIEW_REQUIRED | COMPLETED | APPROVE_PACKAGE ReviewRecord 指向当前版本 |
| 返工超限 | REVIEW_REQUIRED | REVIEW_REQUIRED | 状态不变；human_decision_required=true，停止自动生成 |
| Founder / Reviewer 人工终止 | REVIEW_REQUIRED | FAILED | 必须有 TERMINATE ReviewRecord 和 MANUAL_TERMINATION FailureRecord |
| 当前执行无法自动恢复 | 任一非 COMPLETED 状态 | FAILED | 记录 FailureRecord，不得伪装成功 |
| 人工确认修正后重启 | FAILED | DRAFT | 生成新 Run；保留原失败记录 |

未列出的迁移一律拒绝。FAILED 表示当前执行在现有条件下失败，不是禁止人工修正后重启的永久任务终态；COMPLETED 是终态。

## A.4.5 ExecutionRecord

~~~yaml
ExecutionRecord:
  run_id: string
  task_id: string
  brand_id: string
  module: INTENT | BUSINESS_DECISION | CREATIVE | REWORK
  input_artifact_refs: VersionedRef[]
  context_snapshot_ref: VersionedRef
  output_schema_version: string
  model_provider: string
  base_model: string
  model_version: string | null
  adapter_version: string
  generation_parameters_hash: string
  started_at: datetime
  ended_at: datetime
  latency_ms: integer
  input_tokens: integer | null
  output_tokens: integer | null
  estimated_cost: number | null
  cost_currency: string | null
  run_status: SUCCEEDED | DEGRADED | FAILED | TIMED_OUT | FORMAT_INVALID
  retry_count: integer
  output_artifact_refs: VersionedRef[]
  failure_ref: VersionedRef | null
~~~

## A.4.6 FailureRecord

~~~yaml
FailureRecord:
  failure_id: string
  version: integer
  brand_id: string
  task_id: string
  run_id: string | null
  error_code: MODEL_TIMEOUT | MODEL_UNAVAILABLE | FORMAT_INVALID | SCHEMA_INVALID | HARD_RULE_VIOLATION | FACT_CONFLICT | VISUAL_INPUT_UNREADABLE | EXPORT_FAILED | MANUAL_TERMINATION | INTERNAL_ERROR
  stage: INPUT | MODEL_CALL | PARSE | VALIDATE | REVIEW | STORE
  sanitized_message: string
  retry_count: integer
  fallback_action: RETRY | DEGRADED_OUTPUT | REQUEST_INPUT | HUMAN_REVIEW | FAIL
  last_valid_artifact_refs: VersionedRef[]
  created_at: datetime
~~~

失败规则：

- 重试必须有界，不形成无限 Agent 循环；
- 非模型导出失败可将 run_id 留空，但必须由 MarkdownExportManifest.failure_ref 精确引用；
- 降级输出仍须通过 Schema 和硬规则；
- 无法形成合法 Artifact 时不得返回半结构化文本冒充成功；
- 日志不得包含凭证、完整上传文件或敏感临时链接。

---

# A.5 Intent Intelligence Module

## A.5.1 输入

~~~yaml
IntentRequest:
  schema_version: string
  task_ref: VersionedRef
  context_snapshot_ref: VersionedRef
  execution_mode: QUICK | ENHANCED
~~~

## A.5.2 输出

~~~yaml
IntentExecutionPlan:
  artifact: ArtifactEnvelope
  task_type: VIDEO_CONTENT_CREATION
  platform: WECHAT_VIDEO
  goal_resolution: RESOLVED | RESOLVED_WITH_ALTERNATIVE | AMBIGUOUS | NEEDS_INPUT
  business_goal: BusinessGoal | null
  goal_candidates:
    - goal: BusinessGoal
      rationale: string
      focus: string                  # 侧重点（Founder 2026-08-18 判分批：候选必须是方案骨架，不是光秃标签）
      tradeoffs: string              # 优缺点/取舍
      expected_outcome: string       # 适用结果
      supporting_trace_refs: string[]
  intent_summary: string
  target_audience_refs: VersionedRef[]
  required_context: ContextRequirement[]
  missing_context: ContextRequirement[]
  assumptions: TraceEntry[]
  confidence: ConfidenceStatement
  next_action: CONTINUE_TO_DECISION | REQUEST_INPUT
  trace_bundle: TraceBundle
~~~

约束：

1. goal_resolution 为 AMBIGUOUS 时，business_goal 必须为空、goal_candidates 至少两个且每个候选的 focus / tradeoffs / expected_outcome 非空（先形成方案骨架、讲清侧重与取舍，再请用户选择——不得把未经整理的选择题退给用户）、next_action 必须为 REQUEST_INPUT，Task 必须进入 NEEDS_INPUT；候选只供人工明确目标，不能代替人工门继续 Decision。
2. goal_resolution 为 NEEDS_INPUT 时，business_goal 必须为空、next_action 必须为 REQUEST_INPUT，Task 必须进入 NEEDS_INPUT。
3. 只有 goal_resolution 为 RESOLVED（**不含 RESOLVED_WITH_ALTERNATIVE**——该状态按约束 8 必须停在用户选择点）、business_goal 非空且无 BLOCKING 缺失时，next_action 才能为 CONTINUE_TO_DECISION。
4. QUICK 继续时，跨过的缺失项必须为 QUALITY_REDUCING，并产生对应 ASSUMPTION。
5. BLOCKING 缺失时 goal_resolution 为 NEEDS_INPUT。
6. 同一事实快照只改变目标时，business_goal、required_context 和下游重点应变化；未改变事实必须保持。
7. Intent 只输出视频号内容任务计划。
8. goal_resolution 为 **RESOLVED_WITH_ALTERNATIVE**（已解析＋另有情境备选）时：business_goal 必须非空且等于**按用户原话解析出的主目标**；goal_candidates 至少两个——其中恰有一个 goal 等于该主目标（＝按用户原话的常规／主题方案骨架），其余为触发本状态的重大经营情境所对应的备选目标（登记表见 OD-03 §五）；每个候选的 focus / tradeoffs / expected_outcome 非空；必须给出一个请用户在两个方向之间择一的问题，落点＝ business_goal 那一项 ContextRequirement 的 resolution_question（A.4.2 里唯一承载「要问什么」的字段，与 AMBIGUOUS 的澄清问题同一落点）；next_action 必须为 REQUEST_INPUT，Task 必须进入 NEEDS_INPUT；备选不能代替人工门继续 Decision。
   **触发面（Founder 2026-08-18 第⑥条产品标准 + 分叉 C「窄口径」批复）**：仅当①系统据企业事实已知某个登记在册的重大经营情境（如商品处于库存消化期）、②用户原话未提及该情境、③用户原话解析出的主目标属常规／主题类（即系统正准备直接开做）三条同时成立时，本状态才成立。此时系统**既不得擅自转向**备选目标（那是替用户改目标），**也不得只在内部留痕当作不知道**（那是把已知情境藏起来）。用户已明示该情境（情境即其目标）、或目标本身尚未解析（AMBIGUOUS／NEEDS_INPUT，系统本就在请人裁决）时，本状态不适用——后者再塞备选只会加重用户负担。

---

# A.6 Business Decision Engine

## A.6.1 输入

~~~yaml
BusinessDecisionRequest:
  schema_version: string
  intent_plan_ref: VersionedRef
  context_snapshot_ref: VersionedRef
  active_rule_refs: VersionedRef[]
~~~

## A.6.2 输出

~~~yaml
BusinessDecisionBundle:
  artifact: ArtifactEnvelope
  business_problem: string
  recognized_conflicts:
    - conflict_id: string
      description: string
      side_a: string
      side_b: string
      trace_refs: string[]
  candidate_options:
    - BusinessCandidate
  comparative_tradeoffs:
    - candidate_refs: string[]
      tradeoff: string
      trace_refs: string[]
  candidate_count_status: TARGET_THREE | DEGRADED_TWO | BLOCKED_FEWER_THAN_TWO
  candidate_count_explanation: string | null
  system_recommendation:
    candidate_id: string | null
    judgment_trace_ref: string | null
  human_selection_required: true
  blocked_candidate_diagnostics:
    - candidate_summary: string
      blocking_rule_results: HardRuleResult[]
  confidence: ConfidenceStatement
  trace_bundle: TraceBundle
~~~

## A.6.3 BusinessCandidate

~~~yaml
BusinessCandidate:
  candidate_id: string
  title: string
  strategy: string
  product_roles:
    - product_ref: VersionedRef
      role: ProductRole
      rationale: string
      trace_refs: string[]
  supporting_fact_refs: string[]
  applied_rule_refs: string[]
  assumption_refs: string[]
  model_judgment_refs: string[]
  brand_fit:
    assessment: ALIGNED | TENSION | UNKNOWN
    rationale: string
    trace_refs: string[]
  audience_fit:
    assessment: ALIGNED | TENSION | UNKNOWN
    rationale: string
    trace_refs: string[]
  business_alignment:
    assessment: ALIGNED | TENSION | UNKNOWN
    rationale: string
    trace_refs: string[]
  production_feasibility:
    assessment: ALIGNED | TENSION | UNKNOWN
    rationale: string
    trace_refs: string[]
  risks:
    - condition: string
      possible_impact: string
      mitigation: string | null
      trace_refs: string[]
  why_this_option: string
  why_not_primary_alternative: string
  hard_rule_results: HardRuleResult[]
  confidence: ConfidenceStatement
~~~

约束：

- 正常输出目标为三个候选，最低为两个；
- 三个有效候选时 candidate_count_status 为 TARGET_THREE 且 explanation 可为空；只能形成两个时必须为 DEGRADED_TWO 并说明受哪些事实、规则或实质差异限制；少于两个时为 BLOCKED_FEWER_THAN_TWO，不得进入 DECISION_READY；
- 候选差异必须体现在商业机制、商品角色、叙事路径或风险取舍；
- 候选不得通过标题、Hook 或形容词变化凑数；
- 硬规则导致不足两个有效候选时，不补造候选，返回阻断诊断；
- 适配维度只做定性判断，不计算加权总分；
- system_recommendation 如存在，必须属于 MODEL_JUDGMENT；
- 不输出爆款概率、销量保证或因果承诺。

## A.6.4 DecisionSelection

~~~yaml
DecisionSelection:
  selection_id: string
  version: integer
  brand_id: string
  task_id: string
  decision_bundle_ref: VersionedRef
  selected_candidate_id: string
  review_ref: VersionedRef
  selected_by_role: FOUNDER_REVIEWER
  selected_at: datetime
  rationale: string | null
~~~

selected_candidate_id 必须存在于 decision_bundle_ref 精确版本的 candidate_options。review_ref 必须指向 action=SELECT_CANDIDATE、target_artifact_ref=decision_bundle_ref 且 selected_candidate_id 相同的 ReviewRecord。Creative 必须同时收到精确 decision_bundle_ref.version、DecisionSelection 版本和 selected_candidate_id。没有有效人工选择时不得生成正式制作包。

---

# A.7 Creative Content Engine

## A.7.1 输入

~~~yaml
CreativeContentRequest:
  schema_version: string
  decision_selection_ref: VersionedRef
  decision_bundle_ref: VersionedRef
  context_snapshot_ref: VersionedRef
  rework_request_ref: VersionedRef | null
~~~

## A.7.2 输出

~~~yaml
CreativeContentBundle:
  artifact: ArtifactEnvelope
  decision_selection_ref: VersionedRef
  decision_bundle_ref: VersionedRef
  selected_candidate_id: string
  context_snapshot_ref: VersionedRef
  creative_plan:
    persona_ref: VersionedRef
    audience_tension: string
    story_angle: string
    hook: string
    video_structure: string[]
    fact_refs: string[]
    rule_refs: string[]
    assumptions: TraceEntry[]
  package_artifact_refs:
    content_brief: VersionedRef
    creative_strategy: VersionedRef
    persona_card: VersionedRef
    video_script: VersionedRef
    storyboard: VersionedRef
    voice_package: VersionedRef
    audio_direction: VersionedRef
    product_placement: VersionedRef
    comment_operation_package: VersionedRef
  production_risks: string[]
  validation:
    schema: PASS | FAIL
    hard_rules: PASS | FAIL
    fact_grounding: PASS | FAIL
    package_completeness: PASS | FAIL
  confidence: ConfidenceStatement
  trace_bundle: TraceBundle
~~~

decision_selection_ref 必须精确绑定 decision_bundle_ref 和 selected_candidate_id；CreativeContentBundle.artifact.parent_references 必须同时引用该 DecisionSelection 与 BusinessDecisionBundle。任何一项不一致都必须阻断。

任何一项制作资产缺失或核心字段为空时，package_completeness 不得为 PASS。

---

# A.8 九部分内容制作交付包

九项资产都是带 ArtifactEnvelope 的独立版本。每项 parent_references 至少包含同一 DecisionSelection（SELECTED_FROM）和其 BusinessDecisionBundle（DERIVED_FROM），从而同时保留“人工选了什么”和“选自哪个决策版本”。

| Artifact | 最小必填字段 |
|---|---|
| ContentBrief | business_goal, audience_refs, core_proposition, decision_selection_ref, decision_bundle_ref, product_refs, non_negotiable_fact_refs, rule_refs |
| CreativeStrategy | content_theme, story_angle, audience_tension, emotion_path[], selling_point_order[], video_structure[] |
| PersonaCard | persona_ref, speaker_identity, voice_traits[], audience_relationship, belief_expression, forbidden_styles[] |
| VideoScript | target_duration_seconds, segments[]；每段含 start_second, end_second, visual, spoken_text, product_refs, emotion, trace_refs |
| Storyboard | shots[]；每镜含 shot_id, script_segment_ref, purpose, scene, subject, product_focus, action, framing, shooting_notes |
| VoicePackage | full_voiceover, voice_traits[], pace, emotion（情绪）, cues[]；Cue 支持 PAUSE, EMPHASIZE, SLOW_DOWN, SPEED_UP |
| AudioDirection | mood, tempo, usage_phases[], avoidance[] |
| ProductPlacement | placements[]；每项含 product_ref, script_or_shot_ref, timing, purpose, display_focus, constraints |
| CommentOperationPackage | pinned_comment, faq_items[], official_responses[], prohibited_claim_refs[] |

一致性约束：

1. 九项 Artifact 引用同一 DecisionSelection、BusinessDecisionBundle 与 selected_candidate_id。
2. PersonaCard、口播、画面建议和评论回复使用同一 Persona 与品牌表达边界。
3. Storyboard 每个镜头关联 Script segment，关键 Script 段落有可执行镜头。
4. ProductPlacement 只能引用当前商品池。
5. 材质、价格、库存和功效性陈述必须引用确认事实。
6. 视觉建议只能使用存在图片来源的 VisualProfile；无图时使用不依赖未知视觉细节的建议。
7. 视频结构体现人物、关系、信任建立和商品证明，不输出小红书笔记体。
8. Schema 和硬规则通过后，仍必须由人判断是否值得实际制作。

为支持局部返工，只维护以下最小直接依赖，不扩展为通用 DAG：

| 资产 | 必须写入 parent_references 的直接内容依赖 |
|---|---|
| ContentBrief | DecisionSelection、BusinessDecisionBundle |
| CreativeStrategy | ContentBrief |
| PersonaCard | ContentBrief |
| VideoScript | CreativeStrategy、PersonaCard |
| Storyboard | VideoScript |
| VoicePackage | VideoScript、PersonaCard |
| AudioDirection | CreativeStrategy、VideoScript |
| ProductPlacement | VideoScript、Storyboard |
| CommentOperationPackage | ContentBrief、CreativeStrategy、PersonaCard |

局部修改只重算目标资产及沿本表向下的直接或传递依赖；不受影响的资产版本保持不变。

批准后的 Markdown 导出使用轻量清单，不新增导出平台：

~~~yaml
MarkdownExportManifest:
  export_id: string
  version: integer
  brand_id: string
  task_id: string
  creative_content_bundle_ref: VersionedRef
  approved_review_ref: VersionedRef
  package_artifact_refs: VersionedRef[9]
  format: MARKDOWN
  status: SUCCESS | FAILED
  generated_at: datetime
  checksum: string | null
  failure_ref: VersionedRef | null
~~~

approved_review_ref 必须指向对同一 CreativeContentBundle 版本的 APPROVE_PACKAGE；九项引用必须与该 Bundle 一致。导出不得补写、删减或改写权威对象；失败时 status=FAILED、checksum 为空并记录 failure_ref，不能交付不完整文件。

---

# A.9 Rule、Trace、Artifact、Review 与 Rework

## A.9.1 RuleRecord

~~~yaml
RuleRecord:
  rule_id: string
  brand_id: string
  version: integer
  scope: BRAND | PRODUCT | PLATFORM | TASK
  effect: REQUIRE | PROHIBIT
  target_path: string
  statement: string
  source_ref: SourceRef
  status: ACTIVE | INACTIVE
  effective_at: datetime

HardRuleResult:
  rule_ref: VersionedRef
  target_ref: VersionedRef | null
  target_path: string
  result: PASS | BLOCK
  explanation: string
~~~

Rule Engine 只负责明确硬规则。BLOCK 的 Artifact 不得进入下一人工节点。

## A.9.2 TraceBundle

~~~yaml
TraceBundle:
  trace_bundle_id: string
  brand_id: string
  target_artifact_ref: VersionedRef
  entries:
    - TraceEntry

TraceEntry:
  trace_id: string
  trace_type: FACT | RULE | ASSUMPTION | MODEL_JUDGMENT
  statement: string
  source_refs: SourceRef[]
  object_refs: VersionedRef[]
  target_paths: string[]
  supporting_trace_refs: string[]
  confidence: HIGH | MEDIUM | LOW | null
~~~

FACT 必须引用事实或用户输入；RULE 必须引用 ACTIVE 版本；ASSUMPTION 必须指明缺失项；MODEL_JUDGMENT 必须有支撑 Trace。

## A.9.3 ArtifactEnvelope

~~~yaml
ArtifactEnvelope:
  artifact_id: string
  artifact_type: ArtifactType
  version: integer
  schema_version: string
  brand_id: string
  task_id: string
  context_snapshot_ref: VersionedRef
  source_run_id: string
  parent_references:
    - object_ref: VersionedRef
      relation: DERIVED_FROM | SELECTED_FROM | REVISES
  review_status: PENDING | APPROVED | CHANGES_REQUESTED
  created_at: datetime
  created_by: SYSTEM | BRAND_OPERATOR | FOUNDER_REVIEWER
~~~

ArtifactType 当前包含：

~~~text
INTENT_EXECUTION_PLAN
BUSINESS_DECISION_BUNDLE
CREATIVE_CONTENT_BUNDLE
CONTENT_BRIEF
CREATIVE_STRATEGY
PERSONA_CARD
VIDEO_SCRIPT
STORYBOARD
VOICE_PACKAGE
AUDIO_DIRECTION
PRODUCT_PLACEMENT
COMMENT_OPERATION_PACKAGE
~~~

DecisionSelection、ReviewRecord、ReworkRequest 和 MarkdownExportManifest 是独立的版本化运行记录，不伪装成模型输出 Artifact；Artifact 的 parent_references 可以通过 object_ref 引用这些记录。Artifact 不原地覆盖；返工只为受影响 Artifact 新增版本；旧版本保留。

## A.9.4 ReviewRecord

~~~yaml
ReviewRecord:
  review_id: string
  version: integer
  brand_id: string
  task_id: string
  target_artifact_ref: VersionedRef
  reviewer_role: FOUNDER_REVIEWER
  action: ReviewAction
  selected_candidate_id: string | null
  termination_reason: string | null
  edit_severity: NONE | LOCAL | MATERIAL | REBUILD
  deltas: ReviewDelta[]
  created_at: datetime

ReviewDelta:
  delta_id: string
  target_path: string
  reason: ReworkReason
  instruction: string
  before_value: any | null
  after_value: any | null
  evidence_refs: SourceRef[]
  affected_artifact_refs: VersionedRef[]
~~~

规则：

- SELECT_CANDIDATE 必须以 BusinessDecisionBundle 为 target，selected_candidate_id 必填、termination_reason 为空、edit_severity=NONE，并被对应 DecisionSelection.review_ref 引用；
- APPROVE_PACKAGE 必须以当前 CreativeContentBundle 为 target，selected_candidate_id 与 termination_reason 为空、edit_severity=NONE、deltas 可为空，且只在 validation 全部 PASS 时触发 REVIEW_REQUIRED → COMPLETED；
- REQUEST_LOCAL_REWORK 或 REQUEST_STRATEGY_REWORK 至少包含一个 delta；
- TERMINATE 只允许在 REVIEW_REQUIRED，以当前 CreativeContentBundle 为 target，selected_candidate_id 为空、edit_severity=NONE，并由 Founder / Reviewer 提供 termination_reason；同时创建 stage=REVIEW、error_code=MANUAL_TERMINATION、fallback_action=FAIL 的 FailureRecord，并触发 REVIEW_REQUIRED → FAILED；
- “感觉不好”不能单独成为可执行返工原因；
- FACT_ERROR 必须先更新事实版本和 Snapshot；
- USER_OBJECTIVE_CHANGED 必须返回 Intent；
- BRAND_MISMATCH 可形成 Memory Candidate，但不能自动成为偏好。

## A.9.5 ReworkRequest

~~~yaml
ReworkRequest:
  rework_request_id: string
  version: integer
  brand_id: string
  task_id: string
  review_ref: VersionedRef
  target_artifact_ref: VersionedRef
  scope: LOCAL | STRATEGY
  reason: ReworkReason
  instruction: string
  affected_artifact_refs: VersionedRef[]
  local_rework_count: integer
  strategy_rework_count: integer
  outcome: ALLOWED | HUMAN_DECISION_REQUIRED
~~~

控制规则：

~~~text
局部返工最多 2 次
策略重做最多 1 次
~~~

超限时 outcome 为 HUMAN_DECISION_REQUIRED，Task 保持 REVIEW_REQUIRED，系统停止自动生成。

局部返工只重算 affected_artifact_refs 及 A.8 最小依赖表中的下游依赖。策略重做先使 Task 返回 DRAFT，在复用或更新 Intent 后重新运行 Business Decision，合法候选形成后进入 DECISION_READY；目标改变返回 DRAFT 并重新运行 Intent。

## A.9.6 BrandMemory

~~~yaml
BrandMemoryCandidate:
  candidate_id: string
  version: integer
  brand_id: string
  type: PREFERENCE
  statement: string
  evidence_refs: VersionedRef[]
  proposed_from: DECISION_SELECTION | REVIEW_DELTA
  status: PENDING_APPROVAL
  created_at: datetime

ApprovedBrandMemory:
  memory_id: string
  version: integer
  brand_id: string
  type: PREFERENCE
  statement: string
  evidence_refs: VersionedRef[]
  approved_by_role: FOUNDER_REVIEWER
  approved_at: datetime
  status: APPROVED | REVOKED
~~~

只有 APPROVED Memory 可以作为后续品牌偏好上下文。它始终属于 PREFERENCE，不是 FACT 或硬规则，不自动修改 Prompt、规则或模型权重。

---

# A.10 主 PRD 需求映射

| 主 PRD ID | 本附录承接位置 |
|---|---|
| INT-01 | A.5.2 的 goal_resolution、business_goal 和 goal_candidates |
| INT-02 | A.4.2 与 A.5.2 的 QUICK、ENHANCED 和阻断项 |
| INT-03 | A.4.3 与 A.5.2 的版本化 Snapshot 和目标迁移 |
| INT-04 | A.5.2 的完整 IntentExecutionPlan |
| INT-05 | A.2.3、A.2.4、A.9.2 的来源和 Trace |
| BD-01 | A.6.2 recognized_conflicts |
| BD-02 | A.6.2、A.6.3 的候选数量状态、降级原因与实质差异候选 |
| BD-03 | A.1.2、A.9.2 的四类 Trace |
| BD-04 | A.3、A.6.3 的事实引用与边界 |
| BD-05 | A.6.2、A.6.3 的 comparative_tradeoffs 和候选取舍 |
| BD-06 | A.6.3 的五项定性评价和风险 |
| BD-07 | A.6.3 的条件化判断、风险和置信度 |
| BD-08 | A.6.4 DecisionSelection |
| CR-01 | A.7.1、A.7.2 的精确 DecisionSelection、BusinessDecisionBundle 与 candidate 引用 |
| CR-02 | A.7.2、A.8 的九项完整制作包与批准后 MarkdownExportManifest |
| CR-03 | A.8 的 Persona、口播、画面与评论一致性 |
| CR-04 | A.8 的视频号人物、关系和信任结构 |
| CR-05 | A.8 的 Script、Storyboard 与 ProductPlacement 执行字段 |
| CR-06 | A.3.3、A.7.2 的 VisualProfile 与不确定性 |
| CR-07 | A.8、A.9.1 的事实和硬规则约束 |
| SYS-01 | A.4.4 七状态合同 |
| SYS-02 | A.4.3 版本化 ContextSnapshot |
| SYS-03 | A.9.1 硬规则阻断 |
| SYS-04 | A.7.2、A.8、A.9.3 的 Artifact 版本、双重决策引用与最小父依赖 |
| SYS-05 | A.6.4、A.9.4 的 DecisionSelection、ReviewRecord 与 ReviewDelta |
| SYS-06 | A.9.5 返工范围、次数和停止条件 |
| SYS-07 | A.4.5、A.4.6 的超时、格式失败与受控降级 |
| SYS-08 | A.1.3 与 SourceRef 的单品牌、凭证和文件边界 |
| SYS-09 | A.4.5 的模型、延迟、Token 和成本记录 |
| SYS-10 | A.1.1、A.9.6 的人工批准 BrandMemory |

---

# A.11 实现边界

本附录不预设工作流平台、数据库或接口协议。实现可以借用模型 Adapter、文件解析、托管数据库、对象存储、Dify 或其他薄外壳。

无论采用何种组件，以下语义不得丢失：

~~~text
版本化企业事实
Context Snapshot
Fact / Rule / Assumption / Model Judgment 分离
Founder 人工选择
九项制作交付包
批准后 Markdown 导出
Artifact Parent Reference
Review Delta
有界 Rework
单品牌隔离
最低运行记录
~~~

本附录不要求建设多租户 RLS、企业 IAM、管理员后台、复杂 DAG、自动学习、经验大库、综合评分平台或大规模性能体系。
