from datetime import date, datetime
from typing import Literal, Optional, Union

from pydantic import Field

from explorers.bloomberg.bdl.resources.base import BDLBaseModel, StrEnum


class IntervalDateRange(BDLBaseModel):
    type: Literal['IntervalDateRange'] = Field(
        alias="@type", default='IntervalDateRange')
    startDate: date
    endDate: date


class DurationDateRange(BDLBaseModel):
    type: Literal['DurationDateRange'] = Field(
        alias="@type", default='DurationDateRange')
    days: int
    futureDays: Optional[int] = None


class Period(StrEnum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    quarterly = "quarterly"
    yearly = "yearly"


class HistoryRuntimeOptions(BDLBaseModel):
    type: Literal['HistoryRuntimeOptions'] = Field(
        alias="@type", default='HistoryRuntimeOptions')
    dateRange: Union[DurationDateRange, IntervalDateRange]
    historyPriceCurrency: str
    period: Period


class ActionsDurationDateRange(BDLBaseModel):
    type: Literal['ActionsDurationDateRange'] = Field(
        alias="@type", default='ActionsDurationDateRange')
    days: Optional[int] = 0


class ActionsRuntimeOptions(BDLBaseModel):
    type: Literal['ActionsRuntimeOptions'] = Field(
        alias="@type", default='ActionsRuntimeOptions')
    dateRange: Optional[Union[IntervalDateRange,
                              ActionsDurationDateRange]] = None
    actionsDate: Literal['both', 'effective', 'entry'] = 'entry'


class PricingSnapshotRuntimeOptions(BDLBaseModel):
    type: Literal['PricingSnapshotRuntimeOptions'] = Field(
        alias="@type", default='PricingSnapshotRuntimeOptions')
    maxEmbargo: Optional[int] = None


class IntervalDateTimeRange(BDLBaseModel):
    type: Literal['IntervalDateTimeRange'] = Field(
        alias="@type", default='IntervalDateTimeRange')
    startDateTime: datetime
    endDateTime: datetime


class TickHistoryRuntimeOptions(BDLBaseModel):
    type: Literal['TickHistoryRuntimeOptions'] = Field(
        alias="@type", default='TickHistoryRuntimeOptions')
    dateTimeRange: Union[IntervalDateRange, IntervalDateTimeRange]
    tickType: Optional[Literal["trades",
                               "quotes", "quotesAndTrades"]] = "trades"
