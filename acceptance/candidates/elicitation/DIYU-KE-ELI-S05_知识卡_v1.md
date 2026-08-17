# DIYU-KE-ELI-S05｜Creative：人设、视频号语法与商业策略承接 正式入库知识卡

```yaml
session_id: DIYU-KE-S05-20260817-001
session_theme: S05 Creative：人设、视频号语法与商业策略承接
compiled_on: 2026-08-17
compiled_by: S05 编译代理（按《ELI 知识卡编译规范 v1》执行）
source_files:
  - S-05.txt                                              # 专家原文，忠实版权威（专家一＝审查报告 A／专家二＝B／专家三＝C，按文件出现顺序）
  - DIYU-KE-S05-20260817-001_S05待入库候选包_v1.md          # 候选包 v1（候选资产区为主要转换对象）
  - DIYU-KE-S02-S07_原文对照审查总报告_20260817.md（S05 节）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S05 节）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S05-R02 QUESTION_CARD、PCR-05）
  - S增补追问专家回答.md（三专家 S05-R02 回答）
ruling_basis: Founder（Faye）2026-08-17 整体批准 S01–S08 候选包＋五张追问卡专家回答＋S09 回答（"专家通过"），指示按 E 协议整理为正式入库文档。
card_count_total: 44
card_count_routed: 39
card_count_pending: 5
formal_effect: NONE（全部为候选，正式生效另走批准流程）
```

> **控制声明**：本文件不修改任何既有文件，不构成 PRD／附录 A/B／生产 Prompt／Rule Engine／正式考卷／Persona 正式枚举／Brand Memory 的变更。所有卡片 `review_status` 只取 ROUTED / PENDING 两值；不新增任何状态枚举。

---

## 一、入库知识卡（ROUTED）

### A. 案例细化（CASE_REFINEMENT）

```yaml
elicitation_item_id: ELI-0501
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "品牌要求创始人第一人称讲『为什么我坚持做这件大衣』，但创始人的真实决策、经历、取舍、语言样本和逐句确认全部未提供。"
expert_statement: "合法答案是拒绝交付历史自述成品，同时给三线并行：①访谈提纲（二十分钟采料，问事实不问情怀，脚本从她的回答里剪出来，不从键盘里编）；②现在时第一人称框架（她出镜、亮真身份、带看两三个可证之处，提词只给结构与看点）；③中性讲述垫场版（商品材料已达标，先推进看懂＋咨询）。不可交付的只有一样：初心自述的成品脚本。"
statement_type: BOUNDARY
applies_when: "内容核心主张依赖创始人亲历，但亲历材料缺失。"
does_not_apply_when: "创始人真实材料完整且逐句确认。"
counterexample: "直接写『我坚持了很多年，终于做出这件大衣』。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S05-R01-01；S-05.txt 专家一 §1(3)（三线最终版逐字）"
```

```yaml
elicitation_item_id: ELI-0502
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "同一件大衣的内容，创始人、店长、中性讲述者、纯商品展示四种讲述者都可能被指派。"
expert_statement: "发言权分布：创始人可讲已确认的决策与理由、她当下的真实（现在为什么愿意出镜、此刻上身什么感受）、以『我』的身份介绍可证商品事实；不可讲未提供的初心、多年坚持、设计过程、个人经历、顾客故事。店长可讲顾客常问什么、试穿时常发生什么、她平时怎么答；不可讲设计理由、选款过程、品牌决策——『懂顾客的问题』不等于『懂创始人的答案』。中性讲述者可讲可查证商品事实与画面可见内容；一切第一人称经历与情感证言不可讲，它的天花板是『清楚』，到不了『亲身』。纯商品展示只讲画面能真实呈现的信息。一句话：职位给的是出镜资格，经历给的才是发言资格。"
statement_type: BOUNDARY
applies_when: "系统需要选择真人或品牌讲述者。"
does_not_apply_when: "内容完全不含个人经历、个人动机或岗位经验主张。"
counterexample: "让店长讲『我们为什么选择这个版型』。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S05-R01-02；S-05.txt 专家一 §1(2) 表、专家二 §二、专家三 §5 发言资格边界表"
```

```yaml
elicitation_item_id: ELI-0503
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "反事实：创始人只确认了一条真实信息——『当时在两种版型之间选择了现在这一种』。"
expert_statement: "该事实立即让一条窄创始人内容成立（真实部分启动信任，画面部分完成看懂，结尾落到咨询），但扩写禁区同时成立：不得长出心路历程（事实只说了『选了』，没说纠结多久、顶住了谁）；不得描述未选版型的样貌与被否理由（未提供，真的只有『存在过另一个选项』这一句）；不得历史化拉伸成『我从开店起就想做这样一件』。一个事实是一个支点：撑得起一句证言，撑不起一部传记；合法的扩写方向是向画面扩，不是向人生扩。"
statement_type: BOUNDARY
applies_when: "只获得一条或少量创始人事实。"
does_not_apply_when: "相应故事细节已有独立来源并经本人确认。"
counterexample: "从『在两种版型之间选了当前版型』扩写出多年纠结和深夜改版。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S05-R01-03；S-05.txt 专家一 §6-A（逐字）、专家二 §七、专家三 §6"
```

```yaml
elicitation_item_id: ELI-0504
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "商业方向已定为『让顾客看懂商品并愿意咨询』，创意侧要决定开头、正文、结尾各写什么。"
expert_statement: "开头负责拦住对的人并提出正文能兑现的问题或观看承诺；正文让话跟着画面走、每讲一个可证的点镜头当场给证据、讲完落一个『你自己怎么判断』；结尾把『愿意了解』变成『来问』而不是『下单』。三段共用一条军规：哪一段答不出『这段怎么推进看懂或咨询』，再动人也砍。"
statement_type: BOUNDARY
applies_when: "商业任务已经明确为『看懂＋咨询』。"
does_not_apply_when: "上游明确批准的是其他商业目标。"
counterexample: "全篇讲创业情怀，结尾才短暂出现商品。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S05-R01-04；S-05.txt 专家一 §1(5)、专家二 §五、专家三 §6 三段表"
```

```yaml
elicitation_item_id: ELI-0505
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "创始人个人材料缺失，但商品图片与基础资料已达普通介绍最低要求。"
expert_statement: "停止的是历史证言这一体裁，不是整个内容任务：商品理解与咨询任务可由店长答问、中性讲述或纯商品展示继续推进；不能因为不能编创始人故事就让商业任务停摆。"
statement_type: BOUNDARY
applies_when: "个人材料缺失而商品事实充分。"
does_not_apply_when: "商品事实本身也不足以支撑任何内容。"
counterexample: "因不能编创始人故事，整个商品内容项目停摆。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S05-R01-05；S-05.txt 专家一 §1(1)『拒绝的只是现在就编成品，任务本身照做』"
```

### B. 硬规则候选（RULE_CANDIDATE）

```yaml
elicitation_item_id: ELI-0506
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "脚本出现『我做过、我选择、我坚持、我经历』等第一人称证言句。"
expert_statement: "证言体中每句第一人称经历必须可指回讲述者本人确认的材料；职位和出镜身份不能单独提供事实来源。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容使用第一人称个人证言（经历、决策、偏好、顾客故事）。"
does_not_apply_when: "仅以官方身份介绍已确认商品事实，且不声称个人经历。"
counterexample: "创始人未提供经历，脚本却写『我推翻了好几版』。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S05-R01-01；S-05.txt 专家一 §10 possible_hard_rule (a)、专家三 §10"
```

```yaml
elicitation_item_id: ELI-0507
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "多个候选讲述者（创始人／店长／中性旁白）可供选择。"
expert_statement: "讲述者选择判据＝谁的真实经历覆盖这条内容的核心主张；禁止按职位、权威感或上镜效果选人。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "多个候选讲述者可供选择。"
does_not_apply_when: "内容无个人经历和岗位经验主张。"
counterexample: "因创始人头衔更高，让她讲未参与的设计过程。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S05-R01-02；S-05.txt 专家一 §10 possible_hard_rule (b)、§1(8)"
```

```yaml
elicitation_item_id: ELI-0508
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "把品牌文案『我们只用好面料』改成『我只想用好面料』后交付真人内容。"
expert_statement: "不得仅将普通品牌文案的主语改为第一人称，便宣称完成了真实主理人表达——身份是真的、话不是她的，既无证言之力，又赔上她的脸。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "创始人、主理人、店长或员工以真人身份出镜。"
does_not_apply_when: "本人逐句确认并确实愿意以自己的话表达。"
counterexample: "『我们坚持好面料』改成『我一直坚持好面料』，来源仍为空。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S05-R01-03；S-05.txt 专家一 §7『换装广告』、专家二 §三"
```

```yaml
elicitation_item_id: ELI-0509
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "店长被指派讲这件大衣。"
expert_statement: "岗位人员不得讲述其未参与、未亲历且无来源的设计理由、品牌决策和创始人动机；店长的可信度来自一线经验，不来自她了解创始人的想法，不得因熟悉顾客就升级为设计理念代言人。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "岗位讲述者被用于商品内容。"
does_not_apply_when: "相应决策已由权威材料确认，且讲述者明确以转述而非亲历口吻表达。"
counterexample: "店长说『我当时决定把肩线改成这样』。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S05-R01-04；S-05.txt 专家二 §二-2、专家一 §1(2) 表"
```

```yaml
elicitation_item_id: ELI-0510
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "创意为追求冲击力，把『看懂＋咨询』改写成催单或泛品牌抒情。"
expert_statement: "Creative 输出不得改变上游已选商业方向；创意的职责是承接既定商业方向，不是重新决定它。开头、正文、结尾都必须能说明其如何推进既定目标。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "上游商业方向已经确定。"
does_not_apply_when: "上游方向正式变更并重新批准。"
counterexample: "『看懂＋咨询』任务被创意改成限时催单。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S05-R01-05；S-05.txt 专家一 §7『方向漂移』"
```

```yaml
elicitation_item_id: ELI-0511
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "为真人证言内容写访谈提纲和提词稿。"
expert_statement: "提词要点制：脚本给结构与看点，不替真人写台词性人生；访谈不得诱导或预写不存在的情绪、冲突和人生经历，脚本只能整理、压缩和结构化已采集的真实内容。说话方式缺失的解法不是模仿她，是把话筒还给她。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "制作真人证言、人物故事或品牌主理人内容。"
does_not_apply_when: "明确属于虚构表演且不会被包装为真人事实；该情形不在本案例范围内。"
counterexample: "提纲暗示创始人回答『你为这件衣服牺牲了什么』。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S05-R01-06；S-05.txt 专家一 §10 possible_hard_rule (c)、§1(3)"
```

```yaml
elicitation_item_id: ELI-0512
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "真人故事或品牌情绪较强的成片准备发布。"
expert_statement: "发布前双测验（换商品测验、复述测验）**不过不发**——它是发布前门禁，不是可选启发式。换商品测验：把大衣替换成任意商品后内容仍成立，即判内容与该商品无关；复述测验：观众看完只能复述情绪、说不出商品值得进一步了解的具体原因，即判『看懂』未完成。任一不过则重剪或换路线，不得发布。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容进入发布前审查环节（真人故事或品牌情绪较强时必查）。"
does_not_apply_when: "上游正式批准的目标本身与具体商品无关（组织叙事），此时换商品测验不适用；复述测验仍随『看懂』目标存续。"
counterexample: "因故事感人而放行一条换成任何商品都照样成立的片子。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家一 §10 possible_hard_rule (d)『发布前双测验（换商品、复述）不过不发』（忠实版）；候选包判断 33/34 的『可以采用』为失真侧，已按审查报告 S05-②改回门禁口径；判分语义见 ELI-0518/0519，执行方法见 ELI-0530"
```

```yaml
elicitation_item_id: ELI-0513
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "准备恢复创始人第一人称内容，需要确定哪些企业信息本来就可以公开讲。"
expert_statement: "所需材料之一是『品牌允许公开表达的事实边界』——哪些设计、采购、生产信息可以讲，哪些不能讲；该授权边界须先确认，不能由内容侧默认可讲。"
statement_type: BOUNDARY
applies_when: "内容将涉及设计、采购、生产等企业内部信息。"
does_not_apply_when: "内容只使用商品资料中已公开确认的可见事实。"
counterexample: null
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家二 §七-5（审查报告 S05-⑤点名『硬规则级素材丢失』4 条之一，候选包未挂卡，本卡按原文补入）"
```

```yaml
elicitation_item_id: ELI-0514
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "正文口播稿在描述大衣。"
expert_statement: "正文不得用评价性语言替代事实——『高级』『显瘦』『有质感』『百搭』这类词不构成商品信息；正文只能讲版型、长度、颜色、穿着方式、适合场景等可确认信息，并由画面指向具体细节。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容目标包含让顾客看懂商品。"
does_not_apply_when: null
counterexample: "『版型超正，穿上巨显瘦，面料超级有质感』——去掉口语词后不提供任何有依据的信息。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家二 §五-2『不能做的』、§六（审查报告 S05-⑤丢失素材之二，本卡按原文补入）"
```

```yaml
elicitation_item_id: ELI-0515
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "成片中的商品画面与顾客实际收到的实物之间的关系。"
expert_statement: "真实可信的构成条件之一是商品展示与实物一致；不夸大、不隐瞒、不制造虚假稀缺。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容包含商品画面展示。"
does_not_apply_when: null
counterexample: null
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家二 §六『真实可信来自』（审查报告 S05-⑤丢失素材之三，本卡按原文补入）"
```

```yaml
elicitation_item_id: ELI-0516
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "采用纯商品展示路线（无真人讲述者）。"
expert_statement: "纯商品展示只有资格讲画面能够真实呈现的商品信息；没有资格讲画面无法证明的材质性能、穿着效果、顾客结论和品牌故事。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "采用纯商品展示或以画面证明为主的路线。"
does_not_apply_when: "相应性能／效果另有可核验资料来源并被明确标注。"
counterexample: "画面只有一件黑色大衣，旁白却说『保暖性能远超同类』。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家三 §5 发言资格边界表『纯商品展示』行（审查报告 S05-⑤丢失素材之四，本卡按原文补入）"
```

### C. 判分校准（JUDGE_QUESTION）

```yaml
elicitation_item_id: ELI-0517
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "审查一份含第一人称句子的脚本。"
expert_statement: "逐句提问：『这句话里的「我」是否真实经历过、是否由本人确认、能否指回材料？』任一答案为否，该个人经历句不得通过。"
statement_type: METHOD
applies_when: "内容包含第一人称决策、经历、情绪或顾客故事。"
does_not_apply_when: "纯商品事实旁白。"
counterexample: "句子很口语、很感人，但没有任何本人材料。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S05-R01-01；S-05.txt 专家一 §10 possible_judge_calibration『逐句「这句的我经历过吗」并指回材料』"
```

```yaml
elicitation_item_id: ELI-0518
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "成片人物故事或品牌抒情很强，需要判定它是否真的关于这件商品。"
expert_statement: "换商品测验的判分语义：把大衣换成任何别的商品，这条内容照样成立＝内容根本不关于这件衣服，判定人物故事或品牌抒情压过了商品任务。该测验是发布前门禁的一半（见 ELI-0512），不通过即回 brief 重剪。"
statement_type: METHOD
applies_when: "商品内容包含较强人物或品牌故事。"
does_not_apply_when: "内容目标本身就是与具体商品无关的组织叙事，且上游已批准。"
counterexample: "把大衣换成鞋或包，脚本无需修改。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S05-R01-02（『可以采用』措辞已按 ELI-0512 门禁口径改回）；S-05.txt 专家一 §6-C『最硬的一条』；正反样本对应 CR_DECISION_DRIFT"
```

```yaml
elicitation_item_id: ELI-0519
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "成片语气自然、故事动人，需要判定『看懂』任务是否完成。"
expert_statement: "复述测验的判分语义：观众看完只能复述创始人情绪或形象，说不出商品值得进一步了解的具体原因＝『看懂』失败。该测验是发布前门禁的另一半（见 ELI-0512）。"
statement_type: METHOD
applies_when: "商业目标包含商品理解。"
does_not_apply_when: "上游目标正式改为纯人物或组织认知。"
counterexample: "观众只记住『创始人很坚持』，不知道大衣有什么值得问。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S05-R01-03（『可以采用』措辞已按 ELI-0512 门禁口径改回）；S-05.txt 专家一 §10、§6-C"
```

```yaml
elicitation_item_id: ELI-0520
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "输出强调『像真人、像主理人、不像广告』，评审要判它是否真的可信。"
expert_statement: "自然语气、方言、停顿和情绪不能单独作为真人内容可信的通过证据；必须同时检查身份可核、内容可验、边界可感、关系可续。判据：去掉口语词和语气后，内容是否还提供有依据的信息——如果没有，就只是伪真实。"
statement_type: METHOD
applies_when: "输出强调真人感、主理人感。"
does_not_apply_when: "仅评价表演流畅度，不评价真实性。"
counterexample: "满口口语词，但核心主张均无来源。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S05-R01-04；S-05.txt 专家一 §1(6)、专家二 §六（判断标准逐字）；校准对应 CR_PERSONA_DRIFT"
```

```yaml
elicitation_item_id: ELI-0521
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "由少量采访材料生成故事段落，评审要判扩写是否越界。"
expert_statement: "一个真实事实的扩写范围受来源边界约束：新增冲突、时长、代价、他人反应或人生意义，应视为新增事实而不是文案润色。"
statement_type: METHOD
applies_when: "由少量采访材料生成故事。"
does_not_apply_when: "新增内容有独立来源并经本人确认。"
counterexample: "从『选了当前版型』写出『我为此熬了无数个夜晚』。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S05-R01-05；S-05.txt 专家一 §6-A、专家二 §七、专家三 §6"
```

```yaml
elicitation_item_id: ELI-0522
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "评审一条完整成片的三段结构。"
expert_statement: "两项对账：①开头承诺与正文兑现对账——Hook 是否合格不看它是否有冲击力，而看正文能否用真实商品信息兑现它；②结尾动作与既定商业方向对账。任一段无法说明其商业作用，判为方向漂移或冗余。"
statement_type: METHOD
applies_when: "商业方向已经明确。"
does_not_apply_when: "内容属于另行批准的纯艺术或组织表达。"
counterexample: "Hook 讲创始人苦难，正文没有商品证据，结尾突然催单。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S05-R01-06；S-05.txt 专家一 §10『开头承诺与正文兑现对账；结尾动作与既定商业方向对账』、专家三 §6；数量级失信样本见 ELI-0538"
```

### D. 模块方法（KERNEL_METHOD）

```yaml
elicitation_item_id: ELI-0523
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "任务同时涉及真人、人设、故事和商品，写作尚未开始。"
expert_statement: "第一步先给体裁定性，因为体裁决定合法来源：文案体吃商品事实，证言体吃亲身经历，答问体吃岗位一线经验。定性一错，后面全部是精致的造假。来源不满足时更换体裁，不用写作技巧填补。"
statement_type: METHOD
applies_when: "任务同时涉及真人、人设、故事和商品。"
does_not_apply_when: "纯非事实虚构创作，且不会被包装为真实经历；该情形不在本案例范围。"
counterexample: "未采集亲历便直接进入创始人故事写作。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-01；S-05.txt 专家一 §2 Step 1（逐字）"
```

```yaml
elicitation_item_id: ELI-0524
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "创始人、店长、员工、买手或中性旁白均可成为候选讲述者。"
expert_statement: "第二步盘『谁手里有什么真实』，产出发言权分布图：逐人列出真实身份、第一手经历、岗位经验、可证商品事实和不可讲范围，再选择讲述者；分布图决定每条路线的天花板。"
statement_type: METHOD
applies_when: "多个人物均可成为候选讲述者。"
does_not_apply_when: "内容无需任何人物发言。"
counterexample: "先选头衔最高的人，再替其补内容。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-02；S-05.txt 专家一 §2 Step 2、专家三 §2 Step 1"
```

```yaml
elicitation_item_id: ELI-0525
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "商品资料充分、人物历史材料不足时的交付编排。"
expert_statement: "三线交付并行：访谈采料恢复原体裁；现在时第一人称保留真人身份但不补历史；中性或店长版本立即完成商品任务。垫场版与采料并行优于『押后整条内容等材料齐』——不能在『编故事』与『全部停工』之间二选一。"
statement_type: METHOD
applies_when: "商品资料充分、人物历史材料不足。"
does_not_apply_when: "商品资料本身不足，或用户已批准其他路线。"
counterexample: "在『编故事』与『全部停工』之间二选一。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-03；S-05.txt 专家一 §1(3)、§5 option C 处置（不选押后）"
```

```yaml
elicitation_item_id: ELI-0526
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "对创始人做二十分钟采料访谈。"
expert_statement: "访谈采料事实优先顺序：具体选择与变化→真实理由→第一手接触→实际顾客问题→本人语言；不先问抽象初心和牺牲。典型问法：『这件衣服哪个细节是你要求改过的』『你自己穿过吗，什么场合』『顾客问过什么让你记住的』——事实到手，情绪自己会跟来。"
statement_type: METHOD
applies_when: "需要采集真人证言。"
does_not_apply_when: "只需中性商品说明。"
counterexample: "一上来问『你为品牌坚持了什么』。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-04；S-05.txt 专家一 §1(3) 一（问题逐字）"
```

```yaml
elicitation_item_id: ELI-0527
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "真人愿意出镜但历史材料不足。"
expert_statement: "现在时转写法：『为什么我坚持』讲不了（过去时、无材料），『我现在最想让你看什么』讲得了（现在时、现场真话）。只采集并表达讲述者此刻可确认的身份、关注点、感受和商品观察，不向过去扩写。"
statement_type: METHOD
applies_when: "真人愿意出镜但历史材料不足。"
does_not_apply_when: "历史故事已经充分采集，或本人拒绝出镜。"
counterexample: "从『我今天想讲这件大衣』扩写成『我多年坚持做这件大衣』。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-05；S-05.txt 专家一 §1(3) 二；S05-R02 三专家收敛后的可发布口径见 ELI-0532/0537"
```

```yaml
elicitation_item_id: ELI-0528
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "判断一条视频号真人内容是否真的可信。"
expert_statement: "视频号可信有四个可点名的来源：身份可核（说话的是谁、跟商品什么关系，一句真话说清）；内容可验（说到哪拍到哪，观众边听边验货）；边界可感（敢说『怕冷选它、要轻薄别选它』——敢说不的人，说是才值钱）；关系可续（评论有人答、上条的问题这条回）。真实感＝可验证＋有边界，不是语气词；语气与表演只是表现层。"
statement_type: METHOD
applies_when: "内容目标包含真人信任和咨询关系。"
does_not_apply_when: "纯静态商品信息页。"
counterexample: "只增加方言和停顿便宣称真实可信。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-06；S-05.txt 专家一 §1(6)（逐字）"
```

```yaml
elicitation_item_id: ELI-0529
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "把既定商业方向钉进内容的三段结构。"
expert_statement: "三段功能锚：开头拦住对的人——钩子只能来自真身份或真问题，两种都合法：身份钩子（『我是这家店的创始人』，账号首次出真人，本身就是停留理由）与商品问题钩子（『这件大衣值不值得多看，我带你看三个地方』）；正文教会看——话跟着画面走，人是导览不是主角，讲完落一个『你自己怎么判断』；结尾引来问——把愿意了解变成咨询动作，CTA 是『来问』不是『下单』。每段答不出商业作用则删改。"
statement_type: METHOD
applies_when: "商业目标为商品理解和咨询。"
does_not_apply_when: "上游另行批准不同目标和内容结构。"
counterexample: "情绪开头、故事正文、催单结尾与目标断裂。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-07；S-05.txt 专家一 §1(5)（身份钩子在候选包中被静默收窄为『只能是商品问题』，本卡按原文恢复两种合法钩子——审查报告 S05-④）"
```

```yaml
elicitation_item_id: ELI-0530
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "成片进入发布前审查。"
expert_statement: "发布前三查方法：换商品测验查商品特异性、复述测验查信息有效性、商业方向对账查上下游一致性。三查的执行动作是逐项走查并给出通过／不通过结论；其中双测验的通过与否直接决定能否发布（门禁口径见 ELI-0512），不通过则回 brief 重剪，不通过情绪包装掩盖。"
statement_type: METHOD
applies_when: "真人故事或品牌情绪较强。"
does_not_apply_when: "纯事实短说明且无故事内容；商业方向对账仍适用。"
counterexample: "因故事感人而忽略商品已变成背景。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S05-R01-08；S-05.txt 专家一 §6-C、§10"
```

```yaml
elicitation_item_id: ELI-0531
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "创始人历史材料不足，内容侧必须决定停到哪、以及能不能自行换讲述者。"
expert_statement: "停止与移交义务：①创始人历史自述停在四件材料齐备之前（材料集合本身未收敛，见 ELI-0543）；②现在时版本停在创始人拒绝出镜或试拍证明不可用之时；③用户坚持『没有材料也要写出感人初心』时该形式拒绝交付，三线替代照常给，去留由用户；④讲述者或体裁的更换不得静默进行，必须由用户在合法路线之间作业务选择（HUMAN_DECISION_REQUIRED），并让用户知道讲述者和内容来源发生了变化。会议中使用的 TESTIMONIAL_STOP / CREATIVE_REWORK 仅为会议描述用语，不新增正式状态。"
statement_type: BOUNDARY
applies_when: "个人材料缺失、需要在体裁与讲述者之间改道时。"
does_not_apply_when: "材料齐备且原体裁可直接完成。"
counterexample: "内容侧自行把创始人版换成店长版并直接交付，不告知用户。"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 停止条件节＋判断 38；S-05.txt 专家一 §8、§5 option B『不得静默换人』、专家三 §8 HUMAN_DECISION_REQUIRED"
```

### E. S05-R02 追问轮收敛结论（三专家收敛，最终版）

```yaml
elicitation_item_id: ELI-0532
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "单变量改变：创始人愿本人出镜，现场用自己的话确认一条当下真实表态（『这是我第一次正式在账号里讲这件大衣，我现在最想让大家看清三个地方』），随后只讲已有证据的商品事实。"
expert_statement: "来源分界硬规则：现在时自证／历史需证。说话人就是自己当下意图的唯一权威来源，她当场说出即为证，不需要历史档案；历史陈述（设计历程、耗时、长期坚持、个人穿着史、顾客故事、回忆式情绪、『我们一直……』）无材料一律不可讲。因此『创始人缺史』不构成本条内容的阻断——全程没有一句需要历史材料支撑。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "真人出镜、内容含第一人称表述。"
does_not_apply_when: "内容不含任何第一人称表述。"
counterexample: "由当前出镜意愿推导出『她过去参与过决定、存在持续坚持』。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 三专家收敛（专家三『说话人就是自己当下意图的唯一权威来源』逐字；专家一『现在时第一人称不等同于历史证言』；专家二 Step 1–2）"
```

```yaml
elicitation_item_id: ELI-0533
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "给这条现在时第一人称内容命名、起标题、做封面。"
expert_statement: "该内容最多只能被命名为『创始人现场介绍／创始人当下真实表态／创始人出镜的商品讲解（导览）』；标题只能承诺在场与当下（如『创始人第一次正式讲这件大衣』）。禁用『为什么我坚持做这件大衣』『我的设计初心』『这件大衣背后的故事』『我准备了三年』『这是我的答案』等历史向命名与封面——即使内文合法，这些标题也会把合法的现在时内容重新包装成不存在的历史证言，构成误导。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容主体为现在时第一人称或主持人式商品介绍。"
does_not_apply_when: "历史材料齐备并经本人逐句确认，历史向命名的对应部分随之解禁。"
counterexample: "内文只讲当下与商品事实，标题却写『为什么我坚持做这件大衣』。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 三专家收敛（三份均给出同向命名边界；专家三另命名候选失败标签 TITLE_UPGRADE_TO_HERITAGE，见 ELI-0539）"
```

```yaml
elicitation_item_id: ELI-0534
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "审稿环节检查标题与封面。"
expert_statement: "标题违禁词表作为审稿硬检查项：初心／坚持／背后的故事／一直／多年／为什么我做。命中任一词而正文无对应历史材料，即判命名越过来源边界。"
statement_type: METHOD
applies_when: "现在时第一人称或无历史材料的真人内容送审。"
does_not_apply_when: "对应历史材料已确认并进入正文。"
counterexample: "『这件大衣，我一直想做』配一条只有当下表态的正文。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 三专家收敛（专家三 §10 possible_judge_calibration 逐字词表；专家一『哪些标题会把合法内容重新包装成非法历史证言』清单同向）"
```

```yaml
elicitation_item_id: ELI-0535
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "脚本人员要决定给创始人写逐字台词还是给要点。"
expert_statement: "脚本只给结构＋问题清单＋必须覆盖的事实点＋不可说边界（禁止使用的历史或情绪表述），不写她个人表态部分的逐字台词。分工是『精确性归写手（商品事实）、真实性归本人（当下表态）』：仅商品事实需要逐字级精确，数字与材质可由字幕承担或口播前看一眼事实卡。即使创始人自己要求稿子，也必须由她确认每一句，而不是写手替她完成后再让她照念。"
statement_type: METHOD
applies_when: "真人出镜讲述含第一人称表态的内容。"
does_not_apply_when: "纯中性旁白或纯字幕内容。"
counterexample: "写手起草情绪与经历台词、创始人照读。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 三专家收敛（专家一『只提供问题和要点，不写逐字台词』；专家三『精确归写手、真实归本人』；专家二『简短开场提示＋事实要点』为同向变体，其逐字开场提示以创始人认同为前提）"
```

```yaml
elicitation_item_id: ELI-0536
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "如何确认『这是我第一次正式讲这件大衣』『我现在最想让你看什么』确实是她本人的话。"
expert_statement: "『她说→我们记』采集法：现场开放提问（『你现在最想让顾客注意什么？为什么是这三处？』）、录她原话、用她的措辞；检验标准是拿掉提词她仍能用自己的话说出，且意思由她先说。脚本只能标记『这里由创始人用自己的话表达第一人称开场』。如果这句话是写手先写好再让她念，她就是念稿演员，不是真实主理人。"
statement_type: METHOD
applies_when: "内容含创始人当下表态、当下感受。"
does_not_apply_when: "内容不含任何本人表态，只有可证商品事实。"
counterexample: "写手先写好当下感受句，拍摄时让创始人照念。"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 三专家收敛（专家三『她说→我们记』逐字；专家一『正确流程』；专家二 Step 2）"
```

```yaml
elicitation_item_id: ELI-0537
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "同一冻结局面的单变量变体：无任何历史故事，但创始人可现场说出当下真话。"
expert_statement: "判例结论：这条创始人第一人称内容可以制作并发布。可讲范围＝身份、当下表态、逐一落在有据事实与实拍画面上的『看清处』、诚实邀请咨询；不可扩写到设计历程与理由、投入时长、个人穿着史、顾客故事、回忆式情绪、任何『我们一直……』——哪怕补半句，来源就从『她当场说的』变成『写手替她编的』。发布前须先修正 Hook 数量缺口（见 ELI-0538）。"
statement_type: BOUNDARY
applies_when: "创始人愿出镜、能现场确认当下表态、商品事实已有证据。"
does_not_apply_when: "创始人拒绝出镜／试拍不可用，或商品事实本身无证据。"
counterexample: "以『可以发布』为由，把当下表态顺势扩写成设计历程。"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 三专家收敛（三份均判『做，可发布』；专家三 §10『「有当下真话、无历史故事」作为创始人内容标准判例』）"
```

```yaml
elicitation_item_id: ELI-0538
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "开头承诺『我现在最想让大家看清三个地方』，正文却只有两条已有证据的商品事实。"
expert_statement: "失败模式——承诺-兑现数量缺口：Hook 承诺三个，正文只兑现两个；即使每句话都真实，内容结构仍然失信。修正只有两条合法路径：把开头改成『两个地方』，或补齐第三个有证据且能被画面证明的内容。判分动作＝把 Hook 中的可计数承诺逐项与正文兑现项对账（承接全场已共识的『开头承诺什么，正文必须兑现什么』规则，见 ELI-0522）。本失败模式在 S05-R02 由三份回答中的两份复现而未察（专家一、专家三均照搬『三个地方』＋两条事实），仅专家二抓出并给出修正——该复现本身即该缺口类型难以自审的实证。未指派 B.6 标签（专家二原文 failure_label_candidate: NOT_ASSIGNED），不得私加标签。"
statement_type: FAILURE_MODE
applies_when: "Hook 含可计数承诺（几个地方、几点、几个问题）。"
does_not_apply_when: "Hook 不含可计数承诺。"
counterexample: "『带你看三个地方』，正文只给两处并以情绪补足第三处。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 专家二（§1 直接候选结论、§7 forbidden_outcome『Hook承诺三个地方，正文只兑现两个』逐字）；缺口复现见专家一『看清三个地方』段与专家三 §1／§2 Step 2"
```

```yaml
elicitation_item_id: ELI-0539
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "专家在 S05-R02 回答中为三类失败自行命名了新标签。"
expert_statement: "新失败标签候选三条：GHOSTWRITTEN_TESTIMONY（写手起草情绪与经历台词、创始人照读，第一人称的真实来源变成写手）、TITLE_UPGRADE_TO_HERITAGE（现在时内容配历史向标题或封面，命名承诺的来源在正文中不存在）、PERFORMED_AUTHENTICITY（用口语、停顿、情绪词设计『真实感』，以表演性状冒充来源真实）。三者均为新标签候选，须走 B.8.1 覆盖审查（先检既有 B.6 标签能否覆盖），不得私加标签、不得往既有标签塞新语义。S-05.txt 中专家一对其描述性失败命名明写『不提请入册』、专家三六条 forbidden 全标 NOT_ASSIGNED，该保留态度一并记录。"
statement_type: FAILURE_MODE
applies_when: "真人第一人称内容的失败归因与判分标签指派。"
does_not_apply_when: "既有 B.6 标签已能覆盖该失败语义。"
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 专家三 §7（三个 failure_label_candidate 逐字）；保留态度见 S-05.txt 专家一 §7 题注、专家三 §7"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0540
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "恢复『为什么我坚持做这件大衣』历史型自述所需的最低材料集合。"
expert_statement: "三位专家给出三个互不相同的门槛，TXT 本身未收敛：专家一＝四件缺一不可（真实决策点及理由／与商品的第一手接触／她自己的话的样本／她对成稿的逐句确认）；专家二＝『以下材料中的一部分』即可，并明写『一条具体真实的决策信息，比十句「我坚持」更重要』，一句确认过的选择即可支撑一小段真实自述；专家三＝七项（含创始人确认实际参与、具体选项与选择、选择理由、如何体现在商品上、若讲代价须有确认的取舍、语言样本、逐句确认）。候选包判断 35 单取四项写成已确认判断，属单源未标。"
statement_type: BOUNDARY
applies_when: "拟制作历史型第一人称自述。"
does_not_apply_when: "只做现在时第一人称或非个人证言内容。"
counterexample: "用一个选择事实承载完整长期故事。"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
founder_ruling_20260817: "人设或商品事实任一成立即可创作，不设四项等多重门槛；基本原则＝真实感、烟火气、拒绝AI味、允许不完美/残缺美"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 UN-S05-R01-05；S-05.txt 专家一 §1(7)、专家二 §七、专家三 §6（三门槛逐条定位见审查报告 S05-②）；同题的产品合同侧已在 PCR-05 排队"
founder_question: "历史证言最低材料取哪一版：固定四项缺一不可（专家一），还是随内容主张范围伸缩、一条确认过的决策事实即可支撑等量窄内容（专家二／专家三的相称口径）？"
```

```yaml
elicitation_item_id: ELI-0541
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "真人内容中出现真实情绪流露，剪辑侧要决定能放大到什么程度。"
expert_statement: "配乐、慢镜、重复、停顿等剪辑手段对真实情绪的放大，何时仍是『记录真实流露』、何时变成『制造表演』，专家明确列为需 Founder 裁定的尺度分界；已给出的唯一方向性判据是：若情绪剪辑改变了事实含义、制造不存在的冲突、或让普通停顿看起来像沉重证言，即为越界。更精确尺度留待 S06 制作方法校准。"
statement_type: BOUNDARY
applies_when: "真人内容存在真实情绪流露或希望增强感染力。"
does_not_apply_when: "纯商品旁白无情绪叙事。"
counterexample: "用重配乐和重复剪辑把普通停顿塑造成沉重证言。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
founder_ruling_20260817: "采纳三条越界线（改变事实含义/制造未发生冲突/普通停顿剪成沉重告白），服务于真实感原则"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 UN-S05-R01-02；S-05.txt 专家一 FOUNDER_REVIEW_SUMMARY『需要 Founder 决定』第 2 条、§9 uncertain_points 2"
founder_question: "情绪剪辑（配乐／慢镜／重复／停顿）从『记录真实流露』变成『制造表演』的分界画在哪里；是否直接采用『改变事实含义／制造不存在的冲突／把普通停顿塑造成沉重证言』三条作为越界判据，其余交 S06 校准？"
```

```yaml
elicitation_item_id: ELI-0542
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R02
source_situation: "创始人首次出镜讲这件大衣，后续内容如何排布尚未确定。"
expert_statement: "创始人出镜是本条内容的一次性安排，还是账号长期人格起点——影响后续内容排布，专家明确判定非本卡可定，路由 Founder。（关联既有判断：创始人第一条真人内容若以虚构经历建立信任，会损害整个账号后续真人化路线；风险对象包括创始人个人信用与账号长期信任。）"
statement_type: BOUNDARY
applies_when: "决定创始人真人内容的后续排布与账号人格策略。"
does_not_apply_when: "只裁决本条内容能否发布——该问题已收敛为可发布（ELI-0537）。"
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "人设为长期锚（人设不变、创始人不变）；出镜形式不规定死：真人/口播配音/无真人均合法，按内容自动路由，不必每次出镜"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S05-R02 专家三 FOUNDER_REVIEW_SUMMARY『需要 Founder 决定』唯一条＋§8 HUMAN_DECISION_REQUIRED（追问轮残留，未被三专家收敛覆盖）"
founder_question: "创始人出镜按一次性安排处理，还是确立为账号长期真人人格的起点（后者会连带决定后续内容排布与采料节奏）？"
```

```yaml
elicitation_item_id: ELI-0543
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "人物历史材料缺失时，内容侧交付物里可否包含带占位符的脚本骨架。"
expert_statement: "两位专家在本场新局面正面主张该形态合法：专家二＝『提供第一版受限脚本框架，可以写出开头、正文、结尾的结构，但故事部分留空，标注「待创始人补充真实材料后填充」』＋『提供问题清单』；专家三＝『带事实占位符的内容结构』＋『等待创始人确认的第一人称句子清单』。该主张与 S01 未决项 UN-S01-05（受限输出可否包含占位内容骨架／任务结构模板）同题，不得在 S05 内自行裁断。"
statement_type: BOUNDARY
applies_when: "材料不足导致输出受限，需确定最大合法交付形态。"
does_not_apply_when: "材料齐备可直接完成成品。"
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "同 ELI-0124：2–3方案供选，UN-S01-05 关闭"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家二 §三-3/§三-4、专家三 §6『当前最多能够交付』（候选包整条丢失，本卡按原文补入）；并入 UN-S01-05 证据链（S01 v3 包 L44/L54/L606），裁决前 fail-closed 按 CR-S01-R01-02『只允许条件化选项菜单』口径执行"
founder_question: "S05 这两票新证据计入后，UN-S01-05 如何裁：受限输出可否包含占位内容骨架／留空脚本框架／待确认句子清单，还是维持『只给条件化选项菜单』的 fail-closed 口径？"
```

```yaml
elicitation_item_id: ELI-0544
source_session: DIYU-KE-S05-20260817-001
source_round: S05-R01
source_situation: "店长出镜时，能不能说『很多顾客会担心……』这类概括顾客侧的句子。"
expert_statement: "同型句在两份原文中一判可信、一判否决：专家二把『很多顾客会担心长款大衣压个子，这件大衣其实是 H 型……』作为真实可信的正面样例（来源＝她面对顾客的经验且未过度承诺）；专家三把『很多顾客试过以后都说显瘦』列为一票否决（店长知道常见问题≠存在该顾客反馈与效果证据）。两句的差别可能在于『顾客的顾虑』与『顾客的效果结论』之别，但原文未做此区分，该边界在本场未被披露也未收敛。"
statement_type: BOUNDARY
applies_when: "岗位讲述者概括顾客侧信息（常问、常担心、试后反馈）。"
does_not_apply_when: "讲述者只陈述自己对单个具体顾客问题的处理经过。"
counterexample: "『很多顾客试过以后都说显瘦』——无记录支撑的顾客效果结论。"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
founder_ruling_20260817: "凭真实岗位经历可讲（常问/常担心类），不设多重记录门槛；编造仍禁（真实感原则）"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-05.txt 专家二 §六 正面样例 vs 专家三 §7 forbidden_outcome 第 4 条（审查报告 S05-④『未披露真差异 2 处』之一）"
founder_question: "店长概括顾客侧的合法句式边界怎么划：『顾客常问／常担心什么』（她的岗位经历直接覆盖）可讲、而『顾客试后效果结论』必须有记录才可讲——是否按这条分界收口，还是两类都要求可核记录？"
```

---

## 三、来源统计与残留说明

**卡数与 destination 分布（共 44 张：ROUTED 39／PENDING 5）**

| candidate_destination | ROUTED | PENDING | 合计 |
|---|---|---|---|
| CASE_REFINEMENT | 6 | 0 | 6 |
| RULE_CANDIDATE | 13 | 1 | 14 |
| JUDGE_QUESTION | 8 | 2 | 10 |
| KERNEL_METHOD | 10 | 0 | 10 |
| CONTRACT_PROPOSAL | 2 | 2 | 4 |
| SEMANTIC_LAYER / CASE_CANDIDATE / BRAND_MEMORY_PENDING_EVIDENCE | 0 | 0 | 0 |

**provenance 分布**：AI_PROPOSAL_FOUNDER_APPROVED × 44；FOUNDER_ORIGINAL_JUDGMENT × 0；AI_PROPOSAL_FOUNDER_REVISED × 0。S05 无 Founder 逐条裁决与修改，按编译规范 §3.1 全部记为整体批准；PENDING 卡的 provenance 同样记为整体批准（被批准的是"该问题待裁"这一状态，未决性由 review_status 承载），不使用规范三值之外的取值。

**忠实版覆盖的三处包内失真**

1. **双测验**：候选包判断 33/34 的"可以采用"为失真侧；忠实版为发布前门禁"不过不发"（S-05.txt 专家一 §10-d），已立 ELI-0512 为规则卡，ELI-0518/0519 只承载判分语义并回指门禁。
2. **身份钩子**：候选包把开头收窄为"只能是真实商品问题"；忠实版两种钩子（真身份／真问题）均合法，已在 ELI-0529 恢复。
3. **历史证言最低材料**：候选包判断 35 单取专家一四项写成已确认判断；三份原文实为三门槛且未收敛，改立 PENDING（ELI-0540），ROUTED 层无任何卡断言"四项缺一不可"。

**未转卡内容及原因**

- **产品合同项，引用 PCR-05，不转卡**：①"现在时第一人称"是否成为正式创始人内容类型及其与主持人式介绍、历史证言的正式命名与验收边界（专业侧已由 S05-R02 收敛，见 ELI-0532/0533/0537；剩余为枚举与合同裁决）；②创始人访谈是否纳入产品正式工序、访谈提纲是否为正式交付物、谁采集确认保存原始材料；③咨询型结尾是否要求发布前确认承接人、渠道、时限与升级路径。对应候选包 UN-S05-R01-01/03/04。历史证言最低材料一题虽同在 PCR-05 队列，因属专家陈述未收敛冲突，另立 ELI-0540。
- **被 S05-R02 取代的旧口径不再单独立卡**：候选包判断 5／编译结论 5／UN-01 对"创始人三层级"的三态不一致（现在时第一人称与主持人式介绍是否同一形态），已被追问轮收敛为——现在时第一人称＝创始人出镜的商品讲解／导览（主持人式），与历史证言二分，来源分界见 ELI-0532。
- **不逐条转"已确认判断"清单**：候选包 42 条已确认判断中未挂候选卡的表述性重复项不再单独立卡（E.10"强制每条专家表述进仓库"红线），其实质内容已被上述 44 张卡覆盖。
- **失败标签保留态度**：ELI-0518/0520 沿用候选包的 CR_DECISION_DRIFT／CR_PERSONA_DRIFT 路由（该路由已由标准对齐复核平反为主题 5 预期产出），但 S-05.txt 中专家一"不提请入册"、专家三六条 forbidden 全标 NOT_ASSIGNED 的保留态度一并记录于此，映射既有标签不等于抹去专家的保留。
- **本场无 SEMANTIC_LAYER / BRAND_MEMORY_PENDING_EVIDENCE 卡**：S05 全部输入事实为 SYNTHETIC_SCENARIO_OVERLAY（构建期设定的商业方向、商品资料水平、渠道状况、创始人与店长材料状态），不得写入企业语义层；本场亦无经真实运行证据佐证的品牌偏好，不产生 Brand Memory 候选。
