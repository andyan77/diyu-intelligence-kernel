# tools/ ｜约 5-6 个小脚本，不是平台（C.2 / C.4 边界）

- `validate_schema.py <instance> <schema>`：JSON Schema 校验（三件套之一）
- `run_case.py <case_dir> <output.json> --run-id X`：跑三带 must_hold（L1 只判 FAIL；终态只有 FAIL / PENDING_HUMAN，PASS 只属于 L3 人工）
- `coverage.py [--init-registry]`：四视图 + 知识卡池长度；"禁止结果"分母每次从 B 原文现数（C.4 铁律 2）

边界：不建 Web UI / 数据库 / 趋势系统 / 自动通知；脚本只汇总不推导。
说明：C.6.1 尝试账本的 pre-commit 检查在 kernel 首个模块落地时接入（当前 kernel 为空，先装 C.2 隔离门）。Schema 对嵌套对象（VersionedRef 等）为存在性校验，字段级深度随模块落地逐版收紧——收紧属改考卷，走审批。
