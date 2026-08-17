#!/usr/bin/env bash
# 钩子启用脚本（P0-5「可传播门禁」；施工真源 M0收口修复批次_执行规格.md §二 P0-5「钩子安装脚本」）。
#
# 为什么需要它：git **不会**随 clone 分发 .git/hooks。C.2 隔离门（.githooks/pre-commit）躺在仓库里，
# 但新克隆的机器上默认一次也不会触发——门禁写好了却传播不出去，正是 BLOCK-05 的一半。
# 本脚本把「让 git 认这个目录」这一步从口口相传变成一条命令。
#
# 幂等：已经指向 .githooks 时**一次配置都不写**，直接报告现状并退出 0；重复运行结果一致。
#
# 诚实边界（三条，别把本脚本读成"C.2 已经拦得住了"）：
#   ① 钩子只在**本地**生效。别人 clone 后不跑这一条，他那边就没有 C.2 隔离门；
#   ② `git commit --no-verify` 可以绕过任何 pre-commit 钩子——本地钩子是提醒，不是不可绕过的闸；
#   ③ 因此 CI（.github/workflows/ci.yml → tools/check_m0.py）才是真正跑在服务端、绕不过去的那道。
#      本脚本降低本地误提交的概率，**不构成**"约束已上服务端"的证据；
#   ④ linked worktree 上要当心：`git config core.hooksPath` 写进的是 common `.git/config`，
#      对该仓**所有** worktree 生效，而 `.githooks` 是相对路径——没有 .githooks/ 目录的兄弟
#      worktree 会"配置看着对、一个钩子都不跑"。在哪棵树上装，就在哪棵树上回验。
#
# 用法: install_hooks.sh          启用（幂等）
#       install_hooks.sh --help   打印本用法
#       exit 0=已启用 1=启用失败/前置不成立 2=用法错误
set -euo pipefail

usage() {
  cat <<'EOF'
用法: install_hooks.sh          启用 C.2 隔离门钩子（幂等；已启用时一次配置都不写）
      install_hooks.sh --help   打印本说明
      exit 0=已启用 1=启用失败/前置不成立 2=用法错误
作用: git config core.hooksPath .githooks —— 让 git 认仓库内的 .githooks/ 目录。
      git 不随 clone 分发 .git/hooks，新克隆的机器不跑这条就没有本地 C.2 隔离门。
边界: 钩子只在本地生效；`git commit --no-verify` 可绕过；服务端那道由 CI 的 check_m0 job 把守。
EOF
}

if [ "$#" -gt 0 ]; then
  case "$1" in
    --help|-h) usage; exit 0 ;;
    *) printf '用法错误：install_hooks.sh 不接受参数（实得 %s）\n\n' "$*" >&2; usage >&2; exit 2 ;;
  esac
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

HOOKS_DIR=".githooks"
WANT="$HOOKS_DIR"

# ---- 前置 1：得在 git 工作区里（.git 可能是目录，也可能是 worktree 的一行文件）----
if [ ! -e "$REPO_ROOT/.git" ]; then
  printf 'REJECT | %s 下没有 .git，这里不是 git 工作区，无处启用钩子\n' "$REPO_ROOT" >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  printf 'REJECT | 找不到 git 命令，无法配置 core.hooksPath\n' >&2
  exit 1
fi

# ---- 前置 2：钩子本体得在。目录空着却把 hooksPath 指过去 = 配置看着对、一个钩子都不跑 ----
if [ ! -f "$REPO_ROOT/$HOOKS_DIR/pre-commit" ]; then
  printf 'REJECT | 缺 %s/pre-commit（C.2 隔离门本体）——指过去也没有钩子会跑\n' "$HOOKS_DIR" >&2
  exit 1
fi

# ---- 启用：先读现状，已经对就不写 ----
current="$(git config --get core.hooksPath 2>/dev/null || true)"
if [ "$current" = "$WANT" ]; then
  printf '现状 | core.hooksPath 已是 %s —— 本次未写入任何配置（幂等：重复运行是空操作）\n' "$WANT"
else
  # 必须显式判失败：`git config` 在"有 .git 但不是真 git 仓"（如只有一个空 .git/ 目录）时
  # 以 128 退出并吐 git 原生 `fatal: not in a git directory`。在 set -e 下那个 128 会被原样带出，
  # 违反本脚本自己声明的退出码契约（0/1/2），且不带其他失败路径都有的 `REJECT | ` 前缀——
  # 按 rc==1 判「启用失败」的调用方会把它读成未知状态。这里把 git 原生码收敛回 1。
  if ! git_err="$(git config core.hooksPath "$WANT" 2>&1)"; then
    printf 'REJECT | 写入 core.hooksPath 失败（git 原生报错：%s）——'"$REPO_ROOT"' 下有 .git 但不是可用的 git 仓库？\n' \
           "${git_err:-<无输出>}" >&2
    exit 1
  fi
  printf '写入 | core.hooksPath = %s（原值：%s）\n' "$WANT" "${current:-<未设置>}"
fi

# ---- 回验：不信"命令没报错"，只信读回来的值（exit 0 ≠ 生效）----
verify="$(git config --get core.hooksPath 2>/dev/null || true)"
if [ "$verify" != "$WANT" ]; then
  printf 'REJECT | 配置后回读得到 %s ≠ %s，启用未生效\n' "${verify:-<空>}" "$WANT" >&2
  exit 1
fi

# ---- 可执行位：git 会**静默跳过**不可执行的钩子——配置对、钩子不跑，是最像绿的一种红 ----
fixed=""
for hook in "$REPO_ROOT/$HOOKS_DIR"/*; do
  [ -f "$hook" ] || continue
  if [ ! -x "$hook" ]; then
    chmod +x "$hook"
    fixed="$fixed $(basename "$hook")"
  fi
done
# 注意：这里必须写成 if，不能写 `[ -n "$fixed" ] && printf ...`——
# 在 set -e 下，那种写法在 $fixed 为空（即"没什么要补"的正常路径）时会让整条语句以 1 结束，
# 脚本反而以失败收场：一个"一切正常"的分支把安装脚本判成失败，正是最容易被误读成红的假红。
if [ -n "$fixed" ]; then
  printf '补正 | 以下钩子缺可执行位，已 chmod +x：%s（不可执行的钩子会被 git 静默跳过）\n' "$fixed"
fi

hooks_list="$(cd "$REPO_ROOT/$HOOKS_DIR" && ls -1 | tr '\n' ' ')"
origin="$(git config --show-origin --get core.hooksPath 2>/dev/null | awk '{print $1}' || true)"
printf '启用结果 | core.hooksPath=%s%s | 钩子清单: %s\n' \
       "$verify" "${origin:+（来源 $origin）}" "${hooks_list% }"
printf '生效范围 | 仅本机本仓；`git commit --no-verify` 仍可绕过；服务端那道由 CI 的 check_m0 job 把守\n'
printf 'HOOKS_INSTALLED\n'
