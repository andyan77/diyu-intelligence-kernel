"""确定性断言库 v0.1（考卷区——改检测器=改考卷，需审批 C.6.3）。
契约（C.4 铁律1）：每个 check 返回 (verdict, detail)，verdict ∈ {"OK","FAIL","UNKNOWN"}；
证据不足一律 UNKNOWN 向上冒泡（禁止 default:false / 假绿）。L1 只判 FAIL，不产生 PASS。"""
import json, os, re, subprocess, sys

def _texts(obj, out):
    if isinstance(obj, str): out.append(obj)
    elif isinstance(obj, dict): [_texts(v, out) for v in obj.values()]
    elif isinstance(obj, list): [_texts(v, out) for v in obj]
    return out

def schema_valid(output, ctx, **kw):
    schema = ctx.get("output_schema")
    if not schema or not os.path.exists(schema): return "UNKNOWN", f"输出 schema 未配置或不存在: {schema}"
    r = subprocess.run([sys.executable, os.path.join(ctx["repo_root"], "tools/validate_schema.py"), ctx["output_path"], schema], capture_output=True, text=True)
    return ("OK", "schema 校验通过") if r.returncode == 0 else ("FAIL", r.stdout.strip()[:800])

def candidate_count(output, ctx, min=2, **kw):
    c = output.get("candidate_options")
    if c is None: return "UNKNOWN", "candidate_options 字段缺失，无法计数"
    return ("OK", f"候选数 {len(c)} >= {min}") if len(c) >= min else ("FAIL", f"候选数 {len(c)} < 下限 {min}")

def tradeoff_nonempty(output, ctx, **kw):
    t = output.get("comparative_tradeoffs")
    if t is None: return "UNKNOWN", "comparative_tradeoffs 字段缺失"
    if not t or any(not (x.get("tradeoff") or "").strip() for x in t): return "FAIL", "取舍说明为空"
    for c in output.get("candidate_options") or []:
        if not (c.get("why_this_option") or "").strip() or not (c.get("why_not_primary_alternative") or "").strip():
            return "FAIL", f"候选 {c.get('candidate_id')} 缺少 why_this_option / why_not_primary_alternative"
    return "OK", "取舍与选择/放弃理由齐备"

def trace_types_separated(output, ctx, **kw):
    tb = (output.get("trace_bundle") or {}).get("entries")
    if tb is None: return "UNKNOWN", "trace_bundle.entries 缺失，无法核验四类分离"
    idx = {}
    for e in tb:
        if e.get("trace_type") not in ("FACT", "RULE", "ASSUMPTION", "MODEL_JUDGMENT"):
            return "FAIL", f"trace {e.get('trace_id')} 类型非法: {e.get('trace_type')}"
        idx[e.get("trace_id")] = e["trace_type"]
    expect = {"supporting_fact_refs": "FACT", "applied_rule_refs": "RULE", "assumption_refs": "ASSUMPTION", "model_judgment_refs": "MODEL_JUDGMENT"}
    for c in output.get("candidate_options") or []:
        for field, want in expect.items():
            for ref in c.get(field) or []:
                if ref not in idx: return "FAIL", f"候选 {c.get('candidate_id')} 的 {field} 引用了不存在的 trace {ref}"
                if idx[ref] != want: return "FAIL", f"候选 {c.get('candidate_id')} 把 {idx[ref]} 类 trace {ref} 放进了 {field}（四类混写）"
    return "OK", f"{len(idx)} 条 trace 四类分离且引用类型一致"

_NUM = re.compile(r"\d+(?:\.\d+)?")
def numeric_grounding(output, ctx, snapshot_fields=None, threshold=50, **kw):
    """v0.1 语义：输出文本中 >=threshold 的数字必须能在 Context Snapshot（全快照数字集）中找到。
    snapshot_fields 为守卫：这些字段必须存在于快照。阈值防"三个候选/两套穿搭"误报；收紧属改考卷。"""
    snap = ctx.get("snapshot")
    if snap is None: return "UNKNOWN", "context_snapshot 未加载，无法溯源数字"
    for f in snapshot_fields or []:
        if f not in json.dumps(snap, ensure_ascii=False): return "UNKNOWN", f"快照缺少守卫字段 {f}"
    allowed = {float(m) for m in _NUM.findall(json.dumps(snap, ensure_ascii=False))}
    bad = [m for t in _texts(output, []) for m in _NUM.findall(t) if float(m) >= threshold and float(m) not in allowed]
    return ("OK", "输出数字全部可溯源到快照") if not bad else ("FAIL", f"数字无快照来源: {sorted(set(bad))}")

def human_gate_flag(output, ctx, **kw):
    v = output.get("human_selection_required")
    if v is True: return "OK", "human_selection_required=true"
    if v is False: return "FAIL", "human_selection_required=false（绕过人工门）"
    return "UNKNOWN", "human_selection_required 字段缺失（不得默认视为合规）"

def forbidden_expression(output, ctx, lexicon=None, **kw):
    import yaml
    path = os.path.join(ctx["repo_root"], lexicon) if lexicon else None
    if not path or not os.path.exists(path): return "UNKNOWN", f"词表不存在: {lexicon}"
    with open(path, encoding="utf-8") as f: lex = yaml.safe_load(f)
    terms = [t for v in lex.values() if isinstance(v, list) for t in v]
    hits = sorted({t for txt in _texts(output, []) for t in terms if t in txt})
    return ("OK", f"词表 {len(terms)} 词零命中") if not hits else ("FAIL", f"命中禁用表达: {hits}")
