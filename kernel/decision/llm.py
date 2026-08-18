#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 资产：LLM 调用层（C.3 三步 LLM 的共用出口）。

【M2-EP01 提前段·非正式证据】

职责边界（只做两件事，多一件都不做；协议面与 kernel/intent/llm.py 逐字同构）：
  1. `call_llm(prompt_text, mode)`——把渲染好的 Prompt 发出去、把模型原文拿回来；
     mode="live" 走 DashScope OpenAI 兼容端点，mode="replay:<path>" 直接读一份录制/手写回复。
     三步 LLM（C.3 BD 分步裁决）= runner 依次三次调用本函数，各带各的 mode；本层不知道也
     不需要知道"现在是第几步"——步骤语义全部在 runner 与 prompt 文件里。
  2. `parse_model_json(raw)`——把模型原文解析成 dict。

**不做**的事：
  - 不改写 Prompt、不追加 system 提示、不做"输出不合规就再问一次"的自我修补（B.2.4）；
  - 不做重试。零重试口径：一次调用，失败即失败；要放宽必须走接口规格升级；
  - 不落盘、不打印任何密钥。API key 只从环境变量取，绝不读 .env（用户级 CLAUDE.md
    「密钥注入边界」先例：Prompt 授权某操作但禁掉其唯一前置时先停先问，不自行绕过）。

参数真源：contracts/interaction/generation_parameters.json 逐字段读文件，不在本文件硬编码取值。
max_tokens 取 max_tokens_stage_D：参数文件分 stage_C / stage_D 两档，阶段 D 即商业候选阶段
（contracts/interaction/README.md 明文「baseline_prompt_stage_D = 阶段 D（商业候选）」），
Decision 用 stage_D 是本档的原生语义，非借用。
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# 仓库根：kernel/decision/llm.py → parents[0]=kernel/decision, [1]=kernel, [2]=仓库根
REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_GENERATION_PARAMETERS_PATH = REPO_ROOT / "contracts" / "interaction" / "generation_parameters.json"

# 端点常量：generation_parameters.json 只钉"供应商 + 模型身份 + 生成参数"，没有端点 URL 字段。
# 不往冻结文件里加键（加键 = 改冻结内容 = 全部 Manifest 指纹失效），所以 URL 落在代码侧常量。
DASHSCOPE_COMPATIBLE_ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
EXPECTED_MODEL_PROVIDER = "Alibaba Cloud DashScope"
API_KEY_ENV = "DASHSCOPE_API_KEY"
# 逐字段读的五个键：缺任一个都直接报错，不给默认值——给默认值等于悄悄换了考试条件。
REQUIRED_PARAM_KEYS = ("model_name", "temperature", "top_p", "seed", "max_tokens_stage_D")
REQUEST_TIMEOUT_SECONDS = 120
REPLAY_PREFIX = "replay:"


def _from_config(default, *names):
    """优先取 kernel/decision/config.py 中的同名常量，取不到就用本文件算出的默认值
    （同 kernel/intent 的折中：不猜符号名、也不让路径真源分叉）。"""
    try:
        from . import config  # 局部 import：config 尚未落盘时不影响本模块被 import
    except ImportError:
        return default
    for name in names:
        value = getattr(config, name, None)
        if value:
            return value
    return default


def load_generation_parameters(path=None):
    """读 contracts/interaction/generation_parameters.json 并返回 dict（只读，不改写、不补默认）。"""
    target = Path(path or _from_config(
        _DEFAULT_GENERATION_PARAMETERS_PATH,
        "GENERATION_PARAMETERS_PATH", "GENERATION_PARAMETERS_JSON", "GENERATION_PARAMETERS",
    ))
    with open(target, encoding="utf-8") as f:
        return json.load(f)


def _build_live_payload(prompt_text, params):
    """按 OpenAI 兼容 chat/completions 组装请求体；生成参数逐字段取自参数文件。"""
    missing = [k for k in REQUIRED_PARAM_KEYS if k not in params]
    if missing:
        raise RuntimeError(
            f"generation_parameters.json 缺少必需字段 {missing}；本层不填默认值（填默认 = 静默改运行条件）"
        )
    provider = params.get("model_provider")
    if provider != EXPECTED_MODEL_PROVIDER:
        raise RuntimeError(
            f"参数文件 model_provider={provider!r}，与本调用层写死的端点（{EXPECTED_MODEL_PROVIDER}）不一致；"
            "换供应商必须同批改端点常量，不得把别家模型名发到这个端点"
        )
    return {
        "model": params["model_name"],
        # 单轮 user 消息：Prompt 全文即对应步骤 prompt 文件的渲染结果。
        # 不加 system 消息——加了就等于运行时又叠了一层没被冻结的指令（B.2.4）。
        "messages": [{"role": "user", "content": prompt_text}],
        "temperature": params["temperature"],
        "top_p": params["top_p"],
        "seed": params["seed"],
        "max_tokens": params["max_tokens_stage_D"],
    }


def _call_live(prompt_text):
    """一次 HTTPS 调用，零重试。返回模型回复正文字符串。"""
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"环境变量 {API_KEY_ENV} 未设置：live 模式需要它，且只接受环境变量注入"
            "（本层不读 .env、不写盘、不打印密钥）。离线自测请用 --replay-step1/2/3。"
        )
    params = load_generation_parameters()
    payload = _build_live_payload(prompt_text, params)
    request = urllib.request.Request(
        DASHSCOPE_COMPATIBLE_ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            # Authorization 只出现在这一行，且从不进任何日志/异常文本
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            detail = "（响应正文读取失败）"
        raise RuntimeError(f"DashScope 调用失败 HTTP {e.code}；响应前 200 字：{detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"DashScope 调用失败（网络层）：{e.reason}；零重试口径，本次运行即失败") from e

    try:
        data = json.loads(body)
        content = data["choices"][0]["message"]["content"]
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"DashScope 响应结构不是预期的 chat/completions 形状（{e}）；响应前 200 字：{body[:200]}") from e
    print(f"[decision.llm] live 回执 model={data.get('model')} id={data.get('id')}", file=sys.stderr)
    if not isinstance(content, str):
        raise RuntimeError(f"模型回复 content 不是字符串：{type(content).__name__}")
    return content


def call_llm(prompt_text, mode):
    """按 mode 取模型原文。mode="live" | "replay:<path>"。

    replay 存在的意义：离线自测（零网络）必须能跑通整条三步编排，且"这次跑的是哪份回复"
    可逐字取证；录制/手写回复放 kernel/decision/fixtures/，不进考卷区。
    """
    if mode == "live":
        return _call_live(prompt_text)
    if mode.startswith(REPLAY_PREFIX):
        replay_path = mode[len(REPLAY_PREFIX):]
        if not replay_path:
            raise ValueError("replay 模式必须写成 replay:<path>，<path> 不得为空")
        with open(replay_path, encoding="utf-8") as f:
            return f.read()
    raise ValueError(f"未知 mode={mode!r}；只接受 'live' 或 'replay:<path>'")


def parse_model_json(raw):
    """剥掉可能的 ``` 围栏后 json.loads，返回 dict。解析失败抛异常并带原文前 200 字。

    只剥围栏，**不做**"从任意文本里正则捞出第一个 {...}"的兜底：那种兜底会把
    「模型没守输出契约」这件事悄悄抹平，让格式违约永远暴露不出来。
    """
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        while lines and lines[-1].strip() == "":
            lines.pop()
        if lines and lines[-1].strip().startswith("```"):
            lines.pop()
        text = "\n".join(lines).strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"模型输出不是合法 JSON（{e}）；原文前 200 字：{raw[:200]}") from e
    if not isinstance(parsed, dict):
        raise ValueError(f"模型输出是 {type(parsed).__name__} 而非 JSON 对象；原文前 200 字：{raw[:200]}")
    return parsed
