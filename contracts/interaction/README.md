# contracts/interaction/｜两阶段交互合同与基线 Prompt

| 项目 | 内容 |
|---|---|
| 文件 ID | DIYU-CONTRACT-INTERACTION-README |
| 文件 | `contracts/interaction/README.md` |
| 版本 | **v1.0** |
| 状态 | **CONTENT-FROZEN（内容定稿）；生效 PENDING_RESIGN_P0-6（Founder 重签后本行更新为 EFFECTIVE+签字时间）** |
| 批准 | 内容经 M0 收口修复批次 P0-1「真冻结收敛」逐处关闭后定稿；生效签字 PENDING_RESIGN_P0-6——2026-08-17T19:08:38+08:00 的旧签字批次随 M0 收口宣告撤回（《裁决台账》08-17），按《M0收口修复批次_执行规格.md》P0-6 由 Founder 基于修复后最终资产重新签字，不沿用旧签字时间 |
| 真源 | `B_三个核心模块智能验收合同.md` v0.4（EFFECTIVE）：B.2.2 / B.2.3 / B.2.4 / B.2.5 / B.6.4 / B.8 / B.8.1；`A_模块接口与核心数据字典.md` v0.2（EFFECTIVE）；`PRD_笛语智能核_MVP_V3.0_v0.1.md` |
| 本文件是什么 | 本目录的**状态索引与关系说明**：六份合同文档各承载什么、对应哪条 B 条款、当前版本与状态、IA-0 冻结前置项的关闭记录 |
| 本文件不是什么 | **不计入 B:995 三件套**（那是共同交互合同 ① + 共同输出合同 ② + 基线 Prompt ③ 两份 = 四份文件）；不复述任何真源定义，与真源冲突处一律以真源原文为准 |
| 变更纪律 | 本文件位于 `contracts/`（考试条件区）：改动 = 改考试条件，需版本升级 + Founder 签字 + A/B 双侧回归重跑（`contracts/README.md`、B.9） |
| 修订记录 | v0.1 起草（M0-EP02 建设轮）→ 2026-08-17 IA-0 定格批次 → 2026-08-17 M0 收口修复批次 P0-1 真冻结收敛（删除首行覆盖声明、逐处残留关闭、目录份数口径统一为六份）。**v1.0 内容定稿（2026-08-17 M0 收口修复批次）** → **2026-08-17 P0-1 收尾修复**：全文 `B:NNN` 行号按 B v0.4 逐条重算（v0.3→v0.4 在 B:13 / B:929 / B:943 三处插行，每处引用均已回读 B 该行内容核对） |

> 本目录承载 B.2.3 共同两阶段交互合同的**基线侧实体化文件**。
> 真源是 `B_三个核心模块智能验收合同.md`（v0.4，EFFECTIVE）。本目录所有文件只引用/照抄 B，不复述改写其语义。

## 1. 目录内容与真源对应关系

| 文件 | 承载什么 | 对应 B 条款 | 版本 | 状态 |
|---|---|---|---|---|
| `baseline_prompt_stage_D.md` | 基线侧**阶段 D（商业候选）**的 Prompt 全文、输入占位符契约、输出 JSON 字段合同、字段来源对照 | B.2.3 阶段 D 外部输出 Schema；B.2.4 基线定义与"不得故意写弱" | v1.0 | **内容定稿，随 P0-6 重签生效** |
| `baseline_prompt_stage_C.md` | 基线侧**阶段 C（制作交付包）**的 Prompt 全文、输入占位符契约、九部分输出合同、字段来源对照 | B.2.3 阶段 C 九部分制作包 Schema + production_risks / assumptions / confidence；B.2.4 "阶段 C 只可接收本侧已经匿名冻结的候选选择" | v1.0 | **内容定稿，随 P0-6 重签生效** |
| `e2e_interaction_contract.md` | **两阶段共同交互合同**（B:995 三件套第 ① 件）：两侧共同的两阶段时序、输入契约、两侧同规则条款（调用预算 / 零重试 / `<thinking>` 剥离 / 输出语言 / 工具边界 / Brand Memory / 不伪造内部标识）、Envelope 组装责任 | B.2.2 / B.2.3（B:184-205）/ B.2.4 / B.2.5；Gate IA-0（B:995） | v1.0 | **内容定稿，随 P0-6 重签生效** |
| `e2e_output_contract.md` | **共同输出合同**（B:995 三件套第 ② 件）：阶段 D 外部展示 Schema 逐项（B:188）、阶段 C 九部分逐项（PRD 7.2 含第九项 Comment Operation Package）、引用书写形式、剔除清单、`E2EComparisonEnvelope` 取值来源 | B.2.3（B:188 / B:192 / B:195-201）；PRD 7.2 / 7.3；A.6.2 / A.6.3 / A.7.2 / A.8 | v1.0 | **内容定稿，随 P0-6 重签生效** |
| `anonymity_procedure.md` | **B.2.5 匿名判分流程**：匿名与冻结要求的可执行时序 + 留档清单、B.5.2 双窗口、B.2.5 六项逐项勾选、失败标签映射、P-01～P-14 执行值 | B.2.5 / B.5.2 / B.5.3 / B.5.4 / B.6.4；Gate IA-0（B:997「裁判与匿名流程已确定」） | v1.0 | **内容定稿，随 P0-6 重签生效** |
| `README.md` | 本说明：本目录文件的关系、版本口径、冻结纪律、IA-0 冻结前置项关闭记录 | B.2.2 / B.2.3 / B.2.4；Gate IA-0（B.8） | v1.0 | **内容定稿，随 P0-6 重签生效** |

`anonymity_procedure.md` 与本目录其余文件的衔接点：阶段 D 输出交给它做匿名与选择冻结，冻结结果再回流为阶段 C 的 `{{selected_candidate}}`。该文件的流程细节以其自身条款为准，本 README 不复述。本目录另有参数真源 `generation_parameters.json`（非合同文档，不计入上表六份；见 §5）。

### 三条 B 条款各管什么

| 条款 | 管的事 | 在本目录如何落地 |
|---|---|---|
| **B.2.2「同条件」** | 两侧输入必须一致：同 Context Snapshot、同商品图片与其他输入材料、同业务任务、同硬规则、同最终输出合同、同模型供应商与基础模型版本、同生成参数与工具访问边界；不允许任一侧使用未声明的搜索或知识库；Brand Memory 启用状态与引用完全一致 | 两份 Prompt 的 **§2 输入占位符契约**：`{{context_snapshot}}` / `{{task_statement}}` / `{{hard_rules}}`（阶段 C 另加 `{{selected_candidate}}`）由 runner 逐字替换，不得改写摘要。模型与参数不写死在 Prompt 里，由 Case Manifest（B.2.1）记录，参数真源见 `generation_parameters.json`。**Brand Memory**：B:96「首轮验收关闭 Brand Memory」，故两份 Prompt **不设 Brand Memory 输入通道**，基线侧不注入任何 Brand Memory 内容；启用状态与引用由 Case Manifest 的 `brand_memory_state` / `approved_brand_memory_refs` 记录（B:145-146；DISABLED 时引用列表必须为空，B:180）。**首轮 `DISABLED` 已随 IA-0 定格**；日后若转 `APPROVED_SET`，属改考试条件——必须先在两份 Prompt §2 增设与笛语侧完全一致的 Brand Memory 通道并同批升版，再按 B.8.1 走 Founder 签字 + 双侧回归重跑（OQ-BASELINE-17 ✅预裁决 2026-08-17，《裁决台账》08-17 行） |
| **B.2.3 共同两阶段交互与输出合同** | 两侧执行同一外部交互合同：阶段 D 输出同一外部 Schema → 匿名选择冻结 → 阶段 C 各接本侧被选候选、输出同一九部分包 → 合并为 `E2EComparisonEnvelope` 做最终匿名裁判。只约束可比较的**外部**语义和结构，不要求基线伪造笛语内部 Run / Artifact / Trace ID | 两份 Prompt 的 **§4 输出格式**逐字段列出外部 Schema；**§5 字段来源对照表**标明每个字段来自 B.2.3 明列还是 A 的子字段派生，并列出**刻意不要求基线输出**的笛语内部字段及理由 |
| **B.2.4 通用 LLM 基线** | 正式基线 = 不经笛语模块的同基础模型直接调用；阶段 D 与阶段 C **各允许一次**受控直接调用；不得增加隐藏迭代、自我批改或人工改写；两阶段 Prompt 运行前必须冻结，**不得故意写弱**，不得包含笛语内部模块结果、隐藏规则或另一侧中间产物 | 两份 Prompt 的 **§0 元信息**（允许调用次数 = 1）、**§1 冻结纪律**、**§4 运行约束**。Prompt 正文按业界最佳提示工程诚实写强：明确角色与任务、完整输出字段、思考指引、质量要求与输出前自检 |

### 两阶段串联（B.2.3 流程）

```text
阶段 D：{{context_snapshot}} + {{task_statement}} + {{hard_rules}}
          → 基线侧 1 次调用 → 商业候选外部 Schema
          → B.2.5 匿名（X / Y）→ Founder / Reviewer 各选一个 candidate_id
          → 选择、理由、时间冻结
阶段 C：{{selected_candidate}}（本侧被选候选）+ 同一 {{context_snapshot}} / {{task_statement}} / {{hard_rules}}
          → 基线侧 1 次调用 → 九部分制作交付包 + production_risks + assumptions + confidence
          → runner 组装 E2EComparisonEnvelope（package_section_count: 9）
          → 最终匿名裁判
```

## 2. 版本口径

- 本目录**全部六份合同文档**（两份共同合同 + 两份基线 Prompt + `anonymity_procedure.md` + 本 README）统一为 **v1.0**，内容于 2026-08-17（M0 收口修复批次 P0-1）**同批定稿**；生效以 Founder 重签为准（见各文件文档控制块）。
- **正式 A/B 取证以 v1.0 定稿内容为唯一依据。** 取证开跑另有两条前置：① Founder 重签生效（《M0收口修复批次_执行规格.md》P0-6）；② 笛语侧内部对象 → 外部展示 Schema 转换器与本目录合同对齐（§4 第 4 行，M1 建设项）。两条未成立前的运行只作工程联调，不构成 B 意义上的验收证据。
- 已按 B.2.1 写入 Case Manifest 的四个版本字段：`e2e_interaction_contract_version`（B:147）/ `e2e_output_contract_version`（B:148，与 `E2EComparisonEnvelope.output_contract_version` 同值）/ `baseline_prompt_versions.decision_stage` / `baseline_prompt_versions.creative_stage`。**取值均为 `v1.0`**；三份 B.5.1 端到端案例（E2E-01 / E2E-02 / E2E-03）实测已回填，其余 17 份模块诊断案例按 B.5 适用面留 `null`（"不适用"，非占位待填）。
- 两份 Prompt §6、`e2e_interaction_contract.md` §9、`e2e_output_contract.md` §7、`anonymity_procedure.md` §8 的冻结前待办**已全部关闭**：按 Founder 2026-08-17 预裁决八主题、修复批次两裁决（B v0.4 新增标签 + 匿名流程六执行值）逐条回填。编号沿用 `acceptance/cases/OPEN_QUESTIONS.md` 的既有 `OQ-BASELINE-xx`（17 条全 ✅预裁决 08-17）/ `OQ-ANON-xx`（14 条全 ✅预裁决 08-17），不新造编号；该登记册文首已标「本册全部裁决类条目就此关闭」。本目录不自建待裁登记文件。

## 3. IA-0 冻结纪律

Gate IA-0（B.8）要求「两阶段共同交互合同、输出合同和基线 Prompt 已冻结」。据此：

1. **定稿状态**：六份文件内容已定稿为 v1.0，不再自由修改；此后任何改动一律按下方第 3 条办理（= 改考试条件）。生效签字状态见各文件文档控制块。
2. **冻结动作的前置 = Gate IA-0 三件套齐备**。B:995 要求的是**三件**：① 两阶段**共同交互合同**文件（`e2e_interaction_contract.md`）；② **共同输出合同**文件（`e2e_output_contract.md`）；③ **基线 Prompt**（本目录两份）。**三件均已落盘并于 2026-08-17 同批定稿为 v1.0**。据此：
   - **§4 冻结前置项已全部关闭**：原表中标「是」的行，或已按裁决回填关闭，或已单义化为 M1 结转建设项（第 4 行），无一行以未决状态留在冻结前置面；
   - 定稿动作按既定顺序执行：三件齐备 → 四份文件冻结前待办全部关闭（两份 Prompt §6、`e2e_interaction_contract.md` §9、`e2e_output_contract.md` §7）+ `anonymity_procedure.md` §8 P-01～P-14 全部落值 → 六份同批升 v1.0 → 写入 Case Manifest 四个版本字段 → Founder 重签生效（P0-6）。
   - **同批纪律**：六份文件必须同批升版、同批冻结；相互之间任何已登记的口径差异必须在同一批次内消除，不得一件冻结、另一件仍带差异。**已登记的两处差异（`persona_card.persona_ref` 落点、`voice_package.emotion`）已消除**——两侧现同写 `persona_ref` = A.3.5 `persona_id` 原值、同带 `emotion`（见 `e2e_output_contract.md` §3.3 / §3.6 与 `baseline_prompt_stage_C.md` §4 / §5 / §6）。
   - 注意区分两个「三」：**B:995 的三件套**是合同层面的三类文件（① ② 各一份 + ③ 两份 = 共四份文件）；**本 README** 不计入其中，只是目录说明。二者不可互相顶替。
3. **定稿后的任何改动 = 改考试条件**（B.2.2「同条件」的一部分，见 `contracts/README.md`），必须同时满足：
   - **版本升级**（不得原地覆盖——B.2.1「确需修改时，必须升级案例版本并重新运行两侧」）；
   - **Founder 签字**；
   - **A/B 双侧回归重跑**——只重跑基线侧不成立，因为"同条件"是双侧共同属性；
   - 受影响案例的 Case Manifest 同步升版。
4. **绝对禁止**（B.2.1 / Gate IA-0 最后一条）：**不得在查看结果后修改**事实、裁判问题、允许答案、禁止结果或通过条件；不得依据已看到的结果反向修改本目录任何 Prompt。
5. IA-0 通过只表示**验收条件可以执行**，不表示能力已经成立（B.8）。

## 4. IA-0 冻结前置项关闭记录表

| 项 | 现状（2026-08-17 修复批次 P0-1 收敛后） | 关闭方式 / 关闭时间 |
|---|---|---|
| 共同外部**交互**合同文件 | `e2e_interaction_contract.md` **v1.0 内容定稿**：两阶段时序、输入契约、两侧同规则条款与 Envelope 组装责任均已定义；§9 冻结前待办（含 `anonymity_procedure.md` §8 的 P-02 / P-09 / P-14 回填、笛语侧转换器对齐口径）已逐条关闭 | **已关闭**——B:995 三件套之一，2026-08-17 同批定稿（OQ-BASELINE-16 ✅预裁决 08-17） |
| 共同外部**输出**合同文件 | `e2e_output_contract.md` **v1.0 内容定稿**：阶段 D 逐项（B:188）、阶段 C 九部分逐项（PRD 7.2）、引用书写形式、剔除清单、Envelope 取值来源均已定义。`output_contract_version` 取值 = **`v1.0`**（同一取值同时作为 `E2EComparisonEnvelope.output_contract_version` 与 Manifest 的 `e2e_output_contract_version` / `e2e_interaction_contract_version`，两阶段同值）。原与阶段 C 基线 Prompt 的两处差异（`persona_card.persona_ref` OQ-BASELINE-12 / 05、`voice_package.emotion` OQ-BASELINE-11）已两侧同批消除 | **已关闭**——B:995 三件套之一，2026-08-17 同批定稿（OQ-BASELINE-04 / 05 / 15 / 16 均 ✅预裁决 08-17） |
| 基线 Prompt（本目录两份） | 两份均 **v1.0 内容定稿**，§6 待办逐条关闭：预裁决④（基线零重试、不动 B 合同，整场对称重跑合法）⑤（允许 `<thinking>`、匿名前整段剥离）⑦（VoicePackage 补 `emotion`）已回填；OQ-BASELINE-01～17 共 17 条全部 ✅预裁决 08-17，`persona_ref`、`emotion` 两处差异已按 `e2e_output_contract.md` §7 同批消除 | **已关闭**——B:995 三件套之一，§6 全部关闭后于 2026-08-17 同批定稿 |
| 笛语侧内部对象 → 外部展示 Schema 转换器 | **口径已定死、实现属 M1**：转换器必须遵守的外部字段面、顶层 `risks` 与候选级 `risks` 的分工、`ref` 书写形式已由 OQ-BASELINE-02 / 04 / 05 / 12 / 13（全 ✅预裁决 08-17）裁定并写入 `e2e_output_contract.md` §7 与 `e2e_interaction_contract.md` §9；**转换器本身的实现与可审计留痕是 M1 建设项**，不属 IA-0 内容定稿的前置。正式 A/B 取证在该转换器落盘并与本目录 v1.0 合同对齐后开跑（见 §2 第二条前置②） | **改列为 M1 结转建设项**（2026-08-17 单义化）——本项不在 B:995 三件套内，合同侧口径已随三件套同批定稿 |
| 模型条件定格 | 已定格（Founder 2026-08-17，《裁决台账》08-17 IA-0 行）：`model_provider` = `Alibaba Cloud DashScope`；`model_name` = `qwen-max-0107`（快照版，models 接口实测回执，**两侧同用**）；`model_version` = `snapshot-0107（models 接口回执 2026-08-17）`；多模态 `qwen-vl-max`（无快照版，锁别名 + 逐次运行留存接口回执）；审计侧 `deepseek-v4-pro`（跨厂商审计，非 A/B 参赛方）。生成参数真源 = 本目录 `generation_parameters.json`；`generation_parameters_hash` = 该文件规范化 JSON（UTF-8 + 键排序 + 紧凑分隔符）的 sha256，由冻结门**实时重算**后与 Case Manifest 记录值比对（重算与回填见修复批次 P0-2 / P0-4） | **已关闭**——B:996「模型条件已确定」；OD-02 定格记录 + 《裁决台账》08-17 |
| 裁判与匿名流程 | `anonymity_procedure.md` **v1.0 内容定稿**，§8 P-01～P-14 全部落具体裁决值或精确裁决引用。其中 **P-05 / P-08 / P-11 由 B v0.3→v0.4 新增失败标签 `EVAL_BLINDING_PROCEDURE_INVALID`（B.6.4，已列入自动阻断清单）一枚关闭**——后果 = 该次盲测运行作废、不得作为 IA-4 证据、只能按 B.8.1 修复后同条件重测；六项执行值按 Founder 同日裁决定格：P-04 双问卷间隔隔夜且 ≥12h、P-03 `choices_frozen_at` 取两类问卷均提交后的较晚时刻、P-10 X/Y 标签与展示顺序两次独立随机（同种子派生互不相关子流）、P-12 商业问卷记 `decision_acceptance` / 制作问卷记 `content_adoption` / `edit_severity` 两侧各记取较严者且随本类问卷同时冻结、P-13 独立作答判据 = 作答制作问卷不调阅商业问卷 + 提交勾确认（记忆残留如实登记）、P-06 端到端证据目录 `acceptance/runs/<CASE_ID>/` 固定结构。`<thinking>` 剥离口径按预裁决⑤（允许并在匿名前整段剥离）并入该文件，两份 Prompt 与 `e2e_interaction_contract.md` §5 与之一致 | **已关闭**——B:997「裁判与匿名流程已确定」；B v0.4 + 《裁决台账》08-17「修复批次两裁决」行（OQ-BASELINE-06 / 08、OQ-ANON-01～14 全 ✅预裁决 08-17） |
| E2E 三份 Manifest 的两个合同版本字段与注释指针 | `acceptance/cases/E2E-01 / E2E-02 / E2E-03` 三份运行 Manifest 的 `e2e_interaction_contract_version` / `e2e_output_contract_version` 及 `baseline_prompt_versions` 两个子字段**实测已回填 `v1.0`**；原注释中的「合同文件尚不存在」叙述已改写为起草时的历史记录；按行号书写的 README 指针（`README.md:63`，行号随改版错位已成死指针）已于 2026-08-17 P0-1 收尾修复改为按小节名引用「§4 关闭记录表『共同外部交互/输出合同文件』两行」 | **已关闭**——字段值已回填；三份 E2E Manifest（E2E-01 / E2E-02 / E2E-03）与 `acceptance/cases/OPEN_QUESTIONS.md` OQ-E2E-01-04 / 02-04 / 03-04 依据列的 README 行号指针已同批改为按小节名引用（Manifest 与登记册属考卷区，由该区自身批次修订，**本目录文件不代改**） |

## 5. 相关文件

- `e2e_interaction_contract.md`｜B:995 三件套第 ① 件：两阶段共同交互合同
- `e2e_output_contract.md`｜B:995 三件套第 ② 件：共同输出合同（外部展示 Schema）
- `anonymity_procedure.md`｜B.2.5 匿名判分流程（含 §8 P-01～P-14 执行值）
- `generation_parameters.json`｜生成参数与模型身份的唯一真源（`generation_parameters_hash` 按其规范化 JSON 实时重算）；非合同文档，不计入 §1 六份
- `../README.md`｜contracts/ 总说明（考试条件区改动规则）
- `../schemas/case_manifest.schema.json`｜Case Manifest（B.2.1）
- `../schemas/business_decision_bundle.schema.json`｜笛语侧阶段 D 内部对象（A.6.2），**非**本目录的外部展示 Schema
- `contracts/` 下的 **OD-02 模型与参数定格记录**｜型号组合与定格程序（文件名随本修复批次由「提案」转「定格记录」，此处不写死路径）
- `../../B_三个核心模块智能验收合同.md`｜B.2 受控测试条件 / B.6.4 失败标签 / B.8 Gate IA-0
- `../../A_模块接口与核心数据字典.md`｜A.1.2 四类依据 / A.2.5 ConfidenceStatement / A.6 决策对象 / A.8 九部分交付包
- `../../PRD_笛语智能核_MVP_V3.0_v0.1.md`｜7.2 九部分必需结构 / 7.3 完整性与可用性
