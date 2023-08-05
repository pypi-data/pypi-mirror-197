from typing import List, Union, Literal, Dict, Any, TypedDict
from typing_extensions import Required


class Metric(TypedDict, total=False):
    """metric."""

    version: Literal[1]
    use_case_id: Required[str]
    """required"""

    org_id: Required[int]
    """required"""

    project_id: Required[int]
    """required"""

    metric_id: Required[int]
    """required"""

    type: Required[str]
    """required"""

    timestamp: Required[int]
    """required"""

    tags: Required["_MetricTags"]
    """required"""

    value: Required[Union[int, List[Union[int, float]]]]
    """required"""

    retention_days: Required[int]
    """required"""

    mapping_meta: Required["_MetricMappingMeta"]
    """required"""



_MetricMappingMeta = Dict[str, Any]
"""
patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""



_MetricTags = Dict[str, Any]
"""
patternProperties:
  ^[0-9]$:
    type: integer
"""

