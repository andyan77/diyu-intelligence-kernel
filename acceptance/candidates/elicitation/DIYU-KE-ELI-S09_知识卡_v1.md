# DIYU-KE-ELI-S09｜资产收口与入库治理 正式入库知识卡

```yaml
session_id: DIYU-KE-S09-20260817-001
round_covered: S09-R01（资产收口，三位专家已答且 Founder 批准）
round_not_covered: S09-R00（E2E 匿名判分材料准入，状态 MATERIAL_NOT_READY，未开始，不产知识卡）
source_files:
  - S-09.txt（S09-R01 提问卡）
  - S-09.md（三位专家回答：专家一散文体、专家二 CANDIDATE_RESPONSE、专家三 REVIEW_SUMMARY＋CANDIDATE_RESPONSE）
  - DIYU-KE-S01-S08集中收口与追问包_v1.txt（S09 准入条件与队列路由）
ruling_basis: Founder（Faye）2026-08-17 裁决"S09 的问题和专家回答，我也确认通过"，整体批准、无逐条改写
compiled_by: 主持人 Claude，按《E_领域专家知识提取协议》E.3 转换
compiled_on: 2026-08-17
cards_total: 16
cards_routed: 13
cards_pending: 3
```

> 编译约定：本文件在 E.3 原版 schema 上扩展 `source_round` / `provenance` / `source_ref` 三个字段以满足会议协议的来源纪律；本场无 Founder 逐条改写，全部卡 provenance 为 AI_PROPOSAL_FOUNDER_APPROVED。所有卡均为候选，正式生效须另走批准流程。

---

## 一、入库知识卡（ROUTED）

```yaml
elicitation_item_id: ELI-0901
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "S01–S08 产出收口，判断什么有资格进入候选资产库"
expert_statement: "候选资产入库须全过五条检验：①变量化（把具体商品/人物换成占位符后规则仍完整成立）；②反事实稳定（单变量追问下规则本身不需改写，变的只是应用结果）；③可判定（两个不同执行者按它得出同一判定）；④失败模式已命名（规则知道自己在防什么）；⑤不依赖未裁决前提。每条检验对应它防的一种收口失败（案例走私／未收敛提前入库／口号规则／不知守什么／依赖悬空）。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "任何候选资产（方法/规则/判卷/案例）申请进入候选资产库时"
does_not_apply_when: "案例经验的存放（案例本就不通过变量化检验，走 ELI-0910 的 CASE_SCOPED 通道）"
counterexample: "'内容要真实'——无判定形式、无失败模式，五条不过，属口号，不得入库"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三（五条检验及逐条防守目标）；专家一'三条件'、专家二 Step1–4 为相容子集"
```

```yaml
elicitation_item_id: ELI-0902
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "同上"
expert_statement: "S01–S08 产出分四个流向，每件只有一个去向：方法模块（运行时自动执行）／判卷检验（产出后跑、可容人终审）／人工决策边界（库里存'此处必须停下问人'这条元规则本身）／案例经验（正确但绑定品类、平台、团队或数字，标 CASE_SCOPED 存放）。口诀：规则进 Core，数值进案例，检验进判卷，选择留给人。双挂只允许一种情形：方法与检验是同一规则的执行态与审计态（如声画同证既是拍摄纪律又是抽查项）。"
statement_type: METHOD
applies_when: "对提取产出做资产分拣时"
does_not_apply_when: "尚未通过 ELI-0901 五条检验的原始陈述（先检验后分拣）"
counterexample: "'都很重要、两边都放'——即本场提问卡明令禁止的回答方式"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家二 §1 分拣表＋专家三 §1（含双挂唯一例外）；专家一四分类（资产库/案例/人工）同构"
```

```yaml
elicitation_item_id: ELI-0903
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "同上"
expert_statement: "统一资产路由程序：先把每条结论拆成已知事实／判断方法／条件化规则／专业评价／最终业务选择／案例结果六种成分 → 单变量反事实检查（方法是否稳定、结果是否按预期改变）→ 删除具体商品、数量、人物、台词、时长后检查剩余结构是否仍成立 → 能被明确事实机械判定的进硬规则候选，有评价维度但阈值不确定的进判卷校准，涉及价值选择或授权的留人工。"
statement_type: METHOD
applies_when: "每条候选陈述入库前的成分分离与定性"
does_not_apply_when: null
counterexample: "将 S01–S08 完整回答原样写入 Core——方法、案例结论、假设和临时措辞没有分离（专家二 forbidden_outcome）"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家二 §2 Step1–4 与 §10 possible_module_method"
```

```yaml
elicitation_item_id: ELI-0904
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "一个判断在多个案例中成立，但仍依赖 Founder 专业经验才能确认，应归入哪里"
expert_statement: "按'人贡献的是什么'分流，三种情形三个归属：人确认的是判定结果（规则给出候选判定、人核可或否决）→ 判卷检验（默认落点，最常见）；人确认的是选择本身（规则只能摆选项与代价，选哪个无客观对错）→ 人工决策边界；人补的是规则缺口（检验还没有可判定形式，补上就不再需要人）→ 方法模块候补，补齐判定形式后转正。多次成立只能证明它值得候选化，不能证明它已是无例外硬规则。"
statement_type: METHOD
applies_when: "'多案例成立但仍需人'的争议件归属判定"
does_not_apply_when: null
counterexample: "因'多个案例都成立'直接升级为自动执行的 Core 结论"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三 §6-A（三分流程序）；专家一'人工决策边界为主、Judge Calibration 辅助'与专家二'步骤进 Core、维度进判卷、取舍留人'为相容表述"
```

```yaml
elicitation_item_id: ELI-0905
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "案例经验何时有资格成为候选规则"
expert_statement: "案例经验→候选规则的最低条件（三位专家合并版）：①能从具体商品和人物中抽象出来（变量化成立）；②在至少两个实质不同的案例或反事实中结论保持（单案不提炼——本系列的单变量反事实追问就是在制造第二案例）；③明确适用范围、触发条件、允许结果和禁止结果；④有可判定检验＋已命名失败模式，且反例能说明边界；⑤不依赖未提供的品牌/商品/库存/经营事实、不依赖未裁决前提，违反后能说明具体业务损害；⑥不存在未处理的合法替代方案；⑦经 Founder 审阅立为候选。"
statement_type: BOUNDARY
applies_when: "任何案例级结论申请提炼为候选规则时"
does_not_apply_when: "候选规则→正式规则（另见 ELI-0906，门槛更高）"
counterexample: "把'这个案例算三套'写成'所有外套增减都算新穿搭'——案例结果错误扩大为行业规则"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家一追问2（七条）＋专家二 §7 案例→候选（七条）＋专家三 §6-B 案例→候选（五条），取并集去重"
```

```yaml
elicitation_item_id: ELI-0906
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "候选规则何时可以正式生效"
expert_statement: "候选规则→正式规则的升格条件：①在匿名真实输出上经受 S08 式判分，与 Founder 判定一致；②双向命中——'规则拦下、人也认为该拦'与'规则放行、人也认为该放'各至少一次（只在一个方向被验证的规则可能只是恒真或恒假的摆设）；③适用边界与例外成文（何时不适用）；④配套失败标签与豁免路径（豁免权归 Founder）；⑤与 PRD、附录 A/B 及模块权限一致、不与其他正式规则冲突；⑥Founder 或授权裁决人正式批准；⑦版本化（生效日期、适用模块、复审触发条件）。单一案例可以产生候选规则，但不能直接产生正式规则。"
statement_type: BOUNDARY
applies_when: "候选规则申请转正时（E.8 窄门的具体化）"
does_not_apply_when: null
counterexample: "恒否规则在拦截方向永远'命中'，但错杀代价从未被测过——单向验证升格即此失败"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三 §6-B 候选→正式（五条，双向命中为其独有贡献）＋专家二 §7 候选→正式（八条），合并去重"
```

```yaml
elicitation_item_id: ELI-0907
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "自动化检验与人工豁免的权限边界"
expert_statement: "单向自动化元规则：机器可以拦，不能放——检验有权自动阻止发布，豁免权永在 Founder。检验可以自动说'不'，永远不能自动说'没关系'。拦错的代价是慢，放错的代价是假——不对称的代价要求不对称的权限。"
statement_type: HARD_RULE_CANDIDATE
applies_when: "任何自动化检验（发布拦截、质量门禁、判卷检验）的权限设计"
does_not_apply_when: null
counterexample: "豁免权下放——把'机器可拦'悄悄升级成'机器可放'（专家三 forbidden_outcome）"
candidate_destination: RULE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三（REVIEW_SUMMARY 核心结论3＋§6-C 配套元规则）；与专家一/二的人工裁决清单方向一致"
```

```yaml
elicitation_item_id: ELI-0908
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "S01–S08 中哪些判断必须永久保持 HUMAN_DECISION_REQUIRED"
expert_statement: "必须保持人工裁决的判据：凡是价值函数本身（不是价值函数的应用）——正确性不由事实与规则闭合，而由品牌的偏好、风险胃口与处境决定；涉及品牌责任、真实性、合规、多目标取舍或最终商业责任。清单（三位专家合并）：主推款最终决定；品牌禁用词未确认时的发布；创始人出镜内容真实性与个人经历授权；多目标冲突优先级排序；视觉普通是否升级为商业否决；实拍素材是否真正达到'让顾客看懂'；收集更多个人信息是否值得（顾客摩擦/隐私责任/商业价值权衡）；授权情形下默认策略的内容与锚点；'行'能否把 ASSUMED 升为 CONFIRMED 的语义；品牌表达边界松紧与'冲击力'分寸；成功的数量定义（永远是品牌的数字）；讲述者镜头适性终审与情绪剪辑尺度；旧成品处置与战役时序；发布拦截的豁免；判分维度册发放时机与所有升格裁决。系统能做到的极限是把选项、代价、风险摆到最清楚，然后停下。"
statement_type: BOUNDARY
applies_when: "上述任一局面出现时，系统只能推荐并停止（HUMAN_DECISION_REQUIRED），不得自动决定"
does_not_apply_when: "价值函数的应用（既定规则在明确事实上的执行）——可自动"
counterexample: "系统因库存深或毛利好自动把商品定为主推款；因创始人本人出镜就自动认定内容可靠"
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家一 §四（六项）＋专家二 §8（九项）＋专家三 §6-C（八项），并集去重；判据句取专家三，理由句取专家一"
```

```yaml
elicitation_item_id: ELI-0909
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "哪些内容应作为判卷检验（产出后运行、可容人终审）"
expert_statement: "判卷检验主题清单：画面是否足以让顾客看懂商品（轮廓/结构/细节/上身/动态/真实呈现）；缺失属阻断还是质量下降（删除相关声明后核心结果是否仍成立）；商品是否值得重点推动（多项证据权重不能全局固定）；两个穿搭是否真正不同（灰区存在）；真人表达是否可信（讲述者/经历/事实/语言一致性）；制作包是否真正可执行（普通人员能否无额外会议完成）；局部修改还是商业返工（名义相同的入口实际摩擦差异）；Hook 是否被兑现（需理解整条内容而非单句匹配）。具体检验工具：排除力/新信息/事实溯源三检验；声画同证抽查＋镜头诚实三条件；换商品测验＋复述测验；五步成交说服链逐步指认＋四点一线；ASSUMPTION 块三要素审查；黑名单零出现三查；本人认可测验——注意它天然需要讲述者本人参与，是'带人检验'，不可全自动。"
statement_type: METHOD
applies_when: "对模块产出做发布前/判分时检验"
does_not_apply_when: "把这些检验当作运行时自动放行依据（放行权限见 ELI-0907）"
counterexample: null
candidate_destination: JUDGE_QUESTION
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家二 §5-B 八项判卷主题＋专家三 §1-二 检验工具清单，合并；各工具的本体卡在对应场次 ELI 文件"
```

```yaml
elicitation_item_id: ELI-0910
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "哪些正确结论只能作为案例经验保留"
expert_statement: "案例经验保留原则：结论正确但绑定具体商品、品牌、库存、任务条件、团队或平台的，标 CASE_SCOPED 存放，不进通用 Core；案例经验不是垃圾，是没到提炼温度的原料——等第二、三个异质案例出现再启动提炼（≥2 个实质不同案例才提炼）。本系列 CASE_SCOPED 清单：具体缺失项在本任务的 QUALITY_REDUCING 等级（目标改成'本周成交'即翻转）；800 件库存六周激活暂不定主推的结论；三个组合算三套的具体结论；'这条创始人现场介绍可以发布'的具体判断；三十分钟拍摄的具体分镜与 10 分钟保底清单；小程序表单只做局部修改的具体结论；大衣底线三件画面集（品类绑定，换成鞋就散架）；2–3 套上限数字；竖屏与全程字幕（平台惯例会漂移，进平台档案并配维护机制）；'店长开场＝顾客三问'（案例级最优解）。"
statement_type: BOUNDARY
applies_when: "分拣时识别出绑定具体条件的结论"
does_not_apply_when: "已通过变量化检验的方法结构（进 Core，见 ELI-0901）"
counterexample: "大衣三件套写成全品类规则——在下一个品类上第一次应用即出错，且带着'已入库'的权威出错"
candidate_destination: CASE_CANDIDATE
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家一 §三（六条）＋专家二 §5-C＋专家三 §1-四（含'提炼温度'机制），并集"
```

```yaml
elicitation_item_id: ELI-0911
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "S01–S08 案例材料的保存形态"
expert_statement: "S01–S08 案例应保留为一组相互关联的正例、反例和单变量边界案例，不应拆散后丢失反事实关系。"
statement_type: BOUNDARY
applies_when: "案例经验归档与检索设计"
does_not_apply_when: null
counterexample: null
candidate_destination: CASE_REFINEMENT
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家二 §10 possible_case_refinement"
```

```yaml
elicitation_item_id: ELI-0912
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "收口阶段的失败模式（专家二组）"
expert_statement: "四种泛化失败：①将 S01–S08 完整回答原样写入 Core（方法/案例结论/假设/临时措辞未分离）；②将'这个案例算三套'写成所有外套增减都算新穿搭（案例结果扩大为行业规则）；③将'当前可以继续补拍'写成只要有实物就永远不得停止（忽略人员/画面完整性/任务目标）；④把具体禁用句升级为全品牌禁用词（被禁止的是无来源声明，不是这些词永远不能用）。专家二对全部四条标注 failure_label_candidate: NOT_ASSIGNED——新失败概念不自命名，覆盖审查按 E.2.3 走 B.6 既有标签映射，覆盖不了的走 B.8.1 合同版本升级提案。"
statement_type: FAILURE_MODE
applies_when: "候选资产入库与升格审查时的反面清单"
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家二 §7 forbidden_outcome 四条"
```

```yaml
elicitation_item_id: ELI-0913
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "收口阶段的失败模式（专家三组）"
expert_statement: "五种收口失败（专家三自注'描述性命名，不提请入册'）：①印象收口——不经检验按'感觉重要'分堆，库的第一批杂质最难清除；②案例走私——品类与数字混进通用 Core；③口号入库——无判定形式、无失败模式、无边界的'规则'，执行者各按各的理解跑；④单向验证升格——只在'说不'方向命中过的规则转正；⑤豁免权下放——把'机器可拦'悄悄升级成'机器可放'。这些命名仅为描述性候选，正式标签须走 E.2.3/B.8.1，不得私加。"
statement_type: FAILURE_MODE
applies_when: "同 ELI-0912"
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三 §7 forbidden_outcome 五条"
```

---

## 二、待裁决卡（PENDING）

> **2026-08-17 裁决落盘**：本节全部卡已由 Founder 裁决（八组裁决＋两项补充，见 pending_items.yaml 与 founder_rulings.yaml FR-07/FR-08），review_status 已翻转 ROUTED，裁决文本在各卡 founder_ruling_20260817 字段；文件头部 PENDING 统计以本注为准（归零）。

```yaml
elicitation_item_id: ELI-0914
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "案例经验（CASE_SCOPED 清单，见 ELI-0910）的存放形态"
expert_statement: "案例经验并入夹具库还是建独立经验集——决定它被检索和复用的方式。两案专家均认为合法，未择边。"
statement_type: BOUNDARY
applies_when: null
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "不另建新库（不过度工程化），并入现有素材库"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三 §9 uncertain_points 1；专家三 REVIEW_SUMMARY '需要 Founder 决定'1"
founder_question: "案例经验存放：并入夹具库，还是独立经验集？"
```

```yaml
elicitation_item_id: ELI-0915
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "判卷检验（ELI-0909 清单）的执行主体"
expert_statement: "判卷检验由谁执行——运行时自审、独立审核步、还是仅人工；该决定同时决定哪些检验可以按 ELI-0902 的唯一例外双挂方法模块。"
statement_type: BOUNDARY
applies_when: null
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "知识入库全自动：素材提供→模型提取结构化→验证脚本通过＝正式知识，无须任何人判定审核；候选仅指录入前状态"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三 §9 uncertain_points 2；专家三 REVIEW_SUMMARY '需要 Founder 决定'2"
founder_question: "判卷检验执行主体：运行时自审／独立审核步／仅人工，选哪种（可分检验指定）？"
```

```yaml
elicitation_item_id: ELI-0916
source_session: DIYU-KE-S09-20260817-001
source_round: S09-R01
source_situation: "资产库的新陈代谢机制"
expert_statement: "正式规则被 S08 式判分推翻几次后触发降级复审——无此机制库无新陈代谢。阈值属产品治理数字，专家不代定。"
statement_type: BOUNDARY
applies_when: null
does_not_apply_when: null
counterexample: null
candidate_destination: CONTRACT_PROPOSAL
review_status: ROUTED
founder_ruling_20260817: "不设\"推翻N次自动降级复审\"机制（不过度工程化），出问题 Founder 直接改"
provenance: AI_PROPOSAL_FOUNDER_APPROVED
source_ref: "专家三 §9 uncertain_points 3；专家三 REVIEW_SUMMARY '需要 Founder 决定'3"
founder_question: "正式规则复审触发：被判分推翻几次后降级复审？"
```

---

## 三、来源统计与残留说明

**卡数分布**：CONTRACT_PROPOSAL 11（含 PENDING 3）、RULE_CANDIDATE 1、JUDGE_QUESTION 1、CASE_CANDIDATE 1、CASE_REFINEMENT 1、KERNEL_METHOD 0（本场为治理收口场，方法本体卡在各场次文件）。

**残留说明**：

1. 三位专家对 S01–S08 方法/规则的枚举清单（专家一十条方法结构、专家二 M1–M13 与硬规则候选清单、专家三分拣表一/二）**不在本文件重复立卡**——其内容本体与 S01–S08 各场 ELI 文件的卡一一对应，映射关系见总索引。本场只入库"怎么分拣"的治理知识，不重复"分拣了什么"。
2. S09-R00（E2E 匿名判分材料准入）未开始：三案匿名 A/B 包、封盲、双窗口问卷等前置全部未提交，状态 MATERIAL_NOT_READY——相关合同问题在 PCR-08、实证问题在 EV-04，不产知识卡。窗口一/窗口二判分未发生，本文件不含任何判分结论。
3. 专家二/专家三均声明 INSUFFICIENT_CONTEXT：现行 PRD、附录 A/B 原文与当前资产库结构未提供，本轮只能完成候选分类，不能声称已经入库生效——照记。全部 16 卡均为候选态，正式生效须按 ELI-0906 通道另行批准。
4. 专家一未用十节模板且无事实分级标注（形式纪律缺口，已在追问轮审查中登记）；其内容经主审核对与专家二/三无断言冲突，按散文体原文入卡。
