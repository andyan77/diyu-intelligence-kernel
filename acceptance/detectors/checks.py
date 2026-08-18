"""确定性断言库 v0.5（考卷区——改检测器=改考卷，需审批 C.6.3）。
契约（C.4 铁律1）：每个 check 返回 (verdict, detail)，verdict ∈ {"OK","FAIL","UNKNOWN"}；
证据不足一律 UNKNOWN 向上冒泡（禁止 default:false / 假绿）。L1 只判 FAIL，不产生 PASS。

版本变更史（版本号是给回执 provenance 用的区分力，内容变了就必须升——见 tools/run_case.py
detectors_version / tools/coverage.py detectors_version，两处都读本 docstring 首行）：
  v0.1 → v0.2（M1-EP02 修复批次）：只动新增的四个 intent_* 检测器，既有 BD 侧函数一字未改。
    ① intent_blocking_gate / intent_assumption_coverage 的「缺失集合」改为**并集**
       （missing_context ∪ required_context 中 availability∈{MISSING,CONFLICTING} 的项），
       堵「把阻断项只写进 required_context、missing_context 留空」的绕闸通道；
    ② intent_assumption_coverage 的 statement 子串**兜底命中降为 UNKNOWN**
       （只有 target_paths 精确含 field_path 才算已对应）。
  v0.2 → v0.3（校准修订批②，Founder 2026-08-18 判分批批准，负向测试先行 tools/test_detectors.py ㉒）：
    只动 numeric_grounding（自身语义版 v0.3→v0.4），两处收敛误报、真阳性零放松：
    ① 量词与成语里的单字「一」不作数字提取（一致/一类/一件——RUN-0006/0007/0008 三红实证）；
    ② 系统留痕字段（confidence.basis / confidence.limiting_factors / *.resolution_question）内的
       合同条款号（约束5 / A.5.2 / B:285-286 / §四）豁免；同字段其他数字照查（㉒-g 护栏）。
  v0.3 → v0.4（校准批二，Founder 2026-08-18 复判批第⑥条产品标准，负向测试先行 tools/test_detectors.py ㉔）：
    **只新增** intent_situational_alternative 一个函数，既有检测器一字未改（含 numeric_grounding
    与防编造面全部护栏）——机器面判「系统已知的重大经营情境该并呈却没并呈／被擅自转向」。
  v0.4 → v0.5（校准批二尾批，Founder 2026-08-18 **数字表达裁决**＝C.6.3 改检测器批准，
    负向测试先行 tools/test_detectors.py ㉕；先红证据＝新 18 条期望在旧检测器下 8 项不符，
    其中 5 项是**假绿**：「10%以上」「约10%」「3980元左右」「接近800件」「大概3980元」）：
    只动 numeric_grounding（自身语义版 v0.4→v0.5），新增**保守概括通道**（封闭清单）：
    ① 下界「X以上／不低于X／至少X／超过X」——放行当且仅当 X ≤ 同类快照**最小值**；
    ② 上界「不超过X／X以下／最多X」——放行当且仅当 X ≥ 同类快照**最大值**；
    ③ 原值区间与原值列举照旧走逐值精确命中，本通道不介入；
    ④ 「约／大约／接近／大概／差不多／左右／上下／前后」等**不可判定形式一律判红**，
       即使数值碰巧在快照池内（本案实证：商品名「10%羊绒风衣式大衣」把 10 送进 percent 池）；
    ⑤ **带界标记时按界判，精确命中不再免责**——反方向取整（9.2 →「10%以上」）判红。
    射程边界（如实登记，不得据本通道宣称近似表达已全面可判）：池是**类级**的，同类内混装不同
    对象的数值时（percent 池同时含山羊绒 9.x 与绵羊毛 90.x），针对子集的真陈述会被判红＝**假红**
    方向（㉕-s 用例钉死）；概括通道**只对事实类数字生效**，无单位裸数字仍走原「命中任意值」口径。
"""
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

# ---- 保守概括通道（Founder 2026-08-18 数字表达裁决；本裁决即 C.6.3 改检测器批准）----
# 封闭清单，只此四形：a)「X以上／不低于X」需 X ≤ 同类快照**最小值**；b)「不超过X／X以下」需 X ≥ 同类
# **最大值**；c) 原值区间「min–max」与 d) 原值列举——后两形本就走逐值精确命中，无需本通道。
# 方向硬性保守：下界只许往低取、上界只许往高取，反方向取整（9.2 →「10%以上」）判红。
# **带界标记时按界判，精确命中不再免责**：本案实证——商品名「10%羊绒风衣式大衣」把 10 送进了 percent
# 池，旧口径下「10%以上」「约10%」双双假绿；新口径下两者都红（前者不保守，后者不可判定）。
# 「约／大约／接近／大概／差不多／左右／上下」等不可判定形式**维持禁止**，即使数值碰巧在池内。
_BOUND_LEFT = (("不低于", "LOWER"), ("不超过", "UPPER"), ("不高于", "UPPER"), ("差不多", "VAGUE"),
               ("至少", "LOWER"), ("最多", "UPPER"), ("超过", "LOWER"), ("高于", "LOWER"),
               ("大于", "LOWER"), ("低于", "UPPER"), ("小于", "UPPER"), ("大约", "VAGUE"),
               ("约莫", "VAGUE"), ("接近", "VAGUE"), ("大概", "VAGUE"), ("估计", "VAGUE"),
               ("约", "VAGUE"), ("≥", "LOWER"), ("≤", "UPPER"))
_BOUND_RIGHT = (("及以上", "LOWER"), ("或以上", "LOWER"), ("及以下", "UPPER"), ("以上", "LOWER"),
                ("以下", "UPPER"), ("以内", "UPPER"), ("封顶", "UPPER"), ("左右", "VAGUE"),
                ("上下", "VAGUE"), ("前后", "VAGUE"))
_BOUND_SKIP_RIGHT = set("及或")

def _bound_qualifier(text, start, end, mag_end):
    """返回 (kind, marker)，kind ∈ {"LOWER","UPPER","VAGUE",None}。

    左侧标记必须**紧贴**数字（endswith，只跳空白）——否则「按约束5」里的「约」会把条款号
    误判成近似表达；右侧标记必须**紧跟**数字/量级词/单位之后（startswith，跳空白与「及/或」）。
    两侧都命中时 VAGUE 优先（「大约9%以上」自相矛盾，按不可判定＝判红方向处理）；同侧多标记
    取最长（「不超过」压过「超过」，元组已按长度手排）。
    诚实边界：紧贴数字的构词「约」（如「预约3天」）会被判成近似表达＝**假红**方向，写原值可规避；
    「最近3天」不入列（已剔除裸「近」，避免高频时间说法被误伤）。
    """
    n = len(text)
    i = start
    while i > 0 and text[i - 1] in _SPACES:
        i -= 1
    left = text[max(0, i - 6):i]
    j = max(end, mag_end)
    while j < n and text[j] in _SPACES:
        j += 1
    if j < n and text[j] in _SUFFIX_UNIT:          # 跳过单位本身（9「%」以上 / 800「件」以上）
        j += 1
    while j < n and (text[j] in _SPACES or text[j] in _BOUND_SKIP_RIGHT):
        j += 1
    right = text[j:j + 6]
    hits = []
    for marker, kind in _BOUND_LEFT:
        if left.endswith(marker):
            hits.append((kind, marker)); break
    for marker, kind in _BOUND_RIGHT:
        if right.startswith(marker):
            hits.append((kind, marker)); break
    for kind, marker in hits:
        if kind == "VAGUE":
            return kind, marker
    return hits[0] if hits else (None, None)

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
            # v0.4（Founder 判分批裁决）：量词/成语里的单字「一」即使被窗口线索词或单位归了类
            # 也不作数量——「库存数据一致」「照片一类」「为一件大衣」全是构词不是数量主张。
            # 诚实边界：「库存只有一件」的真实数量主张因此同样免检（裁决接受的盲区）；
            # 阿拉伯数字与多字中文数量（三千件）仍全程在射程（㉒-f/h 护栏钉死）。
            if raw == "一":
                continue
        else:
            v = _signed_value(text, s, raw)
        v *= scale
        if ordinal and abs(v) <= 10:
            continue
        found.append((v, cls) + _bound_qualifier(text, s, e, mag_end))
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

# v0.4（Founder 判分批裁决）：系统留痕字段的值由确定性系统代码生成（闸留痕/限制因子/追问模板句），
# 里面的合同条款号（约束5 / A.5.2 / B:285-286 / §四）是引用不是经营数字。豁免**只**发生在这些
# 路径上、**只**剥条款号模式；同字段里冒出的其他数字（如无源价格）照查（㉒-g 护栏钉死）。
_SYS_TRACE_HEADS = (("confidence", "basis"), ("confidence", "limiting_factors"))
_CLAUSE_REF_RE = re.compile(r"(约束\s*\d+|§\s*[一二三四五六七八九十\d]+|[A-Za-z]+\.\d+(?:\.\d+)*|[A-Za-z]+:\d+(?:-\d+)?)")

def _is_sys_trace_path(segs):
    if segs and str(segs[-1]) == "resolution_question": return True
    return any(len(segs) >= len(h) and tuple(str(s) for s in segs[:len(h)]) == h for h in _SYS_TRACE_HEADS)

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
        # JSON 数值型没有文本上下文，界标记恒 None（数字本身不会自带「以上」）
        acc.append((float(node), _path_class(segs), None, None, ".".join(str(s) for s in segs)))
    elif isinstance(node, str):
        p = ".".join(str(s) for s in segs); pcls = _path_class(segs)
        nums, unres = _text_numbers_out(_CLAUSE_REF_RE.sub(" ", node) if _is_sys_trace_path(segs) else node)
        for v, ucls, qkind, qmark in nums: acc.append((v, ucls or pcls, qkind, qmark, p))
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
    **v0.5 保守概括通道（Founder 2026-08-18 数字表达裁决，封闭清单四形）**：数字带「界标记」时
      改按界判，不再看是否精确命中——下界（以上/不低于/至少/超过/≥）须 X ≤ 同类最小值，
      上界（不超过/以下/最多/≤）须 X ≥ 同类最大值，方向反了判红；「约/接近/大概/左右」等
      不可判定形式一律判红（碰巧在池内也不免责）。原值区间与原值列举不经本通道，照走精确命中。
      本通道**只对事实类数字生效**；裸数字维持原口径。判据实现见 _bound_qualifier。
      ⚠ 池是类级的：percent 池混装山羊绒 9.x 与绵羊毛 90.x，针对子集的真陈述会被判红（假红方向）。
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

    # ---- 明示夸张标注通道（Founder 2026-08-18 内容真实性三层边界裁决 R2；改检测器=改考卷，本批为裁决授权）----
    # 只做标注位，零识别智能：检测器不判断「是否真是艺术夸张」，只认输出对象自带的
    # `_explicit_exaggeration` 数组（元素 = 数值或数字字符串）。被标注的数字免于无源判 FAIL，
    # 但必须留痕（detail 显式列出豁免了哪些）；未标注的照拦。`_` 前缀键不进 out_nums（见
    # _is_annotation_key），标注载体自身的数字不会反过来污染判定。
    exagg_raw = output.get("_explicit_exaggeration") if isinstance(output, dict) else None
    exagg_keys, exagg_invalid = set(), []
    if exagg_raw is not None:
        if not isinstance(exagg_raw, list):
            return "UNKNOWN", "_explicit_exaggeration 不是数组（标注位格式非法，不得默认放行也不得默认判红）"
        for item in exagg_raw:
            if isinstance(item, bool) or not isinstance(item, (int, float, str)):
                exagg_invalid.append(repr(item)); continue
            try:
                exagg_keys.add(_nk(float(str(item).strip())))
            except ValueError:
                exagg_invalid.append(repr(item))
        if exagg_invalid:
            return "UNKNOWN", f"_explicit_exaggeration 含解析不出数值的标注项: {'; '.join(exagg_invalid[:5])}（标注必须精确到数字，不得整句豁免）"

    bad, annotated, generalized = [], [], []
    for v, cls, qkind, qmark, path in out_nums:
        # ---- 保守概括通道（v0.5，Founder 数字表达裁决）----
        # 顺序在精确命中之前：带界标记时按「界」判，碰巧在池里也不免责（判例：「10%以上」红）。
        if qkind == "VAGUE":
            bad.append((v, f"{_fmt(v)}（不可判定的近似表达「{qmark}」@ {path}——裁决3：约/接近/大概类"
                           f"无法由快照原值重算核验，维持禁止）"))
            continue
        if qkind in ("LOWER", "UPPER") and cls in pools:
            pool = pools[cls]
            if not pool:
                bad.append((v, f"{_fmt(v)}（「{qmark}」概括无同类快照来源可核验 @ {path}）"))
                continue
            lo, hi = min(pool), max(pool)
            if qkind == "LOWER" and _nk(v) <= _nk(lo):
                generalized.append(f"{_fmt(v)}「{qmark}」≤ 同类最小值 {_fmt(lo)} @ {path}")
            elif qkind == "UPPER" and _nk(v) >= _nk(hi):
                generalized.append(f"{_fmt(v)}「{qmark}」≥ 同类最大值 {_fmt(hi)} @ {path}")
            else:
                edge = _fmt(lo) if qkind == "LOWER" else _fmt(hi)
                word = "只许往低取（须 ≤ 同类最小值" if qkind == "LOWER" else "只许往高取（须 ≥ 同类最大值"
                bad.append((v, f"{_fmt(v)}（「{qmark}」概括方向不保守：{word} {edge}）@ {path}"))
            continue
        if cls in pools:
            if _nk(v) not in pools[cls]:
                if _nk(v) in exagg_keys:
                    annotated.append(f"{_fmt(v)} @ {path}"); continue
                bad.append((v, f"{_fmt(v)}（{cls} 类无同类快照来源 @ {path}）"))
        else:
            if float(v) < float(threshold): continue
            if _nk(v) not in any_pool:
                if _nk(v) in exagg_keys:
                    annotated.append(f"{_fmt(v)} @ {path}"); continue
                bad.append((v, f"{_fmt(v)}（裸数字无快照来源 @ {path}）"))
    exagg_note = f"；明示夸张标注豁免 {len(annotated)} 处（R2 标注通道，留痕: {'; '.join(annotated[:3])}）" if annotated else ""
    if generalized:
        exagg_note += (f"；保守概括通道放行 {len(generalized)} 处（v0.5 裁决封闭清单，逐条重算留痕: "
                       f"{'; '.join(generalized[:3])}）")
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
    return "OK", f"输出 {len(out_nums)} 处数字全部可溯源到快照同类字段或经明示夸张标注豁免（快照数字 {len(any_pool)} 个）{exagg_note}"
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

# ===================== Intent 侧确定性断言 v0.2（M1-EP02，append-only）=====================
# 为什么要单开四个 Intent 专用检测器，而不复用 BD 那几个：
#   既有 candidate_count / tradeoff_nonempty / trace_types_separated / human_gate_flag 读的都是
#   BusinessDecisionBundle 的字段（candidate_options / comparative_tradeoffs / human_selection_required），
#   IntentExecutionPlan 里根本没有这些键——套上去只会得到一串 UNKNOWN 或**空转的 OK**。
#   尤其 trace_types_separated：它的四类交叉核验整个挂在 `candidate_options` 上，对 Intent 输出
#   那一圈 for 循环是空转，却仍返回「N 条 trace 四类分离且引用类型一致」——一句没验过的话被写成结论
#   （详见三份 INT case.yaml 里逐条写明的取舍理由）。故本段只加 Intent 自己的四条闸，**不改既有函数**。
#
# 四条闸各自的真源（B 为唯一案例真源，A 为字段口径真源）：
#   intent_goal_gate          A.5.2 约束1/2（A:563-564）；B:286 / B:290 / B:294
#   intent_blocking_gate      A.5.2 约束3（A:565）+ A.4.2「BLOCKING 缺失在任何模式都进入 NEEDS_INPUT」(A:394)；B:337
#   intent_assumption_coverage A.5.2 约束4（A:566）+ A.4.2「QUICK 跨过的每项缺失必须产生 ASSUMPTION」(A:393)；B:321-322
#   intent_confidence_cap     B:292「在关键目标未知时给出 HIGH confidence」；B:323
#
# **未覆盖面（如实披露，不得据这四条宣称 Intent 已被机器覆盖）**：
#   ① A.5.2 约束6（同一快照只换目标时计划必须变）是**跨运行**判据，单份输出里无从判定——
#      INT-D03 的核心考点因此仍是人工判分面，三份 case.yaml 与注册表均按 human_required 如实登记；
#   ② 四条闸读的都是**输出自报的字段**。模型若隐瞒缺失项（两个数组都少列一条）、或自称
#      goal_resolution=RESOLVED，这些闸一律看不见——「模型不自报就查不到」是它们共同的射程边界，
#      对应的禁止结果（如「静默确定唯一目标」）保持 human_required，不得因为闸绿了就宣称已覆盖。
#
# v0.2 两处口径变更（M1-EP02 修复批次，逐条写明"为什么"）：
#   ① 缺失集合改**并集**：missing_context 全体 ∪ required_context 中 availability∈{MISSING,CONFLICTING}
#      的条目。v0.1 只读 missing_context，留下一条假绿通道——把一条 availability=MISSING、
#      impact=BLOCKING 的需求只写进 required_context、missing_context 留空，两条闸就都"过"了，
#      而事实上它就是缺的。A.4.2 的 availability 字段本身即权威判据（A:385）。
#      与运行侧 kernel/intent/postcheck.py 的 _collect_missing 同口径（同批同改，两侧不得分叉）。
#   ② ASSUMPTION 配对的 statement 子串兜底**降为 UNKNOWN**：只有 target_paths 精确含 field_path
#      才算已对应。v0.1 把"statement 文本里出现该 field_path 字面量"直接算 OK，而字符串包含会被
#      更长路径的前缀（fp=facts.persona 命中 "facts.persona.tone …"）、被一句复述缺失清单的话
#      顺带满足——那是**假绿方向**的兜底。降为 UNKNOWN 后：确凿未对应仍是 FAIL，只有兜底命中的
#      变成"无从确认"，向上冒泡交人看。运行侧 postcheck P3 同批同改。

_INT_GOAL_RESOLUTIONS = ("RESOLVED", "RESOLVED_WITH_ALTERNATIVE", "AMBIGUOUS", "NEEDS_INPUT")  # A v0.5 第四取值   # A.5.2（A:545）
_INT_IMPACTS = ("BLOCKING", "QUALITY_REDUCING")                     # A.4.2（A:385）
_INT_UNAVAILABLE = ("MISSING", "CONFLICTING")                       # A.4.2 availability 三枚举里的"缺"两态


def _int_plan_guard(output):
    """四条 Intent 闸共用的输入形态守卫：返回 None 表示可以往下读，否则返回 UNKNOWN 的理由。

    为什么空对象也要拦：`{}` 上任何 `.get()` 都返回 None，四条闸会一路走到「字段缺失」分支，
    读起来像"这份输出只是少了几个字段"，实际是**根本没有输出**。两者的处置不同，不能混成一句话。
    """
    if not isinstance(output, dict):
        return f"输出不是 IntentExecutionPlan 对象（实得 {type(output).__name__}），无从读取字段"
    if not output:
        return "输出为空对象（无任何字段），无从核验——空输出不等于合规"
    return None


def _int_is_blank(v):
    """business_goal 是否为空。A.5.2 约束1/2 的原文是「business_goal 必须为空」，
    对应 schema 的 `{"const": null}`；键不在场与空白串一并视为空（宽松方向只放过"确实没填"，
    任何**填了值**的形态都会走 FAIL 分支，不存在因判空而漏红的路径）。"""
    return v is None or (isinstance(v, str) and not v.strip())


def _int_impact_rank(item):
    """缺失项的"严重度"排序键，只用于同一 field_path 在两个数组里写法打架时取严（fail-closed）。
    BLOCKING(2) > impact 不可判(1) > QUALITY_REDUCING(0)：把阻断项在另一处降级成 QR 是最自然的
    绕闸写法，若按"先入为准"就留下旁路；不可判排在 QR 之上，是因为"读不出"至少要冒 UNKNOWN，
    不能被一条 QR 覆盖成 OK。"""
    im = item.get("impact")
    if im == "BLOCKING":
        return 2
    return 0 if im == "QUALITY_REDUCING" else 1


def _int_missing_union(output):
    """缺失集合（**并集口径**，v0.2）。返回 (items, availability 不可判的 field_path 列表, err)；
    err 非 None 时调用方直接冒 UNKNOWN。

    集合 = missing_context 全体 ∪ required_context 中 availability∈{MISSING,CONFLICTING} 的条目，
    按 field_path 去重、冲突取严（见 _int_impact_rank）。为什么不能只读 missing_context：见本段
    段首 v0.2 变更说明①（只读一处 = 把阻断项写进 required_context 即可绕闸）。

    两处的"字段缺失"都返回 UNKNOWN 而不是当成空集：
      · missing_context 缺席 ≠ 没有缺失项——漏写它的输出恰恰是最该被人看一眼的形态；
      · required_context 缺席 → 无从确认 missing_context 是不是全集（并集的另一半读不到了），
        照样是"无从核验"而非"没有别的缺失项"。（两者都是 A.5.2 顶层 required 字段，缺席时
        schema_valid 会另判红；本闸不替它判，只如实说自己核验不了。）
    第二个返回值（availability 不可判）：required_context 里 availability 既不是 AVAILABLE、
      也不在 {MISSING,CONFLICTING} 里的条目——不能算进缺失集合（值读不出，不确定它真缺），
      也不能当没看见（否则把 availability 写歪一个字母就是新的绕闸通道），故单独带出，
      由调用方在"继续下游"分支上冒 UNKNOWN。
    """
    mc = output.get("missing_context")
    if mc is None:
        return None, None, "missing_context 字段缺失，无从核验（字段不在场 ≠ 没有缺失项）"
    if not isinstance(mc, list):
        return None, None, f"missing_context 不是数组（实得 {type(mc).__name__}），无从逐项核验"
    bad = [i for i, x in enumerate(mc) if not isinstance(x, dict)]
    if bad:
        return None, None, f"missing_context 第 {bad} 项不是对象，读不出 impact / field_path"
    rc = output.get("required_context")
    if rc is None:
        return None, None, ("required_context 字段缺失，缺失集合（missing_context ∪ required_context "
                            "缺态）无从核验——阻断项可以只写在 required_context 里，读不到它就"
                            "无从确认 missing_context 已是全集")
    if not isinstance(rc, list):
        return None, None, f"required_context 不是数组（实得 {type(rc).__name__}），无从逐项核验"
    badr = [i for i, x in enumerate(rc) if not isinstance(x, dict)]
    if badr:
        return None, None, f"required_context 第 {badr} 项不是对象，读不出 availability / impact / field_path"

    unreadable_avail, order, index = [], [], {}
    for origin, arr in (("missing_context", mc), ("required_context", rc)):
        for pos, x in enumerate(arr):
            if origin == "required_context":
                av = x.get("availability")
                if av == "AVAILABLE":
                    continue                     # 在场的需求不是缺失项，跳过（不制造假红）
                if av not in _INT_UNAVAILABLE:
                    unreadable_avail.append(x.get("field_path"))
                    continue
            fp = x.get("field_path")
            # field_path 读不出的条目也要进集合（由调用方冒 UNKNOWN），用位置键占位避免互相吞并
            key = fp if isinstance(fp, str) and fp.strip() else "__unbindable__%s#%d" % (origin, pos)
            if key not in index:
                index[key] = x
                order.append(key)
            elif _int_impact_rank(x) > _int_impact_rank(index[key]):
                index[key] = x
    return [index[k] for k in order], unreadable_avail, None


def intent_goal_gate(output, ctx, **kw):
    """A.5.2 约束1/2 的确定性投影：goal_resolution 非 RESOLVED 时，business_goal 必须为空
    且 next_action 必须为 REQUEST_INPUT（A:563-564；B:286 / B:290 / B:294）。

    三态口径：
      OK      goal_resolution=RESOLVED（本闸不适用；RESOLVED 本身是否站得住脚是 L3 人工判分面）
              或 非 RESOLVED 且两项都合规；
      FAIL    非 RESOLVED 却填了唯一 business_goal / 或 next_action 不是 REQUEST_INPUT；
      UNKNOWN goal_resolution 或 next_action 读不出来（禁 default:false）。
    枚举外取值（如 "resolved_ish"）**照样按"非 RESOLVED"判**，不放行——取值合法性由 schema_valid
    另判，本闸不因为一个陌生枚举值就把闸打开（那正是绕过通道）。
    """
    err = _int_plan_guard(output)
    if err:
        return "UNKNOWN", err
    gr = output.get("goal_resolution")
    if gr is None:
        return "UNKNOWN", "goal_resolution 字段缺失，无从判定本闸是否适用（缺字段 ≠ 已解析）"
    if not isinstance(gr, str):
        return "UNKNOWN", f"goal_resolution 不是字符串（实得 {type(gr).__name__}），无从判定"
    if gr == "RESOLVED":
        return "OK", "goal_resolution=RESOLVED，A.5.2 约束1/2 不适用（RESOLVED 是否站得住脚属人工判分面）"
    if gr == "RESOLVED_WITH_ALTERNATIVE":
        # A v0.5 约束8（Founder 2026-08-18 第⑥条）：该状态**按定义**带一个非空主目标
        # （按用户原话解析出来的），所以约束1/2 的「非 RESOLVED 必须清空 business_goal」不适用于它——
        # 它归约束8 管，由 intent_situational_alternative 与 kernel postcheck P10 判。
        # 这里只守住与约束8 共有的那一条硬要求：必须停在 REQUEST_INPUT（不得替人继续）。
        na = output.get("next_action")
        if na is None:
            return "UNKNOWN", "goal_resolution=RESOLVED_WITH_ALTERNATIVE 但 next_action 字段缺失，无从核验"
        if na != "REQUEST_INPUT":
            return "FAIL", (f"goal_resolution=RESOLVED_WITH_ALTERNATIVE 却 next_action={na!r}"
                            "——并呈备选却未把方向选择权交回人工（A.5.2 约束8）")
        return "OK", ("goal_resolution=RESOLVED_WITH_ALTERNATIVE：约束1/2 不适用（主目标按定义非空，归约束8），"
                      "next_action=REQUEST_INPUT 已停在用户选择点；并呈是否合格由 intent_situational_alternative 判")
    off = "" if gr in _INT_GOAL_RESOLUTIONS else f"（另注：{gr!r} 不在 A.5.2 四枚举内，枚举合法性由 schema_valid 判）"
    bg = output.get("business_goal")
    if not _int_is_blank(bg):
        return "FAIL", f"goal_resolution={gr} 却给出唯一 business_goal={bg!r}——目标未解析不得填入唯一目标{off}"
    na = output.get("next_action")
    if na is None:
        return "UNKNOWN", f"goal_resolution={gr} 且 business_goal 为空，但 next_action 字段缺失，无从核验是否 REQUEST_INPUT{off}"
    if na != "REQUEST_INPUT":
        return "FAIL", f"goal_resolution={gr} 却 next_action={na!r}（非 REQUEST_INPUT）——未把决定权交回人工{off}"
    return "OK", f"goal_resolution={gr}：business_goal 为空且 next_action=REQUEST_INPUT{off}"


def intent_blocking_gate(output, ctx, **kw):
    """A.5.2 约束3 / A.4.2「BLOCKING 缺失在任何模式都进入 NEEDS_INPUT」的确定性投影
    （A:565 / A:394；B:337「快速模式绕过阻断项」）：缺失集合含 BLOCKING 项时
    next_action 不得为 CONTINUE_TO_DECISION。

    缺失集合 = missing_context ∪ required_context 中 availability∈{MISSING,CONFLICTING} 的项
    （v0.2 并集口径，见 _int_missing_union 与本段段首变更说明①；与 kernel postcheck 同口径）。

    三态口径：
      OK      next_action 不是 CONTINUE_TO_DECISION（本闸不适用），或 CONTINUE 且无 BLOCKING 缺失；
      FAIL    CONTINUE 且缺失集合里至少一项 impact=BLOCKING；
      UNKNOWN missing_context / required_context / next_action 读不出；或 CONTINUE 且有项目的
              impact 取值不可判、或 required_context 有项目的 availability 取值不可判
              （读不出就无从确认"没有阻断项"，不得默认放行）。
    FAIL 优先于 UNKNOWN：已确证的阻断项是比"某几项读不出"更强的证据，不该被冒泡掩盖
    （同 numeric_grounding 的既定顺序）。
    射程边界：只看输出**自报**的两个数组。模型两处都漏列阻断项时本闸看不见，
    该形态属人工判分面（见本段段首「未覆盖面」②）。
    """
    err = _int_plan_guard(output)
    if err:
        return "UNKNOWN", err
    items, avail_bad, err = _int_missing_union(output)
    if err:
        return "UNKNOWN", err
    na = output.get("next_action")
    if na is None:
        return "UNKNOWN", "next_action 字段缺失，无从判定是否在带阻断项的情况下继续下游"
    blocking = [x.get("field_path") for x in items if x.get("impact") == "BLOCKING"]
    unreadable = [x.get("field_path") for x in items if x.get("impact") not in _INT_IMPACTS]
    if na != "CONTINUE_TO_DECISION":
        return "OK", (f"next_action={na!r}，未继续下游，本闸（A.5.2 约束3）不适用"
                      f"（输出自报阻断缺失 {len(blocking)} 项）")
    if blocking:
        return "FAIL", f"存在 BLOCKING 缺失 {blocking} 却 next_action=CONTINUE_TO_DECISION——阻断项被跨过"
    if unreadable:
        return "UNKNOWN", (f"next_action=CONTINUE_TO_DECISION，但 {len(unreadable)} 项缺失的 impact 取值不可判"
                           f"（{unreadable}，合法值 {list(_INT_IMPACTS)}）——无从确认其中没有阻断项")
    if avail_bad:
        return "UNKNOWN", (f"next_action=CONTINUE_TO_DECISION，但 required_context 有 {len(avail_bad)} 项的 "
                           f"availability 取值不可判（{avail_bad}，合法值 AVAILABLE / "
                           f"{list(_INT_UNAVAILABLE)}）——无从确认它们是不是也是阻断缺失")
    return "OK", (f"next_action=CONTINUE_TO_DECISION，自报的 {len(items)} 项缺失"
                  f"（missing_context ∪ required_context 缺态）均非 BLOCKING")


def intent_assumption_coverage(output, ctx, **kw):
    """A.5.2 约束4 / A.4.2「QUICK 跨过的每项缺失必须产生 ASSUMPTION」的确定性投影
    （A:566 / A:393；B:321-322）：next_action=CONTINUE_TO_DECISION 且有缺失项时，
    每项必须是 QUALITY_REDUCING，且每项都能在 ASSUMPTION 类 trace 里找到对应条目。

    缺失集合 = missing_context ∪ required_context 中 availability∈{MISSING,CONFLICTING} 的项
    （v0.2 并集口径，同 intent_blocking_gate；只读 missing_context 会漏掉"只写在 required_context
    里的缺失项"，那些项同样被跨过，同样必须留假设）。

    **绑定口径（考卷侧确定性约定，A/B 均未规定用哪个字段表达"对应"；v0.2 收紧）**：
      ① 该 ASSUMPTION 条目的 target_paths 数组含该项 field_path（精确相等）→ 判为**已对应**；
      ② 都没有 target_paths 命中，但某条 ASSUMPTION 的 statement 文本里出现该 field_path 字面量
         → 判 **UNKNOWN**（兜底命中，不再算 OK）。理由：字符串包含会被更长路径的前缀
         （fp=facts.persona 命中 "facts.persona.tone …"）、被一句复述缺失清单的话顺带满足——
         用它发绿灯就是假绿；但它也确实不能证明"没有对应"，故冒泡交人看，不判红。
      ③ 两条都不命中 → FAIL（A:566 要求"产生**对应** ASSUMPTION"，任何确定性方式都看不出对应
         关系时等同于没有对应）。
      生产侧消除 UNKNOWN 的办法只有一个：把 field_path 写进 target_paths（A.9.2 该字段就是干这个的）。
    ASSUMPTION 条目池 = trace_bundle.entries ∪ 顶层 assumptions 数组中 trace_type=ASSUMPTION 的条目
    （A.5.2 两处都可承载 TraceEntry，取并集，不预设生产侧写在哪一处）。

    **与运行侧的已知口径分叉（如实登记，不假装两侧等价）**：kernel/intent/postcheck.py 的 P3 属同批
      同改项，本文件写作时实读其 _assumption_covers 已是同样的①②③三档；两侧由不同施工代理并行落盘，
      以各自最终版本为准，发现分叉即以本批规格为准同批修正。P3 的触发前置是 `execution_mode==QUICK 且 CONTINUE`
      （A:566 原文只约束 QUICK 继续）；本闸拿不到 execution_mode（tools/run_case.py 传入的 ctx 只有
      repo_root / output_path / output_schema / snapshot），故**不分模式**，凡 CONTINUE 即适用。
      方向是考卷侧更严，不是更松；ENHANCED 模式下 CONTINUE 却不留假设时本闸照判，属考卷侧自决。

    三态口径：
      OK      非 CONTINUE 分支（不适用）/ CONTINUE 但缺失集合为空 / 逐项 QUALITY_REDUCING 且逐项有
              target_paths 精确对应的 ASSUMPTION；
      FAIL    CONTINUE 且有 BLOCKING 缺失 / ASSUMPTION 池为空 / 有缺失项两档都不命中；
      UNKNOWN 字段读不出、只有 statement 兜底命中、impact 取值不可判、field_path 不可读、
              required_context 的 availability 取值不可判、trace_bundle.entries 与 assumptions 均缺失。
    """
    err = _int_plan_guard(output)
    if err:
        return "UNKNOWN", err
    items, avail_bad, err = _int_missing_union(output)
    if err:
        return "UNKNOWN", err
    na = output.get("next_action")
    if na is None:
        return "UNKNOWN", "next_action 字段缺失，无从判定本闸（A.5.2 约束4）是否适用"
    if na != "CONTINUE_TO_DECISION":
        return "OK", f"next_action={na!r}，未继续下游，本闸（A.5.2 约束4）不适用"
    if not items:
        if avail_bad:
            return "UNKNOWN", (f"缺失集合读出来是空的，但 required_context 有 {len(avail_bad)} 项的 "
                               f"availability 取值不可判（{avail_bad}）——无从确认真的没有被跨过的缺失项")
        return "OK", ("next_action=CONTINUE_TO_DECISION 且缺失集合"
                      "（missing_context ∪ required_context 缺态）为空——无被跨过的缺失项")
    blocking = [x.get("field_path") for x in items if x.get("impact") == "BLOCKING"]
    if blocking:
        return "FAIL", f"CONTINUE 却跨过 BLOCKING 缺失 {blocking}——A.5.2 约束4 只允许跨过 QUALITY_REDUCING"
    unreadable = [x.get("field_path") for x in items if x.get("impact") not in _INT_IMPACTS]
    tb = output.get("trace_bundle")
    entries = tb.get("entries") if isinstance(tb, dict) else None
    asums = output.get("assumptions")
    # 结构漂移必须冒 UNKNOWN 而不是"当它不存在"：entries 若是 dict / 字符串，下面的 list() 会安静地
    # 拆成键名或单字并被 isinstance 过滤掉，池就凭空少了一批条目 → 判出一个**看似确凿**的 FAIL。
    # 假红同样是失真，条件不明时只能向上冒泡。
    for name, v in (("trace_bundle.entries", entries), ("assumptions", asums)):
        if v is not None and not isinstance(v, list):
            return "UNKNOWN", f"{name} 不是数组（实得 {type(v).__name__}），ASSUMPTION 对应关系无从核验"
    if entries is None and not isinstance(asums, list):
        return "UNKNOWN", "trace_bundle.entries 与 assumptions 均读不出，ASSUMPTION 对应关系无从核验"
    pool = [e for e in list(entries or []) + list(asums or [])
            if isinstance(e, dict) and e.get("trace_type") == "ASSUMPTION"]
    if not pool:
        return "FAIL", (f"CONTINUE 且跨过 {len(items)} 项缺失，但 ASSUMPTION 类 trace 条目为 0 条"
                        f"——跨过缺失却不留假设，正是「不提示缺失却输出确定结论」的形态")
    uncovered, weak, unbindable = [], [], []
    for x in items:
        fp = x.get("field_path")
        if not isinstance(fp, str) or not fp.strip():
            unbindable.append(fp)
            continue
        if any(fp in [p for p in (e.get("target_paths") or []) if isinstance(p, str)] for e in pool):
            continue                                  # ① target_paths 精确命中 = 已对应
        # ② statement 兜底：先做类型收窄再做 `in`——非字符串的 statement（结构漂移）若直接参与 `in`，
        #    对 dict 会静默去匹配**键名**、对数字直接抛 TypeError；前者是假绿通道，后者会炸掉整轮判分。
        if any(fp in (e.get("statement") if isinstance(e.get("statement"), str) else "") for e in pool):
            weak.append(fp)
        else:
            uncovered.append(fp)
    if uncovered:
        return "FAIL", (f"以下被跨过的缺失项找不到对应 ASSUMPTION 条目（绑定口径：target_paths 精确含该 "
                        f"field_path；statement 兜底命中只算 UNKNOWN，见本函数 docstring）: {uncovered}")
    if weak:
        return "UNKNOWN", (f"以下被跨过的缺失项只有 statement 文本里出现过 field_path 字面量、没有任何 "
                           f"ASSUMPTION 的 target_paths 精确命中（{weak}）——字符串包含会被更长路径的前缀或"
                           f"一句复述缺失清单的话顺带满足，据此发绿灯即假绿；对应关系无从确认，"
                           f"生产侧把 field_path 写进 target_paths 即可消除本项")
    if unbindable:
        return "UNKNOWN", (f"{len(unbindable)} 项缺失的 field_path 不可读（{unbindable}），"
                           f"无从与 ASSUMPTION 条目建立对应——其余项已逐项命中")
    if unreadable:
        return "UNKNOWN", (f"{len(unreadable)} 项缺失的 impact 取值不可判（{unreadable}），"
                           f"无从确认其为 QUALITY_REDUCING——ASSUMPTION 对应关系本身已逐项命中")
    if avail_bad:
        return "UNKNOWN", (f"required_context 有 {len(avail_bad)} 项的 availability 取值不可判"
                           f"（{avail_bad}）——无从确认缺失集合已完整；已进集合的项均已逐项命中")
    return "OK", (f"CONTINUE 跨过的 {len(items)} 项缺失（missing_context ∪ required_context 缺态）"
                  f"均为 QUALITY_REDUCING，且逐项有 target_paths 精确对应的 ASSUMPTION（池 {len(pool)} 条）")


def intent_confidence_cap(output, ctx, **kw):
    """B:292「在关键目标未知时给出 HIGH confidence」的确定性投影（另见 B:323 快速模式「降低 confidence」）：
    goal_resolution 非 RESOLVED 时 confidence.level 不得为 HIGH。

    「关键目标未知」的机器判据取 goal_resolution != RESOLVED——这是输出里唯一表达"目标是否已定"的
    字段（A:545）。模型自称 RESOLVED 却其实没定，本闸看不见，那属「静默确定唯一目标」的人工判分面。
    三态：OK（RESOLVED 不适用 / 非 RESOLVED 且非 HIGH）；FAIL（非 RESOLVED 且 HIGH）；
    UNKNOWN（goal_resolution 或 confidence.level 读不出——**不得**因为读不到就当成没超标）。
    """
    err = _int_plan_guard(output)
    if err:
        return "UNKNOWN", err
    gr = output.get("goal_resolution")
    if gr is None:
        return "UNKNOWN", "goal_resolution 字段缺失，无从判定本闸是否适用（缺字段 ≠ 目标已定）"
    if not isinstance(gr, str):
        return "UNKNOWN", f"goal_resolution 不是字符串（实得 {type(gr).__name__}），无从判定"
    if gr == "RESOLVED":
        return "OK", "goal_resolution=RESOLVED，置信度上限约束不适用（B:292 只约束关键目标未知时）"
    conf = output.get("confidence")
    if not isinstance(conf, dict):
        return "UNKNOWN", f"confidence 不是对象（实得 {type(conf).__name__}），置信度无从核验"
    lvl = conf.get("level")
    if lvl is None:
        return "UNKNOWN", "confidence.level 字段缺失，置信度无从核验（读不到 ≠ 未超标）"
    if lvl == "HIGH":
        return "FAIL", f"goal_resolution={gr}（关键目标未定）却给出 confidence.level=HIGH"
    return "OK", f"goal_resolution={gr} 且 confidence.level={lvl!r}（非 HIGH）"
# ===================== Intent 侧确定性断言 v0.2 结束 =====================


# ============ Intent 侧判分批新增（Founder 2026-08-18 批准五条统一产品标准；改检测器=改考卷，本批为裁决授权）============

def intent_terminal_state(output, ctx, expect_goal_resolution=None, expect_business_goal=None,
                          expect_next_action=None, **kw):
    """案例级终态断言：考卷用 args 声明该案例的预期终态（B v0.6 允许答案族的机器可判面），
    任何一项不符即 FAIL——「把可直接执行的任务升级成用户决策题」（INT_TASK_ESCALATED）的机器形态
    正是终态落到 REQUEST_INPUT/AMBIGUOUS 而考卷要求 CONTINUE。expect_business_goal 传字面量
    "null" 表示「必须为空」。读不到字段 → UNKNOWN（禁 default 放行）。"""
    if not isinstance(output, dict):
        return "UNKNOWN", f"输出不是结构化对象（实得 {type(output).__name__}），终态无从判定"
    expects = (("goal_resolution", expect_goal_resolution),
               ("business_goal", expect_business_goal),
               ("next_action", expect_next_action))
    if all(w is None for _f, w in expects):
        return "UNKNOWN", "考卷未声明任何预期终态（args 全空），本闸无判定对象——不得默认放行"
    bad = []
    for field, want in expects:
        if want is None:
            continue
        if want == "null":
            if output.get(field) is not None:
                bad.append(f"{field}={output.get(field)!r}（期望 null）")
            continue
        if field not in output:
            return "UNKNOWN", f"{field} 字段缺失，终态无从判定（缺字段 ≠ 符合预期）"
        if output.get(field) != want:
            bad.append(f"{field}={output.get(field)!r}（期望 {want!r}）")
    if bad:
        return "FAIL", "终态不符考卷声明：" + "；".join(bad)
    return "OK", "终态符合考卷声明：" + "；".join(f"{f}={w}" for f, w in expects if w is not None)


def intent_candidate_completeness(output, ctx, **kw):
    """统一产品标准④的机器可判面：AMBIGUOUS 时候选必须是方案骨架——候选 ≥2 且每个候选的
    focus / tradeoffs / expected_outcome 三要素非空；光秃标签选择题判 FAIL（INT_TASK_ESCALATED）。
    非 AMBIGUOUS 时本闸不适用（OK 并注明「不适用 ≠ 已验证」）；字段读不出 → UNKNOWN。"""
    if not isinstance(output, dict):
        return "UNKNOWN", f"输出不是结构化对象（实得 {type(output).__name__}）"
    gr = output.get("goal_resolution")
    if gr is None:
        return "UNKNOWN", "goal_resolution 字段缺失，无从判定本闸适用性"
    if gr != "AMBIGUOUS":
        return "OK", f"goal_resolution={gr}，本闸只在 AMBIGUOUS 下适用（不适用 ≠ 已验证）"
    cands = output.get("goal_candidates")
    if not isinstance(cands, list):
        return "UNKNOWN", "goal_candidates 缺失或非数组（AMBIGUOUS 下这本身已属结构违约，由 schema_valid 判）"
    if len(cands) < 2:
        return "FAIL", f"AMBIGUOUS 候选仅 {len(cands)} 个（A.5.2 约束1 要求至少两个）"
    bad = []
    for i, c in enumerate(cands):
        c = c if isinstance(c, dict) else {}
        lack = [k for k in ("focus", "tradeoffs", "expected_outcome") if not str(c.get(k) or "").strip()]
        if lack:
            bad.append(f"候选{i}({c.get('goal')}) 缺 {lack}")
    if bad:
        return "FAIL", "候选缺三要素（未经整理的选择题退给用户）：" + "；".join(bad)
    return "OK", f"{len(cands)} 个候选三要素齐全（方案骨架成立）"


def _snapshot_fact_value(snapshot, dotted_path):
    """按 `product.lifecycle_stage` 这类点分路径在快照事实区取值。

    只走 facts 区（企业事实），不接受顶层任意键——第⑥条管的是「系统据**企业事实**已知的情境」，
    从 _fixture_note 之类元数据里读出来的"情境"不是企业事实。
    取到 {status, value, ...} 形状时返回 value；取不到返回 (False, None)，取到返回 (True, 值)。
    """
    node = (snapshot or {}).get("facts")
    for seg in dotted_path.split("."):
        if not isinstance(node, dict) or seg not in node:
            return False, None
        node = node[seg]
    if isinstance(node, dict) and "value" in node:
        return True, node["value"]
    return True, node


def intent_situational_alternative(output, ctx, situation_field=None, situation_value=None,
                                   alternative_goal=None, primary_goal=None, **kw):
    """统一产品标准⑥的机器可判面（Founder 2026-08-18 复判批；判据 A.5.2 约束8 + OD-03 §五 登记表）。

    考的是一件事：系统据企业事实已知某个登记在册的重大经营情境、而用户原话未提及时，**有没有把
    两套方案并呈交用户选**——既不许擅自转向该情境目标，也不许只在内部留痕当作不知道。
    失败现场（本闸的来由）：RUN-0013/0014，模型内部写下「该产品处于库存消化期，但任务原话未提及
    清库存或促销意图，因此不能据此推断目标为 INVENTORY_ACTIVATION」，用户侧零呈现。

    考卷用 args 显式声明本案例的情境（**不在检测器里硬编案例**，登记表真源在 OD-03 §五）：
      situation_field   企业事实的点分路径，如 product.lifecycle_stage
      situation_value   触发值，如 库存消化期
      alternative_goal  该情境对应的备选目标，如 INVENTORY_ACTIVATION
      primary_goal      按用户原话解析出的主目标，如 DAILY_CONTENT_OPERATION

    三态：
      · args 未声明齐 / 快照读不到 / 快照里该情境不在场 → UNKNOWN（禁默认放行：考卷声明了情境却
        查无实据，说明考卷与夹具漂移，这本身要人看，不能算通过）；
      · goal_resolution=RESOLVED：business_goal=primary_goal → FAIL「装作不知道」；
        =alternative_goal → FAIL「擅自转向」；其它目标 → UNKNOWN（窄口径射程外）；
      · goal_resolution=RESOLVED_WITH_ALTERNATIVE：逐条核 business_goal 是主目标、候选含主与备两
        方向、两者三要素非空、next_action=REQUEST_INPUT——缺一 FAIL；
      · AMBIGUOUS / NEEDS_INPUT → UNKNOWN（分叉 C 窄口径：系统本就在请人裁决，不是「闷头开做」，
        并呈没发生但也没造成第⑥条要防的后果，交人工判分，不判绿也不判红）。

    ⚠ 射程边界（不得据本闸绿灯宣称第⑥条已被机器覆盖）：只判**该并呈有没有并呈**，判不了两套方案
      写得好不好、侧重取舍讲得对不对——那是 L3 人工判分面（B.4.1/INT-D02 第 4 问）。
    """
    if not isinstance(output, dict):
        return "UNKNOWN", f"输出不是结构化对象（实得 {type(output).__name__}），并呈义务无从判定"
    declared = (situation_field, situation_value, alternative_goal, primary_goal)
    if any(x is None for x in declared):
        return "UNKNOWN", ("考卷未声明完整情境四元组（situation_field / situation_value / "
                           "alternative_goal / primary_goal），本闸无判定对象——不得默认放行")
    snapshot = ctx.get("snapshot") if isinstance(ctx, dict) else None
    if not isinstance(snapshot, dict):
        return "UNKNOWN", "快照不可读，情境是否在场无从判定（禁 default 放行）"
    found, value = _snapshot_fact_value(snapshot, situation_field)
    if not found:
        return "UNKNOWN", f"快照事实区无 {situation_field} 路径，考卷声明的情境查无实据（考卷与夹具漂移，须人工看）"
    if value != situation_value:
        return "UNKNOWN", (f"快照 {situation_field}={value!r}，与考卷声明的触发值 {situation_value!r} 不符，"
                           "本案例本轮不构成第⑥条场合")

    gr = output.get("goal_resolution")
    if gr is None:
        return "UNKNOWN", "goal_resolution 字段缺失，无从判定并呈义务"
    bg = output.get("business_goal")
    sit = f"快照事实 {situation_field}={situation_value!r} 在场且用户原话未提及"

    if gr == "RESOLVED":
        if bg == primary_goal:
            return "FAIL", (f"{sit}，系统却按常规方案径直继续（goal_resolution=RESOLVED，"
                            f"business_goal={bg}）——情境被吞掉、用户侧零呈现（第⑥条「装作不知道」）")
        if bg == alternative_goal:
            return "FAIL", (f"{sit}，系统未经用户选择就把目标定成 {bg}——擅自转向"
                            "（第⑥条：不得擅自转向）")
        return "UNKNOWN", f"{sit}，但 business_goal={bg!r} 既非主目标也非情境备选目标，本闸射程外"

    if gr == "RESOLVED_WITH_ALTERNATIVE":
        bad = []
        if bg != primary_goal:
            bad.append(f"business_goal={bg!r} 不是按用户原话的主目标 {primary_goal!r}（主备颠倒或降级）")
        cands = output.get("goal_candidates")
        if not isinstance(cands, list):
            return "UNKNOWN", "goal_candidates 缺失或非数组（结构违约由 schema_valid 判）"
        by_goal = {c.get("goal"): c for c in cands if isinstance(c, dict)}
        for want, role in ((primary_goal, "主方案"), (alternative_goal, "情境备选")):
            if want not in by_goal:
                bad.append(f"候选里没有{role} {want}")
                continue
            lack = [k for k in ("focus", "tradeoffs", "expected_outcome")
                    if not str(by_goal[want].get(k) or "").strip()]
            if lack:
                bad.append(f"{role} {want} 缺三要素 {lack}")
        if output.get("next_action") != "REQUEST_INPUT":
            bad.append(f"next_action={output.get('next_action')!r}，并呈却未停在用户选择点"
                       "（应为 REQUEST_INPUT；备选不得代替人工选择）")
        if bad:
            return "FAIL", f"{sit}，并呈形态不合格：" + "；".join(bad)
        return "OK", (f"{sit}，已并呈两套方案：主方案 {primary_goal} + 情境备选 {alternative_goal}，"
                      "三要素齐全且停在用户选择点（方案写得好不好属人工判分面）")

    return "UNKNOWN", (f"goal_resolution={gr}，系统本就在请人裁决而非「闷头开做」，"
                       "第⑥条窄口径下本闸不适用（不适用 ≠ 已验证）")
