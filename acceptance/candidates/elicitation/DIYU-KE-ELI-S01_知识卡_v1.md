# DIYU-KE-ELI-S01｜Intent：真实商业目标识别 正式入库知识卡

```yaml
document_id: DIYU-KE-ELI-S01-20260817-V1
session_id: DIYU-KE-S01-20260817-001
session_theme: S01 Intent：真实商业目标识别
covered_rounds: [S01-R01, S01-R02]
source_files:
  - DIYU-KE-S01-20260817-001_S01待入库候选包_v3.md（本场唯一权威来源；S01 无专家 TXT 原文文件）
  - E_领域专家知识提取协议.md（E.2 路由 / E.2.3 失败标签 / E.3 卡模板 / E.10 防膨胀）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S01 一节：有效底稿，需 E.3 转换层）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（第三节 S01 行、第四节 PCR-01）
ruling_basis: Founder（Faye）2026-08-17 裁决 S01–S08 候选包与追问卡专家回答全部批准通过，指示按 E 协议整理为正式入库文档。
compiled_on: 2026-08-17
card_total: 24
routed_count: 24
pending_count: 1
formal_effect: NONE   # 全部为候选，生效另走 A.9.1 / B.8.1 批准流程
```

> **控制声明**：本文件是 E.3 意义上的知识卡（路由单），不是生效资产。任何硬规则、状态值、失败标签、目标枚举、Brand Memory 条目，仍须走对应批准与版本升级流程后才能生效。本文件不修改任何既有文件。
>
> **S01 provenance 特例**：S01 是全系列唯一存在 Founder 逐条裁决与修改的场次。以下各卡 provenance 按 v3 候选包内逐卡已标注等级**原样继承**，不升级、不降级（含 `AI_PROPOSAL_REJECTED`、`UNRESOLVED` 两个会议协议既有等级，见第三节残留说明第 6 条）。

---

## 一、入库知识卡（ROUTED）

```yaml
elicitation_item_id: ELI-0101
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "用户仅输入「帮我推广这件大衣」，未说明什么结果算成功。"
expert_statement: "对「帮我推广这件大衣」，允许的结果是 NEEDS_INPUT 与目标澄清；禁止直接生成任何单一商业路线的方案或内容。"
statement_type: BOUNDARY
applies_when: "输入只确定了推广对象，没有确认商业成功结果。"
does_not_apply_when: "用户已经明确主目标；但其他缺失仍须独立检查。"
counterexample: "系统直接输出「以清库存为目标」的推广方案。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_REVISED
source_ref: "v3 包 CR-S01-R01-01（L175-183）；细化对象为现有 INT-D01／INT-D03 答案族与禁止结果，不得自动新增正式验收案例。"
```

```yaml
elicitation_item_id: ELI-0102
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "用户明确拒绝继续提供目标信息，系统仍须给出交付物。"
expert_statement: "用户拒绝澄清时，只允许输出带明确前提的条件化选项菜单，且任何选项都不得被认定为用户目标。"
statement_type: BOUNDARY
applies_when: "用户明确拒绝继续提供目标信息。"
does_not_apply_when: "用户已经确认主目标。"
counterexample: "用户拒答后，系统自行选择曝光路线并生成内容。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 CR-S01-R01-02（L185-193）；亦为 UN-S01-05 裁决前的 fail-closed 执行口径（见 ELI-0124）。"
```

```yaml
elicitation_item_id: ELI-0103
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "商业目标状态尚未确认，下游模块已可被调用。"
expert_statement: "商业目标状态未确认时，下游不得生成单一商业路线的执行产物。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "goal_status != CONFIRMED。"
does_not_apply_when: "主目标已经确认；其他阻断项仍须单独验证。"
counterexample: "goal_status=UNCONFIRMED 但系统已经生成成交脚本。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R01-01（L197-205）；已由 ELI-0118（HR-S01-R01-01-REV1）提出候选修订，两卡须并审。"
```

```yaml
elicitation_item_id: ELI-0104
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "用户只说了渠道或内容形式（如「发小红书」「拍短视频」）。"
expert_statement: "渠道或内容形式字段不能单独把商业目标状态提升为 CONFIRMED。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "输入只有小红书、视频号、直播、短视频等手段信息。"
does_not_apply_when: "用户同时明确说明了主目标及成功结果。"
counterexample: "因用户说「发小红书」，系统自动确认目标为曝光。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R01-02（L207-215）"
```

```yaml
elicitation_item_id: ELI-0105
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "Intent 输出中混有确认事实、观察、合成条件与模型判断。"
expert_statement: "所有事实型字段必须携带 SourceRef 和 FactStatus；非确认状态可以合法存在，但不得伪装成 CONFIRMED_FACT。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "Intent 输出包含事实型字段。"
does_not_apply_when: "纯控制状态或不构成事实声明的结构字段。"
counterexample: "将视觉观察到的纹理直接记录为已确认面料成分。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_REVISED
source_ref: "v3 包 HR-S01-R01-03（L217-225）；Founder 将原提案「事实只能来自 CONFIRMED_FACT」修订为 SourceRef + FactStatus 纪律。"
```

```yaml
elicitation_item_id: ELI-0106
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "人工评审一份「表面完整、实际未完成」的 Intent 输出。"
expert_statement: "用排除力、新信息、事实溯源三项检验识别表面完整实则未完成的 Intent 输出；事实溯源按 SourceRef + FactStatus 判断。三项检验为判分校准候选，尚未成为正式考卷规则。"
statement_type: BOUNDARY
applies_when: "人工判断 Intent 是否完成了有效编译。"
does_not_apply_when: "用于直接决定正式目标枚举或自动升级事实状态。"
counterexample: "「提升曝光和销量」不能排除任何路线，也没有新增用户确认信息，应判为未完成。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_REVISED
source_ref: "v3 包 JC-S01-R01-01（L229-237）；去处为 INT-D01／INT-D03 人工裁判问题候选。"
```

```yaml
elicitation_item_id: ELI-0107
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "校准中出现虚构目标、常识回填、手段当目标、复述冒充 Intent 四类错误语义。"
expert_statement: "GOAL_FABRICATION、COMMON_SENSE_BACKFILL、MEANS_AS_GOAL、PARAPHRASE_AS_INTENT 只能作为失败概念候选用于校准说明，不得作为正式错误码或 B.6 失败标签使用；必须先做既有标签覆盖审查，覆盖不足时再走合同升级提案。【新标签候选，须走 B.8.1 覆盖审查，不得私加】覆盖审查的既有标签锚点已由排期主题 1 具名（INT_GOAL_ASSUMED、INT_COUNTERFACTUAL_NOT_PROPAGATED、BD_CONFLICT_MISSED），映射本身尚未执行。"
statement_type: FAILURE_MODE
applies_when: "校准中发现现有标签可能无法准确表达上述错误语义。"
does_not_apply_when: "B.6 已有标签能够完整覆盖。"
counterexample: "直接在正式考卷中写入 GOAL_FABRICATION 新标签。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_REJECTED
source_ref: "v3 包 JC-S01-R01-02（L239-247），provenance 原样继承：REJECTED 指向的是「把候选失败概念直接升级为正式错误码／标签」这一被 Founder 否决的原提案，本卡承载的是否决后存续的约束口径（同见 R01 一票否决清单 L161）。既有标签具名锚点见《标准对齐复核结论》S01 一节①。"
```

```yaml
elicitation_item_id: ELI-0108
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "同时存在多个缺失项，需要决定先问哪一个。"
expert_statement: "先识别阻断缺失，再优先询问对下游路线区分力最高的一项；本案例中是「什么结果算成功」。"
statement_type: METHOD
applies_when: "同时存在多个缺失项且需要确定澄清顺序。"
does_not_apply_when: "已有一项明确的更高优先级硬阻断，或该信息已确认。"
counterexample: "固定规定任何场景都必须先问商业目标。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_REVISED
source_ref: "v3 包 MM-S01-R01-01（L251-259）；Founder 将「首问永远指向最上游类型缺失」修订为「优先询问区分力最高的阻断缺失」。三份专家首问方法均为合法答案族成员（方法骨架层），不要求收敛唯一方法。"
```

```yaml
elicitation_item_id: ELI-0109
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "用户同时表达出多个合法商业目标。"
expert_statement: "Intent 可以记录一个主目标和若干次目标；下游策略与验收以主目标为准。"
statement_type: METHOD
applies_when: "用户同时表达多个合法目标。"
does_not_apply_when: "用户尚未确定任何目标，或目标之间的优先级仍不清楚。"
counterexample: "把曝光和成交机械判定为绝对互斥，强制删除其中一个。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_REVISED
source_ref: "v3 包 MM-S01-R01-02（L261-269）；Founder 将「三类目标绝对互斥」修订为「一个主目标、若干次目标」。正式目标枚举本身未裁决，已分流 PCR-01。"
```

```yaml
elicitation_item_id: ELI-0110
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "判断某个推广任务是否必须先拿到商品资料、成交承接与库存。"
expert_statement: "商品最低事实、成交承接和库存采用任务条件化依赖，不设置为全局固定阻断：成交承接只在转化类任务中构成关键依赖，库存只在库存相关任务中构成关键依赖。"
statement_type: METHOD
applies_when: "Intent 模块判断后续任务所需上下文。"
does_not_apply_when: "尚未取得足够信息判断依赖是否适用。"
counterexample: "对纯品牌认知任务强制要求成交链接和库存数量。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_REVISED
source_ref: "v3 包 MM-S01-R01-03（L271-279）；该任务条件化归一口径经 Founder 2026-08-17 差异对比审阅后确认（v3 包 0 章第 3 条），并在 R02 复用（见 ELI-0123）。"
```

```yaml
elicitation_item_id: ELI-0111
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "用户看过条件化目标选项后说「我不懂，你替我决定」。"
expert_statement: "该局面的合法答案族应包含：单一默认方向宣告、推荐依据、授权范围、可否决性、下一步信息请求；不得把默认写成用户已确认目标。"
statement_type: BOUNDARY
applies_when: "用户对当前目标选择作出明确、窄范围的决策委托。"
does_not_apply_when: "用户没有明确授权，或授权对象不是商业目标选择。"
counterexample: "系统直接把目标记为 CONFIRMED 并生成成交脚本。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 CR-S01-R02-01（L438-446）；细化对象为现有 INT-D01／INT-D03，不得自动新增正式验收案例。"
```

```yaml
elicitation_item_id: ELI-0112
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "系统已宣告临时默认方向后，用户补充说出了不同的主目标。"
expert_statement: "用户后续明确说出与默认不同的目标时，默认即时失效，消费过旧默认的下游产物应从 Intent 层起重新判断。"
statement_type: BOUNDARY
applies_when: "用户在默认宣告后补充或改变主目标。"
does_not_apply_when: "用户只补充不影响目标的事实。"
counterexample: "用户说「其实我只想让人认识门店」，系统仍沿用旧成交默认。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 CR-S01-R02-02（L448-456）；对应 Intent 反事实传播与跨模块失效案例细化。"
```

```yaml
elicitation_item_id: ELI-0113
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "用户说「你替我决定」，系统据此代选目标。"
expert_statement: "显式决策委托可以转移当前选择权，但不能创造或转移客观事实权威——不授权系统虚构商品、品牌、库存、平台、受众、活动或成交条件。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "用户明确要求系统代选目标或其他当前决策。"
does_not_apply_when: "用户没有授权，或系统只是在提供建议而未代理选择。"
counterexample: "因用户说「你定」，系统自行补写库存压力和折扣活动。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R02-01（L460-468）"
```

```yaml
elicitation_item_id: ELI-0114
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "一次针对目标选择的委托之后，系统面临受众、价格、调性等新决策。"
expert_statement: "授权必须按当前问题定界，不得静默扩张到其他未决项。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "一次授权发生在具体选项或具体决策问题之后。"
does_not_apply_when: "用户明确给出更广范围且可解释的授权。"
counterexample: "目标代选授权被扩张为价格、受众和品牌调性的全面代决。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R02-02（L470-478）"
```

```yaml
elicitation_item_id: ELI-0115
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "临时默认方向随产物流转到 Business 与 Creative 下游。"
expert_statement: "系统代选的默认方向不得标记为用户确认事实；其来源、假设状态和可否决性必须随下游产物传递。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "使用显式委托形成临时工作目标。"
does_not_apply_when: "用户已经明确陈述主目标并满足确认合同。"
counterexample: "中间层把 ASSUMED_DEFAULT 清洗为 CONFIRMED 后交给 Creative。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R02-03（L480-488）；ASSUMED_DEFAULT 的正式数据结构未裁决，已分流 PCR-01（不得未经合同升级直接加入状态机）。"
```

```yaml
elicitation_item_id: ELI-0116
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "系统准备在用户委托下给出一个默认商业方向。"
expert_statement: "默认方向只能引用版本化产品策略；缺少可追溯策略时，模型不得临场生成默认方向。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "系统准备在用户委托下代选目标。"
does_not_apply_when: "用户已经自己确认目标。"
counterexample: "模型用「大衣通常以卖货为先」作为默认依据。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R02-04（L490-498）；附录 A F2 据此限定入族范围——专家一「最小预设」与专家二「常见推广场景」的运行时临场选向依据不随方法骨架入族，两个锚点主张降格为默认策略锚点的候选输入（已分流 PCR-01）。"
```

```yaml
elicitation_item_id: ELI-0117
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "用户后续目标表态与系统当前默认不一致。"
expert_statement: "用户明确改变目标时，旧默认及依赖旧默认的下游产物必须按影响范围失效，不得继续沿用。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "用户后续目标表态与当前默认不一致。"
does_not_apply_when: "新信息不改变主目标或策略方向。"
counterexample: "目标已改为门店认知，旧成交脚本仍被导出。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R02-05（L500-508）；去处为 Intent invalidation／Rework Controller 规则候选。"
```

```yaml
elicitation_item_id: ELI-0118
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "R01 的「目标未确认即不得生成单一路线」规则遇到显式委托分支。"
expert_statement: "对 R01 候选规则的修订：目标来源可以是用户确认，也可以是显式委托下、由版本化策略产生且携带完整来源标记的临时默认；临时默认不得视为确认事实，任何执行产物仍须通过任务相关事实与约束门。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "Intent 已取得用户确认目标，或取得合法的窄范围委托并形成可追溯默认。"
does_not_apply_when: "用户未确认也未授权，或默认来源不可追溯。"
counterexample: "无授权、无策略来源时直接生成单一商业路线。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 HR-S01-R01-01-REV1（L510-518）；本卡是对 ELI-0103（HR-S01-R01-01）的候选修订，须与之并审后另行批准，不得单独进入任何生产规则。"
```

```yaml
elicitation_item_id: ELI-0119
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "人工评审显式委托分支下系统「代选目标」的一次真实输出。"
expert_statement: "判断代选目标输出是否合格，至少检查七项：委托是否明确、推荐是否单一、默认是否可见、依据是否可追溯、授权范围是否声明、否决权是否保留、改变条件是否声明（说明什么情况下该默认不再成立）；同时检查是否把默认误写为确认事实。"
statement_type: BOUNDARY
applies_when: "人工评审显式委托分支的 Intent 输出。"
does_not_apply_when: "用户已经自己确认目标。"
counterexample: "输出看似给出方向，但未说明其为系统代选，也没有策略来源。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 JC-S01-R02-01（L522-530）；第七项「改变条件是否声明」源自专家一四要素校准候选（推荐＋显式假设＋推荐理由＋改变条件），V2 补录。"
```

```yaml
elicitation_item_id: ELI-0120
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "校准委托分支错误时出现授权洗白、授权蔓延、暗默认等错误语义。"
expert_statement: "AUTHORIZATION_LAUNDERING（授权洗白）、DELEGATION_SCOPE_CREEP（授权范围蔓延）、INVISIBLE_DEFAULT（暗默认）、POLICY_FREESTYLE（策略临场发挥）、ASSUMED_INTENT_PROMOTED_TO_FACT（授权绕过事实门）只作为失败概念候选用于校准说明，不得直接成为正式标签；正式判分必须先映射 B.6 既有标签，覆盖不足时再提交合同版本提案。【新标签候选，须走 B.8.1 覆盖审查，不得私加】"
statement_type: FAILURE_MODE
applies_when: "现有标签可能无法精确表达委托分支错误。"
does_not_apply_when: "B.6 已有标签足以覆盖。"
counterexample: "未做映射审查就新增 AUTHORIZATION_LAUNDERING 正式标签。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 JC-S01-R02-02（L532-540）；与 ELI-0107 共用同一条 B.6 覆盖审查通道。"
```

```yaml
elicitation_item_id: ELI-0121
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "用户已看过可理解的条件化选项，仍说「我不懂，你替我决定」。"
expert_statement: "把「我不懂，你替我决定」拆为授权信号与权衡失败信号：前者允许代理当前选择，后者要求给出一个具体、可撤回的推荐，而不是重复展示同一组选项。"
statement_type: METHOD
applies_when: "用户已经看过可理解选项但仍明确委托系统代选。"
does_not_apply_when: "用户只是问某个术语是什么意思，或没有作出委托。"
counterexample: "用户已委托，系统仍原样重发三选项。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 MM-S01-R02-01（L544-552）；「默认机制原则上在用户已看过一次可理解选项后触发」为本轮已认可的方法候选，尚未形成正式运行时规则。"
```

```yaml
elicitation_item_id: ELI-0122
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "显式委托分支成立且产品已配置可用默认策略。"
expert_statement: "默认生成顺序为：识别窄授权 → 读取版本化默认策略 → 宣告单一默认及依据／范围／否决权 → 记录临时来源状态 → 索取经任务解析器判定的高价值信息 → 事实齐备后再决定是否进入下游。"
statement_type: METHOD
applies_when: "显式委托分支成立且存在可用默认策略。"
does_not_apply_when: "无授权、无策略，或任务涉及不可逆经营决策（价格、折扣、库存处置、品牌战略等，应升级为人工决策或追加授权）。"
counterexample: "先生成完整成交脚本，再补写默认依据。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 MM-S01-R02-02（L554-562）；合法替代方案「推荐后等待用户明确确认」（专家二）同为答案族成员，其确认语义未裁决（已分流 PCR-01）。"
```

```yaml
elicitation_item_id: ELI-0123
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R02
source_situation: "临时默认已宣告，但任务所需上下文仍然缺失。"
expert_statement: "在目标处于临时默认期间，优先收集跨候选高复用、低返工的信息；具体字段必须由 Context Requirement Resolver 判定，不预设全局固定清单。"
statement_type: METHOD
applies_when: "临时默认已形成，但任务仍缺少上下文。"
does_not_apply_when: "字段只对某一尚未选定分支有价值，或收集成本显著。"
counterexample: "把成交链接规定为所有品牌认知任务的必填项。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "v3 包 MM-S01-R02-03（L564-572）；与 ELI-0110 同源于 R01 任务条件化依赖裁决，附录 A F4 已复核无残留。"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0124
source_session: DIYU-KE-S01-20260817-001
source_round: S01-R01
source_situation: "用户拒绝继续澄清，系统进入受限输出，是否可以给出任务结构模板或占位内容骨架。"
expert_statement: "用户拒绝澄清时的受限输出，可否在条件化选项菜单与待补信息清单之外，包含「不含商品声明的任务结构模板」与「明确标注占位符的内容骨架」——R01 专家B 断言禁止（理由：结构输出隐含目标选择，等于隐性替用户选目标），专家C 断言允许，同一条件下断言相反，未曾被显式裁决。"
statement_type: BOUNDARY
applies_when: "用户拒绝继续澄清且系统进入受限输出。"
does_not_apply_when: "用户已确认主目标，或已显式委托代选（走授权分支，见 ELI-0111 至 ELI-0123）。"
counterexample: "未经裁决即向拒答用户输出占位内容骨架。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "受限输出可降级：给出2–3个方案由客户选择"
provenance: UNRESOLVED
source_ref: "v3 包 UN-S01-05（L606-614）＋附录 A F1（L825）；V3.1 Founder 追加裁定已将外层定性为产品交互边界取舍。S05 专家 B／C 的「占位骨架」主张须并入本卡证据链（见《标准对齐复核结论》S05 一节②）。"
founder_question: "受限输出（用户拒答分支）可否包含不含商品声明的任务结构模板与标注占位符的内容骨架？——外层为产品交互边界取舍，随产品合同一并裁定；内嵌业务子问题「内容结构是否必然隐含商业目标选择，还是可通过占位声明做到目标中立」剥离为后续专家追问候选。裁决前 fail-closed 按 ELI-0102（只允许条件化选项菜单）执行。"
```

---

## 三、来源统计与残留说明

**卡数按 destination 分布（共 24 张：ROUTED 23 / PENDING 1）**

| candidate_destination | 卡数 | 卡号 |
|---|---|---|
| RULE_CANDIDATE | 9 | ELI-0103～0105、0113～0118 |
| KERNEL_METHOD | 6 | ELI-0108～0110、0121～0123 |
| CASE_REFINEMENT | 4 | ELI-0101、0102、0111、0112 |
| CONTRACT_PROPOSAL | 3 | ELI-0107、0120（失败概念候选）、0124（PENDING） |
| JUDGE_QUESTION | 2 | ELI-0106、0119 |

**provenance 分布（S01 特例：原样继承 v3 包逐卡标注）**：AI_PROPOSAL_FOUNDER_APPROVED 16（ELI-0102～0104、0111～0123）｜AI_PROPOSAL_FOUNDER_REVISED 6（ELI-0101、0105、0106、0108～0110）｜AI_PROPOSAL_REJECTED 1（ELI-0107）｜UNRESOLVED 1（ELI-0124）｜FOUNDER_ORIGINAL_JUDGMENT 0（v3 包两轮均明记未取得独立 founder_original_reasoning，不得从裁决结果反推）。

**未转卡内容及原因**

1. **7 项未决已分流产品合同队列 PCR-01（Intent 与交互合同），按编译规范第 4.3 条不转 ELI 卡**：UN-S01-01 正式商业目标枚举与附录 A/B 映射｜UN-S01-02 最大澄清轮数及停止结果｜UN-S01-03 QUICK 与 NEEDS_INPUT 边界｜UN-S01-R02-01 显式委托时默认策略来源／方向／版本化机制｜UN-S01-R02-02 用户一句「行」能否把临时默认升级为 CONFIRMED｜UN-S01-R02-03 无默认策略时回退受限输出还是阻断｜UN-S01-R02-04 ASSUMED_DEFAULT 及来源／范围／否决权的正式数据结构。收口包第三节对 S01 的判定为「不追问专家；进入 PCR-01」。其中 UN-S01-01 已获参考素材（排期主题 1 六类目标空间：新品曝光／库存激活／品牌建设／转化／节日内容／用户教育），仍须 PCR-01 与附录 A/B 核对后裁决，本文件不做映射。
2. **UN-S01-05 未被 PCR-01 列举**（PCR-01 七条不含受限输出骨架边界），且其内嵌业务子问题仍属专家层，故立为唯一 PENDING 卡 ELI-0124。
3. **R01 的 UN-S01-R01-01～04 不重复立卡**：01/02/04 已在 R02 收敛为 UN-S01-01/02/03（同一问题换号），03（显式授权下能否给候选推荐）已由 S01-R02 整轮解决，其结论落在 ELI-0111～0123，不再作为未决存在。
4. **两轮「已确认判断」清单（R01 十一条、R02 十一条）不逐条转卡**：按编译规范第 6 条与 E.10「不强制每条专家表述进仓库」，其实质均已由上列卡承载。同理 SESSION_CLOSEOUT 的九条关键判断、来源统计（approved 18／revised 6／rejected 4／unresolved 8）不另立卡。
5. **四条被 Founder 否决的内容不入卡**（转化／曝光／引流写入正式任务本体；候选失败概念直接升级为正式错误码；商品资料与成交承接规定为所有任务固定阻断项；候选硬规则直接写入生产 Rule Engine）——它们不是存续陈述，其约束效力已分别体现在 ELI-0107、ELI-0110、ELI-0123 的 does_not_apply_when／counterexample 与本文件控制声明中。
6. **两个非三值 provenance 的处理（供主审复核）**：编译规范第 2 条 provenance 只列三值，但第 3.2 条要求 S01「原样继承、不升不降」。ELI-0107 的 `AI_PROPOSAL_REJECTED` 与 ELI-0124 的 `UNRESOLVED` 均为项目会议协议（CLAUDE.md 第一节）已有的权威等级，非新造枚举；若改标为 FOUNDER_APPROVED／FOUNDER_REVISED 即构成规范第 3.3 条禁止的等级升级，故保留原值并在卡内 source_ref 说明其含义边界。
7. **附录 A 一致性审查五项发现的落点**：F1 → ELI-0124（PENDING）｜F2 入族限定已写入 ELI-0116 source_ref，不另立卡｜F3（专家A 内部张力）已被 R01 Founder 第 4 条修改消解，登记备查、无残留｜F4（跨轮固定清单冲突）已由 V2 归一并经 Founder 确认，落在 ELI-0110／0123｜F5（轻确认 vs 反射性「行」的风险权衡）属合法取舍差异，已路由 UN-S01-R02-02 → PCR-01。
8. **S01 无专家 TXT 原文文件**，编译规范第 3.4 条（TXT 忠实版优先）在本场无适用对象；《标准对齐复核结论》对 S01 的判定为「有效底稿」，未点名任何「硬规则级素材丢失」或「无源 REJECTED」条目，故本场无按第 3.5 条重新入卡或登记的内容。
