# OPEN_QUESTIONS｜IA-0 待裁项中央登记册

> 性质：考卷区登记册（append-only 精神；改动=改考卷走审批）。**主册 97 条**已由 Founder 于 2026-08-17 裁决或确认执行侧处置，逐条结果见本文件「裁决」列；**建设轮 OQ-BUILD 14 条另表**，逐条状态见该表「关闭状态」列（2026-08-17 M0 收口修复批次实测回填，未关闭者如实标出，不按整体口径宣告关闭）。
> 来源：M0-EP02 草案起草+对抗审查+修复复核两轮工作流（25 blocker + 41 minor 修复后遗留的真实待裁项）。各 manifest/文件注释中的 OQ 编号均指向本文件。
> 总数：**主册 97 条 + 建设轮 OQ-BUILD 14 条 = 111 条**（本文件 `| OQ-` 行实测 111 行）。裁决即落盘：每条裁决结果回填本文件「裁决」/「关闭状态」列并登记《裁决台账》。
> 注（2026-08-17 M0 收口修复批次补）：本册各条「真源依据」列描述的是**起草当时**的仓库状态（例如「contracts/rules/ 仅 .gitkeep」「无 fixtures/ 目录」「contracts/rules/ 为空」）。这些状态已在 M0-EP02 建设轮被推翻——各案例 `fixtures/` 与 `contracts/rules/` 三条 RuleRecord（R-BDD01-001 / R-BDD01-002 / R-FB01-001）均已落盘。依据列作为提问时的历史证据原样保留，不改考卷。

## ✅ IA-0 已完成（2026-08-17 签字生效）：**主册 97 条**裁决类条目就此关闭；建设队列类（OQ-BUILD-06/12/14）转 M1+ 执行

> 范围声明（2026-08-17 M0 收口修复批次补）：上行的「关闭」只覆盖**主册 97 条**。建设轮 OQ-BUILD 14 条不在该整体口径内——其中 7 条（01/02/03/04/07/08/13）经本批次逐条实测已在夹具侧落盘关闭，3 条（06/12/14）为建设队列转 M1+，**4 条（05/09/10/11）实测尚未关闭**，逐条证据见下表「关闭状态」列。签字包 `IA-0_冻结签字包.md` §二 同口径。

> 匿名流程 ANON 组补充（2026-08-17 M0 收口修复批次两裁决）：B 合同 v0.4 补登失败标签 `EVAL_BLINDING_PROCEDURE_INVALID`（一枚关闭 P-05 / P-08 / P-11，后果＝该次盲测作废、不算 IA-4 证据、按 B.8.1 修复后重测）+ 匿名流程六执行值全按推荐定格（P-03 / P-04 / P-06 / P-10 / P-12 / P-13）。逐项取值见 `contracts/interaction/anonymity_procedure.md` v1.0 §8，裁决记录见《裁决台账》08-17「修复批次两裁决」行。

## 预裁决（Founder 2026-08-17，整体按执行侧推荐，台账登记）

8 主题：①模式=「考追问才开增强」（增强：INT-D01 主跑、INT-D02 增强变体；其余全 QUICK；INT-D01 补 QUICK 分支变体，总 20 份）②四句考题定稿（已回填对应 Manifest）③品牌禁语立 RuleRecord（R-FB01-001，词表以 detectors 为唯一运营真源）+ BD-D01「一组规则」=现有 2 条 ④基线零重试、不动 B 合同（整场对称重跑合法）⑤允许 <thinking> 块、匿名前剥离 ⑥匿名三关键：脚本随机+密封文件+git 哈希封存 / 阶段 D 与终审独立随机 / 揭盲后禁回改（要改=重测）⑦A v0.2 补 VoicePackage「emotion（情绪）」⑧OD-02 按提案（qwen-max 当前代两侧同用 / qwen-vl-max / deepseek-chat；t=0.3, top_p=0.8, 固定 seed；版本串 IA-0 实测）。
执行侧自决项：hash=sha256 规范化 JSON、Schema 补版本戳、PENDING 冻结断言门、运行顺序记 run 证据层、allowed_tools 空=零外部工具（内部编排豁免 B.2.2）、Persona 冻结落点=快照内容。

### 素材映射表（Founder 2026-08-17 随 8 主题一并批准；补登于建设轮，纠正"批准未落盘"缺口）

| 案例 | 素材 |
|---|---|
| INT-D01/02/03 | P13 商品事实在场；按各案例考点故意留缺（D01 缺目标、D02 缺人设/品牌信息） |
| BD-D02 | P01+P02+P03 三件套 |
| BD-D03 / E2E-03 | P11 荧光裤 + 受众 A02「克制表达者」 |
| CR-D01 | 商品任一 + 包 4 双人设 R01/R02 |
| CR-D04 | A=P13 清晰图；B=P08 只给文字事实；C=损坏图片文件 |
| E2E-01/02、SYS-D01 | P13 + 五包全套；E2E-02 复用 E2E-01 同一快照只换目标 |

注：映射表**不含**各案例商业目标取值（BD-D03 的 PRODUCT_LAUNCH 系执行侧推断，标 inferred 待 IA-0 确认）。

## 建设轮新增待裁项（OQ-BUILD 系列，2026-08-17 快照建设中发现）

| 编号 | 待裁问题（大白话） | 去向（登记时路由） | 关闭状态（2026-08-17 M0 收口修复批次逐条实测） |
|---|---|---|---|
| OQ-BUILD-01 | INT-D01 快照里 P13 自带的"库存 800/消化期"要不要剔除？留着可能向系统暗示商业目标，还让"虚构库存"这条禁止结果失去判别力 | IA-0 裁决 | ✅ 已关闭——`acceptance/cases/INT-D01/fixtures/context_snapshot.json` `ia0_ruling`：「Founder 2026-08-17 IA-0 裁决（OQ-BUILD-01）：剔除 P13 自带库存与生命周期字段」 |
| OQ-BUILD-02 | INT-D02 快速侧怎么跑得起来？B 只说缺人设/品牌信息，但 OD-03 把商业目标列为一票拦停项——目标从考题句里解析 / 另行冻结 / 还是确认快速侧就该停 | IA-0 裁决 | ✅ 已关闭——`acceptance/cases/INT-D02/fixtures/task_input.json` 冻结 `stated_business_goal=INVENTORY_ACTIVATION`（A.4.1 承载，不改 B 考题句）；两份 INT-D02 Manifest 首行同注 |
| OQ-BUILD-03 | 禁用词表两份口径不一致：品牌包十词 vs 考卷词表（缺"绝绝子/显贵/高级感"，多"跳楼价/亏本价"和虚假稀缺组）——要不要把三词补进考卷词表（改考卷，需批准） | IA-0 裁决 | ✅ 已关闭——`acceptance/detectors/forbidden_lexicon.yaml`「Founder 2026-08-17 IA-0 裁决：补齐数据包·包1 品牌调性禁词（OQ-BUILD-03）」，`brand_tone` 组已含绝绝子 / 显贵 / 高级感 |
| OQ-BUILD-04 | CR 四案例的商业目标取值（6 份快照现为 PENDING） | IA-0 裁决 | ✅ 已关闭——CR-D01 / CR-D02 / CR-D03 / CR-D04(a/b/c) 六份快照 `facts.business_goal.source` 均写「Founder 2026-08-17 IA-0 裁决（OQ-BUILD-04）」 |
| OQ-BUILD-05 | CR-D02 的"人工选择记录"（ReviewRecord）夹具由谁建；跨快照承接（Bundle 引 BD 快照、运行在 CR 快照）合法性 | IA-0 裁决 | ⛔ **尚未关闭**（本批次实测）——`acceptance/cases/CR-D02/fixtures/frozen_decision_selection.json` 的 `review_ref.object_id` 仍为 `PENDING_REVIEW_RECORD_IA0`（ReviewRecord 夹具未落盘）；同文件 `_context_snapshot_ref_note` 记载的跨快照承接合法性亦无裁决落痕。**仍属 Founder 待裁项** |
| OQ-BUILD-06 | CR-D04-a 需要真实清晰商品图片文件；仓库现无任何图片实体（构建期从云盘取，M3 前补齐） | 建设队列 | ⏭ 建设队列——转 M1+/M3 执行（IA-0 §二同口径）；仓库现有 `acceptance/cases/CR-D04/fixtures/corrupted_image.jpg` 为「损坏图片」输入 B 的夹具，不是本条要求的清晰商品图片 |
| OQ-BUILD-07 | E2E-01 / SYS-D01 的"限定周期"具体时间窗口值（OD-03 对库存激活是拦停项，须 Founder 定值） | IA-0 裁决 | ✅ 已关闭——`acceptance/cases/E2E-01/fixtures/context_snapshot.json` 与 `SYS-D01/fixtures/context_snapshot.json` 同写「Founder 2026-08-17 IA-0 裁决：六周（夹具虚构-剧本；OQ-BUILD-07）」 |
| OQ-BUILD-08 | E2E-03 商业目标值 + 三句缺失考题（CR-D02 / E2E-03 / SYS-D01 的 task_statement） | IA-0 裁决 | ✅ 已关闭——`acceptance/cases/E2E-03/fixtures/context_snapshot.json` `business_goal.source` 写「…正常在售新品→新品推广（OQ-BUILD-08）」；CR-D02 / E2E-03 / SYS-D01 三份 Manifest 的 `task_statement` 均已定稿（注写 Founder 2026-08-17 裁决） |
| OQ-BUILD-09 | BD-D01 旧夹具与新批快照对同一商品口径不一致（尺码简写/成分只录一行）——统一即改考卷，是否做 | IA-0 裁决 | ⛔ **尚未关闭**（本批次实测）——仓库内未检索到任何引用 OQ-BUILD-09 的裁决落痕；BD-D01 旧夹具与新批快照的口径统一与否无记录。**仍属 Founder 待裁项** |
| OQ-BUILD-10 | 品牌定位双值并存（B 冻结 HIGH_END vs 品牌包"中高端"【模拟】）——快照已注明以 B 为准，请确认 | IA-0 确认 | ⚠️ **未见 Founder 确认落痕**（本批次实测）——E2E-01 / SYS-D01 快照的 `brand_positioning.coexisting_fixture_statement.note` 已写「与 B 冻结的 HIGH_END 并存，未合并改写；案例判定以 B 冻结值为准」，但该注为执行侧书写，无 IA-0 确认记录。**确认动作仍待 Founder** |
| OQ-BUILD-11 | _fixture_note/source 元数据下发前剥离（不给被测模块看考点）——执行侧已拟定剥离口径 | IA-0 确认 | ⛔ **尚未关闭**（本批次实测）——INT-D01 / INT-D02 / INT-D03 三份快照的 `_fixture_note` 仍写「整份 JSON 是否原样下发给被测模块，B/A 均未规定 → 冻结前须确认剥离口径」，剥离口径未落盘。**仍属 Founder 待裁项** |
| OQ-BUILD-12 | 其余 13 案例的 case.yaml（三带断言执行文件）建设排期——非 IA-0 前置（IA-0 只冻 Manifest） | 建设队列 | ⏭ 建设队列——转 M1+ 执行（IA-0 §二同口径）；非 IA-0 前置 |
| OQ-BUILD-13 | 视频号账号编号 account_id 值（数据包未给，未自造，现为 null+PENDING） | IA-0 裁决 | ✅ 已关闭——CR-D01 / CR-D03 / E2E-01 / E2E-03 / SYS-D01 五份快照 `video_account*.account_id` 均写 `ACC-HXJ-001`，`source` = 「Founder 2026-08-17 IA-0 裁决：虚构编号（OQ-BUILD-13）」 |
| OQ-BUILD-14 | PersonaFacts / VideoAccountFacts 对象注册与版本号（对象落盘后回填 VersionedRef） | 建设队列 | ⏭ 建设队列——转 M1+ 执行（IA-0 §二同口径）；对象落盘后回填 VersionedRef |

## INT（10 条）

| 编号 | 待裁问题（大白话） | 真源依据 | 裁决 |
|---|---|---|---|
| OQ-INT-D01-01 | INT-D01 这场考试到底按「快速模式」还是「增强模式」跑？B 的 INT-D01 全段一次都没提模式，草案只能先占位写 ENHANCED，请 Founder 定。 | B_三个核心模块智能验收合同.md B:271-304（B.4.1/INT-D01 全段无 execution_mode） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D01-02 | B 里写了一句「用户明确选择快速模式时，可以返回暂定目标候选…」——INT-D01 是不是也要再跑一次快速模式？如果要，就得再冻一份运行 Manifest。 | B:284 + B:130（每个正式案例运行前必须冻结一份 Case Manifest） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D01-03 | 三个 Intent 案例的硬规则清单现在都是空的。IA-0 冻结品牌事实时如果附带了硬规则（例如禁用表达清单），要不要登记进这三个案例？ | B:128-166（hard_rule_refs 字段）+ B:271-304 / B:306-348 / B:350-385（三案例均未列规则对象）；仓库现存规则对象仅 acceptance/cases/BD-D01/fixtures/context_snapshot.json 的 R-BDD01-001/002 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D01-04 | allowed_tools 填空数组，是不是就等于「这三个案例一件工具都不许用」？B 只说不许用没声明过的搜索或知识库，并没有说必须填空。 | B:179（B.2.2「不允许任一侧使用未声明的搜索或知识库」，且 B:170 自述适用于正式 A/B） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D01-05 | output_schema_version 现在写的 "v0.1" 找不到出处——仓库里的 Intent 输出 schema 文件本身没写版本号，B 也没规定诊断案例的输出合同版本。IA-0 要定成什么？ | contracts/schemas/intent_execution_plan.schema.json（无版本字段）+ B:128-166 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D01-06 | 现在的自动校验看不见 PENDING 占位——带着 8 个「待定」照样报 SCHEMA_OK。冻结前用什么办法把还带占位的 Manifest 拦下来，不让它被当成已通过？ | contracts/schemas/case_manifest.schema.json + B:163（approved_at 是 datetime，schema 只当普通字符串、无格式校验） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D02-01 | INT-D02 要跑快速、增强两次。除了模式这一项，两次的其他条件（特别是要不要用同一份事实快照）是否必须完全一样？B 对本案例没有规定。 | B:316-330（两族允许答案）+ B:168-182（B.2.2「同条件」自述管的是正式 A/B 两侧，不管同一案例的双模式两次运行） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D02-02 | B 明说不许「编造创始人背景、账号关系或品牌禁语」。IA-0 冻结的品牌禁语清单要不要做成硬规则对象、登记进 INT-D02 的 hard_rule_refs？ | B:334（INT-D02 禁止结果第一条） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D03-01 | INT-D03 的 A/B 两次运行按哪个模式跑？B 的 INT-D03 全段没写，草案两份都先占位写 QUICK；另外两份是否必须取同一个模式，B 也没说。 | B:350-385（B.4.1/INT-D03 全段无 execution_mode） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-INT-D03-02 | B 禁止「后一次读取前一次未批准判断」，说明 A/B 两次运行有先后顺序；但 Case Manifest 里没有记录运行顺序的字段，这个先后怎么固定、怎么留证据？ | B:375（禁止结果）+ B:128-166（B.2.1 Case Manifest 字段表无运行顺序字段） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |

## BD（15 条）

| 编号 | 待裁问题（大白话） | 真源依据 | 裁决 |
|---|---|---|---|
| OQ-BD-D01-01 | BD-D01 这场考试到底用「快速模式」还是「增强模式」跑？B 原文从头到尾没说，现在填的 QUICK 只是占位、没有依据。 | B:391-440（B.4.2/BD-D01 全段不提 execution_mode）；acceptance/cases/BD-D01/manifest.yaml L30-31 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D01-02 | 真正下发给两侧模型的那句业务任务是什么？B 只给了给评委看的「能力问题」，那句是评分用的、不能当任务发给模型。 | B:407-409（能力问题小节）；B:174「相同业务任务」；B:188；acceptance/cases/BD-D01/manifest.yaml L26-28 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D01-03 | R-BDD01-001/002 这两条硬规则现在只写在夹具快照文件里，contracts/rules/ 是空的——要不要在冻结前把它们正式落成规则对象（否则规则正文改了版本号也不会变，没人发现）？ | acceptance/cases/BD-D01/fixtures/context_snapshot.json 的 hard_rules[]；contracts/rules/ 仅 .gitkeep；A.9.1 RuleRecord（A:813） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D01-04 | B 说降级分支要「另冻结一组规则」（是一组、复数），现在只落了 1 条 R-BDD01-002——这组到底是几条、怎么拆？ | B:405（两候选降级分支原文）；acceptance/cases/BD-D01/manifest.yaml L39-41 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D01-05 | BD-D01 的「两候选降级分支」算不算要单独跑一次、单独冻一份 Manifest？现在是把基线禁令和降级分支规则合并在同一份快照里当一次运行。 | B:405；B.2.1「每个正式案例运行前必须冻结一份」(B:130)；夹具 SNAP-BDD01-0001 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D01-06 | output_schema_version 写的 v0.1 是跟着附录 A 的版本走的，但输出 Schema 文件自己没写版本号——这个版本号怎么定、由谁盖章？ | contracts/schemas/business_decision_bundle.schema.json（无版本字段）；M0-EP01_文档版本一致性声明.md 一、现行版本基线 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D02-01 | BD-D02 用「快速模式」还是「增强模式」跑？B 没说，现在的 QUICK 只是占位。 | B:442-473（B.4.2/BD-D02 全段不提 execution_mode）；acceptance/cases/BD-D02/manifest.yaml L27-28 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D02-02 | 下发给模型的用户原话是什么？B 只有一句第三人称的事实描述（商品池三个、用户要十套穿搭），那是快照事实不是任务原话。 | B:446-448（冻结事实小节）；B:174；acceptance/cases/BD-D02/manifest.yaml L23-25 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D02-03 | SNAP-BDD02-0001 这份快照还没建：那三个商品具体是哪三个、事实从哪来？ | B:448；acceptance/cases/BD-D02/ 无 fixtures/ 目录；manifest.yaml L18-20 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D02-04 | IA-0 建 BD-D02 快照时如果带上品牌禁语之类的硬规则，要不要回填到 hard_rule_refs？现在是空的。 | B:442-473（无具名规则/禁令）；contracts/rules/ 仅 .gitkeep；manifest.yaml L30-33 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D02-05 | output_schema_version 的 v0.1 同 BD-D01：输出 Schema 文件自己没写版本号，这个号谁来定？ | contracts/schemas/business_decision_bundle.schema.json（无版本字段） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D03-01 | BD-D03 用「快速模式」还是「增强模式」跑？B 没说，现在的 QUICK 只是占位。 | B:475-511（B.4.2/BD-D03 全段不提 execution_mode）；acceptance/cases/BD-D03/manifest.yaml L25-26 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D03-02 | B 只说输入里「提供品牌定位、受众、场景和商业目标」，这四样的具体内容是什么？不冻下来这场考试没法跑，也没法判两侧同条件。 | B:479-481（输入小节）；acceptance/cases/BD-D03/ 无 fixtures/ 目录；manifest.yaml L17-20 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D03-03 | B 要求答案里结合「品牌表达边界」，这条边界要不要落成一条具名硬规则挂进 hard_rule_refs？现在是空的。 | B:493（品牌表达边界）；contracts/rules/ 仅 .gitkeep；manifest.yaml L27-30 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BD-D03-04 | output_schema_version 的 v0.1 同上：输出 Schema 文件没版本号，这个号谁来定？ | contracts/schemas/business_decision_bundle.schema.json（无版本字段） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |

## CR（18 条）

| 编号 | 待裁问题（大白话） | 真源依据 | 裁决 |
|---|---|---|---|
| OQ-CR-D01-01 | CR-D01 用快速模式还是增强模式跑？B 里这个案例根本没写模式，草案先放着 QUICK 只是占位、没有 B 依据，请 Founder 定。 | B:515-545（B.4.3/CR-D01 全段无 execution_mode 字样）；字段定义 B:142 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D01-02 | CR-D01 每次运行的任务原话怎么写？B 把两种人设写在同一句「分别切换」里，草案给每次运行各引一条人设（B:521+B:523 / B:521+B:524），这样切分的措辞要不要照此冻结？ | B:521-524 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D01-03 | CR-D01 要切成「品牌主理人」「年轻买手」两份运行 Manifest（缺一份不算齐），IA-0 冻结时是否照此签两份？ | B.2.1 B:130「每个正式案例运行前必须冻结一份 Case Manifest」+ B:521-524 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D01-04 | 四份 CR 案例的 hard_rule_refs 现在全是空的：B 在 Creative 四个案例里没给任何规则编号，仓库 contracts/rules/ 也还是空目录。IA-0 前要不要先把「品牌禁用表达」「品牌硬规则」登记成正式规则对象再回填？（CR-D01/D02/D03/D04 同一处） | B:649「三种输入都遵守品牌禁用表达和商品事实；」、B:657「视觉创意覆盖品牌硬规则；」；contracts/rules/ 为空；唯一落盘规则对象在 acceptance/cases/BD-D01/fixtures/context_snapshot.json 的 R-BDD01-001/002 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D01-05 | Creative 的输出合同（九部分制作包）现在仓库里根本没有 Schema 文件，四份 CR 草案的 output_schema_version 只能写 `PENDING_IA0`（引述起草当时的历史状态；反引号包裹 = 引述，非活标记，见 tools/freeze_gate.py 的 bare_marker_count）。这份输出合同谁来落盘、版本号怎么定？（CR-D01/D02/D03/D04 同一处） | contracts/schemas/ 现有 intent_execution_plan / business_decision_bundle / case_manifest / common.defs，无 Creative 输出 Schema；B:587-597 九项交付物；字段定义 B:144 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D01-06 | SNAP-CRD01/02/03/04-000x 这些快照编号目前只是规划名，四个 CR 案例目录下都没有 fixtures/，快照还没造。谁在 IA-0 前把快照建出来、hash 什么时候回填？（CR-D01/D02/D03/D04 同一处） | acceptance/cases/CR-D0*/ 无 fixtures/（对照 acceptance/cases/BD-D01/fixtures/context_snapshot.json）；字段定义 B:139-140 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D01-07 | 四份 CR 案例的 allowed_tools 都填了空数组，但 B 只说「不许用没声明过的搜索或知识库」，并没说必须为空。IA-0 是否确认 Creative 四个案例一律不给任何工具？（CR-D01/D02/D03/D04 同一处） | B.2.2 B:179「不允许任一侧使用未声明的搜索或知识库；」；字段定义 B:161 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D02-01 | CR-D02 用快速模式还是增强模式跑？B 这个案例没写模式，草案的 QUICK 只是占位、没有 B 依据，请 Founder 定。 | B:547-581（B.4.3/CR-D02 全段无 execution_mode 字样） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D02-02 | CR-D02 到底给被测模块下什么任务？B 那句「冻结一个由 Founder / Reviewer 选定的 Business Decision」是跑之前要先做的准备动作，不是发给模型的任务，所以任务栏先空着（PENDING）——请 Founder 定这次运行的任务原话。 | B:553 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D02-03 | CR-D02 被冻结的那份 Business Decision，它的版本化引用（object_id / version）现在还不存在；IA-0 冻结后这条引用写到哪里？（B.2.1 的 Manifest 字段表里没有承接它的字段） | B:553；B.2.1 字段表 B:133-163 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D03-01 | CR-D03 用快速模式还是增强模式跑？B 这个案例没写模式，草案的 QUICK 只是占位、没有 B 依据，请 Founder 定。 | B:583-632（B.4.3/CR-D03 全段无 execution_mode 字样） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D03-02 | CR-D03 在 B 里既没有「输入」也没有「能力问题」，直接就写「输出必须包含九项」。这次运行给模型的任务原话由谁按 B 的意思补？ | B:583-587（直接进入「输出必须包含：」） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D03-03 | CR-D03 的允许答案族要求「批准后能把九项资产完整导出为 Markdown」，这个导出算不算需要事先声明的工具权限（要不要写进 allowed_tools）？ | B:611 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D04-01 | CR-D04 用快速模式还是增强模式跑？B 这个案例没写模式，草案的 QUICK 只是占位、没有 B 依据，请 Founder 定（三份变体同）。 | B:634-668（B.4.3/CR-D04 全段无 execution_mode 字样） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D04-02 | CR-D04 切成输入 A/B/C 三份运行 Manifest（缺一份不算齐），任务原话就是 B 那三句、只去掉加粗符号。IA-0 是否照此签三份、照此措辞冻结？ | B:638 / B:640 / B:642；B.2.1 B:130 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D04-03 | CR-D04 三份快照（有清晰图 / 不给图 / 给坏图）的素材差别谁来准备？三份快照对应 SNAP-CRD04-0001/0002/0003。 | B:638 / B:640 / B:642 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D04-04 | CR-D04 挂着 SYS-03 和 SYS_RULE_VIOLATION 这个失败标签，但现在一条硬规则对象都没有——没有规则，「视觉创意覆盖品牌硬规则」这条禁止结果根本判不了。IA-0 必须先补规则对象吗？ | B:636 映射 SYS-03；B:657 禁止结果；B:668 失败标签；contracts/rules/ 为空 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-CR-D04-05 | CR-D04 要看商品图片（多模态）。B.2.1 的 Manifest 只有一组 model_provider/model_name 字段，多模态模型要不要另记一行？ | B.2.1 字段表 B:157-160；B:638/641 图片输入 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |

## SYS-E2E（23 条）

| 编号 | 待裁问题（大白话） | 真源依据 | 裁决 |
|---|---|---|---|
| OQ-SYS-D01-01 | SYS-D01 真正要下发的那句「局部问题」是哪一条？B 只举了三个例子（拍摄场景不可用／某句口播缺事实依据／某个镜头违反品牌规则），没说用哪个，执行侧不能替 Founder 选。 | B_三个核心模块智能验收合同.md:679-683 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-SYS-D01-02 | SYS-D01 用快速模式还是增强模式跑？B 这一整段从头到尾没提过模式，草案里的 ENHANCED 只是占位、没有任何 B 依据。 | B:672-713（全段无模式表述）；字段定义 B:142 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-SYS-D01-03 | SYS-D01 要不要登记硬规则？B 里「某个镜头违反品牌规则」是用来举例说明返工场景的，不是冻结下来的规则，现在按空数组处理，请确认。 | B:684；contracts/rules/（目录内无任何规则对象） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-SYS-D01-04 | output_schema_version 写的 v0.1 是哪来的？B 没写、contracts/schemas/ 里的 Schema 文件也没声明版本号，现值只是同批草案沿用，需要 IA-0 正式定一个。 | contracts/schemas/*.json（无 version 声明）；字段定义 B:144 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-SYS-D01-05 | SYS-D01 的快照 SNAP-SYSD01-0001 现在只是个名字，案例目录下没有任何夹具文件，hash 算不出来——IA-0 之前由谁、按什么材料把它建出来？ | 仓库现状 acceptance/cases/SYS-D01/（无 fixtures/）；字段定义 B:139-140 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-01-01 | E2E-01 下发给两侧的那句业务任务原文是什么？B 只列了核心事实（库存、品牌定位、禁令、目标方向），没有给出可以直接下发的完整任务句子。 | B:726-732 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-01-02 | E2E-01 用快速模式还是增强模式跑？B 没说，草案里的 QUICK 只是占位。 | B:724-745；字段定义 B:142 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-01-03 | E2E-01 的「禁止低价叫卖」要挂到哪个规则对象上？现在 contracts/rules/ 是空的，全仓库唯一真实存在的同款规则是 BD-D01 夹具里的 R-BDD01-001——是复用它，还是给 E2E 另建规则对象？ | B:730；contracts/rules/（空）；acceptance/cases/BD-D01/fixtures/context_snapshot.json | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-01-04 | 两侧共用的交互合同和输出合同文件还没写出来（contracts/interaction/README 自己登记了这个缺口），三个 E2E 案例的这两个版本号现在只能挂 PENDING——谁在 IA-0 前把这份合同落盘并升 v1.0/FROZEN？ | contracts/interaction/README.md §4 关闭记录表「共同外部交互/输出合同文件」两行 + §1 目录内容表（起草当时按行号写作 :63、:40-41，README 改版后行号已错位，2026-08-17 M0 收口修复批次改为按小节名引用）；B:184-204 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-01-05 | E2E-01 的 output_schema_version 该定成什么？B 没给版本号，contracts/schemas/ 里的 Schema 文件也没声明版本，现值 v0.1 无真源背书。 | contracts/schemas/*.json（无 version 声明）；字段定义 B:144 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-01-06 | E2E-01 的快照还没建（目录里没有夹具）；另外 B 说 Persona 和 VideoAccountFacts「按 Manifest 冻结」，可 Manifest 的字段表里根本没有这两项，它们到底放进 Context Snapshot 还是另找地方？ | B:732 对照字段表 B:133-163；acceptance/cases/E2E-01/（无 fixtures/） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-02-01 | E2E-02 的任务陈述要不要按「E2E-01 定稿任务 + 换目标那一句」拼出来，并且和 E2E-01 同一轮定稿？B 只给了换目标那一句，单看它没有商品和库存背景，两侧收到的任务会失去可比基准。 | B:749、B:751；acceptance/cases/E2E-01/manifest.yaml | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-02-02 | E2E-02 用快速模式还是增强模式跑？B 没说，草案里的 QUICK 只是占位。 | B:747-758；字段定义 B:142 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-02-03 | E2E-02 继承自 E2E-01 的同一条「禁止低价叫卖」，规则对象注册后是两个案例引同一个对象，还是各引各的？ | B:749、B:730；contracts/rules/（空） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-02-04 | 同 OQ-E2E-01-04：两侧共用的交互/输出合同文件缺失，E2E-02 的这两个版本号只能挂 PENDING，谁在 IA-0 前落盘？ | contracts/interaction/README.md §4 关闭记录表「共同外部交互/输出合同文件」两行（起草当时按行号写作 :63，2026-08-17 M0 收口修复批次改为按小节名引用）；B:184-204 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-02-05 | E2E-02 现在直接复用 E2E-01 的快照 ID，并要求 hash 一字不差——请确认「相同企业事实」就是用同一份快照实例，而不是另做一份内容相同的快照。 | B:749；B:172 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-02-06 | E2E-02 的 output_schema_version 该定成什么？现值 v0.1 无真源背书（B 与 Schema 文件均未声明版本号）。 | contracts/schemas/*.json（无 version 声明）；字段定义 B:144 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-03-01 | E2E-03 的商业目标原文是什么？B 明说品牌、受众、Persona 和商业目标都由 Manifest 冻结，也就是要 Founder 给，B 自己没给。 | B:762 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-03-02 | E2E-03 用快速模式还是增强模式跑？B 没说，草案里的 QUICK 只是占位。 | B:760-764；字段定义 B:142 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-03-03 | IA-0 冻结 E2E-03 的品牌事实时，如果这些事实自带硬规则（例如表达禁令），要不要写进本案例的 hard_rule_refs？ | B:762；contracts/rules/（空） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-03-04 | 同 OQ-E2E-01-04：两侧共用的交互/输出合同文件缺失，E2E-03 的这两个版本号只能挂 PENDING，谁在 IA-0 前落盘？ | contracts/interaction/README.md §4 关闭记录表「共同外部交互/输出合同文件」两行（起草当时按行号写作 :63，2026-08-17 M0 收口修复批次改为按小节名引用）；B:184-204 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-03-05 | E2E-03 的 output_schema_version 该定成什么？现值 v0.1 无真源背书（B 与 Schema 文件均未声明版本号）。 | contracts/schemas/*.json（无 version 声明）；字段定义 B:144 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-E2E-03-06 | E2E-03 的快照还没建（目录里没有夹具）；而且 B 说品牌、受众、Persona 由 Manifest 冻结，可 Manifest 字段表里没有这几项，它们放哪？ | B:762 对照字段表 B:133-163；acceptance/cases/E2E-03/（无 fixtures/） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |

## BASELINE（17 条）

| 编号 | 待裁问题（大白话） | 真源依据 | 裁决 |
|---|---|---|---|
| OQ-BASELINE-01 | 基线阶段 D 输出里，装「事实/规则/假设/模型判断」这四类依据的那个容器，草案自己取名叫 basis_entries——笛语侧转换出来的同一个东西该叫什么？两边必须同名，请定一个。 | B:188（B 与 A 都没为这个外部容器命名）；contracts/interaction/baseline_prompt_stage_D.md §5/§6-1 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-02 | 每个候选方案对外展示时，到底露出哪几个子字段？（笛语内部的 trace_refs、hard_rule_results 已按 B 不要求基线伪造而剔除） | A.6.3 BusinessCandidate；contracts/interaction/baseline_prompt_stage_D.md §5/§6-2 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-03 | A 里商品引用是「带版本的引用对象」（VersionedRef），基线只能写商品编号 product_id 原文——这个降级写法两边怎么统一？ | A.6.3 product_roles[].product_ref；B:188（不要求基线伪造笛语内部 ID）；contracts/interaction/baseline_prompt_stage_D.md §5/§6-3 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-04 | B 要求阶段 D 顶层必须有 risks（风险）字段，A 里风险却只挂在每个候选下面。草案两处都写了：顶层装「选哪个候选都躲不掉的风险」，候选级装「这条路线独有的风险」。这个分工对吗？必须和笛语侧转换器一次定死。 | B:188 逐项含 risks vs A.6.3 candidate 级 risks（A.6.2 无顶层 risks）；contracts/interaction/baseline_prompt_stage_D.md §4正文/§5/§6-4 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-05 | 输出里所有「引用」该怎么写？商品写 product_id、受众写 audience_id、硬规则写 rule_id 加版本号已定；但「事实条目」用什么标识 B 和 A 都没规定。两边写法不一样，裁判一眼就能认出哪份是笛语的。 | B:225 B.2.5「相同外层展示格式」；A.3.2/A.3.4/A.3.5/A.9.1；两份 Prompt §5/§6 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-06 | 允不允许基线模型先写一段 <thinking> 思考草稿、再输出 JSON，由 runner 在匿名化之前整段删掉？（笛语侧可以多次调用把推理外化，基线只有一次调用；不给草稿空间等于故意把基线写弱） | B:215「不得故意写弱」；B:182（笛语侧可多模块多次调用）；B:219-230 B.2.5；两份 Prompt §4/§5/§6 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-07 | 基线侧一次调用失败（格式错/截断/超时）后要不要给重试机会？B.2.4 现在只允许一次调用——草案默认零重试、该侧记 FAILED。若你认为该给对称重试预算，那要修改 B 合同（走 B.8.1 版本升级+双侧重跑），请裁决是否立项。 | B:208（B.2.4 一次受控调用）+ B:245（PRE-03-M 限定笛语侧）+ baseline_prompt_stage_D/C §4 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-08 | 阶段 D 输出 → 匿名 → 冻结选择 → 回流成阶段 C 输入，这条衔接以 anonymity_procedure.md 为准；请确认那份文件与两份 Prompt 说的是同一套流程。 | B:188-194 B.2.3；contracts/interaction/anonymity_procedure.md；两份 Prompt §6 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-09 | 两侧输出统一用中文（简体）、字段名和枚举值保留英文——B 没规定语言，这是执行侧为了「两边长得一样」定的口径，请确认笛语侧也照此。 | B:225「使用相同外层展示格式」（B 未规定输出语言）；两份 Prompt §4 输出格式/§5/§6 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-10 | 商品图片这类非文字材料，阶段 C、阶段 D 和笛语侧是不是走同一个通道、同一批材料、同一个顺序？需要核一遍。 | B:173「相同商品图片和其他输入材料」；contracts/interaction/baseline_prompt_stage_C.md §2/§5/§6-5 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-11 | 口播包（voice_package）要不要加「情绪」字段？PRD 明确把情绪列进了 Voice Package 最小内容，附录 A 的 VoicePackage 却没有这个字段。补就两侧一起补，不补就明确记成 PRD 与 A 之间的既有差异。 | PRD:609 vs A:757；contracts/interaction/baseline_prompt_stage_C.md §5/§6-4 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-12 | 九个部分各自对外展示哪些子字段？（笛语内部的引用对象已剔除，两边显示口径必须一样） | A.8（A:751-761）；contracts/interaction/baseline_prompt_stage_C.md §5/§6-1 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-13 | 口播提示条目（cues）、常见问答条目、官方回应条目、假设条目——这几个「条目里面」具体有哪些字段？A.8 没展开。 | A:757 / A:761（A.8 未展开条目内部字段）；contracts/interaction/baseline_prompt_stage_C.md §5/§6-2 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-14 | 视频总时长由案例统一给定（写进任务陈述或硬规则），还是让模型自己定？两侧必须一样才可比。 | B.2.2（B:170-180 同条件）；contracts/interaction/baseline_prompt_stage_C.md §6-3 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-15 | 共同输出合同的版本号（output_contract_version）取什么值？它要写进 Case Manifest 的 e2e_output_contract_version / e2e_interaction_contract_version，且两阶段必须同值。 | B:194-202 E2EComparisonEnvelope；B.2.1 Case Manifest；两份 Prompt §6 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-16 | 「共同交互合同」和「共同输出合同」这两份文件仓库里现在根本没有，谁来建、什么时候建？IA-0 冻结要的是三件（共同交互合同＋输出合同＋基线 Prompt），眼下只有第三件。 | B:995；contracts/interaction/README.md §3/§4 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-BASELINE-17 | Brand Memory 首轮是关掉的，所以两份 Prompt 没有它的入口。以后一旦打开，必须先给两份 Prompt 加一个和笛语侧完全一样的 Brand Memory 输入通道并同批升版——这个前置条件确认吗？ | B:96（首轮验收关闭 Brand Memory）；B:180；contracts/interaction/README.md §1 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |

## ANON（14 条）

| 编号 | 待裁问题（大白话） | 真源依据 | 裁决 |
|---|---|---|---|
| OQ-ANON-01 | 匿名化和封存 X/Y 赋值表这件事，由谁来做？B 只说两类判分可以由 Founder 一个人兼，没指定一个「不判分的第三方」；如果身边根本找不到既不判分、又信得过的人，这条流程就没有合格执行人——请 Founder 定人选，或在确实找不到人时定替代办法。 | contracts/interaction/anonymity_procedure.md §1 硬约束 3 / §8 P-01；B:771（v0.2 取消外部制作裁判）、B:997（IA-0「裁判与匿名流程已确定」） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-ANON-02 | 阶段 D 选候选时用的那张 X/Y 赋值表，到了最后合并终审时是接着用同一张，还是重新抽一次？B 没写。 | contracts/interaction/anonymity_procedure.md §2.4 / §3.1 T4 / §8 P-02；B.2.3（B:190、B:192）、B.2.5、B.10 均未规定 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-ANON-03 | 证据里的「选择冻结时间」（choices_frozen_at）记的是商业问卷交完那一刻，还是两份问卷都交完那一刻？B 两处说法没说清关系。 | contracts/interaction/anonymity_procedure.md §3.3 / §8 P-03；B.5.4（B:809）、B.10（B:1123） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-04 | 两份问卷之间「至少间隔一个工作时段」，到底是隔多久算数（半天？一整天？隔夜？）B 只写了这句话没给时长。 | contracts/interaction/anonymity_procedure.md §0 / §4 / §8 P-04；B.5.2（B:773） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-05 | 如果两份问卷在同一个工作时段里连着做完（或没做到独立作答），这次运行算哪个失败标签？后果是作废重来还是别的？B 的标签表和阻断解除条款都没写，执行侧不敢自己定。 | contracts/interaction/anonymity_procedure.md §4 末段 / §8 P-05；B.5.2（B:773）、B.0（B:29）、B.6.4（B:913-942）、B.8.1 | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-06 | 端到端这几场的证据文件叫什么名字、放在哪个目录下？现在 acceptance/runs/ 里只有诊断运行的样例命名惯例，B 没规定端到端的。 | contracts/interaction/anonymity_procedure.md §7 / §8 P-06；B.10 未规定命名 | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-07 | 这份《匿名判分流程》什么时候由 Founder 签字、从草案转成正式生效版？现在还没提交过。 | contracts/interaction/anonymity_procedure.md 表头状态行 / §8 P-07；B.8 IA-0（B:997） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-ANON-08 | 如果匿名处理时不小心改动了业务内容、或两边的外层展示格式不一样，该记哪个失败标签、后果是什么？这两条是 B.2.5 的要求，B 的标签表里没有对应项，执行侧不自己乱套标签。 | contracts/interaction/anonymity_procedure.md §6 第 3 行 / §8 P-08；B.2.5（B:225、B:230）、B.6.4（B:926-928） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-09 | 揭盲之后，判分人还能不能回头改自己已经冻结的答卷？B 里三处「冻结」的原文都只管到「揭晓来源之前」，揭盲之后没写。 | contracts/interaction/anonymity_procedure.md §3.2 末段 / §5 第 5 条 / §8 P-09；B.2.5（B:228）、B.5.4（B:809）、B.5.2（B:773）；B.2.1（B:166）管的是案例条件不是答卷 | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
| OQ-ANON-10 | 「随机给 X、Y 标签」和「随机排展示顺序」这两件事，必须分别独立抽两次，还是可以用同一次随机结果推出来？B 只是并排列了两条要求。 | contracts/interaction/anonymity_procedure.md §2.1 尾注 / §8 P-10；B.2.5（B:223、B:227） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-11 | 怎么才算证明了 X/Y 的对应关系和展示顺序没有在揭盲后被人偷偷调换？B 只要求记录「足以看出谁选了哪一侧」，没规定防篡改的证明方式；这种「记录齐全但真实性存疑」的情况该记哪个标签也没写。 | contracts/interaction/anonymity_procedure.md §2.4 / §6 第 5 行 / §8 P-11；B.10（B:1123）、B.6.4 EVAL_EVIDENCE_INCOMPLETE（B:928） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-12 | Decision Acceptance（决策采纳）、Content Adoption（内容采用）、Edit Severity（修改严重度）这三项，分别由商业问卷还是制作问卷来填？要不要跟选择一起冻结？B 只给了三组枚举值，没说归属和冻结时点——但 IA-4「所需修改不高于 LOCAL」正是靠 Edit Severity 判的。 | contracts/interaction/anonymity_procedure.md §3.2 / §7 / §8 P-12；B.5.4（B:811-842）、B.5.5 第 5 条（B:859）、B.8 IA-4（B:1049） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-13 | 「独立作答」具体怎么算数？比如做制作问卷时，能不能翻看已经冻结的商业问卷答案？B 写了「时间分离、独立作答」但没定义「独立」的可核查判据。 | contracts/interaction/anonymity_procedure.md §4 独立作答行 / §8 P-13；B.5.2（B:773） | ✅已裁决 08-17 修复批次（值见 anonymity_procedure.md v1.0 §8） |
| OQ-ANON-14 | 两边 Prompt 如果允许模型写 <thinking> 思考块，这段思考要不要在匿名化之前剥掉？剥到什么程度？它算「模型日志/Prompt」（该藏）还是算「业务内容」（不许动）？B 两条要求都没点名思考块。 | contracts/interaction/anonymity_procedure.md §2.3 stripped_fields_manifest / §8 P-14；B.2.5（B:226、B:230）；衔接来源 contracts/interaction/README.md L14、L71（BASELINE 组把该口径落点指向本文件） | ✅预裁决 08-17（方向已定；数值随 B 类建设/IA-0 定格填实） |
