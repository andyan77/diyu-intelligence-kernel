#!/usr/bin/env python3
"""检测器负向/正向测试（P0-3 配套）。纯 assert 脚本，不依赖 pytest；exit 0 = 全过，exit 1 = 有失败。

用法: python3 tools/test_detectors.py
纪律（C.4 铁律1 / 宪法「exit 0 ≠ 通过」）：本脚本只证明**检测器本身**在给定构造输入上返回期望的
(verdict, detail)；它不产生任何案例级 PASS，也不替代 tools/run_case.py 的运行证据。
覆盖范围（v0.2 首版）：三类确定性漏检（阈值下 / 跨字段借位 / 中文数字）+ 泛量词豁免
+ BD-D01 三夹具回归 + UNKNOWN 冒泡（快照缺失 / 守卫字段缺失，禁 default:false）。
新增（v0.3 修复批次，⑩~⑯ 段）：每一条都对应一处**已复现**的旁路，不是设想——
  ⑩ 单位窗口插字（120 余/多/来件、全角括号、单位前置、省略单位）不得退回 any_pool 兜底；
  ⑪ 量级词与中文数字取值（120 万 / 一亿 / 一千二 二义 → UNKNOWN / 成语不作数量）；
  ⑫ 路径分类中文子串碰撞（内容单元→price、款式编码→size）双向修正；
  ⑬ 符号位与全角归一（-800 / 3，980 / 全角数字）；
  ⑭ 输出侧类型守卫（None / {} / 非结构化串一律 UNKNOWN，不发绿灯）；
  ⑮ 中文量词误报（这一件 / 两件套 / 第一天），并断言序数豁免未成为绕过通道；
  ⑯ forbidden_expression 空词表 / 结构漂移 → UNKNOWN。
**未覆盖面（如实披露，不得据本套件宣称检测器无漏判）**：溯源粒度是**类级不是实例级**——
跨实体同类同值借位（快照里 A 款价格 3980，输出写成「B 款也卖 3980 元」）本检测器看不见，
属 L3 人工判分面；本套件不含该面用例，因为确定性检测器在当前快照结构下无法判定它。
新增（M1-EP02 考卷侧，⑰~㉑ 段）：四个 Intent 确定性断言的正/反/负向用例——
  ⑰ intent_goal_gate（A.5.2 约束1/2）：非 RESOLVED 却填目标 / 却不 REQUEST_INPUT；枚举外取值不得放行；
  ⑱ intent_blocking_gate（A.5.2 约束3）：自报阻断项却 CONTINUE；impact 不可判时 UNKNOWN 而非放行；
  ⑲ intent_assumption_coverage（A.5.2 约束4）：跨过的缺失逐项须有对应 ASSUMPTION；FACT 类 trace 不顶替；
  ⑳ intent_confidence_cap（B:292）：目标未定时 HIGH 置信度；读不出置信度时 UNKNOWN；
  ㉑ 三份 INT case.yaml 的考卷绑定冒烟：每条 must_hold 的 check 必须能在检测器库里取到且可调用。
检测器库 v0.1→v0.2 配套（M1-EP02 修复批次，⑱-i~o / ⑲-n~s 段 + 既有期望的逐条修订）：
  · 并集口径：缺失集合 = missing_context ∪ required_context 中 availability∈{MISSING,CONFLICTING}。
    新用例覆盖「阻断项只写 required_context 绕闸」（v0.1 实测判 OK = 假绿主通道）、CONFLICTING 视同缺失、
    AVAILABLE 项不得算缺失（假红方向）、availability 写歪时 UNKNOWN、两处 impact 打架取严、去重计数；
  · 兜底降级：ASSUMPTION 配对只认 target_paths 精确命中，statement 子串命中改判 UNKNOWN。
    新用例给出两种真实的兜底假绿形态（更长路径前缀 / 一句复述缺失清单的话），并断言
    「补 target_paths 即可恢复 OK」与「确凿未对应仍 FAIL 优先」——降级不得把真红稀释成 UNKNOWN。
  · 受口径变化影响的既有期望共 3 条（⑱-g / ⑲-d / ⑲-h），已在各自用例上方逐条注明改动原因。
**这四条同样有射程边界（不得据其绿灯宣称 Intent 已被机器覆盖）**：它们读的都是输出**自报**的字段，
模型漏列缺失项或自称 goal_resolution=RESOLVED 时一律看不见；A.5.2 约束6（跨运行目标迁移）更是
单份输出内无从判定——对应的禁止结果在 prohibited_registry.yaml 里保持 human_required。
"""
import importlib.util, json, os, sys, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("checks", os.path.join(ROOT, "acceptance/detectors/checks.py"))
checks = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(checks)

FAILURES = []
PASSED = []


def check(name, got, want_verdict, want_detail_contains=None, want_detail_excludes=None):
    """want_detail_contains 可传字符串或字符串元组（元组 = 全部必须命中）。

    为什么要能传元组（P0-3 修复批次）：单个 '1200' / '2026' 这类子串可以被 detail 里的字段路径、
    别的数字、甚至夹具注释文字**顺带**满足，断言就退化成「detail 非空」。关键用例改为核对
    (verdict, 触发路径) 二元组——例如同时要求 '1200' 与 '@ business_problem'，
    让「哪个字段触发的红」也进断言，未来退化才拦得住。
    """
    verdict, detail = got
    problems = []
    if verdict != want_verdict:
        problems.append(f"verdict 期望 {want_verdict} 实得 {verdict}")
    wants = (want_detail_contains,) if isinstance(want_detail_contains, str) else (want_detail_contains or ())
    for w in wants:
        if w not in detail:
            problems.append(f"detail 应含 {w!r}")
    if want_detail_excludes and want_detail_excludes in detail:
        problems.append(f"detail 不应含 {want_detail_excludes!r}")
    if problems:
        FAILURES.append(f"[FAIL] {name}: {'; '.join(problems)} | detail={detail!r}")
    else:
        PASSED.append(f"[ok]   {name}: {verdict} | {detail[:110]}")


def ng(output, snapshot, **kw):
    return checks.numeric_grounding(output, {"snapshot": snapshot, "repo_root": ROOT}, **kw)


# ---- 通用夹具快照：库存 800 件 / 吊牌价 3980 元 / 尺码胸围 120 / 周期 6 周 ----
SNAP = {
    "snapshot_id": "SNAP-TEST-0001",
    "facts": {
        "inventory": {"value": 800, "unit": "件", "source": "夹具虚构"},
        "product": {
            "product_id": "P13",
            "price": {"value": 3980, "currency": "CNY", "as_of": "2026-08-17", "source": "截图 IMG_0684"},
            "measurements": {"胸围": 120, "肩宽": 44},
            "composition": "90.2%绵羊毛 9.8%山羊绒",
        },
        "campaign": {"周期": {"value": 6, "unit": "周"}},
    },
}

# ============================ ① 阈值下：49 元无来源 → FAIL ============================
# v0.1 因 threshold=50 直接豁免；v0.2 价格类不设阈值豁免。
check("①-a 49元无来源→FAIL", ng({"copy": "限时价 49 元"}, SNAP), "FAIL", "49")
check("①-b 3980元有来源→OK", ng({"copy": "吊牌价 3980 元"}, SNAP), "OK")
check("①-c 38%无来源→FAIL", ng({"copy": "给到 38% 折扣"}, SNAP), "FAIL", "38")
check("①-d 千分位真值不误报", ng({"copy": "售价 3,980 元"}, SNAP), "OK")

# ====================== ② 跨字段借位：快照 size 有 120，输出「库存 120 件」→ FAIL ======================
check("②-a 尺码120借位给库存→FAIL", ng({"copy": "库存 120 件"}, SNAP), "FAIL", "120")
check("②-b 库存800件→OK", ng({"copy": "库存 800 件"}, SNAP), "OK")
check("②-c 价格3980借位给库存→FAIL", ng({"copy": "库存 3980 件"}, SNAP), "FAIL", "3980")
check("②-d 日期2026借位给价格→FAIL", ng({"copy": "售价 2026 元"}, SNAP), "FAIL", "2026")
check("②-e 周期6周有来源→OK", ng({"copy": "投放 6 周"}, SNAP), "OK")

# ====================== ③ 中文数字：「一千二百件」快照库存无 1200 → FAIL ======================
check("③-a 一千二百件→FAIL", ng({"copy": "库存一千二百件"}, SNAP), "FAIL", "1200")
check("③-b 三千九百八十元有来源→OK", ng({"copy": "吊牌价三千九百八十元"}, SNAP), "OK")
check("③-c 六周有来源→OK", ng({"copy": "投放六周"}, SNAP), "OK")

# ============================ ④ 「八百件」快照 inventory=800 → OK ============================
check("④ 八百件→OK", ng({"copy": "库存八百件的大衣"}, SNAP), "OK")

# ============================ ⑤ 泛量词豁免 ============================
check("⑤-a 三个候选→OK", ng({"copy": "给出三个候选"}, SNAP), "OK")
check("⑤-b 两套穿搭→OK", ng({"copy": "两套穿搭方案"}, SNAP), "OK")
check("⑤-c 阿拉伯泛量词 7 个步骤→OK", ng({"copy": "共 7 个步骤"}, SNAP), "OK")
check("⑤-d 标识符内数字跳过", ng({"copy": "见 IMG_0565 / ACC-HXJ-001 / 尺码 S1"}, SNAP), "OK")
check("⑤-e ISO 时间戳整体跳过", ng({"created_at": "2026-08-17T00:00:00Z"}, SNAP), "OK")

# ---- 边界：JSON 数值型字段也进检（v0.1 的 _texts 只收 str，此洞为侦察补记）----
check("⑥-0 JSON数值型 inventory=1200→FAIL", ng({"inventory": 1200}, SNAP), "FAIL", "1200")

# ============================ ⑥ BD-D01 三夹具回归 ============================
BD = os.path.join(ROOT, "acceptance/cases/BD-D01/fixtures")
# 块 E ②：快照已是引用式，⑥ 走与 run_case.py 同一解引用入口（两套判据=假绿温床）
sys.path.insert(0, ROOT)
from kernel.facts import materialize_legacy_view as _mlv
bd_snap = _mlv(json.load(open(os.path.join(BD, "context_snapshot.json"), encoding="utf-8")))
bd_args = {"snapshot_fields": ["inventory", "price"]}   # 与 acceptance/cases/BD-D01/case.yaml A5 一致
for fixture, want, contains in (
    ("output_good.json", "OK", None),
    ("output_bad_candidate_collapse.json", "OK", None),
    # 二元组断言：不仅要红，还要红在 business_problem 这个字段上（注错点本身），
    # 且必须被判成 inventory 类——防「红在别处也算过」与「退回裸数字兜底也算过」两种退化。
    ("output_bad_fabricated_inventory.json", "FAIL", ("1200", "inventory 类", "@ business_problem")),
):
    out = json.load(open(os.path.join(BD, fixture), encoding="utf-8"))
    check(f"⑥ BD-D01/{fixture}", ng(out, bd_snap, **bd_args), want, contains)

# 夹具注释字段（`_` 开头）不得参与判定：去掉注释后判定必须**完全不变**
_bd_bad = json.load(open(os.path.join(BD, "output_bad_fabricated_inventory.json"), encoding="utf-8"))
_bd_bad_clean = {k: v for k, v in _bd_bad.items() if not k.startswith("_")}
check("⑥-note 去掉 _fixture_note 后判定不变",
      ng(_bd_bad_clean, bd_snap, **bd_args), "FAIL", ("1200", "@ business_problem"))
check("⑥-note 注释里的数字不给输出背书",
      ng({"copy": "库存 4321 件"}, {"_fixture_note": "库存 4321 件", "facts": {"inventory": {"value": 800}}}),
      "FAIL", "4321")

# ============ ⑥-x 明示夸张标注通道（Founder 2026-08-18 内容真实性三层边界 R2；只做标注位零识别智能）============
check("⑥-x1 标注的夸张数字放行且留痕",
      ng({"copy": "这件大衣暖到能卖一百万件", "_explicit_exaggeration": [1000000]}, SNAP),
      "OK", "明示夸张标注豁免")
check("⑥-x2 同一数字未标注照拦（标注通道不是默认放行）",
      ng({"copy": "这件大衣暖到能卖一百万件"}, SNAP),
      "FAIL", "无")
check("⑥-x3 标注项解析不出数值→UNKNOWN（禁整句豁免）",
      ng({"copy": "库存 4321 件", "_explicit_exaggeration": ["整句都算夸张"]}, SNAP),
      "UNKNOWN", "解析不出数值")

# ============================ ⑦ UNKNOWN 冒泡（禁 default:false）============================
check("⑦-a 快照缺失→UNKNOWN", checks.numeric_grounding({"copy": "库存 800 件"}, {"repo_root": ROOT}), "UNKNOWN", "未加载")
check("⑦-b 守卫字段缺失→UNKNOWN", ng({"copy": "库存 800 件"}, SNAP, snapshot_fields=["nonexistent_field"]), "UNKNOWN", "守卫字段")
check("⑦-c 守卫字段子串不再蒙混", ng({"copy": "库存 800 件"}, SNAP, snapshot_fields=["invent"]), "UNKNOWN", "守卫字段")
check("⑦-d 守卫字段存在→正常判定", ng({"copy": "库存 800 件"}, SNAP, snapshot_fields=["inventory", "price"]), "OK")

# ---- threshold 语义：仅作用于无单位裸数字 ----
check("⑧-a threshold 不豁免带单位数字", ng({"copy": "限时价 49 元"}, SNAP, threshold=1000), "FAIL", "49")
check("⑧-b threshold 抬高可放行裸数字", ng({"copy": "编号 77777 备注"}, SNAP, threshold=100000), "OK")
check("⑧-c 默认 threshold=0 裸数字全查", ng({"copy": "编号 77777 备注"}, SNAP), "FAIL", "77777")

# ---- 其余 check 未被本次改动触及的存活性冒烟（只读，不改它们）----
check("⑨-a human_gate_flag 缺失→UNKNOWN", checks.human_gate_flag({}, {}), "UNKNOWN")
check("⑨-b human_gate_flag=false→FAIL", checks.human_gate_flag({"human_selection_required": False}, {}), "FAIL")

# ==========================================================================================
# 以下为 P0-3 修复批次新增：v0.2 实测撞出的旁路，逐条钉成负向用例（每一条都对应一处已复现的假绿/假红）
# ==========================================================================================

# ---- ⑩ 单位上下文窗口：数字与单位之间插一个字，不得退回 any_pool 兜底 ----
# v0.2 实测：只有「库存 120 件」判红，下列五种变形全部假绿（尺码/价格给库存背书）。
for label, copy in (("余件", "库存 120 余件"), ("多件", "库存 120 多件"), ("来件", "库存 120 来件"),
                    ("全角括号", "库存 120（件）"), ("价格借位余件", "库存 3980 余件")):
    check(f"⑩-{label} 模糊量词插字不得绕过跨类禁令", ng({"copy": copy}, SNAP), "FAIL", "inventory 类")
check("⑩-f 单位前置（库存：3980）同样按事实类判", ng({"copy": "库存：3980"}, SNAP), "FAIL", "inventory 类")
check("⑩-g 省略单位（库存 120）同样按事实类判", ng({"copy": "库存 120"}, SNAP), "FAIL", "inventory 类")
check("⑩-h 线索词变体（库存数 3980）", ng({"copy": "库存数 3980"}, SNAP), "FAIL", "inventory 类")
check("⑩-i 十来件（整串曾被丢弃）", ng({"copy": "库存十来件"}, SNAP), "FAIL", "inventory 类")
check("⑩-j 真值仍不误报（库存 800 件）", ng({"copy": "库存 800 件"}, SNAP), "OK")

# ---- ⑪ 量级词与中文数字取值 ----
check("⑪-a 120 万件 = 1200000 不是 120", ng({"copy": "库存 120 万件"}, SNAP), "FAIL", "1200000")
check("⑪-b 一亿件（『亿』曾整体丢弃 → 假绿）", ng({"copy": "库存一亿件"}, SNAP), "FAIL", "100000000")
check("⑪-c 十万件", ng({"copy": "库存十万件"}, SNAP), "FAIL", "100000")
check("⑪-d 口语省略尾数 → UNKNOWN（禁硬转 1002）", ng({"copy": "库存一千二件"}, SNAP), "UNKNOWN", "一千二")
check("⑪-e 成语『千万』不作数量（曾假红 10000000）", ng({"copy": "千万别错过这件大衣"}, SNAP), "OK")
check("⑪-f 『一二线城市』不作数量（曾假红 2）", ng({"copy": "一二线城市主推"}, SNAP), "OK")
check("⑪-g 『三三两两』不作数量（曾假红 2）", ng({"copy": "三三两两地进店"}, SNAP), "OK")
check("⑪-h 一百零五（有零定位，不算省略尾数）", ng({"copy": "库存一百零五件"}, SNAP), "FAIL", "105")
_cn = checks._cn_to_num
assert _cn("一千二百") == 1200 and _cn("十五") == 15 and _cn("十万") == 100000 and _cn("一亿") == 1e8, "中文数字正例回归失败"
assert _cn("一千二") is None and _cn("两百五") is None and _cn("万") is None, "中文数字二义/光杆量级词未返回 None"

# ---- ⑫ 路径分类：中文子串碰撞的双向错误 ----
# 假绿方向（v0.2 实测）：『内容单元』含「元」→ price；『款式编码』含「码」→ size。
_S_COLLIDE = {"facts": {"内容单元数": 4980, "款式编码": 42}}
check("⑫-a 内容单元数 4980 不得给『售价 4980 元』背书", ng({"copy": "售价 4980 元"}, _S_COLLIDE), "FAIL", "price 类")
check("⑫-b 款式编码 42 不得给『42 码』背书", ng({"copy": "建议 42 码"}, _S_COLLIDE), "FAIL", "size 类")
for segs, want in ((["设计元素", "数量"], None), (["内容单元"], None), (["款式编码"], None),
                   (["deadline"], None), (["holidays"], None),
                   (["price"], "price"), (["tag_price"], "price"), (["库存"], "inventory"),
                   (["weeks"], "duration"), (["measurements"], "size")):
    got = checks._path_class(segs)
    check(f"⑫-path {segs} → {want}", ("OK" if got == want else "FAIL", f"实得 {got}"), "OK")

# ---- ⑬ 符号位与全角归一 ----
check("⑬-a 负号不得被静默丢弃（-800 ≠ 800）", ng({"copy": "库存变动 -800 件"}, SNAP), "FAIL", "-800")
check("⑬-b 全角千分位『3，980 元』不误报", ng({"copy": "售价 3，980 元"}, SNAP), "OK")
check("⑬-c 全角数字归一", ng({"copy": "吊牌价 ３９８０ 元"}, SNAP), "OK")

# ---- ⑭ 输出侧类型守卫（退化输入不得发绿灯）----
check("⑭-a output=None→UNKNOWN", ng(None, SNAP), "UNKNOWN", "结构化")
check("⑭-b output={}→UNKNOWN", ng({}, SNAP), "UNKNOWN", "为空")
check("⑭-c output 是错误串→UNKNOWN", ng("生成失败", SNAP), "UNKNOWN", "结构化")
check("⑭-d 无数字时 detail 不得自称已溯源", ng({"copy": "这件大衣值得长期持有"}, SNAP), "OK", "非等同于")

# ---- ⑮ 中文量词误报（CR-D01~D04 全是文案案例，假红会倒逼把检测器改松）----
check("⑮-a 『这一件外套』不是 1 件库存", ng({"copy": "这一件外套很值"}, SNAP), "OK")
check("⑮-b 『两件套穿法』不是 2 件库存", ng({"copy": "两件套穿法"}, SNAP), "OK")
check("⑮-c 『上市第一天』不是 1 天周期", ng({"copy": "上市第一天就有人问"}, SNAP), "OK")
check("⑮-d 『第 3 天』序数不作事实", ng({"copy": "上市第 3 天"}, SNAP), "OK")
check("⑮-e 序数豁免不得成为绕过通道（这 1200 件仍红）", ng({"copy": "这 1200 件大衣"}, SNAP), "FAIL", "1200")

# ---- ⑯ forbidden_expression 空词表假绿 ----
import tempfile as _tf
_lexdir = _tf.mkdtemp(prefix="lex_")
def _lex(name, text):
    p = os.path.join(_lexdir, name)
    open(p, "w", encoding="utf-8").write(text)
    return {"repo_root": _lexdir}, name
_ctx, _n = _lex("empty.yaml", "{}\n")
check("⑯-a 空词表→UNKNOWN（禁 0 词零命中假绿）",
      checks.forbidden_expression({"copy": "清仓甩卖白菜价"}, _ctx, lexicon=_n), "UNKNOWN", "0 个词条")
_ctx, _n = _lex("drift.yaml", "LOW_PRICE_SELLING:\n  a: 清仓甩卖\n")
check("⑯-b 词表结构漂移（值成 dict）→UNKNOWN",
      checks.forbidden_expression({"copy": "清仓甩卖白菜价"}, _ctx, lexicon=_n), "UNKNOWN", "0 个词条")
_ctx, _n = _lex("ok.yaml", "LOW_PRICE_SELLING:\n  - 清仓甩卖\n  - 白菜价\n")
check("⑯-c 正常词表命中→FAIL",
      checks.forbidden_expression({"copy": "清仓甩卖白菜价"}, _ctx, lexicon=_n), "FAIL", "清仓甩卖")
check("⑯-d 正常词表零命中→OK",
      checks.forbidden_expression({"copy": "值得长期持有"}, _ctx, lexicon=_n), "OK")
check("⑯-e 真仓词表存活性（结构未漂移）",
      checks.forbidden_expression({"copy": "值得长期持有"}, {"repo_root": ROOT},
                                  lexicon="acceptance/detectors/forbidden_lexicon.yaml"), "OK")

# ==========================================================================================
# 以下为 M1-EP02 考卷侧新增：四个 Intent 确定性断言（checks.py「Intent 侧确定性断言 v0.2」段）
# 每条闸都按 (正向 OK / 反向 FAIL / 证据不足 UNKNOWN) 三面各配用例——只测 OK 与 FAIL 的套件
# 测不出"读不到字段就放行"这类假绿，而那正是 C.4 铁律1 要拦的形态。
# ==========================================================================================

def _plan(**kw):
    """最小 IntentExecutionPlan 骨架：只含四条闸真正读的字段。

    刻意**不**求过 schema——结构合法性是 schema_valid（各案例 A1）的职责，
    在这里塞满 artifact/trace_bundle 全套字段只会让用例的"被测点在哪"读不出来。
    v0.2 起必须带 required_context（默认空数组）：缺失集合改并集口径后，读不到 required_context
    的输出一律冒 UNKNOWN，骨架不带它会让每条用例都停在"读不出"而测不到真正的被测点。
    """
    p = {"goal_resolution": "RESOLVED", "business_goal": "INVENTORY_ACTIVATION",
         "next_action": "CONTINUE_TO_DECISION", "required_context": [], "missing_context": [],
         "assumptions": [],
         "confidence": {"level": "MEDIUM", "basis": [], "limiting_factors": []},
         "trace_bundle": {"trace_bundle_id": "TB-T", "brand_id": "fixture-brand-01", "entries": []}}
    p.update(kw)
    return p


def _req(fp, impact="QUALITY_REDUCING", availability="MISSING"):
    """一条 ContextRequirement（A.4.2 六字段里断言用得到的四个）。

    availability 可指定：并集口径下 required_context 里的项只有 MISSING / CONFLICTING 才算缺失，
    AVAILABLE 的项必须被跳过（否则把每条已满足的需求都算成缺失，是假红方向）。
    """
    return {"field_path": fp, "purpose": "测试用途", "availability": availability, "impact": impact}


def _asum(fp, tid="TA-1", statement="暂定人设，未经确认"):
    """一条 ASSUMPTION TraceEntry，按首选绑定口径把缺失项挂在 target_paths 上。"""
    return {"trace_id": tid, "trace_type": "ASSUMPTION", "statement": statement, "target_paths": [fp]}


CTX = {"repo_root": ROOT}

# ---- ⑰ intent_goal_gate：A.5.2 约束1/2（A:563-564）----
check("⑰-a AMBIGUOUS 却填唯一目标→FAIL",
      checks.intent_goal_gate(_plan(goal_resolution="AMBIGUOUS", next_action="REQUEST_INPUT"), CTX),
      "FAIL", ("business_goal", "INVENTORY_ACTIVATION"))
check("⑰-b AMBIGUOUS 且目标为空却 CONTINUE→FAIL",
      checks.intent_goal_gate(_plan(goal_resolution="AMBIGUOUS", business_goal=None), CTX),
      "FAIL", ("next_action", "CONTINUE_TO_DECISION"))
check("⑰-c AMBIGUOUS + 目标空 + REQUEST_INPUT→OK",
      checks.intent_goal_gate(_plan(goal_resolution="AMBIGUOUS", business_goal=None,
                                    next_action="REQUEST_INPUT"), CTX), "OK")
check("⑰-d NEEDS_INPUT 同口径（约束2）→FAIL",
      checks.intent_goal_gate(_plan(goal_resolution="NEEDS_INPUT", next_action="REQUEST_INPUT"), CTX),
      "FAIL", "business_goal")
check("⑰-e RESOLVED→OK 且 detail 声明本闸不适用",
      checks.intent_goal_gate(_plan(), CTX), "OK", "不适用")
check("⑰-f goal_resolution 缺失→UNKNOWN（缺字段 ≠ 已解析）",
      checks.intent_goal_gate({"business_goal": None, "next_action": "REQUEST_INPUT"}, CTX),
      "UNKNOWN", "goal_resolution")
check("⑰-g next_action 缺失→UNKNOWN",
      checks.intent_goal_gate({"goal_resolution": "AMBIGUOUS", "business_goal": None}, CTX),
      "UNKNOWN", "next_action")
# 枚举外取值不得成为绕过通道：一个陌生的 goal_resolution 若被当成"不是非 RESOLVED"而放行，
# 只要模型把枚举写歪一个字母就能带着唯一目标继续下游。
check("⑰-h 枚举外取值仍按非 RESOLVED 判→FAIL",
      checks.intent_goal_gate(_plan(goal_resolution="RESOLVED_ISH", next_action="REQUEST_INPUT"), CTX),
      # 「四枚举」：A v0.5 起 goal_resolution 有四个取值（校准批二新增 RESOLVED_WITH_ALTERNATIVE）
      "FAIL", ("business_goal", "四枚举"))
check("⑰-i 空白串目标视为空→OK",
      checks.intent_goal_gate(_plan(goal_resolution="NEEDS_INPUT", business_goal="   ",
                                    next_action="REQUEST_INPUT"), CTX), "OK")
check("⑰-j output=None→UNKNOWN", checks.intent_goal_gate(None, CTX), "UNKNOWN", "不是 IntentExecutionPlan")
check("⑰-k output={}→UNKNOWN", checks.intent_goal_gate({}, CTX), "UNKNOWN", "空对象")

# ---- ⑱ intent_blocking_gate：A.5.2 约束3 / A.4.2（A:565 / A:394）；B:337 ----
check("⑱-a 自报阻断项却 CONTINUE→FAIL",
      checks.intent_blocking_gate(_plan(missing_context=[_req("facts.business_goal", "BLOCKING")]), CTX),
      "FAIL", ("facts.business_goal", "CONTINUE_TO_DECISION"))
check("⑱-b 阻断项 + REQUEST_INPUT→OK（本闸不适用）",
      checks.intent_blocking_gate(_plan(missing_context=[_req("facts.business_goal", "BLOCKING")],
                                        next_action="REQUEST_INPUT"), CTX), "OK", "不适用")
check("⑱-c 全 QUALITY_REDUCING + CONTINUE→OK",
      checks.intent_blocking_gate(_plan(missing_context=[_req("facts.persona")]), CTX), "OK")
check("⑱-d missing_context 缺失→UNKNOWN（字段不在场 ≠ 没有缺失项）",
      checks.intent_blocking_gate({"next_action": "CONTINUE_TO_DECISION"}, CTX), "UNKNOWN", "missing_context")
check("⑱-e impact 取值不可判 + CONTINUE→UNKNOWN（不得默认放行）",
      checks.intent_blocking_gate(_plan(missing_context=[_req("facts.persona", "MAYBE")]), CTX),
      "UNKNOWN", "impact 取值不可判")
# FAIL 优先于 UNKNOWN：已确证的阻断项不该被"另有几项读不出"冒泡掩盖
check("⑱-f 阻断项与不可判项并存→FAIL 优先",
      checks.intent_blocking_gate(_plan(missing_context=[_req("facts.business_goal", "BLOCKING"),
                                                         _req("facts.persona", "MAYBE")]), CTX),
      "FAIL", "facts.business_goal")
# 本条与 v0.1 相比多带了 required_context: []（口径变化影响的既有期望，逐条注明）：
# 并集口径下 required_context 读不出会先冒 UNKNOWN，不带它就测不到"next_action 缺失"这个被测点。
check("⑱-g next_action 缺失→UNKNOWN",
      checks.intent_blocking_gate({"missing_context": [], "required_context": []}, CTX),
      "UNKNOWN", "next_action")
check("⑱-h missing_context 非数组→UNKNOWN",
      checks.intent_blocking_gate(_plan(missing_context={"a": 1}), CTX), "UNKNOWN", "不是数组")

# ---- ⑱ 并集口径（v0.2 新增）：把阻断项只写进 required_context 不再能绕闸 ----
# 这是本批次要堵的**主通道**：missing_context 留空、阻断项藏在 required_context 里，
# v0.1 的两条闸都返回 OK（"自报的 0 项缺失均非 BLOCKING"）——一句没验过的话被写成结论。
check("⑱-i 阻断项只写 required_context + missing_context 空 + CONTINUE→FAIL",
      checks.intent_blocking_gate(
          _plan(required_context=[_req("brand.promotion_boundary", "BLOCKING")], missing_context=[]), CTX),
      "FAIL", ("brand.promotion_boundary", "CONTINUE_TO_DECISION"))
check("⑱-j required_context 里 AVAILABLE 的项不算缺失→OK（并集不得制造假红）",
      checks.intent_blocking_gate(
          _plan(required_context=[_req("facts.product", "BLOCKING", availability="AVAILABLE")]), CTX),
      "OK")
check("⑱-k CONFLICTING 视同缺失（OD-03 四-2）→FAIL",
      checks.intent_blocking_gate(
          _plan(required_context=[_req("facts.inventory", "BLOCKING", availability="CONFLICTING")]), CTX),
      "FAIL", "facts.inventory")
check("⑱-l required_context 缺失→UNKNOWN（并集的另一半读不到 ≠ 没有别的缺失项）",
      checks.intent_blocking_gate({"missing_context": [], "next_action": "CONTINUE_TO_DECISION"}, CTX),
      "UNKNOWN", "required_context")
check("⑱-m availability 取值不可判 + CONTINUE→UNKNOWN（写歪一个字母不得成为新通道）",
      checks.intent_blocking_gate(
          _plan(required_context=[_req("facts.persona", "BLOCKING", availability="MAYBE")]), CTX),
      "UNKNOWN", "availability 取值不可判")
# 同一 field_path 两处 impact 打架时取严：把阻断项在 missing_context 里降级成 QR 是最自然的绕闸写法
check("⑱-n 同一项两处 impact 打架取严→FAIL",
      checks.intent_blocking_gate(
          _plan(missing_context=[_req("brand.promotion_boundary")],
                required_context=[_req("brand.promotion_boundary", "BLOCKING")]), CTX),
      "FAIL", "brand.promotion_boundary")
check("⑱-o 并集去重：同一项两处都写 QR 只计一次→OK 且计数为 1",
      checks.intent_blocking_gate(
          _plan(missing_context=[_req("facts.persona")], required_context=[_req("facts.persona")]), CTX),
      "OK", "1 项缺失")

# ---- ⑲ intent_assumption_coverage：A.5.2 约束4 / A.4.2（A:566 / A:393）；B:321-322 ----
check("⑲-a 逐项 QR 且逐项有对应 ASSUMPTION→OK",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b", "entries": [_asum("facts.persona")]}), CTX),
      "OK")
check("⑲-b 跨过缺失却 0 条 ASSUMPTION→FAIL",
      checks.intent_assumption_coverage(_plan(missing_context=[_req("facts.persona")]), CTX),
      "FAIL", "0 条")
check("⑲-c 两项缺失只覆盖一项→FAIL 且点名未覆盖项",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona"), _req("facts.video_account")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b", "entries": [_asum("facts.persona")]}), CTX),
      "FAIL", ("facts.video_account", "找不到对应 ASSUMPTION"), "facts.persona'")
# v0.2 期望变更（口径收紧，逐条注明原因）：statement 兜底命中由 OK 降为 UNKNOWN。
# 原因：字符串包含会被更长路径前缀、被复述缺失清单的一句话顺带满足（见 ⑲-o/⑲-p 两条新用例），
# 用它发绿灯即假绿；但它也不能证明"没有对应"，故冒泡而不是判红。
check("⑲-d statement 字面兜底命中→UNKNOWN（v0.1 判 OK，假绿方向已堵）",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b",
                              "entries": [{"trace_id": "TA-9", "trace_type": "ASSUMPTION",
                                           "statement": "facts.persona 暂按通用主理人口吻处理"}]}), CTX),
      "UNKNOWN", ("facts.persona", "target_paths"))
check("⑲-e CONTINUE 跨过 BLOCKING→FAIL（约束4 只允许跨 QUALITY_REDUCING）",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.business_goal", "BLOCKING")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b",
                              "entries": [_asum("facts.business_goal")]}), CTX),
      "FAIL", "BLOCKING")
check("⑲-f REQUEST_INPUT→OK（本闸不适用）",
      checks.intent_assumption_coverage(_plan(missing_context=[_req("facts.persona")],
                                              next_action="REQUEST_INPUT"), CTX), "OK", "不适用")
check("⑲-g CONTINUE 且无缺失→OK",
      checks.intent_assumption_coverage(_plan(), CTX), "OK", "无被跨过的缺失项")
# 同 ⑱-g 的理由，本条也补 required_context: []（否则会停在并集口径的 UNKNOWN，测不到被测点）
check("⑲-h trace_bundle 与 assumptions 均读不出→UNKNOWN",
      checks.intent_assumption_coverage({"next_action": "CONTINUE_TO_DECISION",
                                         "required_context": [],
                                         "missing_context": [_req("facts.persona")]}, CTX),
      "UNKNOWN", "无从核验")
check("⑲-i ASSUMPTION 写在顶层 assumptions 数组里也算（并集）→OK",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")], assumptions=[_asum("facts.persona")]), CTX), "OK")
# FACT 类 trace 不得顶替 ASSUMPTION：把"暂定人设"写成 FACT 正是 B:324「不把暂定人设写成事实」要拦的形态
check("⑲-j FACT 类 trace 不顶替 ASSUMPTION→FAIL",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b",
                              "entries": [{"trace_id": "TF-1", "trace_type": "FACT",
                                           "statement": "主理人是资深买手", "target_paths": ["facts.persona"]}]}), CTX),
      "FAIL", "0 条")
check("⑲-k statement 结构漂移（非字符串）不炸且不假绿→FAIL",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b",
                              "entries": [{"trace_id": "TA-8", "trace_type": "ASSUMPTION",
                                           "statement": {"text": "facts.persona"}}]}), CTX),
      "FAIL", "找不到对应 ASSUMPTION")
check("⑲-m entries 结构漂移（非数组）→UNKNOWN 而非假红 FAIL",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")],
                trace_bundle={"trace_bundle_id": "TB-T", "brand_id": "b",
                              "entries": {"TA-1": _asum("facts.persona")}}), CTX),
      "UNKNOWN", "不是数组")
check("⑲-l field_path 不可读→UNKNOWN",
      checks.intent_assumption_coverage(
          _plan(missing_context=[{"field_path": None, "impact": "QUALITY_REDUCING"}],
                assumptions=[_asum("facts.persona")]), CTX),
      "UNKNOWN", "不可读")

# ---- ⑲ 并集口径 + 兜底降级（v0.2 新增）----
# ⑲-n：只写在 required_context 里的缺失项同样是"被跨过的缺失"，同样必须留假设。
#      v0.1 只读 missing_context，这一形态返回 OK（"无被跨过的缺失项"）= 假绿。
check("⑲-n 只写 required_context 的缺失项也要有 ASSUMPTION→FAIL",
      checks.intent_assumption_coverage(
          _plan(required_context=[_req("facts.video_account")], missing_context=[],
                assumptions=[_asum("facts.persona")]), CTX),
      "FAIL", ("facts.video_account", "找不到对应 ASSUMPTION"))
check("⑲-o 兜底假绿形态一：更长路径前缀顺带命中→UNKNOWN 不再 OK",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona")],
                assumptions=[{"trace_id": "TA-7", "trace_type": "ASSUMPTION",
                              "statement": "facts.persona.tone 暂按品牌书的沉稳口吻处理",
                              "target_paths": ["facts.persona.tone"]}]), CTX),
      "UNKNOWN", "facts.persona")
check("⑲-p 兜底假绿形态二：一句复述缺失清单的话顺带命中两项→UNKNOWN",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona"), _req("facts.video_account")],
                assumptions=[{"trace_id": "TA-6", "trace_type": "ASSUMPTION",
                              "statement": "本次跨过 facts.persona、facts.video_account 两项缺失，按通用口径处理"}]),
          CTX),
      "UNKNOWN", ("facts.persona", "facts.video_account"))
check("⑲-q 补上 target_paths 即可恢复 OK（UNKNOWN 有明确消除路径，不是死结）",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona"), _req("facts.video_account")],
                assumptions=[{"trace_id": "TA-6", "trace_type": "ASSUMPTION",
                              "statement": "本次跨过两项缺失，按通用口径处理",
                              "target_paths": ["facts.persona", "facts.video_account"]}]), CTX),
      "OK")
# 确凿未对应仍优先判 FAIL：兜底降级不得把已确证的"根本没这条假设"稀释成 UNKNOWN
check("⑲-r 一项兜底命中 + 一项完全没有→FAIL 优先于 UNKNOWN",
      checks.intent_assumption_coverage(
          _plan(missing_context=[_req("facts.persona"), _req("facts.video_account")],
                assumptions=[{"trace_id": "TA-5", "trace_type": "ASSUMPTION",
                              "statement": "facts.persona 暂按通用口吻处理"}]), CTX),
      "FAIL", "facts.video_account")
check("⑲-s required_context 缺失→UNKNOWN（同 ⑱-l，并集另一半读不到）",
      checks.intent_assumption_coverage({"next_action": "CONTINUE_TO_DECISION",
                                         "missing_context": [_req("facts.persona")],
                                         "assumptions": [_asum("facts.persona")]}, CTX),
      "UNKNOWN", "required_context")

# ---- ⑳ intent_confidence_cap：B:292（另见 B:323）----
check("⑳-a 目标未定却 HIGH→FAIL",
      checks.intent_confidence_cap(_plan(goal_resolution="AMBIGUOUS",
                                         confidence={"level": "HIGH", "basis": [], "limiting_factors": []}), CTX),
      "FAIL", ("AMBIGUOUS", "HIGH"))
check("⑳-b 目标未定 + MEDIUM→OK",
      checks.intent_confidence_cap(_plan(goal_resolution="NEEDS_INPUT"), CTX), "OK")
check("⑳-c RESOLVED + HIGH→OK（本闸不适用；RESOLVED 是否站得住脚属人工面）",
      checks.intent_confidence_cap(_plan(confidence={"level": "HIGH", "basis": [], "limiting_factors": []}), CTX),
      "OK", "不适用")
check("⑳-d confidence 缺失→UNKNOWN（读不到 ≠ 未超标）",
      checks.intent_confidence_cap({"goal_resolution": "AMBIGUOUS"}, CTX), "UNKNOWN", "confidence")
check("⑳-e confidence.level 缺失→UNKNOWN",
      checks.intent_confidence_cap(_plan(goal_resolution="AMBIGUOUS", confidence={"basis": []}), CTX),
      "UNKNOWN", "level")
check("⑳-f goal_resolution 缺失→UNKNOWN",
      checks.intent_confidence_cap({"confidence": {"level": "HIGH"}}, CTX), "UNKNOWN", "goal_resolution")

# ---- ㉑ 考卷绑定冒烟：三份 INT case.yaml 的每条 must_hold 都必须绑得到检测器 ----
# 为什么要在检测器套件里放这一条：run_case.py 对不存在的检测器名只冒 UNKNOWN，而 UNKNOWN 不进
# l1_fail_tags、不改终态——考卷里写错一个函数名，整份回执照样 PENDING_HUMAN，没人看得出那条断言压根没跑。
for _cid in ("INT-D01", "INT-D02", "INT-D03"):
    _cpath = os.path.join(ROOT, "acceptance/cases", _cid, "case.yaml")
    with open(_cpath, encoding="utf-8") as _f:
        _case = yaml.safe_load(_f)
    _items = _case.get("must_hold") or []
    _bad = [i.get("check") for i in _items if not callable(getattr(checks, i.get("check") or "", None))]
    _notag = [i.get("id") for i in _items if not (i.get("tag") or "").strip()]
    check(f"㉑-{_cid} must_hold {len(_items)} 条全部绑得到检测器且带 tag",
          ("OK" if (_items and not _bad and not _notag) else "FAIL",
           f"条数={len(_items)} 未绑定={_bad} 缺tag={_notag}"), "OK")

# ---- ㉒ 判分批修复（Founder 2026-08-18 批准「中文量词与成语里的『一』不作数字提取、系统留痕
# 中的条款号豁免」，负向测试先行）：用例字符串逐字取自 RUN-0006/0007/0008 真实误报现场
# （L3-判分记录-INT-20260818.md + 台账已批准行）。㉒-f/g/h 是真阳性护栏：修复不得放走真编造。 ----
_SNAP22 = {"product": {"inventory": {"value": 800, "unit": "件"}, "price": {"value": 3980, "currency": "CNY"}}}
check("㉒-a 成语「一致」的一不作数量（RUN-0006 basis 原文，左窗口有库存线索也不判）",
      ng({"intent_summary": "用户显式声明目标，且事实池中产品生命周期阶段与库存数据一致支持该目标。"}, _SNAP22), "OK")
check("㉒-b 「一类」的一不作数量（RUN-0008 limiting_factors 原文）",
      ng({"confidence": {"limiting_factors": ["缺 product.material_proof（QUALITY_REDUCING）：面料成分有没有检测报告或吊牌照片一类的凭证？"]}}, _SNAP22), "OK")
check("㉒-c 量词「（为）一件」的一不作数量（RUN-0006 summary 句式；800 件本身必须可溯源）",
      ng({"intent_summary": "任务要求为一件处于库存消化期的羊绒大衣制作内容，库存量为800件。"}, _SNAP22), "OK")
check("㉒-d 系统留痕条款号豁免：confidence.basis 里的「约束5 / A.5.2 / A.4.2」（RUN-0006 basis 原文）",
      ng({"confidence": {"basis": ["闸留痕：系统改判：模型判 RESOLVED，存在阻断缺失 brand.promotion_boundary，改为 NEEDS_INPUT（A.5.2 约束5 / A.4.2）"]}}, _SNAP22), "OK")
check("㉒-e 系统留痕条款号豁免：resolution_question 模板句里的 B 行号引用",
      ng({"missing_context": [{"field_path": "task_input.business_goal", "resolution_question": "这条视频想达成什么？（B:285-286 只问一个最关键问题）"}]}, _SNAP22), "OK")
check("㉒-f 真阳性不松：多字中文数量「三千件」无源仍 FAIL",
      ng({"intent_summary": "库存三千件亟待消化。"}, _SNAP22), "FAIL", "3000")
check("㉒-g 豁免只限条款号：系统留痕里冒出的无源价格仍 FAIL",
      ng({"confidence": {"basis": ["按售价2999元估算折扣空间"]}}, _SNAP22), "FAIL", "2999")
check("㉒-h 真阳性不松：正文无源阿拉伯数字仍 FAIL",
      ng({"intent_summary": "预计触达5000人。"}, _SNAP22), "FAIL", "5000")

# ---- ㉓ 判分批新增两闸（intent_terminal_state / intent_candidate_completeness）----
_CTX23 = {"repo_root": ROOT}
check("㉓-a 终态符合考卷声明→OK",
      checks.intent_terminal_state({"goal_resolution": "RESOLVED", "business_goal": "DAILY_CONTENT_OPERATION",
                                    "next_action": "CONTINUE_TO_DECISION"}, _CTX23,
                                   expect_goal_resolution="RESOLVED",
                                   expect_business_goal="DAILY_CONTENT_OPERATION",
                                   expect_next_action="CONTINUE_TO_DECISION"), "OK")
check("㉓-b 把任务升级成选择题→FAIL（终态落 REQUEST_INPUT）",
      checks.intent_terminal_state({"goal_resolution": "AMBIGUOUS", "business_goal": None,
                                    "next_action": "REQUEST_INPUT"}, _CTX23,
                                   expect_goal_resolution="RESOLVED",
                                   expect_business_goal="DAILY_CONTENT_OPERATION",
                                   expect_next_action="CONTINUE_TO_DECISION"), "FAIL", "REQUEST_INPUT")
check("㉓-c 考卷未声明预期→UNKNOWN（禁默认放行）",
      checks.intent_terminal_state({"goal_resolution": "RESOLVED"}, _CTX23), "UNKNOWN")
check("㉓-d expect=null 语义：business_goal 非空→FAIL",
      checks.intent_terminal_state({"business_goal": "CONVERSION"}, _CTX23, expect_business_goal="null"),
      "FAIL", "CONVERSION")
_CAND_OK = {"goal": "BRAND_STORY", "rationale": "r", "focus": "侧重故事", "tradeoffs": "深但慢", "expected_outcome": "认同"}
_CAND_BARE = {"goal": "BRAND_AWARENESS", "rationale": "r"}
check("㉓-e AMBIGUOUS 候选三要素齐→OK",
      checks.intent_candidate_completeness({"goal_resolution": "AMBIGUOUS",
                                            "goal_candidates": [_CAND_OK, dict(_CAND_OK, goal="BRAND_AWARENESS")]},
                                           _CTX23), "OK")
check("㉓-f 光秃标签候选→FAIL",
      checks.intent_candidate_completeness({"goal_resolution": "AMBIGUOUS",
                                            "goal_candidates": [_CAND_OK, _CAND_BARE]}, _CTX23),
      "FAIL", "BRAND_AWARENESS")
check("㉓-g 候选不足两个→FAIL",
      checks.intent_candidate_completeness({"goal_resolution": "AMBIGUOUS", "goal_candidates": [_CAND_OK]},
                                           _CTX23), "FAIL")
check("㉓-h 非 AMBIGUOUS 不适用→OK 且注明",
      checks.intent_candidate_completeness({"goal_resolution": "RESOLVED", "goal_candidates": []}, _CTX23),
      "OK", "不适用")

# ---- ㉔ 复判批新增：intent_situational_alternative（统一产品标准⑥ / A.5.2 约束8 / OD-03 §五）----
# **测试先行**：本块先于检测器实现写下并实跑（首跑 AttributeError＝检测器不存在，红证在批次回执里），
# 实现后转全绿。用例现场取自 RUN-0013/0014——模型内部写下「该产品处于库存消化期…因此不能据此推断
# 目标为 INVENTORY_ACTIVATION」后用户侧零呈现，即第⑥条所指「装作不知道」。
_SNAP24 = {"facts": {"product": {"lifecycle_stage": {"status": "CONFIRMED", "value": "库存消化期"},
                                 "name": {"status": "CONFIRMED", "value": "羊绒风衣式大衣"}}}}
_CTX24 = {"repo_root": ROOT, "snapshot": _SNAP24}
_CTX24_NOSIT = {"repo_root": ROOT, "snapshot": {"facts": {"product": {"lifecycle_stage": {"value": "在售新品"}}}}}
_ARGS24 = dict(situation_field="product.lifecycle_stage", situation_value="库存消化期",
               alternative_goal="INVENTORY_ACTIVATION", primary_goal="DAILY_CONTENT_OPERATION")
_C_PRIMARY = {"goal": "DAILY_CONTENT_OPERATION", "rationale": "按用户原话", "focus": "春节主题种草",
              "tradeoffs": "稳但不冲量", "expected_outcome": "商品被看见被理解"}
_C_ALT = {"goal": "INVENTORY_ACTIVATION", "rationale": "FACT:product.lifecycle_stage", "focus": "节前动销",
          "tradeoffs": "见效快但偏促销口吻", "expected_outcome": "库存消化"}
_PAIR = {"goal_resolution": "RESOLVED_WITH_ALTERNATIVE", "business_goal": "DAILY_CONTENT_OPERATION",
         "next_action": "REQUEST_INPUT", "goal_candidates": [_C_PRIMARY, _C_ALT]}
check("㉔-a 情境在场却径直按常规继续→FAIL（装作不知道；RUN-0013/0014 现场）",
      checks.intent_situational_alternative({"goal_resolution": "RESOLVED", "business_goal": "DAILY_CONTENT_OPERATION",
                                             "next_action": "CONTINUE_TO_DECISION", "goal_candidates": []},
                                            _CTX24, **_ARGS24), "FAIL", "库存消化期")
check("㉔-b 擅自把目标转向情境目标→FAIL",
      checks.intent_situational_alternative({"goal_resolution": "RESOLVED", "business_goal": "INVENTORY_ACTIVATION",
                                             "next_action": "CONTINUE_TO_DECISION", "goal_candidates": []},
                                            _CTX24, **_ARGS24), "FAIL", "擅自转向")
check("㉔-c 并呈双方案三要素齐＋停在选择点→OK",
      checks.intent_situational_alternative(dict(_PAIR), _CTX24, **_ARGS24), "OK")
check("㉔-d 并呈但只有主方案一个候选→FAIL",
      checks.intent_situational_alternative(dict(_PAIR, goal_candidates=[_C_PRIMARY]), _CTX24, **_ARGS24),
      "FAIL", "INVENTORY_ACTIVATION")
check("㉔-e 并呈但备选缺三要素（光秃标签）→FAIL",
      checks.intent_situational_alternative(
          dict(_PAIR, goal_candidates=[_C_PRIMARY, {"goal": "INVENTORY_ACTIVATION", "rationale": "r"}]),
          _CTX24, **_ARGS24), "FAIL", "三要素")
check("㉔-f 主备颠倒（business_goal 写成情境目标）→FAIL",
      checks.intent_situational_alternative(dict(_PAIR, business_goal="INVENTORY_ACTIVATION"), _CTX24, **_ARGS24),
      "FAIL", "主目标")
check("㉔-g 并呈却仍 CONTINUE（备选代替了人工选择）→FAIL",
      checks.intent_situational_alternative(dict(_PAIR, next_action="CONTINUE_TO_DECISION"), _CTX24, **_ARGS24),
      "FAIL", "REQUEST_INPUT")
check("㉔-h 快照里根本没有该情境→UNKNOWN（考卷与夹具漂移，禁默认放行）",
      checks.intent_situational_alternative({"goal_resolution": "RESOLVED", "business_goal": "DAILY_CONTENT_OPERATION",
                                             "next_action": "CONTINUE_TO_DECISION"}, _CTX24_NOSIT, **_ARGS24),
      "UNKNOWN")
check("㉔-i 考卷未声明情境（args 全空）→UNKNOWN",
      checks.intent_situational_alternative({"goal_resolution": "RESOLVED"}, _CTX24), "UNKNOWN")
check("㉔-j 目标尚未解析（AMBIGUOUS）→UNKNOWN（窄口径：非「闷头开做」场合，不判绿也不判红）",
      checks.intent_situational_alternative({"goal_resolution": "AMBIGUOUS", "business_goal": None,
                                             "next_action": "REQUEST_INPUT"}, _CTX24, **_ARGS24), "UNKNOWN")
# ㉔-k/l：intent_goal_gate 对新枚举值的口径（A v0.5 约束8）。新状态**按定义**带非空主目标，
# 故约束1/2 的「非 RESOLVED 必须清空 business_goal」对它不适用；但「必须停在 REQUEST_INPUT」照判。
# 没有这两条，A5 闸会把合法的并呈形态误判成 INT_GOAL_ASSUMED（实测：D02 试跑首次即如此）。
_PLAN_ALT = {"goal_resolution": "RESOLVED_WITH_ALTERNATIVE", "business_goal": "DAILY_CONTENT_OPERATION",
             "next_action": "REQUEST_INPUT", "required_context": [], "missing_context": [],
             "assumptions": [], "confidence": {"level": "LOW"}}
check("㉔-k 并呈状态带非空主目标不再误判 INT_GOAL_ASSUMED→OK",
      checks.intent_goal_gate(dict(_PLAN_ALT), _CTX23), "OK", "约束8")
check("㉔-l 并呈状态却 CONTINUE（备选代替人工选择）→FAIL",
      checks.intent_goal_gate(dict(_PLAN_ALT, next_action="CONTINUE_TO_DECISION"), _CTX23),
      "FAIL", "交回人工")

# ---- ㉕ 数字表达裁决（Founder 2026-08-18 尾批）：保守概括通道 numeric_grounding v0.5 ----
# **负向测试先行**：本块先于 v0.5 判据写下，用 `git show HEAD:acceptance/detectors/checks.py`
# 的旧版实跑取「先红」证据——旧口径下 ㉕-a 红（该绿判红）、㉕-b/c 绿（该红判绿，且 ㉕-b/c 的绿
# 是**碰巧**：商品名「10%羊绒风衣式大衣」把 10 送进 percent 池），共 3 项不符期望。
# 裁决封闭清单：a)「X以上／不低于X」需 X ≤ 同类最小值；b)「不超过X／X以下」需 X ≥ 同类最大值；
# c) 原值区间；d) 原值列举。方向只许保守；「约/接近/大概/左右」维持禁止。
_SNAP25 = {"product": {"inventory": {"value": 800, "unit": "件"},
                       "price": {"value": 3980, "currency": "CNY"},
                       "name": {"value": "10%羊绒风衣式大衣"},
                       "material": {"value": ["黑色面料:90.2%绵羊毛 9.8%山羊绒", "米色面料:90.3%绵羊毛 9.7%山羊绒",
                                              "晓雾灰面料:90.8%绵羊毛 9.2%山羊绒", "云烟灰面料:90.1%绵羊毛 9.9%山羊绒"]}}}
# —— 裁决四判例，逐条钉死 ——
check("㉕-a 判例1「9%以上」→OK（9 ≤ 同类最小值 9.2，下界往低取）",
      ng({"intent_summary": "该商品含9%以上山羊绒。"}, _SNAP25), "OK", "保守概括通道放行")
check("㉕-b 判例2「10%以上」→FAIL（向上取整；10 碰巧在 percent 池里也不免责）",
      ng({"intent_summary": "该商品含10%以上山羊绒。"}, _SNAP25), "FAIL", ("方向不保守", "9.2"))
check("㉕-c 判例3「约10%」→FAIL（不可判定形式，维持禁止）",
      ng({"intent_summary": "该商品含约10%山羊绒。"}, _SNAP25), "FAIL", "不可判定的近似表达")
check("㉕-d 判例4「9.2%–9.9%」→OK（原值区间，走精确命中）",
      ng({"intent_summary": "山羊绒含量9.2%–9.9%。"}, _SNAP25), "OK")
# —— 封闭清单其余三形 ——
check("㉕-e 原值列举→OK",
      ng({"intent_summary": "四色山羊绒含量分别为9.8%、9.7%、9.2%、9.9%。"}, _SNAP25), "OK")
check("㉕-f 「不低于9%」→OK（下界同义词）",
      ng({"intent_summary": "山羊绒不低于9%。"}, _SNAP25), "OK", "不低于")
check("㉕-g 上界「不超过1000件」→OK（1000 ≥ 同类最大值 800）",
      ng({"intent_summary": "库存不超过1000件。"}, _SNAP25), "OK", "同类最大值 800")
check("㉕-h 上界方向反了「不超过500件」→FAIL（须 ≥ 最大值）",
      ng({"intent_summary": "库存不超过500件。"}, _SNAP25), "FAIL", "只许往高取")
check("㉕-i 下界方向反了「900件以上」→FAIL",
      ng({"intent_summary": "库存900件以上。"}, _SNAP25), "FAIL", "只许往低取")
check("㉕-j 边界值可取「800件以上」→OK（等于最小值，≤ 成立）",
      ng({"intent_summary": "库存800件以上。"}, _SNAP25), "OK")
# —— 不可判定形式全家桶（即使数值精确命中快照也判红）——
check("㉕-k 「3980元左右」→FAIL（3980 是快照原值，但「左右」不可判定）",
      ng({"intent_summary": "定价3980元左右。"}, _SNAP25), "FAIL", "左右")
check("㉕-l 「接近800件」→FAIL", ng({"intent_summary": "库存接近800件。"}, _SNAP25), "FAIL", "接近")
check("㉕-m 「大概3980元」→FAIL", ng({"intent_summary": "售价大概3980元。"}, _SNAP25), "FAIL", "大概")
# —— 反向护栏：本裁决不得扩张为任意近似数字放行（红线原样）——
check("㉕-n 真编造仍红：「三千件」（概括通道不给无界数字开口子）",
      ng({"intent_summary": "库存三千件。"}, _SNAP25), "FAIL", "3000")
check("㉕-o 真编造仍红：「2999元」", ng({"intent_summary": "售价2999元。"}, _SNAP25), "FAIL", "2999")
check("㉕-p 真编造带界也红：「5000件以上」（界标记不是免死金牌）",
      ng({"intent_summary": "库存5000件以上。"}, _SNAP25), "FAIL", "只许往低取")
# —— 不误伤既有通道 ——
check("㉕-q 条款号仍豁免：basis 里「约束5」的「约」不得判成近似表达",
      ng({"confidence": {"basis": ["闸留痕：改为 NEEDS_INPUT（A.5.2 约束5 / A.4.2）"]}}, _SNAP25), "OK")
check("㉕-r 无界原值仍走精确命中：「库存800件」→OK",
      ng({"intent_summary": "库存800件。"}, _SNAP25), "OK")
# —— 射程边界如实登记（类级池混装导致的假红，不藏）——
check("㉕-s 【已知假红·类级池】「绵羊毛90%以上」→FAIL（percent 池混装山羊绒 9.x，最小值 9.2）",
      ng({"intent_summary": "面料含绵羊毛90%以上。"}, _SNAP25), "FAIL", "方向不保守")


for line in PASSED:
    print(line)
for line in FAILURES:
    print(line)
print(f"\n合计 {len(PASSED) + len(FAILURES)} 项：通过 {len(PASSED)}，失败 {len(FAILURES)}")
sys.exit(1 if FAILURES else 0)
