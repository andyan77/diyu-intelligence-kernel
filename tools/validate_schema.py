#!/usr/bin/env python3
"""三件套之一：JSON Schema 校验。用法: validate_schema.py <instance.json> <schema.json>；exit 0=通过 1=违约。

退出码（P0-5 补全，判分语义一字未动）：
  0  SCHEMA_OK          结构过
  1  SCHEMA_INVALID     结构违约，逐条 VIOLATION 打印
  2  SCHEMA_UNVERIFIABLE 用法错误 / 文件读不到 / 不是合法 JSON —— **无法核验 ≠ 通过**
为什么加 2：此前少给参数会裸抛 IndexError 的 traceback，退出码 1 与"结构违约"撞车——
一个路径打错的调用会被读成"这份实例不合规"，两种完全不同的事实用同一个码。
调用方口径（acceptance/detectors/checks.py::schema_valid，考卷区，本次未改）：
  它只按 returncode == 0 分岔，非 0 一律判 FAIL——2 与 1 在它那里同样是"不放行"，
  故本次补码**不放宽**任何既有判分；stdout 首行给机器可读的 SCHEMA_UNVERIFIABLE 摘要，
  是为了让它 r.stdout 截取的 detail 说得清"没核验"而不是留白。
诚实边界：SCHEMA_OK 只说明结构合规，**不代表**取值正确或可冻结
  （OQ-INT-D01-06「SCHEMA_OK ≠ 可冻结」；对 PENDING_* 占位本脚本完全无感，占位由 freeze_gate 拦）。
"""
import json, sys, os
from jsonschema import Draft7Validator, RefResolver

# USAGE **不得包含任何结论标记串**（SCHEMA_OK / SCHEMA_INVALID / SCHEMA_UNVERIFIABLE）。
# 理由（本批次实测缺陷）：--help 与 exit 2 两条路径都会把 USAGE 打出去，而 unverifiable() 的
# stderr 会被 check_m0.run() 并进 stdout——USAGE 里只要出现 SCHEMA_OK，一次"无法核验"的运行
# 其合并输出里就带着"通过"标记，任何按标记子串判绿的调用方（包装脚本、日志巡检、人工肉眼）
# 都会被骗过。所以这里只用退出码措辞，标记串**只允许出现在最后那行真实结论里**。
USAGE = """用法: validate_schema.py <instance.json> <schema.json>
  退出码 0 = 结构过 | 1 = 结构违约（逐条 VIOLATION 打印）| 2 = 无法核验（≠ 通过）
  2 覆盖：参数个数不对 / 文件不存在 / 路径是目录 / 不是合法 JSON / 读取失败
  --help / -h  打印本说明并 exit 0
注意：结构过 ≠ 内容正确 ≠ 可冻结；本脚本对 PENDING_* 占位无感，占位残留由 tools/freeze_gate.py 拦。"""

def unverifiable(reason, show_usage=False):
    """无法核验时的统一出口：stdout 出机器可读摘要，stderr 出给人看的用法，退出码 2。"""
    print(f"SCHEMA_UNVERIFIABLE | {reason}")
    sys.stderr.write((USAGE + "\n") if show_usage else "")
    sys.exit(2)

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def validate(instance_path, schema_path):
    schema = load(schema_path)
    base = "file://" + os.path.abspath(os.path.dirname(schema_path)) + "/"
    resolver = RefResolver(base_uri=base, referrer=schema)
    errors = sorted(Draft7Validator(schema, resolver=resolver).iter_errors(load(instance_path)), key=lambda e: list(e.absolute_path))
    for e in errors:
        print(f"VIOLATION at /{'/'.join(map(str, e.absolute_path))}: {e.message}")
    return len(errors)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] in ("--help", "-h"):
        print(USAGE)                      # --help 是正常用法，exit 0。USAGE 里没有任何结论标记串，
        sys.exit(0)                       # 故一次 --help 的输出中查无 SCHEMA_OK——见 USAGE 上方注释
    if len(args) != 2:
        unverifiable(f"需要恰好 2 个参数（实例、Schema），实得 {len(args)} 个: {args}", show_usage=True)
    instance_path, schema_path = args
    for label, p in (("实例", instance_path), ("Schema", schema_path)):
        if not os.path.exists(p):
            unverifiable(f"{label}文件不存在: {p}")
        if os.path.isdir(p):
            unverifiable(f"{label}路径是目录不是文件: {p}")
    try:
        n = validate(instance_path, schema_path)
    except json.JSONDecodeError as e:      # 读得到但不是合法 JSON：没核验成，不是"违约"
        unverifiable(f"JSON 解析失败（{instance_path} 或 {schema_path}）: {e}")
    except OSError as e:
        unverifiable(f"文件读取失败: {e}")
    print(("SCHEMA_OK" if n == 0 else f"SCHEMA_INVALID ({n} violations)") + f" | {instance_path}")
    sys.exit(0 if n == 0 else 1)
