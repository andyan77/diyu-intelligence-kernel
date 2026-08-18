# kernel/decision 上游语义缺口清单（开工令②：只登记，不代上游定义）

【M2-EP01 提前段·非正式证据】本清单登记 Decision 车道消费上游冻结接口时发现的语义缺口。
**本车道一律不代上游补定义**；每条注明缺口、当前处置、归属车道/裁决点。已有 OQ 编号的引用
既有登记，不重复立项。

| # | 缺口 | 本车道当前处置 | 归属 |
|---|---|---|---|
| 1 | **BD-D02 / BD-D03 无冻结 IntentExecutionPlan 夹具**（C.3 资产⑥、B.4 模块隔离要求"Business Decision 测试使用冻结的 IntentExecutionPlan"；考卷区当前只有 BD-D01 备有 `intent_execution_plan.frozen.json`） | 离线回放场景只覆盖 BD-D01；不为 D02/D03 手造上游 plan（造它 = 代上游定义 + 动考卷区） | 考卷侧批次（acceptance/，届时按 B.2.1 走版本流程） |
| 2 | ~~**快照双形状**~~ → **✅ 已随块 E 关闭（PR #15，本批合流适配）**：15 份快照迁 A.4.3 引用式，kernel/facts 提供官方消费通道。本模块按预案只改了 preprocess（load_snapshot = R1-R5/P2/P3 运行时谓词 fail-closed + materialize_legacy_view 内联兼容视图，与 kernel/intent 同款接线），断言口径零改动 | 已收敛：preprocess.py 诚实边界① | ✅（留痕防复读旧口径） |
| 3 | **ProductRole 五值判定条件未定义**（A.2.6 给了 HERO/SUPPORTING/TRAFFIC/PROFIT/CLEARANCE 枚举；知识提取 S03 把"角色词表正式定义与迁移"路由至 PCR-03 第 4 项，未裁决；卡内仅有主推/辅助/搭配三级阶梯，**不得冒充**五值判定条件） | 本模块只做枚举合法性 + 结构校验（postcheck D9）；角色归属按 MODEL_JUDGMENT 处理（带 rationale 与 trace），代码不发明判定规则 | PCR-03 第 4 项（Founder 裁决点） |
| 4 | **ProductFacts 版本语义**（原：M0 内联夹具无 version 字段，缺省取 1）→ 块 E 后快照 `product_facts_refs[].version` 已带真版本（BD-D01 = 1）；本模块 `product_ref.version` 仍写 1，与快照引用一致。**残留**：装配层未把 product_ref.version 与快照引用版本做程序化绑定（当前恰好同值），事实对象升版时须回此处接线 | 缺省 1 + 注释留痕（runner.assemble_candidate） | 事实对象首次升版时 |
| 5 | **规则集归属**（原：BD-D02/03 hard_rules 空、R-FB01-001 是否挂入待 OQ-BD-D02-04 / OQ-BD-D03-03）→ 块 E 后规则集由**快照 active_rule_refs 钉定**（A.4.3），本模块合流适配已改为只消费快照钉定集（BD-D01 = R-BDD01-001/002 两条，R-FB01-001 不在其列）。D02/03 快照的规则集取值仍属考卷侧/IA-0 既有 OQ | 规则池唯一来源 = 快照视图 hard_rules（preprocess 诚实边界④） | IA-0 既有 OQ，回填时不涉本模块代码 |
| 6 | **BLOCKED_FEWER_THAN_TWO 不得进入 DECISION_READY 的状态机执行面**（A.6.3 约束）：七状态机属 Runtime（A.4.4 / M3-EP02 核心对象，含 DecisionSelection A.6.4 的消费） | bundle 只如实给出三态与阻断诊断；状态迁移拦截与 DecisionSelection/ReviewRecord 消费**本段不建**（不加建：D §七 M2-EP01 未列，M3-EP02 已列） | kernel/runtime（M3-EP02） |
| 7 | **BD-D03 business_goal=PRODUCT_LAUNCH 为 inferred**（既有登记 OQ-BD-D03-02，快照 _fixture_note 自述待 IA-0 确认） | 本批未回放 D03，无消费动作；回放启动前以该 OQ 的裁决值为准 | IA-0 既有 OQ |
