# DIYU-KE-ELI-S07｜System：跨模块一致性、验证边界与返工停止 正式入库知识卡

```yaml
document_id: DIYU-KE-ELI-S07-20260817-V1
session_id: DIYU-KE-S07-20260817-001
session_theme: S07 System：跨模块一致性、验证边界与返工停止
covered_rounds: [S07-R01, S07-R02]
source_files:
  - S-07.txt（S07-R01 三份专家原文；忠实版权威，冲突时以本文件为准）
  - S增补追问专家回答.md（S07-R02 三份专家回答：L354-433 专家一／L1065-1250 专家二／L1704-1829 专家三）
  - DIYU-KE-S07-20260817-001_S07待入库候选包_v1.md（候选资产区 29 张卡的转换来源）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S07-R02 追问卡 L429-471；PCR-07 队列 L174-183）
  - DIYU-KE-S02-S07_原文对照审查总报告_20260817.md（S07 节 L128-135；仅 Founder 能决定事项 L143）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S07 节 L45-46：三处平反＋一处加重）
  - E_领域专家知识提取协议.md（E.2 路由／E.2.3 失败标签／E.3 卡模板／E.10 防膨胀）
  - 知识提取会议排期.md（主题 7 L182-201：Preflight／Delivery Validation／Artifact Reference／Rework Controller／SYS-D01 为既有体系标识）
ruling_basis: Founder（Faye）2026-08-17 裁决 S01–S08 候选包与五张追问卡专家回答全部批准通过，指示按 E 协议整理为正式入库文档。
compiled_on: 2026-08-17
card_total: 39
routed_count: 39
pending_count: 3
formal_effect: NONE   # 全部为候选，生效另走 A.9.1 / B.8.1 批准流程
```

> **控制声明**：本文件是 E.3 意义上的知识卡（路由单），不是生效资产。任何硬规则、状态值、失败标签、停止码、验证器规则，仍须走对应批准与版本升级流程后才能生效。本文件不修改任何既有文件。
>
> **S07 provenance 说明**：本场 Founder 为整体批准（"专家通过"），无逐条改写，亦未提供可与候选分析区分的 `founder_original_reasoning`。故全部卡 provenance 一律 `AI_PROPOSAL_FOUNDER_APPROVED`，不得把专家候选语言改写为 Founder 原始经验。
>
> **本场两处纠正**（对候选包 v1）：① `HR-S07-R01-01`「四线绝对触发重判」此前把有族内分歧的断言铸成硬规则，本次按 S07-R02 三专家收敛写入**修正后版本**（见 ELI-0706），旧版不入卡；② 候选包新造的 `CONFIRMED_CONSTRAINT` / `CONFIRMED_ASSET` 两个状态枚举撞排期「不得直接引入新状态」明文，其内容改用会议协议第四节既有事实纪律词表表达（见 ELI-0734／0735），新枚举不沿用。

---

## 一、入库知识卡（ROUTED）

```yaml
elicitation_item_id: ELI-0701
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "「商品理解＋咨询」制作包已审核未拍摄，用户把主要结果改为「本周直接成交」并要求前面全部保留、只把结尾改成马上购买。"
expert_statement: "合法答案必须拒绝从表达层起改，说明哪些判断失效、哪些事实资产保留，并列出成交设计的最小经营事实；既不接受只改结尾，也不接受全部推倒。"
statement_type: BOUNDARY
applies_when: "主要商业结果发生变化，旧方案尚未拍摄或发布。"
does_not_apply_when: "只修改同一目标内的措辞或错别字。"
counterexample: "「把结尾改成马上购买即可。」"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 CR-S07-R01-01；S-07.txt 专家一 L33、专家二 L133-138、专家三 L495-509 三份同向。细化对象为 SYS-D01 跨模块一致性答案族与禁止结果（排期主题 7 既有案例编号）。"
```

```yaml
elicitation_item_id: ELI-0702
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "同一局面的变体：用户只补充一个真实购买链接，价格、可售库存与履约仍未知。"
expert_statement: "只补链接应允许继续做链接实测与成交版结构草案（解锁设计），但在价格、可售库存与履约未知时不得判定可以发布，也不得添加现货、限时、发货与稀缺承诺。"
statement_type: BOUNDARY
applies_when: "承接只完成部分补齐。"
does_not_apply_when: "价格、库存和履约已全部核验。"
counterexample: "有链接就立即添加「现货马上买」。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 CR-S07-R01-02；S-07.txt 专家一 L87（追问 A「解锁设计，不解锁发布」）、专家三 L632-637（judgment_should_change: PARTIAL）。专家一同文 L35 另有「连改成什么样都还无法设计」的更严表述，与 L87 自相矛盾；编译按其对该反事实的直接作答（L87）采宽口径，该内部矛盾未经裁决，登记于第三节。"
```

```yaml
elicitation_item_id: ELI-0703
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "同一局面的变体：用户听完解释后只回一句「别问了，再有冲击力一点」，不提供任何新经营事实。"
expert_statement: "合格答案可在合法表达域内增强开场、节奏、镜头与信息排序，但必须守住承接与事实边界；当「再冲一点」只剩越线一条路（编限时、造稀缺、无授权谈价）时停止改稿，把「补事实解锁更强表达」与「就此定稿」的选择摆回给用户。"
statement_type: BOUNDARY
applies_when: "用户反复要求增强但不提供新信息。"
does_not_apply_when: "新事实或新授权已经提供。"
counterexample: "用「最后机会」替代库存事实。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 CR-S07-R01-03；S-07.txt 专家一 L91（追问 C：死守承接、规避库存履约、放开合法表达域）、专家三 L745-753。"
```

```yaml
elicitation_item_id: ELI-0704
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "成片已拍摄或剪辑完成，但开头、正文、结尾与发布承接不一致。"
expert_statement: "开头承诺、正文论证、结尾行动、发布承接四点一线；任一断裂即不发，已拍也不发——拍摄成本不能抵消经营与真实性断裂。"
statement_type: BOUNDARY
applies_when: "产物已拍摄或剪辑完成，进入发布判断。"
does_not_apply_when: "四点一致且经营事实已核验。"
counterexample: "因「已经拍完」而放行没有购买入口的催购视频。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 CR-S07-R01-04；S-07.txt 专家一 L43（五种拒发情形＋「四点一线，任一断裂即不发」）、专家二 L358-370（七条拒发）、专家三 L686-694。细化对象为 Delivery Validation 正反样本。"
```

```yaml
elicitation_item_id: ELI-0705
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "目标切换后，旧咨询版在自身目标下仍完整自洽，尚未决定处置。"
expert_statement: "旧咨询版应被评估为新战役的可复用资产，而不是自动废弃或自动上岗；是否用作认知铺垫与顾虑采集，由重做的商业规划决定，不自动先发。"
statement_type: BOUNDARY
applies_when: "旧版本对原目标仍完整成立。"
does_not_apply_when: "旧版本存在事实错误或已不符合品牌边界。"
counterexample: "目标一变立即删除全部旧产物；或未经战役判断自动安排先发。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 CR-S07-R01-05；S-07.txt 专家一 L49（「不自动上岗」）、L129。其「默认先发还是冻结、要不要产品默认规则」的处置权问题已分流 PCR-07 第 1 项，本卡只承载「须评估、不自动作废、不自动先发」的专家判断。"
```

```yaml
elicitation_item_id: ELI-0706
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "上游出现修改请求，需判断从哪一层开始返工（本场两个局面：目标由咨询改成交；目标不变只更换咨询入口）。"
expert_statement: "修改越过主要目标类型、承接形态、事实边界或商品角色任一条线时，不得仅从文案表达层开始返工。其中承接形态一线的触发判据为：顾客被要求的动作性质、行动成本与风险、品牌承诺、落点与接单人力四项中任一项发生实质变化；四项全不变的同性质入口更换不触发本条，按局部返工处理，且返工范围应与变化程度相称。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "已有上游商业判断与下游内容包，出现修改请求。"
does_not_apply_when: "同一目标、同一事实边界内的纯文案修正；以及承接四项判据全不变的同性质入口更换（如评论区→仅收集咨询、不成交、不增加顾客承诺的小程序表单）。"
counterexample: "咨询改成交只替换 CTA；反向的失败是任何承接字段变化即机械触发全流程重做。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 HR-S07-R01-01 的**修正后版本**。四线出自 S-07.txt 专家一 L41；承接线判据为 S07-R02 三专家收敛（专家三「四检法」增补 L1743-1748、专家二「四项检查」L1179-1188/L1250、专家一「行动性质／行动成本／转化责任」L406-428）。原「四线任一即绝对触发、关死条件出口」版本被本卡取代，不另入卡（见第三节残留说明第 2 条）。目标类型一线在经营条件全部齐备时是否开条件出口，仍未裁决，见 ELI-0739（PENDING）。"
```

```yaml
elicitation_item_id: ELI-0707
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "内容要求顾客完成购买、预约、留资等可执行动作。"
expert_statement: "发布型 CTA 必须指向已确认存在、指向正确商品且经实测可完成目标动作的承接；形式上出现链接或商品卡不够。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容要求购买、预约、留资或其他可执行动作。"
does_not_apply_when: "纯信息内容，无行动承诺。"
counterexample: "「马上购买」但没有链接或商品卡；或链接存在却指向错误商品。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 HR-S07-R01-02；S-07.txt 专家一 L13/L47（闭环实测）、专家二 L368、专家三 L662-672。指向既有 Delivery Validation／Artifact Reference（排期主题 7 明文）。"
```

```yaml
elicitation_item_id: ELI-0708
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "目标要求顾客本周完成真实购买，而价格、可售库存、购买路径、履约均未提供。"
expert_statement: "直接成交任务不得通过修改 CTA 跨越价格、可售库存、购买路径和履约等任务相关事实缺口；价格未知不得说划算／历史低价，库存未知不得说现货／最后一批，履约未知不得承诺发货时效与售后结果。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "目标要求真实购买。"
does_not_apply_when: "目标只要求理解、曝光或咨询。"
counterexample: "库存、价格和履约未知时生成现货催购文案。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 HR-S07-R01-03；S-07.txt 专家三 L773（possible_hard_rule 逐字）、专家一 L39、专家二 L291-325。"
```

```yaml
elicitation_item_id: ELI-0709
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "用户压缩时间、要求「别问了、再有冲击力一点」。"
expert_statement: "用户催促、要求更有冲击力或要求少问，不构成降低事实、品牌、承接和履约标准的授权。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "用户压缩时间或要求增强效果。"
does_not_apply_when: "用户提供了真实事实，或有权授权的新经营政策。"
counterexample: "因「别问了」自行编限时库存。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 HR-S07-R01-04；S-07.txt 专家一 L91（「催促不降低事实标准，是本轮给定的硬约束」）、L103（顺从性虚构）、专家二 L404-406、专家三 L678。与 S02「快不降标」同源，跨场各自留卡。"
```

```yaml
elicitation_item_id: ELI-0710
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "旧版本被改造成新的商业用途，需要判断返工是否真的完成。"
expert_statement: "主要目标切换后的返工版若没有新增任何任务相关经营事实，也没有形成新的可执行闭环，不得被标记为已完成目标调整——返工的证据是新事实和新闭环，不是新形容词。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "旧版本被改造成新的商业用途。"
does_not_apply_when: "新目标仅改变文案语气且不改变行为结果（纯风格润色）。"
counterexample: "只增加「限时、购买、别错过」，把音乐调急、字幕加大。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 HR-S07-R01-05；S-07.txt 专家一 L47（事实增量检验）、L97（词语返工）、专家二 L417。"
```

```yaml
elicitation_item_id: ELI-0711
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "目标变化后盘点商品事实、素材、顾客问题与讲述者资格。"
expert_statement: "已确认的事实资产在目标变化后不得自动作废，但在新用途下必须重新检查其相关性与是否仍然成立。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "返工盘点商品事实、素材、顾客问题和讲述者资格。"
does_not_apply_when: "原事实已过期、冲突或来源失效。"
counterexample: "因目标变化删除全部真实商品素材；或未经复核原样用于新目标。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 HR-S07-R01-06；S-07.txt 专家一 L37/L105（「判断才会过期，事实不过期」）、专家二 L237-257、专家三 L582-598。"
```

```yaml
elicitation_item_id: ELI-0712
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "评审一份把咨询／认知内容改成成交内容的返工产物。"
expert_statement: "先数新增经营事实，再检查是否形成新行动闭环；零事实增量且只增加成交词的，应判为表面返工。"
statement_type: METHOD
applies_when: "咨询、认知内容被改成成交内容。"
does_not_apply_when: "目标未改变。"
counterexample: "原稿只增加「马上购买」即判通过。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 JC-S07-R01-01；S-07.txt 专家一 L129（possible_judge_calibration 三查之一）、专家三 L776。"
```

```yaml
elicitation_item_id: ELI-0713
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "评审一份宣称服务直接成交的内容。"
expert_statement: "用五步成交说服链评审：看到商品→形成想要→知道价格→知道在哪买→理解现在行动的真实理由；每一步都应能指向具体画面、口播、商品页或发布承接，缺任何一步不应因语气强烈而判通过。"
statement_type: METHOD
applies_when: "内容宣称服务直接成交。"
does_not_apply_when: "非成交目标的内容。"
counterexample: "有购买口号但没有价格和入口。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 JC-S07-R01-02；S-07.txt 专家一 L47（说服链检验，五步逐字）、L129。"
```

```yaml
elicitation_item_id: ELI-0714
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "评审完整发布包（含发布文案与置顶评论）。"
expert_statement: "用四点一线检查开头、正文、结尾与发布承接是否同向；任一点改变关系姿态或目标，判一致性失败。"
statement_type: METHOD
applies_when: "评审完整发布包。"
does_not_apply_when: "只评审单一素材片段。"
counterexample: "前段「不急着买」，结尾「马上抢」；或视频喊购买而置顶评论仍是咨询口径。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 JC-S07-R01-03；S-07.txt 专家一 L43。"
```

```yaml
elicitation_item_id: ELI-0715
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "发布前审核，需要划分机器可查与必须人判的问题。"
expert_statement: "清单查「有没有」：承接存在且实测可点通、价格／库存／优惠声明是否有来源、置顶口径与视频 CTA 是否同向、违禁表达是否出现、字幕与商品名是否一致；专业人员查「通不通」：说服链是否真走通、姿态是否断裂、选题是否适配新目标、价值是否支撑价格、冲击力是否滑向变相叫卖。"
statement_type: METHOD
applies_when: "发布前审核。"
does_not_apply_when: "仅检查文件是否损坏等技术性检查。"
counterexample: "关键词均通过便宣称内容能够成交。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 JC-S07-R01-04；S-07.txt 专家一 L89（追问 B 逐项分层）、专家三 L716-734。是否固化为发布前标准工序属 PCR-07 第 3 项，本卡只承载分层判据。"
```

```yaml
elicitation_item_id: ELI-0716
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "评审返工范围是否合理（上游目标或策略已改变）。"
expert_statement: "检查输出是否区分判断、事实与纪律三类；全保或全废均应要求说明依据。"
statement_type: METHOD
applies_when: "上游目标或策略改变后的返工评审。"
does_not_apply_when: "只有独立错别字修复。"
counterexample: "目标变化后把真实商品素材全部作废。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 JC-S07-R01-05；S-07.txt 专家一 L55（防全保／全废两个被禁极端）。"
```

```yaml
elicitation_item_id: ELI-0717
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "输出包含购买或其他行动入口，需判定承接是否通过。"
expert_statement: "CTA 承接的通过判断不能只看链接是否存在，还要实测指向正确商品、可售规格存在、目标动作能否真实完成、页面内容与视频是否一致。"
statement_type: METHOD
applies_when: "输出包含购买或其他行动入口。"
does_not_apply_when: "无行动 CTA 的纯信息内容。"
counterexample: "链接存在但指向错误商品。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 JC-S07-R01-06；S-07.txt 专家一 L87（链接实测四项）、专家三 L718-724。"
```

```yaml
elicitation_item_id: ELI-0718
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "用户修改需求或事实发生变化，需要决定返工起点。"
expert_statement: "变化层定位法：先判断变化发生在目标、商业路线、创意结构、制作执行还是局部表达，再从该层向下返工，不向上无差别重做。"
statement_type: METHOD
applies_when: "用户修改需求或事实发生变化。"
does_not_apply_when: "新任务完全独立，与既有产物无继承关系。"
counterexample: "目标变化只改结尾；或错别字修复重跑全部模块。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-01；S-07.txt 专家一 L41/L53（Step 1「层级一旦错判，后面全部按文字活处理」）、专家三 L524-532。指向既有 Rework Controller（排期主题 7 明文）。"
```

```yaml
elicitation_item_id: ELI-0719
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "上游变化导致下游可能失效，需要盘点既有产物的存废。"
expert_statement: "存废三分法：把既有产物拆成①为旧目标作出的判断（过期，须重审）②有来源的事实资产（不过期，换角色复用前须复核相关性）③跨目标纪律（真实性、品牌边界、声画同证、可执行交付，原样继续生效）。"
statement_type: METHOD
applies_when: "上游变化导致下游可能失效。"
does_not_apply_when: "没有既有资产。"
counterexample: "目标一变全保或全废。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-02；S-07.txt 专家一 L6/L37（三分法逐字）、专家二 L237-257、专家三 L582-598。"
```

```yaml
elicitation_item_id: ELI-0720
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "任务从认知／咨询转为直接成交，需要按序补清经营事实。"
expert_statement: "成交任务事实分梯队法：第一梯队（不清则方案无法设计）＝成交承接在哪、可售库存与尺码颜色结构；第二梯队（不清则不能发布）＝履约能力、价格与视频提价授权；第三梯队（不清则不能承诺结果）＝「一批」是多少、按什么口径计算。"
statement_type: METHOD
applies_when: "任务从认知／咨询转为直接成交。"
does_not_apply_when: "无成交目标的任务。"
counterexample: "先写促单脚本，后查有没有货和链接。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-03；S-07.txt 专家一 L7/L39（三梯队逐字）。专家二 L269-325 给出五优先级（承接→库存→价格政策→成功数量→履约）、专家三 L620-630 给出六项排序，两者在「承接与可售结构最先、成功口径属结果承诺层」上与专家一同向，但履约与成功数量的先后不同；入卡采专家一的三梯队骨架，两种排序差异登记于第三节，不作绝对顺序硬规则。"
```

```yaml
elicitation_item_id: ELI-0721
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "内容用途发生变化后，判定返工是否真正完成。"
expert_statement: "新事实＋新闭环验收法：返工完成的证据是新增任务所需经营事实进入内容，并且顾客能够完成新目标动作（路径真的点得通），不是词语变化。"
statement_type: METHOD
applies_when: "内容用途发生变化。"
does_not_apply_when: "纯风格润色。"
counterexample: "加强节奏但没有购买入口。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-04；S-07.txt 专家一 L47（三条检验之事实增量与闭环实测）。"
```

```yaml
elicitation_item_id: ELI-0722
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "发布前验证，需要分配机器检查与人工整审的职责。"
expert_statement: "双层审核法：客观存在性与字段一致由清单检查，商业充分性、说服链与关系姿态由专业人员整审——把存在性交给表，把一致性留给人。"
statement_type: METHOD
applies_when: "发布前验证。"
does_not_apply_when: "仅内部草案且不对外。"
counterexample: "试图用关键词规则判定「为什么现在买」是否有说服力。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-05；S-07.txt 专家一 L89、专家三 L716-734。是否固化为所有发布产物的标准工序、人工成本与升级条件属 PCR-07 第 3 项，本卡不预判。"
```

```yaml
elicitation_item_id: ELI-0723
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "旧内容目标改变，但真实问题、素材与讲述者资格仍有效。"
expert_statement: "旧资产重编排法：真实问题、素材与讲述者资格不按原顺序机械复用，而按新目标重新分配到正文、FAQ、前置内容或后续内容——属购买顾虑的进正文做下单前扫障，属泛了解的转 FAQ 或后续内容。"
statement_type: METHOD
applies_when: "旧内容目标改变但事实资产仍有效。"
does_not_apply_when: "资产已过期或冲突。"
counterexample: "三个咨询问题原顺序不变直接套入成交版。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-06；S-07.txt 专家一 L49、专家二 L423-447、专家三 L593-598。"
```

```yaml
elicitation_item_id: ELI-0724
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "用户反复要求「再改、再冲击」但不提供任何新信息。"
expert_statement: "返工停止法：记录每轮新增的事实、授权或可执行闭环变化；没有增量且只能通过越线增强时停止改稿，并明确指出补充哪些事实可以解锁下一步、若不补充当前能合法交付到什么程度，把选择返回真实决策方。"
statement_type: METHOD
applies_when: "用户反复要求增强但不给新信息。"
does_not_apply_when: "每轮都有实质事实或目标更新。"
counterexample: "连续改十版，仅替换更激烈词汇。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "包 MM-S07-R01-07；S-07.txt 专家一 L91/L113、专家三 L745-753。因其规定输出义务与停止时点（合同语义），按编译规范第 2 条走 CONTRACT_PROPOSAL 而非 KERNEL_METHOD；对应停止码见 ELI-0732。"
```

```yaml
elicitation_item_id: ELI-0725
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "承接入口发生变化，需判断这是换入口还是换路线。"
expert_statement: "承接变更四检法：①动作性质——顾客被要求做的事变没变（问一句→留个人信息→付款，每升一级即路线变化）；②行动成本与风险——要注册、装应用、交个人信息即越线；③品牌承诺——表单若附「限时回复」「留资有礼」，前者是须兑现的新承诺、后者直撞不低价边界；④落点与人力——公开评论改为私下一对一，接的人与工作量变了，须核对有人接得住。①②③任一变化→重回商业判断，返工范围与变化程度相称；四项全不变→仅做局部返工。"
statement_type: METHOD
applies_when: "承接入口变化而商业目标未声明改变。"
does_not_apply_when: "商业目标本身已改变（此时按目标线直接回商业判断）。"
counterexample: "任何承接字段变化即机械要求全流程重做；或因目标没变就完全不检查新入口是否可用。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 三专家收敛：专家三「四检法」（增补 L1743-1748，第④项明写不单独触发回商业判断，本卡保留该限定）、专家二「目标动作—行动成本—顾客承诺—后续结果」四项检查（L1179-1188、L1250）、专家一「行动性质是否改变，或显著提高行动成本、改变转化责任」（L406-428）。本卡为 ELI-0706 承接线判据的方法本体。"
```

```yaml
elicitation_item_id: ELI-0726
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "四检法判定为同性质入口更换后，执行局部返工。"
expert_statement: "入口更换的局部返工限四处：①结尾引导改写为新入口的真实操作指引（在哪点、点了会发生什么）；②发布文案入口指向同步更新；③评论区口径明确；④承接验收——从本条内容的真实入口走一遍。其中①②④的链路可达、步骤数、提交反馈属确定性验证可逐项走查，③的口径与响应节奏属人工经营决定。商业判断不重做。"
statement_type: METHOD
applies_when: "承接四检法全部不变的同性质入口更换。"
does_not_apply_when: "四检法①②③任一项发生实质变化。"
counterexample: "视频仍说「评论区告诉我」，发布文案却引导填写表单。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 三专家收敛：专家三 L1736-1741（四项清单＋确定性／人工判断分离）、专家二 L1075-1081、L1152-1161、专家一 L380-391。"
```

```yaml
elicitation_item_id: ELI-0727
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "商业目标不变（让顾客看懂商品并愿意进一步咨询），只把咨询入口从评论区改为已配置实测的小程序咨询表单；表单只收集咨询，不直接成交，不增加新的顾客承诺。"
expert_statement: "合法答案是局部返工（改结尾＋发布文案＋评论区口径＋承接验收），不重做商业判断；同时必须确认新入口从本条内容可用，且没有增加不必要的顾客承诺或隐私成本。可原样保留：商业目标、商品角色、价格库存判断、品牌边界、商品事实、店长发言安排、内容主体结构、「看懂→想进一步问」的说服逻辑与商品证明镜头。"
statement_type: BOUNDARY
applies_when: "顾客被要求的动作仍是「提出咨询」，仅执行入口更换。"
does_not_apply_when: "新入口带来付款、预约、定金、留资筛选或高敏感信息要求。"
counterexample: "因承接字段变了就回商业层重做整条方案；或因目标没变就免验收直接发布。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 追问卡（收口包 L429-471）＋三专家收敛判断（专家一 L358-433、专家二 L1071-1083、专家三 L1709-1712、L1730-1741）。细化对象为 SYS-D01 跨模块一致性答案族的「入口更换」变体。"
```

```yaml
elicitation_item_id: ELI-0728
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "品牌方称新的咨询表单「已经配置并实测」。"
expert_statement: "「品牌已实测」不等于「本条内容的路径已验收」：发布前必须从本条内容的视频真实入口走一遍——找得到入口、几步能提交、提交后顾客看到什么（多久有人回的预期）、咨询落到谁手上、多快必须回；后台能否真正收到咨询亦须确认。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "承接入口更换或新增，进入发布判断。"
does_not_apply_when: "无行动入口的纯信息内容。"
counterexample: "以「品牌那边测过了」或「目标没变」为由免验收直接发布。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 三专家收敛：专家三 L1715/L1740（逐字）、专家一 L382-389（表单可用性、后台能否收到）、专家二 L1118-1124/L1154-1161（假设：实测环境≠发布环境；提交后有人回复才算承接完成）。与 ELI-0707 同源，本卡是其在「入口更换」局面的具体化。"
```

```yaml
elicitation_item_id: ELI-0729
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "咨询入口迁到表单后，顾客仍会在评论区公开提问。"
expert_statement: "入口迁走后必须先定评论区口径——就地回答还是引导表单，以及是否保留「也可以留言」的备用入口——不得让公开提问悬空。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "承接入口从公开评论迁至站内表单或私域入口。"
does_not_apply_when: "评论区仍是唯一咨询入口，口径未变。"
counterexample: "视频与文案全部指向表单，评论区公开提问无人承接也无口径。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 三专家收敛：专家三 L1739（逐字）、专家一 L387-388、专家二 L1160-1161。"
```

```yaml
elicitation_item_id: ELI-0730
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "评审入口更换后的承接是否达标。"
expert_statement: "验收基线：新入口的响应不得低于旧入口的隐形标准——评论区的隐形承接标准是「公开且快」，表单响应低于它，承接实际是降级。表单侧须明确谁接单、多快回。"
statement_type: METHOD
applies_when: "承接入口更换后的发布前验收。"
does_not_apply_when: "入口未更换。"
counterexample: "表单收集咨询，但没有人员负责回复，或响应时效显著慢于原评论区。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 专家三 L1719、L1830（**单份来源**，未经三方收敛）。专家一 L389、专家二 L1159 均要求核对「谁接收、谁回复、后台能否收到」，但未给出「不得低于旧入口」的基线判据，故本卡按单份主张登记，不冒充收敛结论。"
```

```yaml
elicitation_item_id: ELI-0731
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "识别哪类「链接更换」看似局部、实际已经改变任务。"
expert_statement: "看似换链接、实为换任务的情形：咨询表单换成可付款商品卡（变成交）、进群二维码（变私域拉人）、捆绑「留资送礼」的表单（顾客动机与品牌边界都变）、站外链接在视频号内打不开（可行性变）、普通提问换成付费预约、留言咨询换成经销商加盟申请、商品咨询换成需要大量个人资料的销售线索采集、普通咨询换成预售／定金／库存预约。"
statement_type: FAILURE_MODE
applies_when: "承接入口更换的判定。"
does_not_apply_when: "顾客被要求的动作与承诺完全不变的同性质入口更换。"
counterexample: "把上述任一情形按「只改了个链接」处理，仅做局部返工。"
candidate_destination: CASE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 三专家各自列举合并：专家三 L1750、专家二 L1219-1225、专家一 L420-428。属新局面素材（非既有冻结案例细化），按编译规范第 2 条走 CASE_CANDIDATE；升格为正式验收案例须走 E.8 窄门＋B.8.1。"
```

```yaml
elicitation_item_id: ELI-0732
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "目标切换为直接成交、经营事实全缺的局面，需要给出停止结果。"
expert_statement: "本局面的停止结果按法定三值表达：INSUFFICIENT_CONTEXT＝未取得成功口径、可售库存、价格、购买路径与履约信息前，不继续成交版拍摄；NO_FEASIBLE_SOLUTION＝用户拒绝提供必要经营事实，却坚持制作可以直接成交的内容；HUMAN_DECISION_REQUIRED＝本周成交数量与品牌价格边界、库存能力或履约能力无法同时满足，需调整目标、时间、商品角色或经营政策。"
statement_type: BOUNDARY
applies_when: "跨模块返工与成交前置检查触发停止。"
does_not_apply_when: null
counterexample: "用自造中文停止名（设计暂停／发布暂停／结果承诺暂停／任务回退）替代法定三值，或新增第四个停止码。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-07.txt 专家三 L736-743 原文逐条。候选包「停止条件」节以六个自造中文名承载本内容，两份审查报告均点名该合规映射被丢弃（原文对照报告 S07 第 4 条；标准对齐结论 S07 第 3 条），本卡按原文找回。不得新增停止码枚举。"
```

```yaml
elicitation_item_id: ELI-0733
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "咨询入口更换为小程序表单的局面，需要给出停止结果。"
expert_statement: "本局面的停止结果按法定三值表达：INSUFFICIENT_CONTEXT＝表单字段构成、实际进入路径或提交后的回复责任未确认（不阻断返工范围判断，但阻断「是否触发行动成本一检」的最终认定）；NO_FEASIBLE_SOLUTION＝表单无法从发布环境使用且原评论区入口也被关闭；HUMAN_DECISION_REQUIRED＝表单显著增加个人信息或顾客承诺、或验收发现表单体验明显劣于评论区（加载慢、步骤多）时，是回退还是带伤切换，属品牌经营选择。"
statement_type: BOUNDARY
applies_when: "承接入口更换的返工与验收。"
does_not_apply_when: null
counterexample: "字段未知即宣布返工范围无法判断；或体验劣化时由执行侧自行决定带伤切换。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 专家二 L1210-1217 与专家三 L1816-1818 两份独立给出同结构的法定三值映射，内容合并入卡；专家一未给停止码。"
```

```yaml
elicitation_item_id: ELI-0734
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "关键经营事实（价格、库存、承接、履约、成功数量）全部缺失，而用户要求推进成交内容。"
expert_statement: "不得为顺从新目标自行补写价格、库存、优惠、购买路径、紧迫性或履约承诺；内部存在本周目标，不等于顾客端存在真实紧迫事实。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "任务相关经营事实缺失且未获授权。"
does_not_apply_when: "品牌或经营侧已提供并确认相应事实与授权。"
counterexample: "库存未知时写「最后一批」；价格未知时写「历史低价」。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-07.txt 专家一 L71、专家三 L539、专家二 L366-368。候选包用**新造枚举** `CONFIRMED_CONSTRAINT` 承载本条，该枚举撞排期「不得直接引入新状态、走合同提案」明文（标准对齐结论 S07 第 ② 条加重项）；本卡改用会议协议第四节既有事实纪律与 RULE_CANDIDATE 去处表达，新枚举不沿用。"
```

```yaml
elicitation_item_id: ELI-0735
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "目标切换局面内，需要登记哪些资产在构建期设定条件下仍然有效。"
expert_statement: "本局面（构建期设定条件）内仍然有效的资产：商品资料与真实商品画面、三个真实顾客问题、店长的一线发言权材料、门店拍摄条件与基础制作方法。它们在新用途下须复核相关性，但不因目标变化自动失效。"
statement_type: FACT
applies_when: "本 SYS-D01 目标切换局面内的返工资产盘点。"
does_not_apply_when: "原事实已过期、冲突或来源失效；亦不得当作试点品牌的真实企业事实向局面外推广。"
counterexample: "把这些局面内给定条件写成品牌权威事实，或据此免除新用途下的复核。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包「使用的事实」节原以**新造枚举** `CONFIRMED_ASSET` 标注本条；按会议协议第四节词表，其在本局面内属 SYNTHETIC_SCENARIO_OVERLAY 给定条件下的 CONFIRMED_FACT，不得升级为品牌真实事实。原文支持：S-07.txt 专家一 L37、专家二 L241-257、专家三 L538、L582-590。新枚举不沿用。"
```

```yaml
elicitation_item_id: ELI-0736
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "两轮专家为本场失败模式起了描述性名字，尚无 B.6 既有标签对应。"
expert_statement: "本场专家自造的失败概念——词语返工、门后无路、姿态断裂、顺从性虚构、无差别作废（S07-R01）；BLANKET_REWORK、UNVERIFIED_HANDOFF、ENTRY_EXISTS_FALLACY、CRITERION_FREE_ANSWER（S07-R02）——均为**新标签候选，须走 B.8.1 覆盖审查，不得私加标签、不得往既有标签塞新语义**。专家一明写「描述性命名，不提请入册」；专家三 S07-R01 六条 forbidden 全部标注 failure_label_candidate: NOT_ASSIGNED，该保留态度一并存续。"
statement_type: FAILURE_MODE
applies_when: "准备把本场失败概念工程化为错误码、标签或自动规则。"
does_not_apply_when: "仅作为会议候选与判分描述使用。"
counterexample: "直接新增「词语返工」正式错误码或 B.6 标签。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-07.txt 专家一 L95-105、专家三 L662-684；S07-R02 专家三增补 L1798-1812。与既有 B.6 标签、SYS-D01、Preflight、Delivery Validation、Rework Controller 的**正式映射**属 PCR-07 第 4 项，本卡只登记候选身份与「不得私加」的禁止效力，不做映射。"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0737
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "咨询入口更换为表单，且表单在咨询内容之外还要求顾客留下联系方式或其他个人信息。"
expert_statement: "三专家对此情形的处置分级不一致：专家一＝已改变商业任务，必须回到商业判断重新规划（其原文举例为手机号、身份证、地址等高敏感信息）；专家二＝PARTIAL，内容需解释收集目的、必要性与后续处理，可能需重新评估顾客是否愿意行动，但商品的商业角色不一定需要重做；专家三＝触发四检法第②条行动成本，须回商业判断复核结尾承诺与顾客意愿，返工范围与变化程度相称。"
statement_type: BOUNDARY
applies_when: "承接入口更换，且新入口要求顾客提供个人信息。"
does_not_apply_when: "表单只收集咨询内容本身，不索取个人信息。"
counterexample: "以「目标没变、只是换了个入口」为由跳过任何复核直接发布。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
founder_ruling_20260817: "非问题项：顾客提供/不提供联系方式系统各有预案，自动路由，不触发重规划；系统不销售、不发布销售信息"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 专家一 L423、专家二 L1163-1168、专家三 L1789-1794。三份对「触发什么级别的复核」不一致，属真分歧，不作静默归一。"
founder_question: "表单要求联系方式／个人信息时，返工范围按哪一级——整体重新规划（专家一）／内容层部分复核（专家二）／与变化程度相称的商业层复核（专家三）？**裁决前 fail-closed 按最严口径执行：一律触发商业层复核，不得按纯入口更换处理。**"
```

```yaml
elicitation_item_id: ELI-0738
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R02
source_situation: "表单已配置实测，但其字段构成从未提供。"
expert_statement: "表单要求顾客填写的字段最小集（是否含联系方式）须由品牌决定；该变量决定是否触发承接四检法第②条。字段清单到手前，该认定悬置（INSUFFICIENT_CONTEXT），不得以假定字段推进承接验收结论。"
statement_type: FACT
applies_when: "承接入口更换为需要顾客填写的表单。"
does_not_apply_when: "入口不要求顾客填写任何字段。"
counterexample: "假定表单「只填咨询内容」并据此判定局部返工通过。"
candidate_destination: SEMANTIC_LAYER
review_status: ROUTED
founder_ruling_20260817: "界外：系统是内容创意生成系统，不直接涉及销售，表单字段属用户侧运营事项"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S07-R02 专家三 L1722（需要 Founder 决定栏逐字）、L1816、L1823；专家二 L1233 列为 uncertain_point；专家一 L384 只要求「表单是否收集合理信息，不造成额外隐私顾虑」。属具体经营事实，走 F 采集表／A.3，带 SourceRef，未知须显式 UNKNOWN。"
founder_question: "表单字段最小集是否包含联系方式（及其他个人信息字段）？"
```

```yaml
elicitation_item_id: ELI-0739
source_session: DIYU-KE-S07-20260817-001
source_round: S07-R01
source_situation: "目标跨类变化（咨询→成交），但价格、可售库存、承接、履约等经营条件全部齐备，且原正文已覆盖主要购买顾虑。"
expert_statement: "专家二与专家三主张此时可只修改结尾与发布文案（专家二 L329-341 列出五项齐备条件；专家三 L639-649 列出六项须同时满足的条件）；专家一主张改动越过目标类型一线即必须回商业层重判，未给条件出口。本分歧尚未裁决。"
statement_type: BOUNDARY
applies_when: "主要目标类型变化，但成交所需经营事实已全部核验。"
does_not_apply_when: "经营事实存在任一缺口（本场 S07-R01 局面即属此列，三专家在该局面下结论一致：必须回商业层）。"
counterexample: "在经营条件缺失时援引本条出口只改结尾。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
founder_ruling_20260817: "系统自动识别变化层级并路由返工范围，不硬性一刀切（系统具备自动降级/自动路由能力）"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-07.txt 专家一 L41、专家二 L329-341、专家三 L639-649；原文对照审查总报告 L143 明列为「仅 Founder 能决定的事项」并指出不裁则 ELI-0706 带病。"
founder_question: "目标跨类但经营条件全部齐备时，是否允许只改结尾＋发布文案（专家二／三）？还是目标类型线越线一律回商业层重判（专家一）？**裁决前 fail-closed 按最严口径执行：ELI-0706 的目标类型一线不开条件出口。**"
```

---

## 三、来源统计与残留说明

**卡数按 destination 分布（共 39 张：ROUTED 36 / PENDING 3）**

| candidate_destination | 卡数 | 卡号 |
|---|---|---|
| RULE_CANDIDATE | 10 | ELI-0706～0711、0728、0729、0734、0739（PENDING） |
| KERNEL_METHOD | 9 | ELI-0718～0723、0725、0726、0737（PENDING） |
| CASE_REFINEMENT | 7 | ELI-0701～0705、0727、0735 |
| JUDGE_QUESTION | 7 | ELI-0712～0717、0730 |
| CONTRACT_PROPOSAL | 4 | ELI-0724、0732、0733、0736 |
| CASE_CANDIDATE | 1 | ELI-0731 |
| SEMANTIC_LAYER | 1 | ELI-0738（PENDING） |

**provenance 分布**：AI_PROPOSAL_FOUNDER_APPROVED 39｜AI_PROPOSAL_FOUNDER_REVISED 0｜FOUNDER_ORIGINAL_JUDGMENT 0（本场 Founder 为整体批准，未提供可与候选分析区分的原始理由，不得从裁决结果反推）。

**来源轮次分布**：S07-R01 28 张（ELI-0701～0705、0707～0724、0732、0734～0736、0739）｜S07-R02 11 张（ELI-0706、0725～0731、0733、0737、0738）｜其中 ELI-0706 由 R01 卡经 R02 收敛修正，source_round 记 S07-R02。

**未转卡内容及原因**

1. **五张 UNRESOLVED 卡全部不转 ELI 卡**：UN-S07-R01-01（旧咨询版默认处置）／-02（周期性成交战役是否属产品服务范围）／-03（双层审核是否固化为标准发布工序）／-04（候选方法与 B.6、SYS-D01、Preflight、Delivery Validation、Rework Controller 的正式映射）／-05（「卖出一批」数量、时间、付款／发货／退款计量合同）——五项与收口包 PCR-07「返工、战役和发布治理」逐条对应（收口包 L174-183，status: QUEUED），按编译规范第 4.3 条属产品合同问题、不是专家陈述，引用 PCR-07 即可。其中可由专家判断承载的部分已分别落在 ELI-0705（旧版须评估、不自动作废也不自动先发）、ELI-0715／0722（双层审核判据本体）、ELI-0736（失败概念的候选身份与禁止私加）。
2. **HR-S07-R01-01 旧版（「四线任一即绝对触发重判」，且 does_not_apply_when 关死条件出口）不入卡，被 ELI-0706 取代**。取代理由：该断言在 S07-R01 内即存在族内分歧（专家一＝绝对触发；专家二 L329-341、专家三 L639-649＝经营条件齐备时可局部改），两份审查报告点名「把有分歧的断言铸成硬规则、不裁则规则带病」；S07-R02 三专家已就**承接线**收敛出四检法判据，故承接线按收敛版入卡，**目标线**的条件出口仍未裁，另立 ELI-0739（PENDING）并给出 fail-closed 口径。
3. **两个新造状态枚举不沿用**：候选包「使用的事实」节的 `CONFIRMED_CONSTRAINT` / `CONFIRMED_ASSET` 撞排期「不得直接引入新状态、走合同提案」明文（标准对齐复核结论 S07 的唯一加重项）。其内容已改用会议协议第四节既有事实纪律词表重新表达并给出合法去处：约束项→ELI-0734（RULE_CANDIDATE）、资产项→ELI-0735（SYNTHETIC_SCENARIO_OVERLAY 条件下的 CONFIRMED_FACT，去处 CASE_REFINEMENT）。本文件不申请任何新状态值。
4. **停止条件的六个自造中文名（设计暂停／发布暂停／结果承诺暂停／返工停止／任务回退／人工决定）不作为枚举入卡**：其语义已按专家三原文（S-07.txt L736-743）与 S07-R02 专家二／三原文回填为法定三值 INSUFFICIENT_CONTEXT／NO_FEASIBLE_SOLUTION／HUMAN_DECISION_REQUIRED，见 ELI-0732、ELI-0733。两份审查报告点名「E3 明确给出的正式码未登记」，本次找回。
5. **专家原文内部矛盾两处，登记备查，不作静默归一**：① 专家一 L35「价格库存全无、连改成什么样都还无法设计」与 L87 追问 A「补链接即解锁设计、不解锁发布」自相反——ELI-0702 采其对该反事实的直接作答（L87，宽口径），差异写入该卡 source_ref，未经裁决；② 专家二 L451-453 自写「现在商品卡已经放在视频下方，你可以点进去看尺码和库存」，与其自设的「无承接不得催购」红线相反（该局面承接不存在），候选包已正确筛除该口播，本文件不入卡，此处补留筛除痕迹。
6. **事实梯队顺序的三专家差异不归一**：专家一三梯队（承接＋可售结构／履约＋价格授权／成功数量）、专家二五优先级（承接→库存→价格政策→成功数量→履约）、专家三六项（成功口径→库存→价格→路径→履约→商品角色）在「承接与可售结构最先」上一致，在履约、价格、成功数量的先后上不同。ELI-0720 采专家一的三梯队骨架（其分层判据「不清则无法设计／不能发布／不能承诺结果」最可执行），差异在该卡 source_ref 中明示，不写成绝对顺序硬规则。
7. **不逐条转「已确认判断」与编译结论**：候选包 ROUND_RECORD 的 62 条已确认判断、编译结论 20 条、SESSION_CLOSEOUT 的 12 条关键判断与「本场解决了什么」15 行，按编译规范第 6 条与 E.10「不强制每条专家表述进仓库」不逐条立卡，其实质均已由上列 39 张卡承载。候选包 CLOSEOUT 中 8 处「建立了」措辞在本文件一律不沿用（本文件全部内容为候选，无既成事实表述）。
8. **S08 启动规格不在本场转卡**：候选包「下一轮建议」中的「每模块 2—4 份匿名材料」「与正式 Gate 证据分离」已由标准对齐复核结论平反为排期主题 8（L211／硬纪律 a）逐字既有规格，属 S08 场与 PCR-08／EV-04 队列，S07 不重复立卡。
9. **本场无「无源 REJECTED／虚标 provenance」需重新入卡的条目**：原文对照审查总报告认定 S07 的 revised=0／rejected=0 均有明文依据、未沿用「已立」措辞、跨场引用逐项忠实（该报告 S07 第 7 条正面项），故编译规范第 3.5 条在本场无适用对象。候选包「AI_PROPOSAL_REJECTED」节列出的五种做法（仅改 CTA、无差别作废、无承接催购、用成交词替商业重判、因催促虚构事实）不是被否决的专家陈述，其禁止效力已分别落在 ELI-0706～0710、0734 的 counterexample 与 statement 中。
