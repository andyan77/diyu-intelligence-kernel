# contracts/interaction/｜两阶段交互合同与基线 Prompt

> 本目录承载 B.2.3 共同两阶段交互合同的**基线侧实体化文件**。
> 真源是 `B_三个核心模块智能验收合同.md`（v0.3，EFFECTIVE）。本目录所有文件只引用/照抄 B，不复述改写其语义。

## 1. 目录内容与真源对应关系

| 文件 | 承载什么 | 对应 B 条款 | 版本 | 状态 |
|---|---|---|---|---|
| `baseline_prompt_stage_D.md` | 基线侧**阶段 D（商业候选）**的 Prompt 全文、输入占位符契约、输出 JSON 字段合同、字段来源对照 | B.2.3 阶段 D 外部输出 Schema；B.2.4 基线定义与"不得故意写弱" | v0.1-draft | **PENDING_IA0** |
| `baseline_prompt_stage_C.md` | 基线侧**阶段 C（制作交付包）**的 Prompt 全文、输入占位符契约、九部分输出合同、字段来源对照 | B.2.3 阶段 C 九部分制作包 Schema + production_risks / assumptions / confidence；B.2.4 "阶段 C 只可接收本侧已经匿名冻结的候选选择" | v0.1-draft | **PENDING_IA0** |
| `README.md` | 本说明：三份文件的关系、版本口径、冻结纪律 | B.2.2 / B.2.3 / B.2.4；Gate IA-0（B.8） | v0.1-draft | **PENDING_IA0** |

本目录同时存在 `anonymity_procedure.md`（B.2.5 匿名判分流程，v0.1-draft / PENDING_IA0），由另一任务落盘，**不属本 README 所述三份文件**；其与本目录的衔接点是：阶段 D 输出交给它做匿名与选择冻结，冻结结果再回流为阶段 C 的 `{{selected_candidate}}`。以该文件自身声明为准，本 README 不复述其内容。

### 三条 B 条款各管什么

| 条款 | 管的事 | 在本目录如何落地 |
|---|---|---|
| **B.2.2「同条件」** | 两侧输入必须一致：同 Context Snapshot、同商品图片与其他输入材料、同业务任务、同硬规则、同最终输出合同、同模型供应商与基础模型版本、同生成参数与工具访问边界；不允许任一侧使用未声明的搜索或知识库；Brand Memory 启用状态与引用完全一致 | 两份 Prompt 的 **§2 输入占位符契约**：`{{context_snapshot}}` / `{{task_statement}}` / `{{hard_rules}}`（阶段 C 另加 `{{selected_candidate}}`）由 runner 逐字替换，不得改写摘要。模型与参数不写死在 Prompt 里，由 Case Manifest（B.2.1）记录。**Brand Memory**：B:95「首轮验收关闭 Brand Memory」，故两份 Prompt **不设 Brand Memory 输入通道**，基线侧不注入任何 Brand Memory 内容；启用状态与引用由 Case Manifest 的 `brand_memory_state` / `approved_brand_memory_refs` 记录（B:144-145；DISABLED 时引用列表必须为空，B:179）。**若后续转为 `APPROVED_SET`，必须先在两份 Prompt §2 增设与笛语侧完全一致的 Brand Memory 通道并同批升版，否则 B.2.2 该项不可证**（PENDING_IA0，OQ-BASELINE-17） |
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

- 本目录三份文件当前统一为 **v0.1-draft**，状态 **PENDING_IA0**。
- **draft 不得用于正式 A/B 取证。** 当前状态下运行只能作为工程联调，其结果不构成 B 意义上的验收证据。
- 冻结后：版本升为 `v1.0`，状态改为 `FROZEN`，并写入 Case Manifest 的
  `baseline_prompt_versions.decision_stage` / `baseline_prompt_versions.creative_stage`（B.2.1）。
- 两份 Prompt 内的 `PENDING_IA0` 标记逐条列在各自 §6「冻结前待办」，并各自带 `OQ-BASELINE-xx` 编号供中央待裁清单汇编引用；**全部关闭前不得改状态**。本目录不自建待裁登记文件。

## 3. IA-0 冻结纪律

Gate IA-0（B.8）要求「两阶段共同交互合同、输出合同和基线 Prompt 已冻结」。据此：

1. **冻结前**：本目录文件可自由修改，但每次修改须同步更新受影响文件的 §6 待办清单。
2. **冻结动作的前置 = Gate IA-0 三件套齐备**。B:992 要求的是**三件**：① 两阶段**共同交互合同**文件；② **共同输出合同**文件；③ **基线 Prompt**（本目录两份）。本目录当前只落盘了第 ③ 件，① ② 两件仍是 §4 的已知缺口。据此：
   - **§4 已知缺口表中「是否为 IA-0 冻结前置」列标「是」的行必须全部清零**；缺任一件，**不得执行冻结动作、不得把状态改为 `FROZEN`、不得宣告 IA-0 通过**；
   - 三件齐备且两份 Prompt §6 待办全部关闭后，才执行：Founder 签字 → 本目录三份文件同批升版 → 状态改 `FROZEN` → 写入 Case Manifest。
   - 注意区分两个「三」：**B:992 的三件套**是合同层面的三类文件；**本目录的三份文件**（§1 表格）只是其中第 ③ 件加本说明。二者不可互相顶替。
3. **冻结后的任何改动 = 改考试条件**（B.2.2「同条件」的一部分，见 `contracts/README.md`），必须同时满足：
   - **版本升级**（不得原地覆盖——B.2.1「确需修改时，必须升级案例版本并重新运行两侧」）；
   - **Founder 签字**；
   - **A/B 双侧回归重跑**——只重跑基线侧不成立，因为"同条件"是双侧共同属性；
   - 受影响案例的 Case Manifest 同步升版。
4. **绝对禁止**（B.2.1 / Gate IA-0 最后一条）：**不得在查看结果后修改**事实、裁判问题、允许答案、禁止结果或通过条件；不得依据已看到的结果反向修改本目录任何 Prompt。
5. IA-0 通过只表示**验收条件可以执行**，不表示能力已经成立（B.8）。

## 4. 已知缺口（本目录尚未入驻的文件）

| 缺口 | 说明 | 影响 | 是否为 IA-0 冻结前置 |
|---|---|---|---|
| 共同外部**交互**合同文件 | B.2.3 的外部交互口径目前只以「两份基线 Prompt 各自声明」的形式存在，尚无一份两侧共用的独立合同文件 | 两份 Prompt §5 中标 `PENDING_IA0` 的字段名（如阶段 D 承载四类依据的 `basis_entries`）必须与该共同合同对齐后才能冻结 | **是**——B:992 三件套之一（OQ-BASELINE-16） |
| 共同外部**输出**合同文件 | 阶段 D 外部 Schema 与阶段 C 九部分包 Schema 的两侧共用定义未单独落盘；`output_contract_version` 无取值来源 | 阶段 D 顶层 `risks` 与候选级 `risks` 的分工、全部引用字段书写形式、`output_contract_version` 都挂在这份文件上 | **是**——B:992 三件套之一（OQ-BASELINE-16 / 04 / 05 / 15） |
| 基线 Prompt（本目录两份） | 已落盘，状态 `PENDING_IA0`，§6 待办未清零 | 待办未清零即冻结 = 把未定条件冻死 | **是**——B:992 三件套之一，且需 §6 全部关闭 |
| 笛语侧对应文件 | 本目录当前只有基线侧 Prompt；笛语侧走模块编排，不使用 Prompt 文件，但其内部对象 → 外部展示 Schema 的转换器需可审计 | 影响 B.2.3「不能增加只对一侧可见的业务内容」的可验证性；顶层 `risks` 分工与 ref 书写形式必须与该转换器一次性定死 | 否——不属 B:992 三件套；但 OQ-BASELINE-04 / 05 关闭前，任何案例不得进入正式 A/B |
| 模型条件定格 | OD-02 厂商组合已裁决（台账 08-17），版本 / 参数于 IA-0 定格——本行指后者；正式版本 / 参数 / 基线 Prompt 冻结时一并经 Founder 签字（见《裁决台账》） | Case Manifest 的 `model_provider` / `model_name` / `model_version` / `generation_parameters_hash` 仍为空 | **是**——B:993「模型条件已确定」 |
| 裁判与匿名流程 | `anonymity_procedure.md` 已落盘（v0.1-draft / PENDING_IA0），由另一任务维护；本目录两份 Prompt 的 `<thinking>` 块剥离口径需并入该文件 | `<thinking>` 剥离范围与「不属 B.2.5 业务内容」的认定未确认前，两份 Prompt 的思考空间方案不生效 | **是**——B:994「裁判与匿名流程已确定」（OQ-BASELINE-06 / 08） |

## 5. 相关文件

- `../README.md`｜contracts/ 总说明（考试条件区改动规则）
- `../schemas/case_manifest.schema.json`｜Case Manifest（B.2.1）
- `../schemas/business_decision_bundle.schema.json`｜笛语侧阶段 D 内部对象（A.6.2），**非**本目录的外部展示 Schema
- `../../B_三个核心模块智能验收合同.md`｜B.2 受控测试条件 / B.8 Gate IA-0
- `../../A_模块接口与核心数据字典.md`｜A.1.2 四类依据 / A.2.5 ConfidenceStatement / A.6 决策对象 / A.8 九部分交付包
- `../../PRD_笛语智能核_MVP_V3.0_v0.1.md`｜7.2 九部分必需结构 / 7.3 完整性与可用性
