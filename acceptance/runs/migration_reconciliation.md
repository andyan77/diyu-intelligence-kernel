# 块 E ① 迁移值级对账表（机器生成 —— `python3 tools/migrate_snapshots.py verify --old-ref HEAD`）

- 旧树基线：`HEAD`；新树：工作区当前内容
- 生成面↔磁盘全等：PASS（77 文件）
- 账本条目：991；恒等/搬运回读相等：991；不等：0
- 等值判据：identity/搬运类逐字节比对；形状适配类（wrap-array/money/quantity/range/sourceref 派生）由 transform 语义承担、原文留注解，逐行标注类型如下。

| case | 旧路径 | 旧值 | 新落点 | transform | 回读相等 |
|---|---|---|---|---|---|
| BD-D01 | snapshot_id | "SNAP-BDD01-0001" | cases/BD-D01/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| BD-D01 | brand_id | "fixture-brand-01" | cases/BD-D01/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| BD-D01 | facts.business_goal | {"value": "INVENTORY_ACTIVATION", "source": "BD-D01 冻结事实"} | cases/BD-D01/fixtures/task_input.json:_migrated_from_snapshot.BD-D01.business_goal | relocate-task-input | ✓ |
| BD-D01 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:product_id | identity-plain | ✓ |
| BD-D01 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:name.value | identity | ✓ |
| BD-D01 | facts.product.name.source | "文件级溯源（原快照 _fixture_note 逐字）：BD-D01 冻结事实照抄 B.4.2/BD-D01 +… | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | facts.product.price.original_as_of | "2026-08-17" | cases/BD-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| BD-D01 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| BD-D01 | facts.product.price.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | facts.product.composition.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）"] | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:material.value | wrap-array | ✓ |
| BD-D01 | facts.product.composition.source | "文件级溯源（原快照 _fixture_note 逐字）：BD-D01 冻结事实照抄 B.4.2/BD-D01 +… | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | facts.product.sizes.value | ["XS", "S", "M", "L", "XL"] | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:size_range.value | identity | ✓ |
| BD-D01 | facts.product.sizes.source | "文件级溯源（原快照 _fixture_note 逐字）：BD-D01 冻结事实照抄 B.4.2/BD-D01 +… | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| BD-D01 | facts.product.lifecycle_stage.source | "文件级溯源（原快照 _fixture_note 逐字）：BD-D01 冻结事实照抄 B.4.2/BD-D01 +… | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | facts.product.<absent:category> | null | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:category | required-fill-missing | ✓ |
| BD-D01 | facts.brand_positioning.value | "HIGH_END" | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:positioning.value | identity | ✓ |
| BD-D01 | facts.brand_positioning.source | "BD-D01 冻结事实" | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | facts.brand_positioning.<absent:brand_name> | null | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:brand_name | required-fill-missing | ✓ |
| BD-D01 | facts.brand_positioning.<absent:values> | null | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:values | required-fill-missing | ✓ |
| BD-D01 | facts.brand_positioning.<absent:tone> | null | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:tone | required-fill-missing | ✓ |
| BD-D01 | facts.brand_positioning.<absent:target_customer_summary> | null | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:target_customer_summary | required-fill-missing | ✓ |
| BD-D01 | facts.brand_positioning.<absent:forbidden_expressions> | null | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:forbidden_expressions | required-fill-missing | ✓ |
| BD-D01 | facts.brand_positioning.<absent:commercial_constraints> | null | fixtures/facts/brand/FS-BRAND-BDD01-0001.v1.json:commercial_constraints | required-fill-missing | ✓ |
| BD-D01 | facts.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| BD-D01 | facts.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| BD-D01 | facts.inventory.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-BDD01-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D01 | hard_rules[0].rule_id | "R-BDD01-001" | cases/BD-D01/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| BD-D01 | hard_rules[0] | {"statement": "禁止低价叫卖表达（forbidden_expression: LOW_PRICE_S… | cases/BD-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| BD-D01 | hard_rules[1].rule_id | "R-BDD01-002" | cases/BD-D01/fixtures/context_snapshot.json:active_rule_refs[1].object_id | rule-ref:registered@contracts/rules | ✓ |
| BD-D01 | hard_rules[1] | {"statement": "促销让利路径违反高端品牌禁令（两候选降级分支冻结规则）", "status": "A… | cases/BD-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[1].. | relocate-annotation | ✓ |
| BD-D02 | snapshot_id | "SNAP-BDD02-0001" | cases/BD-D02/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| BD-D02 | brand_id | "fixture-brand-01" | cases/BD-D02/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| BD-D02 | facts.product_pool_size | {"value": 3, "unit": "个商品", "source": "B.4.2/BD-D02「冻结事实」… | cases/BD-D02/fixtures/task_input.json:_migrated_from_snapshot.BD-D02.product_pool_size | relocate-task-input | ✓ |
| BD-D02 | facts.product_pool[0].product_id | "P01" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:product_id | identity-plain | ✓ |
| BD-D02 | facts.product_pool[0].name.value | "人字纹亮丝麻西装" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:name.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].category.value | "西装" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:category.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].category.source | "截图 IMG_0567" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].sku.value | "1H7911911Q" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:sku.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].sku.source | "截图 IMG_0567" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].price.fixture_field | "吊牌价" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[0].price.fixture_field | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[0].price.raw_text | "980元" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[0].price.raw_text | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[0].price.original_as_of | "2026-08-17" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[0].price.original_as_of | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[0].price.value | {"amount": 980, "currency": "CNY", "as_of": "2026-08-17T0… | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| BD-D02 | facts.product_pool[0].price.source | "截图 IMG_0567" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].composition.value | ["79%莱赛尔 15.7%亚麻 5.3%聚酯纤维(含聚酯薄膜纤维) (含微量其他纤维)"] | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:material.value | wrap-array | ✓ |
| BD-D02 | facts.product_pool[0].composition.source | "截图 IMG_0567" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].lining | {"value": "100%聚酯纤维", "source": "截图 IMG_0567"} | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[0].lining.. | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[0].style_attributes.value | ["H型正肩西装", "一粒同色扣", "无袋盖隐形口袋", "袖口排扣"] | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:style_attributes.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].style_attributes.source | "截图 IMG_0573 / 截图 IMG_0575" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].selling_points.note | "数据包字段名为『已确认卖点』，只收录已确认项" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[0].selling_points.note | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[0].selling_points.value | ["“H型正肩西装+人字纹亮丝阔腿裤”", "“一粒同色扣 + 无袋盖隐形口袋”"] | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:selling_points.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].selling_points.source | "截图 IMG_0573 / 截图 IMG_0575" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].sizes.value | ["S", "M", "L", "XL"] | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:size_range.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].sizes.source | "截图 IMG_0567" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].lifecycle_stage.value | "当季在售" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:lifecycle_stage.value | identity | ✓ |
| BD-D02 | facts.product_pool[0].lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[0].inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| BD-D02 | facts.product_pool[0].inventory.value | {"value": 126, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| BD-D02 | facts.product_pool[0].inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P01.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].product_id | "P02" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:product_id | identity-plain | ✓ |
| BD-D02 | facts.product_pool[1].name.value | "人字纹亮丝麻西装裤" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:name.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].category.value | "西装裤" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:category.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].category.source | "截图 IMG_0568" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].sku.value | "1H7953411Q" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:sku.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].sku.source | "截图 IMG_0568" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].price.fixture_field | "吊牌价" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[1].price.fixture_field | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[1].price.raw_text | "798元" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[1].price.raw_text | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[1].price.original_as_of | "2026-08-17" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[1].price.original_as_of | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[1].price.value | {"amount": 798, "currency": "CNY", "as_of": "2026-08-17T0… | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| BD-D02 | facts.product_pool[1].price.source | "截图 IMG_0568" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].composition.value | ["79%莱赛尔 15.7%亚麻 5.3%聚酯纤维(含聚酯薄膜纤维) (含微量其他纤维)"] | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:material.value | wrap-array | ✓ |
| BD-D02 | facts.product_pool[1].composition.source | "截图 IMG_0568" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].lining | {"value": "100%聚酯纤维", "source": "截图 IMG_0568"} | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[1].lining.. | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[1].style_attributes.value | ["人字纹亮丝阔腿裤", "双褶设计", "宽大裤腿"] | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:style_attributes.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].style_attributes.source | "截图 IMG_0573 / 截图 IMG_0577" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].selling_points.note | "数据包字段名为『已确认卖点』，只收录已确认项" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[1].selling_points.note | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[1].selling_points.value | ["“腹部两侧各两道收褶，预留充足立体空间，包容性强，适合久坐人群”", "“纵向褶线视觉拉长腿部”"] | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:selling_points.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].selling_points.source | "截图 IMG_0577" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].sizes.value | ["S", "M", "L", "XL"] | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:size_range.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].sizes.source | "截图 IMG_0568" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].lifecycle_stage.value | "当季在售" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:lifecycle_stage.value | identity | ✓ |
| BD-D02 | facts.product_pool[1].lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[1].inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| BD-D02 | facts.product_pool[1].inventory.value | {"value": 188, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| BD-D02 | facts.product_pool[1].inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P02.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].product_id | "P03" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:product_id | identity-plain | ✓ |
| BD-D02 | facts.product_pool[2].name.value | "亮丝麻针织马甲" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:name.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].category.value | "针织马甲" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:category.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].category.source | "截图 IMG_0569" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].sku.value | "1H7934051Q" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:sku.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].sku.source | "截图 IMG_0569" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].price.fixture_field | "吊牌价" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[2].price.fixture_field | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[2].price.raw_text | "598元" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[2].price.raw_text | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[2].price.original_as_of | "2026-08-17" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[2].price.original_as_of | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[2].price.value | {"amount": 598, "currency": "CNY", "as_of": "2026-08-17T0… | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| BD-D02 | facts.product_pool[2].price.source | "截图 IMG_0569" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].composition.value | ["53.9%莱赛尔 19.7%聚酯纤维 10.1%醋纤 8.9%亚麻 4.9%锦纶 2.5%聚酯薄膜纤维（装饰及… | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:material.value | wrap-array | ✓ |
| BD-D02 | facts.product_pool[2].composition.source | "截图 IMG_0569" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].lining | {"value": null, "status": "缺失", "source": "截图 IMG_0569", … | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[2].lining.. | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[2].style_attributes.value | ["V领", "无袖", "前开扣", "短款针织马甲"] | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:style_attributes.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].style_attributes.source | "截图 IMG_0580 / 截图 IMG_0596" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].selling_points.note | "数据包字段名为『已确认卖点』，只收录已确认项" | cases/BD-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product_pool[2].selling_points.note | relocate-annotation | ✓ |
| BD-D02 | facts.product_pool[2].selling_points.value | ["单品图确认 V 领、无袖、前开扣；可与同页西装和西装裤组合"] | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:selling_points.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].selling_points.source | "截图 IMG_0580 / 截图 IMG_0596" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].sizes.value | ["S", "M", "L", "XL"] | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:size_range.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].sizes.source | "截图 IMG_0569" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].lifecycle_stage.value | "当季在售" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:lifecycle_stage.value | identity | ✓ |
| BD-D02 | facts.product_pool[2].lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D02 | facts.product_pool[2].inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| BD-D02 | facts.product_pool[2].inventory.value | {"value": 94, "unit": "件", "as_of": "2026-08-17T00:00:00+… | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| BD-D02 | facts.product_pool[2].inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD02-P03.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | snapshot_id | "SNAP-BDD03-0001" | cases/BD-D03/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| BD-D03 | brand_id | "fixture-brand-01" | cases/BD-D03/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| BD-D03 | facts.scene | {"value": "真实上班、通勤和周末场景", "source": "模拟", "note": "【模拟】字段… | cases/BD-D03/fixtures/task_input.json:_migrated_from_snapshot.BD-D03.scene | relocate-task-input | ✓ |
| BD-D03 | facts.business_goal | {"value": "PRODUCT_LAUNCH", "source": "执行侧推断（依据数据包·包2 P11… | cases/BD-D03/fixtures/task_input.json:_migrated_from_snapshot.BD-D03.business_goal | relocate-task-input | ✓ |
| BD-D03 | facts.audience.audience_id | "A02" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:audience_id | identity-plain | ✓ |
| BD-D03 | facts.audience.label.note | "数据包·包3 字段名『称呼』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.label.note | relocate-annotation | ✓ |
| BD-D03 | facts.audience.label.value | "克制表达者" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:label.value | identity | ✓ |
| BD-D03 | facts.audience.label.source | "模拟" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:label.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.audience.age_range.original_range_text | "26—32 岁" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.age_range.original_range_text | relocate-annotation | ✓ |
| BD-D03 | facts.audience.age_range.value | {"min": 26, "max": 32, "unit": "岁"} | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:age_range.value | range-parse | ✓ |
| BD-D03 | facts.audience.age_range.source | "模拟" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:age_range.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.audience.occupation_and_lifestyle.value | ["新消费、电商、设计、内容、互联网运营或自由职业；工作环境着装弹性大，会拍短视频和日常照片，但不希望整个人像在追… | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:occupation_or_lifestyle.value | wrap-array | ✓ |
| BD-D03 | facts.audience.occupation_and_lifestyle.source | "模拟" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:occupation_or_lifestyle.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.audience.pain_points.note | "数据包·包3 A02 字段名『真实痛点』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.pain_points.note | relocate-annotation | ✓ |
| BD-D03 | facts.audience.pain_points.value | ["衣柜以黑、白、灰、牛仔为主，想加入荧光色或印花，却担心只能拍一次照片、无法进入日常", "对“显瘦模板”疲劳，… | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:pain_points.value | identity | ✓ |
| BD-D03 | facts.audience.pain_points.source | "模拟" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:pain_points.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.audience.purchase_reasons.note | "数据包·包3 A02 字段名『购买理由』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.purchase_reasons.note | relocate-annotation | ✓ |
| BD-D03 | facts.audience.purchase_reasons.value | ["品牌把反常识单品放进真实上班、通勤和周末场景验证", "买手能给出“这一件负责表达，其余单品负责安定”的具体搭… | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:purchase_reasons.value | identity | ✓ |
| BD-D03 | facts.audience.purchase_reasons.source | "模拟" | fixtures/facts/audience/FS-AUD-BDD03-A02.v1.json:purchase_reasons.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.audience.common_concerns | {"value": ["荧光色、腰果花等强视觉元素会不会很快厌倦", "修身针织或高腰裤在活动、进食和久坐时是否仍… | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.common_concerns.. | relocate-annotation | ✓ |
| BD-D03 | facts.brand.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:brand_name.value | identity | ✓ |
| BD-D03 | facts.brand.brand_name.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.brand.positioning.note | "数据包·包1 字段名『一句话定位』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.positioning.note | relocate-annotation | ✓ |
| BD-D03 | facts.brand.positioning.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:positioning.value | identity | ✓ |
| BD-D03 | facts.brand.positioning.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.brand.values.note | "数据包·包1 字段名『价值主张』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.values.note | relocate-annotation | ✓ |
| BD-D03 | facts.brand.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:values.value | identity | ✓ |
| BD-D03 | facts.brand.values.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.brand.tone.note | "数据包·包1 字段名『说话调性』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.tone.note | relocate-annotation | ✓ |
| BD-D03 | facts.brand.tone.value | ["稳、具体、有判断、留余地；像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:tone.value | wrap-array | ✓ |
| BD-D03 | facts.brand.tone.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.brand.target_customer_summary.note | "数据包·包1 字段名『目标客户一句话』；受众权威对象见 facts.audience" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.target_customer_summary.note | relocate-annotation | ✓ |
| BD-D03 | facts.brand.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:target_customer_summary.value | identity | ✓ |
| BD-D03 | facts.brand.target_customer_summary.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.brand.forbidden_expressions.note | "数据包·包1 字段名『禁用表达清单』照抄；运营判定真源以 acceptance/detectors/forbid… | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.forbidden_expressions.note | relocate-annotation | ✓ |
| BD-D03 | facts.brand.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| BD-D03 | facts.brand.forbidden_expressions.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.brand.commercial_constraints.note | "数据包·包1 字段名『商业硬约束』" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.commercial_constraints.note | relocate-annotation | ✓ |
| BD-D03 | facts.brand.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:commercial_constraints.value | identity | ✓ |
| BD-D03 | facts.brand.commercial_constraints.source | "模拟" | fixtures/facts/brand/FS-BRAND-BDD03-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.product_id | "P11" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:product_id | identity-plain | ✓ |
| BD-D03 | facts.product.name.value | "荧光绿高腰阔腿裤" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:name.value | identity | ✓ |
| BD-D03 | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.category.value | "裤子" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:category.value | identity | ✓ |
| BD-D03 | facts.product.category.source | "截图 IMG_0671" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.sku.value | "02I2K253-A06-G02" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:sku.value | identity | ✓ |
| BD-D03 | facts.product.sku.source | "截图 IMG_0667 / 截图 IMG_0671" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.price.fixture_field | "零售价" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.fixture_field | relocate-annotation | ✓ |
| BD-D03 | facts.product.price.raw_text | "零售价：2280元" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| BD-D03 | facts.product.price.note | "截图原文为『零售价：2280元』，截图未出现『吊牌价』字样——原文口径按数据包·包2 P11 保留，不得改写为吊… | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.note | relocate-annotation | ✓ |
| BD-D03 | facts.product.price.original_as_of | "2026-08-17" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| BD-D03 | facts.product.price.value | {"amount": 2280, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| BD-D03 | facts.product.price.source | "截图 IMG_0671" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.composition.note | "两张截图的成分行写法不同，按数据包原文各自保留，不合并、不改写" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.composition.note | relocate-annotation | ✓ |
| BD-D03 | facts.product.composition.value | ["面料1：棉100%", "面料：棉 100%"] | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:material.value | identity | ✓ |
| BD-D03 | facts.product.composition.source | "截图 IMG_0667（面料1：棉100%）/ 截图 IMG_0671（面料：棉 100%）" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.lining | {"value": null, "status": "缺失", "source": "截图 IMG_0667 / … | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| BD-D03 | facts.product.style_attributes.value | ["荧光绿", "高腰", "阔腿", "附腰带", "商品指数标注版型“合身”、弹力“无弹”、厚度“适中”"] | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:style_attributes.value | identity | ✓ |
| BD-D03 | facts.product.style_attributes.source | "截图 IMG_0664 / 截图 IMG_0667" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.selling_points.note | "数据包字段名为『已确认卖点』，只收录已确认项" | cases/BD-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.selling_points.note | relocate-annotation | ✓ |
| BD-D03 | facts.product.selling_points.value | ["颜色“荧光绿”", "面料“棉100%”", "高腰腰带结构与阔腿裤型"] | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:selling_points.value | identity | ✓ |
| BD-D03 | facts.product.selling_points.source | "截图 IMG_0667 / 截图 IMG_0669 / 截图 IMG_0671" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.sizes.value | ["34", "36", "38", "40"] | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:size_range.value | identity | ✓ |
| BD-D03 | facts.product.sizes.source | "截图 IMG_0670" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.lifecycle_stage.value | "正常在售新品" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:lifecycle_stage.value | identity | ✓ |
| BD-D03 | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| BD-D03 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| BD-D03 | facts.product.inventory.value | {"value": 180, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| BD-D03 | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-BDD03-P11.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | snapshot_id | "SNAP-CRD01-0001" | cases/CR-D01/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| CR-D01 | brand_id | "fixture-brand-01" | cases/CR-D01/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| CR-D01 | facts.business_goal | {"value": "INVENTORY_ACTIVATION", "source": "Founder 2026… | cases/CR-D01/fixtures/task_input.json:_migrated_from_snapshot.CR-D01.business_goal | relocate-task-input | ✓ |
| CR-D01 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:product_id | identity-plain | ✓ |
| CR-D01 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:name.value | identity | ✓ |
| CR-D01 | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:category.value | identity | ✓ |
| CR-D01 | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:sku.value | identity | ✓ |
| CR-D01 | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.price.raw_text | "3980元" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| CR-D01 | facts.product.price.original_as_of | "2026-08-17" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| CR-D01 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| CR-D01 | facts.product.price.source | "截图 IMG_0684（数据包字段名「吊牌价」，截图原文「3980元」）" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:material.value | identity | ✓ |
| CR-D01 | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| CR-D01 | facts.product.style_attributes.value | ["大翻领", "廓形肩线", "H型风衣式", "袖口可调节袖袢", "宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:style_attributes.value | identity | ✓ |
| CR-D01 | facts.product.style_attributes.source | "截图 IMG_0674 / 截图 IMG_0677 / 截图 IMG_0680（IMG_0674 的归属不一致见… | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式", "提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:selling_points.value | identity | ✓ |
| CR-D01 | facts.product.selling_points.source | "截图 IMG_0677 / 截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:size_range.value | identity | ✓ |
| CR-D01 | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| CR-D01 | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| CR-D01 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| CR-D01 | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.product.image_refs.image_asset_status | "PENDING_IMAGE_ASSET_M3" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_status | relocate-annotation | ✓ |
| CR-D01 | facts.product.image_refs.image_asset_note | "真实图片文件不在本仓库（全仓无 IMG_*.jpg/png 资产，2026-08-17 实测）；本字段只是编号引… | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_note | relocate-annotation | ✓ |
| CR-D01 | facts.product.image_refs.source | "截图 IMG_0672 / 截图 IMG_0684（数据包 P13「关联图片编号」原文：IMG_0672、IMG… | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| CR-D01 | facts.product.image_refs.value[0] | "IMG_0672" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[0].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[1] | "IMG_0675" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[1].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[2] | "IMG_0676" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[2].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[3] | "IMG_0677" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[3].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[4] | "IMG_0678" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[4].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[5] | "IMG_0679" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[5].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[6] | "IMG_0680" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[6].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[7] | "IMG_0681" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[7].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[8] | "IMG_0682" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[8].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[9] | "IMG_0683" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[9].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.product.image_refs.value[10] | "IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD01-P13.v1.json:image_refs[10].locator | imageid-to-sourceref | ✓ |
| CR-D01 | facts.video_account.account_id.source | "Founder 2026-08-17 IA-0 裁决：虚构编号（OQ-BUILD-13）" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.account_id.source | relocate-annotation | ✓ |
| CR-D01 | facts.video_account.account_id.value | "ACC-HXJ-001" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:account_id | identity-plain | ✓ |
| CR-D01 | facts.video_account.platform.source | "A.3.6 系统固定 + OD-03 通用阻断项④（本期仅视频号）" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.platform.source | relocate-annotation | ✓ |
| CR-D01 | facts.video_account.platform.value | "WECHAT_VIDEO" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:platform | identity-plain | ✓ |
| CR-D01 | facts.video_account.account_name.value | "衡叙集·穿衣判断（虚构）" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:account_name.value | identity | ✓ |
| CR-D01 | facts.video_account.account_name.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:account_name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.video_account.positioning.value | "面向城市女性的服装选择与真实穿着决策账号：以商品事实、场景试穿和明确取舍，回答“为什么选、怎么穿、何时不选”" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:positioning.value | identity | ✓ |
| CR-D01 | facts.video_account.positioning.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.video_account.content_style.value | ["稳口吻、熟关系、低剪辑刺激", "以一件商品或一个穿衣问题为单集单位，画面保留面料近景、正侧背面、动作和必要的… | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:content_style.value | identity | ✓ |
| CR-D01 | facts.video_account.content_style.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:content_style.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.video_account.audience_relationship.value | "不是销售话术广播站，而是长期衣橱判断伙伴；欢迎观众提交通勤、久坐、身形变化、颜色尝试和门店试穿问题，并允许后续视… | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:audience_relationship.value | identity | ✓ |
| CR-D01 | facts.video_account.audience_relationship.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | facts.video_account.primary_persona_ref.source | "模拟（版本化引用待 PersonaFacts 对象落盘后回填，本文件不自造 version）" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.primary_persona_ref.source | relocate-annotation | ✓ |
| CR-D01 | facts.video_account.primary_persona_ref.unresolved_primary_persona_ref | "沈岚，关联 R01 品牌主理人" | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.primary_persona_ref.unresolved_primary_persona_ref | relocate-annotation | ✓ |
| CR-D01 | facts.video_account.expression_boundaries.value | ["未核对款号、成分、尺码、价格和库存时不得下商品结论", "价格冲突必须同时展示并标记“待裁决”，不得选择性隐藏… | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:expression_boundaries.value | identity | ✓ |
| CR-D01 | facts.video_account.expression_boundaries.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD01-0001.v1.json:expression_boundaries.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D01 | hard_rules[0].rule_id | "R-FB01-001" | cases/CR-D01/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| CR-D01 | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/CR-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| CR-D02 | snapshot_id | "SNAP-CRD02-0001" | cases/CR-D02/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| CR-D02 | brand_id | "fixture-brand-01" | cases/CR-D02/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| CR-D02 | facts.business_goal | {"value": "INVENTORY_ACTIVATION", "source": "Founder 2026… | cases/CR-D02/fixtures/task_input.json:_migrated_from_snapshot.CR-D02.business_goal | relocate-task-input | ✓ |
| CR-D02 | facts.brand.brand_id | "fixture-brand-01" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:brand_id | identity-plain | ✓ |
| CR-D02 | facts.brand.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:brand_name.value | identity | ✓ |
| CR-D02 | facts.brand.brand_name.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.positioning.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:positioning.value | identity | ✓ |
| CR-D02 | facts.brand.positioning.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:values.value | identity | ✓ |
| CR-D02 | facts.brand.values.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.tone.value | ["稳、具体、有判断、留余地", "像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:tone.value | identity | ✓ |
| CR-D02 | facts.brand.tone.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:target_customer_summary.value | identity | ✓ |
| CR-D02 | facts.brand.target_customer_summary.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| CR-D02 | facts.brand.forbidden_expressions.source | "模拟（数据包·包1「禁用表达清单」；与 detectors 词表的差异见 _fixture_note）" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:commercial_constraints.value | identity | ✓ |
| CR-D02 | facts.brand.commercial_constraints.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.brand.audience_refs.status | "NOT_INCLUDED" | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.audience_refs.status | relocate-annotation | ✓ |
| CR-D02 | facts.brand.audience_refs.source | "本任务未把数据包·包3 受众事实纳入 CR-D02 快照；不自造引用" | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.audience_refs.source | relocate-annotation | ✓ |
| CR-D02 | facts.brand.audience_refs.value | [] | fixtures/facts/brand/FS-BRAND-CRD02-0001.v1.json:audience_refs | identity-plain | ✓ |
| CR-D02 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:product_id | identity-plain | ✓ |
| CR-D02 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:name.value | identity | ✓ |
| CR-D02 | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:category.value | identity | ✓ |
| CR-D02 | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:sku.value | identity | ✓ |
| CR-D02 | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.price.raw_text | "3980元" | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| CR-D02 | facts.product.price.original_as_of | "2026-08-17" | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| CR-D02 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| CR-D02 | facts.product.price.source | "截图 IMG_0684（数据包字段名「吊牌价」，截图原文「3980元」）" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:material.value | identity | ✓ |
| CR-D02 | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| CR-D02 | facts.product.style_attributes.value | ["大翻领", "廓形肩线", "H型风衣式", "袖口可调节袖袢", "宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:style_attributes.value | identity | ✓ |
| CR-D02 | facts.product.style_attributes.source | "截图 IMG_0674 / 截图 IMG_0677 / 截图 IMG_0680（IMG_0674 的归属不一致见… | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式", "提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:selling_points.value | identity | ✓ |
| CR-D02 | facts.product.selling_points.source | "截图 IMG_0677 / 截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:size_range.value | identity | ✓ |
| CR-D02 | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| CR-D02 | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| CR-D02 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| CR-D02 | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D02 | facts.product.image_refs.image_asset_status | "PENDING_IMAGE_ASSET_M3" | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_status | relocate-annotation | ✓ |
| CR-D02 | facts.product.image_refs.image_asset_note | "真实图片文件不在本仓库（全仓无 IMG_*.jpg/png 资产，2026-08-17 实测）；本字段只是编号引… | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_note | relocate-annotation | ✓ |
| CR-D02 | facts.product.image_refs.source | "截图 IMG_0672 / 截图 IMG_0684（数据包 P13「关联图片编号」原文：IMG_0672、IMG… | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| CR-D02 | facts.product.image_refs.value[0] | "IMG_0672" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[0].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[1] | "IMG_0675" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[1].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[2] | "IMG_0676" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[2].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[3] | "IMG_0677" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[3].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[4] | "IMG_0678" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[4].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[5] | "IMG_0679" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[5].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[6] | "IMG_0680" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[6].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[7] | "IMG_0681" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[7].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[8] | "IMG_0682" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[8].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[9] | "IMG_0683" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[9].locator | imageid-to-sourceref | ✓ |
| CR-D02 | facts.product.image_refs.value[10] | "IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD02-P13.v1.json:image_refs[10].locator | imageid-to-sourceref | ✓ |
| CR-D02 | hard_rules[0].rule_id | "R-FB01-001" | cases/CR-D02/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| CR-D02 | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/CR-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| CR-D03 | snapshot_id | "SNAP-CRD03-0001" | cases/CR-D03/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| CR-D03 | brand_id | "fixture-brand-01" | cases/CR-D03/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| CR-D03 | facts.business_goal | {"value": "INVENTORY_ACTIVATION", "source": "Founder 2026… | cases/CR-D03/fixtures/task_input.json:_migrated_from_snapshot.CR-D03.business_goal | relocate-task-input | ✓ |
| CR-D03 | facts.decision_selection | {"value": "复用 CR-D02 冻结选择：C1（ART-BDD01-OUT-GOOD 候选一）", "s… | cases/CR-D03/fixtures/task_input.json:_migrated_from_snapshot.CR-D03.decision_selection | relocate-task-input | ✓ |
| CR-D03 | facts.persona_selection | {"value": "R01 沈岚", "source": "执行侧构造（数据包·包5 主出镜人=沈岚）", "i… | cases/CR-D03/fixtures/task_input.json:_migrated_from_snapshot.CR-D03.persona_selection | relocate-task-input | ✓ |
| CR-D03 | facts.brand.brand_id | "fixture-brand-01" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:brand_id | identity-plain | ✓ |
| CR-D03 | facts.brand.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:brand_name.value | identity | ✓ |
| CR-D03 | facts.brand.brand_name.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.positioning.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:positioning.value | identity | ✓ |
| CR-D03 | facts.brand.positioning.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:values.value | identity | ✓ |
| CR-D03 | facts.brand.values.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.tone.value | ["稳、具体、有判断、留余地", "像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:tone.value | identity | ✓ |
| CR-D03 | facts.brand.tone.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:target_customer_summary.value | identity | ✓ |
| CR-D03 | facts.brand.target_customer_summary.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| CR-D03 | facts.brand.forbidden_expressions.source | "模拟（数据包·包1「禁用表达清单」；与 detectors 词表的差异见 _fixture_note）" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:commercial_constraints.value | identity | ✓ |
| CR-D03 | facts.brand.commercial_constraints.source | "模拟" | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.brand.audience_refs.status | "NOT_INCLUDED" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.audience_refs.status | relocate-annotation | ✓ |
| CR-D03 | facts.brand.audience_refs.source | "本任务未把数据包·包3 受众事实纳入 CR-D03 快照；不自造引用" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.audience_refs.source | relocate-annotation | ✓ |
| CR-D03 | facts.brand.audience_refs.value | [] | fixtures/facts/brand/FS-BRAND-CRD03-0001.v1.json:audience_refs | identity-plain | ✓ |
| CR-D03 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:product_id | identity-plain | ✓ |
| CR-D03 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:name.value | identity | ✓ |
| CR-D03 | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:category.value | identity | ✓ |
| CR-D03 | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:sku.value | identity | ✓ |
| CR-D03 | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.price.raw_text | "3980元" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| CR-D03 | facts.product.price.original_as_of | "2026-08-17" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| CR-D03 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| CR-D03 | facts.product.price.source | "截图 IMG_0684（数据包字段名「吊牌价」，截图原文「3980元」）" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:material.value | identity | ✓ |
| CR-D03 | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| CR-D03 | facts.product.style_attributes.value | ["大翻领", "廓形肩线", "H型风衣式", "袖口可调节袖袢", "宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:style_attributes.value | identity | ✓ |
| CR-D03 | facts.product.style_attributes.source | "截图 IMG_0674 / 截图 IMG_0677 / 截图 IMG_0680（IMG_0674 的归属不一致见… | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式", "提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:selling_points.value | identity | ✓ |
| CR-D03 | facts.product.selling_points.source | "截图 IMG_0677 / 截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:size_range.value | identity | ✓ |
| CR-D03 | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| CR-D03 | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| CR-D03 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| CR-D03 | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.product.image_refs.image_asset_status | "PENDING_IMAGE_ASSET_M3" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_status | relocate-annotation | ✓ |
| CR-D03 | facts.product.image_refs.image_asset_note | "真实图片文件不在本仓库（全仓无 IMG_*.jpg/png 资产，2026-08-17 实测）；Storyboa… | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_note | relocate-annotation | ✓ |
| CR-D03 | facts.product.image_refs.source | "截图 IMG_0672 / 截图 IMG_0684（数据包 P13「关联图片编号」原文：IMG_0672、IMG… | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| CR-D03 | facts.product.image_refs.value[0] | "IMG_0672" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[0].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[1] | "IMG_0675" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[1].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[2] | "IMG_0676" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[2].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[3] | "IMG_0677" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[3].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[4] | "IMG_0678" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[4].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[5] | "IMG_0679" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[5].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[6] | "IMG_0680" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[6].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[7] | "IMG_0681" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[7].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[8] | "IMG_0682" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[8].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[9] | "IMG_0683" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[9].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.product.image_refs.value[10] | "IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD03-P13.v1.json:image_refs[10].locator | imageid-to-sourceref | ✓ |
| CR-D03 | facts.video_account.account_id.source | "Founder 2026-08-17 IA-0 裁决：虚构编号（OQ-BUILD-13）" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.account_id.source | relocate-annotation | ✓ |
| CR-D03 | facts.video_account.account_id.value | "ACC-HXJ-001" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:account_id | identity-plain | ✓ |
| CR-D03 | facts.video_account.platform.source | "A.3.6 系统固定 + OD-03 通用阻断项④（本期仅视频号）" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.platform.source | relocate-annotation | ✓ |
| CR-D03 | facts.video_account.platform.value | "WECHAT_VIDEO" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:platform | identity-plain | ✓ |
| CR-D03 | facts.video_account.account_name.value | "衡叙集·穿衣判断（虚构）" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:account_name.value | identity | ✓ |
| CR-D03 | facts.video_account.account_name.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:account_name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.video_account.positioning.value | "面向城市女性的服装选择与真实穿着决策账号：以商品事实、场景试穿和明确取舍，回答“为什么选、怎么穿、何时不选”" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:positioning.value | identity | ✓ |
| CR-D03 | facts.video_account.positioning.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.video_account.content_style.value | ["稳口吻、熟关系、低剪辑刺激", "以一件商品或一个穿衣问题为单集单位，画面保留面料近景、正侧背面、动作和必要的… | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:content_style.value | identity | ✓ |
| CR-D03 | facts.video_account.content_style.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:content_style.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.video_account.audience_relationship.value | "不是销售话术广播站，而是长期衣橱判断伙伴；欢迎观众提交通勤、久坐、身形变化、颜色尝试和门店试穿问题，并允许后续视… | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:audience_relationship.value | identity | ✓ |
| CR-D03 | facts.video_account.audience_relationship.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | facts.video_account.primary_persona_ref.source | "模拟（版本化引用待 PersonaFacts 对象落盘后回填，本文件不自造 version）" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.primary_persona_ref.source | relocate-annotation | ✓ |
| CR-D03 | facts.video_account.primary_persona_ref.unresolved_primary_persona_ref | "沈岚，关联 R01 品牌主理人" | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.primary_persona_ref.unresolved_primary_persona_ref | relocate-annotation | ✓ |
| CR-D03 | facts.video_account.expression_boundaries.value | ["未核对款号、成分、尺码、价格和库存时不得下商品结论", "价格冲突必须同时展示并标记“待裁决”，不得选择性隐藏… | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:expression_boundaries.value | identity | ✓ |
| CR-D03 | facts.video_account.expression_boundaries.source | "模拟" | fixtures/facts/video_account/FS-VIDEOACCOUNT-CRD03-0001.v1.json:expression_boundaries.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D03 | hard_rules[0].rule_id | "R-FB01-001" | cases/CR-D03/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| CR-D03 | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/CR-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| CR-D04a | snapshot_id | "SNAP-CRD04-0001" | cases/CR-D04/fixtures/context_snapshot_a.json:snapshot_id | identity | ✓ |
| CR-D04a | brand_id | "fixture-brand-01" | cases/CR-D04/fixtures/context_snapshot_a.json:brand_id | identity | ✓ |
| CR-D04a | facts.business_goal | {"value": "PRODUCT_LAUNCH", "source": "Founder 2026-08-17… | cases/CR-D04/fixtures/task_input.json:_migrated_from_snapshot.CR-D04a.business_goal | relocate-task-input | ✓ |
| CR-D04a | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:product_id | identity-plain | ✓ |
| CR-D04a | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:name.value | identity | ✓ |
| CR-D04a | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:category.value | identity | ✓ |
| CR-D04a | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:sku.value | identity | ✓ |
| CR-D04a | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.price.raw_text | "3980元" | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| CR-D04a | facts.product.price.original_as_of | "2026-08-17" | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| CR-D04a | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| CR-D04a | facts.product.price.source | "截图 IMG_0684（数据包字段名「吊牌价」，截图原文「3980元」）" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:material.value | identity | ✓ |
| CR-D04a | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| CR-D04a | facts.product.style_attributes.value | ["大翻领", "廓形肩线", "H型风衣式", "袖口可调节袖袢", "宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:style_attributes.value | identity | ✓ |
| CR-D04a | facts.product.style_attributes.source | "截图 IMG_0674 / 截图 IMG_0677 / 截图 IMG_0680（IMG_0674 的归属不一致见… | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式", "提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:selling_points.value | identity | ✓ |
| CR-D04a | facts.product.selling_points.source | "截图 IMG_0677 / 截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:size_range.value | identity | ✓ |
| CR-D04a | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| CR-D04a | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| CR-D04a | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| CR-D04a | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04a | facts.product.image_refs.raw_text | "IMG_0672、IMG_0675—IMG_0682、IMG_0683、IMG_0684；共享图同时关联 P12" | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.image_refs.raw_text | relocate-annotation | ✓ |
| CR-D04a | facts.product.image_refs.image_asset_status | "PENDING_IMAGE_ASSET_M3" | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_status | relocate-annotation | ✓ |
| CR-D04a | facts.product.image_refs.image_asset_note | "真实图片文件不在本仓库；11 个编号只是引用，无本地字节可供 VLM 读取。M3 补齐图片资产前，输入 A 不具… | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_note | relocate-annotation | ✓ |
| CR-D04a | facts.product.image_refs.source | "截图 IMG_0672 / 截图 IMG_0684（数据包 P13「关联图片编号」原文见 raw_text；区间… | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| CR-D04a | facts.product.image_refs.value[0] | "IMG_0672" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[0].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[1] | "IMG_0675" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[1].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[2] | "IMG_0676" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[2].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[3] | "IMG_0677" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[3].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[4] | "IMG_0678" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[4].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[5] | "IMG_0679" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[5].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[6] | "IMG_0680" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[6].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[7] | "IMG_0681" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[7].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[8] | "IMG_0682" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[8].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[9] | "IMG_0683" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[9].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.image_refs.value[10] | "IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04a-P13.v1.json:image_refs[10].locator | imageid-to-sourceref | ✓ |
| CR-D04a | facts.product.visual_profile_ref | {"value": null, "status": "MISSING", "source": "A.3.3：无图片… | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.facts.product.visual_profile_ref.. | relocate-annotation | ✓ |
| CR-D04a | hard_rules[0].rule_id | "R-FB01-001" | cases/CR-D04/fixtures/context_snapshot_a.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| CR-D04a | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/CR-D04/fixtures/context_snapshot_a.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| CR-D04b | snapshot_id | "SNAP-CRD04-0002" | cases/CR-D04/fixtures/context_snapshot_b.json:snapshot_id | identity | ✓ |
| CR-D04b | brand_id | "fixture-brand-01" | cases/CR-D04/fixtures/context_snapshot_b.json:brand_id | identity | ✓ |
| CR-D04b | facts.business_goal | {"value": "PRODUCT_LAUNCH", "source": "Founder 2026-08-17… | cases/CR-D04/fixtures/task_input.json:_migrated_from_snapshot.CR-D04b.business_goal | relocate-task-input | ✓ |
| CR-D04b | facts.product.product_id | "P08" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:product_id | identity-plain | ✓ |
| CR-D04b | facts.product.name.value | "V口翻领短袖 Polo" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:name.value | identity | ✓ |
| CR-D04b | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.category.value | "V口翻领" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:category.value | identity | ✓ |
| CR-D04b | facts.product.category.source | "截图 IMG_0652" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.sku.value | "1G4901591" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:sku.value | identity | ✓ |
| CR-D04b | facts.product.sku.source | "截图 IMG_0652" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.price.raw_text | "498元" | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| CR-D04b | facts.product.price.original_as_of | "2026-08-17" | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| CR-D04b | facts.product.price.value | {"amount": 498, "currency": "CNY", "as_of": "2026-08-17T0… | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| CR-D04b | facts.product.price.source | "截图 IMG_0652（数据包字段名「吊牌价」，截图原文「498元」）" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.material.value | ["藏青面料:37.8%粘纤 31.6%棉 25.4%腈纶 5.2%氨纶", "本白色面料:36.8%粘纤 30.… | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:material.value | identity | ✓ |
| CR-D04b | facts.product.material.source | "截图 IMG_0652" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| CR-D04b | facts.product.style_attributes.value | ["V口翻领", "短袖", "修身轮廓"] | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:style_attributes.value | identity | ✓ |
| CR-D04b | facts.product.style_attributes.source | "截图 IMG_0655 / 截图 IMG_0662（数据包「版型风格特征」——已确认文字事实，本快照不提供其图片… | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.selling_points.value | ["单品图确认 V 口翻领、短袖", "藏青与本白两种面料成分分别列示"] | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:selling_points.value | identity | ✓ |
| CR-D04b | facts.product.selling_points.source | "截图 IMG_0652 / 截图 IMG_0662（数据包「已确认卖点」）" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.size_range.value | ["S", "M", "L", "XL"] | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:size_range.value | identity | ✓ |
| CR-D04b | facts.product.size_range.source | "截图 IMG_0652" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.lifecycle_stage.value | "正常在售" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:lifecycle_stage.value | identity | ✓ |
| CR-D04b | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| CR-D04b | facts.product.inventory.value | {"value": 240, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| CR-D04b | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04b-P08.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04b | facts.product.image_refs.image_refs_status | "NOT_PROVIDED_BY_EXAM_DESIGN" | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_refs_status | relocate-annotation | ✓ |
| CR-D04b | facts.product.image_refs.image_asset_note | "本快照零图片输入：不得依据商品名称、款号或品类补写颜色、版型、纹理或任何未列出的视觉细节；拍摄建议必须不依赖未知… | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_note | relocate-annotation | ✓ |
| CR-D04b | facts.product.image_refs.source | "考题条件 B.4.3/CR-D04「输入 B」原文「不提供图片」——刻意置空。数据包 P08 原有「关联图片编号… | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| CR-D04b | facts.product.visual_profile_ref | {"value": null, "status": "MISSING", "source": "A.3.3：无图片… | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.facts.product.visual_profile_ref.. | relocate-annotation | ✓ |
| CR-D04b | hard_rules[0].rule_id | "R-FB01-001" | cases/CR-D04/fixtures/context_snapshot_b.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| CR-D04b | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/CR-D04/fixtures/context_snapshot_b.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| CR-D04c | snapshot_id | "SNAP-CRD04-0003" | cases/CR-D04/fixtures/context_snapshot_c.json:snapshot_id | identity | ✓ |
| CR-D04c | brand_id | "fixture-brand-01" | cases/CR-D04/fixtures/context_snapshot_c.json:brand_id | identity | ✓ |
| CR-D04c | facts.business_goal | {"value": "PRODUCT_LAUNCH", "source": "Founder 2026-08-17… | cases/CR-D04/fixtures/task_input.json:_migrated_from_snapshot.CR-D04c.business_goal | relocate-task-input | ✓ |
| CR-D04c | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:product_id | identity-plain | ✓ |
| CR-D04c | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:name.value | identity | ✓ |
| CR-D04c | facts.product.name.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:category.value | identity | ✓ |
| CR-D04c | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:sku.value | identity | ✓ |
| CR-D04c | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.price.raw_text | "3980元" | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| CR-D04c | facts.product.price.original_as_of | "2026-08-17" | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| CR-D04c | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| CR-D04c | facts.product.price.source | "截图 IMG_0684（数据包字段名「吊牌价」，截图原文「3980元」）" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:material.value | identity | ✓ |
| CR-D04c | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| CR-D04c | facts.product.style_attributes.value | ["大翻领", "廓形肩线", "H型风衣式", "袖口可调节袖袢", "宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:style_attributes.value | identity | ✓ |
| CR-D04c | facts.product.style_attributes.source | "截图 IMG_0674 / 截图 IMG_0677 / 截图 IMG_0680（数据包已确认文字事实；IMG_0… | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式", "提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:selling_points.value | identity | ✓ |
| CR-D04c | facts.product.selling_points.source | "截图 IMG_0677 / 截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:size_range.value | identity | ✓ |
| CR-D04c | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| CR-D04c | facts.product.lifecycle_stage.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| CR-D04c | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| CR-D04c | facts.product.inventory.source | "夹具虚构-剧本" | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| CR-D04c | facts.product.image_refs.image_refs_status | "PRESENT_CORRUPTED" | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_refs_status | relocate-annotation | ✓ |
| CR-D04c | facts.product.image_refs.image_asset_note | "corrupted_image.jpg＝8192 字节随机字节，扩展名 .jpg 但非合法 JPEG：首两字节非… | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.image_refs.image_asset_note | relocate-annotation | ✓ |
| CR-D04c | facts.product.image_refs.source | "夹具虚构-坏图（不取自数据包截图；本仓无任何真实 IMG_*.jpg 资产）" | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| CR-D04c | facts.product.image_refs.value[0].sourceref_extras | {"source": "夹具虚构-坏图"} | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.image_refs.value[0].sourceref_extras | relocate-annotation | ✓ |
| CR-D04c | facts.product.image_refs.value[0] | {"source_id": "SRC-CRD04C-IMG-001", "brand_id": "fixture-… | fixtures/facts/product/FS-PRODUCT-CRD04c-P13.v1.json:image_refs[0] | sourceref-passthrough-cleaned | ✓ |
| CR-D04c | facts.product.visual_profile_ref | {"value": null, "status": "MISSING", "source": "A.3.3：本快照… | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.facts.product.visual_profile_ref.. | relocate-annotation | ✓ |
| CR-D04c | hard_rules[0].rule_id | "R-FB01-001" | cases/CR-D04/fixtures/context_snapshot_c.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| CR-D04c | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/CR-D04/fixtures/context_snapshot_c.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| E2E-01 | snapshot_id | "SNAP-E2E01-0001" | cases/E2E-01/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| E2E-01 | brand_id | "fixture-brand-01" | cases/E2E-01/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| E2E-01 | facts.time_window | {"value": "六周", "source": "Founder 2026-08-17 IA-0 裁决：六周（… | cases/E2E-01/fixtures/task_input.json:_migrated_from_snapshot.E2E-01.time_window | relocate-task-input | ✓ |
| E2E-01 | facts.audience_facts[0].audience_id | "A01" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:audience_id | identity-plain | ✓ |
| E2E-01 | facts.audience_facts[0].label.value | "稳态通勤者" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:label.value | identity | ✓ |
| E2E-01 | facts.audience_facts[0].label.source | "数据包 包3 A01【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:label.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[0].age_range.original_range_text | "33—42 岁" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience_facts[0].age_range.original_range_text | relocate-annotation | ✓ |
| E2E-01 | facts.audience_facts[0].age_range.value | {"min": 33, "max": 42, "unit": "岁"} | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:age_range.value | range-parse | ✓ |
| E2E-01 | facts.audience_facts[0].age_range.source | "数据包 包3 A01【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:age_range.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[0].occupation_or_lifestyle.value | ["品牌、咨询、教育、行政管理或专业服务岗位；工作日需要见同事和客户，下班后常直接接孩子、赴家宴或处理家庭事务；衣… | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:occupation_or_lifestyle.value | wrap-array | ✓ |
| E2E-01 | facts.audience_facts[0].occupation_or_lifestyle.source | "数据包 包3 A01【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:occupation_or_lifestyle.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[0].pain_points.value | ["上午会议要有边界感，晚上接孩子又不想显得过度正式，硬挺西装常在第二个场景里变得突兀", "通勤单程 40—60… | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:pain_points.value | identity | ✓ |
| E2E-01 | facts.audience_facts[0].pain_points.source | "数据包 包3 A01 真实痛点【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:pain_points.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[0].purchase_reasons.value | ["版型能同时处理会议、通勤、接送和周末轻社交", "品牌明确解释面料、里料、尺码和长期穿着代价", "一件外套能… | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:purchase_reasons.value | identity | ✓ |
| E2E-01 | facts.audience_facts[0].purchase_reasons.source | "数据包 包3 A01 购买理由【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:purchase_reasons.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[0].objections.value | ["羊毛、亚麻或混纺面料是否难打理，真实使用频率会不会低", "宽松版型是否只是模特图成立，自己久坐或含胸时会不会… | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:objections.value | identity | ✓ |
| E2E-01 | facts.audience_facts[0].objections.source | "数据包 包3 A01 常见顾虑【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A01.v1.json:objections.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[1].audience_id | "A02" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:audience_id | identity-plain | ✓ |
| E2E-01 | facts.audience_facts[1].label.value | "克制表达者" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:label.value | identity | ✓ |
| E2E-01 | facts.audience_facts[1].label.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:label.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[1].age_range.original_range_text | "26—32 岁" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience_facts[1].age_range.original_range_text | relocate-annotation | ✓ |
| E2E-01 | facts.audience_facts[1].age_range.value | {"min": 26, "max": 32, "unit": "岁"} | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:age_range.value | range-parse | ✓ |
| E2E-01 | facts.audience_facts[1].age_range.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:age_range.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[1].occupation_or_lifestyle.value | ["新消费、电商、设计、内容、互联网运营或自由职业；工作环境着装弹性大，会拍短视频和日常照片，但不希望整个人像在追… | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:occupation_or_lifestyle.value | wrap-array | ✓ |
| E2E-01 | facts.audience_facts[1].occupation_or_lifestyle.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:occupation_or_lifestyle.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[1].pain_points.value | ["衣柜以黑、白、灰、牛仔为主，想加入荧光色或印花，却担心只能拍一次照片、无法进入日常", "对“显瘦模板”疲劳，… | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:pain_points.value | identity | ✓ |
| E2E-01 | facts.audience_facts[1].pain_points.source | "数据包 包3 A02 真实痛点【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:pain_points.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[1].purchase_reasons.value | ["品牌把反常识单品放进真实上班、通勤和周末场景验证", "买手能给出“这一件负责表达，其余单品负责安定”的具体搭… | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:purchase_reasons.value | identity | ✓ |
| E2E-01 | facts.audience_facts[1].purchase_reasons.source | "数据包 包3 A02 购买理由【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:purchase_reasons.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.audience_facts[1].objections.value | ["荧光色、腰果花等强视觉元素会不会很快厌倦", "修身针织或高腰裤在活动、进食和久坐时是否仍然舒服", "视频中… | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:objections.value | identity | ✓ |
| E2E-01 | facts.audience_facts[1].objections.source | "数据包 包3 A02 常见顾虑【模拟】" | fixtures/facts/audience/FS-AUD-E2E01-A02.v1.json:objections.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.brand_id | "fixture-brand-01" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:brand_id | identity-plain | ✓ |
| E2E-01 | facts.brand_facts.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:brand_name.value | identity | ✓ |
| E2E-01 | facts.brand_facts.brand_name.source | "数据包 包1【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.positioning_statement.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:positioning.value | identity | ✓ |
| E2E-01 | facts.brand_facts.positioning_statement.source | "数据包 包1 一句话定位【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:values.value | identity | ✓ |
| E2E-01 | facts.brand_facts.values.source | "数据包 包1 价值主张【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.tone.value | ["稳、具体、有判断、留余地；像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:tone.value | wrap-array | ✓ |
| E2E-01 | facts.brand_facts.tone.source | "数据包 包1 说话调性【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:target_customer_summary.value | identity | ✓ |
| E2E-01 | facts.brand_facts.target_customer_summary.source | "数据包 包1 目标客户一句话【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.forbidden_expressions.note | "运营真源以 acceptance/detectors/forbidden_lexicon.yaml 为唯一真源（… | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand_facts.forbidden_expressions.note | relocate-annotation | ✓ |
| E2E-01 | facts.brand_facts.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| E2E-01 | facts.brand_facts.forbidden_expressions.source | "数据包 包1 禁用表达清单【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_facts.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:commercial_constraints.value | identity | ✓ |
| E2E-01 | facts.brand_facts.commercial_constraints.source | "数据包 包1 商业硬约束【模拟】" | fixtures/facts/brand/FS-BRAND-E2E01-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[0].persona_id | "R01" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:persona_id | identity-plain | ✓ |
| E2E-01 | facts.persona_facts[0].identity.value | "衡叙集虚构品牌主理人，44 岁；负责商品取舍、定价边界和门店反馈复盘" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:identity.value | identity | ✓ |
| E2E-01 | facts.persona_facts[0].identity.source | "数据包 包4 R01【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:identity.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[0].voice_traits.value | ["句子不快，先把问题和条件说清，再给判断；常用门店试穿、退换原因、面料取舍和一件衣服穿了多久来举例；很少直接下购… | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:voice_traits.value | wrap-array | ✓ |
| E2E-01 | facts.persona_facts[0].voice_traits.source | "数据包 包4 R01 说话风格【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:voice_traits.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[0].beliefs.value | ["“衣服先要进入生活，才有资格谈风格。”", "“不适合你的商品，说清楚比卖出去更重要。”", "“价格要能回到… | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:beliefs.value | identity | ✓ |
| E2E-01 | facts.persona_facts[0].beliefs.source | "数据包 包4 R01 公开表达过的信念【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:beliefs.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[0].audience_relationship.value | "把观众视为长期熟客和共同判断者；允许观众带着不同体型、预算和生活阶段反驳她，不用“教育消费者”的姿态压过真实反馈" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:audience_relationship.value | identity | ✓ |
| E2E-01 | facts.persona_facts[0].audience_relationship.source | "数据包 包4 R01 与粉丝关系【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[0].forbidden_styles.value | ["“姐妹们冲”", "“闭眼买”", "“谁穿谁好看”", "“全网最低”", "“错过后悔”"] | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:forbidden_styles.value | identity | ✓ |
| E2E-01 | facts.persona_facts[0].forbidden_styles.source | "数据包 包4 R01 绝不使用的表达【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:forbidden_styles.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[0].speaker_constraints.value | ["不做高频叫卖直播；不在无法核对款号、价格、成分时讲商品结论；每条视频最多讲一个核心判断；避免过度磨皮和改变服装… | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:speaker_constraints.value | wrap-array | ✓ |
| E2E-01 | facts.persona_facts[0].speaker_constraints.source | "数据包 包4 R01 出镜限制【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R01.v1.json:speaker_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[1].persona_id | "R02" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:persona_id | identity-plain | ✓ |
| E2E-01 | facts.persona_facts[1].identity.value | "衡叙集虚构年轻买手，28 岁；负责新款试穿、颜色与比例实验、年轻客群反馈和一衣多搭验证" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:identity.value | identity | ✓ |
| E2E-01 | facts.persona_facts[1].identity.source | "数据包 包4 R02【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:identity.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[1].voice_traits.value | ["节奏比主理人快，先给镜前结论，再用三个动作或三套搭配验证；常以“我原本也觉得不日常”“换掉哪一件就成立”开场，… | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:voice_traits.value | wrap-array | ✓ |
| E2E-01 | facts.persona_facts[1].voice_traits.source | "数据包 包4 R02 说话风格【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:voice_traits.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[1].beliefs.value | ["“鲜明不等于难穿，关键是整套里只能有一个人负责说话。”", "“试穿不是证明它好，而是找到它在哪个条件下不成立… | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:beliefs.value | identity | ✓ |
| E2E-01 | facts.persona_facts[1].beliefs.source | "数据包 包4 R02 公开表达过的信念【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:beliefs.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[1].audience_relationship.value | "像替观众先试错的同龄同事；会展示犹豫、失败搭配和调整过程，以现场比较建立信任，不把自己放在审美裁判位置" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:audience_relationship.value | identity | ✓ |
| E2E-01 | facts.persona_facts[1].audience_relationship.source | "数据包 包4 R02 与粉丝关系【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[1].forbidden_styles.value | ["“你不懂时尚”", "“普通人驾驭不了”", "“必须拥有”", "“纯欲”", "“辣妹必备”"] | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:forbidden_styles.value | identity | ✓ |
| E2E-01 | facts.persona_facts[1].forbidden_styles.source | "数据包 包4 R02 绝不使用的表达【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:forbidden_styles.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.persona_facts[1].speaker_constraints.value | ["试穿必须保留自然走动、坐下、抬手和侧面镜头；不得只拍正面定格；颜色判断不得使用重滤镜；不替主理人宣布价格政策或… | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:speaker_constraints.value | wrap-array | ✓ |
| E2E-01 | facts.persona_facts[1].speaker_constraints.source | "数据包 包4 R02 出镜限制【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E01-R02.v1.json:speaker_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:product_id | identity-plain | ✓ |
| E2E-01 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:name.value | identity | ✓ |
| E2E-01 | facts.product.name.source | "数据包 P13 商品名【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:category.value | identity | ✓ |
| E2E-01 | facts.product.category.source | "截图 IMG_0684（原文照抄，未规范化）" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.price.verbatim | "截图原文“3980元”" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.verbatim | relocate-annotation | ✓ |
| E2E-01 | facts.product.price.original_as_of | "2026-08-17" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| E2E-01 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| E2E-01 | facts.product.price.source | "截图 IMG_0684；价格事实有效日统一记为 2026-08-17【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.style_number | {"value": "1G9971081", "source": "截图 IMG_0684"} | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.style_number.. | relocate-annotation | ✓ |
| E2E-01 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:material.value | identity | ✓ |
| E2E-01 | facts.product.material.source | "截图 IMG_0684（四色成分原文全录，一字不改）" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.lining | {"value": "缺失", "source": "截图 IMG_0684（截图未出现；故意缺失，按夹具纪律不补… | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| E2E-01 | facts.product.style_attributes.value | ["大翻领、廓形肩线、H型风衣式；袖口可调节袖袢；宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:style_attributes.value | wrap-array | ✓ |
| E2E-01 | facts.product.style_attributes.source | "截图 IMG_0674、IMG_0677、IMG_0680" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式；提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:selling_points.value | wrap-array | ✓ |
| E2E-01 | facts.product.selling_points.source | "截图 IMG_0677、IMG_0684" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:size_range.value | identity | ✓ |
| E2E-01 | facts.product.size_range.source | "截图 IMG_0684（号型原文照抄）" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| E2E-01 | facts.product.lifecycle_stage.source | "数据包 P13【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| E2E-01 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| E2E-01 | facts.product.inventory.source | "数据包 P13【虚构-剧本】；与 B.5.1/E2E-01 冻结事实一致" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.product.image_refs.source | "截图 IMG_0672、截图 IMG_0684" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| E2E-01 | facts.product.image_refs.value | "IMG_0672、IMG_0675—IMG_0682、IMG_0683、IMG_0684；共享图同时关联 P12" | fixtures/facts/product/FS-PRODUCT-E2E01-P13.v1.json:image_refs[0].locator | imagetext-to-sourceref | ✓ |
| E2E-01 | facts.video_account_facts.account_id.source | "Founder 2026-08-17 IA-0 裁决：虚构编号（OQ-BUILD-13）" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.account_id.source | relocate-annotation | ✓ |
| E2E-01 | facts.video_account_facts.account_id.value | "ACC-HXJ-001" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:account_id | identity-plain | ✓ |
| E2E-01 | facts.video_account_facts.platform.source | "A.3.6（platform 系统固定 WECHAT_VIDEO）+ 数据包 包5 视频号账号事实" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.platform.source | relocate-annotation | ✓ |
| E2E-01 | facts.video_account_facts.platform.value | "WECHAT_VIDEO" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:platform | identity-plain | ✓ |
| E2E-01 | facts.video_account_facts.account_name.value | "衡叙集·穿衣判断（虚构）" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:account_name.value | identity | ✓ |
| E2E-01 | facts.video_account_facts.account_name.source | "数据包 包5【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:account_name.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.video_account_facts.positioning.value | "面向城市女性的服装选择与真实穿着决策账号：以商品事实、场景试穿和明确取舍，回答“为什么选、怎么穿、何时不选”" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:positioning.value | identity | ✓ |
| E2E-01 | facts.video_account_facts.positioning.source | "数据包 包5 定位【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.video_account_facts.content_style.value | ["稳口吻、熟关系、低剪辑刺激；以一件商品或一个穿衣问题为单集单位，画面保留面料近景、正侧背面、动作和必要的事实卡… | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:content_style.value | wrap-array | ✓ |
| E2E-01 | facts.video_account_facts.content_style.source | "数据包 包5 内容风格【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:content_style.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.video_account_facts.audience_relationship.value | "不是销售话术广播站，而是长期衣橱判断伙伴；欢迎观众提交通勤、久坐、身形变化、颜色尝试和门店试穿问题，并允许后续视… | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:audience_relationship.value | identity | ✓ |
| E2E-01 | facts.video_account_facts.audience_relationship.source | "数据包 包5 与观众关系【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.video_account_facts.primary_persona_ref.source | "数据包 包5 主出镜人「沈岚，关联 R01 品牌主理人」【模拟】" | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.primary_persona_ref.source | relocate-annotation | ✓ |
| E2E-01 | facts.video_account_facts.primary_persona_ref.value | "R01" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:primary_persona_ref.object_id | personaid-to-versionedref:FS-PERSONA-E2E01-R01 | ✓ |
| E2E-01 | facts.video_account_facts.expression_boundaries.value | ["未核对款号、成分、尺码、价格和库存时不得下商品结论", "价格冲突必须同时展示并标记“待裁决”，不得选择性隐藏… | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:expression_boundaries.value | identity | ✓ |
| E2E-01 | facts.video_account_facts.expression_boundaries.source | "数据包 包5 表达边界【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E01-0001.v1.json:expression_boundaries.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-01 | facts.brand_positioning | {"value": "HIGH_END", "source": "B.5.1/E2E-01 冻结事实（「品牌定位高… | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand_positioning.. | relocate-annotation | ✓ |
| E2E-01 | facts.inventory | {"value": 800, "unit": "件", "source": "B.5.1/E2E-01 冻结事实（… | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.inventory.. | relocate-annotation | ✓ |
| E2E-01 | hard_rules[0].rule_id | "R-BDD01-001" | cases/E2E-01/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| E2E-01 | hard_rules[0] | {"version": 1, "statement": "禁止低价叫卖表达（forbidden_expressio… | cases/E2E-01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| E2E-03 | snapshot_id | "SNAP-E2E03-0001" | cases/E2E-03/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| E2E-03 | brand_id | "fixture-brand-01" | cases/E2E-03/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| E2E-03 | facts.business_goal | {"value": "PRODUCT_LAUNCH", "source": "Founder 2026-08-17… | cases/E2E-03/fixtures/task_input.json:_migrated_from_snapshot.E2E-03.business_goal | relocate-task-input | ✓ |
| E2E-03 | facts.audience_facts[0].audience_id | "A02" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:audience_id | identity-plain | ✓ |
| E2E-03 | facts.audience_facts[0].label.value | "克制表达者" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:label.value | identity | ✓ |
| E2E-03 | facts.audience_facts[0].label.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:label.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.audience_facts[0].age_range.original_range_text | "26—32 岁" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience_facts[0].age_range.original_range_text | relocate-annotation | ✓ |
| E2E-03 | facts.audience_facts[0].age_range.value | {"min": 26, "max": 32, "unit": "岁"} | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:age_range.value | range-parse | ✓ |
| E2E-03 | facts.audience_facts[0].age_range.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:age_range.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.audience_facts[0].occupation_or_lifestyle.value | ["新消费、电商、设计、内容、互联网运营或自由职业；工作环境着装弹性大，会拍短视频和日常照片，但不希望整个人像在追… | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:occupation_or_lifestyle.value | wrap-array | ✓ |
| E2E-03 | facts.audience_facts[0].occupation_or_lifestyle.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:occupation_or_lifestyle.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.audience_facts[0].pain_points.value | ["衣柜以黑、白、灰、牛仔为主，想加入荧光色或印花，却担心只能拍一次照片、无法进入日常", "对“显瘦模板”疲劳，… | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:pain_points.value | identity | ✓ |
| E2E-03 | facts.audience_facts[0].pain_points.source | "数据包 包3 A02 真实痛点【模拟】" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:pain_points.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.audience_facts[0].purchase_reasons.value | ["品牌把反常识单品放进真实上班、通勤和周末场景验证", "买手能给出“这一件负责表达，其余单品负责安定”的具体搭… | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:purchase_reasons.value | identity | ✓ |
| E2E-03 | facts.audience_facts[0].purchase_reasons.source | "数据包 包3 A02 购买理由【模拟】" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:purchase_reasons.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.audience_facts[0].objections.value | ["荧光色、腰果花等强视觉元素会不会很快厌倦", "修身针织或高腰裤在活动、进食和久坐时是否仍然舒服", "视频中… | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:objections.value | identity | ✓ |
| E2E-03 | facts.audience_facts[0].objections.source | "数据包 包3 A02 常见顾虑【模拟】" | fixtures/facts/audience/FS-AUD-E2E03-A02.v1.json:objections.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.brand_id | "fixture-brand-01" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:brand_id | identity-plain | ✓ |
| E2E-03 | facts.brand_facts.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:brand_name.value | identity | ✓ |
| E2E-03 | facts.brand_facts.brand_name.source | "数据包 包1【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.positioning_statement.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:positioning.value | identity | ✓ |
| E2E-03 | facts.brand_facts.positioning_statement.source | "数据包 包1 一句话定位【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:values.value | identity | ✓ |
| E2E-03 | facts.brand_facts.values.source | "数据包 包1 价值主张【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.tone.value | ["稳、具体、有判断、留余地；像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:tone.value | wrap-array | ✓ |
| E2E-03 | facts.brand_facts.tone.source | "数据包 包1 说话调性【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:target_customer_summary.value | identity | ✓ |
| E2E-03 | facts.brand_facts.target_customer_summary.source | "数据包 包1 目标客户一句话【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.forbidden_expressions.note | "运营真源以 acceptance/detectors/forbidden_lexicon.yaml 为唯一真源（… | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand_facts.forbidden_expressions.note | relocate-annotation | ✓ |
| E2E-03 | facts.brand_facts.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| E2E-03 | facts.brand_facts.forbidden_expressions.source | "数据包 包1 禁用表达清单【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_facts.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:commercial_constraints.value | identity | ✓ |
| E2E-03 | facts.brand_facts.commercial_constraints.source | "数据包 包1 商业硬约束【模拟】" | fixtures/facts/brand/FS-BRAND-E2E03-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[0].persona_id | "R01" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:persona_id | identity-plain | ✓ |
| E2E-03 | facts.persona_facts[0].identity.value | "衡叙集虚构品牌主理人，44 岁；负责商品取舍、定价边界和门店反馈复盘" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:identity.value | identity | ✓ |
| E2E-03 | facts.persona_facts[0].identity.source | "数据包 包4 R01【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:identity.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[0].voice_traits.value | ["句子不快，先把问题和条件说清，再给判断；常用门店试穿、退换原因、面料取舍和一件衣服穿了多久来举例；很少直接下购… | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:voice_traits.value | wrap-array | ✓ |
| E2E-03 | facts.persona_facts[0].voice_traits.source | "数据包 包4 R01 说话风格【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:voice_traits.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[0].beliefs.value | ["“衣服先要进入生活，才有资格谈风格。”", "“不适合你的商品，说清楚比卖出去更重要。”", "“价格要能回到… | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:beliefs.value | identity | ✓ |
| E2E-03 | facts.persona_facts[0].beliefs.source | "数据包 包4 R01 公开表达过的信念【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:beliefs.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[0].audience_relationship.value | "把观众视为长期熟客和共同判断者；允许观众带着不同体型、预算和生活阶段反驳她，不用“教育消费者”的姿态压过真实反馈" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:audience_relationship.value | identity | ✓ |
| E2E-03 | facts.persona_facts[0].audience_relationship.source | "数据包 包4 R01 与粉丝关系【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[0].forbidden_styles.value | ["“姐妹们冲”", "“闭眼买”", "“谁穿谁好看”", "“全网最低”", "“错过后悔”"] | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:forbidden_styles.value | identity | ✓ |
| E2E-03 | facts.persona_facts[0].forbidden_styles.source | "数据包 包4 R01 绝不使用的表达【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:forbidden_styles.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[0].speaker_constraints.value | ["不做高频叫卖直播；不在无法核对款号、价格、成分时讲商品结论；每条视频最多讲一个核心判断；避免过度磨皮和改变服装… | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:speaker_constraints.value | wrap-array | ✓ |
| E2E-03 | facts.persona_facts[0].speaker_constraints.source | "数据包 包4 R01 出镜限制【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R01.v1.json:speaker_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[1].persona_id | "R02" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:persona_id | identity-plain | ✓ |
| E2E-03 | facts.persona_facts[1].identity.value | "衡叙集虚构年轻买手，28 岁；负责新款试穿、颜色与比例实验、年轻客群反馈和一衣多搭验证" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:identity.value | identity | ✓ |
| E2E-03 | facts.persona_facts[1].identity.source | "数据包 包4 R02【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:identity.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[1].voice_traits.value | ["节奏比主理人快，先给镜前结论，再用三个动作或三套搭配验证；常以“我原本也觉得不日常”“换掉哪一件就成立”开场，… | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:voice_traits.value | wrap-array | ✓ |
| E2E-03 | facts.persona_facts[1].voice_traits.source | "数据包 包4 R02 说话风格【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:voice_traits.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[1].beliefs.value | ["“鲜明不等于难穿，关键是整套里只能有一个人负责说话。”", "“试穿不是证明它好，而是找到它在哪个条件下不成立… | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:beliefs.value | identity | ✓ |
| E2E-03 | facts.persona_facts[1].beliefs.source | "数据包 包4 R02 公开表达过的信念【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:beliefs.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[1].audience_relationship.value | "像替观众先试错的同龄同事；会展示犹豫、失败搭配和调整过程，以现场比较建立信任，不把自己放在审美裁判位置" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:audience_relationship.value | identity | ✓ |
| E2E-03 | facts.persona_facts[1].audience_relationship.source | "数据包 包4 R02 与粉丝关系【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[1].forbidden_styles.value | ["“你不懂时尚”", "“普通人驾驭不了”", "“必须拥有”", "“纯欲”", "“辣妹必备”"] | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:forbidden_styles.value | identity | ✓ |
| E2E-03 | facts.persona_facts[1].forbidden_styles.source | "数据包 包4 R02 绝不使用的表达【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:forbidden_styles.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.persona_facts[1].speaker_constraints.value | ["试穿必须保留自然走动、坐下、抬手和侧面镜头；不得只拍正面定格；颜色判断不得使用重滤镜；不替主理人宣布价格政策或… | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:speaker_constraints.value | wrap-array | ✓ |
| E2E-03 | facts.persona_facts[1].speaker_constraints.source | "数据包 包4 R02 出镜限制【模拟】" | fixtures/facts/persona/FS-PERSONA-E2E03-R02.v1.json:speaker_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.product_id | "P11" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:product_id | identity-plain | ✓ |
| E2E-03 | facts.product.name.value | "荧光绿高腰阔腿裤" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:name.value | identity | ✓ |
| E2E-03 | facts.product.name.source | "数据包 P11 商品名【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.category.value | "裤子" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:category.value | identity | ✓ |
| E2E-03 | facts.product.category.source | "截图 IMG_0671" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.price.verbatim | "截图原文“零售价：2280元”" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.verbatim | relocate-annotation | ✓ |
| E2E-03 | facts.product.price.note | "数据包原文注明「截图未出现『吊牌价』字样」——本字段登记的是截图上的「零售价」，不得改写为吊牌价" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.note | relocate-annotation | ✓ |
| E2E-03 | facts.product.price.original_as_of | "2026-08-17" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| E2E-03 | facts.product.price.value | {"amount": 2280, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| E2E-03 | facts.product.price.source | "截图 IMG_0671；价格事实有效日统一记为 2026-08-17【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.style_number | {"value": "02I2K253-A06-G02", "source": "截图 IMG_0667、截图 I… | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.style_number.. | relocate-annotation | ✓ |
| E2E-03 | facts.product.material.note | "两处截图写法不同（含空格差异），按一字不改纪律两条原文并列保留，不合并归一" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.material.note | relocate-annotation | ✓ |
| E2E-03 | facts.product.material.value | ["面料1：棉100%", "面料：棉 100%"] | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:material.value | identity | ✓ |
| E2E-03 | facts.product.material.source | "截图 IMG_0667（「面料1：棉100%」）；截图 IMG_0671（「面料：棉 100%」）" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.lining | {"value": "缺失", "source": "截图 IMG_0667、截图 IMG_0671（截图未出现；… | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| E2E-03 | facts.product.style_attributes.value | ["荧光绿、高腰、阔腿、附腰带；商品指数标注版型“合身”、弹力“无弹”、厚度“适中”"] | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:style_attributes.value | wrap-array | ✓ |
| E2E-03 | facts.product.style_attributes.source | "截图 IMG_0664、截图 IMG_0667" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.selling_points.value | ["颜色“荧光绿”；面料“棉100%”；高腰腰带结构与阔腿裤型"] | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:selling_points.value | wrap-array | ✓ |
| E2E-03 | facts.product.selling_points.source | "截图 IMG_0667、截图 IMG_0669、截图 IMG_0671" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.size_range.value | ["34", "36", "38", "40"] | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:size_range.value | identity | ✓ |
| E2E-03 | facts.product.size_range.source | "截图 IMG_0670（号型原文照抄）" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.lifecycle_stage.value | "正常在售新品" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:lifecycle_stage.value | identity | ✓ |
| E2E-03 | facts.product.lifecycle_stage.source | "数据包 P11【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| E2E-03 | facts.product.inventory.value | {"value": 180, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| E2E-03 | facts.product.inventory.source | "数据包 P11【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.product.image_refs.source | "截图 IMG_0664、截图 IMG_0671" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| E2E-03 | facts.product.image_refs.value | "IMG_0664—IMG_0671" | fixtures/facts/product/FS-PRODUCT-E2E03-P11.v1.json:image_refs[0].locator | imagetext-to-sourceref | ✓ |
| E2E-03 | facts.video_account_facts.account_id.source | "Founder 2026-08-17 IA-0 裁决：虚构编号（OQ-BUILD-13）" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.account_id.source | relocate-annotation | ✓ |
| E2E-03 | facts.video_account_facts.account_id.value | "ACC-HXJ-001" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:account_id | identity-plain | ✓ |
| E2E-03 | facts.video_account_facts.platform.source | "A.3.6（platform 系统固定 WECHAT_VIDEO）+ 数据包 包5 视频号账号事实" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.platform.source | relocate-annotation | ✓ |
| E2E-03 | facts.video_account_facts.platform.value | "WECHAT_VIDEO" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:platform | identity-plain | ✓ |
| E2E-03 | facts.video_account_facts.account_name.value | "衡叙集·穿衣判断（虚构）" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:account_name.value | identity | ✓ |
| E2E-03 | facts.video_account_facts.account_name.source | "数据包 包5【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:account_name.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.video_account_facts.positioning.value | "面向城市女性的服装选择与真实穿着决策账号：以商品事实、场景试穿和明确取舍，回答“为什么选、怎么穿、何时不选”" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:positioning.value | identity | ✓ |
| E2E-03 | facts.video_account_facts.positioning.source | "数据包 包5 定位【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.video_account_facts.content_style.value | ["稳口吻、熟关系、低剪辑刺激；以一件商品或一个穿衣问题为单集单位，画面保留面料近景、正侧背面、动作和必要的事实卡… | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:content_style.value | wrap-array | ✓ |
| E2E-03 | facts.video_account_facts.content_style.source | "数据包 包5 内容风格【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:content_style.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.video_account_facts.audience_relationship.value | "不是销售话术广播站，而是长期衣橱判断伙伴；欢迎观众提交通勤、久坐、身形变化、颜色尝试和门店试穿问题，并允许后续视… | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:audience_relationship.value | identity | ✓ |
| E2E-03 | facts.video_account_facts.audience_relationship.source | "数据包 包5 与观众关系【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.video_account_facts.primary_persona_ref.source | "数据包 包5 主出镜人「沈岚，关联 R01 品牌主理人」【模拟】" | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.primary_persona_ref.source | relocate-annotation | ✓ |
| E2E-03 | facts.video_account_facts.primary_persona_ref.value | "R01" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:primary_persona_ref.object_id | personaid-to-versionedref:FS-PERSONA-E2E03-R01 | ✓ |
| E2E-03 | facts.video_account_facts.expression_boundaries.value | ["未核对款号、成分、尺码、价格和库存时不得下商品结论", "价格冲突必须同时展示并标记“待裁决”，不得选择性隐藏… | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:expression_boundaries.value | identity | ✓ |
| E2E-03 | facts.video_account_facts.expression_boundaries.source | "数据包 包5 表达边界【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-E2E03-0001.v1.json:expression_boundaries.source_refs[0].locator | sourceref-derive | ✓ |
| E2E-03 | facts.brand_positioning | {"value": "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度… | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand_positioning.. | relocate-annotation | ✓ |
| E2E-03 | hard_rules[0].rule_id | "R-FB01-001" | cases/E2E-03/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| E2E-03 | hard_rules[0] | {"version": 1, "statement": "禁止在任何输出中使用 fixture-brand-01 … | cases/E2E-03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
| INT-D01 | snapshot_id | "SNAP-INTD01-0001" | cases/INT-D01/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| INT-D01 | brand_id | "fixture-brand-01" | cases/INT-D01/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| INT-D01 | facts.business_goal | {"value": null, "status": "MISSING", "source": "故意缺失（夹具设计… | cases/INT-D01/fixtures/task_input.json:_migrated_from_snapshot.INT-D01.business_goal | relocate-task-input | ✓ |
| INT-D01 | facts.audience.value | null | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.value | relocate-annotation | ✓ |
| INT-D01 | facts.audience.status | "MISSING" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.status | relocate-annotation | ✓ |
| INT-D01 | facts.audience.source | "故意缺失（夹具设计）" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.source | relocate-annotation | ✓ |
| INT-D01 | facts.audience.note | "数据包 §4 包3（A01/A02）存在，本快照刻意不带入；依据 B.4.1/INT-D01「禁止结果」点名「虚… | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.note | relocate-annotation | ✓ |
| INT-D01 | facts.brand.value | null | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.value | relocate-annotation | ✓ |
| INT-D01 | facts.brand.status | "MISSING" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.status | relocate-annotation | ✓ |
| INT-D01 | facts.brand.source | "故意缺失（夹具设计）" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.source | relocate-annotation | ✓ |
| INT-D01 | facts.brand.note | "品牌定位/价值主张/调性/禁用表达/商业硬约束一概不在场。依据 B.4.1/INT-D01「禁止结果」「虚构库存… | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.note | relocate-annotation | ✓ |
| INT-D01 | facts.persona.value | null | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.value | relocate-annotation | ✓ |
| INT-D01 | facts.persona.status | "MISSING" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.status | relocate-annotation | ✓ |
| INT-D01 | facts.persona.source | "故意缺失（夹具设计）" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.source | relocate-annotation | ✓ |
| INT-D01 | facts.persona.note | "数据包 §5 包4（R01 沈岚 / R02 许澄）存在，本快照刻意不带入；禁止由模型补写创始人背景" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.note | relocate-annotation | ✓ |
| INT-D01 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:product_id | identity-plain | ✓ |
| INT-D01 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:name.value | identity | ✓ |
| INT-D01 | facts.product.name.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:category.value | identity | ✓ |
| INT-D01 | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:sku.value | identity | ✓ |
| INT-D01 | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.price.raw_text | "3980元" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| INT-D01 | facts.product.price.original_as_of | "2026-08-17" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| INT-D01 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| INT-D01 | facts.product.price.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:material.value | identity | ✓ |
| INT-D01 | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| INT-D01 | facts.product.style_attributes.value | ["大翻领、廓形肩线、H型风衣式；袖口可调节袖袢；宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:style_attributes.value | wrap-array | ✓ |
| INT-D01 | facts.product.style_attributes.source | "截图 IMG_0674、截图 IMG_0677、截图 IMG_0680" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式；提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:selling_points.value | wrap-array | ✓ |
| INT-D01 | facts.product.selling_points.source | "截图 IMG_0677、截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:size_range.value | identity | ✓ |
| INT-D01 | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D01 | facts.product.image_refs.source | "截图 IMG_0672、截图 IMG_0684" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| INT-D01 | facts.product.image_refs.value | "IMG_0672、IMG_0675—IMG_0682、IMG_0683、IMG_0684；共享图同时关联 P12" | fixtures/facts/product/FS-PRODUCT-INTD01-P13.v1.json:image_refs[0].locator | imagetext-to-sourceref | ✓ |
| INT-D01 | facts.video_account.value | null | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.value | relocate-annotation | ✓ |
| INT-D01 | facts.video_account.status | "MISSING" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.status | relocate-annotation | ✓ |
| INT-D01 | facts.video_account.source | "故意缺失（夹具设计）" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.source | relocate-annotation | ✓ |
| INT-D01 | facts.video_account.note | "数据包 §6 包5 视频号账号事实存在，本快照刻意不带入；禁止由模型补写账号关系" | cases/INT-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.note | relocate-annotation | ✓ |
| INT-D02 | snapshot_id | "SNAP-INTD02-0001" | cases/INT-D02/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| INT-D02 | brand_id | "fixture-brand-01" | cases/INT-D02/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| INT-D02 | facts.business_goal | {"value": null, "status": "MISSING", "source": "故意缺失（夹具设计… | cases/INT-D02/fixtures/task_input.json:_migrated_from_snapshot.INT-D02.business_goal | relocate-task-input | ✓ |
| INT-D02 | facts.audience.value | null | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.value | relocate-annotation | ✓ |
| INT-D02 | facts.audience.status | "MISSING" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.status | relocate-annotation | ✓ |
| INT-D02 | facts.audience.source | "故意缺失（夹具设计）" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.source | relocate-annotation | ✓ |
| INT-D02 | facts.audience.note | "B.4.1/INT-D02「输入」未点名；数据包 §4 包3（A01/A02）存在但本快照未带入，如实登记为缺失" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.note | relocate-annotation | ✓ |
| INT-D02 | facts.brand.value | null | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.value | relocate-annotation | ✓ |
| INT-D02 | facts.brand.status | "MISSING" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.status | relocate-annotation | ✓ |
| INT-D02 | facts.brand.source | "故意缺失（夹具设计）" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.source | relocate-annotation | ✓ |
| INT-D02 | facts.brand.note | "B.4.1/INT-D02「输入」「缺少…品牌信息」；品牌定位/价值主张/说话调性/禁用表达清单/商业硬约束一概… | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.note | relocate-annotation | ✓ |
| INT-D02 | facts.persona.value | null | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.value | relocate-annotation | ✓ |
| INT-D02 | facts.persona.status | "MISSING" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.status | relocate-annotation | ✓ |
| INT-D02 | facts.persona.source | "故意缺失（夹具设计）" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.source | relocate-annotation | ✓ |
| INT-D02 | facts.persona.note | "B.4.1/INT-D02「输入」「缺少影响表达的账号人格」；数据包 §5 包4（R01 沈岚 / R02 许澄… | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.note | relocate-annotation | ✓ |
| INT-D02 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:product_id | identity-plain | ✓ |
| INT-D02 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:name.value | identity | ✓ |
| INT-D02 | facts.product.name.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:category.value | identity | ✓ |
| INT-D02 | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:sku.value | identity | ✓ |
| INT-D02 | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.price.raw_text | "3980元" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| INT-D02 | facts.product.price.original_as_of | "2026-08-17" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| INT-D02 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| INT-D02 | facts.product.price.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:material.value | identity | ✓ |
| INT-D02 | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| INT-D02 | facts.product.style_attributes.value | ["大翻领、廓形肩线、H型风衣式；袖口可调节袖袢；宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:style_attributes.value | wrap-array | ✓ |
| INT-D02 | facts.product.style_attributes.source | "截图 IMG_0674、截图 IMG_0677、截图 IMG_0680" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式；提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:selling_points.value | wrap-array | ✓ |
| INT-D02 | facts.product.selling_points.source | "截图 IMG_0677、截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:size_range.value | identity | ✓ |
| INT-D02 | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| INT-D02 | facts.product.lifecycle_stage.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| INT-D02 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| INT-D02 | facts.product.inventory.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D02 | facts.product.image_refs.source | "截图 IMG_0672、截图 IMG_0684" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| INT-D02 | facts.product.image_refs.value | "IMG_0672、IMG_0675—IMG_0682、IMG_0683、IMG_0684；共享图同时关联 P12" | fixtures/facts/product/FS-PRODUCT-INTD02-P13.v1.json:image_refs[0].locator | imagetext-to-sourceref | ✓ |
| INT-D02 | facts.video_account.value | null | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.value | relocate-annotation | ✓ |
| INT-D02 | facts.video_account.status | "MISSING" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.status | relocate-annotation | ✓ |
| INT-D02 | facts.video_account.source | "故意缺失（夹具设计）" | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.source | relocate-annotation | ✓ |
| INT-D02 | facts.video_account.note | "数据包 §6 包5 视频号账号事实存在，本快照刻意不带入。B.4.1/INT-D02「禁止结果」明禁「编造…账号… | cases/INT-D02/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.note | relocate-annotation | ✓ |
| INT-D03 | snapshot_id | "SNAP-INTD03-0001" | cases/INT-D03/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| INT-D03 | brand_id | "fixture-brand-01" | cases/INT-D03/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| INT-D03 | facts.business_goal | {"value": null, "status": "MISSING", "source": "刻意不入快照（夹具… | cases/INT-D03/fixtures/task_input.json:_migrated_from_snapshot.INT-D03.business_goal | relocate-task-input | ✓ |
| INT-D03 | facts.audience.value | null | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.value | relocate-annotation | ✓ |
| INT-D03 | facts.audience.status | "MISSING" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.status | relocate-annotation | ✓ |
| INT-D03 | facts.audience.source | "故意缺失（夹具设计）" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.source | relocate-annotation | ✓ |
| INT-D03 | facts.audience.note | "B.4.1/INT-D03 未要求受众事实；数据包 §4 包3（A01/A02）存在但本快照未带入。品牌事实内的… | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience.note | relocate-annotation | ✓ |
| INT-D03 | facts.brand.brand_id | "fixture-brand-01" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:brand_id | identity-plain | ✓ |
| INT-D03 | facts.brand.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:brand_name.value | identity | ✓ |
| INT-D03 | facts.brand.brand_name.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.brand.positioning.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:positioning.value | identity | ✓ |
| INT-D03 | facts.brand.positioning.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.brand.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:values.value | identity | ✓ |
| INT-D03 | facts.brand.values.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.brand.tone.value | ["稳、具体、有判断、留余地；像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:tone.value | wrap-array | ✓ |
| INT-D03 | facts.brand.tone.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.brand.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:target_customer_summary.value | identity | ✓ |
| INT-D03 | facts.brand.target_customer_summary.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.brand.forbidden_expressions.note | "照抄数据包 §2 包1「禁用表达清单」10 词；与 acceptance/detectors/forbidden… | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand.forbidden_expressions.note | relocate-annotation | ✓ |
| INT-D03 | facts.brand.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| INT-D03 | facts.brand.forbidden_expressions.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.brand.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:commercial_constraints.value | identity | ✓ |
| INT-D03 | facts.brand.commercial_constraints.source | "模拟" | fixtures/facts/brand/FS-BRAND-INTD03-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.persona.value | null | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.value | relocate-annotation | ✓ |
| INT-D03 | facts.persona.status | "MISSING" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.status | relocate-annotation | ✓ |
| INT-D03 | facts.persona.source | "故意缺失（夹具设计）" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.source | relocate-annotation | ✓ |
| INT-D03 | facts.persona.note | "B.4.1/INT-D03 未要求人设事实；数据包 §5 包4 存在但本快照未带入，如实登记为缺失，禁补" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.persona.note | relocate-annotation | ✓ |
| INT-D03 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:product_id | identity-plain | ✓ |
| INT-D03 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:name.value | identity | ✓ |
| INT-D03 | facts.product.name.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:category.value | identity | ✓ |
| INT-D03 | facts.product.category.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.sku.value | "1G9971081" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:sku.value | identity | ✓ |
| INT-D03 | facts.product.sku.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:sku.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.price.raw_text | "3980元" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.raw_text | relocate-annotation | ✓ |
| INT-D03 | facts.product.price.original_as_of | "2026-08-17" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| INT-D03 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| INT-D03 | facts.product.price.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:material.value | identity | ✓ |
| INT-D03 | facts.product.material.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.lining | {"value": null, "status": "MISSING", "source": "截图 IMG_06… | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| INT-D03 | facts.product.style_attributes.value | ["大翻领、廓形肩线、H型风衣式；袖口可调节袖袢；宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:style_attributes.value | wrap-array | ✓ |
| INT-D03 | facts.product.style_attributes.source | "截图 IMG_0674、截图 IMG_0677、截图 IMG_0680" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式；提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:selling_points.value | wrap-array | ✓ |
| INT-D03 | facts.product.selling_points.source | "截图 IMG_0677、截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:size_range.value | identity | ✓ |
| INT-D03 | facts.product.size_range.source | "截图 IMG_0684" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| INT-D03 | facts.product.lifecycle_stage.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| INT-D03 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| INT-D03 | facts.product.inventory.source | "夹具虚构（剧本）" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| INT-D03 | facts.product.image_refs.source | "截图 IMG_0672、截图 IMG_0684" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| INT-D03 | facts.product.image_refs.value | "IMG_0672、IMG_0675—IMG_0682、IMG_0683、IMG_0684；共享图同时关联 P12" | fixtures/facts/product/FS-PRODUCT-INTD03-P13.v1.json:image_refs[0].locator | imagetext-to-sourceref | ✓ |
| INT-D03 | facts.video_account.value | null | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.value | relocate-annotation | ✓ |
| INT-D03 | facts.video_account.status | "MISSING" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.status | relocate-annotation | ✓ |
| INT-D03 | facts.video_account.source | "故意缺失（夹具设计）" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.source | relocate-annotation | ✓ |
| INT-D03 | facts.video_account.note | "B.4.1/INT-D03 未要求账号事实；数据包 §6 包5 存在但本快照未带入，如实登记为缺失，禁补" | cases/INT-D03/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account.note | relocate-annotation | ✓ |
| SYS-D01 | snapshot_id | "SNAP-SYSD01-0001" | cases/SYS-D01/fixtures/context_snapshot.json:snapshot_id | identity | ✓ |
| SYS-D01 | brand_id | "fixture-brand-01" | cases/SYS-D01/fixtures/context_snapshot.json:brand_id | identity | ✓ |
| SYS-D01 | facts.time_window | {"value": "六周", "source": "Founder 2026-08-17 IA-0 裁决：六周（… | cases/SYS-D01/fixtures/task_input.json:_migrated_from_snapshot.SYS-D01.time_window | relocate-task-input | ✓ |
| SYS-D01 | facts.audience_facts[0].audience_id | "A01" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:audience_id | identity-plain | ✓ |
| SYS-D01 | facts.audience_facts[0].label.value | "稳态通勤者" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:label.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[0].label.source | "数据包 包3 A01【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:label.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[0].age_range.original_range_text | "33—42 岁" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience_facts[0].age_range.original_range_text | relocate-annotation | ✓ |
| SYS-D01 | facts.audience_facts[0].age_range.value | {"min": 33, "max": 42, "unit": "岁"} | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:age_range.value | range-parse | ✓ |
| SYS-D01 | facts.audience_facts[0].age_range.source | "数据包 包3 A01【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:age_range.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[0].occupation_or_lifestyle.value | ["品牌、咨询、教育、行政管理或专业服务岗位；工作日需要见同事和客户，下班后常直接接孩子、赴家宴或处理家庭事务；衣… | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:occupation_or_lifestyle.value | wrap-array | ✓ |
| SYS-D01 | facts.audience_facts[0].occupation_or_lifestyle.source | "数据包 包3 A01【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:occupation_or_lifestyle.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[0].pain_points.value | ["上午会议要有边界感，晚上接孩子又不想显得过度正式，硬挺西装常在第二个场景里变得突兀", "通勤单程 40—60… | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:pain_points.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[0].pain_points.source | "数据包 包3 A01 真实痛点【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:pain_points.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[0].purchase_reasons.value | ["版型能同时处理会议、通勤、接送和周末轻社交", "品牌明确解释面料、里料、尺码和长期穿着代价", "一件外套能… | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:purchase_reasons.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[0].purchase_reasons.source | "数据包 包3 A01 购买理由【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:purchase_reasons.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[0].objections.value | ["羊毛、亚麻或混纺面料是否难打理，真实使用频率会不会低", "宽松版型是否只是模特图成立，自己久坐或含胸时会不会… | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:objections.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[0].objections.source | "数据包 包3 A01 常见顾虑【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A01.v1.json:objections.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[1].audience_id | "A02" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:audience_id | identity-plain | ✓ |
| SYS-D01 | facts.audience_facts[1].label.value | "克制表达者" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:label.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[1].label.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:label.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[1].age_range.original_range_text | "26—32 岁" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.audience_facts[1].age_range.original_range_text | relocate-annotation | ✓ |
| SYS-D01 | facts.audience_facts[1].age_range.value | {"min": 26, "max": 32, "unit": "岁"} | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:age_range.value | range-parse | ✓ |
| SYS-D01 | facts.audience_facts[1].age_range.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:age_range.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[1].occupation_or_lifestyle.value | ["新消费、电商、设计、内容、互联网运营或自由职业；工作环境着装弹性大，会拍短视频和日常照片，但不希望整个人像在追… | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:occupation_or_lifestyle.value | wrap-array | ✓ |
| SYS-D01 | facts.audience_facts[1].occupation_or_lifestyle.source | "数据包 包3 A02【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:occupation_or_lifestyle.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[1].pain_points.value | ["衣柜以黑、白、灰、牛仔为主，想加入荧光色或印花，却担心只能拍一次照片、无法进入日常", "对“显瘦模板”疲劳，… | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:pain_points.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[1].pain_points.source | "数据包 包3 A02 真实痛点【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:pain_points.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[1].purchase_reasons.value | ["品牌把反常识单品放进真实上班、通勤和周末场景验证", "买手能给出“这一件负责表达，其余单品负责安定”的具体搭… | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:purchase_reasons.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[1].purchase_reasons.source | "数据包 包3 A02 购买理由【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:purchase_reasons.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.audience_facts[1].objections.value | ["荧光色、腰果花等强视觉元素会不会很快厌倦", "修身针织或高腰裤在活动、进食和久坐时是否仍然舒服", "视频中… | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:objections.value | identity | ✓ |
| SYS-D01 | facts.audience_facts[1].objections.source | "数据包 包3 A02 常见顾虑【模拟】" | fixtures/facts/audience/FS-AUD-SYSD01-A02.v1.json:objections.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.brand_id | "fixture-brand-01" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:brand_id | identity-plain | ✓ |
| SYS-D01 | facts.brand_facts.brand_name.value | "衡叙集（虚构）" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:brand_name.value | identity | ✓ |
| SYS-D01 | facts.brand_facts.brand_name.source | "数据包 包1【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:brand_name.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.positioning_statement.value | "服务 30—45 岁、需要在工作与日常之间切换的城市女性；中高端日常女装，主做有结构但不过度强势的外套、裤装、针… | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:positioning.value | identity | ✓ |
| SYS-D01 | facts.brand_facts.positioning_statement.source | "数据包 包1 一句话定位【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.values.value | ["先讲商品解决什么、牺牲什么，再谈是否值得买", "一件衣服应能进入真实生活，并在不同场景中被反复使用", "尊… | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:values.value | identity | ✓ |
| SYS-D01 | facts.brand_facts.values.source | "数据包 包1 价值主张【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:values.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.tone.value | ["稳、具体、有判断、留余地；像一位长期做商品和门店的人对熟客解释选择，不喊口号，不催促成交"] | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:tone.value | wrap-array | ✓ |
| SYS-D01 | facts.brand_facts.tone.source | "数据包 包1 说话调性【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:tone.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.target_customer_summary.value | "她愿意为版型、面料与长期使用付合理溢价，但要求品牌把依据和不适合之处说清楚" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:target_customer_summary.value | identity | ✓ |
| SYS-D01 | facts.brand_facts.target_customer_summary.source | "数据包 包1 目标客户一句话【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:target_customer_summary.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.forbidden_expressions.note | "运营真源以 acceptance/detectors/forbidden_lexicon.yaml 为唯一真源（… | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand_facts.forbidden_expressions.note | relocate-annotation | ✓ |
| SYS-D01 | facts.brand_facts.forbidden_expressions.value | ["清仓", "甩卖", "白菜价", "闭眼入", "全网最低", "不买就亏", "秒杀", "绝绝子", "… | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:forbidden_expressions.value | identity | ✓ |
| SYS-D01 | facts.brand_facts.forbidden_expressions.source | "数据包 包1 禁用表达清单【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:forbidden_expressions.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_facts.commercial_constraints.value | ["公开成交价原则上不得低于吊牌价 8 折；例外必须有书面授权、起止时间和适用库存", "同一款出现两个价格且无法… | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:commercial_constraints.value | identity | ✓ |
| SYS-D01 | facts.brand_facts.commercial_constraints.source | "数据包 包1 商业硬约束【模拟】" | fixtures/facts/brand/FS-BRAND-SYSD01-0001.v1.json:commercial_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[0].persona_id | "R01" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:persona_id | identity-plain | ✓ |
| SYS-D01 | facts.persona_facts[0].identity.value | "衡叙集虚构品牌主理人，44 岁；负责商品取舍、定价边界和门店反馈复盘" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:identity.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[0].identity.source | "数据包 包4 R01【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:identity.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[0].voice_traits.value | ["句子不快，先把问题和条件说清，再给判断；常用门店试穿、退换原因、面料取舍和一件衣服穿了多久来举例；很少直接下购… | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:voice_traits.value | wrap-array | ✓ |
| SYS-D01 | facts.persona_facts[0].voice_traits.source | "数据包 包4 R01 说话风格【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:voice_traits.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[0].beliefs.value | ["“衣服先要进入生活，才有资格谈风格。”", "“不适合你的商品，说清楚比卖出去更重要。”", "“价格要能回到… | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:beliefs.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[0].beliefs.source | "数据包 包4 R01 公开表达过的信念【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:beliefs.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[0].audience_relationship.value | "把观众视为长期熟客和共同判断者；允许观众带着不同体型、预算和生活阶段反驳她，不用“教育消费者”的姿态压过真实反馈" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:audience_relationship.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[0].audience_relationship.source | "数据包 包4 R01 与粉丝关系【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[0].forbidden_styles.value | ["“姐妹们冲”", "“闭眼买”", "“谁穿谁好看”", "“全网最低”", "“错过后悔”"] | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:forbidden_styles.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[0].forbidden_styles.source | "数据包 包4 R01 绝不使用的表达【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:forbidden_styles.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[0].speaker_constraints.value | ["不做高频叫卖直播；不在无法核对款号、价格、成分时讲商品结论；每条视频最多讲一个核心判断；避免过度磨皮和改变服装… | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:speaker_constraints.value | wrap-array | ✓ |
| SYS-D01 | facts.persona_facts[0].speaker_constraints.source | "数据包 包4 R01 出镜限制【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R01.v1.json:speaker_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[1].persona_id | "R02" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:persona_id | identity-plain | ✓ |
| SYS-D01 | facts.persona_facts[1].identity.value | "衡叙集虚构年轻买手，28 岁；负责新款试穿、颜色与比例实验、年轻客群反馈和一衣多搭验证" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:identity.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[1].identity.source | "数据包 包4 R02【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:identity.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[1].voice_traits.value | ["节奏比主理人快，先给镜前结论，再用三个动作或三套搭配验证；常以“我原本也觉得不日常”“换掉哪一件就成立”开场，… | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:voice_traits.value | wrap-array | ✓ |
| SYS-D01 | facts.persona_facts[1].voice_traits.source | "数据包 包4 R02 说话风格【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:voice_traits.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[1].beliefs.value | ["“鲜明不等于难穿，关键是整套里只能有一个人负责说话。”", "“试穿不是证明它好，而是找到它在哪个条件下不成立… | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:beliefs.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[1].beliefs.source | "数据包 包4 R02 公开表达过的信念【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:beliefs.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[1].audience_relationship.value | "像替观众先试错的同龄同事；会展示犹豫、失败搭配和调整过程，以现场比较建立信任，不把自己放在审美裁判位置" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:audience_relationship.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[1].audience_relationship.source | "数据包 包4 R02 与粉丝关系【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[1].forbidden_styles.value | ["“你不懂时尚”", "“普通人驾驭不了”", "“必须拥有”", "“纯欲”", "“辣妹必备”"] | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:forbidden_styles.value | identity | ✓ |
| SYS-D01 | facts.persona_facts[1].forbidden_styles.source | "数据包 包4 R02 绝不使用的表达【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:forbidden_styles.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.persona_facts[1].speaker_constraints.value | ["试穿必须保留自然走动、坐下、抬手和侧面镜头；不得只拍正面定格；颜色判断不得使用重滤镜；不替主理人宣布价格政策或… | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:speaker_constraints.value | wrap-array | ✓ |
| SYS-D01 | facts.persona_facts[1].speaker_constraints.source | "数据包 包4 R02 出镜限制【模拟】" | fixtures/facts/persona/FS-PERSONA-SYSD01-R02.v1.json:speaker_constraints.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.product_id | "P13" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:product_id | identity-plain | ✓ |
| SYS-D01 | facts.product.name.value | "10%羊绒风衣式大衣" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:name.value | identity | ✓ |
| SYS-D01 | facts.product.name.source | "数据包 P13 商品名【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:name.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.category.value | "10羊绒版" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:category.value | identity | ✓ |
| SYS-D01 | facts.product.category.source | "截图 IMG_0684（原文照抄，未规范化）" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:category.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.price.verbatim | "截图原文“3980元”" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.verbatim | relocate-annotation | ✓ |
| SYS-D01 | facts.product.price.original_as_of | "2026-08-17" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.price.original_as_of | relocate-annotation | ✓ |
| SYS-D01 | facts.product.price.value | {"amount": 3980, "currency": "CNY", "as_of": "2026-08-17T… | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:price.value | money-envelope+asof-normalize | ✓ |
| SYS-D01 | facts.product.price.source | "截图 IMG_0684；价格事实有效日统一记为 2026-08-17【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:price.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.style_number | {"value": "1G9971081", "source": "截图 IMG_0684"} | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.style_number.. | relocate-annotation | ✓ |
| SYS-D01 | facts.product.material.value | ["黑色面料:90.2%绵羊毛 9.8%山羊绒（含微量其他纤维）（连接线除外）", "米色面料:90.3%绵羊毛 … | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:material.value | identity | ✓ |
| SYS-D01 | facts.product.material.source | "截图 IMG_0684（四色成分原文全录，一字不改）" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:material.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.lining | {"value": "缺失", "source": "截图 IMG_0684（截图未出现；故意缺失，按夹具纪律不补… | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.lining.. | relocate-annotation | ✓ |
| SYS-D01 | facts.product.style_attributes.value | ["大翻领、廓形肩线、H型风衣式；袖口可调节袖袢；宽边长腰带"] | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:style_attributes.value | wrap-array | ✓ |
| SYS-D01 | facts.product.style_attributes.source | "截图 IMG_0674、IMG_0677、IMG_0680" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:style_attributes.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.selling_points.value | ["同页展示敞开穿与收腰穿两种方式；提供黑色、米色、晓雾灰、云烟灰四种面料成分"] | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:selling_points.value | wrap-array | ✓ |
| SYS-D01 | facts.product.selling_points.source | "截图 IMG_0677、IMG_0684" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:selling_points.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.size_range.value | ["150/76A/XS", "155/80A/S", "160/84A/M", "165/88A/L", "17… | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:size_range.value | identity | ✓ |
| SYS-D01 | facts.product.size_range.source | "截图 IMG_0684（号型原文照抄）" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:size_range.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.lifecycle_stage.value | "库存消化期" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:lifecycle_stage.value | identity | ✓ |
| SYS-D01 | facts.product.lifecycle_stage.source | "数据包 P13【虚构-剧本】" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:lifecycle_stage.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.inventory.unit | "件" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:inventory.value.unit | quantity-envelope | ✓ |
| SYS-D01 | facts.product.inventory.value | {"value": 800, "unit": "件", "as_of": "2026-08-17T00:00:00… | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:inventory.value | quantity-envelope+asof-fill-const | ✓ |
| SYS-D01 | facts.product.inventory.source | "数据包 P13【虚构-剧本】；与 B.5.1/E2E-01 冻结的库存数一致（随 SNAP-E2E01-0001… | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:inventory.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.product.image_refs.source | "截图 IMG_0672、截图 IMG_0684" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.product.image_refs.source | relocate-annotation | ✓ |
| SYS-D01 | facts.product.image_refs.value | "IMG_0672、IMG_0675—IMG_0682、IMG_0683、IMG_0684；共享图同时关联 P12" | fixtures/facts/product/FS-PRODUCT-SYSD01-P13.v1.json:image_refs[0].locator | imagetext-to-sourceref | ✓ |
| SYS-D01 | facts.video_account_facts.account_id.source | "Founder 2026-08-17 IA-0 裁决：虚构编号（OQ-BUILD-13）" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.account_id.source | relocate-annotation | ✓ |
| SYS-D01 | facts.video_account_facts.account_id.value | "ACC-HXJ-001" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:account_id | identity-plain | ✓ |
| SYS-D01 | facts.video_account_facts.platform.source | "A.3.6（platform 系统固定 WECHAT_VIDEO）+ 数据包 包5 视频号账号事实" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.platform.source | relocate-annotation | ✓ |
| SYS-D01 | facts.video_account_facts.platform.value | "WECHAT_VIDEO" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:platform | identity-plain | ✓ |
| SYS-D01 | facts.video_account_facts.account_name.value | "衡叙集·穿衣判断（虚构）" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:account_name.value | identity | ✓ |
| SYS-D01 | facts.video_account_facts.account_name.source | "数据包 包5【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:account_name.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.video_account_facts.positioning.value | "面向城市女性的服装选择与真实穿着决策账号：以商品事实、场景试穿和明确取舍，回答“为什么选、怎么穿、何时不选”" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:positioning.value | identity | ✓ |
| SYS-D01 | facts.video_account_facts.positioning.source | "数据包 包5 定位【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:positioning.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.video_account_facts.content_style.value | ["稳口吻、熟关系、低剪辑刺激；以一件商品或一个穿衣问题为单集单位，画面保留面料近景、正侧背面、动作和必要的事实卡… | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:content_style.value | wrap-array | ✓ |
| SYS-D01 | facts.video_account_facts.content_style.source | "数据包 包5 内容风格【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:content_style.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.video_account_facts.audience_relationship.value | "不是销售话术广播站，而是长期衣橱判断伙伴；欢迎观众提交通勤、久坐、身形变化、颜色尝试和门店试穿问题，并允许后续视… | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:audience_relationship.value | identity | ✓ |
| SYS-D01 | facts.video_account_facts.audience_relationship.source | "数据包 包5 与观众关系【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:audience_relationship.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.video_account_facts.primary_persona_ref.source | "数据包 包5 主出镜人「沈岚，关联 R01 品牌主理人」【模拟】" | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.video_account_facts.primary_persona_ref.source | relocate-annotation | ✓ |
| SYS-D01 | facts.video_account_facts.primary_persona_ref.value | "R01" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:primary_persona_ref.object_id | personaid-to-versionedref:FS-PERSONA-SYSD01-R01 | ✓ |
| SYS-D01 | facts.video_account_facts.expression_boundaries.value | ["未核对款号、成分、尺码、价格和库存时不得下商品结论", "价格冲突必须同时展示并标记“待裁决”，不得选择性隐藏… | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:expression_boundaries.value | identity | ✓ |
| SYS-D01 | facts.video_account_facts.expression_boundaries.source | "数据包 包5 表达边界【模拟】" | fixtures/facts/video_account/FS-VIDEOACCOUNT-SYSD01-0001.v1.json:expression_boundaries.source_refs[0].locator | sourceref-derive | ✓ |
| SYS-D01 | facts.brand_positioning | {"value": "HIGH_END", "source": "随 SNAP-E2E01-0001 同源复用带入… | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.brand_positioning.. | relocate-annotation | ✓ |
| SYS-D01 | facts.inventory | {"value": 800, "unit": "件", "source": "随 SNAP-E2E01-0001 … | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.facts.inventory.. | relocate-annotation | ✓ |
| SYS-D01 | hard_rules[0].rule_id | "R-BDD01-001" | cases/SYS-D01/fixtures/context_snapshot.json:active_rule_refs[0].object_id | rule-ref:registered@contracts/rules | ✓ |
| SYS-D01 | hard_rules[0] | {"version": 1, "statement": "禁止低价叫卖表达（forbidden_expressio… | cases/SYS-D01/fixtures/context_snapshot.json:_fixture_note.migration.field_annotations.hard_rules[0].. | relocate-annotation | ✓ |
