> **状态：v1.0 FROZEN（Founder 2026-08-17 IA-0 签字批次生效；正文中残留的 v0.1-draft / PENDING_IA0 冻结待办字样自本行起读作已随本批次冻结定格）**

# 共同输出合同 ｜ e2e_output_contract

| 项目 | 内容 |
|---|---|
| 文件 ID | DIYU-CONTRACT-INTERACTION-E2E-OUTPUT |
| 文件 | `contracts/interaction/e2e_output_contract.md` |
| 版本 | **v0.1-draft** |
| 状态 | **PENDING_IA0 冻结**（未冻结、未生效，不得用于正式 A/B 取证） |
| 真源 | `B_三个核心模块智能验收合同.md` v0.3（EFFECTIVE）：B.2.3、B.2.5、B.8；`A_模块接口与核心数据字典.md` v0.2（EFFECTIVE）：A.1.2、A.2.5、A.2.6、A.3.2、A.3.4、A.3.5、A.6.2、A.6.3、A.7.2、A.8、A.9.1；`PRD_笛语智能核_MVP_V3.0_v0.1.md` 7.2 / 7.3 |
| 本文件是什么 | Gate IA-0（B:992）三件套的**第 ② 件**：两阶段共同**输出**合同——两侧共用的**外部展示 Schema** 逐项定义（阶段 D + 阶段 C），以及引用书写形式、剔除清单、Envelope 取值来源 |
| 本文件不是什么 | 不是笛语侧内部对象定义（那是 A.6.2 / A.6.3 / A.7.2 / A.8）、不是任一侧 Prompt、不定义交互时序（那是 `e2e_interaction_contract.md`）。**只引用真源编号，不复述其定义**；与真源冲突处一律以真源原文为准 |
| 适用范围 | 与 `e2e_interaction_contract.md` 同：B.5.1 三个锁定端到端匿名 A/B 场景（E2E-01 / E2E-02 / E2E-03） |
| 变更纪律 | 本文件位于 `contracts/`（考试条件区）：改动 = 改考试条件，需版本升级 + Founder 签字 + A/B 双侧回归重跑（`contracts/README.md`、B.9） |
| 写入 Case Manifest | `e2e_output_contract_version`（B.2.1，B:147）；同一取值同时作为 `E2EComparisonEnvelope.output_contract_version`（B:200）。与 `e2e_interaction_contract_version` 同批定格、两阶段同值（OQ-BASELINE-15） |
| 起草依据 | B.2.3 阶段 D 逐项（B:187）、阶段 C 逐项（B:191）；PRD 7.2 九部分（PRD:600-614）；A.8 最小必填字段（A:751-761）；`acceptance/cases/OPEN_QUESTIONS.md` 文首「预裁决」（Founder 2026-08-17，《裁决台账》08-17 行） |

---

## 0. 通用口径（两阶段共用）

| 项 | 口径 | 依据 |
|---|---|---|
| 输出体裁 | 除可选 `<thinking>` 块外只输出**一个 JSON 对象**；不得有前言、解释或 Markdown 代码围栏 | B:224；`e2e_interaction_contract.md` §5 第 5 行 |
| 输出语言 | **中文（简体）**；字段名与枚举值保持英文原样，其余取值一律中文，不得中英混排 | **预裁决**（OQ-BASELINE-09）；B:224 |
| 字段名 | 必须逐字一致，两侧同名；笛语侧内部对象转换为本 Schema 后不得改名、不得增删 | B:187 末句「不能增加只对一侧可见的业务内容」 |
| 置信度 | 三级 `HIGH / MEDIUM / LOW`，结构逐字用 A.2.5 `ConfidenceStatement`（`level` / `basis[]` / `limiting_factors[]`）；不得输出百分比、评分或综合总分 | A.2.5（A:186-194）；B.1.2 |
| 四类依据 | `FACT / RULE / ASSUMPTION / MODEL_JUDGMENT` 必须可区分、不得混写；定义见 A.1.2（A:65-72），枚举见 A.2.6 `TraceType`（A:206） | B:187；A.1.2 |
| 不伪造内部标识 | 不要求任一侧输出笛语内部 Run / Artifact / Trace ID；剔除清单见 §4 | B:203 |

---

## 1. 引用书写形式（两侧唯一写法）

**预裁决**：引用一律使用 A 的既有 id 字段原值，不得另造编号、不得使用 `VersionedRef` 等内部引用对象（OQ-BASELINE-05，✅预裁决 08-17）。

| 被引对象 | 写法 | A 真源 | 备注 |
|---|---|---|---|
| 商品 | `product_id` 原值 | A.3.2（A:249） | A.6.3 / A.8 中原为 `VersionedRef` 的商品引用，一律降级为该原值（依据 B:203） |
| 受众 | `audience_id` 原值 | A.3.4（A:304） | 同上 |
| 人物（Persona） | `persona_id` 原值 | A.3.5（A:323） | A.8 PersonaCard 的 `persona_ref: VersionedRef` 按同一降级规则写为该原值（见 §3.3 的落点说明） |
| 硬规则 | `rule_id` 原值 **+ `version` 版本号** | A.9.1（A:818、A:820） | 两者缺一不可；A.1.2 RULE 行要求「必须引用规则版本」（A:68） |
| 事实条目 | **照抄快照中该条事实的原有标识 / 键名路径，不得另造编号** | B 与 A 均未为外部展示合同规定其形式 | 本仓当前夹具中事实以 `facts` 下键名承载（`acceptance/cases/BD-D01/fixtures/context_snapshot.json`，如 `facts.inventory` / `facts.product`），故引用照抄该键名路径。**该具体书写形式随 IA-0 定格**（OQ-BASELINE-05 数值层）——两侧写法一致是 B:224「相同外层展示格式」的前置 |
| 已选候选 | 阶段 D 输出中的 `candidate_id` 原值 | B:198 `selected_candidate_id` | 阶段 C 必须与输入的被选候选完全一致 |

---

## 2. 阶段 D｜商业候选 外部展示 Schema（按 B:187 逐项）

顶层字段 **9 项**，逐项对应 B.2.3 阶段 D 明列内容（B:187）。

| # | 字段 | B:187 明列 | 结构 | 真源 / 裁决 |
|---|---|---|---|---|
| 1 | `business_problem` | 是 | `string` | B:187 明列 |
| 2 | `recognized_conflicts` | 是 | `[{conflict_id, description, side_a, side_b}]` | 子字段逐字来自 A.6.2（A:591-595），已剔除 `trace_refs` |
| 3 | `candidate_options` | 是（**目标三个、最低两个**） | `[BusinessCandidate 外部可见子集]`，逐项见 §2.1 | B:187；数量约束见 A.6.3 约束首条（A:661） |
| 4 | `candidate_count_status` | 是 | `TARGET_THREE \| DEGRADED_TWO \| BLOCKED_FEWER_THAN_TWO` | 枚举逐字来自 A.6.2（A:603） |
| 5 | `candidate_count_explanation` | 是 | `string \| null` | A.6.2（A:604）；三态填写要求见 §2.2 |
| 6 | `comparative_tradeoffs` | 是 | `[{candidate_refs[], tradeoff}]` | 子字段来自 A.6.2（A:600-601），已剔除 `trace_refs` |
| 7 | **`risks`（顶层）** | 是 | `[{condition, possible_impact, mitigation}]` | **B:187 逐项明列 `risks`；A.6.2 BusinessDecisionBundle 无顶层 risks**——顶层容器在 A 中无对应对象，由本合同据 B 设立。子字段沿用 A.6.3 `risks[]`（A:648-651），已剔除 `trace_refs`。分工见 §2.3（**预裁决**，OQ-BASELINE-04） |
| 8 | `basis_entries`（四类依据区分的承载字段） | 是（B:187「FACT / RULE / ASSUMPTION / MODEL_JUDGMENT 区分」） | `[{basis_id, basis_type, statement, source}]` | **B 与 A 均未为外部展示合同命名该容器**（A.9.2 `TraceBundle` 属笛语内部）。本合同取名 `basis_entries`（**预裁决**，OQ-BASELINE-01），与 `baseline_prompt_stage_D.md` §4 同名；`basis_type` 枚举 = A.2.6 `TraceType`（A:206） |
| 9 | `confidence` | 是 | `ConfidenceStatement`（A.2.5） | B:187 明列 |

### 2.1 `candidate_options[]` 外部可见子集

来源 = A.6.3 `BusinessCandidate`（A:619-656）的外部可见子集（**预裁决**，OQ-BASELINE-02）：

| 子字段 | 结构 | 说明 |
|---|---|---|
| `candidate_id` | `string` | A.6.3（A:620） |
| `title` | `string` | A.6.3（A:621） |
| `strategy` | `string` | A.6.3（A:622） |
| `product_roles[]` | `{product_ref, role, rationale}` | A.6.3（A:623-626）；`product_ref` 按 §1 写 `product_id` 原值（A.6.3 原为 `VersionedRef`，依 B:203 降级，OQ-BASELINE-03）；`role` 枚举 = A.2.6 `ProductRole`（A:205）；已剔除条目内 `trace_refs` |
| `supporting_fact_refs[]` | `string[]` | A.6.3（A:628）；写法按 §1 事实条目行 |
| `applied_rule_refs[]` | `string[]` | A.6.3（A:629）；写法按 §1 硬规则行（`rule_id` + `version`） |
| `assumption_refs[]` | `string[]` | A.6.3（A:630）；每个标识必须在 `basis_entries` 中有对应条目 |
| `model_judgment_refs[]` | `string[]` | A.6.3（A:631）；同上 |
| `brand_fit` / `audience_fit` / `business_alignment` / `production_feasibility` | `{assessment, rationale}` | A.6.3（A:632-647）；`assessment` 枚举 = A.2.6 `AlignmentAssessment`（A:207）；**只做定性判断，不计算加权总分**（A.6.3 约束 A:666）；已剔除 `trace_refs` |
| **`risks[]`（候选级，保留）** | `{condition, possible_impact, mitigation}` | **对应 A.6.3 `risks[]`（A:648-651）**；`mitigation` 无有效缓解手段时为 `null`；已剔除 `trace_refs`。与顶层 `risks` 的分工见 §2.3 |
| `why_this_option` | `string` | A.6.3（A:653） |
| `why_not_primary_alternative` | `string` | A.6.3（A:654） |
| `confidence` | `ConfidenceStatement` | A.6.3（A:656） |

### 2.2 候选数量与状态的对应（A.6.3 约束，A:661-668）

- 目标 **3 个**、最低 **2 个**（B:187 明列「目标三个且最低两个」）；
- 3 个有效候选 → `TARGET_THREE`，`candidate_count_explanation` 可为 `null`；
- 只能形成 2 个 → `DEGRADED_TWO`，必须说明受哪些事实、规则或实质差异限制；
- 不足 2 个 → `BLOCKED_FEWER_THAN_TWO`，必须说明阻断原因，**不补造候选**（A:665）；
- 候选差异必须落在商业机制、商品角色、叙事路径或风险取舍；不得以标题、Hook 或形容词变化凑数（A:663-664）；
- 不输出爆款概率、销量保证或因果承诺（A:668）。

### 2.3 顶层 `risks` 与候选级 `risks` 的分工（预裁决，OQ-BASELINE-04）

| 容器 | 装什么 |
|---|---|
| 顶层 `risks` | **整份输出层面**的风险：不论最终选哪个候选都要面对的风险，或候选之间共有的风险 |
| `candidate_options[].risks` | **只属于该条候选**的风险：换一条候选就不存在或性质不同的风险 |

同一条风险不得在两处重复照抄；两处内容不得互相矛盾。**两处都必须填写**（顶层依 B:187 明列，候选级依 A.6.3）。该分工必须与笛语侧「内部对象 → 外部展示 Schema」转换器**一次性定死**——转换器落点尚不存在（`contracts/interaction/README.md` §4 第四行），故本项在冻结前仍带 **PENDING_IA0** 标记。

---

## 3. 阶段 C｜制作交付包 外部展示 Schema（九部分逐项）

顶层字段 = `selected_candidate_id` + **九部分** + `production_risks` + `assumptions` + `confidence`（B:191 明列「同一九部分制作包 Schema、production_risks、assumptions 与 confidence」）。

| 顶层字段 | 结构 | 真源 |
|---|---|---|
| `selected_candidate_id` | `string`，必须与输入的被选候选 `candidate_id` 完全一致 | B:198（Envelope 明列）；PRD 7.3 第 3 条「明确引用已选商业候选」（PRD:622） |
| 九部分（§3.1-§3.9） | 见下 | B:191；部分名与最小内容 PRD 7.2（PRD:602-612）；最小必填字段 A.8（A:751-761） |
| `production_risks` | `string[]` | B:191 明列；A.7.2 同名字段（A:731） |
| `assumptions` | `[{assumption_id, statement, missing_input, impact_if_wrong}]` | B:191 明列；「假设和不确定性必须被显式标记」PRD 7.3 第 6 条（PRD:625）+ A.1.4。**条目内部字段 B / A 均未为外部展示合同展开** → PENDING_IA0（OQ-BASELINE-13） |
| `confidence` | `ConfidenceStatement`（A.2.5） | B:191 明列 |

九部分**全部存在**是硬要求（PRD 7.3 第 1 条，PRD:620；`package_section_count: 9`，B:199）。每部分的「人工可用标准」逐条见 PRD 7.2（PRD:602-612），本文件不复述。

### 3.1 `content_brief`（ContentBrief）

| 子字段 | 结构 | 说明 |
|---|---|---|
| `business_goal` | `string` | A.8（A:753） |
| `audience_refs[]` | `string[]` | 按 §1 写 `audience_id` 原值 |
| `core_proposition` | `string` | A.8（A:753） |
| `product_refs[]` | `string[]` | 按 §1 写 `product_id` 原值 |
| `non_negotiable_fact_refs[]` | `string[]` | 按 §1 事实条目行 |
| `rule_refs[]` | `string[]` | 按 §1 写 `rule_id` + `version` |

已剔除 A.8 的 `decision_selection_ref` / `decision_bundle_ref`（内部 `VersionedRef`，B:203）；两者承载的「承接哪次人工选择」由顶层 `selected_candidate_id` 与 Envelope（§5）承担。

### 3.2 `creative_strategy`（CreativeStrategy）

`content_theme`、`story_angle`、`audience_tension`、`emotion_path[]`、`selling_point_order[]`、`video_structure[]` —— 逐字取 A.8（A:754）。

### 3.3 `persona_card`（PersonaCard）

`speaker_identity`、`voice_traits[]`、`audience_relationship`、`belief_expression`、`forbidden_styles[]` —— 取 A.8（A:755）。

**`persona_ref` 的落点**：A.8 PersonaCard 首个必填字段是 `persona_ref: VersionedRef`。按 §1 的降级规则（与 `product_ref` 同规则、依 B:203），本合同将其写为 **A.3.5 `persona_id` 原值**。
**两侧口径已拉齐（本批消除）**：`baseline_prompt_stage_C.md` 已按同一降级规则在 `persona_card` 内补入 `persona_ref`（写 A.3.5 `persona_id` 原值），其 §5 `persona_card` 行与「引用书写形式」行、§6 第 1 条同批同步。理由：B:203 只豁免「伪造笛语内部 Run / Artifact / Trace ID」，`persona_id` 是**业务标识**、不是内部追踪 ID，故与 `product_ref` 同规则降级保留而非剔除。（OQ-BASELINE-12 / OQ-BASELINE-05：本项**落点已定**，仅随外部可见子集整体定稿同批升版）

### 3.4 `video_script`（VideoScript）

| 子字段 | 结构 | 说明 |
|---|---|---|
| `target_duration_seconds` | `number` | A.8（A:756）。**由案例统一给定还是由模型自定，尚未定** → PENDING_IA0（OQ-BASELINE-14）；两侧口径必须相同才可比 |
| `segments[]` | `{segment_id, start_second, end_second, visual, spoken_text, product_refs[], emotion}` | A.8（A:756）；`product_refs` 按 §1 写 `product_id` 原值；已剔除段内 `trace_refs`（内部）。**`segment_id`：A:756 未列该字段**，为承接 §3.5 Storyboard 的 `script_segment_ref` 由**本合同设立**（与 §2 第 7 行顶层 `risks`、第 8 行 `basis_entries` 同类处理：A 中无对应落点、据 B / 承接需要设立），**两侧同用**；具体书写形式随 §7 第 8 条一并定稿（OQ-BASELINE-13） |

### 3.5 `storyboard`（Storyboard）

`shots[]`，每镜含 `shot_id`、`script_segment_ref`、`purpose`、`scene`、`subject`、`product_focus`、`action`、`framing`、`shooting_notes` —— 逐字取 A.8（A:757）。`script_segment_ref` 指向本包内 `video_script.segments[].segment_id`。

### 3.6 `voice_package`（VoicePackage）

| 子字段 | 结构 | 说明 |
|---|---|---|
| `full_voiceover` | `string` | A.8（A:758） |
| `voice_traits[]` | `string[]` | A.8（A:758） |
| `pace` | `string` | A.8（A:758） |
| **`emotion`（情绪）** | `string` | **A v0.2 已补入**（A:758；A.0 修订记录 A:11：Founder 2026-08-17 裁决补该字段，对齐 PRD 7.2 Voice Package 最小内容 PRD:609）。**预裁决⑦** |
| `cues[]` | `{position, cue_type, note}`；`cue_type ∈ PAUSE \| EMPHASIZE \| SLOW_DOWN \| SPEED_UP` | 枚举逐字来自 A.8（A:758）。**条目内部字段 A.8 未展开** → PENDING_IA0（OQ-BASELINE-13） |

**两侧口径已拉齐（本批消除）**：`baseline_prompt_stage_C.md` 已在 `voice_package` 内补入 `emotion`（`"emotion": "整体情绪基调"`，位置在 `pace` 之后），其 §5 该行改引 A:758 并标「A v0.2 已补入（预裁决⑦）」、§6 第 4 条改为已定。原「A.8 无对应字段」的记述基于 A v0.1，已被 A v0.2（A:758）与预裁决⑦推翻，不再出现于任一文件。（OQ-BASELINE-11：**已定**，仅待同批升版）

### 3.7 `audio_direction`（AudioDirection）

`mood`、`tempo`、`usage_phases[]`、`avoidance[]` —— 逐字取 A.8（A:759）。

### 3.8 `product_placement`（ProductPlacement）

`placements[]`，每项含 `product_ref`、`script_or_shot_ref`、`timing`、`purpose`、`display_focus`、`constraints` —— 逐字取 A.8（A:760）；`product_ref` 按 §1 写 `product_id` 原值，且**只能引用当前商品池**（A.8 一致性约束第 4 条，A:768）。

### 3.9 `comment_operation_package`（CommentOperationPackage）— **PRD 7.2 第九项**

| 子字段 | 结构 | 说明 |
|---|---|---|
| `pinned_comment` | `string` | A.8（A:761）；PRD 7.2 最小内容「置顶评论」 |
| `faq_items[]` | `[{question, answer}]` | A.8（A:761）；PRD 7.2「常见问题」。**条目内部字段 A.8 未展开** → PENDING_IA0（OQ-BASELINE-13） |
| `official_responses[]` | `[{scenario, response}]` | A.8（A:761）；PRD 7.2「官方回应」。同上 → PENDING_IA0（OQ-BASELINE-13） |
| `prohibited_claim_refs[]` | `string[]` | A.8（A:761）；按 §1 写 `rule_id` + `version` |

> 该部分是 PRD 7.2 九部分中的第九项，**不得因「发布后运营」性质被省略**：九个顶层部分全部存在是 PRD 7.3 第 1 条硬要求，`package_section_count: 9`（B:199）据此计数。

### 3.10 一致性与完整性约束（不复述，只给坐标）

两侧同发、同判：A.8「一致性约束」8 条（A:765-772）+ PRD 7.3 完整性与可用性 7 条（PRD:620-626）。硬规则校验属确定性校验（PRD 8.1 / SYS-03），违反者不得进入下一人工审核节点。

---

## 4. 剔除清单（两侧展示口径一致，不得任一侧保留）

依据 B:203「不要求基线伪造笛语内部 Run、Artifact 或 Trace ID」+ B:187 末句「不能增加只对一侧可见的业务内容」。笛语侧转换器必须剔除以下字段后再进入外部展示与判分。

| 阶段 | 剔除字段 | 内部真源 |
|---|---|---|
| D | `artifact`（ArtifactEnvelope）、`system_recommendation`、`human_selection_required`、`blocked_candidate_diagnostics`、`trace_bundle` | A.6.2（A:589、A:605-613） |
| D | 候选内 `hard_rule_results`；`product_roles[]` / 四个适配维度 / `risks[]` / `recognized_conflicts[]` / `comparative_tradeoffs[]` 各处的 `trace_refs` | A.6.3（A:627、A:635-652、A:655）、A.6.2（A:596、A:602） |
| C | `artifact`（ArtifactEnvelope）、`parent_references`、`decision_selection_ref`、`decision_bundle_ref`、`context_snapshot_ref`、`package_artifact_refs`、`validation`（笛语侧自校验四态）、`trace_bundle` | A.7.2（A:707-738）、A.8（A:749 每项资产的 ArtifactEnvelope 与 parent_references、A:753 ContentBrief 两个内部 ref） |
| C | `video_script.segments[].trace_refs` | A.8（A:756） |
| C | `MarkdownExportManifest` 全对象 | A.8（A:793-806）；属批准后导出，不属两侧比较面 |

**不在剔除清单内**：A.8 PersonaCard 的 `persona_ref`（A:755）**不剔除**——按 §1 与 `product_ref` 同一降级规则写 A.3.5 `persona_id` 原值（B:203 只豁免伪造笛语内部 Run / Artifact / Trace ID，`persona_id` 是业务标识），两侧同写，详见 §3.3。

剔除不等于取消：这些对象在笛语侧仍按 A / PRD 保留并受 SYS-04 等条款约束，只是**不进入两侧可比较的外部展示面**。

---

## 5. `E2EComparisonEnvelope` 取值来源（B:194-200）

Envelope 由 runner 组装，**不由任一侧模型输出**（`e2e_interaction_contract.md` §6）。

| 字段 | 取值来源 |
|---|---|
| `decision_output_ref` | 该侧阶段 D 输出（已剥离 `<thinking>`、已按 §2 校验）的留档引用 |
| `frozen_selection_ref` | 阶段 D 冻结点一的选择冻结记录（含选择、理由、时间）——留档字段以 `anonymity_procedure.md` §3 / §7 为准 |
| `creative_package_ref` | 该侧阶段 C 输出（已剥离 `<thinking>`、已按 §3 校验）的留档引用 |
| `selected_candidate_id` | 与该侧阶段 C 输出的 `selected_candidate_id` 一致，且必须存在于该侧阶段 D 的 `candidate_options` |
| `package_section_count` | 常量 `9`（B:199）；与 §3 九部分实际存在数一致，缺一即不得写 9 |
| `output_contract_version` | 本文件冻结后的版本号（= Case Manifest `e2e_output_contract_version`） |

> 三个 `*_ref` 的**命名规范与目录结构 B 未规定** → PENDING_IA0（`anonymity_procedure.md` §8 P-06 / OQ-ANON-06），本文件不自拟。

---

## 6. 版本口径

- 本文件当前 **v0.1-draft / PENDING_IA0**，**不得用于正式 A/B 取证**。
- 冻结后：升 `v1.0`、状态改 `FROZEN`，同一版本号同时写入：Case Manifest `e2e_output_contract_version`（B:147）与 `E2EComparisonEnvelope.output_contract_version`（B:200）；与 `e2e_interaction_contract_version` 两阶段同值（OQ-BASELINE-15）。
- Case Manifest 另有 `output_schema_version`（B:143）。该字段在诊断案例中指模块输出 Schema 版本（现值 `v0.1` 无出处，OQ-INT-D01-05 / OQ-BD-D01-06 等）；**在端到端 A/B 案例中它与本合同版本是否同一取值，B 未规定** → PENDING_IA0，随 OQ-BASELINE-15 一并定格，本文件不自行认定。
- 冻结必须与 `e2e_interaction_contract.md`、两份基线 Prompt **同批**执行（B:992 三件套齐备，缺一不得宣告 IA-0 通过）。

---

## 7. 冻结前待办（PENDING_IA0）

> 编号沿用 `acceptance/cases/OPEN_QUESTIONS.md` 中央登记册的既有 `OQ-BASELINE-xx` / `OQ-ANON-xx`，本文件**不自建登记文件、不新造编号**。

1. `basis_entries` 容器名与笛语侧转换器输出同名（本合同已按预裁决取名，转换器落点尚不存在）。（OQ-BASELINE-01）
2. `candidate_options[]` 外部可见子集（§2.1）与笛语侧转换器逐字对齐。（OQ-BASELINE-02）
3. `product_ref` 由 `VersionedRef` 降级为 `product_id` 原值的写法与转换器一致。（OQ-BASELINE-03）
4. 顶层 / 候选级 `risks` 分工（§2.3）与转换器**一次性定死**；在此之前任何案例不得进入正式 A/B。（OQ-BASELINE-04）
5. 事实条目标识的具体书写形式定格（§1 末行）。（OQ-BASELINE-05）
6. `persona_card` 的 `persona_ref` 落点：**已定并已拉齐**——两侧同写 A.3.5 `persona_id` 原值（本合同 §1 / §3.3；`baseline_prompt_stage_C.md` §4 JSON / §5 / §6 第 1 条已同批补入）。剩余部分仅随九部分外部可见子集整体定稿 + 同批升版。（OQ-BASELINE-12 / OQ-BASELINE-05）
7. `voice_package.emotion`：**已定并已拉齐**——A v0.2（A:758）+ 预裁决⑦，两侧字段集一致（本合同 §3.6；`baseline_prompt_stage_C.md` §4 JSON / §5 / §6 第 4 条已同批补入）。仅待同批升版。（OQ-BASELINE-11）
8. `voice_package.cues[]`、`faq_items[]`、`official_responses[]`、`assumptions[]` 的条目内部字段定稿，**并含 `video_script.segments[].segment_id` 的书写形式**（A.8 / B 均未展开或未列该字段，本文件给出的是执行侧草案结构；`segment_id` 的设立依据见 §3.4）。（OQ-BASELINE-13）
9. `target_duration_seconds` 由案例统一给定还是模型自定。（OQ-BASELINE-14）
10. `output_contract_version` / `e2e_output_contract_version` / `e2e_interaction_contract_version` 取值定格，两阶段同值；并裁定端到端案例的 `output_schema_version` 与本合同版本是否同值（§6）。（OQ-BASELINE-15）
11. Envelope 三个 `*_ref` 的命名与目录结构。（OQ-ANON-06）
12. 笛语侧「内部对象 → 外部展示 Schema」转换器的可审计落点建设（§4 剔除清单的执行方）。（无中央编号；`contracts/interaction/README.md` §4 第四行）
13. Founder 签字：状态由 `PENDING_IA0` 改为 `FROZEN`，版本由 `v0.1-draft` 升为 `v1.0`，与 `e2e_interaction_contract.md`、两份基线 Prompt 同批执行。（OQ-BASELINE-16）

---

*本文件只引用 B / A / PRD，不复述其定义。任何与 `B_三个核心模块智能验收合同.md` v0.3、`A_模块接口与核心数据字典.md` v0.2、`PRD_笛语智能核_MVP_V3.0_v0.1.md` 原文冲突之处，以真源原文为准。*
