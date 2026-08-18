# kernel/decision 上游语义缺口清单（开工令②：只登记，不代上游定义）

【M2-EP01 提前段·非正式证据】本清单登记 Decision 车道消费上游冻结接口时发现的语义缺口。
**本车道一律不代上游补定义**；每条注明缺口、当前处置、归属车道/裁决点。已有 OQ 编号的引用
既有登记，不重复立项。

| # | 缺口 | 本车道当前处置 | 归属 |
|---|---|---|---|
| 1 | **BD-D02 / BD-D03 无冻结 IntentExecutionPlan 夹具**（C.3 资产⑥、B.4 模块隔离要求"Business Decision 测试使用冻结的 IntentExecutionPlan"；考卷区当前只有 BD-D01 备有 `intent_execution_plan.frozen.json`） | 离线回放场景只覆盖 BD-D01；不为 D02/D03 手造上游 plan（造它 = 代上游定义 + 动考卷区） | 考卷侧批次（acceptance/，届时按 B.2.1 走版本流程） |
| 2 | **快照双形状**：考卷夹具快照为内联事实形状（`facts.*` 内嵌值），与 A.4.3 ContextSnapshot v2（引用容器形状，contracts/schemas/context_snapshot.schema.json）不合——BD-D01 夹具对该 Schema 校验 13 处 required 缺失（runtime_verified 2026-08-18）。台账挂起项「考卷夹具对齐新 Facts Schema」已登记该事实（方向=改夹具不改 Schema，须 Founder 批准） | preprocess.py 作唯一适配层消费内联形状（诚实边界①）；形状收敛后只改 preprocess，不动合同不动考卷 | 块 E 车道（快照与 Intent 输入路径改写）+ 台账挂起项 |
| 3 | **ProductRole 五值判定条件未定义**（A.2.6 给了 HERO/SUPPORTING/TRAFFIC/PROFIT/CLEARANCE 枚举；知识提取 S03 把"角色词表正式定义与迁移"路由至 PCR-03 第 4 项，未裁决；卡内仅有主推/辅助/搭配三级阶梯，**不得冒充**五值判定条件） | 本模块只做枚举合法性 + 结构校验（postcheck D9）；角色归属按 MODEL_JUDGMENT 处理（带 rationale 与 trace），代码不发明判定规则 | PCR-03 第 4 项（Founder 裁决点） |
| 4 | **ProductFacts 版本语义缺席**：M0 内联夹具商品无 version 字段，`product_ref.version` 取 1 属执行侧缺省口径（与 kernel/intent 对扁平夹具处理、考卷正样例 output_good.json 先例一致） | 缺省取 1 并在代码注释留痕；事实层 v2 对齐后由真版本号替换 | 块 E / 事实层对齐批次 |
| 5 | **BD-D02/03 hard_rules 空与 R-FB01-001 是否挂入**属改考卷（既有登记 OQ-BD-D02-04 / OQ-BD-D03-03） | 规则池一律读 contracts/rules/ 注册表（A.9.1 真源）+ 品牌过滤，不读快照内嵌 hard_rules 作为规则来源 | IA-0 既有 OQ，回填时不涉本模块代码 |
| 6 | **BLOCKED_FEWER_THAN_TWO 不得进入 DECISION_READY 的状态机执行面**（A.6.3 约束）：七状态机属 Runtime（A.4.4 / M3-EP02 核心对象，含 DecisionSelection A.6.4 的消费） | bundle 只如实给出三态与阻断诊断；状态迁移拦截与 DecisionSelection/ReviewRecord 消费**本段不建**（不加建：D §七 M2-EP01 未列，M3-EP02 已列） | kernel/runtime（M3-EP02） |
| 7 | **BD-D03 business_goal=PRODUCT_LAUNCH 为 inferred**（既有登记 OQ-BD-D03-02，快照 _fixture_note 自述待 IA-0 确认） | 本批未回放 D03，无消费动作；回放启动前以该 OQ 的裁决值为准 | IA-0 既有 OQ |
