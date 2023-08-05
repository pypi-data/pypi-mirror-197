from typing import Union, Any, TypedDict, Literal, List, Dict
from typing_extensions import Required


class GenericMetric(TypedDict, total=False):
    """generic_metric."""

    version: Literal[2]
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

    tags: Required["_GenericMetricTags"]
    """required"""

    value: Required[Union[int, List[Union[int, float]]]]
    """required"""

    retention_days: Required[int]
    """required"""

    mapping_meta: Required["_GenericMetricMappingMeta"]
    """required"""



_GenericMetricMappingMeta = Dict[str, Any]
"""
patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""



_GenericMetricTags = Dict[str, Any]
"""
patternProperties:
  ^.*$:
    type: string
"""

