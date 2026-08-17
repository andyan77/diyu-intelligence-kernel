# 共同两阶段交互合同 ｜ e2e_interaction_contract

| 项目 | 内容 |
|---|---|
| 文件 ID | DIYU-CONTRACT-INTERACTION-E2E-INTERACTION |
| 文件 | `contracts/interaction/e2e_interaction_contract.md` |
| 版本 | **v1.0** |
| 状态 | **EFFECTIVE（已生效；Founder（Faye）重签 2026-08-18T02:39:10+08:00，M0 收口修复批次 P0-6，回执《M0收口回执.md》@24e24a3）** |
| 修订记录 | v0.1-draft 起草（2026-08-17 M0-EP02 建设轮）→ v1.0 内容定稿（2026-08-17 M0 收口修复批次） → **2026-08-17 P0-1 收尾修复**：全文 `B:NNN` 行号按 B v0.4 逐条重算（v0.3→v0.4 在 B:13 / B:929 / B:943 三处插行，每处引用均已回读 B 该行内容核对） |
| 真源 | `B_三个核心模块智能验收合同.md` v0.4（EFFECTIVE）：B.2.1、B.2.2、B.2.3、B.2.4、B.2.5、B.5.1、B.6.4、B.8；`A_模块接口与核心数据字典.md` v0.2（EFFECTIVE）；`PRD_笛语智能核_MVP_V3.0_v0.1.md` |
| 本文件是什么 | Gate IA-0（B:995）三件套的**第 ①  件**：两阶段共同**交互**合同——把 B.2.3 的两侧共同外部交互排成可执行的**时序 + 输入契约 + 两侧同规则**清单 |
| 本文件不是什么 | 不定义输出字段（那是第 ② 件 `e2e_output_contract.md`）、不是任一侧的 Prompt（那是第 ③ 件两份 `baseline_prompt_stage_*.md`）、不复述匿名流程（那是 `anonymity_procedure.md`）。**只引用 B / A / PRD 编号，不复述其定义**；与真源冲突处一律以真源原文为准 |
| 适用范围 | B.5.1 三个锁定端到端匿名 A/B 场景（E2E-01 / E2E-02 / E2E-03）。B.2.3 全段写在「端到端 A/B」名下，B 未把该合同套用于 B.4 模块诊断案例——诊断案例的 Case Manifest 该两字段取 `null`（仓库现状：`acceptance/cases/INT-D02/manifest.quick.yaml` 的 `e2e_interaction_contract_version` / `e2e_output_contract_version` 两字段等，按字段名引用不锁行号），本文件不据此外推 |
| 变更纪律 | 本文件位于 `contracts/`（考试条件区）：改动 = 改考试条件，需版本升级 + Founder 签字 + A/B 双侧回归重跑（`contracts/README.md`、B.9） |
| 写入 Case Manifest | `e2e_interaction_contract_version`（B.2.1，B:147）。定格取值 = **v1.0**，与 `e2e_output_contract_version` / `output_contract_version` 同值（两阶段同值，OQ-BASELINE-15 已定格）；已写入 E2E-01 / E2E-02 / E2E-03 三份运行 Manifest |
| 起草依据 | B.2.3（B:184-205）、B.2.5（B:219-230）、B.8 Gate IA-0（B:988-1000）、`acceptance/cases/OPEN_QUESTIONS.md` 文首「预裁决」（Founder 2026-08-17，《裁决台账》08-17 行） |

---

## 0. 术语与真源指针（本文件不复述定义，只给坐标）

| 术语 / 对象 | 真源坐标 | 本文件用法 |
|---|---|---|
| 「同条件」八项 | B.2.2（B:168-182） | §2 只引用，不逐条复述 |
| 阶段 D / 阶段 C 的外部输出 Schema | B.2.3（B:188 / B:192）；字段逐项见 `e2e_output_contract.md` | §4 只给交付时点，不列字段 |
| 通用 LLM 基线定义、每阶段一次受控调用 | B.2.4（B:206-217） | §5 引用 |
| 匿名处理六项要求 | B.2.5（B:221-230） | §3 只给时点，正文口径见 `anonymity_procedure.md` |
| X / Y 标签、赋值表封存、揭盲前置 | `anonymity_procedure.md` §2 / §3 / §5（其真源为 B.2.5 / B.5.2 / B.5.4 / B.10） | §3 只给衔接点，不复述 |
| `E2EComparisonEnvelope` | B.2.3（B:195-201） | §6 引用字段名，取值来源见 `e2e_output_contract.md` |
| Case Manifest 字段 | B.2.1（B:133-163） | §7 引用 |
| FACT / RULE / ASSUMPTION / MODEL_JUDGMENT | A.1.2（A:63-72）、A.2.6 TraceType（A:206） | 承载字段见 `e2e_output_contract.md`，本文件不复述 |

---

## 1. 两侧与两阶段的定义边界

| 概念 | 坐标 | 本合同的约束 |
|---|---|---|
| 笛语侧（DIYU） | B.2.2 / B:182 | 允许多模块、多次模型调用，但必须记录总调用次数、Token、成本和延迟（B:182）；其内部对象转换为外部展示 Schema 后参与比较 |
| 基线侧（BASELINE） | B.2.4（B:208） | 不经过笛语模块的同基础模型直接调用；阶段 D 与阶段 C **各一次**受控直接调用；Prompt 见 `baseline_prompt_stage_D.md` / `baseline_prompt_stage_C.md` |
| 阶段 D（商业候选） | B.2.3（B:188-190） | 输入同 Snapshot / 任务 / 规则，输出同一外部 Schema；输出先匿名，Founder / Reviewer 在不知来源时分别为 X、Y 各选一个 `candidate_id`，选择、理由和时间冻结后才进入下一阶段 |
| 阶段 C（制作交付包） | B.2.3（B:192） | 两侧各自接收**本侧**被选候选以及相同原始事实和规则，输出同一九部分制作包 Schema + `production_risks` + `assumptions` + `confidence` |

**共同合同只约束可比较的外部语义和结构，不要求基线伪造笛语内部 Run、Artifact 或 Trace ID**（B:204）。**不得增加只对一侧可见的业务内容**（B:188 末句）。

---

## 2. 输入契约（两阶段）

两侧输入必须满足 B.2.2「同条件」全部条款（B:168-182），本文件不复述该条款，只规定**下发形态**：

| 阶段 | 输入项 | 下发形态 | 两侧关系 | 坐标 |
|---|---|---|---|---|
| D | Context Snapshot 全文 | 逐字下发，runner 不得改写、摘要或补写 | 逐字相同 | B:172 |
| D | 业务任务陈述 | 逐字下发 | 逐字相同 | B:174 |
| D | 已启用硬规则全文（含规则标识与版本） | 逐字下发 | 逐字相同 | B:175；规则对象 A.9.1（A:816-827） |
| D | 商品图片与其他非文本材料 | 同一多模态通道、同一批材料、同一顺序 | 逐字相同 | B:173 |
| C | **本侧**被选候选全文（含 `candidate_id`） | 由 §3 冻结结果回流 | **各侧不同**：每侧只收本侧被选候选 | B:192、B:215 |
| C | Context Snapshot / 业务任务 / 硬规则 | 与阶段 D **同一份**，逐字下发 | 逐字相同 | B:210-213 |
| C | 商品图片与其他非文本材料 | 与阶段 D 同一通道、同一批材料、同一顺序 | 逐字相同 | B:173 |

**硬约束：** 阶段 C 只可接收**本侧已经匿名冻结的候选选择**（B:215）；不得把另一侧候选或另一侧任何中间产物注入任一侧（B:215）。

---

## 3. 两阶段时序（每步括号内为真源坐标）

| 步 | 动作 | 承担方 | 坐标 |
|---|---|---|---|
| D1 | 冻结 Case Manifest（含本合同版本、输出合同版本、基线 Prompt 版本、模型条件） | runner + Founder 签字 | B.2.1（B:130、B:147-151） |
| D2 | 同一输入按 §2 同时下发两侧 | runner | B.2.2 |
| D3 | 笛语侧编排产出 → 转换为外部展示 Schema；基线侧 1 次受控调用产出 | 两侧 | B:182、B:208 |
| D4 | **`<thinking>` 块整块剥离**（见 §5 第 3 行），剥离后的 JSON 才是参与比较与判分的输出 | runner（非判分侧） | 预裁决⑤；口径落点 `anonymity_procedure.md`（P-14） |
| D5 | 阶段 D 输出**先匿名**：随机 X / Y 标签、相同外层展示格式、随机排列、隐藏来源与系统名 / Prompt / 调用次数 / 模型日志 | 非判分侧 | B:190、B.2.5（B:221-230）；执行细则 `anonymity_procedure.md` §2 |
| D6 | **冻结点一**：Founder / Reviewer 在不知道来源时，分别为 X、Y 选择一个 `candidate_id`，附理由；**选择、理由和时间冻结后**才进入下一阶段 | Founder / Reviewer | B:190；时序表 `anonymity_procedure.md` §3.1 T2 |
| C1 | 冻结结果回流为各侧阶段 C 的被选候选输入（每侧只回流本侧） | runner | B:192、B:215 |
| C2 | 阶段 C 产出九部分制作包 + `production_risks` + `assumptions` + `confidence` | 两侧 | B:192 |
| C3 | `<thinking>` 块整块剥离（同 D4；不得进入 Envelope） | runner | 预裁决⑤ |
| C4 | 两阶段结果合并为同一 `E2EComparisonEnvelope` | runner（**不由模型输出**） | B:192-202 |
| C5 | **最终匿名裁判**（终审的随机赋值与阶段 D 相互独立） | 判分侧 | B:192；预裁决⑥「阶段 D 与终审独立随机」 |
| C6 | 双窗口作答与冻结、揭盲、证据留档 | 见 `anonymity_procedure.md` §3 / §4 / §5 / §7 | B.5.2 / B.5.3 / B.5.4 / B.10 |

**衔接边界：** D4-D6、C3-C6 的执行细则、留档字段与违规处理**以 `anonymity_procedure.md` 自身声明为准**，本文件只声明时点与前后依赖，不复述（OQ-BASELINE-08）。

---

## 4. 输出交付时点（字段不在本文件）

| 阶段 | 交付物 | 字段定义位置 |
|---|---|---|
| D | 阶段 D 外部展示 Schema（单个 JSON 对象） | `e2e_output_contract.md` §2 |
| C | 阶段 C 九部分制作包外部展示 Schema（单个 JSON 对象） | `e2e_output_contract.md` §3 |
| C4 | `E2EComparisonEnvelope` | B:195-201；取值来源见 `e2e_output_contract.md` §5 |

两阶段输出均为**单个 JSON 对象**，除可选 `<thinking>` 块外不得有其他文字（两侧同规则，见 §5）。

---

## 5. 两侧同规则条款

以下条款**两侧同时适用**。任一条只对一侧成立即违反 B.2.2「同条件」，该次运行不得作为 B 意义上的验收证据。

| # | 规则 | 两侧口径 | 依据 / 裁决状态 |
|---|---|---|---|
| 1 | **调用预算** | 基线侧：阶段 D、阶段 C **各 1 次**受控直接调用，此外不得增加隐藏迭代、自我批改或人工改写。笛语侧：允许多模块多次调用（编排本身是被验证的能力），但必须记录总调用次数、Token、成本和延迟，不得通过无限调用换取结果 | B:208 / B:182（B 明文非对称，本合同照抄不拉平） |
| 2 | **零重试** | 任一侧出现格式非法、输出被 `max_tokens` 截断或调用超时时，**该次调用照实记录，该侧本案例记 FAILED，runner 不得私下追加任何重试**。整场（两侧对称）重跑合法——重跑按 B.2.1「升级案例版本并重新运行两侧」（B:166）执行，不得只重跑单侧 | **预裁决④**（OPEN_QUESTIONS 文首：「基线零重试、不动 B 合同（整场对称重跑合法）」；OQ-BASELINE-07）。B.2.4 明文只给一次受控调用；笛语侧 PRE-03-M 的有界重试（B:245）属 **B.3「进入智能验收前的最低运行检查」**（B:236「只判断系统能否安全进入智能验收，不参与智能能力评分」；B:254「任一最低运行检查失败时，不得进入正式端到端 A/B」），自身限定「当前里程碑模块」，**对两侧均不构成端到端阶段调用的重试预算**——A/B 端到端阶段两侧一律各 1 次调用、零重试（两份基线 Prompt §4 同句） |
| 3 | **`<thinking>` 块** | **允许**两侧模型输出一对 `<thinking>…</thinking>` 块作为草稿空间；由 runner 在**进入 B.2.5 匿名处理之前整块剥离**；剥离后的 JSON 才参与比较与判分；`<thinking>` 块**不得进入** `E2EComparisonEnvelope`、不得进入判分材料 | **预裁决⑤**（OPEN_QUESTIONS 文首：「允许 `<thinking>` 块、匿名前剥离」；OQ-BASELINE-06）。剥离范围与「该块不属 B.2.5『匿名处理不得修改业务内容』（B:230）所指业务内容」的认定已回填 `anonymity_procedure.md` 生效条款（§2.3 `stripped_fields_manifest` / §2.3.1 勾选清单）：**整块剥离**（`<thinking>` 与 `</thinking>` 标记及其间全部内容），执行时点 = 进入 B.2.5 匿名处理之前，执行人 = 非判分侧 runner，被剥离内容留副本于该文件 §2.3 `stripped_copy_location`，不进裁判视图；该块归 B:226「隐藏系统名、Prompt、调用次数和模型日志」一侧 |
| 4 | **输出语言** | **中文（简体）**。字段名与枚举值（如 `ALIGNED` / `HIGH` / `TARGET_THREE` / `PAUSE`）保持英文原样，其余一切字段取值一律中文，不得中英混排、不得夹带英文段落 | **预裁决**（OQ-BASELINE-09 已标 ✅预裁决 08-17，取执行侧推荐口径）。B 未规定输出语言；依据是 B:225「使用相同外层展示格式」——语言或中英混排差异会构成来源指纹 |
| 5 | **输出体裁** | 除可选 `<thinking>` 块外只输出一个 JSON 对象；不得输出前言、解释或 Markdown 代码围栏；不得把推理混进字段值 | B:225「相同外层展示格式」 |
| 6 | **工具边界** | `allowed_tools` 为空数组 = **零外部工具**。笛语侧的**多模块编排与多次模型调用**不计入 `allowed_tools`（B:182 明文授权「编排本身是被验证的能力」，须按 B:182 记录总调用次数、Token、成本和延迟）；**B:179「不允许任一侧使用未声明的搜索或知识库」对两侧同等适用，不因内部编排而豁免**——笛语侧内部模块同样不得检索未声明的搜索或知识库 | B:179（无例外条款）+ B:182（只授权多模块 / 多次调用，未提检索或知识库）；**执行侧自决项**（OPEN_QUESTIONS 文首：「allowed_tools 空=零外部工具（内部编排豁免 B.2.2）」）——本行按 B:179 原文**收窄**该自决项：豁免只及于「多模块 / 多次调用不计入 `allowed_tools`」，不及于检索与知识库禁令。若确需让笛语侧内部检索合法，属**改考试条件**，须走 Founder 裁决而非执行侧自决。定格取值 `allowed_tools: []`，已写入全部 20 份运行 Case Manifest |
| 7 | **Brand Memory** | 首轮验收 `brand_memory_state = DISABLED`，`approved_brand_memory_refs` 必须为空；两份基线 Prompt 不设 Brand Memory 输入通道。若后续转为 `APPROVED_SET`，必须先为两侧增设**完全一致**的 Brand Memory 通道并同批升版，否则 B.2.2 该项不可证 | B:96、B:180；OQ-BASELINE-17 |
| 8 | **模型条件** | 同模型供应商、同基础模型版本、同生成参数与工具访问边界；具体取值不写死在任何合同或 Prompt 文件，由 Case Manifest 的 `model_provider` / `model_name` / `model_version` / `generation_parameters_hash` / `allowed_tools` 记录 | B:176-178、B.2.1（B:157-161）；OD-02 厂商组合已裁决（《裁决台账》08-17），版本与参数已于 IA-0 定格并写入 20 份运行 Manifest：`model_provider = Alibaba Cloud DashScope`、`model_name = qwen-max-0107`（两侧同用）、`model_version = snapshot-0107（models 接口回执 2026-08-17）`；多模态通道 `qwen-vl-max`（无快照版：锁别名 + 逐次运行留存接口返回的实际 model 回执）、跨厂商审计侧 `deepseek-v4-pro`（非 A/B 参赛方）与生成参数（`temperature 0.3` / `top_p 0.8` / 固定 `seed`）的唯一真源 = `contracts/interaction/generation_parameters.json`；Case Manifest 的 `generation_parameters_hash` 一律按该文件当前内容由冻结门实时重算比对，不得手填未经重算的值 |
| 9 | **不伪造内部标识** | 不要求基线伪造笛语内部 Run、Artifact 或 Trace ID；笛语侧向外部展示 Schema 转换时必须剔除对应内部字段，两侧展示口径一致 | B:204；剔除清单见 `e2e_output_contract.md` §4 |
| 10 | **不增加单侧可见内容** | 笛语内部对象可转换为展示 Schema，但**不能增加只对一侧可见的业务内容** | B:188 末句 |
| 11 | **匿名不改业务内容** | 匿名处理不得修改业务内容（`<thinking>` 剥离依第 3 行认定处理） | B:230 |

---

## 6. `E2EComparisonEnvelope` 的组装责任

- 由 **runner 组装**，不由任一侧模型输出（B:192「两阶段结果合并为同一 E2EComparisonEnvelope」，B 未把该对象列入任一侧的输出 Schema）。
- 字段名与 `package_section_count: 9` 照 B:195-201，本文件不复述取值语义；各字段取值来源见 `e2e_output_contract.md` §5。
- `output_contract_version` 取值 = 本目录 `e2e_output_contract.md` 的冻结版本号 **v1.0**，与 Case Manifest 的 `e2e_output_contract_version` 同值；`e2e_interaction_contract_version` = 本文件的冻结版本号 **v1.0**。两阶段同值（OQ-BASELINE-15 已定格）。

---

## 7. 与 Case Manifest 的对应

| Case Manifest 字段（B.2.1） | 由谁决定 | 定格取值（IA-0 2026-08-17 批次） |
|---|---|---|
| `e2e_interaction_contract_version`（B:147） | 本文件冻结版本号 | **v1.0** |
| `e2e_output_contract_version`（B:148） | `e2e_output_contract.md` 冻结版本号 | **v1.0** |
| `baseline_prompt_versions.decision_stage` / `.creative_stage`（B:149-151） | 两份基线 Prompt 冻结版本号 | **v1.0** / **v1.0** |
| `output_schema_version`（B:144） | 见 `e2e_output_contract.md` §6 | **v0.1**——端到端案例该字段指 `contracts/schemas/` 模块输出 Schema 的版本戳，**与本合同 / 输出合同的版本号不同值**（三份 E2E 运行 Manifest 现取 `v0.1`；两份合同版本由 `e2e_interaction_contract_version` / `e2e_output_contract_version` 承载） |
| `allowed_tools`（B:161） | §5 第 6 行 | `[]`（零外部工具） |

> 落盘记录：`acceptance/cases/E2E-01|E2E-02|E2E-03/manifest.yaml` 三份的 `e2e_interaction_contract_version` / `e2e_output_contract_version` 已随 IA-0 批次由原占位值回填为 `"v1.0"`，两行注释同批改为指向本文件与 `e2e_output_contract.md`（原「共同交互合同文件尚不存在」的指针不再出现在字段行）。三份 Manifest 属考卷区，本文件不改动，其修订走审批（见 §9 第 7 条）。

---

## 8. 违规与失败处置

| 情形 | 处置 | 依据 |
|---|---|---|
| 任一侧输出不满足输出合同结构 | 该侧本案例记 FAILED，零重试（§5 第 2 行） | 预裁决④ |
| 两侧输入不一致 / 无法证明条件一致 | 该次运行不得作为验收证据 | B.2.2；失败标签见 B.6.4 `EVAL_CONDITION_MISMATCH` |
| 匿名被破坏（判分人提交前知道来源） | 见 `anonymity_procedure.md` §6 | B.6.4 `EVAL_BLINDING_BROKEN`；本文件不复述 |
| 违反 B.2.5（匿名处理改动业务内容 / 两侧外层展示格式不同） | 标签 `EVAL_BLINDING_PROCEDURE_INVALID`：该次盲测运行作废、不得作为 IA-4 证据，只能按 B.8.1 修复后按相同条件重测；执行细则见 `anonymity_procedure.md` §6 | B.6.4（B v0.4 补登该标签并列入自动阻断清单；Founder 2026-08-17 裁决，《裁决台账》「修复批次两裁决」行） |

---

## 9. 冻结待办关闭记录（IA-0 2026-08-17 签字批次 + M0 收口修复批次回填）

> 编号沿用 `acceptance/cases/OPEN_QUESTIONS.md` 中央登记册的既有 `OQ-BASELINE-xx` / `OQ-ANON-xx`，本文件**不自建登记文件、不新造编号**。

1. **已关闭**：本文件与 `e2e_output_contract.md` 已落盘，并随 M0 收口修复批次 P0-1「真冻结收敛」内容定稿为 v1.0，OQ-BASELINE-16 的「文件不存在」与「未升版」两部分一并关闭；生效签字统一由 P0-6 Founder 重签产生，见文首控制块「状态」行。（OQ-BASELINE-16）
2. **已关闭**：`e2e_interaction_contract_version` = `e2e_output_contract_version` = `output_contract_version` = **v1.0**，两阶段同值；结果见 §6 与 §7 表。（OQ-BASELINE-15）
3. **已关闭**：`anonymity_procedure.md` 的 P-02（阶段 D 与终审**不复用**同一赋值表，终审重新独立随机并另起 `assignment_id`，两张赋值记录各自密封 + git 哈希封存）、P-09（揭盲后禁回改，要改 = 重测）、P-14（`<thinking>` 匿名前**整块剥离**，不属 B:230 业务内容）三项预裁决⑤⑥口径已同批回填该文件生效条款（§2.3 / §2.4 / §3.1 / §5），本文件不代为改写。（OQ-ANON-02 / OQ-ANON-09 / OQ-ANON-14；OQ-BASELINE-06 / OQ-BASELINE-08）
4. **结转 M1（笛语侧模块构建）建设项**：笛语侧「内部对象 → 外部展示 Schema」转换器的可审计落点属笛语侧实现，触发点 = Case Manifest `diyu_build_version` 由 `PENDING_BUILD` 转为实值时；§5 第 9 / 10 行与 `e2e_output_contract.md` §4 的剔除清单、§2.3 的 `risks` 分工必须在**笛语侧首次进入正式 A/B 之前**与该转换器一次性对齐，否则 B:188 末句与 B:204 在笛语侧不可验证。**IA-0 冻结不依赖本项**：Gate IA-0 的必备条件（B.8「Gate IA-0｜验收基线冻结」）是两阶段共同交互合同、输出合同与基线 Prompt 已冻结、模型条件已确定、裁判与匿名流程已确定，均不含笛语侧转换器。（无中央编号；对齐口径随 OQ-BASELINE-02 / 04 / 05 的合同侧定稿已就位）
5. **结转 M1 核验项**：多模态通道三方一致性（阶段 D、阶段 C、笛语侧：同一通道、同一批材料、同一顺序）中的笛语侧一侧在笛语侧构建完成前无实体可核。合同侧两阶段口径已在 §2 定死（同一多模态通道、同一批材料、同一顺序，B:173），三方核验随笛语侧构建同批执行，触发点同第 4 条。（OQ-BASELINE-10）
6. **已关闭**：`allowed_tools = []`；`model_provider = Alibaba Cloud DashScope`、`model_name = qwen-max-0107`、`model_version = snapshot-0107（models 接口回执 2026-08-17）` 已写入 20 份运行 Case Manifest；`generation_parameters_hash` 的唯一真源 = `contracts/interaction/generation_parameters.json`，按该文件当前内容由冻结门实时重算比对（详见 §5 第 6 / 8 行）。（执行侧自决项 + 《裁决台账》OD-02 行）
7. **已关闭**：E2E-01 / E2E-02 / E2E-03 三份 Manifest 的两个合同版本字段已回填 `"v1.0"`，字段行注释指针同批改指本文件与 `e2e_output_contract.md`（改考卷走审批，本文件不代改）。
8. **已关闭（内容面）**：B:995 三件套（本文件 + `e2e_output_contract.md` + 两份基线 Prompt）已随 M0 收口修复批次 P0-1 同批内容定稿为 v1.0，**三件套缺一不得宣告 IA-0 通过**。2026-08-17T19:08:38+08:00 的旧签字批次随 M0 收口宣告撤回（《裁决台账》08-17；`IA-0_冻结签字包.md` 六「签字记录」保留为历史事实，不再作为 M0 收口依据）；生效签字由 P0-6 Founder 基于修复后最终资产重新签字产生，本文件生效状态以文首控制块「状态」行为准。

---

*本文件只引用 B / A / PRD，不复述其定义。任何与 `B_三个核心模块智能验收合同.md` v0.4、`A_模块接口与核心数据字典.md` v0.2 原文冲突之处，以真源原文为准。*
