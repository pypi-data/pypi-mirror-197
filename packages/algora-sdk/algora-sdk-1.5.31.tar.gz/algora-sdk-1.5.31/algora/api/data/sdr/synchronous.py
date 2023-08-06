from algora.api.data.query.model import TimeseriesQueryRequest
from pandas import DataFrame

from algora.api.data.query import query_timeseries
from algora.api.data.sdr.__util import (
    _commodity_request_info,
)
from algora.common.decorators import data_request


@data_request
def commodity(request: TimeseriesQueryRequest):
    """
    Get SDR Commodity dataset.

    Args:
        request (TimeseriesQueryRequest): Dataset timeseries query

    Returns:
        DataFrame: DataFrame
    """
    request = _commodity_request_info(request)
    return query_timeseries(request)
