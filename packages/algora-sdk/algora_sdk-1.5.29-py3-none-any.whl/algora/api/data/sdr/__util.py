from algora.api.data.query.model import TimeseriesQueryRequest


def _commodity_request_info(request: TimeseriesQueryRequest):
    updated_request = request.copy(id="49895def-ee53-4057-8354-8d5ffd735cc1")
    return updated_request
