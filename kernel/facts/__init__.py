# -*- coding: utf-8 -*-
"""kernel/facts —— M1-EP01 Facts 纵切（块 E ②，文件级，不建数据库）。

四件套：
  store.py       事实对象存取（VersionedRef → 磁盘 JSON/YAML 对象；同 ID 同版本撞车即错）
  resolve.py     Snapshot 构建/解引用（十四字段引用式 → 消费端内联兼容视图）
  predicates.py  确定性谓词：P1-P3（结构层，自 tools/test_fact_schemas.py 抽出共用）
                 + R1-R5 运行时谓词（块 E ③）
  test_facts_offline.py  离线回归（含负例）

设计边界（不建设清单 PRD 2.5 / C.8 对照）：无数据库、无存储平台、无对话式界面；
一切以仓库内 JSON/YAML 文件为存储介质，谓词全部确定性、零 LLM。
"""
from .store import FactStore, FactResolutionError
from .resolve import materialize_legacy_view, is_reference_shape
from . import predicates

__all__ = ["FactStore", "FactResolutionError", "materialize_legacy_view",
           "is_reference_shape", "predicates"]
