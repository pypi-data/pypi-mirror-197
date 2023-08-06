"""
Data classes for API requests.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import Field

from algora.common.base import Base
from algora.common.enum import Order, SqlOperator, BooleanOperator
from algora.common.type import Datetime


class NestedFilter(Base):
    field: str
    operator: SqlOperator
    value: Any
    join_operator: Optional[BooleanOperator] = None
    other: Optional["NestedFilter"] = None


class TimeseriesQueryRequest(Base):
    id: Optional[str] = Field(default=None)
    dataset_name: Optional[str] = Field(default=None)
    reference_name: Optional[str] = Field(default=None)
    date: Optional[Datetime] = Field(default=None)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    as_of: Optional[datetime] = Field(default=None)
    page: Optional[int] = Field(default=None)
    limit: Optional[int] = Field(default=None)
    fields: Optional[List[str]] = Field(default=None)
    sort: Optional[Dict[str, Order]] = Field(default=None)
    where: Optional[NestedFilter] = Field(default=None)


class DistinctQueryRequest(Base):
    id: Optional[str] = Field(default=None)
    dataset_name: Optional[str] = Field(default=None)
    reference_name: Optional[str] = Field(default=None)
    field: str = Field(default=None)
