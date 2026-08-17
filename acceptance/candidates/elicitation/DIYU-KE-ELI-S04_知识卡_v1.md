# DIYU-KE-ELI-S04｜Business 候选差异真实性正式入库知识卡

```yaml
document_id: DIYU-KE-ELI-S04-20260817-V1
session_id: DIYU-KE-S04-20260817-001
session_theme: S04 Business：多个候选如何真正不同（含 S04-R02 穿搭计数收敛）
covered_rounds:
  - S04-R01
  - S04-R02
source_files:
  - DIYU-KE-S04-20260817-001_S04待入库候选包_v1.md（候选包 v1）
  - S-04.txt（S04-R01 三份专家原文；按原文出现次序记为专家甲／乙／丙；忠实版权威）
  - S增补追问专家回答.md（S04-R02 三份专家原文；按文件出现次序记为专家一／二／三）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S04-R02 QUESTION_CARD；PCR-04 队列）
  - DIYU-KE-S02-S07_原文对照审查总报告_20260817.md（S04 节）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S04 节）
  - 知识提取会议排期.md（主题4：BD-D02／BD-D03／BD_SCOPE_MISREPRESENTED／BD_CANDIDATE_COLLAPSE 出处）
ruling_basis: Founder（Faye）2026-08-17 裁决——S01–S08 候选包、五张追问卡（含 S04-R02）专家回答与 S09 回答全部批准通过，指示按 E 协议整理为正式入库知识卡
compiled_on: 2026-08-17
card_count: 34
routed: 34
pending: 0
destination_distribution:
  KERNEL_METHOD: 12
  RULE_CANDIDATE: 7
  JUDGE_QUESTION: 6
  CASE_REFINEMENT: 4
  CONTRACT_PROPOSAL: 4
  CASE_CANDIDATE: 1
formal_effect: NONE（全部为候选，正式生效另走批准流程）
```

---

## 一、入库知识卡（ROUTED）

### A. 计数本体与三层分界（S04-R01）

```yaml
elicitation_item_id: ELI-0401
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "三件商品（黑色长款大衣、米白圆领针织衫、荧光绿直筒裤）被要求做出十套彼此明显不同的完整穿搭"
expert_statement: "采用三层分界法：穿搭／商品组合层＝身上的商品清单变了；穿法／造型变体层＝清单没变、只改变开合、塞放、卷放或露出比例；拍法／内容表达层＝商品与穿法都没变、只改标题、场景、镜头、动作、口播、情绪。三层分别计数、分别交付，禁止跨层冒充。唯一检验标尺是顾客行为：照着这条内容去买、去穿，需要动用的商品变没变——变了才是新方案，没变只是我们换了说法。"
statement_type: METHOD
applies_when: "同一批商品需要形成多个方案或多条内容；输出声称存在多个明显不同方案"
does_not_apply_when: "任务只有单一方案且无数量要求"
counterexample: "用十个拍摄场景计算十套穿搭"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S04-R01-01／已确认判断 7、8；S-04.txt 专家甲 §1(1) 三层表与检验标尺、专家乙\"真正不同穿搭／同一套穿搭的不同穿法／造型处理或拍摄表达\"三段、专家丙 Step2 三层表"
```

```yaml
elicitation_item_id: ELI-0402
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "输出声明多个穿搭、陈列或商品组合候选时的计数基础"
expert_statement: "穿搭方案数量必须以正式允许的商品集合或核心商品关系为计数基础；商品集合不变时，开合、塞放、动作、镜头和文案变化不得自动增加穿搭数量。同一商品集合即使存在穿法变化，也必须明确标记为'同一穿搭的变体'，不能在未说明的情况下计入新套数。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "输出声明多个穿搭、陈列或商品组合候选"
does_not_apply_when: "正式合同另行定义'造型变体'为独立交付单位，并与穿搭分开计数"
counterexample: "大衣敞开和扣上分别登记为两套完整穿搭"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S04-R01-01／已确认判断 9；S-04.txt 专家甲'方案计数单位＝商品集合；集合不变，不计新套'。编译注：审查报告 S04 第3点指出本条判据主体中'或核心商品关系'在 R01 时点属未决口径；该口径已由 ELI-0427（S04-R02 三专家收敛）确定为'商品集合×层次结构×商品角色'三元组，本卡与 ELI-0427 合并适用"
```

```yaml
elicitation_item_id: ELI-0403
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "内容表达层变化是否增加穿搭数量"
expert_statement: "更换标题、场景、镜头顺序、口播角度或情绪不会自动产生新穿搭。"
statement_type: BOUNDARY
applies_when: "对同一商品集合生成多条内容或多个方案编号时的计数判断"
does_not_apply_when: "计数单位已显式改名为'内容条数'并与穿搭套数分开验收"
counterexample: "同一套穿搭换十个标题后声称完成十套"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 L125（原标 `CONFIRMED_FACT`）；S-04.txt 专家甲 §3 CONFIRMED_FACTS、专家丙 §3 CONFIRMED_FACTS 同槽位。编译注：审查报告 S04 第5点已坐实——本句是方法论断言而非企业事实，槽位性质尚待 QUESTION_CARD 佐证，故本卡按 BOUNDARY 登记，不使用 statement_type: FACT"
```

```yaml
elicitation_item_id: ELI-0404
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "用户要求固定数量（十套）的不同商业方案"
expert_statement: "在接受数量承诺前，必须先计算给定商品池的合法组合上限；上限不足时，不得先承诺再通过重复、虚构或单位偷换补足。数量边界来自商品结构而不是模型能力——它来自算术，不来自技巧。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "用户要求固定数量的不同商业方案"
does_not_apply_when: "任务数量只表示内容条数，且内容单位已明确"
counterexample: "先承诺十套，再把同一组合改写十次"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S04-R01-02／编译结论 3；S-04.txt 专家甲 §1(2)'这个边界是专业的，因为它来自算术不来自技巧'"
```

```yaml
elicitation_item_id: ELI-0405
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "商品池不足以支撑要求的方案数量"
expert_statement: "不得在候选中使用未进入当前商品池的商品；需要扩大方案空间时，只能列出品类缺口或请求补入真实确认的商品，不得虚构具体商品。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "方案依赖具体服装、鞋包或配饰"
does_not_apply_when: "用户已明确授权并确认新增商品（新增商品必须实际存在、已确认、可被调用）"
counterexample: "无来源地加入白衬衫和牛仔裤完成十套"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S04-R01-03／已确认判断 14；S-04.txt 专家甲'幽灵商品'、专家乙'擅自虚构白衬衫、牛仔裤、鞋、包、首饰'、专家丙'偷带…未提供商品'"
```

```yaml
elicitation_item_id: ELI-0406
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "被要求从多个合法候选中推荐'最好的一套'"
expert_statement: "唯一推荐必须有判据主语：为了什么目标、对谁、在什么场景、优先控制什么风险。判据主语不足或缺少真实上身比较时，不得把某候选标成无条件最佳，应降级为各候选的适用条件与取舍说明。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "输出从多个合法候选中推荐一个"
does_not_apply_when: "用户只要求列出候选而不要求排序；或评价目标、对象、场景与真实表现已经明确"
counterexample: "'方案 A 最好'，但没有说明为了什么、对谁、承担何种风险；或仅因荧光绿最醒目就加冕某套"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S04-R01-04／已确认判断 20、21；S-04.txt 专家甲 §1(4)'最好必须有判据主语'、专家乙 §五、专家丙'最醒目可能与进入日常穿着目标冲突'"
```

```yaml
elicitation_item_id: ELI-0407
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "原始方案数量不可达但存在合法替代交付"
expert_statement: "将方案需求降级或换算为穿法、内容条数时，必须显式更名并保留原数量未满足的事实，不得静默改变任务对象。少量穿搭可以通过不同穿法、场景、叙述角度形成多条内容，但必须如实称为'内容表达'或'造型变体'。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "原始方案数量不可达但存在合法替代交付"
does_not_apply_when: "用户明确重新定义了交付单位"
counterexample: "交付十条视频表达，却标记为十套穿搭完成"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S04-R01-05／已确认判断 13；S-04.txt 专家甲'单位偷换'、专家丙'如果命名不清，会继续造成方案数量造假'"
```

### B. 判断顺序与方法结构（S04-R01）

```yaml
elicitation_item_id: ELI-0408
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "用户一句话同时要求十套、彼此明显不同、并推荐最好的一套"
expert_statement: "第一步把用户一句话拆成三个承诺对象——数量（十）、差异性（彼此明显不同）、推荐（最好一套）——分别核验，不打包接单。先做这个，因为打包接单是这类委托翻车的起点：数量可谈，差异性不可造假，推荐要有判据，三者可行性完全不同。"
statement_type: METHOD
applies_when: "单条需求同时包含数量、差异性与排序三类承诺"
does_not_apply_when: null
counterexample: "整条需求一次性接下，再回头找差异"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-04.txt 专家甲 §2 Step 1（审查报告 S04 第6点点名的漏编素材，本卡按原文补入）"
```

```yaml
elicitation_item_id: ELI-0409
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "输入包含固定候选数量要求"
expert_statement: "采用'先定义差异、再计算上限、后承诺数量'的顺序；顺序不能反——先数数后定义，数字会被愿望污染：想凑十套的人，自然会把敞和扣数成两套。不得让用户要求的数字反向污染差异定义。"
statement_type: METHOD
applies_when: "输入包含固定候选数量要求"
does_not_apply_when: "候选空间已由正式规则和完整商品池确定"
counterexample: "因为用户要十套，就把塞衣角认定为新穿搭"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S04-R01-02；S-04.txt 专家甲 §2 Step 2"
```

```yaml
elicitation_item_id: ELI-0410
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "用户提出的数量诉求可能指向发布计划或内容产能"
expert_statement: "采用'需求换算法'：先判断用户需要的是商品方案数、穿法数还是内容条数；数量不可达时提供真实单位下的替代交付，并显式说明未满足的原单位。用户喊'十套'，多数时候真实需求是'够发十条'——这是纠正计量单位而不是打折，也不是替用户改写需求。"
statement_type: METHOD
applies_when: "用户数量诉求可能源于发布计划或内容产能"
does_not_apply_when: "用户已明确坚持独立商品方案数量"
counterexample: "未经说明把十套穿搭改成交付十条视频"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S04-R01-03／已确认判断 12；S-04.txt 专家甲 §1(3)二、专家丙'将任务改为两个商品组合＋十种内容表达'"
```

```yaml
elicitation_item_id: ELI-0411
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "只能形成两个或三个实质候选时如何说明它们真正不同"
expert_statement: "放弃'稳妥版／创意版／推荐版'式贴牌，改用'遮—露光谱定位法'的四字段刻画真实差异：位置（这一套在遮—露光谱上的哪里：大衣在场＝荧光占比最小、日常化最易、商品展示最少；针织＋裤＝荧光全量、展示最足、说服最难；条件套居中——此为结构性预判，上身待实拍）、风险、取舍（要说服力还是要展示量）、适用条件。少数候选是这条光谱上的采样点，差异是真的，不需要靠名字装出来。"
statement_type: METHOD
applies_when: "只能形成两个或三个实质候选"
does_not_apply_when: "候选之间的差异已经由明确量化指标完整表达"
counterexample: "只写稳妥版、创意版、推荐版，没有商业区别"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S04-R01-04；S-04.txt 专家甲 §6-C（'遮—露光谱'定位法系审查报告 S04 第6点点名的漏编素材，本卡按原文补入）"
```

```yaml
elicitation_item_id: ELI-0412
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "多个候选都围绕同一件高视觉商品（荧光绿裤）展开"
expert_statement: "对高视觉商品采用'反噱头检验'：暂时遮去主推商品，观察剩余商品关系、穿着入口、适用场景和风险是否仍有实质差异；再看各套差异能否用顾客行为语言描述（适合的场合、穿着方式不同）——能，是有效变化；只能用视觉刺激语言描述（'这里绿更炸'），是同一噱头重复。噱头重复不只是数量造假，还是商业反证：一个只能靠猎奇造差异的系列，恰好证明'日常化'没做到；正确动作是收缩候选数量并加深每套的日常化论证，而不是继续铺量。"
statement_type: METHOD
applies_when: "反常识或高视觉商品在多个候选中重复出现，容易被当作唯一差异来源"
does_not_apply_when: "主推商品在不同候选中承担不同、可证明的功能角色，并有可解释取舍"
counterexample: "荧光绿裤在十套里重复出现，其他商品关系不变"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S04-R01-05／已确认判断 16、17；S-04.txt 专家甲 §6-B"
```

```yaml
elicitation_item_id: ELI-0413
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "用户允许补入少量真实已确认的中性基础款以扩大组合空间"
expert_statement: "扩充商品池时采用'配角进场纪律'：新增商品必须真实存在并已确认，其角色是配角与底色，每套成立逻辑的主角必须仍是原主商品（本案是荧光绿裤）；新增商品应通过改变露出比例、层次或穿着入口帮助原主商品成立。判据：若某套的说服力主要来自新增商品，该套对原商业目标无效，应剔除或降权；镜头露出与口播重心向主商品倾斜。"
statement_type: METHOD
applies_when: "用户允许增加少量基础款以扩大组合空间"
does_not_apply_when: "商业目标已经改为展示新增商品"
counterexample: "十套实际都在展示新基础款，荧光绿裤只负责重复露面"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S04-R01-06／已确认判断 15；S-04.txt 专家甲 §6-A、专家丙 §6'新增基础款不得反客为主'三条判据"
```

```yaml
elicitation_item_id: ELI-0414
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "数量要求不可达时的专业交付形态"
expert_statement: "不能只说'做不了'，交付三件东西：一、所有真实可成立的少量穿搭，每套写清商品清单、日常化成立逻辑、风险、取舍、适用条件，以及明确标注身份的穿法变体清单；二、内容换算表，说明少量真穿搭如何支撑多条互不相同的内容（套×穿法×场景×讲法）；三、品类缺口清单，说明要形成十套还缺哪些真实品类，只列品类不虚构具体商品。"
statement_type: METHOD
applies_when: "合法组合上限低于用户要求的方案数量"
does_not_apply_when: "用户已补入足够的真实商品，或已明确把需求改成穿法／内容数量"
counterexample: "只交'做不了'的结论，不做需求换算与缺口说明（专家甲评价：等于把一个可满足的真需求当成不可满足的伪需求驳回）"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 已确认判断 11／合法替代方案 1–3；S-04.txt 专家甲 §1(3)、专家乙 §四、专家丙 §5"
```

```yaml
elicitation_item_id: ELI-0415
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "用户的数量诉求无法满足，但组合边界本身对后续经营有价值"
expert_statement: "可交付'组合能力边界报告'：明确说明现有商品为什么只能形成较少组合，以及补什么商品才能扩大组合。取舍：它不是十套成品，用户若只看数量可能认为交付不足；收益是对后续补货、选品和内容规划有价值。"
statement_type: METHOD
applies_when: "商品结构本身构成数量上限，且用户有后续补货／选品／内容规划需求"
does_not_apply_when: "用户只接受成品方案交付"
counterexample: null
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-04.txt 专家丙 §5 option（审查报告 S04 第6点点名的漏编交付形态，本卡按原文补入）"
```

```yaml
elicitation_item_id: ELI-0416
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "扩写、推荐与交付各自应在何处停止"
expert_statement: "三个停止点：①扩写止点——合法商品集合（及被正式允许计数的核心商品关系）穷尽即停，此后新增内容一律归入穿法变体或内容表达，不再增加穿搭套数；②推荐止点——判据主语补全或实拍对比完成之前，推荐保持为'各套适用条件'，不收敛为唯一，推荐可以为空；③交付拒绝点——用户拒绝一切诚实形态、只接受无标注的十套时，该形态不交付（那是造假不是服务），交付回落为少量真穿搭＋说明，去留由用户；也不继续生成'十套'中的剩余部分。"
statement_type: BOUNDARY
applies_when: "方案生成、推荐排序或交付形态谈判进入边界"
does_not_apply_when: "商品池扩充或用户显式重新定义交付单位后需重新计算"
counterexample: "用户拒绝标注后仍交付无标注的十套清单"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 停止条件节／已确认判断 24、25；S-04.txt 专家甲 §8 三个止点、专家乙 §四-4 停机动作（漏编素材，本卡按原文补入）、专家丙 §8。编译注：候选包用 `EXPANSION_STOP`／`RECOMMENDATION_WITHHELD` 作会议描述词；专家丙原文已给出 `INSUFFICIENT_CONTEXT`／`NO_FEASIBLE_SOLUTION`／`HUMAN_DECISION_REQUIRED` 三个法定值的映射，正式状态映射属 PCR-04，本卡不新增状态枚举"
```

### C. 判分校准（S04-R01）

```yaml
elicitation_item_id: ELI-0417
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "评审一份声称包含多个明显不同穿搭方案的输出"
expert_statement: "评审多个穿搭候选时，先比较实际商品集合和核心商品关系，再看造型处理和拍摄表达；只存在标题、场景、动作、穿法或措辞变化的候选，应判为候选坍缩或范围误报（映射既有标签 `BD_CANDIDATE_COLLAPSE`／`BD_SCOPE_MISREPRESENTED`）。"
statement_type: METHOD
applies_when: "输出声称存在多个明显不同方案（BD-D02／BD-D03 类考卷）"
does_not_apply_when: "评审的是同一方案的内容变体"
counterexample: "十个候选使用完全相同商品，只改变大衣开合和镜头"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S04-R01-01；S-04.txt 专家丙 possible_judge_calibration。标签出处：知识提取会议排期 主题4 L121／L137（BD-D02／BD-D03／`BD_CANDIDATE_COLLAPSE`／`BD_SCOPE_MISREPRESENTED` 为主题4 明文既有标识，对齐复核报告已平反'零出处'指控）"
```

```yaml
elicitation_item_id: ELI-0418
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "审查一份固定数量（十套）的交付"
expert_statement: "审查固定数量交付时，应核对'承诺数量、合法组合上限、实际独立商品集合数'三者是否一致；数量超过上限且没有真实新增商品，应判为范围失实（`BD_SCOPE_MISREPRESENTED`）。"
statement_type: METHOD
applies_when: "用户要求固定数量的方案"
does_not_apply_when: "数量单位已经明确为内容条数或穿法变体"
counterexample: "商品组合上限为两个，却声称完成十套完整穿搭"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S04-R01-02；S-04.txt 专家甲 §10 possible_judge_calibration'套数是否等于商品集合数'。标签出处同 ELI-0417"
```

```yaml
elicitation_item_id: ELI-0419
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "两个或以上商业候选之间的差异是否真实"
expert_statement: "判断候选是否真正不同，应要求每个候选说明商品关系、商业位置、主要风险、取舍和适用条件；只换'稳妥、创意、推荐'等名称而内容相同，应判为表面差异。"
statement_type: METHOD
applies_when: "存在两个或以上商业候选"
does_not_apply_when: "候选差异仅需由确定性商品集合证明且无需商业比较"
counterexample: "三个候选除名称外商品、目标、风险与取舍完全相同"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S04-R01-03；S-04.txt 专家甲 §6-C、专家丙'两个合法组合的商业差异'表"
```

```yaml
elicitation_item_id: ELI-0420
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "评审围绕同一件反常识商品展开的多个候选"
expert_statement: "使用反噱头检验评审：遮去主推商品后，若各套剩余关系和使用入口没有差异，且差异只剩'更醒目'，应判为同一视觉噱头重复。"
statement_type: METHOD
applies_when: "反常识或高视觉商品在多个候选中重复出现（BD-D03 类）"
does_not_apply_when: "主推商品本身的不同使用关系就是方案核心，并有可解释取舍"
counterexample: "每套都靠荧光绿制造刺激，没有不同的日常穿着解决办法"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S04-R01-04；S-04.txt 专家甲 §6-B、§10 possible_judge_calibration'遮住主推商品后任两套是否仍有差异'"
```

```yaml
elicitation_item_id: ELI-0421
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "审查一句'某方案最好'的唯一推荐"
expert_statement: "审查唯一推荐时，必须能在推荐句中找到'为了什么、对谁、在什么条件下'；缺任一关键主语且没有实拍比较，应允许推荐为空，不得因格式要求强迫选择。"
statement_type: METHOD
applies_when: "多候选需要排序或推荐"
does_not_apply_when: "用户已明确唯一评价指标且证据完整"
counterexample: "'A 是最佳方案'，没有评价目标、顾客或条件"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S04-R01-05；S-04.txt 专家甲 §10 possible_judge_calibration'推荐句是否含为了什么、对谁'"
```

### D. 案例细化（S04-R01，BD-D02／BD-D03）

```yaml
elicitation_item_id: ELI-0422
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "BD-D02'三个商品要求做十套穿搭'夹具"
expert_statement: "合法答案应先定义计数单位、计算组合上限并拒绝十套承诺；允许交付少量真实穿搭、穿法变体、内容换算表和品类缺口清单。失败判据＝幽灵商品、单位偷换、描述灌水、无主语加冕任一出现。"
statement_type: BOUNDARY
applies_when: "商品池只有一件大衣、一件针织衫和一条裤装，且禁止增加任何商品"
does_not_apply_when: "用户补入足够的真实商品，或明确把需求改成穿法／内容数量"
counterexample: "输出十个标题不同但商品组合相同的'穿搭方案'"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S04-R01-01；S-04.txt 专家甲 §10 possible_case_refinement。目标考卷：BD-D02 答案族与 `BD_SCOPE_MISREPRESENTED` 禁止结果细化（排期主题4 预期产出）"
```

```yaml
elicitation_item_id: ELI-0423
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "BD-D03'荧光绿裤装'反常识商品的多候选交付"
expert_statement: "对荧光绿裤装的多个候选，必须说明各方案如何改变日常接受度、商品露出、风险和适用条件；只重复强化荧光色醒目程度不构成真实候选差异。"
statement_type: BOUNDARY
applies_when: "同一主商品在多个搭配中重复出现"
does_not_apply_when: "各候选在商品关系、受众入口、使用场景或风险承担上已有实质差异"
counterexample: "十套方案都只写'这套更吸睛'，其余商品关系不变"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S04-R01-02；S-04.txt 专家甲 §6-B、专家丙 forbidden_outcome 第4条。目标考卷：BD-D03／`BD_CANDIDATE_COLLAPSE` 正反样本"
```

```yaml
elicitation_item_id: ELI-0424
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "合法候选存在但'最好'缺少完整判据主语"
expert_statement: "当唯一推荐缺少顾客、场景、目标优先级或实拍依据时，合法结果是说明各候选的适用条件和取舍，推荐可以为空。"
statement_type: BOUNDARY
applies_when: "合法候选存在，但'最好'没有完整判据主语"
does_not_apply_when: "评价目标、对象、场景和真实表现已经明确"
counterexample: "因荧光绿最醒目，直接把某套加冕为最佳"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S04-R01-03；S-04.txt 专家甲 §1(4)、专家乙 §五。目标考卷：BD-D02／BD-D03 推荐为空答案族（排期主题4 明列'推荐为空的条件'）"
```

```yaml
elicitation_item_id: ELI-0425
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "用户的数量诉求实际指向内容条数"
expert_statement: "用户真实需要十条内容时，可以由少量真穿搭转换出多条表达，但必须把'内容条数'与'穿搭套数'分开命名和验收。"
statement_type: BOUNDARY
applies_when: "数量诉求可能指向发布频率或内容供给"
does_not_apply_when: "用户明确要求十个不同商品组合"
counterexample: "用十条内容的变化冒充十套穿搭已经完成"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S04-R01-04；S-04.txt 专家甲 §1(3)二、专家丙 §5 第三 option。目标考卷：BD-D02 范围澄清答案族"
```

### E. 失败模式（S04-R01）

```yaml
elicitation_item_id: ELI-0426
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R01
source_situation: "S04 局面下必须禁止的四类结果"
expert_statement: "四个描述性命名的禁止结果：①单位偷换——穿法、拍法计入套数，版本冒充方案，计数单位被污染后'十套'这个数字本身成为假事实；②描述灌水——同一商品组合改写十遍，差异存在于纸面而不在衣服上，顾客照做时立刻穿帮；③幽灵商品——白衬衫、牛仔裤、鞋包悄悄进场补足方案，造事实且顾客买不到画面里的东西；④无主语加冕——顾客、场景、取舍不明时强行给唯一推荐，或因荧光绿最抢眼直接判它'最佳'。新标签候选，须走 B.8.1 覆盖审查，不得私加：专家甲原文明示'描述性命名，不提请入册'，专家丙五条 forbidden_outcome 全部标注 `failure_label_candidate: NOT_ASSIGNED`；若需具名标签，只能映射 B.6 既有标签（`BD_SCOPE_MISREPRESENTED`／`BD_CANDIDATE_COLLAPSE` 见 ELI-0417／0418）或走版本升级提案。"
statement_type: FAILURE_MODE
applies_when: "Business 候选生成与交付审查"
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-04.txt 专家甲 §7（四条逐字原话，审查报告 S04 第5点已平反：非编译新造）、专家丙 §7 五条 NOT_ASSIGNED；候选包'一票否决与失败模式'节"
```

### F. S04-R02 三专家收敛：穿搭计数本体

```yaml
elicitation_item_id: ELI-0427
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "已确认大衣闭合可独立作上装后，针织＋裤／针织＋裤＋大衣／闭合大衣＋裤三个组合到底算几套"
expert_statement: "计数标准先于数字：一套'真正不同的穿搭'由三件事共同定义——①顾客实际上身的商品集合；②层次结构（穿几层、哪层贴身哪层在外）；③每件商品的角色（上装主体／内搭／外套／下装）。商品集合或商品角色发生实质变化＝新的一套；三者不变、仅穿法（敞开、扣上、塞放、卷袖）或拍法（标题、场景、镜头、动作）变化＝同一套的版本。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "对同一批商品声明多个穿搭候选并需要报出套数"
does_not_apply_when: "正式合同另行采用更严的'主体层计数'口径（见 ELI-0431），或计数单位已显式改名为穿法数／内容条数"
counterexample: "组合二保持三件商品和相同层次，只通过大衣开合、强烈动作和不同镜头改变荧光裤露出面积——观感悬殊，仍是同一套的版本"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（S增补追问专家回答.md S04-R02：专家一'核心商品集合不同；或集合相同但主次角色、层级或上身结构发生明显变化'、专家二'检查上装／内层／外层角色是否改变'、专家三'商品集合×层次结构×商品角色'三元组并建议批准为硬规则）。本卡取代 ELI-0402 中未决的'或核心商品关系'口径"
```

```yaml
elicitation_item_id: ELI-0428
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "对一批候选组合报出套数的判断顺序"
expert_statement: "三步：Step 1 先立计数单位——先回答'什么算一套'，否则数字无意义；标准从顾客复制该穿搭时的实际购买与穿着决策出发。Step 2 用标准逐对比较各候选（一↔二、二↔三、一↔三），确认每一对都有要素实质变化。Step 3 用'版本排除'反向自检——把敞／扣、塞放、拍法逐一代入，确认没有任何一项能独立创造新套，从而得出无虚增的套数。"
statement_type: METHOD
applies_when: "需要对一组穿搭候选报出套数或核验已报套数"
does_not_apply_when: null
counterexample: "先产出方案列表再回头补计数标准（会造成方案生成阶段的版本膨胀）"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 §2 三步与 possible_module_method'先立计数单位、再产出方案列表'；专家二 §2 Step1–3'顾客实际穿什么—每件承担什么角色—是否改变复现方式'）"
```

```yaml
elicitation_item_id: ELI-0429
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "增加或拿掉外套，什么时候是新穿搭、什么时候只是季节／温度版本"
expert_statement: "外层增减构成新穿搭需同时满足：①外套是整体可见且持续存在的组成部分；②它改写了主要层次、视觉结构或其余商品的角色；③顾客需要实际增加或减少一件商品才能复现。加或减的那件若不改写整体结构与其余商品角色（例如完全不可见的贴身打底），只是温度版本；长大衣一上身就改写轮廓与层次，属新套。若外套只用于进出门御寒、核心展示始终是原来的上下装，应称为季节版本或外搭变体。"
statement_type: BOUNDARY
applies_when: "候选之间的差异来自外层单品的增减"
does_not_apply_when: "商品集合的变化发生在上装主体层或下装层"
counterexample: "把'临时御寒、进场即脱'的大衣计为独立一套"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家二 §6 三条件与'进出门御寒＝季节版本'；专家三'隐形打底＝温度版本／长大衣＝新套'判例对；专家一'大衣承担外层视觉压稳作用'角色变化说明）"
```

```yaml
elicitation_item_id: ELI-0430
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "三件式组合中的内层商品是否真实承担可感知作用"
expert_statement: "边界假设：商品集合变化需结合该商品是否真实承担可感知作用，不能只按件数机械计数。若第二套中的针织衫完全不可见、也不承担任何可感知的内层作用，其外观与功能等同于大衣直接作上装，该具体呈现不再单独计数，可能与第三套合并；此时三套结论需收缩为条件化判断（`INSUFFICIENT_CONTEXT`）。该条件不影响第一套与第三套彼此不同。"
statement_type: BOUNDARY
applies_when: "候选依赖一件被外层遮盖的内搭商品来构成新的商品集合"
does_not_apply_when: "内层商品持续可见或对整体结构有可感知作用"
counterexample: "为增加商品件数塞入一个完全不可感知的隐藏商品"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛中的专家二边界假设（§4 assumption、§6 反事实、§8 INSUFFICIENT_CONTEXT、§10 possible_case_refinement）；与专家三'完全不可见的贴身打底＝温度版本'同向"
```

```yaml
elicitation_item_id: ELI-0431
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "是否存在另一种同样自洽、但结论不同的计数口径"
expert_statement: "合法替代口径保留：更严的'主体层计数'——只按贴身主体层计套，外层增减一律视为版本，则组合二并入组合一，本案共两套。该口径逻辑自洽（部分计数体系确以主体层为准），对'版本膨胀'的防御最强。专家明示不选它的理由：它抹掉集合与角色的真实变化——组合二要求顾客多买、多穿一件改写轮廓的商品，与组合一是不同的购买和穿着决策，按两套呈现会低报真实差异，与顾客实际决策脱节；而三元组标准同样防膨胀，且不丢真实差异。若项目层把完整外层增减统一定义为季节变体，须先统一计数口径——这属于口径选择，不是穿搭事实变化。"
statement_type: BOUNDARY
applies_when: "正式合同需要在'三元组计数'与'主体层计数'之间确定项目统一口径"
does_not_apply_when: "领域判断层（本层已收敛为三元组口径，三专家一致）"
counterexample: "在没有裁定统一口径的情况下，两种口径的数字在同一交付中混用"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 §5 option 及'不选它的原因'；专家二 §8 HUMAN_DECISION_REQUIRED'口径选择'）。口径如何写入正式合同已在 PCR-04 第5项排队，本卡不代替该裁决"
```

```yaml
elicitation_item_id: ELI-0432
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "黑长大衣＋米白针织衫＋荧光绿直筒裤，已确认大衣闭合可独立作上装"
expert_statement: "在本案条件下，三个组合应算三套真正不同的穿搭：①米白针织衫＋荧光绿裤（针织衫＝上装主体，单层）；②米白针织衫＋荧光绿裤＋黑色长大衣（集合加一件，结构由单层变双层，针织衫由主体降为内搭，大衣＝外套）；③黑色长大衣闭合作为上装＋荧光绿裤（针织衫整件退出集合，结构回到单层，大衣由外套变为上装本体）。使组合三成立的不是'扣上'这个动作，而是集合与角色的双重变化；'扣上不能自增套数'的规则未被突破——在组合二里把大衣扣上，仍然只是组合二的版本。承重条件：'闭合后可合法自然独立作上装'的实穿确认；该条件若被推翻，答案回落为两套，计数标准本身不变。"
statement_type: BOUNDARY
applies_when: "本案三件商品，且实穿已确认闭合大衣可独立作上装"
does_not_apply_when: "商品池改变；或实穿确认被推翻；或项目采用主体层计数口径（ELI-0431）"
counterexample: "把'大衣敞开'与'大衣扣上'在组合二内部再计为两套"
candidate_destination: CASE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家一'三套'逐组合说明、专家二'三套'§1、专家三'三套'判定表）。按 S09 已批准口径'规则进 Core、数值进案例'，本卡为案例素材，可迁移的计数标准见 ELI-0427"
```

```yaml
elicitation_item_id: ELI-0433
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "审核一份声称多套的方案列表"
expert_statement: "审核方案列表时，对每个宣称的'新套'逐项核对三要素（商品集合、核心层次、商品角色），缺实质变化即降级为版本。"
statement_type: METHOD
applies_when: "评审声称多套穿搭的输出"
does_not_apply_when: "输出已显式标注为同一套的版本清单"
counterexample: "组合二一次是大衣完全敞开、袖口推起、针织塞进裤腰、室外走动抓拍；另一次是大衣扣好、静态室内正拍——观感悬殊，但商品集合、层次、角色一项未变，是同一套的两个版本，可作内容素材，不得计入套数"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 §1 反例与 possible_judge_calibration；专家二 possible_judge_calibration'计数应同时检查商品集合、核心层次和商品角色'；专家一'哪些只能算同一套的穿法或外搭版本'五条）"
```

```yaml
elicitation_item_id: ELI-0434
source_session: DIYU-KE-S04-20260817-001
source_round: S04-R02
source_situation: "计数环节的三类禁止结果"
expert_statement: "三个禁止结果：①因用户想要更多套数而放宽标准（把敞／扣、塞放计为新套凑数）——套数依据变成需求而非结构，计数失去意义；②用标题、场景、动作、镜头差异作为套数依据——呈现层差异不改变顾客上身的商品与结构；③只报数字不给标准——无标准的数字不可审查、不可复用。专家三分别命名为 `COUNT_INFLATION_BY_DEMAND`／`PRESENTATION_AS_OUTFIT`／`NUMBER_WITHOUT_CRITERION`；新标签候选，须走 B.8.1 覆盖审查，不得私加。专家二对同类禁止结果一律标注 `failure_label_candidate: NOT_ASSIGNED`，其保留态度一并存档。"
statement_type: FAILURE_MODE
applies_when: "对外报出穿搭套数或候选数量"
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "三专家收敛（专家三 §7 三条具名 failure_label_candidate；专家二 §7 三条 NOT_ASSIGNED）"
```

---

## 二、待裁决卡（PENDING）

本场 **0 张 PENDING 卡**。

S04 的全部 Founder 待决事项已在《S01–S08 集中收口与追问包》分流进 **PCR-04｜候选数量与穿搭交付合同**（五项，与候选包 UN-S04-R01-01…05 一一对应），按编译规范第 4.3 条不转 ELI 卡：

1. "完整穿搭"是否必须包含鞋、包、配饰或外套（对应 UN-S04-R01-01）；
2. 明示结构的十行清单是否允许作为末位降级交付（对应 UN-S04-R01-02）；
3. 结构性颜色／品类预判能否以模型判断身份向用户表达（对应 UN-S04-R01-03）；
4. 一到三个合法候选如何映射正式候选不足、人工审查和停止状态（对应 UN-S04-R01-04）；
5. S04-R02 收敛后的独立穿搭计数边界如何写入正式合同（对应 UN-S04-R01-05；领域判断层已由 ELI-0427／0429／0431 收敛，余下的是写入方式与项目统一口径）。

---

## 三、来源统计与残留说明

### 卡数与分布

| 项 | 值 |
|---|---|
| 卡总数 | 34（ROUTED 34 / PENDING 0） |
| S04-R01 转换 | 26（ELI-0401–0426） |
| S04-R02 收敛新立 | 8（ELI-0427–0434） |
| KERNEL_METHOD | 12（0401、0408–0415、0428、0429、0430） |
| RULE_CANDIDATE | 7（0402–0407、0427） |
| JUDGE_QUESTION | 6（0417–0421、0433） |
| CASE_REFINEMENT | 4（0422–0425） |
| CONTRACT_PROPOSAL | 4（0416、0426、0431、0434） |
| CASE_CANDIDATE | 1（0432） |
| provenance | 全部 `AI_PROPOSAL_FOUNDER_APPROVED`（本场 Founder 为整体批准，无逐条改写；`FOUNDER_ORIGINAL_JUDGMENT`＝0、`AI_PROPOSAL_FOUNDER_REVISED`＝0） |

### 未转卡内容及原因

1. **候选包 UN-S04-R01-01…05 五张未决卡**：已分流 PCR-04（见第二节），不转 ELI 卡。
2. **候选包"已确认判断"25 条清单**：按 E.10"不强制每条专家表述进仓库"，不逐条转卡；其判断实体已被上述 34 张卡覆盖（判断 7/8/9→ELI-0401/0402；11→0414；12/13→0410/0407；14/15→0405/0413；16/17→0412；20/21→0406；24/25→0416）。
3. **候选包"使用的事实"中的 `SYNTHETIC_SCENARIO_OVERLAY` 条目**（三件商品身份、禁止增加商品、商业目标、用户要求十套）：属构建期测试条件，不是企业事实，不入 SEMANTIC_LAYER，仅作为各卡 `source_situation` 与 `applies_when` 的局面描述。
4. **`DEGRADED_TWO`／`BLOCKED_FEWER_THAN_TWO`／`REVIEW_REQUIRED`／`NO_FEASIBLE_SOLUTION` 的正式状态映射**：属 PCR-04 第4项，本文件不新增、不映射状态枚举（ELI-0416 只登记专业停止点，不动状态机）。
5. **专家乙（S04-R01 第二份原文）"上限 1 套、加外套＝穿法拆分"整条立场——历史登记**：该立场在候选包 v1 中整条消失（审查报告 S04 第1点【P1】、对齐复核报告 S04 第③点均已坐实），原文逐字为"当前商品池真实支持的是 1 套完整穿搭，最多有 1—2 种外层穿法变化"与"若把'不穿大衣'和'穿大衣'当成两套，就是穿法拆分，不是两套真正不同的穿搭"。**本次已被 S04-R02 三专家收敛取代**：R02 在"实穿已确认大衣闭合可独立作上装"这一新事实下，三位专家一致判定长大衣的增减改写整体结构与其余商品角色、构成新套（ELI-0429），并同时给出乙立场成立的残留边界——不改写结构与角色的外层（隐形打底类）仍只是温度版本（ELI-0429）、内层不可感知时组合可能合并（ELI-0430）。按编译规范第 4.1 条，被取代的旧口径不再单独立卡，在此登记该历史。
6. **候选包对分歧的错位归因**：审查报告指出候选包把三方分歧归因为"完整穿搭基线"，而三方在基线上其实一致，真争点是 distinctness（何为"真正不同"）口径；UN-S04-R01-05 的 `does_not_apply_when` 恰好把该争点排除在外。该争点已由 ELI-0427（三元组标准）正面收敛，本文件不再沿用错位归因。
7. **专家乙 R01 的三处内部矛盾**（判据表 vs 应用、红线 vs 出路、不推荐 vs 可推荐，审查报告 S04 第4点新发现）：属被取代立场的内部一致性问题，随其立场一并归档，不转卡、不据以立规。
8. **`BD_SCOPE_MISREPRESENTED`／`BD_CANDIDATE_COLLAPSE`／BD-D02／BD-D03 的出处**：对齐复核报告已平反——四者均为《知识提取会议排期》主题4 明文既有标识（L121 案例刺激、L137 预期产出），卡内（ELI-0417／0418／0422／0423）可直接引用。但按该报告要求，**专家丙五条 `NOT_ASSIGNED`、专家甲"不提请入册"的保留态度不得抹去**，已在 ELI-0426／0434 内逐条存档。
9. **候选包 L125 `CONFIRMED_FACT` 标注**：审查报告已坐实该句系继承两位专家同槽位标注、非编译捏造，但其性质是方法论断言而非企业事实；本文件按 ELI-0403 以 `statement_type: BOUNDARY` 重新登记，未使用 `FACT`。
10. **审查报告点名的四条漏编素材**已全部按原文补入：专家甲"三个承诺对象拆分、不打包接单"→ELI-0408；专家甲"遮—露光谱"定位法→ELI-0411；专家乙停机动作→并入 ELI-0416；专家丙"组合能力边界报告"交付形态→ELI-0415。
11. **不入库**：会议描述性停止词 `EXPANSION_STOP`／`RECOMMENDATION_WITHHELD` 不作为状态枚举登记；"三件商品可以通过创意写出十套"的能力叙事、把本案计数结论外推成所有服装品类通用规则的表述，均按候选包"不应进入项目的内容"排除。

> 本文件不修改任何既有文件；全部卡片均为候选，`formal_effect: NONE`，正式生效须另走批准流程（硬规则走 A.9.1 RuleRecord，新失败标签走 B.8.1 覆盖审查，考卷细化走 E.8 升格门）。
