# C｜三个核心模块工程化落地与防死循环方案

## C.0 文档控制

| 项 | 值 |
|---|---|
| 版本 | v0.2（Founder 2026-08-16 采纳生效，见《裁决台账》08-16「工程化落地方案采纳」行；C.8 对抗审查否决清单 08-17 定案，执行侧不得重提） |
| 日期 | 2026-08-16 |
| 从属关系 | 本方案是**执行侧工程方案**，从属于 主 PRD / 附录 A / 附录 B；任何冲突以 PRD/A/B 为准 |
| 产出方式 | 4 个视角独立设计（评测工程 / 知识工程 / 架构落地 / 流程治理）→ 3 个对抗审查（过度工程化 / 冻结一致性 / 评测假绿）→ 人工综合裁决；关键事实已逐条对照 PRD/A/B 原文核验 |
| 定位 | 回答一个问题：**怎么把三份已冻结的合同文档，变成执行侧可以照着做、且做不出假绿、陷不进死循环的工程对象** |

### v0.1 → v0.2 修订记录

| # | 修订 | 依据 |
|---|---|---|
| 1 | 知识提取上游协议独立成 E 文档；C.4 / C.7 改为引用 E，不再自持口径 | Founder 采纳知识工程方法综合裁决 |
| 2 | 知识路由由"三去处"修正为"五去处"（补 Brand Memory 时序门与方法双路），定义权在 E.2 | 同上 |
| 3 | `acceptance/` 增加 `candidates/` 候选池（未来案例候选 + 知识卡队列） | E.3 / E.8 |
| 4 | coverage.py 规格边界固化（只汇总不推导 / 完整性仪表非能力证明 / 不建 UI 与库） | 同上 |
| 5 | Founder 周报增加知识卡池长度指标 | E.3 生命周期纪律 |

---

# C.1 总裁决：你缺的不是方法论，是"可执行形态"

你问"三个核心模块应该参考借鉴什么"。对照检查的结论是：**你要借鉴的方法论，已经全部写进 PRD/A/B 了**——

| 你想借鉴的领域 | 已有落点（真源） | 真正的缺口 |
|---|---|---|
| 专家系统 / 知识工程 → Decision Contract | 附录 A 已冻结（A.6 BusinessDecisionBundle、A.9 Rule / Trace / Review / Rework） | schema 还是"人读的 Markdown"，没有变成机器校验代码 |
| 案例驱动 CBR → Golden Dataset | 附录 B.4 十一条诊断案例 + B.5 三条 E2E = **14 条已冻结黄金案例** | 案例还没有可运行的执行文件和确定性断言 |
| LLM Evaluation → Evaluation Contract | 附录 B 整份就是（失败标签 B.6 / 闸门 IA-0~4 / 证据记录 B.10） | 没有 runner、没有检测器，"禁止结果"一条都还查不了 |
| 广告创意策略框架 | PRD 第 7 章九部分交付包 + A.7/A.8 | 缺分步编排实现 |
| 防死循环 | B.8.1 阻断解除三条路 + Rework Controller | **执行侧自身**（AI 编码代理改 prompt / 改代码这一层）还没有任何防死循环机制 |

所以本方案不再引入任何新方法论。全部内容只做一件事：

> **把"人读的合同"降解为"机器可执行的红绿灯"，并给执行侧套上物理上绕不过去的流程枷锁。**

一个类比：PRD/A/B 是《考试大纲》+《题库》+《评分细则》，都写好了；现在缺的是**考场**——答题卡机器、监考规则、防作弊摄像头。本方案就是考场施工图。

---

# C.2 仓库三区制：考卷、考生、考试条件物理隔离

```text
diyu-kernel/
├── contracts/            ← 考试条件区（改动 = 改考试条件，需版本升级 + A/B 双侧重跑）
│   ├── schemas/            A 附录 → JSON Schema（IntentExecutionPlan、BusinessDecisionBundle、
│   │                       九部分交付包、CaseManifest、AcceptanceEvidenceRecord…）
│   ├── rules/              已批准硬规则 RuleRecord（A.9.1）
│   └── interaction/        B.2.3 两阶段交互合同 + 冻结的基线 Prompt
│
├── kernel/               ← 考生区（唯一允许高频迭代的区域）
│   ├── intent/  decision/  creative/     每模块七类资产（见 C.3）
│   └── runtime/            薄 Runtime：七状态机、Artifact Reference、Rework Controller
│
├── acceptance/           ← 考卷区（改动需单独审批 + 案例版本升级）
│   ├── cases/              14 条案例的执行文件（只引用 B，不复述 B）
│   ├── detectors/          确定性断言 + 禁用表达词表
│   ├── judge/              trace_auditor 等探针 Prompt
│   ├── runs/               运行证据（AcceptanceEvidenceRecord 及引用产物）
│   ├── attempts/           尝试账本（见 C.6）
│   ├── locks/              熔断锁（见 C.6）
│   └── candidates/         未来案例候选池 + 知识卡队列（E 协议产物暂存区，升格走 E.8 窄门）
│
└── tools/                  runner、覆盖率统计、gate 脚本（约 5-6 个小脚本，不是平台）
```

**唯一的硬门（pre-commit，约 10 行 bash）**：

> 一个 commit **不得同时**修改 `kernel/`（考生）与 `acceptance/` 或 `contracts/`（考卷/考试条件）。

这是"改考卷过考试"的物理防线：AI 代理调 prompt 时顺手放宽断言、改 schema 下限，在文件系统层面直接做不到。

**为什么 `contracts/` 单独成区**：输出 Schema 同时是 B.2.2"同条件"定义的一部分——改它等于同时改笛语和基线两侧的考试条件，所以它既不属于可自由迭代的考生区，也不属于考卷区，改动必须版本升级并触发 B.9 的回归重跑。

---

# C.3 一个"智能模块" = 七类资产，不是一个 Prompt

防止"三个模块 = 三个 Prompt"的判定标准写在前面：

> **红线测试：删掉某模块的全部代码、只留下 prompt 文本，如果行为基本不变——它已经退化成 Prompt 套壳。**

每个模块目录必须包含七类资产：

| # | 资产 | 例（Business Decision） | 谁改得动 |
|---|---|---|---|
| 1 | 输入/输出 schema 引用 | 指向 `contracts/schemas/business_decision_bundle.json` | 版本升级流程 |
| 2 | 分步 prompt 链 | 冲突识别 → 候选生成 → 逐候选取舍，三个 prompt 文件 | **执行侧可高频改（唯一）** |
| 3 | 确定性前处理 | 从 ContextSnapshot 组装事实清单；missing_context 由 ContextRequirement（A.4.2）字段 diff 算出，**不交给 LLM 判断** | 代码评审 |
| 4 | 确定性后校验 | schema 校验、候选数下限、枚举合法性、数字溯源（输出里的数字必须在快照里找得到） | 代码评审 |
| 5 | Trace 组装 | FACT/RULE/ASSUMPTION/MODEL_JUDGMENT 四类分离（A.1.2）；**模型只许引用预物化的 FACT/RULE ID，不许自己新建** | 代码评审 |
| 6 | 冻结 fixtures | 上游模块的冻结输出（如 BD 测试用冻结 IntentExecutionPlan——对齐 B.4 模块隔离要求） | 案例版本流程 |
| 7 | 模块清单 manifest | 本模块当前 prompt 版本、schema 版本、分步结构——CaseManifest 里 `module_contract_versions` 的取值来源 | 自动生成 |

**分步裁决**（不是越细越好）：

- Intent：1 步 LLM + 确定性前后处理（missing_context 已被拿走，剩余任务单步可胜任）
- Business Decision：3 步 LLM（冲突识别 → 候选生成 → 逐候选取舍评估）+ 1 步确定性装配。拆开的理由：BD_CONFLICT_MISSED / BD_CANDIDATE_COLLAPSE / BD_TRADEOFF_MISSING 是三个独立失败标签，拆成三步后每个标签能定位到具体一步，调优不再是"重写整个大 prompt 碰运气"
- Creative：1 步策略承接 + 3 步资产生成（脚本/分镜/口播等分批），批间用确定性一致性检查抓 CR_CROSS_ARTIFACT_CONFLICT

---

# C.4 案例执行格式：三带式行为契约

每条案例一个目录（`acceptance/cases/BD-D01/`），核心是 `case.yaml` 的三带结构：

```yaml
case_id: BD-D01
contract_ref: B.4.2/BD-D01        # B 是唯一真源；本文件只引用，不复述 B 的原文
tier: core

must_hold:                        # 第一带：确定性断言（零模型调用，每次全跑，只判 FAIL）
  - {id: A1, check: schema_valid,       tag: SYS_SCHEMA_INVALID}
  - {id: A2, check: candidate_count,    args: {min: 2}, tag: BD_CANDIDATE_COLLAPSE}
  - {id: A3, check: tradeoff_nonempty,  tag: BD_TRADEOFF_MISSING}
  - {id: A4, check: trace_types_separated, tag: BD_TRACE_MIXED}
  - {id: A5, check: numeric_grounding,  args: {snapshot_fields: [inventory, price]}, tag: BD_FACT_FABRICATION}
  - {id: A6, check: human_gate_flag,    tag: BD_HUMAN_GATE_BYPASSED}

judge_probes:                     # 第二带：LLM 辅助探针（只出 CLEAN / SUSPECT / UNCLEAR，永不判 PASS）
  - id: J1
    ask: "两个候选的差异是否体现在商业机制/商品角色/叙事路径？还是只有标题与形容词不同？"
    verdict_enum: [CLEAN, SUSPECT, UNCLEAR]
    on: {SUSPECT: BD_CANDIDATE_COLLAPSE, UNCLEAR: ESCALATE}

human_questions:                  # 第三带：人工裁判问题（只写 B 的引用号，不重写问题）
  - {ref: B.4.2/BD-D01}
```

四条铁律：

1. **无检测器 → PENDING_HUMAN，绝不自动 PASS。** 每条 B 里的"禁止结果"必须在注册表里挂一个状态：`deterministic:<断言ID>` / `llm_assisted:<探针ID>` / `human_required` / `not_detectable_declared`（须写原因和 owner）。后两种状态下该项结果只能是 PENDING_HUMAN。runner 内所有安全判断用三态 `{true, false, unknown}`，unknown 一律向上冒泡，禁止任何 `default: false`。——这直接对应我们踩过的先例：无检测器却把 `fabricated_real_customer` 硬写 false = 假绿。
2. **分母永远由脚本实时统计，不许手工硬编码。** 本次三方独立数 B 的"禁止结果"条数，数出 47 / 53 / 58 三个不同值——这就是硬编码分母必错的实证。`tools/coverage.py` 每次从 B 原文现数。
3. **期望值写"路线无关必要条件"（answer_family invariants），不写标准文本**；且每条 invariant 必须挂到三带之一作为执行者——没有执行者的评分标准是装饰品。与历史 PASS 样例（exemplar）的相似度**禁止**作为评分依据；人工判分先独立判、后看 exemplar 校准，防止判准随系统输出漂移的棘轮效应。
4. **改案例 = 改考卷**：需 Founder 签字 + 案例版本升级 + 双侧重跑（B.2.1 / B.8.1 路径 2），且申请理由**不得引用"当前输出长什么样"**——时间序上先有案例修改理由、后看输出，堵死"补写案例合理化已有输出"的后门。
5. **案例细化、裁判问题、失败模式的上游来源走 E 协议**（出声思考会 + 临时知识卡 + 知识五去处路由，E.2-E.4）。特别地：**B.6 失败标签表是冻结的**——会议产出只能映射既有标签，覆盖不了的新失败模式走 B.8.1 版本升级提案，不得私加标签。

**coverage.py 规格边界**（防止它膨胀成新治理项目）：

- 四个视图 + 一个附加指标：维度视角（10 维度 × 落点案例）/ 案例视角（14 条 × 断言/探针/人工问题/状态）/ 禁止结果视角（live 分母 × 检测器四态）/ 闸门视角（IA-0~4 × 前置结果）/ 知识卡池长度（E.3）；
- 只读已有元数据、输出 Markdown/JSON 的小脚本——**不建 Web UI、不建数据库、不做趋势系统、不做自动通知**；
- **脚本只汇总，不推导**：案例自己声明所属维度、断言自己声明目标案例、Gate 自己声明前置案例；脚本不许"猜这条案例大概属于哪个维度"；
- 它是**完整性仪表，不是能力证明**——覆盖率 100% 不等于三个模块成功，能力成立只由 B.8 闸门判定。

---

# C.5 判分三层制

| 层 | 判什么 | 有权判 PASS？ | 成本 |
|---|---|---|---|
| L1 确定性程序 | Schema / 必填枚举 / 硬规则结构位 / 候选数 / 数字溯源 / Runtime 状态 / 成本延迟 | **只能判 FAIL**，不能判 PASS | 零 |
| L2 LLM 辅助 | 证据定位、失败标签建议、跨资产矛盾检测 | **永不**（输出只有 CLEAN/SUSPECT/UNCLEAR） | 低 |
| L3 人工裁判 | 冲突是否真实、候选是否实质差异、创意是否承接决策、能否开拍 | **唯一有权**（B.1.5 原文） | 高，需限流 |

L2 的四条降自由度机制（防"judge 自我循环"）：

1. **跨厂商强制**：`judge_provider ≠ model_provider`，runner 启动断言，不满足直接退出，不留"这次先将就"的口子（此配置校验失败按运行配置错误处理，**不占用** B.6 冻结标签 EVAL_CONDITION_MISMATCH 的语义）
2. **屏蔽自述理由**：judge 只看最终产物，不看系统自己写的推荐理由和 trace——模型会被自己的散文说服
3. **只问可证伪命题**：允许的句式只有三类——"文本中是否出现 X""A 处与 B 处是否矛盾""这句话能否在快照里找到出处"；"好不好/更专业吗"一律上交人类
4. **首建且只建 trace_auditor**：输入 = 快照 + 一条 FACT trace，输出 = GROUNDED / NOT_FOUND / CONTRADICTS + 出处引文。这是纯检索题，模型偏见影响最小、抓 BD_FACT_FABRICATION 价值最高。启用门槛：10 条人工样本（其中 3 条故意注入编造数字）必须 10/10 全中。

**Judge 校准集推迟建设**：等积累 ≥30 条人工已判的真实 run 之后再建（现在建只能造人工数据，且静态校准集会被 judge prompt 反复调到刚好过关——把校准集用成了训练集）。

---

# C.6 防死循环四件套（全部是"物理上做不到"，不是"要求自觉"）

## 1. 尝试账本（Attempt Ledger）

每次改 `kernel/` 里的 prompt/编排，必须先在 `acceptance/attempts/` 登记一条：

```yaml
attempt_id: ATT-0031
hypothesis: "候选取舍缺失是因为第3步prompt没有强制引用放弃方"   # 假设
target_failing_run: RUN-0088                                    # 必须指向真实存在的失败 run
regression_after: RUN-0092                                      # 改完跑回归的 run
delta: {fixed: [BD-D01/A3], broken: [], net: +1}                # 净变化
```

pre-commit 检查：`kernel/` 有改动而账本无新条目 → 拒绝提交。**没有失败 run 就不许改 prompt**——从机制上消灭"感觉可以更好"式的漂移调优。

## 2. 三轮熔断锁

同一案例、同一失败标签，连续 3 条 attempt 未修复 → 生成 `acceptance/locks/BD-D01.lock`，其后针对该案例的新 attempt 被 runner 直接拒绝。解锁只有三条路（对齐 B.8.1）：

- (a) 结构化修复：把"求模型做到"改成"机器保证"（加必填字段/拆步/加确定性断言）——**此类重构第一步 net=0 属正常，豁免死循环信号统计**；
- (b) 案例本身无效 → 案例版本升级流程（Founder 签字）；
- (c) Founder 裁决缩小能力范围（同步改 PRD/A/B）。

## 3. 考卷考生物理隔离

即 C.2 的 pre-commit 硬门 + C.4 铁律 4 的改考卷审批。**检测器代码（`acceptance/detectors/`）也在考卷区**——把 min_chars 从 30 改成 10、把候选数下限从 2 改成 1，同样是改考卷，同样需要审批。

## 4. 死循环信号与升级路径

| 信号 | 阈值 | 触发动作 |
|---|---|---|
| 净进展停滞 | 连续 3 条 attempt net ≤ 0（结构化重构豁免） | 停止调 prompt，进 Founder 裁决队列 |
| 翻烧饼 | 同一案例 修好→又坏→又修好 ≥ 2 轮 | 判定为合同/案例问题而非 prompt 问题，升级裁决 |
| 阻断标签存量不降 | 一票阻断标签（B.6 列表）存量连续 2 周不减 | 周报置顶，Founder 裁决是否缩范围 |

**采样口径统一裁决**：开放式生成三次跑出不同候选是常态，不是缺陷，**不设**"不一致即失败"的判定。日常迭代 n=1 控成本；Gate 正式验收跑 n=3，任何一次出现一票阻断标签即记该标签（就严不就宽），但 PASS 仍只能由 L3 人工判。

---

# C.7 Founder 驾驶舱（每周 ≤ 4 小时硬预算，三源合并后的唯一口径）

| 时段 | 内容 |
|---|---|
| 90 分钟 × 1 | 出声思考 / 判分校准会——**议程、八问、选题优先级、素材演进全部按 E 协议执行**（E.4-E.7；M0 以业务局面为主，有真输出后优先判实物） |
| 60 分钟 × 1 | 裁决队列：清 PENDING_HUMAN、批改考卷申请、解熔断锁 |
| 剩余 ≤ 90 分钟 | 机动（E2E 裁判、闸门签字） |

**你的一页周报（机器生成，不是执行侧写的散文）**：

```text
本周 attempt 数 / 净 delta（修复-新破坏）
一票阻断标签存量（逐条列，含在哪个案例）
禁止结果检测覆盖率（脚本实时统计，四种状态各占多少）
PENDING_HUMAN 队列长度 + 等你裁决的 N 件事
熔断锁清单
知识卡池长度（E.3 队列积压——持续增长不清空 = 经验库在偷偷生长的信号）
```

**你的"不做"清单**：不读 prompt diff、不看代码、不给"感觉不错/感觉不对"式反馈——所有反馈必须落到 B 的失败标签或裁判问题上。你看不懂代码没关系：**周报上这五个数字连续两周不动，就是执行侧在原地打转的铁证**，你据此触发 C.6 的升级路径即可。

另需提前启动的一件事（对抗审查抓出的"轻得危险"）：**Gate IA-3 需要"制作使用者确认至少一个完整包可以执行"、IA-4 需要商业+制作两类裁判**——摄影师/内容执行人员这个外部裁判有寻找和排期周期，必须当成有前置时间的交付物，建议 M1 期间就锁定人选（对应 OD-04）。

---

# C.8 对抗审查后被否决 / 降级的建议（附原因，防止后续被重新提出）

| 原建议 | 处置 | 原因 |
|---|---|---|
| 建"冲突原型库"（含典型解法路径）注入生成 prompt | **否决**，降级为验收侧案例设计分类学（只给出题人看，不给系统看） | 违反 B.1.4"先事实后经验"（等于未批准经验库），且使 E2E 同条件 A/B 失效 |
| ADVISORY 规则按 override 次数自动升降级 | **否决** | 触 PRD 2.5"不自动学习/自动改规则"红线；规则变更只能 Founder 显式批准 |
| 在冻结的 14 条外新增边界层/对抗层案例 14-18 条 | **降级** | B.11 明禁"数百条低价值案例"；对抗类只保留提示注入等安全冒烟检查，不计入能力证明 |
| "裸 LLM 基线也能过的案例，当周重写" | **修正** | 触 B.2.1"不得看结果后改通过条件"；改为标 `discriminative: false` 上报周报，走 B.8.1 路径 2（版本升级 + 双侧重跑） |
| 3 次采样不一致 → 判失败并作废 delta | **否决** | 开放式生成多样性是常态；且不得往 B.6 冻结标签表塞新语义。口径见 C.6 |
| 禁用表达词表命中 → 确定性一票阻断 | **修正** | 硬规则阻断是 Rule Engine 的职责（PRE-02，考生区内的产品能力）；验收侧词表只做嫌疑网——命中 → 人工确认后才定 SYS_RULE_VIOLATION，防词表假阳性误杀（"这件不便宜，但值"） |
| 第一周建 30 条 judge 校准集 | **推迟** | 尚无人工已判 run 可用；先建 trace_auditor（C.5） |
| 全量请求/响应 cassette 进 git | **降级** | B.10 只要求最小证据；git 只存 run 产物引用与 hash，原始大对象放本地运行目录 |
| 各视角合计 31 项"第一周动作" | **砍到 3 项**（见 C.9） | 对非技术创始人 + AI 代理团队超订约 4 倍，直接落地会拖垮 MVP 而不是保护它 |

---

# C.9 排期：第一周只做三件事

对齐 Gate IA-0（验收基线冻结）的准备工作：

1. **仓库三区骨架 + 隔离门**：建 C.2 目录结构 + 10 行 pre-commit + 把附录 A 的三个核心对象（IntentExecutionPlan、BusinessDecisionBundle、CaseManifest）转成 JSON Schema 并配校验脚本
2. **BD-D01 单条案例落地**：manifest + fixtures + 6-8 条确定性断言，然后**故意注错**（把候选砍到 1 个、把库存数字改成快照里没有的值），确认断言真的变红并报出正确的失败标签——"断言的断言"，这一步没做，后面全部绿灯都不可信
3. **检测覆盖率首版**：脚本实时统计 B 的"禁止结果"总条数，注册表先全标 `human_required`，跑出第一版诚实基线（预期覆盖率很难看，**难看是它的功能**——这是唯一一个团队越诚实数字越好看的指标）

第 2-4 周（对齐 M1 起步）：

- **空心骨架纵切**：零 LLM 调用，用假数据把 Intent→Decision→人工选择→Creative→九部分包 的状态机、schema 校验、Artifact 引用全线走通（PRE-07 系列检查的雏形）
- 然后按 **Decision 先行 → Intent → Creative** 逐段换真 LLM 调用（Decision 是价值核心和风险最大处，先证明它）
- 每落一个模块，跑通对应诊断案例的 L1 断言层

**前 4 周明确不做**（防执行侧自行加戏）：judge 校准集、Dify 编排、DOCX/PDF 导出、任何仪表盘 UI、E2E 正式 A/B（基线 Prompt 冻结即可，正式跑等 IA-1~3）。

---

# C.10 需要 Founder 裁决的事项（真正的开放问题，其余照本方案执行）

| # | 事项 | 关联 |
|---|---|---|
| 1 | OD-02：基础模型/版本/参数 + 两阶段基线 Prompt 冻结（M0 退出前必须裁决）。连带裁决：trace_auditor 跨厂商（系统侧用谁，auditor 就用另一家）——是否接受引入第二家模型供应商 | B.2.4、C.5 |
| 2 | `contracts/` 区改动的审批人是否 = Founder（改 schema 即改"同条件"，触发双侧重跑，成本高） | C.2、B.2.2 |
| 3 | 每周 4 小时驾驶舱预算是否可承诺；90 分钟出声思考会从哪周开始 | C.7 |
| 4 | C.8 否决/降级清单是否照准（照准后写入本文档 v1.0 冻结，执行侧不得重提） | C.8 |
| 5 | 制作侧裁判（摄影师/内容执行）人选启动时间（OD-04 的前置） | C.7、Gate IA-3/4 |
