# kernel/decision replay 夹具（C.3 资产⑥配套）

**全部为手写、不是真实录制**（【M2-EP01 提前段·非正式证据】）。将来若加入真实录制件，必须
新增一行写明 run_id / 调用时间 / 实际 model，与手写件分开存放、不得混用同一命名。

命名：`<场景名>.<考什么>.step<N>.model_reply.json`；**在磁盘上不是合法 JSON 的用 `.txt`**
（标成 .json 会误导任何按扩展名解析的工具）。

| 文件 | 配套输入 | 手写这份是为了考什么 |
|---|---|---|
| `BD-D01.step1.model_reply.json` | acceptance/cases/BD-D01/fixtures/{intent_execution_plan.frozen,context_snapshot}.json | 冲突识别绿路径：CF-1 两面均指池内事实与 ACTIVE 规则 |
| `BD-D01.step2.model_reply.json` | 同上 + step1 | 两候选降级分支绿路径：两个实质差异候选 + 促销路线进 ruled_out_paths（机器谓词可确认 BLOCK）→ DEGRADED_TWO |
| `BD-D01.step3.model_reply.json` | 同上 + step2 | 取舍双向陈述 + 带判据主语的推荐（挂 MODEL_JUDGMENT） |
| `BD-D01.step2.blocked_candidate.model_reply.json` | 同 BD-D01 | 变体：第三候选 C3 strategy 含禁用词 → step3 前被拦进阻断诊断（explanation 不回写原词）、其假设/判断零残留、D7 仍零命中、DEGRADED_TWO、exit 0 |
| `NEG-01.out_of_pool_product.step2.model_reply.json` | 同 BD-D01 | 池外商品 P99 → postcheck D9 判红、exit 1（bundle 留取证） |
| `NEG-02.not_json.step1.model_reply.txt` | 同 BD-D01 | 输出契约违约（散文非 JSON）→ exit 2、零半成品 |
| `NEG-03.judgment_no_support.step3.model_reply.json` | 同 BD-D01 + 正样例 step1/2 | MODEL_JUDGMENT 无支撑引用 → trace 层报错、exit 2 |
| `NEG-04.duplicate_candidate_id.step2.model_reply.json` | 同 BD-D01 | candidate_id 重号 → 唯一性硬闸报错、exit 2、零半成品 |

手写这些回复时守的三条纪律：

1. **只写模型有权写的键**：三步各自 prompt「输出格式」列出的字段，一个不多
   （NEG 件的 `_fixture_note` 是夹具注释约定，`_` 前缀键两侧一律不参与判定）；
2. **数字只用快照里有的**（800 / 3980 等；D8 类级溯源口径），文本零禁用词
   （acceptance/detectors/forbidden_lexicon.yaml，只读对齐）；
3. **正样例内容参考了考卷正样例 output_good.json 的两候选方向**——这是模拟"模型应答成什么样"
   的夹具素材，不是把答案写进系统：进入 prompt 的只有方法骨架（见各 prompt 文件头
   method_structure_inputs），本目录任何内容都不会被渲染进 prompt。
