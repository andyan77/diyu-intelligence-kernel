# kernel/intent/fixtures｜资产⑥ replay 夹具

## 这些文件是什么（先读这一句）

**全部为「手写」的模型回复，不是任何一次真实 LLM 调用的录制产物。**

写在最前面是为了堵一条假绿：文件名里带 `model_reply`，一眼看去很像「某次真跑的留痕」。
若把手写件当成录制件，就会得出「模型确实这么答过」这种**没有发生过的结论**——
本模块的红线是「无检测器不得判 PASS、未确认事实禁止确定性表述」，这条同样适用于夹具自身的来源。

真实录制件将来若落盘，须在本表新增一行并写明 run_id / 调用时间 / 实际 model 字段（`generation_parameters.json`
的 `_note` 要求逐次运行留存接口返回的实际 model），与手写件分开存放，不得混用同一命名。

## 用途

`kernel/intent/llm.py::call_llm(prompt_text, "replay:<path>")` 直接读文件内容当作模型原文返回。
于是 `test_intent_offline.py` 可以**零网络**跑通整条编排（前处理 → 1 步 LLM → 确定性覆盖与硬闸 → Preflight），
且「这次跑的是哪份回复」可逐字取证。

## 清单

| 文件 | 配套快照 / 任务原话 | 手写这份回复是为了考什么 |
|---|---|---|
| `INT-D01.quick.model_reply.json` | `acceptance/cases/INT-D01/fixtures/context_snapshot.json`｜「帮我推广羊绒大衣。」QUICK | 模型**承认目标没说清**：`AMBIGUOUS` + 两个实质不同候选 + 一个澄清问题（B.4.1/INT-D01 允许答案族） |
| `INT-D01.enhanced.model_reply.txt` | 同上，ENHANCED | 同上；**并且外面套了 ` ```json ` 围栏**——真实模型经常这么回，用来实跑 `llm.parse_model_json` 的剥围栏路径。故扩展名是 `.txt`：它在磁盘上不是合法 JSON，标成 `.json` 会误导任何按扩展名解析的工具。**诚实边界：带围栏本身是一次格式违约**（`prompts/intent_v0.2.md` 三、明令「不要输出 markdown 代码围栏」），当前实现选择**容忍并剥除**，且**不留任何痕迹**——产物里看不出这次模型没按格式回。A.4.6 的 `FORMAT_INVALID` 尚未接线到本模块，故这属**已知容忍项**，不是"格式已合规"。接线之后这份夹具应当同时被记一次格式违约 |
| `INT-D02.quick.model_reply.json` | `acceptance/cases/INT-D02/fixtures/context_snapshot.json`｜「为这件羊绒大衣制作春节前视频号内容。」QUICK + `--stated-goal INVENTORY_ACTIVATION` | 模型自报 `confidence_level: HIGH`——用来实测「模型自报只会被调低、不会被调高」（runner G6） |
| `INT-D03.input-a.model_reply.json` | `acceptance/cases/INT-D03/fixtures/context_snapshot.json`｜「用这件羊绒大衣促进春节前库存消化。」QUICK | 目标迁移的 A 侧：解析为 `INVENTORY_ACTIVATION` |
| `INT-D03.input-b.model_reply.json` | 同一份快照｜「用同一件羊绒大衣建立品牌长期价值，不以本期销量为主要目标。」QUICK | 目标迁移的 B 侧：解析为 `BRAND_STORY`。两侧共用同一份快照，唯一变量是任务原话（B.4.1/INT-D03「输入」） |
| `INT-D01.quick.live-20260818.model_reply.json` | `acceptance/cases/INT-D01/fixtures/context_snapshot.json`｜「帮我推广羊绒大衣。」QUICK | **不是手写——live 真实回复逐字录制**（唯一一份）：qwen3-max-2026-01-23，DashScope id `chatcmpl-f0cd5add-f381-9b96-9624-2748cab8b56f`，prompt v0.2，2026-08-18 冒烟第 3 发（前两发失败已登 ATT-0004 / 台账）。当次运行 PREFLIGHT_OK：`AMBIGUOUS` + 双候选 + 澄清问题 + `model_judgments=[]`（v0.2 纪律9 生效实证）。未接线到 SCENARIOS——录制目的是留住第一份真实模型行为样本，供回归与对照，不替代手写考点夹具 |
| `NEG-01.forced_continue.model_reply.json` | `acceptance/cases/INT-D01/fixtures/context_snapshot.json`｜「帮我推广羊绒大衣。」QUICK | **负向**：模型硬给 `RESOLVED` + 目标，并越权写了一个 `next_action: CONTINUE_TO_DECISION`（Prompt 明令模型不得输出该字段）。考「阻断缺失在场时，模型说什么都拦得住」 |
| `NEG-02.out_of_pool_ref.model_reply.json` | 同上 | **负向**：模型在**顶层 `referenced_fact_ids`** 里编了一个事实池里没有的 `FACT:product.stock_level`。考 C.3 资产⑤红线「模型只许引用预物化 ID」——该 ID 会进 `trace.build_trace_bundle`，组装期即硬失败（exit 2），不得被静默清洗掉 |
| `NEG-03.candidate_ref_out_of_pool.model_reply.json` | 同上 | **负向（第二条路径）**：同一个池外 ID **只**出现在 `goal_candidates[].referenced_fact_ids` 里，顶层引用全部干净。runner 只把顶层 `referenced_fact_ids` 传给 `build_trace_bundle`，所以这条路径**不会**在组装期挂掉——它一路走到 Preflight，由 `postcheck` P6 判「候选支撑引用悬空」→ exit 1，plan 照写盘。两条路径必须各有一份夹具：只留 NEG-02 的话，「候选里的幻觉引用」这条通道无人把守，而 AMBIGUOUS 运行的主要输出恰恰就是候选 |

## 手写这些回复时守的三条纪律

1. **只写模型有权写的字段**：`prompts/intent_v0.2.md` 的输出契约九个键。唯一例外是 `NEG-01`
   刻意多写的 `next_action`——那正是它要考的越权行为，不是笔误。
2. **引用 ID 逐字取自事实池**：`FACT:<field_path>`，由 `preprocess.materialize_fact_pool` 从对应快照物化。
   例外只有 `NEG-02`（顶层引用）与 `NEG-03`（候选引用）刻意编造的那一个 ID。
3. **`intent_summary` 不写阿拉伯数字**：Preflight P9 要求摘要里的数字能在快照文本中找到出处。
   手写件不去踩这条线，是因为本批夹具要考的是目标解析与硬闸，不是数字溯源；
   把两件事混在一份夹具里，判红时分不清是哪一条出的问题。
