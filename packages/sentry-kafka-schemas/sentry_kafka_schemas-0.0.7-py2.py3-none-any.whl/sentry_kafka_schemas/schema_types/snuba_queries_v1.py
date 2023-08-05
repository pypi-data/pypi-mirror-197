from typing import Any, Dict, TypedDict, List, Union
from typing_extensions import Required


class ClickhouseQueryProfile(TypedDict, total=False):
    """clickhouse_query_profile."""

    time_range: Required[Union[int, None]]
    """required"""

    table: str
    all_columns: List[str]
    """
    required

    required

    required

    required
    """

    multi_level_condition: Required[bool]
    """required"""

    where_profile: Required["ClickhouseQueryProfileWhereProfile"]
    """required"""

    groupby_cols: Required[List[str]]
    """
    required

    required

    required

    required
    """

    array_join_cols: Required[List[str]]
    """
    required

    required

    required

    required
    """



class ClickhouseQueryProfileWhereProfile(TypedDict, total=False):
    """clickhouse_query_profile_where_profile."""

    columns: Required[List[str]]
    """
    required

    required

    required

    required
    """

    mapping_cols: Required[List[str]]
    """
    required

    required

    required

    required
    """



class QueryMetadata(TypedDict, total=False):
    """query_metadata."""

    sql: Required[str]
    """required"""

    sql_anonymized: Required[str]
    """required"""

    start_timestamp: Required[Union[int, None]]
    """required"""

    end_timestamp: Required[Union[int, None]]
    """required"""

    stats: Required[Dict[str, Any]]
    """required"""

    status: Required[str]
    """required"""

    trace_id: Required[Union[str, None]]
    """required"""

    profile: Required["ClickhouseQueryProfile"]
    """required"""

    result_profile: Required[Union[Dict[str, Any], None]]
    """required"""

    request_status: Required[str]
    """required"""

    slo: Required[str]
    """required"""



class Querylog(TypedDict, total=False):
    """
    querylog.

    Querylog schema
    """

    request: Required["_QuerylogRequest"]
    """required"""

    dataset: Required[str]
    """required"""

    entity: Required[str]
    """required"""

    start_timestamp: Required[Union[int, None]]
    """required"""

    end_timestamp: Required[Union[int, None]]
    """required"""

    status: Required[str]
    """required"""

    projects: Required[List[int]]
    """required"""

    query_list: Required[List["QueryMetadata"]]
    """required"""

    timing: Required["_QuerylogTiming"]
    """required"""

    snql_anonymized: str


class _QuerylogRequest(TypedDict, total=False):
    id: str
    body: Dict[str, Any]
    referrer: str


class _QuerylogTiming(TypedDict, total=False):
    timestamp: int
    duration_ms: int
    marks_ms: Dict[str, Any]
    tags: Dict[str, Any]
