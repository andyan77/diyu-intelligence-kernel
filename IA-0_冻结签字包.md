# IA-0 冻结签字包

| 项 | 值 |
|---|---|
| 文档编号 | DIYU-MVP-V3-IA0-SIGN |
| 版本 | v1.0 |
| 状态 | EFFECTIVE（已生效；Founder（Faye）重签 2026-08-18T02:39:10+08:00，M0 收口修复批次 P0-6，回执《M0收口回执.md》@24e24a3） |
| 性质 | IA-0 已定格考试规则的权威转录 + 签字批次记录（不承载施工流程） |
| 修订记录 | v0.1 起草（2026-08-17 M0-EP02 建设轮）→ v1.0 内容定稿（2026-08-17 M0 收口修复批次） |

> 给 Founder 的一页话：这一包只记两件事——IA-0 已经定格的全部考试规则（§一~§五），以及签字批次事实（§六）。
> 2026-08-17T19:08:38+08:00 的首签是历史事实，**该次 M0 收口宣告已于同日撤回**（外部审查判 BLOCK，见《裁决台账》08-17「M0 收口宣告撤回」行）；重签见《M0收口修复批次_执行规格.md》P0-6。

## 一、定格结果（IA-0 冻结的考试规则，本节为唯一权威转录）

| 项 | 定格值 | 真源 |
|---|---|---|
| A/B 主模型（笛语侧与基线侧同用） | qwen3-max-2026-01-23（快照版；2026-08-18 真实调用回执，OD-02 v1.1 §四。原定格 qwen-max-0107 实测不可调用，Founder 2026-08-18 块 0 裁决替换并于同日级联落地 20 份 Manifest 与参数真源 v1.1） | 台账 08-17「IA-0 冻结签字生效」行；contracts/OD-02_模型与参数定格记录.md §一 |
| 多模态（商品图 VisualProfile） | qwen-vl-max（无快照版：锁别名，逐次运行留存接口返回的实际 model 回执） | contracts/interaction/generation_parameters.json |
| trace_auditor / L2 探针 | deepseek-v4-pro（跨厂商审计侧，非 A/B 参赛方） | contracts/interaction/generation_parameters.json |
| 生成参数 | temperature 0.3｜top_p 0.8｜seed 20260817｜max_tokens 阶段 D 4096 / 阶段 C 8192｜输出语言 zh-CN | contracts/interaction/generation_parameters.json |
| 合同批次 | contracts/interaction/ 六份 .md 合同文件（README / anonymity_procedure / baseline_prompt_stage_C / baseline_prompt_stage_D / e2e_interaction_contract / e2e_output_contract）v1.0 CONTENT-FROZEN（内容定稿；生效随 P0-6 重签） | contracts/interaction/ |

型号与参数的唯一真源是 `contracts/interaction/generation_parameters.json`（该文件自述为 `generation_parameters_hash` 唯一真源）；本表为其只读转录，冲突以 json 为准。
运行前补填的构建版本类 4 项字段按 §五 双模式纪律于每次运行前补填并过运行态门。

## 二、冻结资产清单

| 资产 | 位置 | 状态 |
|---|---|---|
| 14 条案例 → **20 份运行 Manifest**（一变体一份：INT-D01×2、INT-D02×2、INT-D03×2、CR-D01×2、CR-D04×3） | acceptance/cases/*/manifest*.yaml | 已定格；经 25 blocker + 41 minor 对抗修复；Schema 全绿回执按修复批次 P0-4 用当前 HEAD 重跑后回填（带 commit SHA + Python 版本 + 执行命令） |
| 两阶段基线 Prompt（诚实写强，B.2.4 零重试口径） | contracts/interaction/baseline_prompt_stage_D.md、baseline_prompt_stage_C.md | v1.0 CONTENT-FROZEN |
| 匿名判分流程（含 B.5.2 双窗口、B.2.5 六项逐项留档清单、P-01~P-14 裁决值） | contracts/interaction/anonymity_procedure.md | v1.0 CONTENT-FROZEN |
| 共同两阶段交互合同 / 共同输出合同 | contracts/interaction/e2e_interaction_contract.md、e2e_output_contract.md | v1.0 CONTENT-FROZEN |
| OD-02 模型与参数定格记录（角色分配 + 生成参数 + 定格执行留痕） | contracts/OD-02_模型与参数定格记录.md | v1.0 CONTENT-FROZEN |
| 规则注册表首批 3 条 | contracts/rules/R-BDD01-001.yaml、R-BDD01-002.yaml、R-FB01-001.yaml | 已落盘 |
| 待裁项中央登记册（**主册 97 条 + 建设轮 OQ-BUILD 14 条 = 111 条**，编号可追溯到每份文件） | acceptance/cases/OPEN_QUESTIONS.md | 主册 97/97 已裁决（2026-08-17 预裁决批次 + M0 收口修复批次两裁决关闭）；OQ-BUILD 14 条另表，逐条关闭状态见该文件「建设轮新增待裁项」表的「关闭状态」列（其中 OQ-BUILD-06/12/14 为建设队列类，转 M1+ 执行） |

## 三、A 类裁决结果（Founder 2026-08-17 整体按推荐）

| 主题 | 裁决结论 | 落盘位置 |
|---|---|---|
| 1. 每场考试用什么模式跑（快速/增强） | 模式原则＝「考追问才开增强」；增强侧 INT-D01 主跑 + INT-D02 增强变体，其余全 QUICK；INT-D01 另补 QUICK 变体 → 总 20 份运行 Manifest | OPEN_QUESTIONS.md 文首①；台账 08-17「IA-0 预裁决」行 |
| 2. 四个案例缺「考题原句」（BD-D01/BD-D02/CR-D03/E2E-01） | 四句考题定稿，已回填对应 Manifest | OPEN_QUESTIONS.md 文首②；对应 Manifest 的 task_statement |
| 3. 品牌禁语是否立正式硬规则对象、BD-D01「一组规则」几条 | 品牌禁语立 RuleRecord R-FB01-001（词表以 detectors 为唯一运营真源）；BD-D01「一组规则」＝现有 2 条（R-BDD01-001/002） | OPEN_QUESTIONS.md 文首③；contracts/rules/ |
| 4. 基线侧失败要不要重试 | 基线零重试维持，B 合同不动；整场对称重跑合法 | OPEN_QUESTIONS.md 文首④ |
| 5. 模型让不让「打草稿」 | 允许 `<thinking>` 块，匿名化前整段剥离 | OPEN_QUESTIONS.md 文首⑤；anonymity_procedure.md §8 P-14 |
| 6. 匿名流程人选与细则（P-01~P-14） | 三关键定格：脚本随机 + 密封文件 + git 哈希封存 / 阶段 D 与终审独立随机 / 揭盲后禁回改。其余执行值与违规标签由 M0 收口修复批次两裁决补齐：B v0.4 新增失败标签 EVAL_BLINDING_PROCEDURE_INVALID（一枚关闭 P-05/P-08/P-11，后果＝该次盲测作废、不算 IA-4 证据、按 B.8.1 修复后重测）+ 六执行值（P-04 隔夜且≥12h／P-03 取两类问卷较晚时刻／P-10 两次独立随机／P-12 三组记录归属与冻结时点／P-13 独立作答判据／P-06 证据目录结构） | OPEN_QUESTIONS.md 文首⑥；台账 08-17「修复批次两裁决」行；anonymity_procedure.md v1.0 §8 |
| 7. PRD 与 A 的口播包「情绪」字段分歧 | A 合同 v0.1→v0.2：VoicePackage 补 `emotion`（情绪）字段，对齐 PRD 7.2 | OPEN_QUESTIONS.md 文首⑦；A_模块接口与核心数据字典.md |
| 8. OD-02 定格 | 已定格并经 2026-08-18 v1.1 修订：qwen3-max-2026-01-23 两侧同用（原 qwen-max-0107 实测不可调用，块 0 裁决替换）/ qwen-vl-max 锁别名 / 审计 deepseek-v4-pro；参数真源 contracts/interaction/generation_parameters.json（值见 §一） | contracts/OD-02_模型与参数定格记录.md §一§二；台账 08-17 |

执行侧自决项（同批登记，不占 Founder 时间）：hash=sha256 规范化 JSON、Schema 补版本戳、PENDING 冻结断言门、运行顺序记 run 证据层、allowed_tools 空＝零外部工具（内部编排豁免 B.2.2）、Persona 冻结落点＝快照内容。落盘见 OPEN_QUESTIONS.md 文首。

## 四、B 类｜执行侧建设项（已交付）

- ✅ Context Snapshot 夹具全部落盘（照抄审计逐字命中《衡叙集》夹具数据包）+ `snapshot_hash` 算法定格；**20 份 Manifest 的 `snapshot_hash` 已全量回填**（20 = Manifest 份数，见 §五「齐套」）。夹具本身的目录数与快照 JSON 份数**不写记忆值**，以 P0-4 重跑脚本对 `acceptance/cases/*/fixtures/` 的实测输出为准
- ✅ 共同两阶段交互合同、共同输出合同两份文件落盘（补齐 B:995 三件套缺其二）+ 笛语侧转换器 ref/risks 分工对齐 → `contracts/interaction/e2e_interaction_contract.md`、`contracts/interaction/e2e_output_contract.md`
- ✅ contracts/rules/ RuleRecord 注册表首批落盘（品牌禁语 → R-FB01-001；BD-D01 → R-BDD01-001/002）
- ✅ 冻结断言门实现 → `tools/freeze_gate.py`（真实口径见 §五）。**R1–R13 十三条红线已交付**（逐条定义见该文件头部；含 §五曾列为待建的四项：`PENDING_IA0` 扫描 = R11 面一、份数机器断言 = R1 声明份数自校验、参数文件哈希实时重算 = R8、真源正文 digest 校验 = R10）。活体证据 → `tools/test_freeze_gate_mutations.py`：22 项负向变异逐条实测门必须转红 + 未变异副本送签态判绿 / 运行态只红设计内三条。**仍未取得活体证据的是 R5 / R6 / R7 三条**（见 §五末条），不得据「十三条已交付」读成「十三条已验证」
- ✅ 齐套口径登记（定义见 §五）

## 五、齐套与冻结判据（单义定义，供机器断言引用）

- **齐套**＝14 案例 ↔ **20 份**运行 Manifest（多输入/双模式案例一变体一份），缺任一变体不得计齐套。
- **冻结态**由三者共同表达：正式资产名（无 `.draft`）+ 冻结门 GATE_GREEN 回执（带 commit SHA）+ 台账签字行。**不再由文件名单独承载。**
- **冻结门双模式真实口径**（`tools/freeze_gate.py`，Founder 2026-08-17 批准，属改考卷）：
  - **送签态**（`--mode=sign`）仅豁免 4 个运行前补填的构建版本类字段，且取值必须**恰为** `PENDING_BUILD`——`diyu_build_version`、`module_contract_versions.intent`、`module_contract_versions.business_decision`、`module_contract_versions.creative`；任何其他占位或空值仍判红。
  - **运行态**（默认，无参数）不豁免，运行前全查。
  - **✅ 已实现（现时态；截至 M0 收口修复批次 P0-2 修复轮）**：
    - **齐套份数机器断言**（原 P0-2 待建项，本行已可改为现时态）：`tools/freeze_gate.py` 的 R1 除比对脚本常量 `EXPECTED_MANIFESTS=20` 外，另实时解析**三处书面声明**——本节上面那句「齐套」定义、`acceptance/cases/OPEN_QUESTIONS.md` 文首预裁决①、`contracts/OD-02_模型与参数定格记录.md` §三第 2 条——任一处与常量对不上即 GATE_RED（检测器 `check_declared_counts`；负向变异 M18 实测：把本节声明改成 21 份而常量不动 → 门转红）。原「R1 比对的是脚本常量、不是解析出的声明份数」这条缺口就此关闭：常量与真源必须同批改，门不替任何一方拍板。
    - **`PENDING_IA0` 扫描**（原 P0-2 待建项）：R11 面一，扫描面 = `contracts/**` 全部文件 + `acceptance/cases/**` 整棵（Manifest / `case.yaml` / fixtures / 登记册）+ 两份根级冻结声明，**两模式同红**。引述历史状态时用反引号整体包裹（`` `PENDING_IA0` ``）按引述放行，裸标记判红——引述豁免是机器可判的约定，不是把某份文件排除出扫描面的后门。
    - **冻结件正文保护**：`contracts/interaction/` 七份自述 CONTENT-FROZEN 的文件已纳入 `contracts/frozen_digests.json`，受 R10 同款校验（正文字节 digest + 声明版本 + `version_history` 链）。此前它们只有「一行版本号」被读过，正文可被整体改写/掏空而门仍绿（负向变异 M15 即该路径，现已转红）。
  - **✅ 原「仍未取得活体证据」两条已关闭（现时态；截至块 A / 块 E，2026-08-18）**：
    - ~~R5 / R6 / R7 尚无负向变异覆盖~~ → 块 A M21-M24 补齐活体证据（R5 值校验 / 规则正文冻结 / R6 内容绑定 / R7 版本指针），十三条红线现均持至少一条变异活体证据；
    - ~~运行态表现按同一实现推断、未逐条实测~~ → 块 E Z-12 运行态横扫：全部送签态 RED 变异在运行态逐条复测命中被测红线（tools/test_freeze_gate_mutations.py Z12 段）；
  - **⛔ 仍如实保留的诚实边界**：
    - `version_history` 链的诚实边界见 `contracts/frozen_digests.json` 的 `_chain_algorithm`：它把「顺手把门弄绿」抬成「显式重写冻结历史」，**不等于**正文不可篡改。
- **签字动作定义（B.2.1）**：A 类裁决逐项落盘 → B 类建设项交付 → 冻结门（送签模式）GATE_GREEN → 20 份 Manifest 写入 `approved_by` / `approved_at` → 台账登记。

## 六、签字记录（批准行；只增不改）

| 批次 | 签字人 | 时间 | 覆盖 | 当前效力 |
|---|---|---|---|---|
| IA-0 首签 | Founder（Faye） | 2026-08-17T19:08:38+08:00 | 20 份 Manifest 的 `approved_by` / `approved_at` | 该次收口宣告已于同日撤回（外部审查 BLOCK，台账 08-17）；签字记录保留为历史事实，不再作为 M0 收口依据 |
| IA-0 重签 | Founder（Faye） | 2026-08-18T02:39:10+08:00 | 修复批次六项 BLOCK 全关闭后的最终资产（受审树 24e24a3，回执《M0收口回执.md》） | ✅ 生效；20 份 Manifest approved_at 同批回填 |
| 主模型级联补签 | Founder（Faye） | 2026-08-18T15:19:52+08:00 | 20 份 Manifest（model 两字段/case_version/构建版本字段升版后全量）+ generation_parameters.json v1.1 + 本签字包刷新行 | 现行有效（与 P0-6 重签共同构成在案签字链） |
| 内容真实性三层边界（块 C）签字 | Founder（Faye） | 2026-08-18T16:04:02+08:00 | 20 份 Manifest（块 C 四版本指针 PRD v0.2 / A v0.3 / B v0.5 / creative_stage v1.1 + case_version 升格后全量；B v0.5、A v0.3、PRD v0.2、baseline_C v1.1 四份修订随本批生效）；Founder 本轮批复原文「确认签字」 | 现行有效（签字提交只动 20 行 approved_at，内容指纹由门 R6 实时核验） |
