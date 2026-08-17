# DIYU-KE-ELI-S02｜Intent：阻断缺失、非阻断缺失与降级 正式入库知识卡

```yaml
session_id: DIYU-KE-S02-20260817-001
session_theme: S02 Intent：阻断缺失、非阻断缺失与降级
covered_rounds: [S02-R01, S02-R02, S02-R03]
compiled_on: 2026-08-17
compiler: 主持人 Claude（S02 场编译代理）
ruling_basis: Founder（Faye）2026-08-17 裁决——S01–S08 候选包＋五张追问卡专家回答＋S09 回答全部批准通过，按《E_领域专家知识提取协议》整理为正式入库知识卡。
source_files:
  - E_领域专家知识提取协议.md（E.3 卡模板／E.2.2 路由／E.2.3 失败标签纪律／E.10 防膨胀）
  - DIYU-KE-S02-20260817-001_S02待入库候选包_v1.md（R01／R02 会议纪要与候选资产）
  - S-02.txt（S02-R02 专家原文，忠实版权威；与候选包冲突时以本文件为准）
  - DIYU-KE-S02-S07_原文对照审查总报告_20260817.md（S02 节：不闭环，问题 1–6）
  - DIYU-KE-八份记录_标准对齐复核结论_20260817.md（S02 节：主题2 缺口加重、E.3 转换层缺失）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S02-R03 QUESTION_CARD；PCR-01/02、EV-01 路由）
  - S增补追问专家回答.md（S02-R03 三位专家独立回答）
expert_id_map:
  S-02.txt（R02）:
    专家甲: 第一份 CANDIDATE_RESPONSE（L29–132，判"继续做"）
    专家乙: 第二份 CANDIDATE_RESPONSE（L134–331，判 INSUFFICIENT_CONTEXT／必须停）
    专家丙: 末段散文体回答（L331–533，判必须停）
  S增补追问专家回答.md（R03）:
    专家一: 散文体（L1–99）
    专家二: CANDIDATE_RESPONSE（L437–601）
    专家三: FOUNDER_REVIEW_SUMMARY＋CANDIDATE_RESPONSE（L1251–1360）
provenance_note: 本场 Founder 为整体批准、无逐条改写，故 provenance 一律 AI_PROPOSAL_FOUNDER_APPROVED（规范 3.1）。PENDING 卡的该字段只表示"陈述本身在已批准语料内"，不表示冲突处置已裁决。
card_count:
  total: 38
  routed: 34
  pending: 4
  by_destination: {KERNEL_METHOD: 10, RULE_CANDIDATE: 12, JUDGE_QUESTION: 7, CASE_REFINEMENT: 4, CONTRACT_PROPOSAL: 4, BRAND_MEMORY_PENDING_EVIDENCE: 1, SEMANTIC_LAYER: 0, CASE_CANDIDATE: 0}
formal_effect: NONE（全部为候选；生效另走 A.9.1／B.8.1 批准流程）
```

---

## 一、入库知识卡（ROUTED）

### R01 段：缺失判定与受限交付

```yaml
elicitation_item_id: ELI-0201
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "大衣刚上新，用户要一条让顾客看懂并愿进一步了解的视频号内容，八项资料缺失且用户拒绝再被追问"
expert_statement: "先从用户要求的结果倒推最低成立条件，再核对现有事实，最后逐项做删除测验；不能先按字段缺失数量决定停不停。"
statement_type: METHOD
applies_when: "商业结果目标明确，但上下文不完整"
does_not_apply_when: "目标仍未定义，应先处理目标识别"
counterexample: "看到八项缺失就直接拒绝，不检查当前任务是否真正需要这些信息"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S02-R01-01（L232-240）；判据形态见 ELI-0202"
```

```yaml
elicitation_item_id: ELI-0202
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "同上；需判断八项缺失中哪些真正阻断任务"
expert_statement: "判断缺失是否会让任务停止时，应删除所有依赖该缺失的声明并重新检验核心结果；删除后核心结果仍成立才可继续，删除后核心结果无法成立则必须停止或改变任务。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "已明确用户希望达成的结果，但存在一个或多个资料缺口"
does_not_apply_when: "商业结果本身尚未明确"
counterexample: "因字段缺失数量多而一律停止，未检查是否可以删除相关表达"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R01-01（L158-166）；方法顺序见 ELI-0201"
```

```yaml
elicitation_item_id: ELI-0203
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "缺价格、库存、材质及证明、受众调研、账号人设、创始人或品牌故事、品牌禁用词、成交承接共八项"
expert_statement: "商品、品牌、库存、受众和人物经历等事实缺口只能删除、隐藏或保持未知，不得用假设补成事实；假设只可用于用户让渡的创作自由度（拍摄结构、叙述角度、语气），并应保留其模型判断属性。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "缺少客观事实，但仍存在可调整的内容路线"
does_not_apply_when: "用户或权威资料已经确认相关事实"
counterexample: "没有受众资料却写'专为 30 岁职场女性设计'"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R01-02（L168-176）"
```

```yaml
elicitation_item_id: ELI-0204
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "用户要求'快点、别再问'，且部分输入置信度低"
expert_statement: "快速交付和低置信度必须带来声明范围收缩：合法的快是减少声明、改用中性表达、交付删减清单和拍摄指引；不得仅增加标签而保留与完整版相同的事实性表达。QUICK 只能减少内容数量和声明范围，不能降低真假标准、合规标准或来源标注义务。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "用户要求少问快出，或输入置信度较低"
does_not_apply_when: "所有声明均有充分来源支持"
counterexample: "给'羊毛材质'标低置信度后照常写进发布文案"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R01-03（L178-186）＋已确认判断 7/8（L50-51）；QUICK 的正式定义与'跨过 QUALITY_REDUCING 缺失是否须产生 ASSUMPTION'不在本卡范围，见 PCR-01／PCR-02；S07 场另有同题'快不降标'卡（编号由 S07 编译产出）"
```

```yaml
elicitation_item_id: ELI-0205
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "品牌禁用词及表达约束字段为空，无法区分'没梳理过'与'确认没有'"
expert_statement: "'品牌已确认没有额外禁用词'和'品牌从未梳理过禁用词'是两个不同事实；前者可作为有来源的确认，后者仍是信息缺失，不能被写成'没有限制'，必须收窄表达并保留人工自查。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "品牌未提供禁用词、品牌表达边界或审核规则"
does_not_apply_when: "品牌已通过有来源记录明确确认不存在额外限制"
counterexample: "字段为空时系统自动落'无限制'并直发"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R01-04（L188-196）；两态如何映射 A.2.4 FactValue 五态属产品合同，见 PCR-02，本卡不作映射"
```

```yaml
elicitation_item_id: ELI-0206
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "用户明确要求不再追问，只能交付受限版本"
expert_statement: "受限交付必须显式列出删减的声明类别、仍存在的风险和补齐后可解锁的内容；不得让用户误把删减版当成完整水平。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "因资料不足而交付删减版"
does_not_apply_when: "产物已满足完整资料合同"
counterexample: "交付极简脚本但不说明因缺料删去了卖点、人设和品牌表达"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R01-05（L198-206）"
```

```yaml
elicitation_item_id: ELI-0207
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "八项缺失是否构成'所有内容任务的固定必需资料'"
expert_statement: "一项资料的重要性由'缺失项 × 当前结果 × 发布路径 × 内容路线'共同决定，不是字段的永久属性；目标改为直接成交时成交承接、库存与部分价格信息才显著上升为必要条件。"
statement_type: METHOD
applies_when: "同一资料在不同任务中的必要性不同"
does_not_apply_when: "存在明确的全局法律或品牌硬禁令"
counterexample: "把库存数量设置为所有品牌认知内容的必填信息"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S02-R01-02（L242-250）"
```

```yaml
elicitation_item_id: ELI-0208
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "用户明确说'不要再问'，但仍有八项资料缺口"
expert_statement: "用户拒绝继续回答时，优先采用'声明前提＋交付受限版本＋附缺料与风险说明'的无追问路径；只有真正无法成立时才停止。"
statement_type: METHOD
applies_when: "用户明确要求不再追问，且存在合法受限产物"
does_not_apply_when: "核心任务缺少不可替代的信息或授权"
counterexample: "用户说别问后，系统仍连续提出八个字段问题"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S02-R01-03（L252-260）；'最多允许几个高价值澄清问题'属产品合同，见 PCR-01"
```

```yaml
elicitation_item_id: ELI-0209
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "非成交型商品理解目标＋用户拒绝补资料的具体局面"
expert_statement: "用户已明确非成交型商品理解目标并拒绝继续补资料时，允许通过删除无依据声明、附删减清单和风险提示交付受限版本；不得把删减版包装成完整商品说明。缺什么必须删除对应的整族内容：价格和优惠、库存和稀缺、材质与证明、受众指称、人设自述、品牌故事、购买指令均不得出现。"
statement_type: BOUNDARY
applies_when: "当前已知信息足以形成不依赖缺失事实的最低合法内容，且发布前存在人工查看"
does_not_apply_when: "删除相关内容后核心结果已无法成立，或产物将直发且关键品牌约束未知"
counterexample: "缺少材质资料仍写'高级羊毛质感'，只把置信度标成低"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S02-R01-01（L136-144）＋已确认判断 6（L49）；proposed_destination 原写 INT-D02 答案族与受限输出禁止结果细化"
```

```yaml
elicitation_item_id: ELI-0210
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "单变量反事实：主要结果从'商品理解'改为'本周直接成交'"
expert_statement: "将主要结果单独改为'本周直接成交'时，应重新判断价格、库存和成交承接；不得沿用非成交任务的缺失处理结论。"
statement_type: BOUNDARY
applies_when: "商业结果从商品理解／进一步了解改变为可归因成交"
does_not_apply_when: "仍是认知、理解或问题征集任务"
counterexample: "没有任何购买路径，却继续交付以成交为目标的脚本"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S02-R01-02（L146-154）"
```

```yaml
elicitation_item_id: ELI-0211
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R01
source_situation: "人工评审受限版本或标了 confidence=low 的版本"
expert_statement: "判分受限／低置信度产物须查两层：一是不能只检查是否有标签，还要检查无依据的声明类别是否实际被删除、隐藏或改成非事实性表达；二是三项同时成立——禁止声明零出现、所有事实有来源、删减清单与正文实际删减一致。"
statement_type: METHOD
applies_when: "人工评审受限版本或低置信度版本；判断受限交付是否诚实、可用、可追溯"
does_not_apply_when: "输入事实完整且不走受限路线"
counterexample: "输出写了 confidence=low，正文仍包含材质、功效和精准人群断言；或清单说已删除受众判断，正文仍写'适合职场女性'"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S02-R01-01（L210-218）＋JC-S02-R01-02（L220-228）合并为一卡（规范 6 同场重复合并）"
```

### R02 段：画面证据、镜头诚实与降级

```yaml
elicitation_item_id: ELI-0212
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "商品图只能辨认是同一件大衣，看不清轮廓、局部、面料、上身与动态"
expert_statement: "先把商品理解所需的信息按载体分成两半——可拍摄的（形、上身、动态、表面呈现）与必须由资料证明的（成分、功能、价格、人群），再决定是补画面、补资料、受限继续还是停止；两类缺口恢复路径不同，不可互相冒充。"
statement_type: METHOD
applies_when: "商品资料和视觉素材同时不足"
does_not_apply_when: "所需信息已全部有来源"
counterexample: "用材质说明替代缺失的上身与动态展示"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S02-R02-01（L510-518）；S-02.txt 专家甲 §2 Step1（L56）与 §10 possible_module_method（L130）"
```

```yaml
elicitation_item_id: ELI-0213
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "判断当前识别级图片把顾客带到了哪一层"
expert_statement: "把顾客所得分三层：商品识别（知道存在这件大衣、能认出是同一商品）／外观理解（看清完整轮廓、主要结构和可区分的设计细节）／穿着与性能理解（理解上身比例、动态表现、材质或功能）。'让顾客看懂'型任务至少要求达到外观理解层；只达到商品识别层即不成立。"
statement_type: BOUNDARY
applies_when: "需要判断现有素材把内容带到哪一层，以及缺口应补画面还是补资料"
does_not_apply_when: "任务本身只要求商品存在通知"
counterexample: "顾客看完只能说'我知道它上新了'，仍被判为完成商品理解"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-02.txt 专家乙三层分界表（L156-163）——候选包漏编，据原文对照审查报告 S02 问题 6 补入"
```

```yaml
elicitation_item_id: ELI-0214
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "R01 曾结论'拍给顾客看可以替代说给顾客听'，R02 对其补边界"
expert_statement: "'用画面替代文字说明'只在同一实物可拍、画面达到当前品类最低理解门槛且没有改变商品呈现（不改形、不改色质、不断章）时成立；仅能识别商品身份的图片不满足该条件，其在成片中的合法角色只有一个——证明拍的和卖的是同一件。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "内容准备依靠视觉展示完成商品理解"
does_not_apply_when: "任务只是新品存在通知，或有充分文字事实但不承诺视觉理解"
counterexample: "识别级单图经缩放、平移、配乐被包装为完整商品展示"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R02-01（L446-454，原标 AI_PROPOSAL_FOUNDER_REVISED）；据原文对照审查报告 F-D（该 REVISED 实为 REVIEW_SUMMARY 建议、非 Founder 修改）并按规范 3.3 改标 APPROVED。其中'品类最低理解门槛'是否必含动态，见 PENDING 卡 ELI-0235"
```

```yaml
elicitation_item_id: ELI-0215
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "用手机实拍同一件大衣，可自由选择角度、灯光与后期"
expert_statement: "商品镜头必须遵守'不改形、不改色质、不断章'：不借位、不用夹子在背后收腰、不垫改结构；自然光或中性灯、禁美化滤镜与调色改变商品呈现色；特写必须有完整轮廓镜头打底，禁只拍最好看的十厘米。破坏任一条件时，画面不再只是中性呈现，而是在无声地主张一个实物不具备的属性。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "使用实物图片或视频证明商品外观"
does_not_apply_when: "纯内部示意且明确不代表真实商品呈现"
counterexample: "用夹子收腰后拍摄，却让顾客认为商品本身是收腰版型；或用广角低角度拉长比例使版型与实物不一致"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R02-02（L456-464）；S-02.txt 三份原文共同支持——专家甲 §1-3（L39）、专家乙 forbidden 四条（L280-286）、专家丙 §四-2（L408-416）"
```

```yaml
elicitation_item_id: ELI-0216
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "画面不足时是否可以改交'新品预告＋问题征集'"
expert_statement: "从商品理解降级为新品预告属于任务结果变化，必须取得用户同意并如实标注产物性质（交付物必须明确命名为'新品预告'，不得写成'商品理解''看懂这件大衣'）；静默降级即失败——任务对象被偷换，用户失去了'要不要接受降级'的决定权。降目标不降真实性：预告文案同样禁材质、价格、品质、人群断言，镜头诚实三条件同样约束。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "现有资料或画面不足以完成原目标，但存在较低信息密度的合法内容"
does_not_apply_when: "原目标仍可通过受限路线完成"
counterexample: "系统静默交付新品预告并声称已完成商品理解"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R02-03（L466-474）；三份原文共同支持——专家甲 §7 静默降级（L106）、专家乙 §8 HUMAN_DECISION_REQUIRED（L300-301）、专家丙 §一与附录（L338、L517-523）"
```

```yaml
elicitation_item_id: ELI-0217
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "系统说明拍摄清单能达到什么水平"
expert_statement: "系统只能承诺交付物达到规定的信息与制作规格（'按清单拍全后，素材具备支持商品理解的最低信息'），不得承诺观众一定理解、喜欢、咨询或产生传播结果；承诺的主语是规格不是结果——结果里有用户执行与观众反应两段系统管不到的路。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "系统说明受限版本或拍摄清单能够达到的水平"
does_not_apply_when: "有独立、充分的真实效果证据且合同允许作相应陈述"
counterexample: "'按这五个镜头拍，顾客一定会看懂并下单。'"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 HR-S02-R02-04（L476-484）；S-02.txt 专家甲 §1-2（L37）、§7 承诺越界（L108）"
```

```yaml
elicitation_item_id: ELI-0218
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "资料与画面双缺，文案容易改用形容词撑场"
expert_statement: "'高级、显瘦、有质感、百搭、适合通勤'一类评价性表述在资料不足的版本中一律禁用——它们的机制是用形容词填画面留下的空，让内容显得完整靠的不是信息而是修辞；同样禁'看完你就全明白了'式看懂承诺与替顾客下结论。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "商品事实或画面证据不足，仍需交付内容"
does_not_apply_when: "该判断有实拍画面或有来源资料直接支撑（此时仍受表达边界词表约束，见 PCR-02）"
counterexample: "内容无材质声明，却通过滤镜和'高级质感'共同制造品质暗示"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-02.txt 三份原文逐字共识——专家甲 §7 形容词填坑（L102）、专家乙 forbidden 第一条（L268）、专家丙 §四-1（L402）；候选包已确认判断 R02-7（L335）但未单独挂卡。正式词表边界见 PCR-02"
```

```yaml
elicitation_item_id: ELI-0219
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "人工评审一条大衣'商品理解'内容是否成立"
expert_statement: "判断'商品理解内容'是否成立时，不只检查商品是否出镜，还要检查画面是否覆盖完整轮廓、上身、动态及必要细节，并判断观众是否能够提出具体商品问题。"
statement_type: METHOD
applies_when: "人工评审大衣商品理解内容"
does_not_apply_when: "任务明确只是新品预告"
counterexample: "商品出镜三秒但看不清轮廓，仍被判为完成商品理解"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S02-R02-01（L488-496）；本卡列举的'动态'是否为一票否决项未裁，见 ELI-0235"
```

```yaml
elicitation_item_id: ELI-0220
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "评审资料不足条件下的拍摄方案或成片"
expert_statement: "受限大衣内容应检查三类失败：评价词是否填坑、镜头是否改变商品印象、承诺是否从规格膨胀为结果。"
statement_type: METHOD
applies_when: "评审资料不足下的拍摄方案或成片"
does_not_apply_when: "所有商品事实和真实素材均充分——但镜头诚实仍应独立检查"
counterexample: "内容无材质声明，却通过滤镜和'高级质感'共同制造品质暗示"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 JC-S02-R02-02（L498-506）"
```

```yaml
elicitation_item_id: ELI-0221
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "如何在成片上判定'知道有新品'与'真正看懂'"
expert_statement: "两个可直接执行的判据：①去标题测试——去掉标题和'新品'两个字后，顾客能否仅依据内容说出这件大衣的整体外观以及至少一个可区分特点；不能则仍是新品预告。②复述式判据——观众看完能说出'这是一件 XX 领、XX 长度、XX 版型的大衣，看起来是 XX 面料，上身大概 XX 效果'，才算看懂。"
statement_type: METHOD
applies_when: "判定一条内容属于存在性告知还是商品理解"
does_not_apply_when: "任务已明确命名为新品预告"
counterexample: "顾客看完只能说'我知道它上新了'，内容仍被标记为完成商品理解"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-02.txt 专家乙去标题测试（L303-307）＋专家丙复述式测试标准（L491-503）——候选包漏编，据原文对照审查报告 S02 问题 6 补入并合并为一卡"
```

```yaml
elicitation_item_id: ELI-0222
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "内容发布后评论区有真实顾客反馈可观察"
expert_statement: "用顾客问题的具体程度作为商品理解的反馈信号：只能问商品是什么、多少钱，说明主要停留在存在性认知；能够问长度、袖口、上身等具体问题，说明形成了更具体的理解。"
statement_type: METHOD
applies_when: "内容发布后有评论或咨询反馈可观察"
does_not_apply_when: "尚无真实用户反馈——不能把该信号当作事前事实"
counterexample: "只有泛问仍宣称观众已充分理解商品"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S02-R02-03（L530-538）；S-02.txt 专家甲核心结论 3（L7）。这些问题能否升级为受众资料来源另见 PENDING 卡 ELI-0238"
```

```yaml
elicitation_item_id: ELI-0223
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "判定'现有图片只能识别商品身份'之前"
expert_statement: "在判定画面不足之前先做一项前置核查：原始图片究竟是源文件本身缺乏有效细节，还是只是当前预览／展示尺寸过小；若原图实际分辨率足够，重新检查后可能直接恢复制作。同时确认——当前图片不能通过重新裁切或放大恢复原本不存在的细节信息，技术放大不等于新增事实。"
statement_type: METHOD
applies_when: "以'画面不足'为由准备停止或降级之前"
does_not_apply_when: "源文件已核实确无有效细节"
counterexample: "对低清图片做 AI 补细节、纹理增强或生成上身效果，再当作该商品实拍"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S-02.txt 专家乙 §4 第二条假设（L207-209）＋forbidden 第二条（L272-274）——候选包漏编，据原文对照审查报告 S02 问题 6 补入"
```

```yaml
elicitation_item_id: ELI-0224
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "同一件实物无法拍摄，识别级图片又不足以形成商品理解"
expert_statement: "实物无法拍摄且用户拒绝把目标降为新品预告时，必须停止商品理解任务，停止交付物是恢复条件说明书而不是空手拒绝；用户同意降级后只允许完成'告知新品存在＋问题征集'。"
statement_type: BOUNDARY
applies_when: "画面无法达到商品理解门槛，且同一实物不可拍"
does_not_apply_when: "同一实物可拍（此时按 ELI-0225 继续），或已有足够真实素材"
counterexample: "未经同意把预告版当成商品理解版交付"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 CR-S02-R02-02（L434-442）；S-02.txt 专家甲 §8（L112）、专家乙 §8（L294-298）。注意：本卡未覆盖'轮廓级画面＋文字资料补足能否恢复'这一支路，该支路专家甲与乙丙相反且未裁，见 PENDING 卡 ELI-0236"
```

### R03 段：实物当天可拍局面的三专家收敛结论

```yaml
elicitation_item_id: ELI-0225
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "识别级商品图不能让顾客看懂大衣，但门店当天能拿到同一件实物并愿意完全照拍摄清单补拍"
expert_statement: "确认同一件实物当天可拍后应继续工作，不停止：缺失的性质从'信息不存在、无人提供'变成'信息还没到手'，前者该停，后者该继续并进入'备产等素材'；专业上继续的理由是没有补写商品事实，而是把获取事实的责任转交给现场拍摄——缺什么就去取得什么。"
statement_type: METHOD
applies_when: "现有画面不足以支撑商品理解，但同一件实物可被真实拍摄、且执行方愿意按清单补拍"
does_not_apply_when: "实物不可拍或无人可执行拍摄（回落 ELI-0224）"
counterexample: "把'资料当前不足但可现场采集'与'资料不可取得'混为一谈，一律按停止处理"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 三专家收敛（专家一 L5-27／专家二 L445-447、L466／专家三 L1256、L1280-1281、L1288）；取代候选包 R01/R02'继续做 vs 必须停'旧分歧口径与 CR-S02-R02-01"
```

```yaml
elicitation_item_id: ELI-0226
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "同上；素材尚未回传时今天最多能交付什么"
expert_statement: "素材回传前的交付物重定义为三件且三件都是中间产物：①实拍清单（每个镜头写明拍什么、怎么拍、拍到什么程度可用、替顾客回答哪个问题）；②不补写任何商品事实的中性内容框架（开场／看懂点占位／结尾引导，事实位全部留空标注'待素材'）；③素材验收标准（哪条能用、哪条须重拍）。素材回传并通过验收之前不承诺：已形成可发布成片、发布时间、任何具体商品描述、原目标完整达成。"
statement_type: BOUNDARY
applies_when: "实物可拍、已决定继续，但真实素材尚未回传"
does_not_apply_when: "素材已回传并通过验收（进入按实际覆盖范围写作阶段）"
counterexample: "在素材回来前预写'垂感好''上身显高'等只能由素材确认的描述"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 三专家收敛（专家一 L7-18、L31-71／专家二 L449-461／专家三 L1257-1258、L1282-1284）。本卡同时是 UN-S01-05'占位骨架／留空脚本'议题的追加证据，本场不裁断"
```

```yaml
elicitation_item_id: ELI-0227
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "交付了拍摄清单之后，是否可以对用户报'已完成'"
expert_statement: "交付拍摄清单不得标记任务完成——清单是内部工具、是把'我们不知道'变成'我们去拍'的证据采集准备，顾客还没有看到任何东西；任务完成的唯一标准是发布内容能让顾客看懂这件大衣。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "以拍摄清单／内容框架／验收标准作为阶段交付物"
does_not_apply_when: "成片已发布且经验收判定达成理解目标"
counterexample: "把'已交付一条商品理解内容''已经可以发布'写进交付说明，而实际只给了清单"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 三专家收敛（专家一 L73-82／专家二 L553-555、L576／专家三 L1261、L1284、L1332-1334）"
```

```yaml
elicitation_item_id: ELI-0228
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "门店回传的素材只覆盖了清单的一部分（例如只有正面平铺，没有局部和上身；或关键部位模糊、颜色失真）"
expert_statement: "素材不足时继续停止在'素材不可用'状态，不能硬剪：缺什么内容就缩到什么并把缺口明说，不能通过剪辑、滤镜、文案补写掩盖画面信息不足，也不得用相似商品画面、库存图或口头描述顶替未拍到的镜头；降级产物必须如实命名（如'商品初步展示素材'／仅覆盖已有素材的'细节看点'内容），不得冒充完成，或继续要求补拍缺失部分。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "实拍素材部分回传，未覆盖清单的必需镜头"
does_not_apply_when: "素材按清单拍全并通过验收"
counterexample: "素材没拍全，却用'有质感、显瘦、挺括'等文案补齐；或用相似大衣的上身镜头补位"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 三专家收敛（专家一 L71、L84-99／专家二 L475、L544-549、L561-563／专家三 L1263、L1326-1328、L1336-1338）。'用户持续不回应时降级内容发布还是搁置'未裁，见 ELI-0237"
```

```yaml
elicitation_item_id: ELI-0229
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "决定实拍能把哪些缺口补回来、哪些补不回来"
expert_statement: "把缺口按'实拍能否恢复'二分——能恢复：外观、结构、细节、动态、以及实物自带标签可查的信息；不能恢复：品牌故事、设计初衷、顾客故事。后者不随实拍恢复，本轮就不做、内容里就不出现，而不是降低真实性去凑；它们的缺席不影响'看懂商品'这个目标本身。"
statement_type: METHOD
applies_when: "实物可拍、需要划定本轮内容可讲范围"
does_not_apply_when: "任务目标本身就是品牌故事或创始人理念型内容（此时对应资料从增强项变成必要依据，见 ELI-0207）"
counterexample: "实拍素材到位后顺势补写品牌理念或创始人故事"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 专家三 §2 Step2（L1289）＋建议批准第 4 条（L1264）；专家一（L57-61）、专家二（L461）同向禁止预写未经素材确认的内容"
```

```yaml
elicitation_item_id: ELI-0230
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "没有任何材质资料，但实物在手"
expert_statement: "材质成分可以拍衣服里缝着的成分标／洗水标特写，属于有据可查、不是补写；即实物自带的标签是材质类事实的一条合法来源通道。"
statement_type: BOUNDARY
applies_when: "缺材质资料且同一实物可拍，需判断材质信息是否仍属不可得"
does_not_apply_when: "实物不可拍或标签缺失／不可辨认；也不适用于保暖性、耐穿度、品质评价等标签不承载的判断"
counterexample: null
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 专家三 §1（L1280）＋建议批准清单基线（L1262）——【单源】专家一、专家二未提及该通道，不构成三专家收敛；按规范 4 以原文入卡并标注单源"
```

```yaml
elicitation_item_id: ELI-0231
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "清单要交给门店普通员工执行"
expert_statement: "清单按'镜头↔顾客问题'成对编写——每个镜头标注它替顾客回答什么问题，并附合格／不合格示例与'拍到什么程度可用'的判据，以降低执行偏差；例如'拍正面上身，镜头中要能看清肩线落点、衣长与身体比例、门襟闭合后的整体轮廓'。"
statement_type: METHOD
applies_when: "把拍摄任务交接给非专业执行人员"
does_not_apply_when: null
counterexample: "只给镜头名词清单（'拍正面''拍细节'），不写合格标准与对应顾客问题"
candidate_destination: KERNEL_METHOD
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 专家三 §1 与 §10 possible_module_method（L1282、L1359）、REVIEW_SUMMARY 建议修订（L1267）；专家一 L43-46、专家二 L451-453（每个镜头需要证明什么、拍到什么程度算合格）同向"
```

```yaml
elicitation_item_id: ELI-0232
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "实拍素材回传，判断可否进入成片制作"
expert_statement: "素材回传后逐条验收：关键部位是否清楚；颜色、版型是否因角度或光线失真；是否能看到轮廓而非只有局部；是否有上身效果而非只有平铺。并按实际拍到的信息决定内容可讲范围——不能按原拍摄计划假定素材已经拍到。"
statement_type: METHOD
applies_when: "实拍素材回传后的可用性判定与声明范围收缩"
does_not_apply_when: null
counterexample: "按清单原定镜头写好文案，素材缺上身仍保留上身描述"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 三专家收敛（专家一 §3 素材核验标准 L62-71／专家二 §10 possible_judge_calibration L596-597、Step4 L474-475／专家三 §1 素材验收标准 L1282、§10 降级对照表 L1360）"
```

```yaml
elicitation_item_id: ELI-0233
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "本案大衣：需要给门店一份'拍到什么才算看懂'的最低画面清单"
expert_statement: "本案大衣的最低画面清单，R02 结构为'底线三件＋增强两件'——底线：完整轮廓（正背、自然下垂）、上身展示、动态展示；增强：面料表面近拍、关键局部。R03 三专家清单在此基础上共同覆盖：完整正面与完整背面轮廓（挂拍／平铺）、侧面或连续转动、开合状态与主要结构、关键局部（领口、肩线、门襟、袖口、下摆、扣袋）、面料自然光下的表面纹理近拍、真人正／侧／背整体上身、走动或转身的动态与垂坠；专家三另加内里与成分标洗水标特写、上身镜头标注穿着者身高。本清单只对大衣成立，不得外推为全品类规律。"
statement_type: BOUNDARY
applies_when: "任务目标是让顾客形成大衣外观与穿着层面的初步理解，且实物可拍"
does_not_apply_when: "其他品类、纯新品预告或只需商品身份识别的任务"
counterexample: "将同一清单无条件套用于首饰或鞋类；用大衣动态展示要求评判耳饰内容"
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 MM-S02-R02-02（L520-528）＋S02-R03 三专家清单（专家一 L33-46／专家二 L520-535／专家三 L1262）合并为一卡（规范 6 同题合并）。分歧保留：专家二把上身与动态设为'内容准备谈论上身比例／活动状态时'才必需的条件项（L531），是否为无条件底线未裁，见 ELI-0235；品类外推校准走 EV-01"
```

```yaml
elicitation_item_id: ELI-0234
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "专家三对本局面三种失败方式各给了一个具名标签候选"
expert_statement: "本轮出现三个专家新命名的失败概念：FAKE_COMPLETION_BY_DELIVERABLE_SWAP（把交付清单宣布为内容已完成）、FOOTAGE_SUBSTITUTION（用相似商品画面、库存图或口头描述顶替未拍到的镜头）、SILENT_GOAL_SWITCH（因用户不回应而静默转为新品预告）。三者均为新标签候选，须走 B.8.1 覆盖审查确认 B.6 既有标签能否覆盖，不得私加标签、不得往既有标签塞新语义。"
statement_type: FAILURE_MODE
applies_when: "把本场失败模式接入正式失败标签体系时"
does_not_apply_when: "B.6 既有标签已能完整表达该失败语义（则映射既有标签，不新增）"
counterexample: "直接把三个名字写进 Rule Engine 或错误码表"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 专家三 §7（L1332-1342）；S02-R02 三份原文均把 failure_label_candidate 标为 NOT_ASSIGNED 或注明'不提请入册'（S-02.txt 专家甲 L100、专家乙 L270-290），该保留态度一并记录"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0235
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "静态素材覆盖轮廓、局部、面料、上身，独缺动态"
expert_statement: "'动态展示'是否为大衣商品理解内容的画面底线，本场存在同文双口径：候选包 L327-331 把动态写成已认可的底线三件之一，同包 UN-S02-R02-02（L552-560）又把'缺动态是否算商品理解成立但降档'列为未裁决，并自记反例'未裁决便把动态设为所有大衣内容的一票否决项'。原文侧：专家甲主张大衣是穿出来的形、底线必含上身与动态，但同时自曝提请裁定（S-02.txt L96、L125）；专家乙丙把上身／动态设为'内容准备谈论穿着表现时'才成为必要证据的条件项（L248、L455-469）；S02-R03 专家二（L544-549）与专家三（L1326）在缺动态时给出的是'降级为外观理解／细节看点内容并删除相应声明'，未回答它是否仍算商品理解成立。"
statement_type: BOUNDARY
applies_when: "判定一条缺动态的大衣内容是否达成商品理解目标，以及必须公开哪些限制"
does_not_apply_when: "动态素材已具备，或任务只是新品预告"
counterexample: "未裁决便把动态设为所有大衣内容的一票否决项"
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
founder_ruling_20260817: "懂＝量级非开关：缺动态但静态齐全＝懂度7–8/10，成立但降档（有动态视频＝10）"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包已确认判断 R02-3（L327-331）× UN-S02-R02-02（L552-560）同态矛盾，原文对照审查报告 S02 问题 3 坐实；S-02.txt 专家甲 L96/L125 vs 专家乙 L248、专家丙 L455-469"
founder_question: "缺动态但静态四类齐全的大衣内容，记为'商品理解成立但降档并明示缺口'，还是记为'未达成商品理解'？（实证输入见 EV-01；裁决前 ELI-0214/0219/0233 中的'最低理解门槛'含动态与否保持悬置）"
```

```yaml
elicitation_item_id: ELI-0236
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "画面只到轮廓级、无上身与动态，但可以补充有来源的文字商品资料"
expert_statement: "画面不足时能否用有来源的文字资料把'让顾客看懂'目标恢复，三份原文相反：专家乙给出路径二——画面有限但补充能形成'商品整体是什么样＋至少一个可区分真实特点'的有来源资料即可恢复（S-02.txt L250-257）；专家丙给出条件二——补充材质成分、版型特征、适穿场景、设计要点等有来源事实，最低门槛为完整轮廓＋（上身效果或局部细节）（L453-471）；专家甲相反——'文字资料补不回画面，对服装看懂而言画面是承重墙、资料是装修'（L6、L41）。候选包将该分歧写成'补充文字版型或材质说明可以完全替代缺失的上身和动态画面'并列入 REJECTED，审查报告认定为稻草人化（无人持有'完全替代'这一极端立场），两条非画面恢复通道整体丢失。"
statement_type: BOUNDARY
applies_when: "实物不可拍或画面只能到轮廓级，但有可取得的有来源商品资料"
does_not_apply_when: "同一实物可拍（走 ELI-0225 补画面通道）"
counterexample: "材质说明配一张认不清的图，顾客得到的仍是'知道'而非'看懂'（专家甲反例，L41）"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "按懂度量级制评估：有来源文字资料可加分但不满级，不再是能否恢复的二选一"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "原文对照审查报告 S02 问题 1/2 与'仅 Founder 能决定的事项'第 2 条；据规范 3.5 从候选包 R02 REJECTED 第 3 条（L368）撤出并按原文重立"
founder_question: "'轮廓级画面＋有来源文字资料补足'能否使'看懂商品'目标恢复（专家乙丙＝能，专家甲＝不能）？裁决结果决定 ELI-0224 的必停边界是否需要开一条非画面恢复通道。"
```

```yaml
elicitation_item_id: ELI-0237
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R03
source_situation: "门店回传素材不全，用户又持续不回应，无法取得降级同意"
expert_statement: "素材不全且用户持续不回应时，降级内容是直接发布还是搁置待补，专家三明列为需要 Founder 决定并计入 HUMAN_DECISION_REQUIRED（L1270、L1348）；专家二把同一缺口表述为'门店只完成新品识别素材时，是否正式把任务降低为新品预告'亦列 HUMAN_DECISION_REQUIRED（L573-574）。既有纪律 ELI-0216 要求降级必须取得用户同意，但用户不回应时同意无从取得，降级发布许可归属未定。"
statement_type: BOUNDARY
applies_when: "实拍素材未覆盖必需镜头，且用户对降级请求持续不回应"
does_not_apply_when: "用户明确同意或明确拒绝降级"
counterexample: "以'用户不回应＝默认同意'为由直接发布降级内容"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "系统无自动发布（用户输入式生产系统），预设：压着不发"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "S02-R03 专家三 REVIEW_SUMMARY 需要 Founder 决定（L1270）＋§8（L1348、L1353）；专家二 §8（L573-574）"
founder_question: "素材不全且用户持续不回应时，降级内容是直接发布（并如实标注）还是搁置待补？降级发布许可归属谁？"
```

```yaml
elicitation_item_id: ELI-0238
source_session: DIYU-KE-S02-20260817-001
source_round: S02-R02
source_situation: "降级为新品预告＋问题征集后，评论区收到顾客问题"
expert_statement: "新品预告收集到的顾客问题能否正式成为受众资料来源；若可以，如何区分真实需求信号、偶发评论和运营诱导结果。专家甲把它列为设计时待裁三项之一，并指出若可立，降级路径将从'退路'升格为'采料工序'（S-02.txt L90、L126）。"
statement_type: PREFERENCE_HYPOTHESIS
applies_when: "内容以问题征集作为信息采集路径，且有真实可追溯的用户反馈"
does_not_apply_when: "没有真实用户反馈或反馈不可追溯"
counterexample: "将一条评论直接升级为确认受众事实"
candidate_destination: BRAND_MEMORY_PENDING_EVIDENCE
review_status: ROUTED
founder_ruling_20260817: "预设：评论不自动入库"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "候选包 UN-S02-R02-03（L562-570）；S-02.txt 专家甲 §6-A（L90）、§9-3（L126）"
founder_question: "评论区顾客问题能否正式立为受众资料的采集来源？若可以，真实需求信号 / 偶发评论 / 运营诱导结果如何区分，入库须经哪一道人工确认？（A.9.6 规定访谈陈述不够格直接进 Brand Memory，本项同样不得自动入库）"
```

---

## 三、来源统计与残留说明

### 卡数与去向

| 项 | 数 |
|---|---|
| 卡总数 | 38 |
| ROUTED | 34（ELI-0201…0234） |
| PENDING | 4（ELI-0235…0238） |
| KERNEL_METHOD | 10 |
| RULE_CANDIDATE | 12 |
| JUDGE_QUESTION | 7（含 PENDING 1） |
| CASE_REFINEMENT | 4 |
| CONTRACT_PROPOSAL | 4（含 PENDING 2） |
| BRAND_MEMORY_PENDING_EVIDENCE | 1（PENDING） |
| SEMANTIC_LAYER / CASE_CANDIDATE | 0 |

provenance：34 张 ROUTED ＋ 4 张 PENDING 全部为 `AI_PROPOSAL_FOUNDER_APPROVED`；`FOUNDER_ORIGINAL_JUDGMENT` 与 `AI_PROPOSAL_FOUNDER_REVISED` 各 0——本场无与候选分析可分离的 Founder 原始理由，候选包内唯一一条 `FOUNDER_REVISED`（HR-S02-R02-01）经审查报告 F-D 坐实系 REVIEW_SUMMARY 建议，已按规范 3.3 降标为 APPROVED（见 ELI-0214）。

### 未转卡内容与原因

1. **旧"继续做 vs 必须停"分歧口径**：候选包 CR-S02-R02-01（L424-432，实物可拍时继续交付最低画面清单）及 R01/R02 围绕该分歧的立场性表述，已被 S02-R03 三专家收敛整体取代，不再单独立卡，由 ELI-0225／0226／0227 承接。
2. **9 条 REJECTED 一律不以 REJECTED 身份出现**（候选包 R01 四条 L81-84、R02 五条 L366-370；TXT 与 REVIEW_SUMMARY 均无 Founder 否决动作，原文对照审查报告 F-D／S02 问题 1 已坐实为镜像反推）。逐条去向：
   - R01-1「仅因缺材质证明就停」、R02-2「实物可拍时仅因图片不足绝对停」→ 实质由 ELI-0225 正面收敛承接，不另立卡；
   - R01-2「把材质/价格/库存/承接定为所有任务固定必需」→ ELI-0207 正面覆盖；
   - R01-3「用合理假设补写事实」→ ELI-0203 正面覆盖；
   - R01-4「QUICK 可跳过事实与合规检查」→ ELI-0204 正面覆盖，正式定义交 PCR-01／PCR-02；
   - R02-1「识别级图片足以完成大衣商品理解」→ ELI-0214 正面覆盖；
   - R02-3「文字说明可完全替代上身与动态画面」→ 审查报告认定为对专家乙丙"轮廓级画面＋文字补足可恢复"的稻草人化，无人持该极端立场；乙丙真实主张按原文重立为 PENDING 卡 ELI-0236；
   - R02-4「三＋二外推全品类」→ 由 ELI-0233 的 does_not_apply_when 承接，实证走 EV-01；
   - R02-5「素材达最低规格＝顾客一定看懂」→ ELI-0217 正面覆盖。
3. **BLOCKING / QUALITY_REDUCING 主题缺口（不造卡，仅登记）**：排期主题 2 Q4 与预期产出明文要求逐项判定 `BLOCKING|QUALITY_REDUCING` 并产出 `missing_context[].impact` 判断方法，本场三份原文零讨论、候选包未登记落空（标准对齐复核结论 S02 ①，判定"主题 2 实质未完成"）。本场以"删除测验"（ELI-0201／0202）＋"四元组条件化"（ELI-0207）为实际方法产出，是否以其替代该二元标签须由 Founder 显式裁决或补会，本文件不代为裁决、不新增状态枚举。
4. **产品合同与实证问题不转 ELI 卡（规范 4.3），引用队列号**：
   - UN-S02-R01-01 直发无人审路径 → PCR-02；
   - UN-S02-R01-02 指向性语言／评价词／可验伪断言正式词表 → PCR-02（ELI-0218 只立"资料不足时禁遮羞词"的业务判断，不定义词表）；
   - UN-S02-R01-03 QUICK 正式定义 → PCR-01／PCR-02，并附带标准对齐复核结论 S02 ②：候选包 QUICK 断言与排期口径（"QUICK 只能跨过 QUALITY_REDUCING 缺失且必须产生对应 ASSUMPTION"）不一致且无专家支撑，一并交合同审查对齐；
   - UN-S02-R01-04「已确认无禁用词 vs 从未梳理」的 FactValue 映射 → PCR-02（排期主题 2 Q5 指定用 A.2.4 五态表达）；
   - UN-S02-R01-05 最大高价值澄清轮数与停止策略 → PCR-01；
   - UN-S02-R02-01 最低画面集是否按品类分层校准 → EV-01（真实素材验证，禁止直接全品类化）。
5. **"实物可拍"前提的口径矛盾（已消解，登记备查）**：审查报告 S02 问题 4 指出候选包把专家甲的 assumption 升格为已确认前提、与包内 assumption 条目互斥。S02-R03 QUESTION_CARD 把"门店当天能拿到同一件实物、愿意完全照清单补拍"列为本轮唯一新增事实，故 R03 分支（ELI-0225…0234）以该事实为给定输入；实物不可拍分支由 ELI-0224 单独承载，两支不再互斥。
6. **专家乙"只输出待补画面的制作结构"选项**（S-02.txt L225-229）：属 UN-S01-05（占位骨架／留空脚本是否为合法交付形态）的追加证据，本场不裁断；其合法性在 R03 被三专家以"事实位留空的内容框架"共同承接，证据随 ELI-0226 登记，交 S01 未决项裁决时一并计入。
7. **具体案例答案不写成通用规则**：三专家 R03 给出的逐条镜头文案示例（如"拍正面上身要看清肩线落点、衣长与身体比例、门襟闭合后的整体轮廓"）、开场／结尾结构示例、大衣清单的具体件数，随案例卡 ELI-0233／ELI-0231 保存，不外推为全品类硬规则（规范 6：规则进 Core、数值进案例）。
8. **不逐条转"已确认判断"清单**：候选包 R01 十一条、R02 十一条"已确认判断"未逐句立卡（E.10 红线：强制每条专家表述进仓库），其可迁移内容已被上列 34 张 ROUTED 卡覆盖；纯局面复述与统计性表述不入库。
9. **跨场重复**：ELI-0204（快与低置信度不降标准）在 S07 场另有同题卡，各场保留各自卡，编号由 S07 场编译产出后互相回填。
