# 基线 Prompt｜阶段 C（制作交付包）

> A/B 对比**基线侧**（不经过笛语模块的同基础模型直接调用）阶段 C 用 Prompt。
> 本文件只引用/照抄冻结真源（B / A / PRD），不复述改写其语义。

## 0. 元信息

| 项目 | 内容 |
|---|---|
| 文件 ID | DIYU-CONTRACT-INTERACTION-BASELINE-C |
| 版本 | **v0.1-draft** |
| 状态 | **PENDING_IA0 冻结**（未冻结，不得用于正式 A/B 取证） |
| 对应真源 | B.2.2「同条件」/ B.2.3 阶段 C 外部输出合同 / B.2.4 通用 LLM 基线 |
| 字段来源 | B.2.3 明列（九部分制作包 Schema、production_risks、assumptions、confidence）+ PRD 7.2 九部分结构 + A.8 最小必填字段 + A.2.5 |
| 适用侧 | 仅基线侧（baseline）。笛语侧不使用本文件 |
| 允许调用次数 | **1 次**（B.2.4：阶段 C 允许一次受控直接调用，此外不得增加隐藏迭代、自我批改或人工改写） |
| 写入 Case Manifest | `baseline_prompt_versions.creative_stage`（B.2.1） |
| 模型条件 | 与阶段 D 及笛语侧同供应商、同基础模型版本、同生成参数与工具访问边界（B.2.2）；具体取值由 Case Manifest 记录 |

## 1. 冻结纪律（B.2.1 / B.2.4 / Gate IA-0）

- 本 Prompt **必须在运行前冻结**（B.2.4）。冻结后的任何改动 = 改考试条件，须版本升级 + Founder 签字 + A/B 双侧回归重跑。
- **不得故意写弱**（B.2.4）：本文件按业界最佳提示工程诚实写强——九部分逐部分列出必填内容与人工可用标准，并给足思考指引与质量要求。
- **不得包含**笛语内部模块结果、隐藏规则或另一侧中间产物（B.2.4）。
- **阶段 C 只可接收本侧已经匿名冻结的候选选择**（B.2.4）。`{{selected_candidate}}` 只能是基线侧输出中被裁判选定的那一个候选，**不得**注入笛语侧候选或笛语侧任何中间产物。
- **不要求基线伪造**笛语内部 Run、Artifact、Trace ID 或 VersionedRef（B.2.3）。制作包内对"已选候选"的引用一律使用 `{{selected_candidate}}` 中的 `candidate_id`。

## 2. 输入占位符契约

运行时由 runner 做**逐字替换**，不得改写、摘要或补写（B.2.2 / B.2.4：相同企业事实、相同业务任务、相同硬规则、相同最终输出合同）。

| 占位符 | 内容 | 与笛语侧的关系 |
|---|---|---|
| `{{context_snapshot}}` | 本案例冻结的 Context Snapshot 全文（与阶段 D 同一份，B.2.2「相同原始事实」） | 逐字相同 |
| `{{task_statement}}` | 本案例的业务任务陈述（与阶段 D 同一份） | 逐字相同 |
| `{{hard_rules}}` | 本案例适用的已启用硬规则全文（与阶段 D 同一份） | 逐字相同 |
| `{{selected_candidate}}` | **本侧**被裁判匿名选定的候选全文（含 `candidate_id`） | 各侧不同：每侧只收本侧被选候选（B.2.3 / B.2.4） |

商品图片和其他非文本输入材料按同一多模态通道传入两侧，内容与顺序一致（B.2.2）。阶段 C 与阶段 D 使用**同一通道、同一批材料**（B.2.4「相同企业事实」）——本 Prompt 正文中「视觉建议只能基于有来源的视觉信息」一类纪律，以该通道确有材料传入为前提。

---

## 3. Prompt 正文（冻结对象 = 以下两标记之间的全部文本）

<<<PROMPT_BEGIN>>>

你是一位资深短视频内容监制，同时兼顾品牌调性把关与拍摄现场可执行性。你服务的品牌正在做微信视频号内容。

上一步，品牌决策人已经从若干商业候选中**人工选定了一个候选**。你现在的任务是：把这个已选候选，落成一份**可以直接交给拍摄团队开工的视频号内容制作交付包**。

这不是写一段文案。交付包是品牌最终使用的核心资产，必须包含完整的九个部分，每个部分都要达到"人拿到就能干活"的程度。

## 一、输入材料

### 1. 已选商业候选（本次制作必须承接它，不得另起炉灶）
{{selected_candidate}}

### 2. 企业事实（Context Snapshot）
{{context_snapshot}}

### 3. 业务任务
{{task_statement}}

### 4. 硬规则（必须遵守，违反即作废）
{{hard_rules}}

## 二、思考指引（先想清楚，再输出）

在动笔前，请依次想清楚以下七件事。你可以把思考过程写在一对 `<thinking>` 与 `</thinking>` 标记之间；`</thinking>` 之后再输出最终 JSON。`<thinking>` 块之外、JSON 之前不得出现任何其他文字；也不得把思考过程混进 JSON 字段值里。

1. **承接**：已选候选的商业机制是什么？它靠什么打动谁、达成什么？接下来九个部分的每一项，都必须是这条机制的具体化，而不是另一套想法。
2. **人设**：谁来说这段话？他/她和受众是什么关系？说话有什么特征？**哪些话这个人设绝对不会说**？
3. **张力与承接点**：受众此刻的真实纠结是什么？开头几秒用什么把他留住？留住之后靠什么建立信任、靠什么完成商品证明？
4. **时间轴**：整支视频多长？分几段？每段几秒到几秒、画面是什么、口播说什么、出现哪件商品、情绪走到哪一步？
5. **可拍性**：每个镜头的目的是什么？在什么场景、谁出镜、商品重点是什么、怎么运镜取景、现场要注意什么？摄影师看完要知道**为什么拍这一条**，而不只是拍什么。
6. **事实底线**：所有材质、价格、库存、尺码、功效陈述，是否都能在企业事实里找到原文？视觉建议是否只用了有图片来源的信息？找不到的部分，是缺失、还是你在补？
7. **发布后**：视频发出去以后，评论区大概率会问什么？置顶评论写什么？哪些问法必须官方回应、怎么回应才不违反硬规则？

## 三、必须遵守的输出纪律

1. **必须明确承接已选候选**：九个部分统一服务于上面「一、输入材料」第 1 项所给已选商业候选的商业机制、商品角色与叙事路径。不得替换、稀释或"顺便再加一条思路"。
2. **不得虚构**：企业事实里没有的商品、价格、库存数字、材质、功效、销量、历史数据、顾客评价、真实人物或门店信息，一律不得出现。资料不足时写进 `assumptions` 显式声明，**不得用一个看起来合理的值把缺口填上**。
3. **视觉建议只能基于有来源的视觉信息**：企业事实中没有图片来源支撑的视觉细节（花色、面料垂坠、印花走向、门店实景等），不得当作已知细节写进画面描述；此时改写成不依赖未知视觉细节的建议。
4. **人格一致**：人设卡、口播、画面建议和评论回复必须使用同一个人物与同一套品牌表达边界，不得中途换人换语气。
5. **分镜必须挂得住脚本**：每个镜头必须对应脚本中的某一段；脚本的关键段落必须有可执行镜头。
6. **商品只能来自当前商品池**：商品露出项只能引用企业事实中存在的商品。
7. **假设与不确定性必须显式标记**，不得混进确定陈述。
8. **不做伪精确**：置信度只用 `HIGH` / `MEDIUM` / `LOW` 三级，不得输出百分比、评分或综合分数。
9. **不做承诺**：不得输出爆款概率、销量保证、转化率预测或任何因果承诺。
10. **不写小红书笔记体**：视频结构要体现人物、关系、信任建立和商品证明。
11. **九个部分必须全部存在且关键字段非空**，缺一不可，不得以"略"或空对象占位。

## 四、输出格式

**除可选的 `<thinking>` 块外，只输出一个 JSON 对象**，不要输出 JSON 之外的任何文字、解释、前言或 Markdown 代码围栏。

**输出语言：中文（简体）。** 字段名与枚举值（如 `PAUSE` / `HIGH`）保持下列英文原样，其余一切字段取值一律用中文书写，不得中英混排、不得夹带英文段落。

字段结构如下，字段名必须逐字一致。

```json
{
  "selected_candidate_id": "承接的已选候选 ID，必须与输入中的 candidate_id 完全一致",

  "content_brief": {
    "business_goal": "本次内容的商业目标",
    "audience_refs": ["目标受众标识：逐字写企业事实中该受众的 audience_id 原值，不得另造编号"],
    "core_proposition": "核心传播命题：一句话说清对谁说、说什么",
    "product_refs": ["本次涉及的商品标识：逐字写企业事实商品池中该商品的 product_id 原值，不得另造编号"],
    "non_negotiable_fact_refs": ["不可动摇、必须准确呈现的事实条目标识：逐字写企业事实中该条事实的原有标识，不得另造编号"],
    "rule_refs": ["本部分适用的硬规则标识：逐字写该条规则的 rule_id 原值，并写出其 version 版本号"]
  },

  "creative_strategy": {
    "content_theme": "内容主题",
    "story_angle": "叙事切入角度",
    "audience_tension": "受众此刻的真实纠结",
    "emotion_path": ["情绪路径，按先后顺序"],
    "selling_point_order": ["卖点排序，按呈现先后"],
    "video_structure": ["内容结构，按段落顺序"]
  },

  "persona_card": {
    "speaker_identity": "谁来说：身份与立场",
    "voice_traits": ["说话特征"],
    "audience_relationship": "与受众的关系",
    "belief_expression": "这个人相信什么、如何表达这种相信",
    "forbidden_styles": ["这个人设绝对不会用的表达方式"]
  },

  "video_script": {
    "target_duration_seconds": 0,
    "segments": [
      {
        "segment_id": "S1",
        "start_second": 0,
        "end_second": 0,
        "visual": "这一段画面是什么",
        "spoken_text": "这一段口播原文",
        "product_refs": ["这一段出现的商品标识：写企业事实中该商品的 product_id 原值"],
        "emotion": "这一段的情绪"
      }
    ]
  },

  "storyboard": {
    "shots": [
      {
        "shot_id": "SH1",
        "script_segment_ref": "对应的脚本 segment_id",
        "purpose": "这个镜头要达成什么",
        "scene": "场景",
        "subject": "人物/主体",
        "product_focus": "商品重点",
        "action": "动作与调度",
        "framing": "景别与取景",
        "shooting_notes": "现场注意事项"
      }
    ]
  },

  "voice_package": {
    "full_voiceover": "完整口播全文，可直接照读",
    "voice_traits": ["声音特征"],
    "pace": "整体语速与节奏说明",
    "cues": [
      {
        "position": "在口播全文中的位置（引用该处原文片段）",
        "cue_type": "PAUSE | EMPHASIZE | SLOW_DOWN | SPEED_UP",
        "note": "为什么在这里这样处理"
      }
    ]
  },

  "audio_direction": {
    "mood": "情绪基调",
    "tempo": "节奏",
    "usage_phases": ["在视频哪些阶段如何使用"],
    "avoidance": ["要避免的音乐类型或用法"]
  },

  "product_placement": {
    "placements": [
      {
        "product_ref": "商品标识：逐字写企业事实商品池中该商品的 product_id 原值",
        "script_or_shot_ref": "对应的脚本段或镜头 ID",
        "timing": "出现时点",
        "purpose": "为什么在这里出现",
        "display_focus": "展示重点",
        "constraints": "展示约束（不得展示什么、不得声称什么）"
      }
    ]
  },

  "comment_operation_package": {
    "pinned_comment": "置顶评论原文",
    "faq_items": [
      {
        "question": "受众大概率会问的问题",
        "answer": "回答原文"
      }
    ],
    "official_responses": [
      {
        "scenario": "什么情形下使用",
        "response": "官方回应原文"
      }
    ],
    "prohibited_claim_refs": ["评论区绝对不能说的陈述所对应的硬规则标识：逐字写该条规则的 rule_id 原值，并写出其 version 版本号"]
  },

  "production_risks": ["制作与发布环节的风险，逐条列出"],

  "assumptions": [
    {
      "assumption_id": "AS-1",
      "statement": "采用了什么工作假设",
      "missing_input": "因为缺了什么资料才需要这个假设",
      "impact_if_wrong": "假设不成立会影响哪一部分"
    }
  ],

  "confidence": {
    "level": "HIGH | MEDIUM | LOW",
    "basis": ["整份交付包的置信依据"],
    "limiting_factors": ["削弱置信度的因素"]
  }
}
```

### 九部分的人工可用标准（每一部分都要达到）

| 部分 | 达标标准 |
|---|---|
| `content_brief` | 审核者能一句话判断“为什么做、对谁说、说什么” |
| `creative_strategy` | 能看出如何承接已选商业策略 |
| `persona_card` | 口播、画面和评论回复能保持一致人格 |
| `video_script` | 可用于拍摄准备，而非纯文案 |
| `storyboard` | 摄影人员知道每个镜头的执行目的 |
| `voice_package` | 出镜者可据此录制 |
| `audio_direction` | 能指导选乐，不要求系统生成音乐 |
| `product_placement` | 商品露出服务内容和商业目标 |
| `comment_operation_package` | 发布后可以直接用于基础互动 |

### 自检（输出前逐条确认）

- [ ] 九个顶层部分全部存在，且关键字段都不为空？
- [ ] `selected_candidate_id` 与输入中的已选候选完全一致，九个部分都在服务这一条候选？
- [ ] 每个数字（价格、库存、尺码、时长、时点）都能在企业事实或本脚本内部找到依据？
- [ ] 所有材质、价格、库存、功效性陈述都引用了企业事实中的确认事实？
- [ ] 视觉建议没有依赖企业事实里没有图片来源支撑的细节？
- [ ] 每个镜头都挂到了某个脚本 segment，脚本关键段落都有镜头？
- [ ] 商品露出项只引用了企业事实商品池里的商品？
- [ ] 人设卡的 `forbidden_styles` 在口播和评论回复里没有被违反？
- [ ] 所有硬规则逐条对照过，没有触线表达？
- [ ] 所有假设都写进 `assumptions` 而不是混进确定陈述？
- [ ] 所有商品引用写的是企业事实中的 `product_id` 原值，受众引用写的是 `audience_id`，规则引用带上了 `rule_id` 与 `version`？
- [ ] 没有任何百分比评分、爆款概率或销量保证？
- [ ] 全文为中文（简体），除字段名与枚举值外没有中英混排？
- [ ] `</thinking>` 之后的输出是且只是一个合法 JSON 对象？

<<<PROMPT_END>>>

---

## 4. 运行约束（runner 侧，非 Prompt 内容）

- 阶段 C 只允许 **1 次**受控直接调用（B.2.4）；调用次数、Token、成本、延迟按 B.2.2 记录。
- 不允许基线侧使用未声明的搜索或知识库（B.2.2）。
- `{{selected_candidate}}` 必须是**已冻结**的匿名裁判选择结果（B.2.3：选择、理由和时间冻结后才进入下一阶段）。
- 两阶段结果合并为同一 `E2EComparisonEnvelope` 后再做最终匿名裁判（B.2.3）。Envelope 由 runner 组装，**不由基线模型输出**：
  `decision_output_ref` / `frozen_selection_ref` / `creative_package_ref` / `selected_candidate_id` / `package_section_count: 9` / `output_contract_version`。
- 匿名处理按 B.2.5 执行（随机 X / Y 标签、相同外层展示格式、随机排列、揭晓前冻结裁判原始选择）；匿名处理不得修改业务内容。
- **`<thinking>` 块的处置（草案提案，PENDING_IA0，OQ-BASELINE-06）**：模型可选输出的 `<thinking>…</thinking>` 块由 runner 在**进入 B.2.5 匿名处理之前整块剥离**，剥离后的 JSON 才是参与比较与判分的输出；`<thinking>` 块不得进入 `E2EComparisonEnvelope`。剥离范围与「该块不属 B.2.5『匿名处理不得修改业务内容』所指的业务内容」这一认定，须写入 `anonymity_procedure.md` 并两侧同规则；Founder 未在 IA-0 裁决前，本条不得视为已生效。
- **失败处置（草案提案，PENDING_IA0，OQ-BASELINE-07）**：基线侧出现 `FORMAT_INVALID` / `SCHEMA_INVALID`、输出被 `max_tokens` 截断或调用超时时，默认口径为**零重试**——B.2.4 明文「阶段 D 和阶段 C 各允许一次受控直接调用；除此之外不得增加隐藏迭代」：该次调用照实记录（次数、Token、成本、延迟按 B.2.2），该侧本案例记 FAILED，不得由 runner 私下追加任何重试。笛语侧 PRE-03-M 的有界重试（B:244）自身限定「当前里程碑模块」，不适用于基线侧。若 Founder 认为基线侧应享有对称重试预算，**那等于修改 B.2.4 考试条件，必须走 B.8.1 版本升级 + 双侧重跑**，不能由本文件自行约定——是否立项，见 OQ-BASELINE-07。与阶段 D §4 同一条规则，两阶段不得各行其是。

## 5. 字段来源对照表（可审计溯源）

| 输出字段 | 真源 | 性质 |
|---|---|---|
| 九部分顶层结构（`content_brief` … `comment_operation_package`） | B.2.3 「同一九部分制作包 Schema」；部分名与最小内容来自 PRD 7.2；最小必填字段来自 A.8 | 冻结要求 |
| `content_brief` 子字段 | A.8：`business_goal, audience_refs, core_proposition, product_refs, non_negotiable_fact_refs, rule_refs`（已剔除 `decision_selection_ref` / `decision_bundle_ref`——属笛语内部 VersionedRef，B.2.3 不要求基线伪造） | **PENDING_IA0**（OQ-BASELINE-12）：外部可见子集需确认 |
| `creative_strategy` 子字段 | A.8 逐字 | 冻结要求 |
| `persona_card` 子字段 | A.8（已剔除 `persona_ref`——内部 VersionedRef；A.3.5 `persona_id` 未在本外部 Schema 出现） | **PENDING_IA0**（OQ-BASELINE-12） |
| `video_script` 子字段 | A.8（已剔除段内 `trace_refs`——内部） | 冻结要求 |
| `storyboard` 子字段 | A.8 逐字 | 冻结要求 |
| `voice_package` 子字段 | A.8（A:757 VoicePackage）：`full_voiceover, voice_traits[], pace, cues[]`；Cue 枚举 `PAUSE / EMPHASIZE / SLOW_DOWN / SPEED_UP` 逐字来自 A.8。**PRD 7.2（PRD:609）为 Voice Package 明列的最小内容是「完整口播、停顿、强调、语速和情绪」，其中「情绪」在 A.8 VoicePackage 中无对应字段**——本文件按 A.8 起草、未自造字段，差异不静默丢弃，登记为待裁 | Cue 条目内 `position` / `note` 为 **PENDING_IA0**（OQ-BASELINE-13，A.8 未展开 Cue 内部字段）；「情绪」是否补入为 **PENDING_IA0**（OQ-BASELINE-11） |
| `audio_direction` 子字段 | A.8 逐字 | 冻结要求 |
| `product_placement` 子字段 | A.8 逐字 | 冻结要求 |
| `comment_operation_package` 子字段 | A.8：`pinned_comment, faq_items[], official_responses[], prohibited_claim_refs[]` | `faq_items` / `official_responses` 条目内部字段为 **PENDING_IA0**（OQ-BASELINE-13，A.8 未展开） |
| `selected_candidate_id` | B.2.3 E2EComparisonEnvelope 明列；PRD 7.3 第 3 条「明确引用已选商业候选」 | 冻结要求 |
| `production_risks` | B.2.3 明列；A.7.2 同名字段 | 冻结要求 |
| `assumptions` | B.2.3 明列；「显式标记假设与不确定性」来自 PRD 7.3 第 6 条 / A.1.4 | 条目内部字段（`assumption_id` / `missing_input` / `impact_if_wrong`）为 **PENDING_IA0**（OQ-BASELINE-13，B / A 未为外部展示合同展开） |
| `confidence` | B.2.3 明列；结构逐字来自 A.2.5 ConfidenceStatement | 冻结要求 |
| 全部引用字段的书写形式（`audience_refs` / `product_refs` / `non_negotiable_fact_refs` / `rule_refs` / `prohibited_claim_refs` / 段内 `product_refs` / `placements[].product_ref`） | 商品用 A.3.2 `product_id`；受众用 A.3.4 `audience_id`；硬规则用 A.9.1 `rule_id` + `version`。**事实条目标识：B 与 A 均未为外部展示合同规定其形式**，本文件只要求「照抄企业事实中的原有标识、不得另造」。人物引用：A.8 PersonaCard 的 `persona_ref` 已按 B.2.3 剔除，故本外部 Schema 无 `persona_id` 落点；若共同输出合同后续补入，必须用 A.3.5 `persona_id` | **PENDING_IA0**（OQ-BASELINE-05）：事实引用书写形式随共同输出合同定稿；两侧写法一致是 B.2.5「相同外层展示格式」的前置 |
| 输出语言 = 中文（简体） | **B 未规定输出语言**；本文件按 B.2.5「使用相同外层展示格式」取两侧同一语言口径，避免语言或中英混排差异构成来源指纹 | **PENDING_IA0**（OQ-BASELINE-09）：须确认笛语侧同为中文（简体），且与阶段 D 同口径 |
| `<thinking>` 块（不进入输出合同） | **B 未规定**；本文件按 B.2.4「不得故意写弱」补足草稿空间（对照 B:181 笛语侧可多模块多次调用把推理外化） | **PENDING_IA0**（OQ-BASELINE-06）：方案与剥离口径由 Founder 在 IA-0 裁决 |
| 多模态输入通道（§2 表下声明） | B.2.2（B:172）「相同商品图片和其他输入材料」；与阶段 D §2 同源同句 | **PENDING_IA0**（OQ-BASELINE-10）：阶段 C、阶段 D 与笛语侧三方通道一致性须核验 |
| 输出纪律第 1–7 条 | A.8「一致性约束」1–7 + PRD 7.3 完整性与可用性 1–7 | 属"相同最终输出合同"，两侧同发（B.2.4） |
| 九部分人工可用标准表 | PRD 7.2「人工可用标准」列逐字 | 冻结要求 |

**已刻意不要求基线输出的字段**（A.7.2 / A.8 有、但属笛语内部）：`artifact` / `ArtifactEnvelope`、`parent_references`、`decision_selection_ref`、`decision_bundle_ref`、`context_snapshot_ref`、`package_artifact_refs`、`validation`（笛语侧自校验四态）、`trace_bundle`、`MarkdownExportManifest`。理由：B.2.3「不要求基线伪造笛语内部 Run、Artifact 或 Trace ID」+「不能增加只对一侧可见的业务内容」。

## 6. 冻结前待办（PENDING_IA0）

> 每条编号 `OQ-BASELINE-xx` 供中央待裁清单汇编引用；本文件不自建登记文件。

1. 九部分各自的**外部可见子字段集**定稿（内部 VersionedRef 一律剔除，两侧显示口径必须一致）。（OQ-BASELINE-12）
2. `voice_package.cues[]`、`comment_operation_package.faq_items[]` / `official_responses[]`、`assumptions[]` 的条目内部字段定稿。（OQ-BASELINE-13）
3. `target_duration_seconds` 是否由案例统一给定（写进 `{{task_statement}}` 或硬规则），还是由模型自定——影响两侧可比性。（OQ-BASELINE-14）
4. `voice_package` 是否补入 PRD 7.2 明列而 A.8 未展开的「情绪」字段——补则两侧同补并写进共同输出合同，不补则明确记为 PRD 与 A 之间的既有差异。（OQ-BASELINE-11）
5. 阶段 C 多模态输入通道与阶段 D、笛语侧三方一致性核验（同一通道、同一批材料、同一顺序）。（OQ-BASELINE-10）
6. 全部引用字段的书写形式定稿——事实条目标识尤其未定；两侧写法一致是 B.2.5「相同外层展示格式」的前置。（OQ-BASELINE-05）
7. `<thinking>` 块方案由 Founder 在 IA-0 裁决：本文件已按「允许 `<thinking>` 块、runner 在匿名化前整块剥离」起草，剥离范围与「不属 B.2.5 业务内容」的认定须写入 `anonymity_procedure.md`，两侧同规则。（OQ-BASELINE-06）
8. 基线侧 `FORMAT_INVALID` / 截断 / 超时的处置规则（§4 已给对称提案）由 Founder 裁决，两侧同规则并写入 Case Manifest。（OQ-BASELINE-07）
9. 与 `anonymity_procedure.md` 的衔接确认：阶段 D 输出 → B.2.5 匿名（X / Y）→ 选择冻结 → 回流为本阶段 `{{selected_candidate}}`；衔接口径以 `anonymity_procedure.md` 自身声明为准，本文件不复述。（OQ-BASELINE-08）
10. 输出语言口径确认：本文件写死中文（简体），须确认笛语侧与阶段 D 同口径。（OQ-BASELINE-09）
11. `output_contract_version` 取值，写入 Case Manifest 的 `e2e_output_contract_version` / `e2e_interaction_contract_version`（B.2.1）——与阶段 D §6 同一项，两阶段必须同值。（OQ-BASELINE-15）
12. 模型供应商、模型版本、生成参数、allowed_tools 定格并写入 Case Manifest（OD-02 厂商组合已裁决（台账 08-17），版本 / 参数于 IA-0 定格——本项指后者，见《裁决台账》）。
13. Founder 签字，状态由 `PENDING_IA0` 改为 `FROZEN`，版本由 `v0.1-draft` 升为 `v1.0`。
