from datetime import date, datetime, time
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field, TypeAdapter

from explorers.bloomberg.bdl.resources.base import (BDLBaseModel, BDLResourceCollection,
                                                    IssueModifiedMixin, StrEnum)


class TriggerFrequency(StrEnum):
    Adhoc = "adhoc"
    Once = "once"
    Daily = "daily"
    Weekday = "weekday"
    Weekend = "weekend"
    Weekly = "weekly"
    Monthly = "monthly"


class TriggerSummary(BDLBaseModel):
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    title: str
    description: Optional[str] = None
    identifier: str
    issued: datetime
    modified: datetime


class TriggerCollection(BDLResourceCollection):
    type: Literal['TriggerCollection'] = Field(alias="@type")
    contains: List[TriggerSummary]


class TriggerCreateBase(BDLBaseModel):
    title: str
    description: Optional[str] = None
    identifier: str


class SubmitTriggerCreate(TriggerCreateBase):
    type: Literal['SubmitTrigger'] = Field(
        alias="@type", default='SubmitTrigger')


class ScheduledTriggerCreate(TriggerCreateBase):
    type: Literal['ScheduledTrigger'] = Field(
        alias="@type", default='ScheduledTrigger')
    frequency: TriggerFrequency
    startDate: Optional[date] = None
    startTime: Optional[time] = None


class BvalSnapshotTriggerCreate(TriggerCreateBase):
    type: Literal['BvalSnapshotTrigger'] = Field(
        alias="@type", default='BvalSnapshotTrigger')
    frequency: TriggerFrequency
    snapshotTime: time
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None


class PricingSnapshotTriggerCreate(TriggerCreateBase):
    type: Literal['PricingSnapshotTrigger'] = Field(
        alias="@type", default='PricingSnapshotTrigger')
    frequency: TriggerFrequency
    snapshotTime: time
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None


TriggerCreate = Union[
    SubmitTriggerCreate, ScheduledTriggerCreate, BvalSnapshotTriggerCreate, PricingSnapshotTriggerCreate]


class TriggerGet(BDLBaseModel, IssueModifiedMixin):
    title: str
    description: Optional[str] = None
    identifier: str
    referencedByActiveRequests: bool


class SubmitTriggerGet(TriggerGet):
    id: str = Field(alias="@id")
    type: Literal['SubmitTrigger'] = Field(alias="@type")


class ScheduledTriggerGet(TriggerGet):
    id: str = Field(alias="@id")
    type: Literal['ScheduledTrigger'] = Field(alias="@type")
    frequency: TriggerFrequency
    startDate: Optional[date] = None
    startTime: Optional[time] = None


class BvalSnapshotTriggerGet(TriggerGet):
    id: str = Field(alias="@id")
    type: Literal['BvalSnapshotTrigger'] = Field(alias="@type")
    frequency: TriggerFrequency
    snapshotTime: time
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None


class PricingSnapshotTriggerGet(TriggerGet):
    id: str = Field(alias="@id")
    type: Literal['PricingSnapshotTrigger'] = Field(alias="@type")
    frequency: TriggerFrequency
    snapshotTime: time
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None


class SubmitTriggerPatch(BDLBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[TriggerFrequency] = None
    startDate: Optional[date] = None
    startTime: Optional[time] = None


class ScheduledTriggerPatch(BDLBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[TriggerFrequency] = None
    startDate: Optional[date] = None
    startTime: Optional[time] = None


class BvalSnapshotTriggerPatch(BDLBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[TriggerFrequency] = None
    snapshotTime: Optional[time] = None
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None


class PricingSnapshotTriggerPatch(BDLBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[TriggerFrequency] = None
    snapshotTime: Optional[time] = None
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None


TriggerView = Annotated[
    Union[
        SubmitTriggerGet,
        ScheduledTriggerGet,
        BvalSnapshotTriggerGet,
        PricingSnapshotTriggerGet,
    ],
    Field(discriminator="type"),
]
TriggerAdapterView = TypeAdapter(TriggerView)


class TriggerCollectionView(BDLResourceCollection):
    type: Literal['TriggerCollection'] = Field(
        alias="@type", default='TriggerCollection')
    contains: List[TriggerSummary]
