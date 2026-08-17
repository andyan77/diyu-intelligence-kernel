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

# ======================= numeric_grounding v0.3（P0-3 修复批次）=======================
# v0.2 已把数字绑定到「字段路径 + 单位语义」；v0.3 堵的是 v0.2 自身被实测撞出的六条旁路：
#   ① 单位窗口只看紧邻一个字符 → 「库存 120 余件 / 多件 / 来件 / （件）」全部退回裸数字兜底，跨类禁令消失
#   ② 量级词 万/亿 单独成串被当数值（『120 万件』= 120 + 0；『库存一亿件』只抽到「一」后被当构词丢弃）
#   ③ _path_class 对整条路径做子串包含 → 单字关键词「元/码/尺」制造双向误分类（内容单元数→price）
#   ④ 无符号位、无全角归一 → 「-800 件」符号翻转过关；「3，980 元」被切成 3 与 980 误报
#   ⑤ 中文数字口语省略尾数（一千二 / 两百五）被硬转成 1002 / 205；成语（千万 / 万一）被当数量
#   ⑥ 中文量词（这一件 / 上市第一天 / 两件套）被当事实计数，服装文案必然假红
# 纪律：解析不出确定数值又紧邻事实单位/线索词 → UNKNOWN 向上冒泡，**不静默丢弃**（丢弃 = 编造数字判过）。
#
# 溯源粒度声明（**类级，不是实例级**——L3 人工判分面，不得被读成已覆盖）：
#   本检测器判的是「输出里的数字能否在快照的**同类**字段中找到同值」，不绑定实体实例。
#   即：快照中 P77 的价格 3980，输出写成「另一款风衣也卖 3980 元」同样判 OK——把 A 款价格安到 B 款上，
#   本检测器看不见。该风险属 B.1.5 / C.5 的 L3 人工判分面，PENDING_HUMAN 不等于已覆盖它。
#   同一声明已写入 acceptance/cases/BD-D01/case.yaml 的 A5 行注释（考卷侧同源留痕）。
_NUM_V2 = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")      # 支持千分位，修 v0.1「3,980 元」误报
_CN_RUN = re.compile(r"[零一二两三四五六七八九十百千万亿]+")
# 标识符/时间戳的构成字符（含 ':'，使 ISO 时间戳 2026-08-17T00:00:00Z 被识别为单个标识符整体）
_TOKEN_CHARS = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-./:")
_ASCII_ALPHA = re.compile(r"[A-Za-z]")
_SPACES = " \t\xa0　"
_SIGNS = "-−－"

# 全角归一：只做**定点**替换，不用 unicodedata.NFKC（NFKC 会连带重写兼容汉字/罗马数字等无关字符，
# 在中文文案里放大误伤面）。全角逗号只在「千分位位置」归一——前面是数字、后面恰好三位数字且再无数字。
# 已知歧义并留痕：`800，900`（全角逗号当列举分隔）会被归一成 800900 → 该值不在快照池 → 判红。
# 这是**假红**方向（宁可多报不漏报），不构成假绿；真出现时按 L3 人工判分处理。
_FW_MAP = {ord(a): b for a, b in zip("０１２３４５６７８９％（）［］：－−",
                                     "0123456789%()[]:--")}
_FW_COMMA_RE = re.compile(r"(?<=\d)，(?=\d{3}(?!\d))")

def _normalize(text):
    return _FW_COMMA_RE.sub(",", text.translate(_FW_MAP))

_FACT_CLASSES = ("price", "inventory", "duration", "percent", "size")
# 数后（跳过量级词/模糊量词/左括号后）的事实单位 → 事实类；数前的货币符号见 _PREFIX_UNIT
_SUFFIX_UNIT = {"件": "inventory", "元": "price", "折": "price", "周": "duration",
                "天": "duration", "%": "percent", "％": "percent", "码": "size"}
_PREFIX_UNIT = {"¥": "price", "￥": "price"}
# 泛量词：计数语义，不是可溯源事实 → 豁免（防「三个候选 / 两套穿搭」误报）
_GENERIC_QUANT = set("个套句条张位步项次组款种")
# 量级词：与**前面**的数值相乘，不得单独成数（『120 万件』= 1200000 件，不是 120 与 0 两个数）
_MAGNITUDE = {"百": 100, "千": 1000, "万": 10000, "亿": 100000000}
# 模糊量词：数字与单位之间的插入字，跳过后继续找单位（『120 余件 / 多件 / 来件』）
_FUZZY_AFTER = set("余多来几起整")
_FUZZY_AFTER_PAIRS = ("左右", "上下", "出头", "以上", "以下", "开外")
_OPEN_BRACKET = set("([{【「《〈")
# 序数/指示词：其后的小数值是量词用法不是事实计数（这一件 / 上市第一天 / 第 3 天）。
# 只对 |值| ≤ 10 生效——否则「这 1200 件」就成了绕过通道。
_ORDINAL_LEFT = set("第这那每首本该各另")
# 左侧事实线索词：单位前置或省略后缀时（库存：3980 / 库存数 3980 / 库存 120）同样按事实类判定，
# 且**禁止**退回 any_pool 兜底——「无单位裸数字命中快照任意值即可」正是跨类借位的最后一个出口。
_LEFT_CUE = (
    ("inventory", ("库存", "存货", "现货", "备货", "在库", "剩余")),
    ("price",     ("价格", "售价", "吊牌", "标价", "单价", "活动价", "原价", "成交价", "定价")),
    ("duration",  ("周期", "工期", "时长", "账期", "交期")),
    ("size",      ("尺码", "尺寸", "胸围", "肩宽", "衣长", "袖长", "腰围")),
    ("percent",   ("折扣", "转化率", "毛利率", "占比", "百分比")),
)
_LEFT_WINDOW = 6
_SENTENCE_STOP = set("。！？!?；;\n\r")

# 路径分类：**逐段**匹配 + 词边界，不对 '.'.join 后的整串做 `in`。
# 单字关键词「元/码/尺/周/天」已从路径规则中删除——它们只应作为**单位**参与 _unit_context /
# _unit_text_class；留在路径里会制造「内容单元数→price」「款式编码→size」这类双向误分类。
_PATH_CLASS_CN = (
    ("price",     ("价格", "售价", "吊牌", "标价", "单价", "活动价", "原价", "成交价", "定价", "金额")),
    ("inventory", ("库存", "存货", "现货", "备货", "在库")),
    ("duration",  ("周期", "工期", "时长", "天数", "周数", "账期", "交期")),
    ("percent",   ("百分比", "占比", "比率", "转化率", "毛利率", "折扣")),
    ("size",      ("尺码", "尺寸", "胸围", "肩宽", "衣长", "袖长", "腰围", "码数")),
)
# ASCII 段按 [^a-z0-9] 切词后做**全词**匹配（deadline 不再命中 duration，holidays 不再命中 days）
_PATH_CLASS_EN = (
    ("price",     {"price", "prices", "msrp", "cny", "rmb"}),
    ("inventory", {"inventory", "stock", "onhand"}),
    ("duration",  {"duration", "weeks", "days", "cycle", "lead"}),
    ("percent",   {"percent", "percentage", "ratio", "rate"}),
    ("size",      {"size", "sizes", "measurement", "measurements", "bust", "shoulder"}),
)
_EN_WORD_RE = re.compile(r"[a-z0-9]+")
# 元数据字段（ID / 日期 / 版本 / 来源 / 引用）不得成为事实类溯源源，只进「任意值」兜底池，
# 这是「禁跨商品、日期、版本、尺码借位」的关键——例如 price.as_of=2026-08-17 不能给价格背书。
_META_EXACT = {"as_of", "source", "sources", "currency", "unit", "units", "version",
               "schema_version", "id", "type", "status", "note", "date", "time", "index", "idx"}
_META_SUFFIX = ("_id", "_at", "_ref", "_refs", "_type", "_status", "_version",
                "note", "_url", "_uri", "_path", "_paths")
_VALUE_KEYS = {"value", "amount", "qty", "quantity", "count", "number", "num"}
_CN_DIGIT = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
_CN_UNIT = {"十": 10, "百": 100, "千": 1000}
# 成语/叠词停用表：这些串是修辞不是数量（千万别 / 万一 / 一二线 / 三三两两）
_CN_STOPWORDS = frozenset(["千万", "万一", "一二", "二三", "三两", "七八", "八九",
                           "三三两两", "七七八八", "百十", "百八十", "一二三", "十万八千"])

def _cn_to_num(s):
    """中文数字 → float；**不可解析或有歧义一律返回 None**（由上层记 UNKNOWN，禁硬转）。

    正例：一千二百→1200 / 八百→800 / 六→6 / 十五→15 / 十万→100000 / 一亿→100000000 / 一百零五→105。
    返回 None 的三类（v0.2 取值错误的本体）：
      ① 口语省略尾数：一千二（口语 1200 / 字面 1002）、两百五（口语 250 / 字面 205）——二义，不硬转；
      ② 光杆量级词：万 / 千万 / 百——不是数量（v0.2 把「万」算成 0，配合任意值兜底制造过假绿）；
      ③ 停用成语/叠词：见 _CN_STOPWORDS。
    """
    if s in _CN_STOPWORDS:
        return None
    result = section = number = 0
    seen_digit = False
    last_unit = 0
    zero_marker = False
    for ch in s:
        if ch in _CN_DIGIT:
            if ch == "零":
                zero_marker = True
            number = _CN_DIGIT[ch]
            seen_digit = True
        elif ch in _CN_UNIT:
            section += (number or 1) * _CN_UNIT[ch]
            number = 0
            last_unit = _CN_UNIT[ch]
            zero_marker = False
        elif ch == "万":
            result += (section + number) * 10000
            section = number = 0
            last_unit = 10000
            zero_marker = False
        elif ch == "亿":
            result = (result + section + number) * 100000000
            section = number = 0
            last_unit = 100000000
            zero_marker = False
        else:
            return None
    # ② 光杆量级词：整串无任何数字字、也无「十」定位，却含百/千/万/亿 → 不是数量。
    #    （「万」「千万」「百万」属此类；「十万」「十亿」有「十」作十位定位，是确定数量，照算。）
    if not seen_digit and "十" not in s and any(c in "百千万亿" for c in s):
        return None
    # ① 口语省略尾数：末位是裸数字、前面最近的单位 ≥ 百、且中间没有「零」定位 → 二义
    if number and last_unit >= 100 and not zero_marker:
        return None
    total = result + section + number
    return float(total) if (seen_digit or last_unit) else None

def _unit_context(text, start, end):
    """返回 (kind, cls, scale, ordinal, mag_end)。

    kind ∈ {"fact","generic",None}；scale = 右侧量级词连乘（120 万 → ×10000）；
    ordinal=True 表示左侧紧邻序数/指示词；mag_end = 量级词吃掉后的位置（供调用方推进游标，
    避免『120 万』里的「万」被中文数字流重复计一次）。
    优先级：右侧事实单位 > 右侧泛量词 > 左侧货币符号 > 左侧事实线索词。
    """
    n = len(text)
    scale = 1.0
    j = end
    while True:                                   # ① 量级词（可连乘：3 千万）
        k = j
        while k < n and text[k] in _SPACES:
            k += 1
        if k < n and text[k] in _MAGNITUDE:
            scale *= _MAGNITUDE[text[k]]
            j = k + 1
            continue
        break
    mag_end = j
    k, steps = j, 0                               # ② 右窗口：跳过空白/模糊量词/左括号后再找单位
    while k < n and steps < 4:
        if text[k] in _SPACES or text[k] in _FUZZY_AFTER or text[k] in _OPEN_BRACKET:
            k += 1; steps += 1; continue
        if text[k:k + 2] in _FUZZY_AFTER_PAIRS:
            k += 2; steps += 1; continue
        break
    kind = cls = None
    if k < n:
        c = text[k]
        if c in _SUFFIX_UNIT:
            nxt = text[k + 1] if k + 1 < n else ""
            if nxt in _GENERIC_QUANT:             # 两件套 / 三件装：复合量词，不是事实计数
                kind = "generic"
            else:
                kind, cls = "fact", _SUFFIX_UNIT[c]
        elif c in _GENERIC_QUANT:
            kind = "generic"
    i = start - 1                                 # ③ 左侧
    while i >= 0 and text[i] in _SPACES:
        i -= 1
    ordinal = i >= 0 and text[i] in _ORDINAL_LEFT
    if kind is None:
        if i >= 0 and text[i] in _PREFIX_UNIT:
            kind, cls = "fact", _PREFIX_UNIT[text[i]]
        else:
            lo, win = start, []
            while lo > 0 and len(win) < _LEFT_WINDOW:
                ch = text[lo - 1]
                if ch in _SENTENCE_STOP:
                    break
                win.append(ch); lo -= 1
            left = "".join(reversed(win))
            for cue_cls, words in _LEFT_CUE:
                if any(w in left for w in words):
                    kind, cls = "fact", cue_cls
                    break
    return kind, cls, scale, ordinal, mag_end

def _in_identifier(text, start, end):
    """数字是否嵌在字母数字标识符里（S1 / IMG_0565 / ACC-HXJ-001 / B.4.2 / v0.1）。"""
    i, j = start, end
    while i > 0 and text[i - 1] in _TOKEN_CHARS: i -= 1
    while j < len(text) and text[j] in _TOKEN_CHARS: j += 1
    return bool(_ASCII_ALPHA.search(text[i:j]))

def _signed_value(text, start, raw):
    """把紧邻左侧的负号并入数值。前一位是标识符字符（2026-08-17 的 '-'）时不算符号位。"""
    v = float(raw.replace(",", ""))
    if start > 0 and text[start - 1] in _SIGNS:
        prev2 = text[start - 2] if start >= 2 else ""
        if prev2 == "" or prev2 not in _TOKEN_CHARS:
            return -v
    return v

def _iter_numbers(text):
    """阿拉伯数字流与中文数字流按位置合并，产出 (start, end, raw, is_cn)。调用方用游标去重。"""
    toks = [(m.start(), m.end(), m.group(), False) for m in _NUM_V2.finditer(text)]
    toks += [(m.start(), m.end(), m.group(), True) for m in _CN_RUN.finditer(text)]
    toks.sort(key=lambda t: (t[0], t[1]))
    return toks

def _text_numbers_out(text):
    """输出侧提取：返回 (numbers, unresolved)。

    numbers = [(value, fact_class|None)]；标识符内数字跳过；泛量词与序数量词豁免；
    单字中文数字且无单位视为构词（唯一 / 一致 / 二者）不作数量。
    unresolved = [原文串]——中文数字**紧邻事实单位或左侧事实线索词**却解析不出确定数值
    （口语省略尾数 / 光杆量级词），按三态纪律交由上层冒 UNKNOWN，禁止静默丢弃。
    """
    text = _normalize(text)
    found, unresolved, cursor = [], [], 0
    for s, e, raw, is_cn in _iter_numbers(text):
        if s < cursor:
            continue
        if not is_cn and _in_identifier(text, s, e):
            cursor = e
            continue
        kind, cls, scale, ordinal, mag_end = _unit_context(text, s, e)
        cursor = max(e, mag_end)
        if kind == "generic":
            continue
        if is_cn:
            # 成语/叠词是修辞不是数量：与泛量词同档静默豁免，**不**进 unresolved
            # （否则「三两件外套」这类日常说法会把整条断言拖成 UNKNOWN = 噪音）。
            if raw in _CN_STOPWORDS:
                continue
            v = _cn_to_num(raw)
            if v is None:
                if kind == "fact":
                    unresolved.append(raw)
                continue
            if cls is None and len(raw) == 1:
                continue
        else:
            v = _signed_value(text, s, raw)
        v *= scale
        if ordinal and abs(v) <= 10:
            continue
        found.append((v, cls))
    return found, unresolved

def _text_numbers_snap(text):
    """快照侧提取：宽松（标识符内数字也收，泛量词也收），只用于放宽可溯源集合。"""
    text = _normalize(text)
    found, cursor = [], 0
    for s, e, raw, is_cn in _iter_numbers(text):
        if s < cursor:
            continue
        kind, cls, scale, _ordinal, mag_end = _unit_context(text, s, e)
        cursor = max(e, mag_end)
        if is_cn:
            v = _cn_to_num(raw)
            if v is None:
                continue
        else:
            v = _signed_value(text, s, raw)
        found.append((v * scale, cls if kind == "fact" else None))
    return found

def _path_class(segs):
    """逐段 + 词边界分类。任一段命中元数据判据即整条路径退出事实类（只进任意值兜底池）。"""
    for s in segs:
        s = str(s).lower()
        if s in _META_EXACT or s.endswith(_META_SUFFIX): return None
    for seg in segs:
        seg = str(seg).lower()
        for cls, keys in _PATH_CLASS_CN:
            if any(k in seg for k in keys):          # 中文关键词均为多字，段内包含即可
                return cls
        words = set(_EN_WORD_RE.findall(seg))
        for cls, keys in _PATH_CLASS_EN:
            if words & keys:                          # ASCII 走全词匹配，不做子串包含
                return cls
    return None

def _unit_text_class(s):
    s = s.lower()
    for token, cls in (("元", "price"), ("cny", "price"), ("rmb", "price"), ("¥", "price"), ("￥", "price"),
                       ("件", "inventory"), ("pcs", "inventory"),
                       ("周", "duration"), ("天", "duration"), ("day", "duration"), ("week", "duration"),
                       ("%", "percent"), ("percent", "percent"),
                       ("码", "size"), ("cm", "size")):
        if token in s: return cls
    return None

# 夹具注释约定：`_` 开头的键是**注释/元数据**（_fixture_note 等），两侧一律不参与判定。
# 理由：注释文字里的数字既不该给输出背书（快照侧），也不该被当成模型编造（输出侧）——
# 让说明文字影响判定 = 判定依赖非考试条件。A 合同的输出对象字段无下划线前缀，故不误伤真实字段。
def _is_annotation_key(k):
    return str(k).startswith("_")

def _collect_snapshot(node, segs, acc, keys, paths, hint=None):
    paths.add(".".join(str(s) for s in segs))
    if isinstance(node, dict):
        sib = None
        for uk in ("unit", "units", "currency"):
            u = node.get(uk)
            if isinstance(u, str): sib = _unit_text_class(u) or sib
        for k, v in node.items():
            if _is_annotation_key(k): continue
            keys.add(str(k))
            _collect_snapshot(v, segs + [k], acc, keys, paths, sib if str(k) in _VALUE_KEYS else None)
    elif isinstance(node, list):
        for i, v in enumerate(node): _collect_snapshot(v, segs + [i], acc, keys, paths, hint)
    elif isinstance(node, bool) or node is None:
        return
    elif isinstance(node, (int, float)):
        acc.append((float(node), _path_class(segs) or hint))
    elif isinstance(node, str):
        pcls = _path_class(segs)
        for v, ucls in _text_numbers_snap(node): acc.append((v, ucls or pcls or hint))

def _collect_output(node, segs, acc, unresolved):
    if isinstance(node, dict):
        for k, v in node.items():
            if _is_annotation_key(k): continue
            _collect_output(v, segs + [k], acc, unresolved)
    elif isinstance(node, list):
        for i, v in enumerate(node): _collect_output(v, segs + [i], acc, unresolved)
    elif isinstance(node, bool) or node is None:
        return
    elif isinstance(node, (int, float)):
        acc.append((float(node), _path_class(segs), ".".join(str(s) for s in segs)))
    elif isinstance(node, str):
        p = ".".join(str(s) for s in segs); pcls = _path_class(segs)
        nums, unres = _text_numbers_out(node)
        for v, ucls in nums: acc.append((v, ucls or pcls, p))
        for raw in unres: unresolved.append((raw, p))

def _nk(v): return round(float(v), 6)
def _fmt(v): return str(int(v)) if float(v).is_integer() else ("%.6g" % v)

def numeric_grounding(output, ctx, snapshot_fields=None, threshold=0, **kw):
    """v0.3 语义（P0-3 修复批次；改检测器=改考卷，需审批 C.6.3）：数字绑定「字段路径 + 单位」溯源，禁跨类借位。

    快照侧：递归收集 (数值, 字段路径)，按路径**逐段词边界**分类 price / inventory / duration / percent /
      size / 其他；JSON 数值型与字符串内数字都收；`{value, unit|currency}` 同级单位参与分类；
      ID / 日期 / 版本 / 来源 / 引用等元数据路径只进「任意值」兜底池，不给事实类背书。
    输出侧：提取阿拉伯数字（含千分位、负号、全角）与中文数字（零一二两三四五六七八九十百千万亿）；
      单位上下文取**右侧窗口**（先吃量级词 百/千/万/亿 与前值相乘，再跳过模糊量词 余/多/来/左右…
      与左括号，然后认 件/元/周/天/%/折/码）与**左侧窗口**（货币符号 ¥/￥；事实线索词 库存/售价/
      尺码/周期… 6 字内）；嵌在字母数字标识符里的数字（S1 / IMG_0565 / ACC-HXJ-001）跳过；
      泛量词（个套句条张位步项次组款种）与序数量词（这一件 / 第一天，|值| ≤ 10）豁免。
    判定：带事实类归属的数字必须命中「同类」字段路径的快照值——跨类命中不算（尺码 120 不能给
      「库存 120 件」「库存 120 余件」背书），且无论大小（49 元也查，不设阈值豁免）；
      **只有左右窗口都无事实线索的裸数字**才回退到「命中快照任意值即可」的兜底池。
    三态：中文数字紧邻事实单位/线索词却解析不出确定数值（一千二 / 两百五 / 光杆量级词）→ UNKNOWN
      向上冒泡；输出不是结构化对象或为空 → UNKNOWN。禁止静默丢弃、禁 default:false。
    ⚠ 溯源粒度是**类级不是实例级**：跨实体同类同值借位（A 款价格安到 B 款）本检测器看不见，
      属 L3 人工判分面（同声明见本文件 v0.3 段首与 BD-D01/case.yaml A5 行注释）。
    threshold：v0.2 起**仅**作用于「无单位裸数字」的下限，默认 0（全查）；对带事实单位的数字无效。
    snapshot_fields：守卫，这些字段必须作为快照的键 / 路径存在，否则 UNKNOWN 向上冒泡（禁 default:false）。
    """
    snap = ctx.get("snapshot")
    if snap is None: return "UNKNOWN", "context_snapshot 未加载，无法溯源数字"
    if not isinstance(output, (dict, list)):
        return "UNKNOWN", f"输出不是结构化对象（实得 {type(output).__name__}），无法逐字段溯源"
    if len(output) == 0:
        return "UNKNOWN", "输出为空（无任何字段/元素），无从逐字段溯源——空输出不等于已溯源"
    snap_nums, snap_keys, snap_paths = [], set(), set()
    _collect_snapshot(snap, [], snap_nums, snap_keys, snap_paths)
    for f in snapshot_fields or []:
        f = str(f)
        if not (f in snap_keys or f in snap_paths or any(p == f or p.startswith(f + ".") for p in snap_paths)):
            return "UNKNOWN", f"快照缺少守卫字段 {f}（v0.2 按键/路径核验，不再子串匹配）"
    pools = {c: set() for c in _FACT_CLASSES}
    any_pool = set()
    for v, cls in snap_nums:
        any_pool.add(_nk(v))
        if cls in pools: pools[cls].add(_nk(v))

    out_nums, unresolved = [], []
    _collect_output(output, [], out_nums, unresolved)
    bad = []
    for v, cls, path in out_nums:
        if cls in pools:
            if _nk(v) not in pools[cls]:
                bad.append((v, f"{_fmt(v)}（{cls} 类无同类快照来源 @ {path}）"))
        else:
            if float(v) < float(threshold): continue
            if _nk(v) not in any_pool:
                bad.append((v, f"{_fmt(v)}（裸数字无快照来源 @ {path}）"))
    if bad:
        # 硬 FAIL 优先于 UNKNOWN：已确证的无源数字是比「无从核验」更强的证据，不得被冒泡掩盖。
        seen, msgs = set(), []
        for v, m in sorted(bad, key=lambda x: x[0]):
            if m in seen: continue
            seen.add(m); msgs.append(m)
        detail = "数字无快照来源: " + "; ".join(msgs)
        if unresolved:
            detail += "；另有 %d 处中文数字无从解析（见 UNKNOWN 口径）" % len(unresolved)
        return "FAIL", detail[:800]
    if unresolved:
        items = "; ".join(f"{raw} @ {path}" for raw, path in unresolved[:5])
        return "UNKNOWN", ("中文数字紧邻事实单位/线索词但解析不出确定数值（口语省略尾数 / 光杆量级词 / 成语），"
                           f"无从溯源，共 {len(unresolved)} 处: {items}")[:800]
    if not out_nums:
        return "OK", (f"输出中未发现任何数字（**非等同于**已溯源：只是没有可查的数字；"
                      f"快照数字 {len(any_pool)} 个）")
    return "OK", f"输出 {len(out_nums)} 处数字全部可溯源到快照同类字段（快照数字 {len(any_pool)} 个）"
# ===================== numeric_grounding v0.3 结束 =====================

def human_gate_flag(output, ctx, **kw):
    v = output.get("human_selection_required")
    if v is True: return "OK", "human_selection_required=true"
    if v is False: return "FAIL", "human_selection_required=false（绕过人工门）"
    return "UNKNOWN", "human_selection_required 字段缺失（不得默认视为合规）"

def forbidden_expression(output, ctx, lexicon=None, **kw):
    """词表零命中 → OK；命中 → FAIL；**词表解析出 0 个词条 → UNKNOWN**（禁空词表假绿）。

    空词表假绿本体：terms 为空时 hits 必空，于是「清仓甩卖白菜价」也会返回 ('OK','词表 0 词零命中')。
    词表结构一漂移（某键的值从 list 变成 dict、或整份词表为空），禁用表达检测就整体失效且无人知晓
    ——这正是铁律「无检测器不得判 PASS」要拦的形态，故改为三态：无词条 = 无从核验 = UNKNOWN。
    """
    import yaml
    path = os.path.join(ctx["repo_root"], lexicon) if lexicon else None
    if not path or not os.path.exists(path): return "UNKNOWN", f"词表不存在: {lexicon}"
    with open(path, encoding="utf-8") as f: lex = yaml.safe_load(f)
    if not isinstance(lex, dict):
        return "UNKNOWN", f"词表 {lexicon} 顶层不是映射对象（实得 {type(lex).__name__}），禁用表达无从核验"
    terms, malformed = [], []
    for k, v in lex.items():
        if isinstance(v, list):
            terms.extend(t for t in v if isinstance(t, str) and t.strip())
        else:
            malformed.append(str(k))
    if not terms:
        return "UNKNOWN", (f"词表 {lexicon} 解析出 0 个词条，禁用表达无从核验"
                           + (f"（结构异常键: {malformed}）" if malformed else ""))
    hits = sorted({t for txt in _texts(output, []) for t in terms if t in txt})
    if hits:
        return "FAIL", f"命中禁用表达: {hits}"
    if malformed:
        return "UNKNOWN", (f"词表 {lexicon} 有 {len(malformed)} 个键的值不是列表（{malformed}），"
                           f"这部分词条未参与核验——已核验的 {len(terms)} 词零命中，但覆盖面残缺")
    return "OK", f"词表 {len(terms)} 词零命中"
