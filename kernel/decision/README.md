# kernel/decision — Business Decision Engine（M2-EP01）

> **【提前段·非正式证据】** 本模块属 D §十一「开发可乱序，闸门按序关闭」授权的提前开发段
> （琥珀段）施工产物。IA-1 尚未 PASS，**本目录一切自测结论都不是 IA-2 取证**；Gate IA-2 的
> 关闭前提与程序以 B.8 为准。
>
> **证据等级自述**（协作契约第 4 条）：离线回放 47+ 项自测 = **结构层达标**（runtime_verified
> 的只是"确定性编排与校验面按合同形状工作"）；live 真实调用未执行，候选质量、冲突识别的
> 语义正确性均属 L2/L3 判分面，**本 README 不作任何「符合真源／验收通过」表述**。

## 职责（A.6 三条命脉）

读 BusinessDecisionRequest（A.6.1：冻结 IntentExecutionPlan + Context Snapshot + ACTIVE 规则），
产出 BusinessDecisionBundle（A.6.2/A.6.3），三条命脉由确定性代码焊死、不问模型：

1. **候选 2-3 个且有真实商业取舍差异**——candidate_count_status 三态按存活候选数计算；
   凑不出不凑（DEGRADED_TWO 带受限说明；不足两个返回阻断诊断，不补造）；
2. **recognized_conflicts 显式识别**——冲突两面必须可溯到池内 FACT/RULE；
3. **human_selection_required 恒 true**——系统推荐属 MODEL_JUDGMENT，永不免除人工选择。

## 七类资产落位（C.3）

| 资产 | 文件 |
|---|---|
| ① schema 引用 | config.py（只引用 contracts/schemas/，不复制） |
| ② 分步 prompt 链 | prompts/decision_step{1,2,3}_*_v0.1.md（三步：冲突识别→候选生成→逐候选取舍，C.3 BD 分步裁决） |
| ③ 确定性前处理 | preprocess.py（事实/规则池物化 + 输入闸 IG1-IG6 + A.6.1 请求装配） |
| ④ 确定性后校验 | rules_engine.py（逐规则 HardRuleResult，G.2 第 4 条四点纪律）+ postcheck.py（Preflight D1-D11 三态） |
| ⑤ Trace 组装 | trace.py（四类分离；模型只许引用预物化 ID） |
| ⑥ 冻结 fixtures | 上游输入用考卷区 BD-D01 冻结件（只读）；模型回复回放件在 fixtures/ |
| ⑦ 模块清单 | module_manifest.py → module_manifest.json（自动生成，手改无效） |

「Product Role Engine 骨架」= 商品池物化（preprocess）+ 五值枚举与池内校验（postcheck D9）
+ 角色作为带理由的 MODEL_JUDGMENT（prompt step2）。**角色判定条件未裁决**（PCR-03 第 4 项），
代码不发明判定规则——见 UPSTREAM_GAPS.md 第 3 条。

## 判分归属（C.5）

本目录全部自测属 **L1 考生自查**：只判 FAIL / 只证结构，**不判 PASS**。候选实质差异、
冲突识别完备性、取舍质量属 L2 探针 / L3 人工判分面；逐规则质检单（机器可查/仅人可查两栏）
随每次运行落在 report 的 machine_human_register。

## 运行

```bash
# 离线自测（纯 replay，零网络零密钥零写考卷区）
python3 kernel/decision/test_decision_offline.py

# 单次回放
python3 -m kernel.decision.runner \
  --plan acceptance/cases/BD-D01/fixtures/intent_execution_plan.frozen.json \
  --snapshot acceptance/cases/BD-D01/fixtures/context_snapshot.json \
  --replay-step1 kernel/decision/fixtures/BD-D01.step1.model_reply.json \
  --replay-step2 kernel/decision/fixtures/BD-D01.step2.model_reply.json \
  --replay-step3 kernel/decision/fixtures/BD-D01.step3.model_reply.json \
  --out /tmp/bdb.json --report /tmp/bdb.report.json

# live（密钥只接受环境变量 DASHSCOPE_API_KEY 预注入；本模块不读 .env）
python3 -m kernel.decision.runner --plan … --snapshot … --live --out … --report …
```

退出码：0 = Preflight 全过；1 = 判红（bundle 照写盘留取证）；2 = 没跑完（零半成品）。

## 知识吸收与防泄题声明

三份 prompt 的 method_structure_inputs 逐条登记了从知识提取候选卡（S03/S04）吸收的**方法
骨架**（判断顺序 / 候选唯一性三元组 / 四字段刻画 / 推荐判据主语），全部已去商品名词、数值、
考卷编号与失败标签名；**案例答案族、光谱预判、具体话术、未裁决标签名一律未进入本目录任何
会被渲染进 prompt 的内容**（C.8：不建冲突原型库注入 prompt；E.3 候选态纪律）。
