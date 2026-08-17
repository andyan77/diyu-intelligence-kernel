# B｜三个核心模块智能验收合同

## B.0 文档控制

| 项目 | 内容 |
|---|---|
| 文档编号 | DIYU-MVP-V3-B |
| 版本 | v0.3 |
| 状态 | **EFFECTIVE（已批准生效）** |
| 批准 | Founder（Faye）2026-08-17 批准；生效基线 = 主 PRD v0.1 + 附录 A v0.1 + 附录 B v0.3（当日经 v0.2→v0.3 标签补登修订，Founder 批准）三份一并生效 |
| v0.1→v0.2 修订 | Founder 2026-08-17 裁决（OD-04）：制作判断由 Founder 以制作视角承担，取消外部制作裁判角色——修订 B.5.2 与 Gate IA-3 对应条文；其余条款不变。修订依据与风险知悉记录见《裁决台账》 |
| v0.2→v0.3 修订 | Founder 2026-08-17 裁决：B.6.2 补登失败标签 BD_SCOPE_MISREPRESENTED，修复 BD-D02 引用了未登记标签的缺陷；其余条款不变。裁决记录见《裁决台账》 |
| 适用产品 | 笛语智能核 MVP V3.0 |
| 关联主文档 | PRD_笛语智能核_MVP_V3.0_v0.1.md |
| 关联数据合同 | A_模块接口与核心数据字典.md |
| 合同责任人 | Founder / Reviewer |
| 生效方式 | 与同版本主 PRD、附录 A 一并批准 |
| 验收效力 | 对对应里程碑具有阻断权 |

本合同回答且只回答一个问题：

> **在相同企业事实、相同基础模型和相同输出要求下，笛语的商业决策与视频号内容制作交付包，是否明显优于直接使用 ChatGPT／Claude？**

主 PRD 定义产品应具备什么能力、如何运行；本合同定义如何证明这些能力成立。二者不能互相替代。

当本合同对应的退出门未通过时，即使代码测试通过、页面可操作、Schema 合法、接口联通，也不得宣称相应里程碑完成。

本合同中的“必须”和“不得”是阻断性要求；“允许答案族”表示可以存在多种合理答案，不代表唯一标准文案。

---

# B.1 验收总原则

## B.1.1 三层证据缺一不可

正式智能验收由三类证据组成：

1. 三个核心模块的诊断案例；
2. 同条件端到端匿名 A/B；
3. 人工选择、修改严重度和失败分类记录。

模块诊断证明各模块是否具备目标能力；端到端 A/B 判断产品是否优于通用 LLM；人工记录证明结果是否真正值得投入制作。

单独完成任何一层，都不能回答 MVP 的终极验证问题。

## B.1.2 不设置综合总分

本合同不采用：

- 综合总分；
- 自动审美评分；
- 数百格打分矩阵；
- 用例通过数量作为完成度；
- 用平均分掩盖关键失败；
- LLM Judge 单独决定发布。

案例结果只允许：

~~~text
PASS
FAIL
INCONCLUSIVE
~~~

INCONCLUSIVE 不等于通过，必须补齐证据、重新运行或重新裁判。

## B.1.3 允许答案族，不设唯一答案

商业决策和创意内容可以存在多个合理答案。验收关注：

- 是否忠于企业事实；
- 是否识别真实商业问题；
- 是否形成有实质差异的选择；
- 是否解释取舍；
- 是否遵守品牌和任务规则；
- 是否忠实传递人工选择；
- 是否能转化为实际制作；
- 是否明显优于直接调用通用 LLM。

不得把某一句文案、某一种创意或某一个推荐方向写成唯一正确答案。

## B.1.4 先事实，后经验

首轮 MVP 验收只允许使用：

- Brand Facts；
- Product Facts；
- Audience Facts；
- Persona Facts；
- Video Account Facts；
- 当前任务合同；
- 已批准硬规则；
- 通用基础模型的内化能力。

首轮验收关闭 Brand Memory。后续评估 Brand Memory 时，只能使用人工批准的记录，并必须在 Case Manifest 中显式列出。

禁止使用未批准的钩子库、卖点库、场景库、人群经验库或成品素材库为笛语提供隐藏优势。

## B.1.5 人工裁判拥有最终语义裁决权

确定性程序负责检查：

- Schema；
- 必填字段和枚举；
- 硬规则；
- Runtime 状态；
- Artifact Reference；
- 超时和格式失败；
- 成本与延迟记录。

人工裁判负责判断：

- 商业冲突是否真实；
- 候选是否有实质差异；
- 取舍是否有价值；
- 创意是否忠实承接决策；
- 内容是否符合视频号；
- 制作人员是否愿意实际使用；
- 笛语是否明显优于基线。

LLM Judge 只能辅助格式检查、失败标签建议或证据整理，不能独立给出里程碑 PASS。

---

# B.2 受控测试条件

## B.2.1 Case Manifest

每个正式案例运行前必须冻结一份 Case Manifest：

~~~yaml
CaseManifest:
  case_id: string
  case_version: string
  prd_version: string
  data_contract_version: string
  acceptance_contract_version: string
  context_snapshot_id: string
  snapshot_hash: string
  task_statement: string
  execution_mode: QUICK | ENHANCED
  hard_rule_refs: VersionedRef[]
  output_schema_version: string
  brand_memory_state: DISABLED | APPROVED_SET
  approved_brand_memory_refs: VersionedRef[]
  e2e_interaction_contract_version: string | null
  e2e_output_contract_version: string | null
  baseline_prompt_versions:
    decision_stage: string | null
    creative_stage: string | null
  diyu_build_version: string
  module_contract_versions:
    intent: string
    business_decision: string
    creative: string
  model_provider: string
  model_name: string
  model_version: string | null
  generation_parameters_hash: string
  allowed_tools: string[]
  approved_by: string
  approved_at: datetime
~~~

不得在查看结果后修改事实、裁判问题、允许答案、禁止结果或通过条件。确需修改时，必须升级案例版本并重新运行两侧。

## B.2.2 “同条件”的定义

正式 A/B 必须满足：

- 相同 Context Snapshot；
- 相同商品图片和其他输入材料；
- 相同业务任务；
- 相同硬规则；
- 相同最终输出合同；
- 相同模型供应商和基础模型版本；
- 相同生成参数与工具访问边界；
- 不允许任一侧使用未声明的搜索或知识库；
- Brand Memory 启用状态和 approved_brand_memory_refs 完全一致；DISABLED 时引用列表必须为空。

笛语可以进行多模块、多次模型调用，因为编排本身是被验证的能力，但必须记录总调用次数、Token、成本和延迟，不得通过无限调用换取结果。

## B.2.3 共同两阶段交互与输出合同

端到端 A/B 的两侧必须执行同一外部交互合同，不能让笛语回答“候选加制作包”，却只让基线回答一段成品文案。

**阶段 D｜商业候选：** 两侧接收同一 Snapshot、任务和规则，并输出同一外部 Schema：business_problem、recognized_conflicts、目标三个且最低两个 candidate_options、candidate_count_status、candidate_count_explanation、comparative_tradeoffs、risks、FACT / RULE / ASSUMPTION / MODEL_JUDGMENT 区分及 confidence。笛语内部对象可转换为该展示 Schema，但不能增加只对一侧可见的业务内容。

阶段 D 输出先匿名。Founder / Reviewer 在不知道来源时，分别为 X、Y 选择一个 candidate_id；选择、理由和时间冻结后才进入下一阶段。

**阶段 C｜制作交付包：** 两侧各自接收本侧被选候选以及相同原始事实和规则，并输出同一九部分制作包 Schema、production_risks、assumptions 与 confidence。两阶段结果合并为同一 E2EComparisonEnvelope 后再进行最终匿名裁判：

~~~yaml
E2EComparisonEnvelope:
  decision_output_ref: string
  frozen_selection_ref: string
  creative_package_ref: string
  selected_candidate_id: string
  package_section_count: 9
  output_contract_version: string
~~~

共同合同只约束可比较的外部语义和结构，不要求基线伪造笛语内部 Run、Artifact 或 Trace ID。

## B.2.4 通用 LLM 基线

正式基线是不经过笛语模块的同基础模型直接调用。为遵守共同交互合同，阶段 D 和阶段 C 各允许一次受控直接调用；除此之外不得增加隐藏迭代、自我批改或人工改写。每阶段输入包括：

- 相同企业事实；
- 相同业务任务；
- 相同硬规则；
- 相同最终输出合同。

两阶段基线 Prompt 都必须在运行前冻结，不得故意写弱，也不得包含笛语内部模块结果、隐藏规则或另一侧中间产物。阶段 C 只可接收本侧已经匿名冻结的候选选择。

ChatGPT 或 Claude 消费端界面可以作为补充观察，但其模型版本、系统提示或工具状态不可确认时，不能单独构成“同基础模型条件”的正式证据。

## B.2.5 匿名处理

端到端结果必须：

- 使用随机 X、Y 标签；
- 隐藏生成来源；
- 使用相同外层展示格式；
- 隐藏系统名、Prompt、调用次数和模型日志；
- 随机排列展示顺序；
- 在揭晓来源前冻结裁判原始选择。

匿名处理不得修改业务内容。

---

# B.3 进入智能验收前的最低运行检查

这些检查只判断系统能否安全进入智能验收，不参与智能能力评分。

| 检查 ID | 检查内容 | 通过条件 | 映射需求 |
|---|---|---|---|
| PRE-01-I | Intent Schema | 有效 Intent 输入可解析；缺必填字段时返回受控错误；不得展示半成品为成功 | INT-04、SYS-07 |
| PRE-01-B | Business Decision Schema | 有效 Decision 输入输出可解析；候选数量状态与降级原因合法；半结构化文本不得冒充成功 | BD-02、SYS-07 |
| PRE-01-C | Creative、九项资产与导出 Schema | 九项资产和批准后 Markdown 导出可校验；缺项、错版本或导出失败不得标记成功 | CR-02、SYS-07 |
| PRE-02-B | Decision 事实与硬规则 | 商品池、库存、价格、品牌禁令等事实或规则冲突时阻断 BusinessDecision 候选，不得补写或绕过 | BD-04、SYS-03 |
| PRE-02-C | Creative 事实、硬规则与包完整性 | Creative 违反禁用表达、商品事实或九项包完整性时阻断 Artifact | CR-07、SYS-03 |
| PRE-03-M | 通用模型与格式失败 | 当前里程碑模块的 MODEL_TIMEOUT、MODEL_UNAVAILABLE、FORMAT_INVALID / SCHEMA_INVALID 均有有界重试和明确降级或 FAILED，不得伪装成功 | SYS-07 |
| PRE-03-V | 视觉输入失败 | VISUAL_INPUT_UNREADABLE 和低置信视觉属性均显式降级，不得伪装成确认事实或成功视觉识别 | CR-06、SYS-07 |
| PRE-04 | 单品牌隔离 | 当前案例不得引用另一品牌的事实、文件、Artifact 或 Memory | SYS-08 |
| PRE-05 | 基础凭证和文件安全 | 输出、日志及 M3 起的导出物不暴露凭证、临时令牌或未授权文件 | SYS-08 |
| PRE-06 | 成本与延迟记录 | 每个 Run 可追溯模型版本、Token、估算成本和总延迟 | SYS-09 |
| PRE-07-I | Intent 状态、版本与引用 | 只使用七状态；DRAFT、NEEDS_INPUT、FAILED 相关迁移命中 A.4.4；非法迁移被拒绝；Intent Artifact 与 Snapshot 引用有效 | SYS-01、SYS-02、SYS-04 |
| PRE-07-B | Decision 状态、版本与引用 | DRAFT → DECISION_READY 及拒绝、目标变化路径合法；DecisionSelection、SELECT_CANDIDATE ReviewRecord、Bundle 与 candidate_id 精确一致 | SYS-01、SYS-04、SYS-05 |
| PRE-07-C | Creative、返工与终态 | DECISION_READY → CREATIVE_READY → REVIEW_REQUIRED、局部返工、策略重做、FAILED 重启、批准及人工终止路径合法；人工终止产生 TERMINATE ReviewRecord 与 MANUAL_TERMINATION FailureRecord；非法迁移被拒绝；COMPLETED 无后继；返工超限不产生第八状态；双重决策引用和父引用有效 | SYS-01、SYS-04、SYS-05、SYS-06 |

任一最低运行检查失败时，不得进入正式端到端 A/B。

---

# B.4 模块诊断案例

模块诊断尽量隔离被测模块：

- Intent 测试不依赖后续创意质量；
- Business Decision 测试使用冻结的 IntentExecutionPlan；
- Creative 测试使用人工冻结的 DecisionSelection；
- 返工测试使用冻结的父 Artifact。

其他模块的优秀输出不能抵消被测模块失败。

## B.4.1 Intent Intelligence

### INT-D01｜模糊目标不得擅自确定

**映射：** INT-01、INT-04、INT-05

**输入：**

> 帮我推广羊绒大衣。

商品存在，但未提供新品曝光、库存激活、转化或品牌建设目标。

**允许答案族：**

- 提出一个最关键澄清问题；
- 返回少量可能目标供用户选择；
- 用户明确选择快速模式时，可以返回暂定目标候选，但必须保留 AMBIGUOUS、missing_context、assumptions 和非高置信度；
- goal_resolution 非 RESOLVED 时 next_action=REQUEST_INPUT，Task 进入 NEEDS_INPUT，直到人工明确目标。

**禁止结果：**

- 静默确定唯一目标；
- 虚构库存、销售目标、受众或品牌定位；
- 在关键目标未知时给出 HIGH confidence；
- 未经人工确认直接进入唯一商业策略。
- 以“已给出两个目标候选”为由设置 CONTINUE_TO_DECISION。

**人工裁判问题：**

1. 系统是否承认目标尚未确定？
2. 请求的信息是否是当前任务真正需要的？
3. 假设是否容易被用户识别和纠正？

**主要失败标签：**

INT_GOAL_ASSUMED、INT_MISSING_CONTEXT_MISSED、INT_CONFIDENCE_OVERSTATED、BD_HUMAN_GATE_BYPASSED。

### INT-D02｜快速模式与增强模式

**映射：** INT-02、INT-04、INT-05

**输入：**

> 为这件羊绒大衣制作春节前视频号内容。

商品基本事实存在，但缺少影响表达的账号人格或品牌信息。

**允许答案族：**

快速模式：

- 非阻断信息缺失时允许继续；
- 显式列出 missing_context；
- 把暂定内容标为 ASSUMPTION；
- 降低 confidence；
- 不把暂定人设写成事实。

增强模式：

- 只追问能改变当前任务判断的关键信息；
- 阻断项缺失时进入 NEEDS_INPUT；
- 资料补充后生成新 Context Snapshot。

**禁止结果：**

- 编造创始人背景、账号关系或品牌禁语；
- 不提示缺失却输出确定结论；
- 为单一任务索取大量无关资料；
- 快速模式绕过阻断项；
- 强制完成完整企业资料库。

**人工裁判问题：**

1. 快速模式能否继续但不掩盖不确定性？
2. 增强模式是否只询问高价值信息？
3. 事实、缺失项和假设是否清晰分离？

**主要失败标签：**

INT_MISSING_CONTEXT_MISSED、INT_CONFIDENCE_OVERSTATED、INT_OVER_COLLECTION、INT_MODE_IGNORED、BD_FACT_FABRICATION。

### INT-D03｜同一商品的目标迁移

**映射：** INT-03、INT-04、INT-05、SYS-02

**输入 A：**

> 用这件羊绒大衣促进春节前库存消化。

**输入 B：**

> 用同一件羊绒大衣建立品牌长期价值，不以本期销量为主要目标。

除商业目标外，两组使用相同事实快照。

**允许答案族：**

- business_goal、required_context 和下游重点发生可解释变化；
- 商品和品牌事实保持不变；
- 不要求特定文案。

**禁止结果：**

- 两次 IntentExecutionPlan 只有措辞差异；
- 库存激活目标残留在品牌建设任务中；
- 因目标变化篡改稳定事实；
- 后一次读取前一次未批准判断。

**人工裁判问题：**

1. 目标变化是否真正改变了任务计划？
2. 应保持不变的事实是否保持？
3. 变化是否足以驱动不同的 Business Decision？

**主要失败标签：**

INT_COUNTERFACTUAL_NOT_PROPAGATED、INT_CROSS_RUN_CONTAMINATION、SYS_LINEAGE_BROKEN。

## B.4.2 Business Decision Engine

所有 Business Decision 案例都必须区分 FACT、RULE、ASSUMPTION 和 MODEL_JUDGMENT。混写成不可追溯文本时不得通过。

### BD-D01｜高端品牌的库存与价值冲突

**映射：** BD-01、BD-02、BD-03、BD-05、BD-06、BD-08、SYS-03

**冻结事实：**

~~~yaml
inventory: 800
brand_positioning: HIGH_END
forbidden_expression:
  - LOW_PRICE_SELLING
business_goal: INVENTORY_ACTIVATION
~~~

**两候选降级分支：** 另冻结一组规则，使第三条原本可能的促销路径明确违反高端品牌禁令，而其余事实只足以支持两个实质差异方向。该分支不要求凑出第三个候选；要求 candidate_count_status=DEGRADED_TWO，并在 candidate_count_explanation 中引用限制原因。输出两个却无原因、用措辞变化补第三个，或少于两个仍进入 DECISION_READY，均为 FAIL。

**能力问题：**

系统能否识别“需要销量”与“不能损害高端品牌价值”的冲突，并形成可供人工选择的商业候选？

**允许答案族：**

可以采用人物信任、产品价值证明、场景需求或其他有事实依据的路线。候选必须在商业机制、商品角色、叙事或风险取舍上有实质差异。

每个候选必须说明：

- 为什么选择该路径；
- 为什么不优先选择主要替代路径；
- 主要风险；
- 哪些内容只是模型判断。

**禁止结果：**

- 使用低价、甩卖或虚假稀缺表达；
- 忽略库存和品牌价值冲突；
- 候选只是标题和措辞变化；
- 只给唯一结论；
- 保证销量、转化率或爆款；
- 未经人工选择直接进入 Creative。

**人工裁判问题：**

1. 系统识别的是该品牌的商业冲突，还是通用营销问题？
2. 候选是否值得 Founder 真正选择？
3. 取舍说明是否足以帮助拒绝另一方向？
4. 事实、规则、假设和判断是否分离？

**主要失败标签：**

BD_CONFLICT_MISSED、BD_CANDIDATE_COLLAPSE、BD_TRADEOFF_MISSING、BD_TRACE_MIXED、SYS_RULE_VIOLATION、BD_HUMAN_GATE_BYPASSED。

### BD-D02｜有限商品池不得补写

**映射：** BD-04、BD-05、SYS-03

**冻结事实：**

商品池只有三个商品，用户要求“做十套穿搭”。

**允许答案族：**

- 说明现有商品不足以支持十套独立商品组合；
- 请求补充商品；
- 收敛为少量核心穿搭；
- 复用同一商品但明确说明；
- 使用通用辅助单品时，明确它不是企业商品池 SKU。

**禁止结果：**

- 虚构七个商品、颜色、尺码或库存；
- 把通用搭配建议伪装为企业商品；
- 重复组合却宣称十个实质不同方案；
- 不披露事实边界。

**人工裁判问题：**

1. 系统是否宁可调整方案，也不创造事实？
2. 替代方案是否仍有商业和制作价值？
3. 外部通用单品的边界是否清楚？

**主要失败标签：**

BD_FACT_FABRICATION、BD_SCOPE_MISREPRESENTED、SYS_FACT_BOUNDARY_BROKEN。

### BD-D03｜反常识商品的情境判断

**映射：** BD-06、BD-07

**输入：**

商品为荧光绿色裤装，并提供品牌定位、受众、场景和商业目标。

**允许答案族：**

系统可以推荐，也可以不推荐，但必须结合：

- 色彩面积；
- 层次关系；
- 搭配方式；
- 使用场景；
- 目标受众；
- 商业目标；
- 品牌表达边界。

**禁止结果：**

- 仅凭“颜色太大胆”直接否定；
- 无视品牌和目标而一律追求猎奇；
- 宣称荧光色天然带来流量；
- 把审美偏好写成企业事实；
- 为证明反常识而强行推荐不可执行方案。

**人工裁判问题：**

1. 结论是否来自情境判断？
2. 系统是否说明商品怎样服务或不能服务目标？
3. 风险和使用边界是否具体？

**主要失败标签：**

BD_CONTEXTUAL_REASONING_MISSING、BD_UNGROUNDED_REJECTION、BD_UNGROUNDED_RECOMMENDATION、BD_TRACE_MIXED。

## B.4.3 Creative Content Engine

### CR-D01｜同一方向下的人设反事实

**映射：** CR-01、CR-03

**输入：**

使用相同商品、商业目标和已选候选，分别切换：

- 品牌主理人人设；
- 年轻买手人设。

**允许答案族：**

两份内容保持相同商业命题和商品事实，但在信任关系、口播、Hook、举例方式、镜头重心和情绪路径上产生有意义差异。

**禁止结果：**

- 只替换称谓或少量形容词；
- 人设变化导致商业方向漂移；
- 为强化人设编造人物经历；
- Script、PersonaCard、Storyboard 和评论回复使用不同人设。

**人工裁判问题：**

1. 不看标签能否识别两种关系？
2. 两种表达是否仍服务同一商业决策？
3. 人设变化是否贯穿口播、画面和商品展示？

**主要失败标签：**

CR_PERSONA_DRIFT、CR_DECISION_DRIFT、CR_CROSS_ARTIFACT_CONFLICT、BD_FACT_FABRICATION。

### CR-D02｜视频号语法与决策承接

**映射：** CR-01、CR-04

**输入：**

冻结一个由 Founder / Reviewer 选定的 Business Decision。

**允许答案族：**

形式可以不同，但必须：

- 有明确说话的人；
- 建立人与受众的关系；
- 通过表达过程建立信任；
- 适合口播和视频观看；
- 将所选方向落实到 Hook、叙事、商品证明和行动引导。

**禁止结果：**

- 实质为小红书图文笔记；
- 以标签和种草清单替代人物表达；
- 内容流畅但改变已选方向；
- 未经批准重新选择候选；
- 只写平台名，结构中没有人物、关系或信任。

**人工裁判问题：**

1. 这是视频号中的人物表达，还是换平台名的通用文案？
2. 内容能否回指已选商业方向？
3. 商品出现是否服务叙事？

**主要失败标签：**

CR_PLATFORM_MISMATCH、CR_DECISION_DRIFT、CR_GENERIC_COPY_ONLY。

### CR-D03｜完整且可制作的交付包

**映射：** CR-02、CR-03、CR-05、SYS-04

输出必须包含：

1. Content Brief；
2. Creative Strategy；
3. Persona Card；
4. Video Script；
5. Storyboard；
6. Voice Package；
7. Audio Direction；
8. Product Placement；
9. Comment Operation Package。

**允许答案族：**

不要求影视工业级分镜，但制作人员应能回答：

- 谁来说；
- 对谁说；
- 为什么这样说；
- 每段拍什么；
- 商品何时出现；
- 口播如何执行；
- 音频是什么方向；
- 评论区如何承接；
- Founder / Reviewer 批准后，能否把同一权威版本的九项资产完整导出为 Markdown。

**禁止结果：**

- 缺少任一必需交付物；
- Storyboard 无法指导拍摄；
- Script、VoicePackage 与 PersonaCard 矛盾；
- ProductPlacement 与商业策略无关；
- 关键条件需要制作人员重新猜测；
- 只有漂亮文字，没有拍摄行动；
- 导出缺项、引用旧版本、在导出时改写内容或失败却标记成功。

**人工裁判问题：**

1. 如果明天开拍，是否还需要重新做一次商业策划？
2. 九项资产是否共同指向一个方案？
3. 修改一处时能否按附录 A 的最小依赖定位受影响产物？
4. 批准后的 Markdown 是否与九项权威对象逐项一致？

**主要失败标签：**

CR_PACKAGE_INCOMPLETE、CR_NOT_PRODUCIBLE、CR_CROSS_ARTIFACT_CONFLICT、CR_DECISION_DRIFT、SYS_LINEAGE_BROKEN。

### CR-D04｜视觉证据与硬规则

**映射：** CR-06、CR-07、SYS-03

**输入 A：** 提供清晰商品图片。

**输入 B：** 不提供图片，只提供商品名称与已确认文字事实。

**输入 C：** 提供损坏、不可读或只能低置信识别局部属性的图片。

**允许答案族：**

- 输入 A 形成带图片来源的 PROVISIONAL VisualProfile；
- 输入 B 不编造颜色、版型、纹理或细节；
- 输入 C 返回 VISUAL_INPUT_UNREADABLE，或只保留可引用的低置信 PROVISIONAL 属性并明确限制；
- 三种输入都遵守品牌禁用表达和商品事实；
- 无视觉证据时给出不依赖未知细节的拍摄建议。

**禁止结果：**

- 无图时依据商品名称猜测视觉属性；
- 图片不可读或低置信时仍输出确定视觉属性；
- 把 VLM 观察写成已确认事实；
- 视觉创意覆盖品牌硬规则；
- 使用不存在的材质、颜色或商品细节。

**人工裁判问题：**

1. 视觉结论是否能回指图片？
2. 无图时系统是否诚实降级？
3. 创意是否在事实和规则边界内仍具有可制作性？

**主要失败标签：**

CR_VISUAL_FABRICATION、CR_VISUAL_CONFIDENCE_OVERSTATED、SYS_RULE_VIOLATION、SYS_FACT_BOUNDARY_BROKEN。

## B.4.4 横向受控能力

### SYS-D01｜选择、批准、局部返工、版本引用与停止条件

**映射：** SYS-04、SYS-05、SYS-06、SYS-10

**前置条件：**

存在 BusinessDecisionBundle v1。Founder / Reviewer 先选择候选，形成成对、关联一致且 candidate_id 相同的 SELECT_CANDIDATE ReviewRecord 与 DecisionSelection；随后形成 CreativeBundle v1 → VideoScript v1。

制作使用者提出一个明确局部问题，例如：

- 当前拍摄场景不可用；
- 某句口播缺少事实依据；
- 某个镜头违反品牌规则。

**通过条件：**

- 候选选择同时记录 ReviewRecord 和 DecisionSelection，二者精确引用 BusinessDecisionBundle v1 与 candidate_id；
- 修改原因使用受控枚举；
- 只重做受影响 Artifact 及附录 A 最小依赖表中的下游依赖；
- 不改变已选商业方向；
- 产生新版本与 parent_references，并保留 DecisionSelection 与 BusinessDecisionBundle 双重引用；
- ReviewDelta 记录修改前后；
- 两次局部修改或一次策略重做后停止自动生成；
- 策略重做采用 REVIEW_REQUIRED → DRAFT → DECISION_READY，局部返工采用 REVIEW_REQUIRED → CREATIVE_READY → REVIEW_REQUIRED；
- 超限时保持 REVIEW_REQUIRED 并设置 human_decision_required；
- 超限后若 Founder / Reviewer 选择人工终止，形成 TERMINATE ReviewRecord 和 MANUAL_TERMINATION FailureRecord，并沿 REVIEW_REQUIRED → FAILED；
- 只有人工批准的偏好进入 BrandMemory；
- 对当前 CreativeContentBundle 的 APPROVE_PACKAGE ReviewRecord 触发 COMPLETED，旧版本或未通过 validation 的包不能被批准。

**禁止结果：**

- 修改一句口播却重生成全部策略；
- 局部问题导致候选被静默替换；
- 候选选择只写自由文本，或 ReviewRecord 与 DecisionSelection 指向不同 candidate_id；
- 覆盖旧版本；
- 把“感觉不好”自动沉淀为规则；
- 无限重试；
- 模型自行批准 BrandMemory；
- 没有 APPROVE_PACKAGE 记录就进入 COMPLETED。

**主要失败标签：**

SYS_LINEAGE_BROKEN、SYS_REWORK_SCOPE_EXPANDED、SYS_REWORK_LIMIT_BYPASSED、SYS_UNAPPROVED_MEMORY_USED、CR_DECISION_DRIFT。

---

# B.5 端到端匿名 A/B

## B.5.1 锁定场景

首轮正式验收使用三个不可互相替代的高价值场景。增加大量相似案例不能抵消任一锁定场景的关键失败。

### E2E-01｜高端品牌库存激活

核心事实：

- 羊绒大衣库存 800 件；
- 品牌定位高端；
- 禁止低价叫卖；
- 目标是在限定周期内促进销售；
- Persona 和 VideoAccountFacts 按 Manifest 冻结。

必须经历：

~~~text
Intent
→ 商业冲突识别
→ 目标三个、最低两个候选
→ 阶段 D 匿名人工选择
→ 阶段 C 完整视频号制作交付包
→ E2EComparisonEnvelope 匿名终审
~~~

该场景证明笛语能否处理“销量与品牌价值”的冲突。

### E2E-02｜同事实下的品牌资产目标

与 E2E-01 使用相同企业事实，只把目标改为：

> 建立长期品牌资产，不以本期销量为主要目标。

该场景证明：

- Intent 是否随目标迁移；
- Business Decision 是否改变取舍；
- Creative 是否承接新方向；
- 系统是否避免沿用库存激活结果。

### E2E-03｜反常识商品的可用创意

商品为荧光绿色裤装；品牌、受众、Persona 和商业目标在 Manifest 中冻结。

不要求系统必须推荐该商品，而要求它基于面积、层次、场景、受众、品牌和目标形成可解释判断，并把人工选定方向转成可拍摄的完整交付包。

## B.5.2 人工裁判构成（v0.2 修订）

每个端到端案例至少需要两类判断：

- 商业判断：Founder / Reviewer 或实际商业决策人；
- 制作判断：由 Founder 以制作使用者视角承担（v0.2 修订：取消外部制作裁判角色，Founder 2026-08-17 裁决，说服力折损风险已知悉）。

两类判断必须**时间分离、独立作答**：先完整提交商业问卷并冻结，之后（至少间隔一个工作时段）再以制作视角作答制作问卷；作答制作问卷时不得修改已冻结的商业问卷。两类关键选择不一致时，案例为 INCONCLUSIVE，可引入另一名独立裁判或修复后重测，不得取平均分宣称通过。

## B.5.3 匿名裁判问题

商业裁判回答：

1. 哪一份更准确理解真实商业任务？
2. 哪一份候选更值得进行真实商业选择？
3. 哪一份更清楚说明事实、规则、假设、取舍和风险？
4. 如果只能选一份进入生产，选择 X、Y、NEITHER 还是 NO_MATERIAL_DIFFERENCE？
5. 必须修改什么才会批准？

制作裁判回答：

1. 哪一份更忠实承接已选商业方向？
2. 哪一份更符合视频号人物、关系和信任表达？
3. 哪一份可以更直接进入拍摄？
4. 哪一份减少了制作前重新解释和沟通？
5. 如果只能选一份实际制作，选择 X、Y、NEITHER 还是 NO_MATERIAL_DIFFERENCE？
6. 必须修改哪些资产？

所有裁判还必须回答：

> 优势是否来自商业判断和可制作性，而不只是篇幅、排版或文字流畅度？

## B.5.4 人工结果记录

商业裁判和制作裁判各自先记录：

~~~text
X
Y
NEITHER
NO_MATERIAL_DIFFERENCE
~~~

每个选择必须附理由和需要修改的字段或资产，并在来源揭晓前冻结。X/Y 与 DIYU/BASELINE 的映射只能在两类裁判提交后解封。

Decision Acceptance：

~~~text
SELECTED_AS_IS
SELECTED_WITH_LOCAL_EDIT
REJECTED
INCONCLUSIVE
~~~

Content Adoption：

~~~text
READY_TO_PRODUCE
LOCAL_EDIT_REQUIRED
STRATEGIC_REWORK_REQUIRED
UNUSABLE
INCONCLUSIVE
~~~

Edit Severity：

~~~text
NONE
LOCAL
MATERIAL
REBUILD
~~~

- NONE：无需修改；
- LOCAL：不改变商业方向的局部文案、镜头或执行修正；
- MATERIAL：跨多个资产修改，或改变关键命题、人设或结构；
- REBUILD：重新选择策略或重做大部分交付包。

Edit Severity 是修改分类，不是分数，不得转换为总分或平均分。

## B.5.5 “明显优于”的案例判定

某个端到端案例只有同时满足以下条件，才可判定笛语明显优于基线：

1. 商业裁判选择笛语进入实际生产链路；
2. 制作裁判选择笛语作为实际制作输入；
3. 理由至少命中以下一项，而非只评价文风或排版：
   - 更准确识别商业冲突；
   - 候选和取舍更有价值；
   - 事实与规则约束更可靠；
   - 更忠实承接人工决策；
   - 制作可执行性更高；
4. 笛语没有阻断性失败；
5. 笛语所需修改不高于 LOCAL；
6. 基线不是同等可用或更值得制作。

NO_MATERIAL_DIFFERENCE 不能证明 MVP 价值。

三个锁定场景分别承担不同能力证明，必须逐案通过；其他案例数量不能抵消其中任何一个失败。

---

# B.6 失败标签

失败标签用于定位和修复，不用于加权计分。

## B.6.1 Intent

| 标签 | 含义 |
|---|---|
| INT_GOAL_ASSUMED | 目标不明确时擅自确定唯一目标 |
| INT_MISSING_CONTEXT_MISSED | 未识别关键缺失信息 |
| INT_CONFIDENCE_OVERSTATED | 不确定条件下置信度过高 |
| INT_OVER_COLLECTION | 索取与当前任务无关的大量资料 |
| INT_MODE_IGNORED | 未遵守快速或增强模式 |
| INT_COUNTERFACTUAL_NOT_PROPAGATED | 目标变化未改变计划 |
| INT_CROSS_RUN_CONTAMINATION | 前一任务未批准判断污染当前任务 |

## B.6.2 Business Decision

| 标签 | 含义 |
|---|---|
| BD_CONFLICT_MISSED | 未识别核心商业冲突 |
| BD_CANDIDATE_COLLAPSE | 多个候选实质相同 |
| BD_TRADEOFF_MISSING | 未说明选择与放弃原因 |
| BD_FACT_FABRICATION | 虚构企业、商品、受众或经营事实 |
| BD_SCOPE_MISREPRESENTED | 把无法满足的任务范围宣称为已满足或可满足（如重复组合冒充足量方案、隐瞒范围缺口） |
| BD_TRACE_MIXED | 事实、规则、假设和判断混写 |
| BD_CONTEXTUAL_REASONING_MISSING | 只套用通用偏好 |
| BD_UNGROUNDED_REJECTION | 无依据否定商品或方向 |
| BD_UNGROUNDED_RECOMMENDATION | 无依据推荐商品或方向 |
| BD_HUMAN_GATE_BYPASSED | 未经人工选择进入 Creative |

## B.6.3 Creative

| 标签 | 含义 |
|---|---|
| CR_DECISION_DRIFT | 创意偏离已选商业方向 |
| CR_PERSONA_DRIFT | 人设在资产间漂移 |
| CR_PLATFORM_MISMATCH | 不符合视频号表达逻辑 |
| CR_GENERIC_COPY_ONLY | 只有通用文案，没有生产方案 |
| CR_PACKAGE_INCOMPLETE | 缺少必需交付物 |
| CR_NOT_PRODUCIBLE | 制作人员无法据此执行 |
| CR_CROSS_ARTIFACT_CONFLICT | Script、Storyboard、Voice 等冲突 |
| CR_VISUAL_FABRICATION | 虚构视觉属性 |
| CR_VISUAL_CONFIDENCE_OVERSTATED | 视觉不确定性被隐藏 |

## B.6.4 System 与验收过程

| 标签 | 含义 |
|---|---|
| SYS_FACT_BOUNDARY_BROKEN | 企业事实边界被突破 |
| SYS_RULE_VIOLATION | 输出违反硬规则 |
| SYS_SCHEMA_INVALID | 输出不符合 Schema |
| SYS_FAILURE_UNHANDLED | 超时或格式失败未安全处理 |
| SYS_CROSS_BRAND_LEAK | 引用其他品牌数据 |
| SYS_LINEAGE_BROKEN | 版本或父引用不可追溯 |
| SYS_REWORK_SCOPE_EXPANDED | 局部修改不必要扩大 |
| SYS_REWORK_LIMIT_BYPASSED | 超过返工上限仍自动运行 |
| SYS_UNAPPROVED_MEMORY_USED | 使用未经批准的 BrandMemory |
| EVAL_CONDITION_MISMATCH | A/B 条件不一致 |
| EVAL_BLINDING_BROKEN | 裁判提交前知道来源 |
| EVAL_EVIDENCE_INCOMPLETE | 原始结果、评审或修改证据缺失 |

以下失败一经出现，自动阻断相应里程碑，不能由其他案例抵消：

- INT_GOAL_ASSUMED；
- BD_FACT_FABRICATION；
- BD_HUMAN_GATE_BYPASSED；
- CR_DECISION_DRIFT；
- CR_PACKAGE_INCOMPLETE；
- SYS_RULE_VIOLATION；
- SYS_CROSS_BRAND_LEAK；
- SYS_UNAPPROVED_MEMORY_USED；
- EVAL_CONDITION_MISMATCH；
- EVAL_BLINDING_BROKEN。

---

# B.7 需求与案例映射

| 需求 | 主要诊断或检查 |
|---|---|
| INT-01 | INT-D01 |
| INT-02 | INT-D02 |
| INT-03 | INT-D03 |
| INT-04 | PRE-01-I、INT-D01 至 INT-D03 |
| INT-05 | INT-D01 至 INT-D03 |
| BD-01 | BD-D01 |
| BD-02 | PRE-01-B、BD-D01 的两候选降级分支 |
| BD-03 | BD-D01、BD-D03 |
| BD-04 | PRE-02-B、BD-D02 |
| BD-05 | BD-D01、BD-D02 |
| BD-06 | BD-D01、BD-D03 |
| BD-07 | BD-D03 |
| BD-08 | BD-D01、PRE-07-B、E2E-01 至 E2E-03 |
| CR-01 | CR-D01、CR-D02、E2E-01 至 E2E-03 |
| CR-02 | PRE-01-C、CR-D03 |
| CR-03 | CR-D01、CR-D03 |
| CR-04 | CR-D02 |
| CR-05 | CR-D03 |
| CR-06 | PRE-03-V、CR-D04 |
| CR-07 | PRE-02-C、CR-D04 |
| SYS-01 | PRE-07-I、PRE-07-B、PRE-07-C |
| SYS-02 | PRE-07-I、INT-D03、全部 E2E |
| SYS-03 | PRE-02-B、PRE-02-C、BD-D01、CR-D04 |
| SYS-04 | PRE-07-I、PRE-07-B、PRE-07-C、CR-D03、SYS-D01 |
| SYS-05 | PRE-07-B、PRE-07-C、SYS-D01 |
| SYS-06 | PRE-07-C、SYS-D01 |
| SYS-07 | PRE-01-I、PRE-01-B、PRE-01-C、PRE-03-M、PRE-03-V |
| SYS-08 | PRE-04、PRE-05 |
| SYS-09 | PRE-06、全部 E2E |
| SYS-10 | SYS-D01 |

每条核心需求至少有一个明确验收映射。增加实现字段不自动增加核心能力；改变能力语义时必须同步修改主 PRD、本表和相关案例。

---

# B.8 里程碑阻断规则

## Gate IA-0｜验收基线冻结

必须具备：

- 主 PRD、附录 A、本合同版本互相引用；
- 30 条核心需求编号一致；
- 锁定案例和 Case Manifest 已批准；
- 两阶段共同交互合同、输出合同和基线 Prompt 已冻结；
- 模型条件已确定；
- 裁判与匿名流程已确定；
- 没有依据已看到的结果反向修改通过条件。

IA-0 只表示验收条件可以执行，不表示能力已经成立。

## Gate IA-1｜Intent 能力成立

必须满足：

- PRE-01-I、PRE-03-M、PRE-04、PRE-05、PRE-06、PRE-07-I 通过；
- INT-D01、INT-D02、INT-D03 均为 PASS；
- 无未关闭的目标擅断、事实虚构或阻断项绕过；
- 输入、输出、Trace 与人工结论可追溯。

对应主 PRD M1。

## Gate IA-2｜Business Decision 能力成立

必须满足：

- IA-1 保持 PASS；
- PRE-01-B、PRE-02-B、PRE-07-B 通过；
- BD-D01、BD-D02、BD-D03 均为 PASS；
- Founder / Reviewer 能在候选中做出真实选择，并形成一致的 ReviewRecord 与 DecisionSelection；
- 候选具有实质差异；
- 无事实虚构、硬规则违反、Trace 混写或人工门绕过。

对应主 PRD M2。

## Gate IA-3｜Creative 与受控返工成立

必须满足：

- IA-1、IA-2 保持 PASS，PRE-01-I、PRE-01-B、PRE-01-C、PRE-02-B、PRE-02-C、PRE-03-M、PRE-03-V、PRE-04 至 PRE-06、PRE-07-I、PRE-07-B、PRE-07-C 均保持通过；
- CR-D01 至 CR-D04、SYS-D01 均为 PASS；
- 九部分制作包完整，批准后 Markdown 导出与同一权威版本一致；
- Founder 以制作使用者视角确认至少一个完整包可以执行（v0.2 修订，同 B.5.2）；
- 方向、Persona、事实、视觉证据和资产引用一致；
- 返工范围、版本和停止条件有效；
- 无未批准 BrandMemory。

对应主 PRD M3。

## Gate IA-4｜端到端显著优于基线

必须满足：

- IA-0、IA-1、IA-2、IA-3 均为 PASS，且无未关闭的既往阻断失败；
- E2E-01、E2E-02、E2E-03 均按同条件匿名流程完成；
- 三个场景逐案满足“明显优于”定义；
- 商业与制作裁判都选择笛语；
- 选择理由指向商业判断或制作价值；
- 所需修改不高于 LOCAL；
- 无阻断性失败；
- 成本、延迟与模型条件记录完整；
- Founder 明确签署 MVP 裁决。

任一锁定场景为 FAIL、INCONCLUSIVE、NEITHER 或 NO_MATERIAL_DIFFERENCE 时，IA-4 不通过。

对应主 PRD M4。

## B.8.1 阻断解除

验收失败只能通过以下方式解除：

1. 修复后按相同条件重测；
2. 案例本身无效，升级合同和 Manifest 版本后重新运行；
3. Founder 明确缩小 MVP 能力范围，并同步修改主 PRD、附录 A 和本合同。

不得通过口头豁免、删除失败记录、增加大量简单用例或改变口径把 FAIL 改成 PASS。

---

# B.9 变更与回归

以下变化必须重跑受影响的模块诊断和端到端案例：

- 企业事实 Schema；
- 输出合同；
- 硬规则；
- 任一模块模板或编排；
- 基础模型或版本；
- Context Contract；
- BrandMemory 启用状态或内容；
- Rework Controller；
- Artifact Reference。

只改变无业务语义的展示样式时可以不重跑，但必须证明底层输入、输出和版本引用未变化。

模型供应商使用漂移别名时，正式验收必须记录运行时间窗口和可获得的实际版本信息。无法证明条件一致时标记 EVAL_CONDITION_MISMATCH。

---

# B.10 最小验收证据

每个正式案例只要求保存一份最小 AcceptanceEvidenceRecord 及其引用的原始输入输出，不建设复杂评测平台或执行包森林。

~~~yaml
AcceptanceEvidenceRecord:
  evidence_id: string
  case_manifest_ref: string
  case_id: string
  run_ids: string[]
  raw_diyu_output_ref: string
  raw_baseline_output_ref: string | null
  anonymized_output_refs: string[]
  commercial_review_ref: string | null
  production_review_ref: string | null
  commercial_choice: X | Y | NEITHER | NO_MATERIAL_DIFFERENCE | null
  commercial_choice_reason: string | null
  production_choice: X | Y | NEITHER | NO_MATERIAL_DIFFERENCE | null
  production_choice_reason: string | null
  required_edit_targets: string[]
  choices_frozen_at: datetime | null
  blind_label_map_ref: string | null
  decision_acceptance: SELECTED_AS_IS | SELECTED_WITH_LOCAL_EDIT | REJECTED | INCONCLUSIVE | null
  content_adoption: READY_TO_PRODUCE | LOCAL_EDIT_REQUIRED | STRATEGIC_REWORK_REQUIRED | UNUSABLE | INCONCLUSIVE | null
  edit_severity: NONE | LOCAL | MATERIAL | REBUILD | null
  failure_labels: string[]
  blocking_failures: string[]
  cost_and_latency_summary: string
  case_result: PASS | FAIL | INCONCLUSIVE
  approved_by: string
  approved_at: datetime
~~~

端到端案例中，commercial_choice、production_choice、choices_frozen_at 和 blind_label_map_ref 必填；blind_label_map 只能在 choices_frozen_at 后揭晓，并必须足以证明两类裁判实际选择的是哪一侧。模块诊断案例可将这些字段留空。证据中不得保存明文凭证。原始输入、输出和人工选择不得只保留摘要。

---

# B.11 本合同明确不建设

本合同不要求建设：

- 自动审美评分器；
- 综合智能分数；
- LLM Judge 发布系统；
- 大规模评测平台；
- 数百条低价值案例；
- 多租户 RLS；
- 企业 IAM；
- 完整审计平台；
- SLA 和灾备演练；
- 大规模并发压测；
- 自动 Prompt 或规则学习；
- 自动 BrandMemory 写入；
- 爆款预测。

这些能力不得成为验证三个智能模块的前置条件。

---

# B.12 最终验收裁决

MVP 不因“能够生成内容”而成立。

只有当受控证据表明：

1. Intent 能识别任务和真正缺失的信息；
2. Business Decision 能在企业事实与规则内形成有价值的取舍；
3. Creative 能把人工选定方向转成完整、统一、可制作的视频号交付包；
4. 在相同事实、模型和输出合同下，人工匿名选择笛语而不是通用 LLM；
5. 修改记录证明笛语减少了重新决策和重新制作；

才能对终极问题给出：

> **是，笛语在当前受控范围内明显优于直接使用通用大模型。**

否则，裁决必须保持：

> **尚未证明。**
