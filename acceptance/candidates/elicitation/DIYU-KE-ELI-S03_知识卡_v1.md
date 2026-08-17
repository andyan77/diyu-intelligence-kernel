# DIYU-KE-ELI-S03｜Business：商业冲突与商品角色 正式入库知识卡

```yaml
session_id: DIYU-KE-S03-20260817-001
rounds_compiled: [S03-R01, S03-R02]
source_files:
  - S-03.txt（专家原文，忠实版权威；专家一 L27-135／专家二 L136-368／专家三 L369-512）
  - S增补追问专家回答.md（S03-R02：专家一 L102-186／专家二 L604-751／专家三 L1360-1474）
  - DIYU-KE-S03-20260817-001_S03待入库候选包_v1.md（候选卡底稿）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S03-R02 QUESTION_CARD L286-328；PCR-03 L132-140）
  - DIYU-KE-S02-S07_原文对照审查总报告_20260817.md（S03 节 L95-101）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S03 节 L33-34）
ruling_basis: Founder（Faye）2026-08-17 对 S01–S08 候选包＋五张追问卡专家回答整体批准（"可以通过"），指示按 E 协议整理入库；本文件不修改任何既有文件，全部卡片为候选。
compiled_on: 2026-08-17
card_count_total: 38
card_count_routed: 35
card_count_pending: 3
```

---

## 一、入库知识卡（ROUTED）

### A. 方法层（KERNEL_METHOD）

```yaml
elicitation_item_id: ELI-0301
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "某款大衣库存 800 件、六周内要求有效激活、品牌禁止低价叫卖，被要求当场定是否主推"
expert_statement: "商业角色判断采用'压力与资格分离'：先识别库存、期限和管理压力属供给侧，再独立核验需求、履约、经济性、可讲性和品牌姿态，禁止由压力直接推出角色。800 件说明品牌多想卖它，不说明顾客多想买它。"
statement_type: METHOD
applies_when: "库存量、期限或管理压力容易推动系统过早选定商品角色"
does_not_apply_when: "任务不涉及商品资源优先级；或需求侧证据已独立成立"
counterexample: "只因库存深就确认主推"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S03-R01-01；S-03.txt 专家一 §2 Step1 L59、专家二 §1 L153、专家三 §一 L373"
```

```yaml
elicitation_item_id: ELI-0302
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "800 件深库存成因未知，被要求直接给角色结论"
expert_statement: "深库存至少区分三种本质不同的成因：备货型（刚进入销售周期、无滞销证据、候选资格完好）、滞销型（已真实销售但需求不足，主推等于放大已被验证失败的东西，除非病因找到且窗口内可修）、结构型（总量大但集中于难售尺码颜色或不可正常承接，内容做得越好伤得越重）。三类局面不能采用同一主推判断。"
statement_type: METHOD
applies_when: "库存总量较大但形成原因未知"
does_not_apply_when: "库存成因和可售结构已经确认"
counterexample: "把刚到货的正常备货直接判为滞销清理款"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S03-R01-02；S-03.txt 专家一 §1(1) L35"
```

```yaml
elicitation_item_id: ELI-0303
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "深库存商品是否够格获得主推级资源"
expert_statement: "深库存商品的主推资格至少五类核验：①需求证据（动销史证明正价卖得动／病因已识别且窗口内可修／低资源试探拿到真实需求信号）；②履约结构（主流尺码颜色有货、承接通畅）；③经济性（在允许价格政策内毛利撑得起投入）；④可讲性（有非价格的'现在理由'可讲＋实拍达到最低画面集）；⑤姿态相容（劝购强度与禁叫卖边界共存）。任一否决项坐实即停止主推路线。**该五条的完备性专家自评为 MEDIUM——是否存在品类特有的第六条，待真实案例校准，不得按定论使用。**"
statement_type: METHOD
applies_when: "商品准备获得明显高于普通商品的内容、渠道和运营资源，并承担主要经营责任"
does_not_apply_when: "仅进行低资源观察或内部资料采集；若项目中'主推'只表示偶尔增加露出，资格门槛须重新校准（专家一/专家二同标为 assumption）"
counterexample: "仅因视觉好看就跳过经济性和承接核验"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S03-R01-03（含审查报告点名的 MEDIUM 置信度补回）；S-03.txt 专家一 §1(4) L41-49、§9 L123。族内差异：专家二列九条（S-03.txt L232-245，含'激活目标明确'与'有相对其他商品更合理的资源优先级'）、专家三列六条（L445-467，含'品牌认可六周目标并有可衡量标准'）；其中'成功口径是否属资格前置'为 2:1 分歧，路由 PCR-03，见第三节"
```

```yaml
elicitation_item_id: ELI-0304
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "接手局面后第一步先看什么：库存数量、商品图片还是视频内容"
expert_statement: "三份回答一致否定同三个起点：**不先看库存总量**（是压力表不是诊断书，报问题多大不报问题是什么，且该数已知、再盯不产生新信息，总量大反而可能是滞销信号）；**不先看商品图片**（只回答好不好看，回答不了为什么还剩 800 件，容易用主观审美替代商业判断）；**不先做视频选题**（渠道与执行层，先定内容再倒推角色＝先开枪后画靶，容易返工）。起点必须落在需求侧证据与经营口径一侧。"
statement_type: METHOD
applies_when: "商品角色/资源优先级判断的起点选择"
does_not_apply_when: "任务本身只要求视觉评估或内容排期，不含角色决定"
counterexample: "先设计六周选题脚本，再论证这款为什么该主推"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §1(1) L35、专家二 §2 L163-183、专家三 §二 L380-402（3/3 共识，审查报告点名候选包只保留了结论未保留判断结构）"
```

```yaml
elicitation_item_id: ELI-0305
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "确定诊断顺序后，逐层核验什么"
expert_statement: "诊断五层顺序：动销与成因 → 价格毛利与允许的价格动作空间（禁低价之下还能动什么，属品牌政策必须问来、不能猜）→ 库存结构与成交承接 → 商品与画面表现 → 受众与账号基础。渠道已定不改变该顺序——渠道是'在哪说'，代替不了'凭什么卖'。"
statement_type: METHOD
applies_when: "深库存商品的角色核验；专家一自荐为方法候选"
does_not_apply_when: "族内起点存在差异：专家二主张第一步先定义'六周激活成功'的数量与结果口径（S-03.txt L163-172），专家三主张动销/退货/顾客反馈与成功数量要求同时索要（L384-385）；三份在'不先看总量、不先看图片、不先做视频'上一致（见 ELI-0304），起点先后差异属 PCR-03 第 1 项下游，本卡不作裁决"
counterexample: "跳过价格政策直接进入内容表现评估，导致方案落在被禁手段上"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §1(1) L35、§10 possible_module_method L133（审查报告点名'专家一自荐的诊断五层顺序方法卡'整条消失，据原文补卡）"
```

```yaml
elicitation_item_id: ELI-0306
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "只盯这一款大衣决定角色，未看同批其他商品"
expert_statement: "主推是组合选择，不能只看单品库存：须与同批其他商品比较机会成本，再决定它是主推、辅助露出、搭配商品，还是不进入本轮内容重点；'有相对其他商品更合理的资源优先级'本身就是一条主推资格条件。若同批存在强商品，组合出货是深库存的经典出路，但同批商品的库存与表现属必须补齐的事实，不得用未知商品去救未知商品。"
statement_type: METHOD
applies_when: "多商品在同一窗口竞争有限内容位与运营资源"
does_not_apply_when: "同批商品的库存与表现事实未回传时，不得据此直接选定组合路线（只能列为核验后的合法候选）"
counterexample: "只因该单品库存最深就把六周内容位全部给它，从未比较同批其他商品的贡献"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家二 §2 Step4 L197-198＋资格表第 8 行 L244、专家三 §七-4 L506、专家一 option C L89＋§8 补齐清单第 7 项 L328（审查报告点名的 2/3 共识'同批机会成本比较'整条消失，据原文补卡）"
```

```yaml
elicitation_item_id: ELI-0307
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "主推资格核验若不通过，商品是否就此出局"
expert_statement: "角色门槛是阶梯而非开关：主推需过五条资格；辅助露出的门槛只是'不减分'；搭配角色只需'给主角加分'。因此资格核验失败不等于商品出局，是角色降级——这也是'候选'状态安全的原因：五条查完，角色自动清楚。"
statement_type: METHOD
applies_when: "商品未通过主推资格核验，需要决定其后续处置"
does_not_apply_when: "商品命中断码不可修、无承接、退货品质风险等否决项——此时不是降级问题（见 ELI-0314）"
counterexample: "五条资格差一条即宣布商品完全退出本轮内容"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §1(4) L51（候选包只保留'辅助/搭配'名称，丢失两级门槛口径，据原文补卡）"
```

```yaml
elicitation_item_id: ELI-0308
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "证据不足但窗口只有六周，等资料还是先动手"
expert_statement: "时间紧张时采用'核验与行动同构'：调阅经营数据并索要成功口径、按最低画面集实拍采素材、承接自查修通、发一条低资源试探内容读需求信号、盘点账号基础——这些动作的产出恰好就是资格条件的判据来源，对任何最终角色都不白做，因此零返工。窗口须设角色决定点：不能无限期观察，窗口内必须作出主推或非主推决定。'抢时间'的正确形态是并行，不是跳步。"
statement_type: METHOD
applies_when: "角色未定、证据不足但窗口有限"
does_not_apply_when: "已出现必须先解决的品质、合规或履约硬风险"
counterexample: "一边完全停工等资料，一边在最后一周仓促押注；或先批量生成内容再补商业判断"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S03-R01-04；S-03.txt 专家一 §1(6) L55、专家二 §8 '不会造成明显返工的动作' L336-343、专家三 §七 L499-511；'不能无限期观察'补自专家三 §四-2 L429。注：专家一给出的'六周切段＋第一周末为决定点'属时间结构候选，其中'成功口径未定义时可否启动整窗'为 2:1 未决（PCR-03 第 1 项），本卡不构成启动授权；'第一周末'为案例级数值不入通用方法"
```

```yaml
elicitation_item_id: ELI-0309
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "品牌拿不出历史动销、毛利、退货数据"
expert_statement: "可用低资源试探取证：发一条受限形态的试探性商品理解内容，不押注不承诺，只验证点击、咨询、加购等早期信号，评论区反应就是最便宜的需求侧读数，并辅以现场盘库与承接检查。但其效力有边界——测试规模或受众错误时，结果不能代表主推潜力；单条内容播放量高本身不是需求证据。"
statement_type: METHOD
applies_when: "小商家或新商品缺少可靠历史经营数据，但窗口已开始"
does_not_apply_when: "完整经营数据可得；该路径是否成为**正式**降级核验路径属产品合同问题（PCR-03 第 3 项），本卡不作正式化"
counterexample: "因无历史数据就永久拒绝判断，或反过来完全凭感觉定主推；把一条试探内容的高播放当成动销证据"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §1(6) L55、专家二 option L254-258（效力边界 risks 行）、专家三 §七-5 L507-508"
```

```yaml
elicitation_item_id: ELI-0310
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "同一商品库存从 800 件变成 20 件"
expert_statement: "库存深度决定战役规模与内容节奏：深库存需要分段验证和持续承接，浅库存应限制投入、避免内容制造无法兑现的需求（风险方向从'卖不掉'掉头为'内容起量但没货卖'）；库存深度不决定事实标准、承接核验和品牌边界——不因量小放松诚实。"
statement_type: METHOD
applies_when: "同一商品库存数量发生明显变化，需重定内容节奏与资源规模"
does_not_apply_when: "另有独立品牌建设目标足以支撑长期投入"
counterexample: "20 件库存仍按 800 件设计六周集中战役"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S03-R01-05；S-03.txt 专家一 §6-B L95、专家二 §6 L275-280"
```

### B. 规则层（RULE_CANDIDATE）

```yaml
elicitation_item_id: ELI-0311
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "库存 800 件被当作'必须主推'的理由"
expert_statement: "供给侧压力只能提高评估优先级，不能单独赋予商品任何主推或其他商业角色资格。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "角色建议主要由库存量、期限或管理压力驱动"
does_not_apply_when: "同时存在可追溯的需求、经济性、履约和商品证据"
counterexample: "`inventory=800` 因而自动输出'主推款'"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S03-R01-01；S-03.txt 专家一 §7 forbidden_outcome'压力定角色' L103、专家二 §7 L291-293（failure_label_candidate: NOT_ASSIGNED，专家立场保留）、专家三 §一 L373"
```

```yaml
elicitation_item_id: ELI-0312
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "输出只写'建议作为引流款'而不说明依据"
expert_statement: "商品角色建议必须同时给出资格条件、证据来源和适用边界；角色名不得单独作为商业判断结论。只写角色名而不说明为什么，是没有完成商业判断。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "输出对具体商品使用主推、辅助、搭配、引流、利润或清理等角色语言"
does_not_apply_when: "仅引用现行合同定义而不对具体商品作角色建议"
counterexample: "'建议作为引流款'，但没有说明需求、价格、库存和承接依据"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S03-R01-02；S-03.txt 专家一 §10 possible_hard_rule(b) L133。角色词表本身（Hero/Support/Traffic/Profit/Clearance 的正式定义与迁移）不在本卡范围，引 PCR-03 第 4 项"
```

```yaml
elicitation_item_id: ELI-0313
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "品牌禁止低价叫卖，方案随即改为'只能做品牌故事'"
expert_statement: "一个商业手段被品牌禁止，只能排除该手段，不能自动选定另一条路线；替代路线必须有独立证据和取舍说明——品牌故事路线对'六周激活'是否有效，需要它自己的论证，不能靠禁令反推上位。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "品牌禁止折扣、叫卖、某渠道或某种表达方式"
does_not_apply_when: "品牌同时明确指定了合法替代路线"
counterexample: "禁止低价，因此自动转成品牌故事主推"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S03-R01-03；S-03.txt 专家一 §7'规则定路线' L105、§10 possible_hard_rule(c) L133、专家三 §一 L374"
```

```yaml
elicitation_item_id: ELI-0314
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "库存压力很大，是否存在无论如何都要拒绝主推的情形"
expert_statement: "主推决定前必须排除下列否决情形，任一坐实即否决：①主流尺码或颜色严重断裂且不可修复（需求进来无处落）；②已验证滞销且病因不可修或修不起；③无有效成交承接或无法正常履约；④退货、品质或售后风险未排除（主推等于放大退货，库存问题升级成现金流加口碑双重问题）；⑤在允许政策内经济性不成立；⑥唯一可用的紧迫理由只能依靠品牌禁止的低价或变相清仓话术——此时正确动作是换角色或把'重谈边界'作为建议提交品牌，重谈是品牌决策，专业人员只能提出。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "商品将获得主推级资源并承担经营责任"
does_not_apply_when: "仅进行低风险内部观察，不扩大需求"
counterexample: "明知主流尺码不可售仍投放主推内容"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S03-R01-04；S-03.txt 专家一 §1(5) L53、专家二 §7 L295-305（全部 NOT_ASSIGNED）、专家三 §六 L471-493"
```

```yaml
elicitation_item_id: ELI-0315
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "商品与同类高度同质化，在品牌边界内找不到任何值得表达的点"
expert_statement: "'商品没有可识别差异点'构成主推否决：版型、面料、设计、场景或搭配上找不到值得放大的真实点，视频内容就无法讲清价值，只能变成'有一件大衣'——此时内容只能靠虚构卖点成立，主推是错误决定。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "已核验商品在品牌边界内不存在任何可表达的真实差异点（可讲性为零）"
does_not_apply_when: "仅是'视觉/上镜普通'但存在非视觉的真实购买理由——该情形已由 S03-R02 收敛为不构成商业否决，见 ELI-0329；本卡只覆盖'一个可讲的真实理由都没有'"
counterexample: "把'不够惊艳'当成'没有差异点'从而否决一个动销成立的商品"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家三 §六-4 L484-485、§五-4 L458-459；专家一'可讲性'资格条件 L48（审查报告点名的否决项遗漏，据原文补卡；与 R02 收敛结论的边界已在 does_not_apply_when 划清）"
```

```yaml
elicitation_item_id: ELI-0316
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "品牌没给'六周有效激活'的数量或经营口径"
expert_statement: "成功没有数量定义时，不得对窗口作整体结果承诺；若品牌既不给成功定义也拿不出任何数据，改为'试探—读数—滚动决定'，每段只承诺下一段。激活不等于清仓：正价卖出一部分＋建立持续动销＋为余量找到出路结构都是激活的合法形态，定义权在品牌。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "经营目标缺少可衡量口径，但窗口已经开始"
does_not_apply_when: "品牌已明确成功口径。**注意**：族内更严立场存在——专家二把'激活目标明确'、专家三把'品牌认可六周目标并有可衡量标准'直接列为主推资格条件（即口径缺失时主推资格不成立，2:1），专家一主张仅不作整窗承诺；本卡只登记三份共同的下限，'口径缺失是否禁止启动整窗战役'路由 PCR-03 第 1 项，未裁决"
counterexample: "把未定义的'有效激活'擅自填成'六周清完 800 件'，据此制造过度紧迫的方案"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §10 possible_hard_rule(d) L133、§8'必须升级暂停' L117、§1(2) L37；专家二资格表首行 L235、专家三 §五-6 L464-466（审查报告点名的硬规则级素材遗漏，据原文补卡）"
```

```yaml
elicitation_item_id: ELI-0317
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "不降价，但改用'最后 X 件''错过再无''手慢无'制造紧迫"
expert_statement: "品牌禁止的是'叫卖姿态'，不只是降价动作——因此连变相话术也不可用；不说降价但天天喊'最后 X 件''错过再无'属姿态违禁，规则名亡实亡。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "品牌边界为'禁止低价叫卖'，方案需要制造购买紧迫感"
does_not_apply_when: null
counterexample: "以'库存紧张'话术替代降价，实现同一种叫卖姿态"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §1(2) L37、§7'变相叫卖' L111。**忠实版**：候选包在该禁令后加挂的豁免口'且没有对应真实库存结构依据'系编译对专家一未消解内部矛盾（§7 无例外 vs §6-B'真实的仅 20 件是合法的非价格紧迫感' L95）的单方裁决，审查报告 S03 第 5 条点名，本卡不予采用；该例外问题另立 ELI-0338（PENDING）"
```

### C. 判分层（JUDGE_QUESTION）

```yaml
elicitation_item_id: ELI-0318
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "人工评审一份主推/资源优先级建议"
expert_statement: "首先检查结论依据来自需求侧证据还是仅来自库存和期限压力；只引用供给侧压力的主推建议应判为专业判断不足。"
statement_type: BOUNDARY
applies_when: "人工评审主推或资源优先级建议"
does_not_apply_when: "任务只要求库存风险提示，不要求角色决定"
counterexample: "'库存很多，所以一定要重点推广。'"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S03-R01-01；S-03.txt 专家一 §10 possible_judge_calibration 第 1 问 L133"
```

```yaml
elicitation_item_id: ELI-0319
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "输出用发布条数或播放量宣称库存已激活"
expert_statement: "合格的商业判断必须区分'激活'与'清仓'，并说明成功口径由谁定义；把内容发布、播放或互动量直接等同于库存激活，应判为目标偷换。"
statement_type: BOUNDARY
applies_when: "输出讨论库存激活、动销恢复或窗口经营结果"
does_not_apply_when: "用户已经明确定义内容测试为唯一结果"
counterexample: "发布六条视频即宣称完成库存激活"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S03-R01-02；S-03.txt 专家一 §7'激活清仓等式' L109、专家二 §7 L311-313（NOT_ASSIGNED）"
```

```yaml
elicitation_item_id: ELI-0320
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "角色未定但已开始动手，评审这些先行动作是否专业"
expert_statement: "检查先行动作能否同时为多个合法角色提供证据；只服务于尚未确认的单一路线、失败后全部报废的动作，应视为返工风险（不同构＝有返工隐患）。"
statement_type: BOUNDARY
applies_when: "角色尚未确定但时间窗口有限"
does_not_apply_when: "角色已由充分证据确认"
counterexample: "在角色未定前批量拍摄六周成交脚本"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S03-R01-03；S-03.txt 专家一 §10 possible_judge_calibration 第 3 问 L133"
```

```yaml
elicitation_item_id: ELI-0321
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "输出给出一组角色分配：A 主推、B 辅助、C 利润款"
expert_statement: "角色建议出现时，应检查是否说明'为什么这个商品适合该角色、什么条件变化会失去该角色'，以及是否交代了与同批商品的取舍；只罗列角色名属于表面完整、实质空白。"
statement_type: BOUNDARY
applies_when: "输出包含一个或多个商品角色"
does_not_apply_when: "仅做数据采集计划"
counterexample: "'A 是主推，B 是辅助，C 是利润款'，没有任何依据"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S03-R01-04；S-03.txt 专家二 §10 possible_judge_calibration L366（'替代角色取舍'口径据原文补回）"
```

```yaml
elicitation_item_id: ELI-0322
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "评审一份在'禁止低价叫卖'边界下写出的方案"
expert_statement: "评审第二问：被禁的手段有没有以变相话术回流——检查方案是否在不降价的表面下重新使用了被禁的叫卖姿态。"
statement_type: BOUNDARY
applies_when: "品牌存在明确禁用手段，评审其下游内容与话术方案"
does_not_apply_when: "品牌无相关禁令"
counterexample: "方案未降价，但通篇'最后机会''错过再无'，评审只核对价格未核对姿态"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §10 possible_judge_calibration 第 2 问 L133（候选包三问只落两问，据原文补卡）"
```

```yaml
elicitation_item_id: ELI-0323
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "评审'现在就定主推、边推边验'类提案"
expert_statement: "评审'边推边验'提案时，代价计算不能只算内容返工：断码、滞销、无承接任何一条事后坐实，报废的是账号连续多条向粉丝推一个买不到或不想买的商品——损害的是账号信用与流量资源，不只是素材。核验只要几天且与行动完全重叠时，跳过它省下的时间买不回押错的代价。"
statement_type: BOUNDARY
applies_when: "评审以'时间紧'为由跳过资格核验的方案"
does_not_apply_when: "核验成本确实远高于押错代价（须显式论证，不得默认）"
counterexample: "评审只比较'省下一周'与'多拍一批素材'，不计入账号信用损耗"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §5 option B L87、专家三 §三 L416（据原文补卡）"
```

### D. 案例层（CASE_REFINEMENT）

```yaml
elicitation_item_id: ELI-0324
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "库存 800 件、六周激活、禁止低价叫卖的大衣局面（商品夹具未回传）"
expert_statement: "该案例的合法答案族：拒绝立即定主推，将商品列为优先核验候选，并说明成功口径、库存成因和主推资格尚未得到证明；失败判据＝压力定角色、规则定路线、内容倒推商业、激活清仓等式、替品牌补写目标数字任一出现。"
statement_type: BOUNDARY
applies_when: "输入只有库存压力、期限和品牌边界，缺少需求、经济性、履约和商品证据"
does_not_apply_when: "主推资格所需证据已经完整且无否决项"
counterexample: "因库存深直接制定六周主推内容战役"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S03-R01-01；S-03.txt 专家一 §10 possible_case_refinement L133、专家二 §1 L143-153、专家三 §一 L371"
```

```yaml
elicitation_item_id: ELI-0325
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "单变量反事实：实拍确认商品视觉与上身表现普通"
expert_statement: "视觉普通确认时，不得用夸张语言把它包装成内容主角；应重新判断它是否仍有经营价值，以及是否适合通过搭配、场景或服务内容间接推动。"
statement_type: BOUNDARY
applies_when: "视觉表现普通，但其他经营条件可能成立"
does_not_apply_when: "商品视觉和内容表现本身是经证据确认的优势。**本条的最终版由 S03-R02 三专家收敛给出**（ELI-0328/0329/0330/0331）：经营重点与镜头主角互不自动推导，视觉普通永不单独构成商业否决"
counterexample: "用'高级、显瘦、必入'等空洞形容强行支撑六周单品主角路线"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S03-R01-02；S-03.txt 专家一 §6-A L93、专家二 §6 L268-273"
```

```yaml
elicitation_item_id: ELI-0326
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "单变量反事实：库存从 800 件变为 20 件"
expert_statement: "不应沿用深库存六周战役；内容节奏和资源投入必须与可售供给匹配，20 件适合单条内容自然售罄，做成六周主推反而制造缺货失望。诊断顺序、承接核验、禁低价约束与事实纪律照旧。"
statement_type: BOUNDARY
applies_when: "库存深度是唯一改变变量"
does_not_apply_when: "仍存在其他独立战略目标需要长期内容投入"
counterexample: "为 20 件库存连续六周集中推广，导致需求起来后无货可售"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S03-R01-03；S-03.txt 专家一 §6-B L95、专家二 §6 L275-280。专家一同处主张'真实的仅 20 件是合法的非价格紧迫感'，与 ELI-0317 的边界关系未消解，另见 ELI-0338（PENDING）"
```

```yaml
elicitation_item_id: ELI-0327
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "单变量反事实：品牌从禁止低价叫卖改为允许一次有边界的限时优惠"
expert_statement: "只能把它视为新增一个工具，不是新的商业逻辑：优惠只解决'现在理由'这一项，救不了断码、无承接、退货问题；仍须核验需求、库存结构、毛利、承接、品质和品牌姿态；且必须先把'一次''有边界'落成具体幅度、时长、范围，不得自行展开成'可以促销了'；允许限时优惠≠允许叫卖腔。"
statement_type: BOUNDARY
applies_when: "品牌价格政策从完全禁止变为一次受限授权"
does_not_apply_when: "优惠幅度、时长和范围仍未明确——此时不能进入机制设计"
counterexample: "一听到'允许优惠'就自动确认主推并设计清仓促销"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S03-R01-04；S-03.txt 专家一 §6-C L97、专家二 §6 L282-287"
```

### E. 追问轮 S03-R02 收敛结论

```yaml
elicitation_item_id: ELI-0328
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "其他经营条件全部成立（真实动销、码色可售、毛利成立、承接履约正常、符合禁低价边界、六周目标明确），只有实拍确认外观与上身表现普通"
expert_statement: "'经营上是否重点推动'与'内容中是否担任镜头主角'是两个独立决定，任何一方不得自动推导另一方。本局面三份回答一致：经营重点维持（支撑重点推动的全部依据本轮一项未变，'上镜普通'改变的是用什么方式推，不是该不该推），镜头主角撤下（画面普通的商品连续单独出镜只有两种结局：内容数据差，或团队被迫用无依据形容词包装它）。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "商品经营价值与视觉内容价值不一致"
does_not_apply_when: "两者方向一致且无歧义。是否把两者正式拆成两个角色维度、如何映射 Hero／Support 等现行词表，属产品合同问题（PCR-03 第 2/4 项），本卡不作正式化"
counterexample: "因为它是经营重点，就让每条内容反复使用相同商品画面（专家二明列为禁止结果）；或因为不上镜就撤掉经营投入"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（S增补追问专家回答.md 专家一 L104-145、专家二 L610-628＋§10 L750、专家三 L1389-1400＋§10 L1474 possible_hard_rule 逐字'经营重点与镜头主角为两个独立决定，任何一方不得自动推导另一方'）"
```

```yaml
elicitation_item_id: ELI-0329
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "视觉普通是否足以把商品从经营重点上撤下来"
expert_statement: "视觉普通本身永远不单独构成商业否决——它只是内容限制。否决只能来自实证，两条路径：①窗口内用诚实内容与既有承接手段认真跑过后，动销节奏仍明显达不到激活要求，且持续投入的内容与人力成本吃掉该品可贡献的毛利（此时降的是'重点推动'这个决定本身：缩目标或换处置路径）；②实拍暴露的不是'镜头普通'而是商品本身的问题（上身表现差到与既往动销证据矛盾），此时回头重审需求证据是否仍然成立。专家二同侧补充的实证信号：真实动销下降、退货或不满上升、资源投入失衡，或商品只能靠误导表达才能继续推动；专家一同侧补充：需要大量修图滤镜才能成立、退货投诉大量指向'实物和视频差距大'、没有场景搭配服务等手段可以弥补。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "商品视觉表现普通而经营证据成立，需判断是否继续重点推动"
does_not_apply_when: "商品在品牌边界内一个可讲的真实理由都没有（可讲性为零）——该情形另由 ELI-0315 覆盖，不属'仅视觉普通'"
counterexample: "仅凭'不上镜'否决一个动销、毛利、履约都成立的商品"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 L1367/L1402 逐字'视觉普通本身永远不够格否决'；专家二 L726'不能仅凭不上镜否决商品'；专家一 L185-186'只有它开始侵蚀真实成交和品牌信任时，才构成商业否决'）。否决线的数值门槛未提供，见 ELI-0336（PENDING）"
```

```yaml
elicitation_item_id: ELI-0330
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "商品退出镜头主角位后，六周内容怎么安排才不虚构优点"
expert_statement: "四类替代内容安排，商品在每类中都保留成交路径：①搭配内容——镜头主角是整套搭配，它作为基础件出现，链接与讲解指向它；②场景内容——镜头主角是人与真实使用场景，展示'真实生活怎么穿'，普通反而可信；③答疑内容——镜头主角是店长回答真实顾客问题，直接服务已在考虑它的人，促成咨询；④事实内容——尺码、版型、不同身高上身对比，普通商品最需要的'看懂型'信息。这些安排都不依赖视觉夸赞，而更接近购买决策。"
statement_type: METHOD
applies_when: "商品经营价值成立但不适合独立承担镜头吸引力"
does_not_apply_when: "账号被限定为单品主角展示一种内容形态时不成立（专家三明列为 assumption）；每类安排都需真实素材：真实顾客问题、真实存在且适配的搭配商品或场景、真实服务资料，缺素材时属 INSUFFICIENT_CONTEXT"
counterexample: "宣布'做搭配内容'但搭配商品是虚构的；或让搭配商品抢走经营重点"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 §1 四类表 L1393-1399；专家二 §5 三个 option L657-673＋§8 L718；专家一 L140-167 四项）"
```

```yaml
elicitation_item_id: ELI-0331
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "宣布商品'当配角'之后，它的经营责任怎么办"
expert_statement: "'配角'只指镜头位置，不指经营位置：每种内容结构里它都必须是购买路径明确指向的商品——挂它的链接、答它的问题、给它的库存导流。宣布'当配角'却不给成交路径，等于退出经营，名实不符。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "商品从镜头主角位撤下但仍是经营重点"
does_not_apply_when: "商品同时也已退出经营重点（此时是资源重分配，不是配角安排）"
counterexample: "内容改成搭配/场景，但链接、答疑与导流全部指向别的商品"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 L1400 逐字＋§7 failure ROLE_WITHOUT_SALES_PATH L1457-1459；专家二 §5 risks'不能让搭配商品抢走经营重点' L667；专家一 §4'商品卡、尺码表和价格信息…把可售信息讲清楚' L166-167）"
```

```yaml
elicitation_item_id: ELI-0332
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "评审'普通但卖得动'这一主张时，什么算证据什么算自我安慰"
expert_statement: "有效证据：在正常品牌政策下产生真实成交；动销不是由一次异常低价造成；主流尺码颜色都有实际流动；毛利和退货结果可接受；成交能够正常履约；结果在一定时期或多次经营中重复出现；咨询转化真实存在。不是充分证据：员工认为'应该好卖'；库存很深；单条内容播放量高；少数顾客口头称赞；为库存压力寻找理由；'曝光了总会卖''买家应该都满意'。另需注意：商品究竟赢在哪些非视觉维度，须回查成交与咨询记录确认，不由内容自行认定，更不由内容补写。"
statement_type: BOUNDARY
applies_when: "评审以'商品普通但卖得动'为前提的经营主张"
does_not_apply_when: "商品尚无任何真实成交历史（此时属 R01 的需求证据核验，见 ELI-0303）"
counterexample: "用一条视频的高播放量证明商品需求成立"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家二 §6 证据/非证据两列 L677-692；专家三 L1372 证据分级＋L1389'须回查成交与咨询记录确认'；专家一 L118-126 经营证据六项）"
```

```yaml
elicitation_item_id: ELI-0333
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "答疑型内容里，店长怎么讲一件外观普通的大衣"
expert_statement: "店长可用经验陈述形态直接承认普通并给出真实卖点，示例：'它不是那种一上身就很有冲击力的衣服，但很多顾客看中的是它实穿、版型稳、好搭。'——**专家自带限定：如果这些卖点有真实依据，就不是形容词，而是经验陈述**；镜头展示真实信息，不回避普通。"
statement_type: BOUNDARY
applies_when: "答疑/店长建议型内容，商品视觉普通且卖点有可回查的真实依据"
does_not_apply_when: "卖点无真实依据时该句退化为形容词包装，直接违反禁令。**并且**：该示例含顾客侧陈述（'很多顾客看中的是它实穿'），店长转述顾客侧正面样例的可用性在 S05 尚未收敛——审查报告记录 S05 两位专家对同型句一判可信、一判一票否决，历史证言最低材料集合亦为 S05 未决项（PCR-05）；本卡不越 S05 边界，该句形态待 S05 裁决后方可作为可用范例"
counterexample: "把'很多顾客看中它实穿'写进脚本，但门店无任何咨询或复购记录支撑"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S增补追问专家回答.md 专家一 S03-R02 §替代内容安排-3 L159-164（含其自带的'须有真实依据'限定，逐字保留）"
```

```yaml
elicitation_item_id: ELI-0334
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "'普通'是制作方的镜头判断，观众反应尚未实测"
expert_statement: "合法替代路径：先实测再换位——用 1–2 条诚实的单品内容试观众真实反应，再决定是否撤主角位。理由是'普通'目前只是制作方判断，小成本验证在专业上站得住，用数据而非判断定角色可避免误撤；代价是占用窗口开头 1–2 个内容位，若明显失败则损失窗口早期时间。专家在窗口紧的前提下把'直接换位'列为主候选，同时声明实测方案同样合法，取舍权在 Founder。"
statement_type: METHOD
applies_when: "窗口时间允许，且'视觉普通'结论来自制作方判断而非观众数据"
does_not_apply_when: "窗口过紧，或试探内容需靠夸张形容词才能成立"
counterexample: "把'实测'做成六周主推级投入，实质是先押注再找理由"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S增补追问专家回答.md 专家三 S03-R02 §5 L1431-1436"
```

```yaml
elicitation_item_id: ELI-0335
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "本场专家为三种禁止结果新命名了失败标签"
expert_statement: "新失败标签候选三项：`UNSUPPORTED_CLAIM_INFLATION`（用夸张形容词把'普通'包装成卖点继续扛镜头）、`INVENTORY_FORCED_HERO`（'库存深所以必须当主角'式推导——库存深度只支撑经营优先级，不产生镜头适配性）、`ROLE_WITHOUT_SALES_PATH`（宣布当配角但不给成交路径）。**新标签候选，须走 B.8.1 覆盖审查后方可入册，不得私加，也不得往既有标签塞新语义。**同场另两位专家的立场须一并保留：专家二 S03-R02 三条禁止结果全部显式标注 `NOT_ASSIGNED`，专家一 S03-R01 明写'描述性命名，不提请入册'。"
statement_type: FAILURE_MODE
applies_when: "对本场禁止结果做失败标签映射时"
does_not_apply_when: "B.6 既有标签已能覆盖该失败语义（须先做覆盖审查）"
counterexample: "把三个新名字直接写进 Rule Engine 或考卷标签表"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S增补追问专家回答.md 专家三 §7 L1449-1459；专家二 §7 L703-713（NOT_ASSIGNED×3）；S-03.txt 专家一 §7 L101"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0336
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "视觉普通的商品继续重点推动，但'跑到什么程度算不达标'没有数值"
expert_statement: "六周激活的达标节奏数值与放弃线未在卡内提供，专家明确声明'不应由我设定'；否决线因此只能给结构、无法量化（该部分自评置信度 MEDIUM）。同一缺口在专家一处表现为'点击、停留显著低于阈值'——阈值同样未定。"
statement_type: BOUNDARY
applies_when: "需要判定'诚实内容认真跑过后仍达不到激活要求'是否成立"
does_not_apply_when: "品牌已给出达标节奏与放弃线"
counterexample: "由执行侧自行设定放弃线，等于替品牌决定不可逆经营承诺"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "数字属品牌运营侧；数字未定不作整窗承诺；系统不打包票、自动降级"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛残留（专家三 需要 Founder 决定第 1 项 L1378、§8 L1463、§9 L1469；专家一 L173-174）"
founder_question: "六周激活的达标节奏数值（每周/累计多少）与放弃线由品牌定——请给出数值口径，或裁定由谁在什么时点给。"
```

```yaml
elicitation_item_id: ELI-0337
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R02
source_situation: "搭配/场景/答疑/事实四类内容实测后仍带不动咨询"
expert_statement: "四类诚实内容认真跑过后仍带不动咨询时，是降低六周激活目标还是改换处置路径（如退出本轮重点、转其他渠道），专家明确路由给 Founder，不代为选择；同侧表述见专家二的 HUMAN_DECISION_REQUIRED——经验证的边际贡献已低于其他商品或渠道时，需要决定是否重新分配资源。"
statement_type: BOUNDARY
applies_when: "替代内容安排已实测且结果不佳，窗口仍在进行"
does_not_apply_when: "尚未实测，或经营证据本身已被推翻（此时走 ELI-0329 第二条路径重审需求证据）"
counterexample: "执行侧自行下调品牌设定的经营目标"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "系统自动路由降级，不需逐项人裁"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛残留（专家三 需要 Founder 决定第 2 项 L1379、§8 L1465；专家二 §8 HUMAN_DECISION_REQUIRED L723-724）"
founder_question: "四类内容实测后仍带不动咨询时，默认动作是降目标还是换处置路径？由谁决定、在窗口第几周决定？"
```

```yaml
elicitation_item_id: ELI-0338
source_session: DIYU-KE-S03-20260817-001
source_round: S03-R01
source_situation: "禁止叫卖姿态，但库存确实只剩 20 件——这个真实事实能不能说"
expert_statement: "专家一原文内部存在未消解的两处：§7 将'最后 X 件／错过再无'一律列为变相叫卖（无例外），§6-B 又称'真实的仅 20 件是合法的非价格紧迫感（本测试条件下有据可依的事实声明）'。真实库存事实能否用作紧迫感表达、与'禁止叫卖姿态'边界的关系，专家未消解，编译不得代裁。"
statement_type: BOUNDARY
applies_when: "品牌边界为禁止低价叫卖，而库存结构事实本身具备紧迫含义"
does_not_apply_when: "库存结构事实未经盘点核实——无论边界如何裁决，虚构库存紧迫都被禁止（三份一致）"
counterexample: "候选包直接为禁令加挂'且没有对应真实库存结构依据'的豁免口，选宽松侧代品牌裁决（审查报告 S03 第 5 条点名）"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "紧迫感话术一律不说（含真实库存的紧迫表达）"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-03.txt 专家一 §7 L111 vs §6-B L95（同一专家内部矛盾，忠实登记，不作单方消解）"
founder_question: "'禁止低价叫卖'是否禁止一切紧迫感表达，还是允许陈述经盘点核实的真实库存事实（如确实仅剩 20 件）？请裁定边界。"
```

---

## 三、来源统计与残留说明

**卡数**：38 张＝ROUTED 35＋PENDING 3。

**destination 分布**：KERNEL_METHOD 12（0301–0310、0330、0334，其中 0330/0334 出自 R02）；RULE_CANDIDATE 10（0311–0317、0328、0329、0331）；JUDGE_QUESTION 7（0318–0323、0332）；CASE_REFINEMENT 5（0324–0327、0333）；CONTRACT_PROPOSAL 4（0335 ROUTED＋0336/0337/0338 PENDING）。SEMANTIC_LAYER / CASE_CANDIDATE / BRAND_MEMORY_PENDING_EVIDENCE 本场为 0——本场全部商品与经营事实均为构建期合成条件（SYNTHETIC_SCENARIO_OVERLAY），不得作为企业事实入语义层；亦无品牌偏好陈述。

**provenance**：全部 38 张为 `AI_PROPOSAL_FOUNDER_APPROVED`（Founder 2026-08-17 整体批准，无逐条改写）。`FOUNDER_ORIGINAL_JUDGMENT` 0、`AI_PROPOSAL_FOUNDER_REVISED` 0——本场无 Founder 独立业务理由，不得把专家候选语言改写为 Founder 原始经验。

**按审查报告修正后入卡的项（S03 六条问题清单逐条对应）**：

1. 【P1 建议批准 5 条被扩记为 18 条已确认】本文件不逐条转录候选包"已确认判断"清单（E.10 红线：强制每条专家表述进仓库），只转候选资产卡＋追问轮收敛结论＋审查点名遗漏素材；每张卡的 source_ref 落到具体专家与段落，扩记链条不再复制。
2. 【P2 真冲突未暴露：成功口径缺失是否已使主推资格不成立，专家二/三＝不成立 vs 专家一＝待裁，2:1】该问题已在收口包分流为 **PCR-03 第 1 项**（成功数量未定义时是否禁止整窗战役），按编译规范 §4.3 不转 ELI 卡；冲突本身在 ELI-0316 的 `does_not_apply_when` 与 ELI-0303 的 `source_ref` 中显式登记，三份共同下限（不得作窗口整体承诺）单独立卡。
3. 【P3 七项实质主张消失】已据 S-03.txt 原文补卡：同批机会成本比较（ELI-0306）、诊断五层顺序（ELI-0305）、五条件 MEDIUM 置信度（ELI-0303 卡内恢复）、角色降级阶梯"不减分/加分"（ELI-0307）、诊断起点三不看的判断结构（ELI-0304）、低资源试探的效力边界（ELI-0309）、"六周内必须作出决定、不能无限期观察"（并入 ELI-0308）。
4. 【硬规则级／判分级素材丢失】补卡四条：专家一 §10 possible_hard_rule(d)"成功无数量定义时不得作窗口整体承诺"（ELI-0316）、专家三"无可识别差异点"否决项（ELI-0315）、专家一评审三问第 2 问"被禁手段是否以变相话术回流"（ELI-0322）、专家一 option B"押错代价含账号信用与流量资源"（ELI-0323）。
5. 【真实性豁免口系单方裁决】候选包在变相叫卖禁令后加挂的"且没有对应真实库存结构依据"**未采用**；ELI-0317 用忠实严格版，例外问题另立 ELI-0338（PENDING），不以已裁身份入卡。
6. 【"整窗启动"抢裁】候选包"在成功口径未明确前……可安排前段试探和后段执行"未作为已裁结论入 ROUTED 卡；ELI-0308 只登记核验与行动同构与"须设决定点"，并明示该卡不构成启动授权；启动权归 PCR-03 第 1 项。
7. 【两处平反已按报告执行】Hero/Support/Traffic/Profit/Clearance 为排期主题 3 Q6 既有体系，本文件引用合规（正式定义与迁移仍归 PCR-03 第 4 项）；"角色是否固有属性"为排期主题 3 Q7 原题，非编译加码——该命题本身属产品词表范畴，未单独立通用卡，其可操作部分已分解进 ELI-0307（角色降级阶梯）与 ELI-0328（两个独立决定）。

**未转卡的内容及原因**：

- 候选包 UNRESOLVED 四张（UN-S03-R01-01…04：成功门是否强制、经营/内容角色是否正式拆分、无数据商家滚动试探是否正式降级路径、正式角色词表定义与迁移）——全部落在 **PCR-03（Business 成功门与角色词表）** 队列，属产品合同问题而非专家陈述，按编译规范 §4.3 不转 ELI 卡，此处引用队列号即可。
- 候选包"已确认判断 1–18"与 SESSION_CLOSEOUT 的十条关键判断清单——与上述卡片同源、内容重复，按 E.10 不逐条建卡。
- 案例级具体数值与安排（"第一周末为角色决定点""六周切段"的具体周次、"800/20 件"具体数量结论）——按 S09 已批准口径"规则进 Core、数值进案例"，只在 CASE_REFINEMENT 卡（ELI-0324/0326）与相关卡的 source_ref 中保留，不写成通用方法。
- 专家对 B.6 失败标签的处置（专家一"不提请入册"、专家二 NOT_ASSIGNED×9、专家三三个新名）——未向任何既有 `BD_*` 标签作映射指派，专家保留态度原样登记于 ELI-0335，覆盖审查走 B.8.1。
- 跨场挂钩：ELI-0333 的店长顾客侧陈述形态挂 S05 未决边界（PCR-05／S05 专家间对同型句一判可信一判否决），本场不越界裁决；ELI-0303 的"最低画面集"口径承自 S02，本场不重新定义。

> 本文件全部卡片为 PROVISIONAL 候选，不构成现行 PRD、附录 A/B、生产 Prompt、Rule Engine、正式考卷、商品角色枚举或 Brand Memory 的变更；正式生效另走批准流程。
