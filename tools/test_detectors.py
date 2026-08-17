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
"""
import importlib.util, json, os, sys

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
bd_snap = json.load(open(os.path.join(BD, "context_snapshot.json"), encoding="utf-8"))
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

for line in PASSED:
    print(line)
for line in FAILURES:
    print(line)
print(f"\n合计 {len(PASSED) + len(FAILURES)} 项：通过 {len(PASSED)}，失败 {len(FAILURES)}")
sys.exit(1 if FAILURES else 0)
