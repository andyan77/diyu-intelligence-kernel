#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kernel/decision 资产③：确定性前处理（BusinessDecisionRequest 装配 + 事实/规则池物化 + 输入闸）。

【M2-EP01 提前段·非正式证据】

职责边界：
  1. `load_plan(path)` / `load_snapshot(path)`——只读原始 dict；
  2. `materialize_fact_pool(snapshot)`——把快照事实压成可引用的扁平池（模型只许引用池内 ID）；
  3. `load_rule_pool()` / `filter_rule_pool_by_brand(pool, brand_id)`——读 RuleRecord 注册表并按品牌过滤；
  4. `check_input_gates(plan, snapshot, rule_pool)`——生成前输入闸 IG1-IG6（G.2 第 4 条双阶段命名的
     Preflight 侧，落 A.5.2 / A.1.3 / OD-03 既有语义）；
  5. `build_request(plan, snapshot, rule_pool)`——按 A.6.1 装配 BusinessDecisionRequest（证据回显用）。

每一条判定都必须是同一份输入必得同一份输出的纯函数——不读时钟、不读随机、不读网络、
不看模型说了什么。

诚实边界（写在最前面，免得被当成"已覆盖"）：
  ① 快照消费走 kernel/facts 官方收敛通道（块 E 落地后本批合流适配）：load_snapshot =
     R1-R5/P2/P3 运行时谓词 fail-closed → materialize_legacy_view 解引用产出内联兼容视图，
     与 kernel/intent/preprocess.load_snapshot 同款接线；旧内联形状**直接拒绝**（两套形状
     并行 = 假闭环温床，E-05 口径）。原登记的「快照双形状」缺口（UPSTREAM_GAPS 第 2 条）
     随块 E 迁移关闭，本文件按预案只改本层、零改断言口径。
  ② 视图内 MISSING 叶子原样进池（value=null, status=MISSING），**不补写不剔除**——
     缺失可见是 A.1.4 的前提；status 语义级核验（如禁引 MISSING 作支撑）属后续批次。
  ③ 输入闸 IG3 只核验上游 plan 的**自洽性**（BLOCKING 必须 AVAILABLE、missing 无 BLOCKING），
     **不复算 OD-03 需求清单**——复算 = 代上游（Intent）定义语义，越车道。上游算错时本闸看不见，
     该风险属上游考卷（INT 系列）判分面。
  ④ 规则池唯一来源 = 快照视图的 hard_rules（A.4.3 active_rule_refs 解引用产物，快照钉定
     本次运行的规则集）；本模块**不再**自行扫 contracts/rules 全量目录——两个来源并存
     就是「同一事实两个落点」。
"""

import json

from .config import (
    AVAILABILITY_AVAILABLE,
    FACT_ID_PREFIX,
    GOAL_RESOLUTION_RESOLVED,
    IMPACT_BLOCKING,
    NEXT_ACTION_CONTINUE,
    OUTPUT_SCHEMA_VERSION,
)


def load_snapshot(path):
    """读 A.4.3 引用式 Context Snapshot → 运行时谓词 → 解引用，返回内联兼容视图 dict。

    与 kernel/intent/preprocess.load_snapshot 同款接线（诚实边界①）：
      1. kernel.facts.predicates.run_all_runtime：snapshot_hash 实算 / 引用可解析且 ACTIVE /
         BrandMemory 首轮必空 / locator 无明文凭证 / 同 ID 同版本禁覆盖 / P2 / P3，任何红即抛错；
      2. kernel.facts.resolve.materialize_legacy_view：解引用产出内联兼容视图
         {snapshot_id, task_id, brand_id, version, facts, hard_rules}，旧内联形状直接拒绝。
    视图不含任何 `_` 前缀键（解引用层已剔除迁移注解，防泄题与过期数值溯源面）。
    """
    with open(path, encoding="utf-8") as f:
        snapshot = json.load(f)
    if not isinstance(snapshot, dict):
        raise ValueError(f"快照不是 JSON 对象：{type(snapshot).__name__}（{path}）")
    from kernel.facts import FactStore, materialize_legacy_view, predicates as _fact_predicates
    store = FactStore()
    red = _fact_predicates.run_all_runtime(snapshot, store)
    if red:
        raise ValueError("快照未过 kernel/facts 运行时谓词（R1-R5/P2/P3），拒绝装载：\n  " + "\n  ".join(red))
    return materialize_legacy_view(snapshot, store)


def load_plan(path):
    """读冻结 IntentExecutionPlan 原始 dict（C.3 资产⑥：上游冻结 fixture，B.4 模块隔离）。"""
    with open(path, encoding="utf-8") as f:
        plan = json.load(f)
    if not isinstance(plan, dict):
        raise ValueError(f"IntentExecutionPlan 不是 JSON 对象：{type(plan).__name__}（{path}）")
    return plan


# ============================ 事实池物化 ============================

def _walk_facts(node, path, out):
    """深度优先展开 facts 子树。`_` 开头的键是注释/元数据（夹具注释约定），一律跳过。"""
    if isinstance(node, dict):
        if "value" in node:
            # 形如 {value, unit?, source?, status?} 的事实叶子
            out.append({
                "fact_id": FACT_ID_PREFIX + path,
                "field_path": path,
                "value": node.get("value"),
                "unit": node.get("unit"),
                "status": node.get("status"),
                "source": node.get("source"),
            })
            return
        for key in node:
            if isinstance(key, str) and key.startswith("_"):
                continue
            _walk_facts(node[key], f"{path}.{key}" if path else key, out)
        return
    if isinstance(node, list):
        # 列表按元素展开；标量列表（如 sizes）整体作为一个事实值
        if all(not isinstance(item, (dict, list)) for item in node):
            out.append({
                "fact_id": FACT_ID_PREFIX + path,
                "field_path": path,
                "value": list(node),
                "unit": None,
                "status": None,
                "source": None,
            })
            return
        for i, item in enumerate(node):
            _walk_facts(item, f"{path}[{i}]", out)
        return
    # 裸标量（如 product_id / composition 直接是字符串）
    out.append({
        "fact_id": FACT_ID_PREFIX + path,
        "field_path": path,
        "value": node,
        "unit": None,
        "status": None,
        "source": None,
    })


def materialize_fact_pool(snapshot):
    """把快照 facts 子树压成扁平事实池。

    返回 [{fact_id, field_path, value, unit, status, source}]，顺序 = 深度优先遍历序
    （dict 按插入序，与 JSON 文件书写序一致），保证同一快照两次物化逐字节相同。
    快照没有 facts 键时返回空池——**不报错**：池空与否由输入闸 IG5 判，物化层只如实转录。
    """
    out = []
    facts = snapshot.get("facts")
    if isinstance(facts, dict):
        _walk_facts(facts, "facts", out)
    return out


def list_product_ids(snapshot):
    """收集快照内的企业商品池 product_id 集合（BD_FACT_FABRICATION 的结构判定基准）。

    覆盖两种既有夹具形状：facts.product（单商品，BD-D01）与 facts.product_pool（列表，BD-D02）。
    取不到任何 product_id 时返回空列表，由输入闸 IG5 判红，本函数不报错。
    """
    facts = snapshot.get("facts") or {}
    ids = []
    product = facts.get("product")
    if isinstance(product, dict):
        pid = product.get("product_id")
        if isinstance(pid, dict):
            pid = pid.get("value")
        if pid:
            ids.append(str(pid))
    pool = facts.get("product_pool")
    if isinstance(pool, list):
        for item in pool:
            if not isinstance(item, dict):
                continue
            pid = item.get("product_id")
            if isinstance(pid, dict):
                pid = pid.get("value")
            if pid:
                ids.append(str(pid))
    return ids


# ============================ 规则池 ============================

def rule_pool_from_snapshot(view):
    """从快照视图取本次运行的规则池（诚实边界④：快照 active_rule_refs 钉定规则集，
    kernel/facts 已解引用为完整 A.9.1 RuleRecord dict 清单；本函数只做形状断言与稳定排序）。

    排序按 rule_id，保证池序确定（prompt 渲染逐字节稳定的前提）。透传不编造。
    """
    pool = view.get("hard_rules")
    if pool is None:
        raise ValueError("快照视图缺 hard_rules 键（materialize_legacy_view 契约面），拒绝空手组池")
    for record in pool:
        if not isinstance(record, dict) or not record.get("rule_id"):
            raise ValueError(f"快照视图 hard_rules 含不合形条目：{record!r}（缺 rule_id 或不是映射）")
    return sorted(pool, key=lambda r: r["rule_id"])


def filter_rule_pool_by_brand(pool, brand_id):
    """按品牌过滤规则池（A.1.3 单品牌隔离）。过滤发生在进 prompt 之前——
    过滤晚一步，别的品牌的规则就已经被模型读过了，产物里删干净也没用。"""
    if not brand_id:
        raise ValueError("brand_id 为空，无法过滤规则池（A.1.3 不一致时必须阻断，不能自动补全）")
    return [r for r in pool if r.get("brand_id") == brand_id]


def filter_active_rules(pool):
    """只留 status=ACTIVE 的规则（A.9.2：RULE 必须引用 ACTIVE 版本）。

    这是**单点**过滤：runner 组池时调用一次，prompt 渲染 / 规则评估 / 请求装配 / D6 覆盖
    核验全部消费同一份已过滤池——对抗审查抓获的缺口是「渲染进 prompt 的池未按 status 过滤，
    非 ACTIVE 规则会以『已启用硬规则（ACTIVE）』的名义被模型读到」（runtime_verified），
    各消费点各自过滤必然再漏，收敛到这里。"""
    return [r for r in pool if r.get("status") == "ACTIVE"]


# ============================ 输入闸（生成前） ============================

def _gate(gate_id, item, ok, detail):
    return {"id": gate_id, "item": item, "verdict": "OK" if ok else "FAIL", "detail": detail}


def check_input_gates(plan, snapshot, rule_pool):
    """生成前输入闸 IG1-IG6。返回 [{id, item, verdict, detail}]；任何 FAIL 都意味着
    这份请求**不该进入候选生成**（runner 归到退出码 2：没跑完，不产出半成品 bundle）。

    这些闸消费的是**上游已冻结的判定**（A.5.2 约束 3 的放行信号），不复算上游语义（诚实边界③）。
    """
    gates = []

    next_action = plan.get("next_action")
    gates.append(_gate(
        "IG1", "上游放行信号（A.5.2 约束3：仅 CONTINUE_TO_DECISION 可进 Decision）",
        next_action == NEXT_ACTION_CONTINUE,
        f"next_action={next_action!r}",
    ))

    goal_resolution = plan.get("goal_resolution")
    business_goal = plan.get("business_goal")
    gates.append(_gate(
        "IG2", "目标已解析（goal_resolution=RESOLVED 且 business_goal 非空）",
        goal_resolution == GOAL_RESOLUTION_RESOLVED and bool(business_goal),
        f"goal_resolution={goal_resolution!r} business_goal={business_goal!r}",
    ))

    blocking_not_available = [
        r.get("field_path") for r in (plan.get("required_context") or [])
        if r.get("impact") == IMPACT_BLOCKING and r.get("availability") != AVAILABILITY_AVAILABLE
    ]
    blocking_missing = [
        m.get("field_path") for m in (plan.get("missing_context") or [])
        if m.get("impact") == IMPACT_BLOCKING
    ]
    gates.append(_gate(
        "IG3", "上游 plan 自洽：BLOCKING 需求全 AVAILABLE 且 missing 无 BLOCKING（不复算 OD-03）",
        not blocking_not_available and not blocking_missing,
        f"required 中非 AVAILABLE 的 BLOCKING={blocking_not_available} missing 中 BLOCKING={blocking_missing}",
    ))

    plan_brand = (plan.get("artifact") or {}).get("brand_id")
    snap_brand = snapshot.get("brand_id")
    rule_brands = sorted({r.get("brand_id") for r in rule_pool})
    brand_ok = bool(plan_brand) and plan_brand == snap_brand and all(b == plan_brand for b in rule_brands)
    gates.append(_gate(
        "IG4", "单品牌隔离（A.1.3：plan / snapshot / 规则池 brand_id 全等）",
        brand_ok,
        f"plan={plan_brand!r} snapshot={snap_brand!r} rules={rule_brands}",
    ))

    product_ids = list_product_ids(snapshot)
    gates.append(_gate(
        "IG5", "商品在池（OD-03 §一 #1：至少选定一个商品且在库——此处只判结构性在场）",
        len(product_ids) >= 1,
        f"product_ids={product_ids}",
    ))

    snapshot_ref = (plan.get("artifact") or {}).get("context_snapshot_ref") or {}
    gates.append(_gate(
        "IG6", "快照绑定（plan.artifact.context_snapshot_ref 指向本次输入快照）",
        snapshot_ref.get("object_id") == snapshot.get("snapshot_id"),
        f"plan 引用 {snapshot_ref.get('object_id')!r} vs 快照 {snapshot.get('snapshot_id')!r}",
    ))

    return gates


# ============================ BusinessDecisionRequest 装配 ============================

def build_request(plan, snapshot, rule_pool):
    """按 A.6.1 逐字段装配 BusinessDecisionRequest（字段名照抄，不增不减）。

    仅用于证据回显与下游引用——A.6.1 的三个 ref 都是 VersionedRef（A.2.2：模块之间
    不允许只传可变对象 ID），版本缺省取 1 的口径与 kernel/intent runner 对 M0 扁平夹具的
    处理一致（缺 version 字段时取 1 并在此写明来源，不静默当作"已知版本"）。
    """
    artifact = plan.get("artifact") or {}
    brand_id = artifact.get("brand_id")
    if not brand_id:
        raise ValueError("上游 plan.artifact 缺 brand_id，装配不出合法请求（A.1.3）")
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "intent_plan_ref": {
            "object_type": "IntentExecutionPlan",
            "object_id": artifact.get("artifact_id"),
            "version": int(artifact.get("version", 1)),
            "brand_id": brand_id,
        },
        "context_snapshot_ref": {
            "object_type": "ContextSnapshot",
            "object_id": snapshot.get("snapshot_id"),
            "version": int(snapshot.get("version", 1)),
            "brand_id": brand_id,
        },
        "active_rule_refs": [
            {
                "object_type": "RuleRecord",
                "object_id": r.get("rule_id"),
                "version": int(r.get("version", 1)),
                "brand_id": r.get("brand_id"),
            }
            for r in rule_pool
            if r.get("status") == "ACTIVE"
        ],
    }
