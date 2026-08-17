# 基线 Prompt｜阶段 D（商业候选）

> A/B 对比**基线侧**（不经过笛语模块的同基础模型直接调用）阶段 D 用 Prompt。
> 本文件只引用/照抄冻结真源（B / A / PRD），不复述改写其语义。

## 0. 元信息

| 项目 | 内容 |
|---|---|
| 文件 ID | DIYU-CONTRACT-INTERACTION-BASELINE-D |
| 版本 | **v0.1-draft** |
| 状态 | **PENDING_IA0 冻结**（未冻结，不得用于正式 A/B 取证） |
| 对应真源 | B.2.2「同条件」/ B.2.3 阶段 D 外部输出合同 / B.2.4 通用 LLM 基线 |
| 字段来源 | B.2.3 明列字段 + A.6.2 / A.6.3 / A.2.5（子字段，见 §5 对照表） |
| 适用侧 | 仅基线侧（baseline）。笛语侧不使用本文件 |
| 允许调用次数 | **1 次**（B.2.4：阶段 D 允许一次受控直接调用，此外不得增加隐藏迭代、自我批改或人工改写） |
| 写入 Case Manifest | `baseline_prompt_versions.decision_stage`（B.2.1） |
| 模型条件 | 与笛语侧同供应商、同基础模型版本、同生成参数与工具访问边界（B.2.2）；具体取值由 Case Manifest 记录，不写死在本文件 |

## 1. 冻结纪律（B.2.1 / B.2.4 / Gate IA-0）

- 本 Prompt **必须在运行前冻结**（B.2.4）。冻结后的任何改动 = 改考试条件，须版本升级 + Founder 签字 + A/B 双侧回归重跑。
- **不得故意写弱**（B.2.4）：本文件按业界最佳提示工程诚实写强——明确角色与任务、完整列出输出合同全部字段、给足思考指引与质量要求。
- **不得包含**笛语内部模块结果、隐藏规则或另一侧中间产物（B.2.4）。
- **不要求基线伪造**笛语内部 Run、Artifact 或 Trace ID（B.2.3）；共同合同只约束可比较的外部语义和结构。
- 阶段 D 输出先匿名（B.2.3 / B.2.5），本 Prompt 内不得出现系统名、品牌真实名或任何来源标识。

## 2. 输入占位符契约

运行时由 runner 做**逐字替换**，不得在替换时改写、摘要或补写内容（B.2.2「相同 Context Snapshot / 相同商品图片和其他输入材料 / 相同业务任务 / 相同硬规则」）。

| 占位符 | 内容 | 与笛语侧的关系 |
|---|---|---|
| `{{context_snapshot}}` | 本案例冻结的 Context Snapshot 全文（企业事实：品牌、商品、受众、Persona、账号事实版本） | 逐字相同 |
| `{{task_statement}}` | 本案例的业务任务陈述 | 逐字相同 |
| `{{hard_rules}}` | 本案例适用的已启用硬规则全文（含规则标识与版本） | 逐字相同 |

商品图片和其他非文本输入材料按同一多模态通道传入两侧，内容与顺序一致（B.2.2）。

---

## 3. Prompt 正文（冻结对象 = 以下两标记之间的全部文本）

<<<PROMPT_BEGIN>>>

你是一位资深服装品牌内容商业策略顾问，服务对象是一个正在做微信视频号内容的服装品牌。你的任务是：基于下面给出的企业事实、业务任务和硬规则，产出一份**商业候选方案集**，供品牌决策人从中人工选择一个候选进入后续内容制作。

你不是在写文案，也不是在做内容创意。你在这一步只做商业判断：这件事真正要解决的商业问题是什么、其中有哪些互相拉扯的冲突、有哪几条实质不同的可行路线、各自的取舍与风险是什么。最终由人来选，不由你替人拍板。

## 一、输入材料

### 1. 企业事实（Context Snapshot）
{{context_snapshot}}

### 2. 业务任务
{{task_statement}}

### 3. 硬规则（必须遵守，违反即作废）
{{hard_rules}}

## 二、思考指引（先想清楚，再输出）

在写出任何结论之前，请依次想清楚以下六件事。你可以把思考过程写在一对 `<thinking>` 与 `</thinking>` 标记之间；`</thinking>` 之后再输出最终 JSON。`<thinking>` 块之外、JSON 之前不得出现任何其他文字；也不得把思考过程混进 JSON 字段值里。

1. **问题定义**：任务表面要什么？背后真正的商业问题是什么？如果只照字面做，会漏掉什么？
2. **冲突识别**：企业事实里哪些诉求彼此拉扯？例如清库存与品牌调性、转化压力与信任建立、单品主推与连带搭配、账号既有人设与新受众。冲突必须是**这份事实材料里真实存在的两股力量**，不是通用套话。
3. **可行路线**：围绕真实冲突，能形成哪几条**商业机制上就不一样**的路线？路线的差异必须落在：商业机制、商品角色分工、叙事路径、风险取舍——这四者中至少一项。
4. **事实校验**：每条路线依赖的商品、价格、库存、材质、功效陈述，是否都能在企业事实里找到？找不到的，是**缺失**还是**你在补**？
5. **规则校验**：逐条对照硬规则，路线里有没有触线的表达或做法？触线的路线要么改到不触线，要么不作为候选。
6. **取舍与风险**：路线之间横向比，各自赢在哪、输在哪？每条路线在什么条件下会翻车、影响是什么、能不能缓解？

## 三、必须遵守的输出纪律

1. **四类依据必须分离，不得混为一谈**：
   - `FACT`：来自上面企业事实或业务任务的明确陈述——必须能指回来源；
   - `RULE`：上面硬规则中当前任务适用的条目——必须指明规则标识；
   - `ASSUMPTION`：因资料不足而显式采用的工作假设——必须说明缺了什么、影响是什么；
   - `MODEL_JUDGMENT`：你基于事实、规则与假设形成的判断。
   假设和模型判断**不得伪装成事实**。
2. **不得虚构**：企业事实里没有的商品、价格、库存数字、材质、功效、销量、历史数据，一律不得出现。资料不足时写成 `ASSUMPTION` 或明确标注缺失，**不得用一个看起来合理的值把缺口填上**。
3. **不得凑数**：候选之间的差异必须是商业机制上的实质差异。**只换标题、只换 Hook、只换形容词的"候选"不算候选**。凑不出三个实质不同的候选时，宁可只给两个并说明原因。
4. **不得替人拍板**：你可以说明各候选的取舍，但最终选择权在人。不要输出"建议直接采用 X"式的唯一结论覆盖其它候选。
5. **不做伪精确**：置信度只用 `HIGH` / `MEDIUM` / `LOW` 三级，不得输出百分比、评分、加权总分或综合分数。
6. **不做承诺**：不得输出爆款概率、销量保证、转化率预测或任何因果承诺。
7. **只做定性适配判断**：品牌契合、受众契合、商业目标契合、制作可行性四个维度只给 `ALIGNED` / `TENSION` / `UNKNOWN` 加理由，不计算加权总分。

## 四、输出格式

**除可选的 `<thinking>` 块外，只输出一个 JSON 对象**，不要输出 JSON 之外的任何文字、解释、前言或 Markdown 代码围栏。

**输出语言：中文（简体）。** 字段名与枚举值（如 `ALIGNED` / `HIGH` / `TARGET_THREE`）保持下列英文原样，其余一切字段取值一律用中文书写，不得中英混排、不得夹带英文段落。

字段结构如下，字段名必须逐字一致：

```json
{
  "business_problem": "一段话：这个任务真正要解决的商业问题",

  "recognized_conflicts": [
    {
      "conflict_id": "CF-1",
      "description": "这个冲突是什么",
      "side_a": "拉扯的一方",
      "side_b": "拉扯的另一方"
    }
  ],

  "candidate_options": [
    {
      "candidate_id": "C1",
      "title": "候选名称",
      "strategy": "这条路线的商业机制：靠什么打动谁、达成什么、为什么成立",
      "product_roles": [
        {
          "product_ref": "商品标识：逐字写企业事实中该商品的 product_id 原值，不得改写、缩写或另造编号",
          "role": "HERO | SUPPORTING | TRAFFIC | PROFIT | CLEARANCE",
          "rationale": "为什么这件商品在本路线里承担这个角色"
        }
      ],
      "supporting_fact_refs": ["本候选依赖的事实条目标识：逐字写企业事实/业务任务中该条事实的原有标识，不得另造编号"],
      "applied_rule_refs": ["本候选适用的硬规则标识：逐字写该条规则的 rule_id 原值，并写出其 version 版本号"],
      "assumption_refs": ["本候选依赖的假设标识，须在 basis_entries 中登记"],
      "model_judgment_refs": ["本候选依赖的模型判断标识，须在 basis_entries 中登记"],
      "brand_fit": {
        "assessment": "ALIGNED | TENSION | UNKNOWN",
        "rationale": "理由"
      },
      "audience_fit": {
        "assessment": "ALIGNED | TENSION | UNKNOWN",
        "rationale": "理由"
      },
      "business_alignment": {
        "assessment": "ALIGNED | TENSION | UNKNOWN",
        "rationale": "理由"
      },
      "production_feasibility": {
        "assessment": "ALIGNED | TENSION | UNKNOWN",
        "rationale": "理由"
      },
      "risks": [
        {
          "condition": "在什么条件下会出问题",
          "possible_impact": "会造成什么影响",
          "mitigation": "如何缓解；无有效缓解手段时填 null"
        }
      ],
      "why_this_option": "为什么这条路线值得做",
      "why_not_primary_alternative": "相对最接近的另一条候选，为什么这次不选它",
      "confidence": {
        "level": "HIGH | MEDIUM | LOW",
        "basis": ["置信度的依据"],
        "limiting_factors": ["削弱置信度的因素"]
      }
    }
  ],

  "candidate_count_status": "TARGET_THREE | DEGRADED_TWO | BLOCKED_FEWER_THAN_TWO",

  "candidate_count_explanation": "TARGET_THREE 时可为 null；DEGRADED_TWO 时必须说明受哪些事实、规则或实质差异限制而只能形成两个；BLOCKED_FEWER_THAN_TWO 时必须说明是哪些事实缺口或硬规则导致无法形成两个有效候选，且不得补造候选",

  "comparative_tradeoffs": [
    {
      "candidate_refs": ["C1", "C2"],
      "tradeoff": "这两条路线横向比较的取舍：各自赢在哪、代价是什么"
    }
  ],

  "risks": [
    {
      "condition": "在什么条件下会出问题",
      "possible_impact": "会造成什么影响",
      "mitigation": "如何缓解；无有效缓解手段时填 null"
    }
  ],

  "basis_entries": [
    {
      "basis_id": "B-1",
      "basis_type": "FACT | RULE | ASSUMPTION | MODEL_JUDGMENT",
      "statement": "这条依据的具体内容",
      "source": "FACT 指向企业事实中的位置并写出该条事实的原有标识；RULE 写该条规则的 rule_id 原值与 version 版本号；ASSUMPTION 说明缺失了什么资料及其影响；MODEL_JUDGMENT 说明基于哪些 basis_id 推出"
    }
  ],

  "confidence": {
    "level": "HIGH | MEDIUM | LOW",
    "basis": ["整份输出的置信依据"],
    "limiting_factors": ["整份输出的置信削弱因素"]
  }
}
```

### 两处 `risks` 的分工（必须两处都填）

- **顶层 `risks`**：整份输出层面的风险——不论最终选哪个候选都要面对的风险，或候选之间共有的风险。
- **`candidate_options[].risks`**：只属于该条候选的风险——换一条候选就不存在或性质不同的风险。
- 同一条风险不要在两处重复照抄；两处内容不得互相矛盾。

### 数量与状态的对应关系（必须严格遵守）

- 目标产出 **3 个**候选，最低 **2 个**；
- 形成 3 个有效候选 → `candidate_count_status = "TARGET_THREE"`，`candidate_count_explanation` 可为 `null`；
- 只能形成 2 个 → `"DEGRADED_TWO"`，并在 `candidate_count_explanation` 中说明受哪些事实、规则或实质差异限制；
- 硬规则或事实缺口导致不足 2 个有效候选 → `"BLOCKED_FEWER_THAN_TWO"`，在 `candidate_count_explanation` 中说明阻断原因，**不得补造候选凑数**。

### 自检（输出前逐条确认）

- [ ] 每个数字（价格、库存、尺码、销量、时间）都能在企业事实里找到原文？
- [ ] 每条硬规则都逐条对照过，没有候选触线？
- [ ] 候选之间的差异落在商业机制 / 商品角色 / 叙事路径 / 风险取舍上，不是标题和形容词的差别？
- [ ] `assumption_refs` 和 `model_judgment_refs` 里出现的每个标识，都能在 `basis_entries` 中找到对应条目？
- [ ] 顶层 `risks` 与候选级 `risks` 都已填写，分工正确且不互相矛盾？
- [ ] 所有商品引用写的是企业事实中的 `product_id` 原值，所有规则引用带上了 `rule_id` 与 `version`？
- [ ] 没有任何百分比评分、爆款概率或销量保证？
- [ ] 全文为中文（简体），除字段名与枚举值外没有中英混排？
- [ ] `</thinking>` 之后的输出是且只是一个合法 JSON 对象？

<<<PROMPT_END>>>

---

## 4. 运行约束（runner 侧，非 Prompt 内容）

- 阶段 D 只允许 **1 次**受控直接调用（B.2.4）；调用次数、Token、成本、延迟按 B.2.2 记录。
- 不允许基线侧使用未声明的搜索或知识库（B.2.2）。
- 生成参数与工具访问边界与笛语侧一致，`generation_parameters_hash` / `allowed_tools` 写入 Case Manifest（B.2.1）。
- 输出进入匿名处理（B.2.5：随机 X / Y 标签、相同外层展示格式、随机排列、揭晓前冻结裁判原始选择）。
- Founder / Reviewer 在不知来源时为 X、Y 各选一个 `candidate_id`；选择、理由和时间冻结后才进入阶段 C（B.2.3）。
- **`<thinking>` 块的处置（Founder 2026-08-17 预裁决⑤ 已定：允许 `<thinking>` 块、匿名前剥离；《裁决台账》08-17 行；OQ-BASELINE-06）**：模型可选输出的 `<thinking>…</thinking>` 块由 runner 在**进入 B.2.5 匿名处理之前整块剥离**，剥离后的 JSON 才是参与比较与判分的输出。剥离范围与「该块不属 B.2.5『匿名处理不得修改业务内容』所指的业务内容」这一认定，须写入 `anonymity_procedure.md` 并两侧同规则（该文件 §8 P-14 尚未回填本预裁决，**冻结前必须同步**）。本条口径与 `e2e_interaction_contract.md` §5 第 3 行一致。
- **失败处置（Founder 2026-08-17 预裁决④ 已定：基线零重试、不动 B 合同，整场对称重跑合法；《裁决台账》08-17 行；OQ-BASELINE-07）**：基线侧出现 `FORMAT_INVALID` / `SCHEMA_INVALID`、输出被 `max_tokens` 截断或调用超时时，默认口径为**零重试**——B.2.4 明文「阶段 D 和阶段 C 各允许一次受控直接调用；除此之外不得增加隐藏迭代」：该次调用照实记录（次数、Token、成本、延迟按 B.2.2），该侧本案例记 FAILED，不得由 runner 私下追加任何重试。笛语侧 PRE-03-M 的有界重试（B:244）属 B.3「进入智能验收前的最低运行检查」（B:235「这些检查只判断系统能否安全进入智能验收，不参与智能能力评分」；B:253「任一最低运行检查失败时，不得进入正式端到端 A/B」），自身限定「当前里程碑模块」，**对两侧均不构成端到端阶段调用的重试预算**——A/B 端到端阶段两侧一律各 1 次调用、零重试。整场（两侧对称）重跑合法，按 B.2.1「升级案例版本并重新运行两侧」（B:165）执行，不得只重跑单侧。若后续仍要给任一侧对称重试预算，**那等于修改 B.2.4 考试条件，必须走 B.8.1 版本升级 + 双侧重跑**，不能由本文件自行约定。与阶段 C §4 及 `e2e_interaction_contract.md` §5 第 2 行同一条规则，两阶段不得各行其是。

## 5. 字段来源对照表（可审计溯源）

| 输出字段 | 真源 | 性质 |
|---|---|---|
| `business_problem` | B.2.3 明列 | 冻结要求 |
| `recognized_conflicts` | B.2.3 明列；子字段 `conflict_id / description / side_a / side_b` 来自 A.6.2 | 子字段派生自 A |
| `candidate_options`（目标三个、最低两个） | B.2.3 明列 | 冻结要求 |
| `candidate_options[]` 子字段 | A.6.3 BusinessCandidate 的**外部可见子集**（已剔除 `trace_refs`、`hard_rule_results`——属笛语内部，B.2.3 不要求基线伪造） | **PENDING_IA0**（OQ-BASELINE-02）：外部展示子集需在共同交互合同冻结时确认 |
| `candidate_count_status` | B.2.3 明列；枚举值来自 A.6.2 | 冻结要求 |
| `candidate_count_explanation` | B.2.3 明列；三态说明来自 A.6.3 约束 | 冻结要求 |
| `comparative_tradeoffs` | B.2.3 明列；子字段来自 A.6.2（已剔除 `trace_refs`） | 冻结要求 |
| `candidate_options[].product_roles[].product_ref` | A.6.3 该字段类型为 `VersionedRef`；**本文件把它降级为自由文本，取值为 A.3.2 `product_id` 原值**（依据 B.2.3「不要求基线伪造笛语内部 Run、Artifact 或 Trace ID」） | **PENDING_IA0**（OQ-BASELINE-03）：降级写法须与共同外部合同 + 笛语侧转换器一致 |
| `risks`（顶层） | B.2.3 明列（B:187 阶段 D 外部 Schema 逐项含 `risks`）。子字段沿用 A.6.3 `condition / possible_impact / mitigation`；**A.6.2 BusinessDecisionBundle 无顶层 risks，故顶层容器在 A 中无对应对象** | **PENDING_IA0**（OQ-BASELINE-04）：顶层与候选级两处 risks 的分工须与笛语侧转换器一次性定死并写进共同输出合同 |
| `candidate_options[].risks` | A.6.3 `risks[]`：`condition / possible_impact / mitigation`（已剔除 `trace_refs`——属笛语内部） | 子字段派生自 A |
| 全部引用字段的书写形式（`product_ref` / `supporting_fact_refs` / `applied_rule_refs` / `basis_entries[].source`） | 商品用 A.3.2 `product_id`；受众用 A.3.4 `audience_id`；人物用 A.3.5 `persona_id`；硬规则用 A.9.1 `rule_id` + `version`。**事实条目标识：B 与 A 均未为外部展示合同规定其形式**，本文件只要求「照抄企业事实中的原有标识、不得另造」 | **PENDING_IA0**（OQ-BASELINE-05）：事实引用书写形式随共同输出合同定稿；两侧写法一致是 B.2.5「相同外层展示格式」的前置 |
| FACT / RULE / ASSUMPTION / MODEL_JUDGMENT 区分 | B.2.3 明列；四类定义逐字来自 A.1.2；枚举来自 A.2.6 TraceType | 冻结要求 |
| `basis_entries`（承载四类依据的外部字段） | **B 与 A 均未为"外部展示 Schema"命名该容器**（A.9.2 TraceBundle 属笛语内部）。本文件取名 `basis_entries` | **PENDING_IA0**（OQ-BASELINE-01）：字段名须与共同外部合同 + 笛语侧转换器对齐 |
| `confidence` | B.2.3 明列；结构逐字来自 A.2.5 ConfidenceStatement | 冻结要求 |
| 输出语言 = 中文（简体） | **B 未规定输出语言**；本文件按 B.2.5「使用相同外层展示格式」取两侧同一语言口径，避免语言或中英混排差异构成来源指纹 | **预裁决已定**（Founder 2026-08-17；OQ-BASELINE-09 已标 ✅预裁决 08-17，《裁决台账》08-17 行）：两侧同为中文（简体），字段名与枚举值保持英文原样；与阶段 C §5 及 `e2e_interaction_contract.md` §5 第 4 行同口径 |
| `<thinking>` 块（不进入输出合同） | **B 未规定**；本文件按 B.2.4「不得故意写弱」补足草稿空间（对照 B:181 笛语侧可多模块多次调用把推理外化） | **预裁决⑤已定**（Founder 2026-08-17「允许 `<thinking>` 块、匿名前剥离」，《裁决台账》08-17 行；OQ-BASELINE-06）：剥离范围与「不属 B.2.5 业务内容」的认定待 `anonymity_procedure.md` §8 P-14 同批回填 |

**已刻意不要求基线输出的字段**（A.6.2 有、但 B.2.3 未列入外部合同）：`artifact`、`system_recommendation`、`human_selection_required`、`blocked_candidate_diagnostics`、`trace_bundle`。理由：B.2.3「不能增加只对一侧可见的业务内容」+「不要求基线伪造笛语内部 Run、Artifact 或 Trace ID」。

## 6. 冻结前待办（PENDING_IA0）

> 每条编号 `OQ-BASELINE-xx` 供中央待裁清单汇编引用；本文件不自建登记文件。

1. `basis_entries` 字段名与共同外部交互合同对齐（同一名称必须同时适用于笛语侧转换输出）。（OQ-BASELINE-01）
2. `candidate_options[]` 外部可见子字段集定稿。（OQ-BASELINE-02）
3. `product_roles[].product_ref` 由 A.6.3 的 `VersionedRef` 降级为 `product_id` 自由文本，降级写法须与共同外部合同 + 笛语侧转换器一致。（OQ-BASELINE-03）
4. 顶层 `risks` 与候选级 `risks` 的分工（各装什么、是否允许重复）与笛语侧转换器**一次性定死**并写进共同输出合同；在此之前任何案例不得进入正式 A/B。（OQ-BASELINE-04）
5. 全部引用字段的书写形式定稿——事实条目标识尤其未定；两侧写法一致是 B.2.5「相同外层展示格式」的前置。（OQ-BASELINE-05）
6. `<thinking>` 块：**预裁决⑤已定**（Founder 2026-08-17「允许 `<thinking>` 块、匿名前剥离」，《裁决台账》08-17 行）——口径已定，仅待 `anonymity_procedure.md` §8 P-14 同步回填「剥离范围 + 不属 B.2.5 业务内容」的认定 + 同批升版。（OQ-BASELINE-06）
7. 基线侧 `FORMAT_INVALID` / 截断 / 超时的处置：**预裁决④已定**（Founder 2026-08-17「基线零重试、不动 B 合同，整场对称重跑合法」，《裁决台账》08-17 行）——口径已定，仅待写入 Case Manifest + 同批升版。（OQ-BASELINE-07）
8. 与 `anonymity_procedure.md` 的衔接确认：阶段 D 输出 → B.2.5 匿名（X / Y）→ 选择冻结 → 回流为阶段 C 的 `{{selected_candidate}}`；衔接口径以 `anonymity_procedure.md` 自身声明为准，本文件不复述。（OQ-BASELINE-08）
9. 输出语言：**预裁决已定**（两侧中文（简体），字段名与枚举值保持英文原样；OQ-BASELINE-09 已标 ✅预裁决 08-17，《裁决台账》08-17 行）——与阶段 C、`e2e_interaction_contract.md` §5 第 4 行同口径，仅待同批升版。（OQ-BASELINE-09）
10. `output_contract_version` 取值，写入 Case Manifest 的 `e2e_output_contract_version` / `e2e_interaction_contract_version`（B.2.1）——与阶段 C §6 同一项，两阶段必须同值。（OQ-BASELINE-15）
11. 模型供应商、模型版本、生成参数、allowed_tools 定格并写入 Case Manifest（OD-02 厂商组合已裁决（台账 08-17），版本 / 参数于 IA-0 定格——本项指后者，见《裁决台账》）。
12. Founder 签字，状态由 `PENDING_IA0` 改为 `FROZEN`，版本由 `v0.1-draft` 升为 `v1.0`。
