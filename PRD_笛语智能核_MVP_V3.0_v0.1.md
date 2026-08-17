# 笛语智能核 MVP V3.0 产品需求文档

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档编号 | DIYU-PRD-MVP-V3 |
| 版本 | v0.1 |
| 状态 | **EFFECTIVE（已批准生效）** |
| 批准 | Founder（Faye）2026-08-17 批准；生效基线 = 主 PRD v0.1 + 附录 A v0.2（当日补情绪字段修订）+ 附录 B v0.4（当日两次标签补登修订，末次为 M0 收口修复批次补登 EVAL_BLINDING_PROCEDURE_INVALID）三份一并生效，历次当日修订均经 Founder 批准 |
| 日期 | 2026-08-16 |
| 产品范围 | 服装品牌微信视频号内容商业决策与制作交付 |
| 决策责任人 | Founder |
| 本版目的 | 把已冻结的产品方向转化为可实现、可审核、可阻断验收的 MVP 合同 |

### 受控文档关系

本项目只维护以下一份主 PRD 和两份受控附录：

1. 本文档：定义产品使命、能力、运行边界、用户旅程与里程碑。
2. A_模块接口与核心数据字典.md：定义当前 MVP 必需的对象、字段、枚举、Schema 与不确定性表达。
3. B_三个核心模块智能验收合同.md：定义如何证明能力成立，并对相应里程碑拥有阻断权。

三份文档必须使用同一版本基线。若三者出现冲突：

- 产品能力与范围以主 PRD 为准；
- 字段和接口以附录 A 为准；
- 验收方法与退出阻断以附录 B 为准；
- 任何跨文档冲突均不得由执行人员自行解释，必须阻断并同步修订三份文档。

### 来源与边界

本文档依据以下材料形成：

- 笛语智能核.md 中的 MVP V3.0 冻结裁决；
- 三个核心模块测试矩阵建议.md 中的智能能力测试思想；
- Founder 对执行范围、角色、交互、工程保障、验收方法和文档结构的纠正裁决。

本文档不会把 PRD 编写、测试通过或技术组件存在等同于业务交付完成。MVP 是否成立，最终取决于第 1 章的终极验证问题能否获得肯定答案。

---

# 1. 产品使命与终极验证问题

## 1.1 产品使命

笛语 MVP 的使命不是证明 AI 能生成内容，而是让通用大模型在服装品牌的真实企业事实、商业目标和品牌约束下，稳定形成更值得执行的商业判断与视频号内容制作交付。

## 1.2 终极验证问题

> **在相同企业事实、相同基础模型和相同输出要求下，笛语的商业决策与视频号内容制作交付包，是否明显优于直接使用 ChatGPT／Claude？**

这是项目存在的理由，不是普通指标之一。任何功能、工程组件、测试数量或文档完整度，如果不能帮助回答这一问题，都不构成 MVP 的核心进展。

## 1.3 产品定义

> 笛语 MVP 是一个面向服装品牌的视频号内容商业决策与生产系统。它通过 Intent Intelligence Module、Business Decision Engine 和 Creative Content Engine，把企业输入编译为可解释、可审核、可修改、可制作的视频号内容制作交付包。

系统不替代 GPT、Claude 或 VLM，而是在其外部增加：

- 企业事实约束；
- 任务与上下文合同；
- 商业候选与取舍；
- 视频号内容生产结构；
- 事实、规则、假设和模型判断追踪；
- 人工选择、审核与有限返工；
- 经批准的品牌偏好沉淀。

## 1.4 商业假设

直接使用通用 LLM 的主要不足不是文字生成能力，而是：

- 容易在商业目标不清时直接给答案；
- 难以稳定区分事实、假设与模型判断；
- 容易把商业冲突简化成单一建议；
- 不能稳定承接品牌人设、禁用表达和商品事实；
- 产出常停留在“可读文案”，而非摄影与内容团队可直接执行的制作包；
- 人工修改无法形成可控、可追踪的品牌偏好。

笛语的商业假设是：通过领域智能模块、企业事实层和受控人工决策，可以在不自建基础模型、不先建设大型经验库的前提下，获得显著的商业判断和生产可用性增量。

## 1.5 唯一平台

MVP 只服务微信视频号服装内容生产。

本阶段不支持：

- 抖音；
- 小红书；
- 公众号；
- 多平台自动适配。

平台数量不是本阶段的验证目标。MVP 只验证商业判断、品牌人格、内容叙事与生产交付能否形成闭环。

---

# 2. 目标用户、用户价值与非目标

## 2.1 目标客户

目标客户是需要持续生产视频号内容、拥有基本品牌与商品资料，并愿意由负责人参与商业方向审核的服装品牌。

首批试点品牌、商品范围和具体业务目标由 Founder 在 M0 里程碑冻结，不在本版中假定。

## 2.2 两类系统角色

### Brand Operator

负责：

- 初始化或补充品牌、商品、受众、账号与人设资料；
- 创建内容任务；
- 回答关键上下文问题；
- 查看系统产出；
- 发起内容包导出。

### Founder / Reviewer

负责：

- 判断和选定商业候选；
- 审核内容包是否符合品牌和商业方向；
- 指定返工类型与原因；
- 确认完成；
- 批准可进入 Brand Memory 的品牌偏好。

摄影师、剪辑师和内容执行人员是交付包使用者和可制作性评价者，但不在 MVP 中建设为系统账户角色。

## 2.3 用户价值

### 对品牌负责人

- 商业方向不再被直接隐藏在一份文案中；
- 可以看到候选、取舍、风险和事实依据；
- 可以在生成内容前先选方向；
- 品牌禁区与商品事实可以被持续约束。

### 对内容生产人员

- 获得完整制作包，而非一段散文式文案；
- 减少脚本、分镜、口播、商品露出与评论运营之间的二次翻译；
- 降低结构性重写和跨角色沟通成本。

### 对企业

- 同一品牌事实可以在不同任务中复用；
- 人工选择与修改有来源、版本和理由；
- 只有明确批准的偏好才进入品牌记忆。

## 2.4 MVP 目标

MVP 必须验证：

1. 系统能理解真实商业任务，而非只做表层文本分类。
2. 系统能在事实和规则约束下形成有实质差异的商业候选，并说明取舍。
3. 系统能把选定的商业方向忠实转成视频号制作交付包。
4. 真实审核者认为笛语结果比同条件的通用 LLM 结果更值得拿去制作。
5. 系统在失败、资料不足和返工时保持可控，不通过虚构填补缺口。

## 2.5 明确非目标

MVP 不建设：

- 多平台 Adapter；
- 自动视频生成或生图系统；
- 数字人、ControlNet；
- 基础模型微调；
- 自动爆款预测或商业预测模型；
- 自动学习和自动改写 Prompt、规则或权重；
- 钩子、卖点、场景、人群和成品素材经验大库；
- 公共服装知识库；
- 复杂 DAG 和无限 Agent 循环；
- 管理员后台、品牌控制台或生产仪表盘；
- 完整多租户 RLS、企业级 IAM 和复杂审计系统；
- 全面 SLA、灾备演练和大规模性能压测；
- Billing 或 Marketplace。

以上事项并非永不建设，而是不得成为智能核 MVP 验证的前置条件。

---

# 3. MVP 用户旅程与极简交互

## 3.1 端到端用户旅程

~~~text
品牌资料初始化
    ↓
创建视频号内容任务
    ↓
识别商业目标与关键上下文
    ↓
快速模式继续，或增强模式补充资料
    ↓
查看商业候选
    ↓
Founder / Reviewer 选定商业方向
    ↓
生成视频号内容制作交付包
    ↓
审核、局部修改或一次策略重做
    ↓
确认完成并导出
    ↓
经批准的偏好进入 Brand Memory
~~~

## 3.2 三个工作面

| 工作面 | 主要角色 | 最小能力 | 明确不建设 |
|---|---|---|---|
| 任务与资料输入 | Brand Operator | 品牌初始化、选择商品、输入任务、查看缺失上下文、选择快速或增强模式 | 完整品牌后台、复杂表单编排 |
| 商业候选选择 | Founder / Reviewer | 查看商业问题、候选策略、事实与风险、选定方向或要求补充资料 | 复杂决策驾驶舱、自动预测看板 |
| 内容包审核、修改与导出 | Founder / Reviewer、Brand Operator | 查看九部分内容包、按原因申请返工、确认完成、导出 | 生产排期、剪辑协作、完整 DAM |

三个工作面可以由一个极简 Web Host 承载，不要求先建设完整信息架构。

## 3.3 关键旅程规则

1. 用户目标不明确时，系统不得擅自确定唯一商业目标。
2. 关键事实缺失时，系统必须明确缺失项；快速模式只能在非阻断信息缺失时继续。
3. Business Decision 必须先于 Creative Content。
4. Creative Content 必须引用已选商业候选，不得静默改变方向。
5. 所有制作包都必须经过 Founder / Reviewer 审核后才能进入 COMPLETED。
6. 修改必须关联原因和目标字段，不能以“感觉不好”作为唯一返工合同。

## 3.4 Runtime 状态

MVP 只使用以下七个任务状态：

| 状态 | 含义 |
|---|---|
| DRAFT | 任务正在创建、上下文正在整理，或目标变更后等待重新执行 |
| NEEDS_INPUT | 缺少阻断性事实或需要用户明确商业目标 |
| DECISION_READY | 商业候选已生成，等待 Founder / Reviewer 选择 |
| CREATIVE_READY | 已选方向对应的内容包生成成功 |
| REVIEW_REQUIRED | 内容包或返工版本等待人工审核 |
| COMPLETED | 人工确认完成，可导出 |
| FAILED | 当前执行在现有输入或运行条件下无法自动恢复，任务停止并保留失败原因；修正后可由人工重启 |

允许的主状态迁移：

~~~text
DRAFT → NEEDS_INPUT | DECISION_READY | FAILED
NEEDS_INPUT → DRAFT | FAILED
DECISION_READY → DRAFT | CREATIVE_READY | FAILED
CREATIVE_READY → REVIEW_REQUIRED | FAILED
REVIEW_REQUIRED → CREATIVE_READY | DRAFT | COMPLETED | FAILED
FAILED → DRAFT
~~~

关键事件必须沿上述状态迁移：Intent 发现阻断项时进入 NEEDS_INPUT；资料补齐后回到 DRAFT；合法候选生成后进入 DECISION_READY；人工选定候选且 Creative 生成成功后进入 CREATIVE_READY；完整性和硬规则通过后进入 REVIEW_REQUIRED；批准后进入 COMPLETED。拒绝全部候选、策略重做或商业目标变化都先回到 DRAFT，再按既有链路重新执行。FAILED 只能在修正输入、配置或运行条件后由人工重启到 DRAFT。

模型执行中的短暂“运行中”不新增产品状态，由 Run 记录承担。超过返工上限时不发生状态迁移：任务保持 REVIEW_REQUIRED，并设置 human_decision_required，不增加新的状态或跨层 DAG。详细事件—状态合同见附录 A。

---

# 4. 最小系统架构与 Build / Borrow

## 4.1 最小架构

~~~text
三工作面极简 Host
        ↓
薄 Runtime
Task / Context Snapshot / Run / Artifact / Review / Revision
        ↓
Diyu Intelligence Kernel
Intent → Business Decision → Creative Content
        ↓
企业语义事实层
Brand / Product / Audience / Persona / Video Account Facts
        ↓
LLM / VLM Adapter
GPT / Claude / 可替换视觉模型
~~~

横向最小能力：

- Context Contract；
- Rule Engine；
- Visual Understanding；
- Fact / Rule / Assumption / Judgment Trace；
- Artifact Reference；
- Review Delta；
- Rework Controller。

## 4.2 极简 Host

Host 只负责：

- 呈现三个工作面；
- 接收结构化输入和文件；
- 展示候选与交付包；
- 收集人工选择、审核和修改原因；
- 导出最终内容包。

Host 不承担领域推理，不把业务规则散落在页面代码中。

## 4.3 薄 Runtime

Runtime 只负责：

- 七状态任务流转；
- Context Snapshot 冻结；
- 三模块顺序调用；
- 模型调用、超时和结构化解析；
- Artifact 版本与父引用；
- Review、Revision 与最小运行记录。

Runtime 不建设通用工作流平台、复杂 DAG 或无限循环 Agent。

## 4.4 Build / Borrow 裁决

| 能力 | 裁决 |
|---|---|
| 三个领域智能模块及其合同 | 自建 |
| 企业事实模型与上下文合同 | 自建 |
| 商业候选、取舍与 Trace | 自建 |
| 制作交付包结构 | 自建 |
| 智能验收合同与证据记录 | 项目治理产物；以轻量文件和记录执行，不进入产品 Runtime，不建设验收平台 |
| Review Delta、Artifact Reference、Rework 规则 | 自建 |
| GPT、Claude、VLM 推理能力 | 借用 |
| 通用模型 API、文件解析、对象存储、数据库 | 借用 |
| Dify 或云 Agent 平台 | 可借用，但不能成为产品合同的唯一实现 |
| 通用 UI 框架与部署平台 | 借用 |

底层组件可以替换，但模块输入输出、Trace、审核和验收语义不得随供应商变化。

## 4.5 最低运行要求

首版只要求：

- 输入输出 Schema 校验；
- 硬规则校验；
- 模型超时、不可用和格式失败处理；
- 单品牌工作区数据隔离；
- 基础凭证保护和文件访问控制；
- 每次 Run 记录模型、版本、延迟、Token 与估算成本；
- 错误可定位到具体模块和 Run。

本阶段不以企业级基础设施完备度作为智能能力验证前置。

---

# 5. 三个核心模块合同

## 5.1 通用合同原则

每个模块必须明确：

- 能力目标；
- 输入；
- 输出；
- 事实来源；
- 硬规则边界；
- 假设与模型判断；
- 异常与降级；
- 人工审核点；
- 对应智能验收案例。

“合同完整”是指足以表达当前 MVP 用户旅程和验收案例，不需要靠临时自由文本补洞；不要求一次性枚举服装行业全部任务和异常。

## 5.2 Intent Intelligence Module

### 能力目标

把用户自然语言需求和企业上下文编译为 IntentExecutionPlan，明确真实商业目标、必需上下文、缺失项、置信度和下一步。

### 输入

- 用户任务；
- 当前 Brand、Product、Audience、Persona、Video Account Facts；
- 用户选择的快速或增强模式；
- 当前平台固定为 WECHAT_VIDEO。

### 输出

- artifact；
- task_type 与 platform；
- goal_resolution、business_goal 与 goal_candidates；
- intent_summary 与 target_audience_refs；
- required_context 与 missing_context；
- assumptions 与 confidence；
- next_action 与 trace_bundle。

详细 Schema 见附录 A。

### 核心能力需求

| ID | 可独立验收的能力 |
|---|---|
| INT-01 | 目标不明确时不得擅自选定唯一目标；必须给出候选目标或提出澄清请求，并在人工明确前进入 NEEDS_INPUT。 |
| INT-02 | 关键事实不足时必须区分快速模式和增强模式；阻断性事实缺失时两种模式都进入 NEEDS_INPUT。 |
| INT-03 | 同一商品改变商业目标后，IntentExecutionPlan 必须相应变化，同时保持未改变的商品事实不变。 |
| INT-04 | 每次输出必须符合 IntentExecutionPlan Schema，并明确 missing_context、assumptions、confidence 与 next_action。 |
| INT-05 | Intent 不得虚构品牌、商品、受众或账号事实；所有事实性依据必须能够引用来源。 |

### 人工审核点

- 系统不能从现有事实区分商业目标时，由 Brand Operator 补充；
- 用户目标发生实质变化时，任务回到 DRAFT 并重新执行 Intent；
- Founder / Reviewer 可否决 Intent 解释，但必须记录变更后的目标。

## 5.3 Business Decision Engine

### 能力目标

基于企业事实、商业目标和约束，生成有实质差异的商业候选，说明冲突、取舍、事实、规则、假设、风险与模型判断。

### 输入

- 已确认的 IntentExecutionPlan；
- 固定的 Context Snapshot；
- 商品、品牌、受众、Persona 与账号事实；
- 硬规则和生产约束。

### 输出

- artifact；
- business_problem 与 recognized_conflicts；
- candidate_options；每个候选内含 product_roles、适配判断、风险与取舍；
- comparative_tradeoffs；
- system_recommendation，可为空；
- human_selection_required；
- candidate_count_status 与 candidate_count_explanation；
- blocked_candidate_diagnostics；
- confidence 与 trace_bundle。

目标输出三个商业候选；在事实或约束不足以支持三个实质差异候选时，最少输出两个，并以结构化状态和原因说明为什么不能形成第三个候选。不得用措辞变化冒充不同策略。

### 核心能力需求

| ID | 可独立验收的能力 |
|---|---|
| BD-01 | 必须识别并明确表达当前任务的核心商业问题与主要冲突。 |
| BD-02 | 必须生成目标三个、最低两个有实质差异的商业候选，差异体现在目标路径、商品角色、叙事或风险取舍，而非措辞。 |
| BD-03 | 必须区分 Fact、Rule、Assumption 与 Model Judgment，模型判断不得伪装成企业事实。 |
| BD-04 | 必须遵守商品池、库存、价格、品牌限制等事实边界，不得为满足要求虚构商品或条件。 |
| BD-05 | 每个候选必须说明为什么选择该路径、为什么不优先选择主要替代路径。 |
| BD-06 | 候选必须覆盖品牌适配、受众适配、商业目标、制作可行性和风险，不要求建立预测型 Ranker。 |
| BD-07 | 面对非常规商品或表达，不得只做机械保守判断；必须结合面积、层次、场景和目标给出有条件结论。 |
| BD-08 | Creative Content 生成前必须由 Founder / Reviewer 明确选定商业候选；系统推荐不能替代人工选择。 |

### 人工审核点

Founder / Reviewer 必须能够：

- 查看候选差异和依据；
- 选择一个候选；
- 要求补充事实；
- 变更目标并返回 DRAFT；
- 拒绝全部候选并记录原因。

## 5.4 Creative Content Engine

### 能力目标

把已选商业候选转化为符合视频号人物、关系和信任传播逻辑，且内容团队可以执行的视频号内容制作交付包。

### 输入

- DecisionSelection 精确版本；
- BusinessDecisionBundle 精确版本与已选 candidate_id；
- Persona、品牌语气、账号关系和禁用表达；
- Product Facts 与 VisualProfile；
- 制作约束。

### 输出

- artifact；
- decision_selection_ref、decision_bundle_ref 与 selected_candidate_id；
- context_snapshot_ref；
- creative_plan；
- 九项 package_artifact_refs；
- production_risks 与 validation；
- confidence 与 trace_bundle。

### 核心能力需求

| ID | 可独立验收的能力 |
|---|---|
| CR-01 | CreativePlan 和制作包必须忠实承接已选商业候选，不得静默替换商业目标、商品角色或主要策略。 |
| CR-02 | 必须输出第 7 章定义的九部分完整制作包；缺失必需部分不得进入 REVIEW_REQUIRED；批准后的同一权威版本必须能完整导出为 Markdown。 |
| CR-03 | Persona、口播、故事角度、画面建议和评论回应必须保持同一身份、语气和关系模式。 |
| CR-04 | 内容必须符合视频号的人物、关系和信任建立逻辑，不能只是小红书笔记或商品卖点列表换壳。 |
| CR-05 | 脚本和 Storyboard 必须让摄影或内容执行人员知道拍什么、为什么拍、商品展示什么及注意事项。 |
| CR-06 | 有商品图片时必须形成 VisualProfile；无法可靠识别的视觉属性必须标记不确定，不得猜测。 |
| CR-07 | 内容必须遵守品牌禁用表达、商品事实和硬规则，创意表达不得覆盖事实边界。 |

### 人工审核点

Founder / Reviewer 审核：

- 商业方向是否被忠实承接；
- 品牌、人设与账号表达是否一致；
- 制作包是否值得进入实际制作；
- 修改属于局部返工还是策略重做。

---

# 6. 企业语义事实层与品牌初始化

## 6.1 架构硬原则：先事实，后经验

MVP Day 1 建设：

- Brand Facts；
- Product Facts；
- Audience Facts；
- Persona Facts；
- Video Account Facts。

MVP Day 1 不先建设：

- 钩子经验大库；
- 卖点经验大库；
- 场景经验大库；
- 人群经验大库；
- 成品素材经验大库。

初始创意来源固定为：

~~~text
企业事实
+
任务合同
+
通用大模型的内化能力
~~~

运行后只记录：

- 人工选择；
- 人工修改；
- 品牌明确偏好。

只有经过 Founder / Reviewer 批准的内容才能形成 Brand Memory。系统不得自动修改 Prompt、规则或权重。

## 6.2 五类事实

| 事实对象 | 当前 MVP 的目的 |
|---|---|
| Brand Facts | 约束定位、价值观、语气、目标客户、禁用表达和商业限制 |
| Product Facts | 约束 SKU、品类、价格、库存、材质、版型、颜色、卖点、图片和生命周期 |
| Audience Facts | 表达目标人群、痛点、购买理由、异议和已知边界 |
| Persona Facts | 定义谁来说、声音、信念、关系和禁止表达方式 |
| Video Account Facts | 固定平台、账号内容风格、受众关系和已知平台约束 |

每条事实必须区分：

- 用户明确提供；
- 文件抽取；
- 系统推断；
- 未验证。

系统推断不能直接升级为企业事实。

## 6.3 品牌初始化

MVP 支持两种初始化方式：

1. 对话式：Brand Operator 按关键问题补充资料；
2. 资料抽取式：从品牌和商品资料中提取候选事实，再由用户确认。

抽取结果必须保留来源和确认状态。

## 6.4 快速模式与增强模式

### 快速模式

- 只要求当前任务不可缺少的阻断性事实；
- 非阻断信息不足时允许继续；
- 必须列出 missing_context 和 assumptions；
- 必须降低 confidence；
- 不得通过虚构补齐。

### 增强模式

- 主动请求影响商业判断或人设一致性的关键资料；
- 缺失时进入 NEEDS_INPUT；
- 资料补充后生成新的 Context Snapshot。

## 6.5 Context Snapshot

每次 Intent、Business Decision 和 Creative 执行必须绑定不可变的 Context Snapshot。用户后续修改事实时必须产生新版本，不能静默改变已经生成的 Artifact。

| ID | 可独立验收的能力 |
|---|---|
| SYS-02 | 每次模块执行必须绑定包含品牌、商品、受众、Persona 与账号事实版本的 Context Snapshot；事实变化必须形成新版本。 |

---

# 7. 视频号内容制作交付包

## 7.1 最终购买资产

视频号内容制作交付包是用户最终购买和使用的核心资产，不以单段文案作为完成结果。

## 7.2 九部分必需结构

| 部分 | 最小内容 | 人工可用标准 |
|---|---|---|
| Content Brief | 内容目标、目标受众、核心传播命题 | 审核者能一句话判断“为什么做、对谁说、说什么” |
| Creative Strategy | 主题、情绪路径、卖点排序、内容结构 | 能看出如何承接已选商业策略 |
| Persona Card | 谁来说、怎么说、不能说什么 | 口播、画面和评论回复能保持一致人格 |
| Video Script | 时间段、画面、口播、商品、情绪 | 可用于拍摄准备，而非纯文案 |
| Storyboard | 镜头目的、场景、人物、商品重点、注意事项 | 摄影人员知道每个镜头的执行目的 |
| Voice Package | 完整口播、停顿、强调、语速和情绪 | 出镜者可据此录制 |
| Audio Direction | 情绪、节奏和使用阶段 | 能指导选乐，不要求系统生成音乐 |
| Product Placement | 出现时点、出现原因、展示重点 | 商品露出服务内容和商业目标 |
| Comment Operation Package | 置顶评论、常见问题、官方回应 | 发布后可以直接用于基础互动 |

详细字段见附录 A。

## 7.3 完整性与可用性

制作包进入 REVIEW_REQUIRED 前必须同时满足：

1. 九个顶层部分全部存在；
2. 所有关键商品事实与 Context Snapshot 一致；
3. 明确引用已选商业候选；
4. Persona、口播、画面和评论回应一致；
5. Storyboard 含可执行镜头信息；
6. 假设和不确定性被显式标记；
7. 硬规则校验通过。

MVP 以结构化对象作为内部权威版本，并至少支持人类可读的 Markdown 导出。导出必须绑定已经批准的 CreativeContentBundle、九项资产及 Review 版本；不得导出旧版本、缺失部分或在导出时重写内容。导出失败必须显式记录，不能把不完整文件标记为成功。是否增加 DOCX 或 PDF 为待决事项，不影响内部合同。

---

# 8. 规则、审核、返工与最小版本引用

## 8.1 Rule Engine

Rule Engine 只承载明确、可验证的硬规则，例如：

- 不得虚构不存在的商品；
- 品牌禁止低价叫卖；
- 不得使用未确认的材质或功效描述；
- 制作包必须包含九个必需部分。

软性偏好不能伪装成硬规则，应作为 Model Judgment 或经批准的 Brand Memory 处理。

| ID | 可独立验收的能力 |
|---|---|
| SYS-03 | 硬规则必须在相关模块输出后执行确定性校验；违反硬规则的 Artifact 不得进入下一人工审核节点。 |

## 8.2 Trace 分类

每个关键商业判断必须归入以下一种类型：

- FACT：来自 Context Snapshot 的事实；
- RULE：已确认的硬规则；
- ASSUMPTION：为继续任务而显式声明的假设；
- MODEL_JUDGMENT：模型基于事实与规则形成的判断。

四类信息不得混写成无法区分的解释段落。

## 8.3 Artifact Reference

MVP 不建设复杂 DAG，只记录：

- artifact_id；
- type；
- version；
- source_run_id；
- context_snapshot_id；
- parent_references；
- review_status。

| ID | 可独立验收的能力 |
|---|---|
| SYS-04 | 当前里程碑已经生成的 Intent、Decision、Creative 和 Package Artifact 必须具有版本、来源 Run、Context Snapshot 与父引用，能够还原当前内容来自哪次人工选择和哪个商业决策版本。 |

## 8.4 Review Delta

人工审核必须记录：

- 审核的 Artifact 与版本；
- 审核决定；
- 修改原因类别；
- 目标字段或部分；
- 人工说明；
- 新旧版本引用。

允许的主要原因：

- FACT_ERROR；
- RULE_CONFLICT；
- PRODUCTION_ISSUE；
- BRAND_MISMATCH；
- USER_OBJECTIVE_CHANGED。

| ID | 可独立验收的能力 |
|---|---|
| SYS-05 | 每次候选选择必须形成成对且关联一致的 DecisionSelection 与 ReviewRecord；每次批准或返工必须形成 ReviewRecord；返工必须指向原因和目标范围，不能只保存无结构评价。 |

## 8.5 Rework Controller

MVP 限制：

- 局部修改最多 2 次；
- 策略重做最多 1 次；
- 超过上限后不得自动继续生成；
- 任务保持 REVIEW_REQUIRED，并设置 human_decision_required；
- 只有 Founder / Reviewer 可以决定完成、重新定义目标或人工终止。人工终止必须形成 TERMINATE ReviewRecord 与 MANUAL_TERMINATION FailureRecord，并沿 REVIEW_REQUIRED → FAILED 执行；不增加第八状态。

局部返工生成受影响资产的新版本，并沿 `REVIEW_REQUIRED → CREATIVE_READY → REVIEW_REQUIRED` 返回审核。策略重做或拒绝全部候选必须先进入 DRAFT，再复用或更新 Intent 重新运行 Business Decision，合法候选形成后进入 DECISION_READY；商业目标变化必须重新运行 Intent。

| ID | 可独立验收的能力 |
|---|---|
| SYS-06 | 系统必须区分局部返工与策略重做，执行次数上限，并在超限时停止自动生成。 |

## 8.6 Runtime、失败与最小运行治理

| ID | 可独立验收的能力 |
|---|---|
| SYS-01 | 任务只能使用第 3.4 节七个状态，并遵守允许的状态迁移。 |
| SYS-07 | 模型超时、不可用、Schema 解析失败和视觉输入不可读必须产生明确失败码；不得把格式失败当作有效内容继续。 |
| SYS-08 | 所有 Task、Snapshot、Run 和 Artifact 必须绑定同一 brand_id；系统不得读取或引用其他品牌工作区的数据，凭证和上传文件必须采用基础访问保护。 |
| SYS-09 | 每个 Run 必须记录模型供应方、模型版本、调用时间、延迟、Token 用量和估算成本。 |
| SYS-10 | Brand Memory 只能来自明确的人工选择或修改证据并经 Founder / Reviewer 批准；不得自动改变 Prompt、规则或权重。 |

---

# 9. 智能验收与 ChatGPT／Claude 基线对比

## 9.1 受控验收合同

附录 B 是本章的规范性执行合同，对相应里程碑拥有阻断权。它不是普通 QA 附录，也不能被主 PRD 中的功能描述替代。

任何核心能力需求只有在以下两项同时成立时才可标记为已验收：

1. 对应产品行为满足主 PRD 与附录 A；
2. 对应诊断或端到端案例通过附录 B 的人工验收和禁止结果检查。

## 9.2 三类证据

### 模块诊断案例

用于判断 Intent、Business Decision 和 Creative 各自是否具备目标能力，并定位错误发生在哪一层。

### 端到端匿名 A/B

在相同企业事实、相同基础模型、相同模型版本和参数、相同输出要求下，对比：

- A：直接调用 ChatGPT／Claude 的基线结果；
- B：经过笛语三模块与事实、规则、审核合同的结果。

两侧使用附录 B 冻结的共同两阶段交互合同：先输出同结构的商业候选与取舍，由不知来源的 Founder / Reviewer 分别选定候选；再基于各自被选候选输出同结构的九部分制作包。直接基线每阶段只进行一次受控直接调用，不接收笛语中间产物或隐藏迭代。最终比较包必须去除来源标识并随机顺序呈现。

### 人工选择和修改记录

记录审核者：

- 更愿意把哪份结果拿去制作；
- 为什么；
- 需要哪些修改；
- 修改属于何种严重度；
- 是否存在禁止结果。

## 9.3 唯一核心裁判问题

> 在不知道输出来源的情况下，基于当前品牌与商品事实，哪一份结果更值得实际拿去制作？

允许结论：

- 选择笛语输出；
- 选择通用 LLM 输出；
- 两者相当；
- 两者都不可用。

选择必须附理由和修改记录，不能只给综合分。

## 9.4 成功观察指标

| 指标 | 定义 |
|---|---|
| Decision Acceptance | Founder / Reviewer 是否接受某一商业候选进入 Creative，而不需要推翻整个商业问题 |
| Content Adoption | 内容包是否愿意进入真实或受控模拟制作流程 |
| Edit Severity | 人工修改是无修改、局部润色、局部事实或制作修正、结构性重写，还是策略推翻 |
| Failure Class | 失败发生在目标、事实、规则、候选差异、决策承接、人设、平台语法、制作性、包完整性或模型运行 |

这些指标用于形成证据，不合成为自动总分。

## 9.5 明确禁止的验收方式

不采用：

- 自动审美总分；
- 数百格机械测试矩阵；
- 用例数量作为完成度；
- 单一平均分掩盖事实虚构或硬规则违反；
- LLM Judge 单独决定发布；
- 在看到结果后修改基线、允许答案或退出门；
- 用 Schema 通过替代商业价值判断。

LLM Judge 如被使用，只能辅助聚类、格式检查或发现候选问题，不能独立放行里程碑。

## 9.6 里程碑阻断原则

以下任一情况存在时，相应里程碑不得退出：

- 虚构品牌、商品或受众关键事实；
- 违反硬规则；
- 读取或引用其他品牌数据；
- Intent 在目标不明时擅自确定唯一目标；
- 商业候选只是措辞变化；
- Creative 静默偏离已选商业方向；
- 制作包缺少必需部分或无法执行；
- A/B 基线条件不一致；
- 只依赖自动评分而无人工使用判断；
- 附录 B 中标记为阻断的案例尚未关闭。

---

# 10. 里程碑、退出门与待决事项

## 10.1 里程碑

### M0：合同基线冻结

交付：

- 主 PRD；
- 附录 A；
- 附录 B；
- 首批试点事实材料；
- 基础模型与 A/B 条件；
- 待决事项裁决记录。

退出门：

- 三份文档版本一致；
- OD-01 至 OD-04 已裁决；
- 模块合同覆盖已锁定用户旅程和验收案例；
- Founder 批准验收阻断规则。

### M1：企业事实层与 Intent

交付：

- 五类事实最小 Schema；
- 对话式或资料抽取式初始化；
- Context Snapshot；
- IntentExecutionPlan；
- 快速与增强模式；
- 支撑当前模块的七状态、Artifact 引用、失败处理、单品牌隔离、基础文件与凭证安全、成本与延迟记录；
- 对应诊断证据。

退出门：

- INT-01 至 INT-05、SYS-01、SYS-02、SYS-04、SYS-07 至 SYS-09 在 M1 适用范围内通过附录 B 对应检查；
- 无未关闭的事实虚构、目标擅断或阻断性缺失信息绕过；
- Founder 确认 Intent 输出足以驱动 Business Decision。

### M2：Business Decision

交付：

- 商业问题与冲突；
- 目标三个、最低两个实质差异候选；
- Product Role；
- Fact / Rule / Assumption / Model Judgment Trace；
- 候选选择工作面；
- 对应诊断证据。

退出门：

- BD-01 至 BD-08、SYS-03 和 SYS-05 的候选选择记录部分通过附录 B 对应案例；
- M1 已通过能力保持回归通过；
- 无未关闭的事实越界、候选同质化或 Trace 混淆；
- Founder / Reviewer 能基于候选做出真实选择。

### M3：Creative、制作包与受控返工

交付：

- CreativePlan；
- 九部分视频号内容制作交付包；
- VisualProfile；
- 内容包审核、局部返工和导出；
- Artifact Reference、Review Delta、Rework Controller；
- Approved Brand Memory 的人工批准路径。

退出门：

- CR-01 至 CR-07、SYS-06、SYS-10 首次通过对应案例，SYS-05 完成批准与返工记录部分；
- SYS-01、SYS-03、SYS-04、SYS-07 至 SYS-09 在完整 Creative、制作包、返工和导出链路上保持回归通过；
- M1、M2 的附录 B Gate 保持通过；
- 至少一个完整内容包被摄影或内容执行人员判断为可执行；
- 无未关闭的方向偏离、人格冲突、硬规则违反或包不完整。

### M4：匿名 A/B 与 MVP 裁决

交付：

- 锁定的代表性端到端案例；
- 同条件 ChatGPT／Claude 基线；
- 匿名随机对比记录；
- 人工选择、修改严重度和失败分类；
- Founder MVP 裁决。

退出门：

- 附录 B 的 IA-0 至 IA-3 均保持 PASS，且端到端 IA-4 退出门成立；
- 不存在关键阻断失败；
- 证据能够直接回答终极验证问题；
- Founder 明确裁决继续、修正或停止，而不是以“测试已跑完”代替商业判断。

## 10.2 需求总表

本版共有 30 条核心能力需求：

- INT-01 至 INT-05：5 条；
- BD-01 至 BD-08：8 条；
- CR-01 至 CR-07：7 条；
- SYS-01 至 SYS-10：10 条。

只有可独立验收的核心能力编号。字段说明、示例和未来设想不额外拆成大量 FR。

需求首次阻断归属如下；已经通过的 SYS 能力在后续里程碑继续回归，不因首次通过而停止验证：

| 首次阻断里程碑 | 核心需求 | 说明 |
|---|---|---|
| M1 | INT-01 至 INT-05；SYS-01、SYS-02、SYS-04、SYS-07 至 SYS-09 | 先覆盖当前已实现的 Intent、事实、状态、引用和最低运行保障 |
| M2 | BD-01 至 BD-08；SYS-03；SYS-05 的候选选择部分 | 商业候选、硬规则阻断及结构化人工选择；SYS-05 在 M3 完成其余语义 |
| M3 | CR-01 至 CR-07；SYS-05 的批准与返工部分；SYS-06、SYS-10 | 完整制作包、审核返工和人工批准记忆；其余 SYS 在完整链路回归 |
| M4 | 无新增核心需求 | IA-0 至 IA-3 继续有效，并用同条件匿名 A/B 裁决整体价值 |

## 10.3 待决事项

以下事项必须在相应里程碑开始前裁决，不得由执行人员静默假定：

| ID | 待决事项 | 最迟裁决点 | 决策人 |
|---|---|---|---|
| OD-01 | 首批试点品牌、SKU 和代表性商业目标 | M0 退出前 | Founder |
| OD-02 | A/B 使用的基础模型、版本、参数和直接基线提示合同 | M0 退出前 | Founder / 技术负责人 |
| OD-03 | 不同任务类型的阻断性最小上下文字段 | M0 退出前 | Founder / 产品负责人 |
| OD-04 | 端到端匿名 A/B 的审核者构成与最终签字人 | M0 退出前 | Founder |
| OD-05 | 薄 Runtime 采用 Dify、云 Agent 平台或轻量自建代码 | M1 开始前 | 技术负责人 |
| OD-06 | Markdown 之外是否需要 DOCX 或 PDF 导出 | M3 开始前 | Founder / Brand Operator |
| OD-07 | VLM 供应方及商品图片不可读时的人工补充方式 | M3 开始前 | 技术负责人 / Brand Operator |
| OD-08 | M4 后是否进入真实发布试点及其商业数据观察范围 | M4 裁决时 | Founder |

## 10.4 主要风险与控制

| 风险 | 控制 |
|---|---|
| 产品退化为 Prompt 包装 | 用三个模块合同、Trace 和基线 A/B 验证领域增量 |
| 重新变成传统知识库工程 | 固定“先事实、后经验”，禁止 Day 1 建设经验大库 |
| 候选数量有了但策略同质 | BD-02 与匿名人工判断同时阻断 |
| 模型流畅表达掩盖事实虚构 | FactRef、硬规则和禁止结果一票阻断 |
| 制作包形式完整但不可执行 | 由实际制作使用者判断镜头、口播和商品展示能否执行 |
| A/B 对比不公平 | M0 预先锁定事实、模型、参数、输出合同与盲测方式 |
| 文档和执行范围膨胀 | 只保留十章、两附录、两角色、三工作面和七状态 |
| 基础模型变化导致结论漂移 | 每次 Run 记录模型版本，并按版本重跑代表性案例 |

## 10.5 MVP 完成定义

MVP 完成不等于：

- 三个模块代码存在；
- Schema 全部通过；
- 测试用例全部执行；
- 页面能够导出文件；
- 文档已经批准。

MVP 完成必须同时满足：

1. 三个模块在其诊断案例中表现出目标能力；
2. 端到端输出遵守事实、规则、方向和制作包合同；
3. 在同条件匿名 A/B 中，笛语形成稳定、可解释的实际制作偏好；
4. 人工修改主要是可控局部修改，而非反复推翻商业策略；
5. Founder 对终极验证问题作出明确肯定裁决。
