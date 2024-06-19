from datetime import date, datetime, time
from enum import IntEnum
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field, TypeAdapter

from explorers.bloomberg.bdl.resources.base import (BDLBaseModel, BDLResourceCollection,
                                                    IssueModifiedMixin, StrEnum)
from explorers.bloomberg.bdl.resources.field_list import (FieldListInputItemCleanName,
                                                          FieldListInputItemId,
                                                          FieldListInputItemMnemonic)
from explorers.bloomberg.bdl.resources.request_formats import (ActionsFormat,
                                                               BvalSnapshotFormat,
                                                               DataFormat, EntityFormat,
                                                               HistoryFormat,
                                                               PricingSnapshotFormat)
from explorers.bloomberg.bdl.resources.runtime_options import (
    ActionsRuntimeOptions, HistoryRuntimeOptions,
    PricingSnapshotRuntimeOptions, TickHistoryRuntimeOptions)
from explorers.bloomberg.bdl.resources.terminal_identity import TerminalIdentity
from explorers.bloomberg.bdl.resources.triggers import TriggerFrequency
from explorers.bloomberg.bdl.resources.universe import UniverseInputItems


class RequestUniverse(BDLBaseModel):
    type: Literal['Universe'] = Field(alias="@type", default='Universe')
    contains: List[UniverseInputItems]


class RequestCreate(BDLBaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    universe: Union[RequestUniverse, str]
    terminalIdentity: Optional[TerminalIdentity] = None


class RequestView(RequestCreate, IssueModifiedMixin):
    id: str = Field(alias="@id")
    frequency: TriggerFrequency
    lastRunDateTime: Optional[datetime] = None
    nextRunDateTime: Optional[datetime] = None
    enabled: Optional[bool] = None
    dataset: str


class SecurityRequestType(StrEnum):
    DataRequest = "DataRequest"
    HistoryRequest = "HistoryRequest"
    ActionsRequest = "ActionsRequest"
    BvalSnapshotRequest = "BvalSnapshotRequest"
    PricingSnapshotRequest = "PricingSnapshotRequest"
    TickHistoryRequest = "TickHistoryRequest"
    EntityRequest = "EntityRequest"


class RequestSummary(BDLBaseModel, IssueModifiedMixin):
    id: str = Field(alias="@id")
    type: SecurityRequestType = Field(alias="@type")
    title: str
    identifier: str
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = True
    dataset: str
    universe: str
    fieldList: Optional[str] = None
    trigger: str
    frequency: TriggerFrequency
    lastRunDateTime: Optional[datetime] = None
    nextRunDateTime: Optional[datetime] = None


class RequestCollectionView(BDLResourceCollection):
    type: Literal['RequestCollection'] = Field(
        alias="@type", default='RequestCollection')
    contains: List[RequestSummary]


class RequestCollection(BDLBaseModel):
    id: str = Field(alias="@id")
    type: Literal['RequestCollection'] = Field(alias="@type")
    title: str
    identifier: str
    description: Optional[str] = None
    totalItems: int
    pageCount: int
    contains: List[RequestSummary]


class RequestFieldList(BDLBaseModel):
    contains: List[
        Union[
            FieldListInputItemMnemonic,
            FieldListInputItemCleanName,
            FieldListInputItemId,
        ]
    ]


class RequestDataFieldList(RequestFieldList):
    type: Literal['DataFieldList'] = Field(
        alias="@type", default='DataFieldList')


class RequestHistoryFieldList(RequestFieldList):
    type: Literal['HistoryFieldList'] = Field(
        alias="@type", default='HistoryFieldList')


class RequestBvalSnapshotFieldList(RequestFieldList):
    type: Literal['BvalSnapshotFieldList'] = Field(
        alias="@type", default="BvalSnapshotFieldList")


class RequestEntityFieldList(RequestFieldList):
    type: Literal['EntityFieldList'] = Field(
        alias="@type", default='EntityFieldList')


class RequestScheduledTrigger(BDLBaseModel):
    type: Literal['ScheduledTrigger'] = Field(
        alias="@type", default='ScheduledTrigger')
    frequency: TriggerFrequency
    startDate: Optional[date] = None
    startTime: Optional[time] = None


class RequestSubmitTrigger(BDLBaseModel):
    type: Literal['SubmitTrigger'] = Field(
        alias="@type", default='SubmitTrigger')


class MediaType(BDLBaseModel):
    type: Literal['MediaType'] = Field(alias="@type", default='MediaType')
    outputMediaType: Literal["text/csv", "application/json"]


class MediaTypeWithFieldIdentifier(MediaType):
    fieldIdentifierType: Optional[Literal['cleanName', 'mnemonic']] = None


class TickHistoryMediaTypeFormat(MediaType):
    outputMediaType: Union[Literal[
        "application/x-tar;archive-media-type=gzip-csv",
        "application/x-tar;archive-media-type=parquet",
        "application/zip;archive-media-type=gzip-csv",
        "application/zip;archive-media-type=parquet"
    ]]


class MediaTypeOnlyJson(MediaType):
    outputMediaType: Literal['application/json']


class PricingSourceDetail(BDLBaseModel):
    mnemonic: str


class DataPricingSourceOptions(BDLBaseModel):
    type: Literal['DataPricingSourceOptions'] = Field(
        alias="@type", default='DataPricingSourceOptions')
    prefer: Optional[PricingSourceDetail] = None
    exclusive: Optional[bool]
    skip: Optional[List[PricingSourceDetail]] = None


class HistoryPricingSourceOptions(BDLBaseModel):
    type: Literal['HistoryPricingSourceOptions'] = Field(
        alias="@type", default='HistoryPricingSourceOptions')
    prefer: Optional[PricingSourceDetail]
    exclusive: Optional[bool] = None
    includeSourceInOutput: Optional[bool] = None


class ActionsFilter(BDLBaseModel):
    actionEventTypeMnemonics: List[str]
    actionMnemonics: List[str]


class BvalSnapshotTier(IntEnum):
    Tier_1 = 1
    Tier_2 = 2


class RequestBvalSnapshotTrigger(BDLBaseModel):
    type: Literal['BvalSnapshotTrigger'] = Field(
        alias="@type", default='BvalSnapshotTrigger')
    snapshotTime: time
    snapshotTimeZoneName: str
    snapshotDate: Optional[date]
    frequency: TriggerFrequency


class BvalPricingSourceOptions(BDLBaseModel):
    type: Literal['BvalPricingSourceOptions'] = Field(
        alias="@type", default='BvalPricingSourceOptions')
    pricingSource: Optional[Literal['BVAL', 'BVIC']] = 'BVAL'


class PricingSnapshotPricingSourceOptions(BDLBaseModel):
    type: Literal['PricingSnapshotPricingSourceOptions'] = Field(alias="@type",
                                                                 default='PricingSnapshotPricingSourceOptions')
    prefer: Optional[PricingSourceDetail] = None
    exclusive: Optional[bool] = None


class TickHistoryPricingSourceOptions(BDLBaseModel):
    type: Literal['TickHistoryPricingSourceOptions'] = Field(alias="@type")
    prefer: Optional[PricingSourceDetail] = None
    exclusive: Optional[bool] = None


class RequestPricingSnapshotTrigger(BDLBaseModel):
    type: Literal["PricingSnapshotTrigger"] = Field(
        alias="@type", default='PricingSnapshotTrigger')
    snapshotTime: time
    snapshotTimeZoneName: Optional[str] = None
    snapshotDate: Optional[date] = None
    frequency: TriggerFrequency


class EntityRequest(BaseModel):
    type: Literal['EntityRequest'] = Field(
        alias="@type", default='EntityRequest')
    fieldList: Union[RequestEntityFieldList, str]
    trigger: Union[RequestSubmitTrigger, RequestScheduledTrigger, str]
    formatting: Optional[Union[MediaType, EntityFormat]] = None


class EntityRequestCreate(RequestCreate, EntityRequest):
    pass


class EntityRequestGet(RequestView, EntityRequest):
    pass


class PricingSnapshot(BDLBaseModel):
    type: Literal['PricingSnapshotRequest'] = Field(
        alias="@type", default='PricingSnapshotRequest')
    trigger: Union[RequestPricingSnapshotTrigger, str]
    formatting: Optional[Union[MediaType, PricingSnapshotFormat]] = None
    pricingSourceOptions: Optional[PricingSnapshotPricingSourceOptions] = None
    runtimeOptions: Optional[PricingSnapshotRuntimeOptions] = None


class PricingSnapshotRequestCreate(RequestCreate, PricingSnapshot):
    pass


class PricingSnapshotRequestGet(RequestView, PricingSnapshot):
    pass


class TickHistory(BDLBaseModel):
    type: Literal['TickHistoryRequest'] = Field(
        alias="@type", default='TickHistoryRequest')
    trigger: Union[RequestSubmitTrigger, str]
    formatting: TickHistoryMediaTypeFormat
    pricingSourceOptions: Optional[TickHistoryPricingSourceOptions] = None
    runtimeOptions: Optional[TickHistoryRuntimeOptions] = None


class TickHistoryRequestCreate(RequestCreate, TickHistory):
    pass


class TickHistoryRequestGet(RequestView, TickHistory):
    pass


class DataRequest(BDLBaseModel):
    type: Literal['DataRequest'] = Field(alias="@type", default='DataRequest')
    fieldList: Union[RequestDataFieldList, str]
    trigger: Union[RequestScheduledTrigger, RequestSubmitTrigger, str]
    formatting: Optional[Union[MediaTypeWithFieldIdentifier,
                               DataFormat]] = None
    pricingSourceOptions: Optional[DataPricingSourceOptions] = None


class DataRequestCreate(RequestCreate, DataRequest):
    pass


class DataRequestGet(RequestView, DataRequest):
    pass


class HistoryRequest(BDLBaseModel):
    type: Literal['HistoryRequest'] = Field(
        alias="@type", default='HistoryRequest')
    fieldList: Union[RequestHistoryFieldList, str]
    trigger: Union[RequestScheduledTrigger, RequestSubmitTrigger, str]
    runtimeOptions: Optional[HistoryRuntimeOptions] = None
    formatting: Optional[Union[MediaType, HistoryFormat]] = None
    pricingSourceOptions: Optional[HistoryPricingSourceOptions] = None


class HistoryRequestCreate(RequestCreate, HistoryRequest):
    pass


class HistoryRequestGet(RequestView, HistoryRequest):
    pass


class ActionsRequest(BDLBaseModel):
    type: Literal['ActionsRequest'] = Field(
        alias="@type", default='ActionsRequest')
    actionsFilter: Optional[ActionsFilter] = None
    trigger: Union[RequestScheduledTrigger, RequestSubmitTrigger, str]
    runtimeOptions: Optional[ActionsRuntimeOptions] = None
    formatting: Optional[Union[MediaTypeOnlyJson, ActionsFormat]] = None


class ActionsRequestCreate(RequestCreate, ActionsRequest):
    pass


class ActionsRequestGet(RequestView, ActionsRequest):
    pass


class BvalSnapshot(BaseModel):
    type: Literal['BvalSnapshotRequest'] = Field(
        alias="@type", default='BvalSnapshotRequest')
    fieldList: Union[RequestBvalSnapshotFieldList, str]
    trigger: Union[RequestBvalSnapshotTrigger, str]
    formatting: Optional[Union[MediaTypeWithFieldIdentifier,
                               BvalSnapshotFormat]] = None
    snapshotTier: BvalSnapshotTier
    pricingSourceOptions: Optional[BvalPricingSourceOptions] = None


class BvalSnapshotRequestCreate(RequestCreate, BvalSnapshot):
    pass


class BvalSnapshotRequestGet(RequestView, BvalSnapshot):
    pass


class SecurityRequestPatch(BDLBaseModel):
    # This is a common class as all universe patch details are shared
    title: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    universe: Optional[Union[RequestUniverse, str]] = None


SecurityRequestView = Annotated[
    Union[
        DataRequestGet,
        HistoryRequestGet,
        ActionsRequestGet,
        BvalSnapshotRequestGet,
        PricingSnapshotRequestGet,
        TickHistoryRequestGet,
        EntityRequestGet
    ],
    Field(discriminator="type"),
]
SecurityRequestViewAdapter = TypeAdapter(SecurityRequestView)
SecurityRequestCreate = Union[
    DataRequestCreate,
    HistoryRequestCreate,
    ActionsRequestCreate,
    BvalSnapshotRequestCreate,
    PricingSnapshotRequestCreate,
    TickHistoryRequestCreate,
    EntityRequestCreate
]
