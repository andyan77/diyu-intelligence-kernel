# tools/ ｜约 5-6 个小脚本，不是平台（C.2 / C.4 边界）

- `check_m0.py`：**M0 门禁统一入口**（P0-5）。顺序跑 冻结门送签态 → 变异回归 → 检测器测试 → BD-D01 三夹具 → Schema 四例烟测，五步全过才打 `CHECK_M0_GREEN`；每步同时核验退出码与输出标记（exit 0 ≠ 通过）。[4/5] 连 `case_version` 与 `(id, check, tag)` 有序断言集合一并全等断言（考卷被删断言时终态与标签纹丝不动，只有它拦得住）；[5/5] 含负例（结构违约 exit 1、不可核验 exit 2），一个"永远放行"的校验器在这两条上必红。冻结门**运行态**不计入判绿，只多打一行**按类别写实**的统计（R2=PENDING_BUILD 设计内 / R11=PENDING_RESIGN_P0-6 待重签 / R12=approved_at 已撤回待重签），冒出新类别或与基线数不符时当场加 ⚠。HEAD 不是 40 位 sha 时末行改打 `CHECK_M0_UNATTRIBUTED_GREEN`（仍 exit 0，但**不可**作为绑定提交的证据）。不接受任何参数，改口径=改考卷
- `install_hooks.sh`：启用 C.2 隔离门钩子（`git config core.hooksPath .githooks`），幂等；git 不随 clone 分发 `.git/hooks`，不跑这条本地就没有隔离门。钩子仅本地生效且 `--no-verify` 可绕过——服务端那道由 CI 的 `check_m0` job 把守
- **clone 后的上手顺序**：`pip install -r requirements.txt` → `bash tools/install_hooks.sh` → `python3 tools/check_m0.py`（三条跑完即得一份带 ROOT/HEAD 归属的门禁结论；CI 跑的是同一条 `check_m0` 命令，逐字一致）。第一条在**干净 venv** 里实测过 exit 0；若系统 python 里装的是别的版本，check_m0 环境行会打漂移提示（提示不改判绿），要与证据同条件复跑请在钉版 venv 里跑
- `validate_schema.py <instance> <schema>`：JSON Schema 校验（三件套之一）。exit 0=SCHEMA_OK / 1=SCHEMA_INVALID / 2=SCHEMA_UNVERIFIABLE（用法错误、文件读不到、非法 JSON——**无法核验 ≠ 通过**）；`--help` 打印用法并 exit 0。**用法文本里刻意不含任何结论标记串**——否则 `--help` 与 exit 2 的输出里都会带着 `SCHEMA_OK`，按标记判绿的调用方会被一次空跑骗过（`check_m0.py --help` 同理不含 `CHECK_M0_GREEN`）
- `run_case.py <case_dir> <output.json> --run-id X`：跑三带 must_hold（L1 只判 FAIL；终态只有 FAIL / PENDING_HUMAN，PASS 只属于 L3 人工）
- `coverage.py [--init-registry]`：四视图 + 知识卡池长度；"禁止结果"分母每次从 B 原文现数（C.4 铁律 2）
- `freeze_gate.py`：IA-0 冻结断言门（十三条红线 R1-R13：齐套 20 / 占位与空白 / Schema / 快照哈希与归属 / 规则解析与 A.9.1 字段集 / 签字三件套 / 版本指针实时核对 / 参数指纹实时重算 / 合同版本实时解析 / 真源 digest+version_history 链 / 待决扫描 / 身份唯一+撤回签字黑名单 / 30 需求×14 案例映射）；唯一合法开关 `--mode=sign`（送签态，Founder 08-17 批准），其余口径写死于常量，改口径=改考卷

边界：不建 Web UI / 数据库 / 趋势系统 / 自动通知；脚本只汇总不推导。
说明：C.6.1 尝试账本的 pre-commit 检查在 kernel 首个模块落地时接入（当前 kernel 为空，先装 C.2 隔离门）。Schema 对嵌套对象（VersionedRef 等）为存在性校验，字段级深度随模块落地逐版收紧——收紧属改考卷，走审批。
