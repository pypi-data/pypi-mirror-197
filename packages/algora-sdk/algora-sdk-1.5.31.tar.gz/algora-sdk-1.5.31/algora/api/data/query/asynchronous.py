import pandas as pd
from requests import Response

from algora.api.data.query.__util import (
    _query_timeseries_request_info,
    _query_distinct_fields_request_info,
    _query_dataset_csv_request_info,
)
from algora.api.data.query.model import TimeseriesQueryRequest, DistinctQueryRequest
from algora.common.requests import __async_post_request, __async_get_request


async def async_query_timeseries(request: TimeseriesQueryRequest) -> pd.DataFrame:
    """
    Asynchronously query timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_timeseries_request_info(request)
    return await __async_post_request(**request_info)


async def async_query_dataset_csv(id: str, request: TimeseriesQueryRequest) -> Response:
    """
    Asynchronously query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, request)
    return await __async_get_request(**request_info)


async def async_query_distinct_fields(request: DistinctQueryRequest) -> pd.DataFrame:
    """
    Asynchronously query dataset for distinct values of a specified field.

    Args:
        request (DistinctQueryRequest): Distinct query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_distinct_fields_request_info(request)
    return await __async_post_request(**request_info)
