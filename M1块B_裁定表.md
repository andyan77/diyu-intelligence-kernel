# M1-EP01 语义补强（块 B）· 指控裁定表

> 性质：块 B 交付物之一。依据 Founder 派发的三份 M1-EP01 审查报告（审查一判「达标」、审查二判「需返工」、审查三判「需返工」），全部指控逐条编号、逐条复现后裁定。复现基线：main@5de6506，独立 worktree，定向条款重放全部 runtime_verified。修复遵守测试先行铁律（新测试先跑、亲眼看红、再修到绿），范围按派发包 B-2 封顶。

## 一、裁定汇总

| # | 指控（来源） | 复现结果 | 裁定 | 处置 |
|---|---|---|---|---|
| Y-01 | FactValue 状态合同不完整：MISSING/NOT_APPLICABLE/PROVISIONAL 可省略 value 键、CONFIRMED 空串可过、CONFLICTING 顶层可保留已选值（审查二 IS-01 / 审查三 X-02 / 审查一问题1 部分） | 定向重放 5 条全 VALID（假绿） | **属实** | B-2①：约束1 加禁空串、约束3 加 required value（显式 null）、约束4 加顶层 value 必须 null；bad5/8/9 负例钉住，修复后重放全拦 |
| Y-02 | FactValueStringArray 把字段级空数组例外扩大成全局（审查二 IS-02） | `values` CONFIRMED+[] VALID（假绿） | **属实** | B-2①：基础类型 CONFIRMED 禁空数组（bad6 钉住）；新增 FactValueStringArrayEmptyOk 仅供 A 点名三字段（forbidden_expressions / forbidden_styles / expression_boundaries）；白名单正向由 brand_facts.ok2 钉住（CONFIRMED+[] 必须仍绿） |
| Y-03 | MODEL_EXTRACTION→只许 PROVISIONAL 只在注释（审查二 IS-03 / 审查三 X-01） | MODEL_EXTRACTION+CONFIRMED VALID | **属实** | B-2②：谓词 P1 落地第六步；brand_facts.predbad1 钉住（结构合法、谓词必拦） |
| Y-04 | 单品牌隔离未进可执行合同：跨品牌 Snapshot 引用可过（审查二 IS-05） | brand_facts_ref.brand_id=brand-B VALID | **属实** | B-2②：谓词 P2（Snapshot 内全部 brand_id 与顶层全等）；context_snapshot.predbad1 钉住 |
| Y-05 | ContextSnapshot 引用可错族、规则/记忆状态不读、hash 不验（审查二 IS-06） | object_type=ProductFacts VALID | **属实（部分修）** | B-2②：谓词 P3（object_type↔目标族映射表）钉 predbad2；hash 值核验/RuleRecord ACTIVE/BrandMemory APPROVED/版本追加——派发包明示本轮不做，登记挂起（触发点=运行时对象落地） |
| Y-06 | 价格 Money 双层皆可无 as_of（审查二 IS-07） | 双层删除后 VALID | **属实** | B-2①：Money.as_of 必填（内层）。定层依据：A 未指明层级（行 180 与 267 并存），按 Quantity.as_of（行 269-272 非可空）对称口径定内层，两类时效性事实同层同严；product_facts.bad5 钉住 |
| Y-07 | datetime 全线降级为任意 string（审查二 IS-08） | updated_at="不是时间" VALID | **属实** | B-2①：全量 format=date-time + 测试启用 FormatChecker + **fail-closed 自检**（环境缺 rfc3339 库时第六步直接红，不许静默放行）；requirements.txt 增 rfc3339-validator==0.1.4；bad11 钉住 |
| Y-08 | additionalProperties 开放，合同可被静默扩张（审查二 IS-09） | rogue 字段 VALID | **属实** | B-2①：definitions 全量 + 七族顶层 additionalProperties:false（顶层枚举全部合法键；`_fixture_note`/`_note` 显式允许并注明 OQ-BUILD-11 剥离口径）；bad10 钉住。信封不关（allOf 平铺会误拒族字段），由族顶层承担并留注 |
| Y-09 | 47 项基线未钉死，删样例仍绿（审查二 NS-01 / 审查三非语义1） | 审查实测删 bad3 后 46/46 GREEN | **属实** | B-2③：三级计数钉死（族集合/每族 ok·bad·predbad/断言总数 72）；活体复测：删 visual_profile.bad3 → 计数红+总数红 |
| Y-10 | 负例只匹配消息子串，不绑 validator/路径（审查二 NS-02 / 审查三非语义2） | 静态确认（L118 子串判定） | **属实（增量修）** | B-2③：新负例协议三元组（substr+validator+path 同条错误绑定）；本轮 13 个新负例全带三元组；存量 26 个保持子串（计数钉死防退化），按派发包「新负例绑定」口径不回改存量 |
| Y-11 | 正例覆盖不足以证明合法状态空间（审查二 NS-03） | 每族仅 1 正例属实 | **属实（按范围修）** | B-2③：公共类型状态矩阵做一次不按族展开——brand_facts.ok2（五状态+白名单空数组）+ product_facts.ok2（Money/Quantity/Range × PROVISIONAL/MISSING/NOT_APPLICABLE）；全组合矩阵为派发包写死不做项 |
| Y-12 | 品牌 ID 四种写法并存；规则引用与规则文件品牌不一致；快照引用不能解引用（审查一问题3 / 审查三 X-03） | grep 确认四写法 | **属实** | B-2④：七份正例统一 `fixture-brand-01`（与 contracts/rules/ 及 BD 夹具同域，悬空规则引用随之闭合） |
| Y-13 | 正例三处失真：虚构库存包装成不存在的 SYSTEM_RECORD；snapshot_hash 四种算法均不匹配；VideoAccount 声称与 R01 冲突却引 R02 且指向不存在的 R01 v2（审查三 X-04） | 逐处核实（数据包 L397/L408/L419 对照） | **属实** | B-2④：库存来源改 BRAND_OPERATOR_INPUT+夹具虚构-剧本标注（三分法）；snapshot_hash 按 canonical 算法实算回填并注明口径；alternative 2 改抄 R01 L397 原文、primary_persona_ref 改指实存的 FS-PERSONA-R01-0001 v1 |
| Y-14 | 考卷夹具对齐「方向已定」只存在于文件头注，台账无挂起项（审查一问题2 / 审查二 NS-04） | grep 全仓 1 处命中属实 | **属实** | 台账挂起表补行（触发点=下次动 acceptance/ 考卷时，须 Founder 批准） |
| Y-15 | 接口形状偏宽：空串 ID / Range min>max / version 0 或负 / nullable≠optional 无统一原则（审查二 IS-10 / 审查三 X-05 部分） | 属实 | **属实（不修）** | A 未规定处不自行加严（三条铁律「不猜」）；不在派发包七条收紧内；登记于测试文件头诚实边界，运行时谓词批次一并议 |
| Y-16 | 51 个 required 约束仅 8 个受删除变异保护（审查三非语义3） | 套件自述属实 | **属实（部分缓解）** | 三级计数钉死拦「删样例缩覆盖」；全量 required 变异为派发包块 A 写死不做项的同类（成本/收益），登记不展开 |
| Y-17 | $ref 断裂只抛 traceback、红路径文案错误（审查三非语义4） | 静态确认 | **属实** | B-2③顺手修：校验器异常一律入标准 FACT_SCHEMAS_RED 收尾 |
| Y-18 | PR 无 GitHub 原生 review 记录（审查二 NS-05） | 属实 | **属实（不做）** | 派发包写死不做（GitHub 原生 review 补录）；复审由独立窗口承担（派发包回执与复审节） |
| Y-19 | PyYAML 5.4.1 ≠ 钉版 6.0.2 环境提示（审查一问题4） | 本机同现象 | **属实（无动作）** | check_m0 自打 ⚠ 设计内；钉版环境证据由服务端 CI 承担 |

## 二、修复前后对照（全部 runtime_verified）

| 假绿路径（修复前 VALID） | 修复后 |
|---|---|
| MISSING 省略 value 键 | ✗ required @ $.field |
| CONFIRMED value="" | ✗ not @ $.field.value |
| CONFIRMED 普通数组=[] | ✗ minItems @ $.field.value |
| PROVISIONAL 缺 uncertainty_reason | ✗ required |
| CONFLICTING 顶层保值 | ✗ type(null) @ $.field.value |
| Money 双层无 as_of | ✗ anyOf→required as_of |
| updated_at 非法日期 | ✗ format |
| rogue 合同外字段 | ✗ additionalProperties |
| MODEL_EXTRACTION+CONFIRMED | ✗ 谓词 P1 |
| 跨品牌 Snapshot 引用 | ✗ 谓词 P2 |
| 引用错族 object_type | ✗ 谓词 P3 |
| 白名单 forbidden_expressions CONFIRMED+[] | ✓ 仍合法（例外保留在字段级） |
| 删一个样例 | ✗ 计数钉死红（审查三实测路径已拦） |

第六步 47 → **72** 项；样例 33 → **46** 份（ok 9 / bad 34 / predbad 3）；schema_version 升 v2 系列（A-3.x-v2，破坏性变更）。
