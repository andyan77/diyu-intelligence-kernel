# 检测覆盖率报告（诚实基线——完整性仪表，不是能力证明；能力成立只由 B.8 闸门判定）

分母（脚本自 B 原文现数，禁止硬编码）：**58 条禁止结果**，分布于 11 个案例段

## 运行证据溯源（provenance，P0-4）

本报告的全部数字来自下述提交指针所在工作区的**当时内容**；取不到的字段留 `null`（不编造）。

```json
{
  "commit_sha": "37b2d55f3a20c64fe888a74bf8ec5ea1f4847f0b",
  "generator": {
    "path": "tools/coverage.py",
    "version": "v0.1",
    "sha256": "984d4b629eaef59fbb2c61e3f5adb05d85034377a5895288adde3b9a2390f570"
  },
  "commit_sha_source": ".git/HEAD + refs/packed-refs（读文件，未执行 git 命令）",
  "repo_root": "/tmp/claude-1000/-home-faye------/e029e7e8-93e8-43c1-bd03-b35e5cb53033/scratchpad/wt-blockA",
  "generated_at": "2026-08-17T22:10:36-07:00",
  "python_version": "3.10.12",
  "deps": {
    "jsonschema": "3.2.0",
    "PyYAML": "5.4.1"
  },
  "argv": [
    "tools/coverage.py"
  ],
  "sources": {
    "B_contract": {
      "path": "B_三个核心模块智能验收合同.md",
      "sha256": "79dc80057552b166583b49d2afc640f8b0ad132fb43fdc1e8e5b4113c2d63c87"
    },
    "prohibited_registry": {
      "path": "acceptance/detectors/prohibited_registry.yaml",
      "sha256": "6576878344225f60995cf1a7f1fd5fc703ae102810df82b5c082ca2d55f586d0"
    }
  },
  "detectors_version": "v0.1",
  "detectors_sha256": "4a4ee730a2fc501cf58857431ec387fde66551339dbe1ba8d136f7658668f30b",
  "detectors_path": "acceptance/detectors/checks.py",
  "note": "证据绑定生成时刻的工作区内容；与 HEAD 的一致性由干净 clone 回执核验"
}
```

## 视图1｜案例视角（14 条锁定案例 × 执行文件落地）

| 案例 | 执行文件 | 断言 | 探针 | 人工问题引用 |
|---|---|---|---|---|
| INT-D01｜模糊目标不得擅自确定 | 未落地 | — | — | — |
| INT-D02｜快速模式与增强模式 | 未落地 | — | — | — |
| INT-D03｜同一商品的目标迁移 | 未落地 | — | — | — |
| BD-D01｜高端品牌的库存与价值冲突 | ✅ | 7 | 1 | 1 |
| BD-D02｜有限商品池不得补写 | 未落地 | — | — | — |
| BD-D03｜反常识商品的情境判断 | 未落地 | — | — | — |
| CR-D01｜同一方向下的人设反事实 | 未落地 | — | — | — |
| CR-D02｜视频号语法与决策承接 | 未落地 | — | — | — |
| CR-D03｜完整且可制作的交付包 | 未落地 | — | — | — |
| CR-D04｜视觉证据与硬规则 | 未落地 | — | — | — |
| SYS-D01｜选择、批准、局部返工、版本引用与停止条件 | 未落地 | — | — | — |
| E2E-01｜高端品牌库存激活 | 未落地 | — | — | — |
| E2E-02｜同事实下的品牌资产目标 | 未落地 | — | — | — |
| E2E-03｜反常识商品的可用创意 | 未落地 | — | — | — |

执行文件落地：1/14

## 视图2｜禁止结果视角（检测器四态）

| 状态 | 条数 | 占比 |
|---|---|---|
| deterministic | 3 | 5% |
| llm_assisted | 0 | 0% |
| human_required | 55 | 94% |
| not_detectable_declared | 0 | 0% |

确定性/探针覆盖合计：3/58（其余全部 PENDING_HUMAN，绝不自动 PASS）

## 视图3｜维度视角（案例声明制，脚本不推导）

0 条案例声明了维度（暂无；案例落地时自行声明）

## 视图4｜闸门视角（Gate 声明制）

IA-0 ~ IA-4：前置案例清单未声明（gates.yaml 待 IA 准备时落，真源 B.8）

## 附加指标｜知识卡池长度（E.3）

acceptance/candidates/elicitation/：**9 张**（持续增长不清空 = 第四个经验库早期信号）
