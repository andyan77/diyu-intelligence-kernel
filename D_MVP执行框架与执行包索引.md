# D｜笛语 Intelligence Kernel MVP 执行框架
## ——围绕三个核心智能模块的产品验证型 MVP（执行索引 + 排期视图）

## D.0 文档控制

| 项 | 值 |
|---|---|
| 版本 | v1.4（由 Founder 起草 v1.0 经审查修订） |
| 日期 | 2026-08-16 |
| 定位 | **执行索引 + 排期视图**。本文档给执行侧一张地图：先做什么、后做什么、每步验收挂在哪。 |
| 从属关系 | 从属于 主 PRD / 附录 A / 附录 B（三份冻结真源）及 C 方案（执行侧工程机制）。**任何冲突以 PRD/A/B 为准。本文档只引用编号，不复述定义——转述不作为验收口径。** |

### v1.0 → v1.1 修订记录（7 处，均经原文核验）

| # | 修订 | 依据 |
|---|---|---|
| 1 | M4 测试案例由"例如：新品品牌内容…"改为 B.5.1 冻结的 E2E-01/02/03 | B.5.1 三场景不可互相替代 |
| 2 | M0 两个执行包重新定义：PRD/A/B 已冻结存在，剩余工作是裁决与可执行化，不是重写文档；删除简化 schema 复述 | 防第二真源漂移 |
| 3 | 基线表述对齐 B.2.4：正式基线=同模型直接调用，消费端界面只作补充观察 | B.2.4 |
| 4 | Rework 允许原因补回 `PRODUCTION_ISSUE`（5 项枚举） | A.2.6 ReworkReason |
| 5 | 各 EP 验收标准改为指向 Gate IA-n / PRE / 案例编号，不自写宽松口径 | B.8 |
| 6 | 补"开发可乱序、闸门按序关闭"的和解规则 | B.4 模块隔离、B.8 |
| 7 | M3-EP02 验收补挂 SYS-D01 与 B.10 证据记录 | Gate IA-3 |

### v1.1 → v1.2 修订记录

| # | 修订 | 依据 |
|---|---|---|
| 1 | 新增文档体系地图（含 E / F 与归档区） | 文档间口径一致性 |
| 2 | M0-EP01 试点材料采集挂接 F 采集表 | OD-01 工具落位 |
| 3 | 历史文档（笛语智能核.md、三个核心模块测试矩阵建议.md）归档至 archive/ | 防过时口径被引用 |

### v1.2 → v1.3 修订记录

| # | 修订 | 依据 |
|---|---|---|
| 1 | 文档地图增加 G（后 MVP 愿景暂存与 MVP 边界裁决） | Founder 裁决：BRAND_STORY 窄门 + 试点为品牌账号 |

### v1.3 → v1.4 修订记录

| # | 修订 | 依据 |
|---|---|---|
| 1 | 文档地图增加《知识提取会议排期》（E 协议排期细化，派生参考非 Gate） | Founder 2026-08-17 裁决：9 个主题工作单元排期采纳 |

### 文档体系地图（真源层级）

| 层级 | 文档 | 性质 |
|---|---|---|
| 冻结真源 | 主 PRD / A 模块接口与核心数据字典 / B 三个核心模块智能验收合同 | 一切口径以此为准，修改走版本升级 |
| 执行机制 | C 三个核心模块工程化落地与防死循环方案 | 仓库三区制、案例执行格式、判分三层、防死循环 |
| 执行索引 | D 本文档 | Gate 排期与执行包地图，只引用不复述 |
| 工作协议 | E 领域专家知识提取协议 | 出声思考会、知识卡、知识五去处路由 |
| 排期参考 | 知识提取会议排期 | E 协议的排期细化：9 个主题工作单元；**派生排期参考，冲突以 E/B 为准，不是 Gate** |
| 采集工具 | F 品牌事实初始化采集表 | A.3 的人话表单（OD-01 工具 + 品牌初始化功能雏形） |
| 边界与暂存 | G 后MVP愿景暂存与MVP边界裁决 | MVP 边界裁决记录 + 后 MVP 愿景登记；**不得作为任何 Gate 前置或需求来源** |
| 历史归档 | archive/（笛语智能核.md、三个核心模块测试矩阵建议.md） | 已被 PRD / A / B 取代，不得作为现行口径引用 |

各文档版本号只登记在各自"文档控制"章节，文件名不带版本号（主 PRD 为冻结真源保持原名）。

---

# 一、MVP 总原则（冻结）

## 1. MVP 唯一目标

笛语 MVP 只回答一个问题（= 主 PRD 1.2 终极验证问题）：

> **在相同企业事实、相同基础模型、相同输出要求下，笛语是否能够稳定地产生比通用 LLM 更具商业价值的视频号内容制作交付包？**

不是验证：

- 系统是否完整；
- SaaS 是否成熟；
- 工程架构是否复杂；
- 是否具备所有企业功能。

---

# 二、MVP 产品核心结构

## 核心智能层（唯一护城河）

```text
Diyu Intelligence Kernel
├── Intent Intelligence Module
├── Business Decision Engine
└── Creative Content Engine
```

## 支撑能力层（服务核心，不形成独立产品价值）

```text
Supporting Layer
├── Enterprise Semantic Layer
├── Runtime Service
├── Rule Engine
├── Artifact Reference
├── Review Delta
└── Rework Controller
```

## 外部能力层（借用，Build/Borrow 裁决见主 PRD 4.4）

```text
Infrastructure Layer
├── LLM / VLM
├── Dify / Minimal Host（OD-05 待裁决）
├── PostgreSQL
├── OSS
└── Search / Tools
```

---

# 三、MVP Gate 总览

正式采用 M0-M4 五个 Gate（与主 PRD 10.1 里程碑一一对应，验收闸门为附录 B.8 的 IA-0 至 IA-4）：

```text
M0  产品合同与验证基线          ← Gate IA-0
↓
M1  企业事实层 + Intent         ← Gate IA-1
↓
M2  Business Decision Engine    ← Gate IA-2
↓
M3  Creative + Runtime 闭环     ← Gate IA-3
↓
M4  笛语 vs 通用 LLM 价值验证   ← Gate IA-4
```

---

# 四、执行包总览

## 5 个 Gate，8 个执行包

```text
M0
├── M0-EP01  合同基线核对与待决事项裁决
└── M0-EP02  验收合同可执行化与基线冻结

M1
├── M1-EP01  Enterprise Semantic Layer
└── M1-EP02  Intent Intelligence Module

M2
└── M2-EP01  Business Decision Engine

M3
├── M3-EP01  Creative Content Engine
└── M3-EP02  Runtime 与生产闭环

M4
└── M4-EP01  Diyu vs General LLM 验证
```

---

# 五、M0：产品合同与验证基线

> **重要：M0 的文档类交付物已经存在。** 主 PRD、附录 A（模块接口与数据字典）、附录 B（智能验收合同，含 11 条诊断案例 + 3 条 E2E + 失败标签 + 五道闸门）均已冻结落盘。M0 剩余的真实工作不是写文档，而是**裁决 + 可执行化**。

---

# M0-EP01｜合同基线核对与待决事项裁决

## 执行意图

让三份真源文档正式生效，消除"知道做什么、不知道什么叫成功"的状态。

## 工作内容

1. 三份文档版本一致性核对（互相引用的版本号对齐）；
2. **OD-01 至 OD-04 裁决**（主 PRD 10.3，M0 退出前必须，不得由执行人员静默假定）：
   - OD-01 首批试点品牌、SKU 和代表性商业目标（Founder）；
   - OD-02 A/B 基础模型、版本、参数和直接基线提示合同（Founder / 技术负责人）；
   - OD-03 不同任务类型的阻断性最小上下文字段（Founder / 产品负责人）；
   - OD-04 端到端匿名 A/B 的审核者构成与最终签字人（Founder）——**制作侧裁判（摄影/内容执行人员）有寻找与排期周期，须提前启动**；
3. 首批试点事实材料收集（对应 OD-01；采集工具：**F 品牌事实初始化采集表**——字段派生自 A.3，只采事实不采经验，经验类内容分流到 E 协议）。

## 交付物

- 待决事项裁决记录（OD-01~04）；
- 首批试点事实材料；
- 文档版本一致性声明。

产品定义见主 PRD 1.3；三模块职责见主 PRD 5.2-5.4；数据合同见附录 A.5-A.8；非目标清单见主 PRD 2.5。**本文档不复述。**

## 验收标准

= 主 PRD 10.1 M0 退出门：三份文档版本一致；OD-01 至 OD-04 已裁决；模块合同覆盖已锁定用户旅程和验收案例；Founder 批准验收阻断规则。

---

# M0-EP02｜验收合同可执行化与基线冻结

## 执行意图

把附录 B（已冻结的测试矩阵）从"人读的合同"变成"机器能跑的红绿灯"，并冻结 A/B 对比条件。这是整个项目最重要的质量基线。

## 工作内容

1. **验收合同可执行化**（按 C 方案执行）：
   - 仓库三区制骨架（contracts / kernel / acceptance）+ 考卷考生隔离门；
   - 附录 A 核心对象转 JSON Schema（IntentExecutionPlan、BusinessDecisionBundle、CaseManifest 先行）；
   - 首条案例执行文件（BD-D01：manifest + fixtures + 确定性断言 + 故意注错验证断言会红）；
   - 禁止结果检测覆盖率注册表（分母由脚本从 B 实时统计，禁止硬编码）；
2. **Case Manifest 批准**（B.2.1）：14 条锁定案例（11 条诊断 + 3 条 E2E）逐条冻结 Manifest（多输入/双模式案例一变体一份 → 共 **20 份**运行 Manifest，齐套口径见《IA-0 冻结签字包》§五）；
3. **基线冻结**（B.2.3 / B.2.4）：
   - 两阶段共同交互合同与输出合同冻结；
   - 两阶段基线 Prompt 运行前冻结，不得故意写弱；
   - **正式基线 = 不经过笛语模块的同基础模型直接 API 调用**（阶段 D、阶段 C 各一次受控调用）；ChatGPT/Claude 消费端界面因模型版本不可确认，**只作补充观察，不构成正式证据**；
4. **匿名流程确定**（B.2.5）：随机 X/Y 标签、盲测冻结、揭晓规则。

## 验收标准

= Gate IA-0（B.8）全部条件。测试维度、正例/失败/边界案例、人工判断标准均已在附录 B 定义（B.4 诊断案例 / B.5 E2E / B.6 失败标签 / B.1.2 不设综合总分），**本 EP 不新写口径，只做可执行化**。

---

# 六、M1：企业事实层 + Intent

# M1-EP01｜Enterprise Semantic Layer

## 执行意图

让系统拥有企业事实。不是经验库（主 PRD 6.1"先事实，后经验"）。

## 目标

建立五类事实（Schema 以附录 A.3 为准）：

```text
Brand Facts        （A.3.1）
Product Facts      （A.3.2，含 VisualProfile A.3.3）
Audience Facts     （A.3.4）
Persona Facts      （A.3.5）
Video Account Facts（A.3.6）
```

## 交付物

- 五类事实最小 Schema 实现与校验；
- 对话式或资料抽取式品牌初始化；
- Context Snapshot（A.4.3）。

## 数据原则（对齐 A.1）

必须：有来源（SourceRef）、有版本（VersionedRef）、Unknown 显式（A.1.4 不确定性必须显式）。
禁止：自动补事实、编造品牌属性。

## 验收标准

品牌人员可以上传资料，系统形成可用于内容任务的事实上下文；数据合规性通过 PRE-04（单品牌隔离）、PRE-05（凭证与文件安全）。终验收并入 Gate IA-1。

---

# M1-EP02｜Intent Intelligence Module

## 执行意图

把用户需求转换为业务任务。

## 输入 / 输出

输入：自然语言任务（如"帮我推广这件羊绒大衣"）+ ContextSnapshot。
输出：IntentExecutionPlan，**字段以 A.5.2 为准**。

## 核心组件

- **Intent Parser**：理解需求；
- **Task Classifier**：识别任务类型（新品 / 清库存 / 品牌传播 / 用户教育…）；
- **Context Requirement Resolver**：判断当前任务需要哪些关键资料（阻断性最小字段按 OD-03 裁决结果，**由确定性字段 diff 得出，不交给 LLM 判断**——见 C.3）；
- **Progressive Context Completion**：资料不足时请求补充 / 降低置信度 / 输出受限结果（快速与增强模式，主 PRD 6.4）。

## 验收标准

= Gate IA-1（B.8）：PRE-01-I、PRE-03-M、PRE-04、PRE-05、PRE-06、PRE-07-I 通过；**INT-D01（模糊目标不得擅自确定）、INT-D02（快速/增强模式）、INT-D03（同商品目标迁移）均 PASS**；无未关闭的目标擅断、事实虚构或阻断项绕过；输入、输出、Trace 与人工结论可追溯。另需主 PRD M1 退出门：Founder 确认 Intent 输出足以驱动 Business Decision。

---

# 七、M2：Business Decision Engine

# M2-EP01｜Business Decision Engine

## 执行意图

建立笛语核心商业判断能力。不是预测销量，不是自动商业专家，而是：

> 基于事实和约束生成结构化商业候选。

## 输入 / 输出

输入：BusinessDecisionRequest（A.6.1）。
输出：BusinessDecisionBundle，**字段以 A.6.2 / A.6.3 为准**。三个关键语义不得丢失：

- `recognized_conflicts`：显式冲突识别（对应 BD_CONFLICT_MISSED）；
- `candidate_count_status`：TARGET_THREE / DEGRADED_TWO / BLOCKED_FEWER_THAN_TWO 三态——目标三个候选、最低两个，少于两个不得进入 DECISION_READY，不补造候选；
- `human_selection_required: true`：**系统推荐（system_recommendation，属 MODEL_JUDGMENT）不免除人工选择**（对应 BD_HUMAN_GATE_BYPASSED）。

## 核心能力

- **Product Role Engine**：Hero / Supporting / Traffic / Profit / Clearance（枚举以 A.2.6 为准）；
- **Candidate Generator**：候选差异必须体现在商业机制、商品角色、叙事路径或风险取舍，不得靠标题和形容词凑数（A.6.3 约束）；
- **Candidate Evaluation**：brand_fit / audience_fit / business_alignment / production_feasibility 定性判断（ALIGNED / TENSION / UNKNOWN），不计算加权总分；
- **Trace 四类分离**：FACT / RULE / ASSUMPTION / MODEL_JUDGMENT（A.1.2）。

## 验收标准

= Gate IA-2（B.8）：IA-1 保持 PASS；PRE-01-B、PRE-02、PRE-07-B 通过；**BD-D01（库存与价值冲突）、BD-D02（有限商品池不得补写）、BD-D03（反常识商品情境判断）均 PASS**；Founder / Reviewer 能做出真实选择并形成一致的 ReviewRecord 与 DecisionSelection；候选实质差异；无事实虚构、硬规则违反、Trace 混写或人工门绕过。

---

# 八、M3：Creative Content + Runtime

# M3-EP01｜Creative Content Engine

## 执行意图

把商业决策转化为视频号内容生产方案。

## 输入 / 输出

输入：CreativeContentRequest（A.7.1）——必须精确绑定 DecisionSelection 与 BusinessDecisionBundle。
输出：CreativeContentBundle，**字段以 A.7.2 为准**（creative_plan + 九部分交付包引用 + validation 四项 + trace）。九部分交付包结构以 A.8 为准。

## 核心能力

- **Persona**：谁来说（PersonaFacts A.3.5，人设一致性对应 CR_PERSONA_DRIFT）；
- **Story Strategy**：为什么用户关注（audience_tension / story_angle）；
- **Hook Strategy**：开头如何建立兴趣；
- **Video Grammar**：视频号表达方式（对应 CR_PLATFORM_MISMATCH）;
- **Visual Understanding**：商品轮廓、色彩、视觉重点、拍摄注意（VisualProfile A.3.3；视觉不可读时显式降级，PRE-03-V，不得虚构视觉属性）。

## 验收标准

CR-D01（人设反事实）、CR-D02（视频号语法与决策承接）、CR-D03（完整可制作交付包）、CR-D04（视觉证据与硬规则）均 PASS；至少一个完整内容包被摄影或内容执行人员判断为可执行。终验收并入 Gate IA-3。

---

# M3-EP02｜Runtime 与生产闭环

## 执行意图

让三个模块成为可运行系统。不建设复杂 Agent、复杂 DAG。

## 最小 Runtime

七状态及允许迁移**以 A.4.4 为准**：

```text
DRAFT / NEEDS_INPUT / DECISION_READY / CREATIVE_READY / REVIEW_REQUIRED / COMPLETED / FAILED
```

（HUMAN_DECISION_REQUIRED 是 REVIEW_REQUIRED 下的标记，不是第八状态；未列出的迁移一律拒绝。）

## 核心对象

Task、ContextSnapshot、Run、Artifact、Review、Revision、**DecisionSelection（A.6.4）、FailureRecord（A.4.6）**。

## Artifact Reference

按 A.9.3 ArtifactEnvelope（id / type / version / source / parent_references）。

## Rework Controller

允许原因（**A.2.6 ReworkReason，5 项**）：

- FACT_ERROR（须先更新事实版本和 Snapshot）；
- RULE_CONFLICT；
- **PRODUCTION_ISSUE**；
- BRAND_MISMATCH（可形成 Memory Candidate，但不自动成为偏好）；
- USER_OBJECTIVE_CHANGED（必须返回 Intent）。

限制：局部修改最多 2 次；策略重做最多 1 次；超限 outcome=HUMAN_DECISION_REQUIRED，停止自动生成（A.9.5 / 主 PRD 8.5）。

## 验收标准

= Gate IA-3（B.8）中 Runtime 相关条件：PRE-07-I/B/C 全部状态迁移检查通过；**SYS-D01（选择、批准、局部返工、版本引用与停止条件横向案例）PASS**；三模块真实串联、修改不造成上下游错配、失败可恢复、不无限循环；每个正式案例按 **B.10 AcceptanceEvidenceRecord** 留存最小验收证据。

---

# 九、M4：价值验证

# M4-EP01｜Diyu vs General LLM

## 执行意图

回答项目存在意义：同样条件下，笛语是否明显优于通用 LLM？

## 测试条件

= B.2.2"同条件"定义：同 Snapshot、同图片材料、同任务、同硬规则、同最终输出合同、同模型供应商与版本、同生成参数与工具边界、Brand Memory 状态一致；笛语可多模块多次调用（编排是被验证的能力），但须记录总调用次数、Token、成本、延迟。

## 测试案例（B.5.1 锁定，三个不可互相替代，不得用相似案例抵消）

| 编号 | 场景 | 证明什么 |
|---|---|---|
| **E2E-01** | 高端品牌库存激活（羊绒大衣 800 件、禁低价叫卖、限期促销） | 能否处理"销量 vs 品牌价值"冲突 |
| **E2E-02** | 同事实、只改目标为长期品牌资产 | 目标迁移能否传导整条链路（Intent 迁移 → 取舍改变 → 创意承接，不沿用库存激活结果） |
| **E2E-03** | 反常识商品（荧光绿裤装） | 不武断拒绝、基于面积/层次/场景/受众形成可解释判断并落成可拍摄交付包 |

## 判断方式

两阶段匿名 A/B（B.2.3）：阶段 D 匿名选候选并冻结 → 阶段 C 各自生成完整交付包 → E2EComparisonEnvelope 匿名终审（B.2.5）。评价的不是"哪个更长"，而是：商业策略可信度、内容采用意愿、修改幅度（edit_severity）、是否愿意直接制作——记录字段以 B.10 为准。

## 验收标准

= Gate IA-4（B.8）：IA-0~IA-3 均保持 PASS；三场景逐案满足"明显优于"定义（B.5.5）；商业与制作裁判都选择笛语；所需修改不高于 LOCAL；无阻断性失败；成本延迟与模型条件记录完整；Founder 明确签署 MVP 裁决。任一场景 FAIL / INCONCLUSIVE / NEITHER / NO_MATERIAL_DIFFERENCE 即不通过。**不能平均分覆盖严重失败（B.1.2）。**

---

# 十、最终 MVP 执行总表

| Gate | 执行包 | 核心目标 | 验收闸门 |
|---|---|---|---|
| M0 | EP01 | 合同基线生效 + OD-01~04 裁决 | IA-0（部分） |
| M0 | EP02 | 验收合同可执行化 + 基线冻结 | IA-0（全部） |
| M1 | EP01 | 企业事实层成立 | IA-1（并入） |
| M1 | EP02 | Intent 成立 | IA-1 |
| M2 | EP01 | Business Decision 成立 | IA-2 |
| M3 | EP01 | Creative 成立 | IA-3（并入） |
| M3 | EP02 | Runtime 闭环成立 | IA-3 |
| M4 | EP01 | 证明笛语价值 | IA-4 |

---

# 十一、最终工程优先级

资源有限时的**开发投入**优先级：

1. **M0-EP02 验收可执行化**——不知道怎么判断成功，就不知道怎么开发；
2. **M2-EP01 Business Decision**——最可能形成差异的模块；
3. **M3-EP01 Creative Content**——最终用户购买的是内容交付；
4. **M1-EP01 事实层**——提供企业上下文；
5. **Runtime 和 Host**——够用即可。

## 和解规则（本节与 Gate 顺序的关系）

> **开发可乱序，闸门按序关闭。**

- BD 可以先行开发：用**冻结的 IntentExecutionPlan fixture** 和最小事实包驱动（附录 B.4 本就要求模块诊断隔离被测模块——"Business Decision 测试使用冻结的 IntentExecutionPlan"）；
- 但 Gate IA-2 的关闭前提是 IA-1 保持 PASS（B.8 原文），验收次序不可颠倒；
- 事实层排第四指的是**打磨投入**的优先级，不是可以没有——BD 没有事实快照连输入都不存在，M1-EP01 的最小版本是 BD 开发的前置。

---

# 十二、最终冻结一句话

> **笛语 MVP 不是先建设一个完整 AI SaaS，而是先验证三个核心智能模块是否能够在企业事实约束下，持续产生比通用 LLM 更具商业价值的视频号内容制作交付包。**

```text
M0 定义能力
M1 理解企业
M2 做商业判断
M3 生产内容
M4 证明价值
```

这就是当前 `diyu-intelligence-kernel` 的 MVP 执行框架。
