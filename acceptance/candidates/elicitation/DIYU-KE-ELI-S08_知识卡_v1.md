# DIYU-KE-ELI-S08｜模块真实输出材料采集与封盲正式入库知识卡

```yaml
compiled_document_id: DIYU-KE-ELI-S08-20260817-V1
session_id: DIYU-KE-S08-20260817-001
session_theme: S08 Calibration：模块真实输出匿名判分准备（材料采集与封盲）
source_files:
  - S-08.txt（三份专家原文，忠实版权威）
  - DIYU-KE-S08-20260817-001_S08材料采集与封盲待入库候选包_v1.md（候选包 v1）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S08 节问题清单，逐条修正）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S08 不追问，剩余项分流 PCR-08／EV-04）
  - E_领域专家知识提取协议.md（E.3 卡 schema／E.10 不建设）
  - 知识提取会议排期.md（主题 8：2—4 份匿名材料、两条硬纪律）
ruling_basis: Founder（Faye）2026-08-17 对 S01—S08 候选包整体裁决“可以通过”，指示按 E 协议整理为正式入库知识卡。
expert_index: 专家一＝S-08.txt L1–L127（FOUNDER_REVIEW_SUMMARY＋§1–§10）；专家二＝L128–L295（“一、明确结论”至“结论”）；专家三＝L296–L471（CANDIDATE_RESPONSE，含法定停止码）
compiled_on: 2026-08-17
card_count_total: 28
card_count_routed: 27
card_count_pending: 1
formal_effect: NONE（全部为候选，正式生效另走批准流程）
```

> **前置状态声明**：本场硬前置未满足——Intent／Business Decision／Creative Content 三模块均无会话外真实运行输出，因此本场没有产生任何可判分材料，也没有产生 PASS／FAIL／INCONCLUSIVE 与失败标签。本文件收录的全部是**材料采集与封盲纪律**，不是判分结论。

---

## 一、入库知识卡（ROUTED）

```yaml
elicitation_item_id: ELI-0801
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "S08 首组匿名判分材料准备：手里唯一的成文文本是 S01—S07 专家候选稿，是否可以匿名后充当被评系统输出"
expert_statement: "评估材料铁律：必须产自被评系统的真实运行，会议文本永久不得充当。会议候选稿回答的是『专家认为应该怎么做』，不是『被评系统实际做了什么』；用会议自己的稿子给会议提取的标准打分是自证循环，评估基准从源头失真。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "准备 S08 或其他模块真实输出校准／盲评材料"
does_not_apply_when: "只做方法讨论，不进行输出判分"
counterexample: "将 S01 专家回答匿名为输出 A"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 建议批准1／§1／§7；专家二 一、五；专家三 §1"
```

```yaml
elicitation_item_id: ELI-0802
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "能否在当前会话中现场跑一份『普通 LLM 对照输出』充当基线"
expert_statement: "对照模型的运行必须来自无会议上下文的新会话，与系统侧同输入包、同工具开关、同重试政策。读过全部判分标准、参与制定预期行为的会话等于让阅卷人下场考试——这不是形式瑕疵，是公平性的结构死穴；考出的不是基线是表演。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "生成普通 LLM 或其他对照臂输出"
does_not_apply_when: "判分对象本来就是经过相同知识注入的系统版本，且比较合同明确如此"
counterexample: "在本会议线程中重新问『帮我推广这件大衣』并当作零上下文基线"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 建议批准2／§1／§2 Step2／§5 option C／§7『污染考生』"
```

```yaml
elicitation_item_id: ELI-0803
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "同一匿名比较组的输入应冻结到什么程度"
expert_statement: "冻结输入包：用户原话、商品事实、品牌事实、视觉材料、人为测试条件、业务约束、是否使用网页搜索／数据库／图片理解等额外资料，逐项成文后冻结；所有系统吃同一份，一字不差。任何一处不一致，就不能作为同一组比较。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "形成 A／B／C／D 同组比较前的输入准备"
does_not_apply_when: "不同案例分别独立判分，不做同组比较"
counterexample: "A 看过商品图、B 没看图，却放入同组"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 采集规范表第 1 行；专家二 三.2／三.5；专家三 §2 Step2"
```

```yaml
elicitation_item_id: ELI-0804
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "各臂运行时的工具与重试条件如何统一"
expert_statement: "统一运行条件：工具开关（联网／数据库／图像理解）全组一致——全开或全关，逐份记录；重试政策统一（建议：一次运行不重试，或统一 N 次取首个完成）；记录运行时间。模型／系统／Prompt／工具版本与运行时间记入封存面，不进入 Founder 判分面。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "执行同组真实运行"
does_not_apply_when: "系统能力结构本身不同、差异已预先写入比较合同"
counterexample: "系统侧能看图、对照侧不能看图，却宣称公平比较"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 采集规范表第 2 行／建议批准2；专家三 §2 Step2／Step4"
```

```yaml
elicitation_item_id: ELI-0805
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "已有的几份输出并非来自完全相同的输入，能不能靠删掉多余信息补救"
expert_statement: "一律按冻结后的同一输入包重新运行。删除信息只能改变呈现、改不了生成——多出来的输入早已流进每个判断、每处取舍、每分自信；而且删除本身就是被禁的修改。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "候选输出的输入条件被发现不一致"
does_not_apply_when: null
counterexample: "输入不一致后，通过删掉输出中的额外信息宣称恢复公平"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §6A（追问1裁定）；专家二 三.2；专家三 §5 末段"
```

```yaml
elicitation_item_id: ELI-0806
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "某个候选系统拿不出原始记录、或无法按冻结输入重跑时怎么办"
expert_statement: "拿不出未加工原始记录（含报错原文）的系统退出本组，不以转述或重建代替——重建的『原始输出』是另一种冒充；不可重跑的系统标记为『不可比』，退出本组。宁缺一份，不硬凑一组。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "组装同组匿名材料时发现某臂不可导出或不可重跑"
does_not_apply_when: null
counterexample: "为凑齐四份，把执行人员转述整理的版本当作某臂的原始输出"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §4 第二条假设 impact_if_false／§6A"
```

```yaml
elicitation_item_id: ELI-0807
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "真实运行结果在进入判分前允许做哪些加工"
expert_statement: "原样保存：输出按产生原样存档，含停止、报错、拒答；禁止润色、纠错、删减、重排、补写、摘要、节选。否则 Founder 判的将是执行人员的编辑水平，不是系统。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "保存与展示真实运行结果"
does_not_apply_when: "判分结束后的另行编辑示范，且不再冒充原始输出"
counterexample: "删除一段失败说明，让输出更像完整答案"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 采集规范表第 3 行／§7『化妆样本』；专家二 三.3；专家三 §6"
```

```yaml
elicitation_item_id: ELI-0808
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "某份运行是模型判定资料不足而停止、拒答或要求补充，要不要保留进组"
expert_statement: "行为性停止（模型判定资料不足、拒绝作答、要求补充）完整保留为一等样本。本系列七轮反复确立『知道何时停』是模块质量的核心，一次有据的拒答可能是全组最优答案；剔除失败等于用系统最好的日子评估系统。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "运行未给出完整业务产物，但停止出自模型自身判断"
does_not_apply_when: "运行正常完成"
counterexample: "只收成功运行，失败、停止、拒答被替换（幸存者卷宗）"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §6B（追问2裁定）／建议批准4／§7；专家二 三.3；专家三 §6 第二段／§7"
```

```yaml
elicitation_item_id: ELI-0809
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "运行发生超时、断网、服务端报错，与模型自身停止如何区分处理"
expert_statement: "环境故障与行为性停止分账：可由日志确证为环境故障（超时、断网、服务端错误）的，同输入重跑，原故障件存档备查；无法确证性质的，按原样保留并在材料清单中明示，不由执行人员自行判定『无效』。不得把行为性停止改记为环境故障后反复重跑。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "批次中存在未完成运行"
does_not_apply_when: "全部运行正常完成"
counterexample: "把模型的资料不足停止当成超时后重跑，直到得到完整方案"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §6B／建议批准4；专家三 §6 第二段。**分歧留痕**：重跑范围专家一为该臂同输入重跑替换、专家三为『对全部候选按相同条件重新运行』，本卡只收两者共同部分（原件存档、不静默替换），范围之争已分流 PCR-08"
```

```yaml
elicitation_item_id: ELI-0810
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "输出正文里自称模型名，匿名化允许改到什么程度"
expert_statement: "最小遮盖原则：原始输出唯一允许的触碰是身份指纹（输出内自称模型名、水印性措辞），用中性占位符替换并逐处登记于封存表；文件名与元数据清洗，新建纯文本载体。不得改动其他正文。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "把真实输出转为 Founder 可见匿名面"
does_not_apply_when: null
counterexample: "未登记地删除身份指纹或改写水印性文本"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 建议批准3／§1 采集规范表第 4 行；专家三 §8 末句"
```

```yaml
elicitation_item_id: ELI-0811
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "哪些位置会泄露来源、导致匿名名存实亡"
expert_statement: "指纹泄露面至少包括：标题、文件名、元数据、措辞说明、排版外壳、内部引用、正文自称。任一处揭示来源，匿名即名存实亡，判分退化为品牌印象打分。"
statement_type: FAILURE_MODE
applies_when: "匿名包提交前的泄露面检查"
does_not_apply_when: "判分已冻结并进入揭盲阶段"
counterexample: "匿名包文件名仍带模型名，正文已遮盖便宣称已匿名"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §7『指纹泄露』／§6C（排版习惯亦是指纹）；专家二 三.4；专家三 §7"
```

```yaml
elicitation_item_id: ELI-0812
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "A／B／C／D 的编号怎么分配"
expert_statement: "A—D 编号随机分配并记入封存表——顺序本身会锚定，第一份常被当基准；不得按系统顺序、模型强弱、生成时间或执行人员偏好排列。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "形成 Founder 匿名判分包"
does_not_apply_when: "判分已冻结并进入揭盲阶段"
counterexample: "固定把笛语放在 A"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 建议批准5／§1 采集规范表第 5 行；专家三 §2 Step5"
```

```yaml
elicitation_item_id: ELI-0813
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "字母与真实来源的对应关系放在哪、什么时候能看"
expert_statement: "封存对照表单独成文：字母↔来源系统／模型／Prompt 版本／运行时间／工具条件／故障标记／遮盖处清单；判分完成前判分人不得读取。Founder 完成独立判分冻结后才可揭盲并讨论来源差异。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "生成真实来源映射并交付匿名判分"
does_not_apply_when: "判分已冻结并允许揭盲"
counterexample: "来源映射作为匿名包附件一起发送"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 采集规范表第 6 行；专家二 四；专家三 §2 Step5／§8。保管主体本身未决，见 ELI-0828（PENDING）"
```

```yaml
elicitation_item_id: ELI-0814
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "各份输出格式明显不同，是统一外壳还是保留原版"
expert_statement: "两分法——结构、顺序、措辞、详略是内容，一字不动；字体、标题渲染、空行风格是外壳，可施加同一变换统一之，变换内容记入封存表且可逆。外壳统一的第二个理由是排版习惯本身可能揭盲。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "不同系统输出展示形态差异明显"
does_not_apply_when: "输出仅为纯文本且无版式差异"
counterexample: "为统一展示而改写标题层级、压缩长度或重排段落"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §6C（追问3裁定）；专家三 §6 第三段"
```

```yaml
elicitation_item_id: ELI-0815
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "制作包、拍摄卡片这类交付物，版式差异要不要抹平"
expert_statement: "交付物本身以版式为质量的模块（制作包、拍摄卡片类——可执行性就在排版里）保留原版，让可用性差异被看见；输出内部标题、顺序、段落、长度和格式应保留，因为可用性本身也是判分对象。"
statement_type: BOUNDARY
applies_when: "被评模块的交付物版式直接承担可制作性／可用性"
does_not_apply_when: "输出无版式价值的纯文本模块"
counterexample: "把一份可执行拍摄卡重写成普通段落后再判可制作性"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §6C 例外条款；专家三 §6 what_remains_stable"
```

```yaml
elicitation_item_id: ELI-0816
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "本轮无法交材料，可交付的替代物是什么"
expert_statement: "材料采集六步法：冻结输入包 → 统一运行条件 → 原样保存 → 最小遮盖 → 随机编号 → 封存对照表。六步为顺序依赖，不得先收几份历史答案再事后补齐条件说明。"
statement_type: METHOD
applies_when: "准备第一组及后续模块校准材料"
does_not_apply_when: "已进入判分且材料冻结"
counterexample: "先收几份历史答案，再事后尝试补齐条件说明"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 采集规范表／§10 possible_module_method；专家二 六（11 步流程为同一方法的展开表述）；专家三 §2"
```

```yaml
elicitation_item_id: ELI-0817
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "交给 Founder 的材料与不能交的材料如何切分"
expert_statement: "双包交付：Founder 可见包＝模块名称、同一份用户原始请求、同一份可用事实／视觉材料／测试条件／业务约束／已知缺失、统一工具与运行条件说明、匿名输出 A—D；封存包＝真实来源、模型与 Prompt 版本、工具条件、运行时间、故障标记、遮盖处清单、原始记录位置。判分前不得向 Founder 提供来源映射或执行侧的优劣评价、摘要、推荐顺序。"
statement_type: METHOD
applies_when: "准备正式匿名判分交付"
does_not_apply_when: "判分完成且已正式揭盲"
counterexample: "匿名包里附一句『B 看起来最完整』"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 采集规范表第 6 行／§1 三；专家二 三.5／四；专家三 §8『Founder可见材料包』"
```

```yaml
elicitation_item_id: ELI-0818
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "由谁来做遮盖与编号——做的人必然知道来源，会不会破坏盲评"
expert_statement: "封盲文员分工：知情文员执行遮盖、编号与封存表制作，Founder 只接触匿名面。文员知道来源不损判分公正——判分人不知道才是全部要点；代价与对策是文员不参与业务判分，且在判分讨论轮次中不引用、不暗示来源。"
statement_type: METHOD
applies_when: "需要由第三方处理带来源标签的原始输出"
does_not_apply_when: "自动化管线能够可靠完成封盲且全程可审计"
counterexample: "材料整理人告诉 Founder『B 看起来最像笛语』"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 二／§1 三／§10。封存表由谁保管未决，见 ELI-0828"
```

```yaml
elicitation_item_id: ELI-0819
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "第一组要不要同时覆盖 Intent、Business Decision、Creative Content 三个模块"
expert_statement: "只选一个模块，不强行覆盖三个：哪一个已经具备可复现的运行输入和可导出的真实输出就选哪一个；第一组准备 2—4 份完整原始输出，不为凑齐四份混入不可比结果。"
statement_type: BOUNDARY
applies_when: "启动首组校准材料采集"
does_not_apply_when: "已具备多个模块的同条件可比材料"
counterexample: "因判据清晰就默认 Intent 已能导出可用真实结果"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家二 三.1；专家三 §2 Step1／Step3；『2—4 份』归因《知识提取会议排期》主题 8 会议材料条（非本场新增）。具体选哪个模块与案例待裁，分流 PCR-08"
```

```yaml
elicitation_item_id: ELI-0820
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "三模块均无真实运行输出时，本轮的正确状态是什么"
expert_statement: "维持 MATERIAL_NOT_READY——不提交不存在的真实输出，也不为让流程继续而凑出一组『看似完整』的判分材料；这是正确的处理结果，不是流程失败。该状态维持至会话外真实运行材料到位。（新状态名候选，须走合同提案批准，不得私加状态枚举。）"
statement_type: BOUNDARY
applies_when: "校准材料尚未满足准入条件"
does_not_apply_when: "已取得同条件 2—4 份完整原始输出并通过准入检查"
counterexample: "为推进排期用会议稿凑一组材料，宣称 S08 已启动"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1／§8；专家二 一、结论；专家三 §1"
```

```yaml
elicitation_item_id: ELI-0821
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "任一采集要件缺失时，能不能先开始业务判分、边判边补"
expert_statement: "材料准入先于业务判分：冻结输入、同条件运行、原始输出完整性、遮盖登记、随机编号、封存映射任一缺失，则不进入 Founder 业务判分，维持 INSUFFICIENT_CONTEXT。"
statement_type: BOUNDARY
applies_when: "匿名输出包提交判分前"
does_not_apply_when: "仅保存单次运行记录，不组织判分"
counterexample: "只有 A／B 输出，没有输入事实和工具说明便开始判分"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家二 六（正式提交前必须完成的步骤）；专家三 §8 提交要件七项"
```

```yaml
elicitation_item_id: ELI-0822
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "这批校准材料判完之后，能不能拿去当正式盲测或 Gate 的通过证明"
expert_statement: "本组材料仅用于校准，不得转作正式盲测或 Gate 证据；判分若改动通过边界（允许答案、禁止结果、人工裁判问题），该案例必须升级版本并重新运行两侧——校准材料一经判分人与方法设计者消费即已被消费，不能再充当独立证明。"
statement_type: BOUNDARY
applies_when: "校准输出已用于调方法、改判据或已暴露给判分人"
does_not_apply_when: "从未用于方法调整、且满足正式冻结合同的独立材料"
counterexample: "用同一批 A／B 输出先调标准，再宣称它们证明系统通过"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 一『规范附则』／建议批准清单／§10 possible_hard_rule(e)；专家三 §3 CONFIRMED_FACTS 末条／§6 what_remains_stable；口径与《知识提取会议排期》主题 8 硬纪律 a 同向（非本场新增）"
```

```yaml
elicitation_item_id: ELI-0823
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "本场与后续材料轮的停止条件应落在哪些法定停止码"
expert_statement: "本轮即 INSUFFICIENT_CONTEXT：至少需补齐一个确定的模块与案例、用户原始请求、当次完整事实／视觉材料／测试条件、业务约束、2—4 份完整原始输出、各份工具使用情况、单独封存的来源映射。NO_FEASIBLE_SOLUTION：无法取得任何模块的完整原始运行结果，或无法确认各份结果实际使用了什么输入和工具。HUMAN_DECISION_REQUIRED：同时存在多组符合条件的材料时，需要材料负责人选择第一组案例；选择标准是完整和可比，而不是哪组输出更精彩。"
statement_type: BOUNDARY
applies_when: "校准材料轮需要给出停止结果"
does_not_apply_when: null
counterexample: "为本场另造『材料准备停止』『匿名化停止』等场内专用停止名"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家三 §8（法定三停止码原文映射，逐字采用）"
```

```yaml
elicitation_item_id: ELI-0824
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "已有的 S01—S07 材料留还是不留、怎么摆放"
expert_statement: "S01—S07 可以保留，但不能当判分材料：它们是领域判断提取、方法沉淀、候选包与会议讨论材料，应标记为 DOMAIN_ELICITATION_CANDIDATES，与 S08 判分材料隔离存放；待真实运行输出取得后再单独组织 S08 材料包。（新标记候选，须走合同提案批准，不得私加。）"
statement_type: BOUNDARY
applies_when: "S08 材料区组织与存放"
does_not_apply_when: null
counterexample: "把 S01—S07 与 S08 匿名输出放在同一材料目录，判分时误当系统结果"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家二 五"
```

```yaml
elicitation_item_id: ELI-0825
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "本轮识别出的五类评估失败该不该新增失败标签"
expert_statement: "五个描述性命名——候选稿冒充运行、化妆样本、幸存者卷宗、指纹泄露、污染考生。专家一明示『描述性命名，不提请入册』，专家三对全部禁止结果标 failure_label_candidate: NOT_ASSIGNED。新标签候选须走 B.8.1 覆盖审查，不得私加、不得往 B.6 既有标签塞新语义。"
statement_type: FAILURE_MODE
applies_when: "记录评估流程侧失败模式"
does_not_apply_when: "模块业务失败标签的选择（只能从 B.6 既有标签中选）"
counterexample: "把『幸存者卷宗』直接写进 B.6 标签表当作已生效标签"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §7（含『不提请入册』原文立场）；专家三 §7 五条 NOT_ASSIGNED"
```

```yaml
elicitation_item_id: ELI-0826
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "S01—S07 判据汇编成的判分维度册要不要在判分前发给 Founder"
expert_statement: "维度册可以先编好（Intent：三检验与首问纪律；Business：需求侧证据与角色资格；Creative：声画同证、发言权、可执行三件套）。判前给效率高但会塑形 Founder 判断；判后对照可额外测出『Founder 直觉与已提取判据的一致性』——这本身就是校准的产出。专家一建议判后，发放时机待裁。"
statement_type: METHOD
applies_when: "S08 正式匿名判分的判分协议设计"
does_not_apply_when: "尚无真实材料"
counterexample: "判前强制灌输全部候选标准，却声称测到了未经引导的 Founder 直觉"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §5 option B／§9-2／§10 possible_judge_calibration。发放时机裁决本身分流 PCR-08，本卡只收专家已给出的方法与代价分析"
```

```yaml
elicitation_item_id: ELI-0827
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "一份『没有交付成品』的输出在判分时怎么算"
expert_statement: "不得把所有『未输出成品』统一判 FAIL：一次有据的拒答可能优于三份流畅的错误，行为性停止进入业务质量判断；环境故障进入运行可靠性记录，不参与同一业务质量排序或需明确标注。"
statement_type: BOUNDARY
applies_when: "输出出现拒答、中止、资料不足或未完成"
does_not_apply_when: "运行正常完成"
counterexample: "所有『未输出成品』统一判 FAIL"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §6B；专家三 §6 第二段"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0828
source_session: DIYU-KE-S08-20260817-001
source_round: S08-R00
source_situation: "封盲文员知道来源，封存表交给谁保管才能既不落在文员手上、又在判分完成前不被判分人 Founder 看见"
expert_statement: "专家一在同一份回答内给出两个互斥安排：『封存表产出后仅存于 Founder 处』（§1 二、§1 三）与『封存对照表……判分完成前不见 Founder』（§1 采集规范表第 6 行）。TXT 内无自洽解。专家二、专家三的有源部分只到『单独封存、判分前 Founder 不可见』，均未指定保管主体。稳定边界＝判分人在判分冻结前不可见（已入 ELI-0813）；保管主体待 Founder 裁决。"
statement_type: BOUNDARY
applies_when: "生成真实来源映射并安排保管"
does_not_apply_when: "判分已冻结并允许揭盲"
counterexample: "Founder 作为判分人同时能直接打开未加保护的映射文件"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "封盲映射全部由 Founder 本人保管，Founder 是唯一判定人，不设第三方"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-08.txt 专家一 §1 二／§1 三 vs §1 采集规范表第 6 行（单份内部矛盾）；专家二 四；专家三 §2 Step5"
founder_question: "揭盲前的封存映射由谁保管——Founder 本人持有但承诺判分前不开启、还是交由不参与判分的第三方持有？（本次不采用候选包 v1 的『执行侧／独立文员／指定保管人』三选项，该枚举三份专家原文均无出处，属无源缝合。）该问题同时在 PCR-08 队列。"
```

---

## 三、来源统计与残留说明

### 3.1 卡数与分布

| 项 | 数 |
|---|---|
| 卡总数 | 28 |
| ROUTED | 27 |
| PENDING | 1 |

**candidate_destination 分布**：RULE_CANDIDATE 14（ELI-0801…0814）｜CONTRACT_PROPOSAL 11（0816、0817、0818、0819、0820、0821、0822、0823、0824、0825、0828）｜JUDGE_QUESTION 3（0815、0826、0827）｜SEMANTIC_LAYER 0｜KERNEL_METHOD 0｜CASE_REFINEMENT 0｜CASE_CANDIDATE 0｜BRAND_MEMORY_PENDING_EVIDENCE 0。

**provenance 分布**：AI_PROPOSAL_FOUNDER_APPROVED 28；FOUNDER_ORIGINAL_JUDGMENT 0；AI_PROPOSAL_FOUNDER_REVISED 0（本场 Founder 为整体批准，无逐条修改，不得把候选语言冒充 Founder 原始经验）。

**statement_type 分布**：HARD_RULE_CANDIDATE 13｜BOUNDARY 9｜METHOD 4｜FAILURE_MODE 2｜FACT 0｜PREFERENCE_HYPOTHESIS 0。

### 3.2 按复核报告逐条修正的项

1. **21 卡自造去处枚举全部废弃**：候选包 v1 的 `proposed_destination` 为自由英文短语（Evaluation material admission policy candidate、Blind-review governance candidate、Calibration material pipeline candidate 等 21 条），全部不再使用；本文件一律改用 E.3 冻结八值枚举，`status: PROVISIONAL` 改为 `review_status ∈ {ROUTED, PENDING}`。
2. **6 个自造停止名全部废弃**，改用法定三停止码（ELI-0823 采用专家三原文映射）：材料准备停止／组装停止 → `INSUFFICIENT_CONTEXT`；匿名化停止（无法在不改内容前提下移除指纹）、判分停止（映射已泄露、当前组失去盲评资格）→ `NO_FEASIBLE_SOLUTION`（当前组退出，需重新组织材料）；人工决定 → `HUMAN_DECISION_REQUIRED`；「正式证据停止」不是停止码，其实质是校准与 Gate 的隔离边界，已入 ELI-0822。
3. **CONFIRMED_CONSTRAINT 不复用**：候选包 v1「使用的事实」区的 `CONFIRMED_CONSTRAINT` 是新造枚举（撞排期「不得直接引入新状态、走合同提案」），本文件不使用；相关内容按 E.3 卡内 `expert_statement` ＋ `source_ref` 表达。
4. **专家一单份内部矛盾不作缝合**：候选包用「执行侧／独立文员／其他指定保管人」三选项弥合，该枚举三份原文均无出处，本次不采用；矛盾条转 PENDING 卡 ELI-0828，稳定边界（判分人判分前不可见）单独入 ELI-0813。专家二、专家三无与之冲突的有源方案，故不另立卡。
5. **四附录治理装置不转卡（E.10 红线）**：附录 A.2 冻结输入包字段表、A.4 run 记录 schema（`run_id`／`raw_output_sha256`／`retry_of` 等）、A.6 遮盖登记 schema、A.7 随机编号与封存、A.9 十三项 checklist、附录 B 匿名包模板、附录 C 封存映射 yaml（`custodian`／`access_policy`／`randomization_seed_or_record`），以及全部哈希、ID 登记册、保管权限字段——一律**不建设、不转卡**。核对结果：**「哈希」「登记册」「保管主体」三项在 S-08.txt 三份原文中零出现**，属编译期新增治理装置。其中属专家原文主张的纪律要点已提炼为 ELI-0803（输入包最小成分）、0810（遮盖登记）、0812（随机编号）、0813（封存表内容）、0817（双包边界）、0821（准入先于判分），共 6 张卡。
6. **零 SourceRef 已修复**：每张卡 `source_ref` 指到 S-08.txt 具体专家与小节；非本场原创的口径显式归因（如「2—4 份」归《知识提取会议排期》主题 8）。

### 3.3 未转卡内容及原因

1. **排期硬纪律 b（每条人工判定记录为「人工已判 run」，喂 C.5 judge 校准集，目标 ≥30 条人工已判 run）**：三份专家原文均未讨论此项，非专家陈述，不转 ELI 卡；执行挂接在 **EV-04｜S08 真实匿名材料**（会话外取得真实输出后才可能产生人工已判 run），其合同口径（判分记录格式、入校准集条件）归 **PCR-08｜匿名评估运行合同**。在 EV-04 未交付前，C.5 judge 校准集在 S08 侧为零条目，不得用会议判断补数。
2. **排期硬纪律 a（校准材料 ≠ 正式考卷证据，B.2.1 Manifest 冻结）**：有专家原文支撑（专家一 §1「规范附则」、专家三 §6），已入 **ELI-0822**；排期归因写在该卡 `source_ref`，本文件不重复立卡。
3. **五项未决执行政策**（首组模块与案例、维度册发放时机、对照运行环境标准、运行重试与环境故障替换政策、封存映射保管主体与访问隔离）：已由《S01—S08 集中收口与追问包》分流 **PCR-08｜匿名评估运行合同**，属产品合同问题，按编译规范不转 ELI 卡；其中保管主体一项因涉及专家原文内部矛盾，按本次任务指示另立 PENDING 卡 ELI-0828（内容与 PCR-08 同题，不重复裁决）。
4. **环境故障重跑范围分歧**（专家一：该臂同输入重跑替换；专家三：对全部候选按相同条件重新运行）：真实分歧，不作静默合并，共同部分已入 ELI-0809 并在卡内留痕，范围裁决归 PCR-08。
5. **候选包 v1「只有一份真实输出时……不得复制或改写成多份」**：S-08.txt 三份原文均无此表述，属编译捏合，不入卡（其禁止意图已被 ELI-0807 原样保存纪律覆盖）。
6. **候选包 v1「重跑政策必须在采集前冻结」的强表述**：原文可支撑的是「重试政策统一并逐份记录」（专家一采集规范表第 2 行），「冻结」与「不得事后调整」为编译加强，本文件只收原文强度（ELI-0804），事后政策裁决归 PCR-08。
7. **CASE_REFINEMENT／CASE_CANDIDATE 本场为 0**：专家一明示「本轮不产领域案例；采集规范本身即流程资产」；S08-R00 是材料准入流程轮，不得包装为 Intent／Business／Creative 的新正式案例（E.1／E.8）。
8. **候选包「已确认判断」42 条不逐条转卡**（E.10「强制每条专家表述进仓库」红线）：其判断内容已被本文件 28 张卡覆盖；同场重复表述合并入卡（如专家二「六、正式提交前必须完成的 11 步」与专家一「六步采集法」为同一方法的两种表述，合并入 ELI-0816／0821）。
9. **本场未挂接 B.6 业务失败标签**：无真实输出即无失败标签判定；五个评估流程侧描述性命名按专家原文立场保留为「不提请入册」（ELI-0825）。
10. **待复核项（本编译无法核）**：附录 A／C 与附录 B.2.1 Manifest 冻结机制是否重复建设——附录 B 原文不在库，留给 Founder 核，本文件不因此新建任何冻结机制。
