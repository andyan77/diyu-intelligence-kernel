# IA-0 冻结签字包（✅ 已签字生效：Founder 2026-08-17T19:08:38+08:00；送签模式 GATE_GREEN 后写入 20 份 Manifest）

> 定格结果：主模型 qwen-max-0107（两侧同用）｜多模态 qwen-vl-max（锁别名+运行回执）｜审计 deepseek-v4-pro｜参数真源 contracts/interaction/generation_parameters.json｜合同批次 v1.0 FROZEN。运行前补填字段（构建版本类 4 项）按双模式纪律于每次运行前补填并过运行态门。

> 给 Founder 的一页话：IA-0 是"考试规则公证"关。这一包就是全部考试规则的定稿材料。**现在还不用签**——下面 B 类建设项做完、全部 PENDING 占位清零后，我把定稿版送到你面前，你花约 15 分钟走完 A 类裁决并签字，M0 即告收口。

## 一、已就绪资产（草案态，全部可机械校验）

| 资产 | 位置 | 状态 |
|---|---|---|
| 14 条案例 → **19 份运行 Manifest 草案**（多输入/双模式案例一变体一份：INT-D02×2、INT-D03×2、CR-D01×2、CR-D04×3） | acceptance/cases/*/manifest*.draft.yaml | 19/19 过 Schema；经 25 blocker + 41 minor 对抗修复 |
| 两阶段基线 Prompt（诚实写强，B.2.4 零重试口径） | contracts/interaction/baseline_prompt_stage_D/C.md | v0.1-draft |
| 匿名判分流程（含 B.5.2 双窗口、B.2.5 六项逐项留档清单） | contracts/interaction/anonymity_procedure.md | v0.1-draft |
| OD-02 模型与参数定格提案（型号家族+定格程序，版本串 IA-0 实测填入） | contracts/OD-02_模型与参数定格提案.md | DRAFT |
| 待裁项中央登记册（97 条，编号可追溯到每份文件） | acceptance/cases/OPEN_QUESTIONS.md | 全部 PENDING_IA0 |

## 二、A 类｜✅ 已全部预裁决（Founder 2026-08-17 整体按推荐，见 OPEN_QUESTIONS 文首与台账）

以下留档为当时的裁决主题：

1. **每场考试用什么模式跑**（快速/增强）——B 没写的约 10 场，我届时附推荐值表（OQ-*-execution_mode 系列）
2. **四个案例缺"考题原句"**——BD-D01/BD-D02/CR-D03/E2E-01 需要你各补一句正式任务陈述（OQ-BD-D01-xx 等）
3. **品牌禁语要不要立成正式硬规则对象**，以及 BD-D01"一组规则"到底几条（OQ-*-hard_rule 系列）
4. **基线侧失败要不要重试**——现默认零重试；给重试=修改 B 合同，需你立项（OQ-BASELINE-07）
5. **模型让不让"打草稿"**——基线侧 thinking 块允许+匿名前剥离的提案（OQ-BASELINE-06）
6. **匿名流程 14 项人选与细则**——赋值表由谁封存、违规后果标签等（OQ-ANON-01~14）
7. **PRD 与 A 的一处小分歧**——口播包"情绪"字段 PRD 列了、A 没列，改哪边（OQ-BASELINE-11）
8. **OD-02 定格**——当日 API 实测版本串+参数表签字（contracts/OD-02 提案 §三）

## 三、B 类｜执行侧建设项（做完才允许送签，不用你参与）

- 18 份缺失的 Context Snapshot 夹具（素材取自衡叙集数据包）+ snapshot_hash 算法定格
- 共同两阶段交互合同、共同输出合同两份文件落盘（B:992 三件套缺其二）+ 笛语侧转换器 ref/risks 分工对齐
- contracts/rules/ RuleRecord 注册表首批落盘（品牌禁语清单 → 规则对象）
- **冻结断言门**：送签前脚本扫描全部 Manifest，任何 PENDING 残留 = 物理拒绝送签（堵"带着占位签字"的假绿）
- 齐套口径登记：14 案例 ↔ 19 份运行 Manifest（缺任一变体不得计齐套）

## 四、IA-0 当天剩余动作（如实口径：约 30-40 分钟；可再压缩，见注）

1. **版本定格**：API 实测两家 models 列表 → 版本串 + 参数哈希填入 20 份 Manifest；
2. **补值裁决**（建设轮发现的 Founder 值类事项，见 OPEN_QUESTIONS 的 OQ-BUILD 系列）：时间窗口天数、E2E-03 与 CR 四案例商业目标、三句缺失考题、账号编号、INT-D01 库存剔除与 INT-D02 快速侧处理、词表三词补入、BD-D01 口径统一与两项确认类；
3. **冻结断言门全绿** → 你签字（approved_by/approved_at）→ draft 转 FROZEN → M0 退出门核验。

> 注：第 2 项我可在送签前再出一轮带推荐值的选择题（同 08-17 预裁决模式），把当天压缩回 ≈15 分钟。

## 附｜签字动作定义（B.2.1）

A 类逐项裁决落盘 → B 类清零 → PENDING 扫描断言过 → 19 份 Manifest 的 approved_by/approved_at 写入你的签字与时间戳 → 状态 draft→FROZEN → M0 退出门核验。
