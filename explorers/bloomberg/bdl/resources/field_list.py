from typing import List, Literal, Optional, Union

from pydantic import Field

from explorers.bloomberg.bdl.resources.base import (BDLBaseModel, BDLResourceCollection,
                                                    IssueModifiedMixin, StrEnum)


class FieldListType(StrEnum):
    DataFieldList = "DataFieldList"
    HistoryFieldList = "HistoryFieldList"
    BvalSnapshotFieldList = "BvalSnapshotFieldList"
    EntityFieldList = "EntityFieldList"


class FieldListInputItemMnemonic(BDLBaseModel):
    mnemonic: str


class FieldListInputItemCleanName(BDLBaseModel):
    cleanName: str


class FieldListInputItemId(BDLBaseModel):
    id: str = Field(serialization_alias="@id")


class FieldListSummary(BDLBaseModel, IssueModifiedMixin):
    id: str = Field(alias="@id")
    type: FieldListType = Field(alias="@type")
    title: str
    description: Optional[str] = None
    identifier: str


class FieldListCollection(BDLResourceCollection):
    type: Literal['FieldListCollection'] = Field(
        alias="@type", default='FieldListCollection')
    contains: List[FieldListSummary]


class FieldListItem(BDLBaseModel):
    id: str = Field(alias="@id")
    identifier: str
    cleanName: str
    title: str
    dlCommercialModelCategory: str
    loadingSpeed: str
    type: str
    mnemonic: str


class FieldListView(BDLResourceCollection, IssueModifiedMixin):
    type: FieldListType = Field(alias="@type")
    referencedByActiveRequests: bool
    contains: List[FieldListItem]


class FieldListCreate(BDLBaseModel):
    title: str
    type: FieldListType = Field(serialization_alias="@type")
    description: Optional[str] = None
    identifier: str
    contains: List[
        Union[
            FieldListInputItemMnemonic,
            FieldListInputItemCleanName,
            FieldListInputItemId,
        ]
    ]


class DataFieldListCreate(FieldListCreate):
    type: Literal['DataFieldList'] = Field(
        serialization_alias="@type", default='DataFieldList')


class HistoryFieldListCreate(FieldListCreate):
    type: Literal['HistoryFieldList'] = Field(
        serialization_alias="@type", default='HistoryFieldList')


class BvalSnapshotFieldListCreate(FieldListCreate):
    type: Literal['BvalSnapshotFieldList'] = Field(
        serialization_alias="@type", default='BvalSnapshotFieldList')


class EntityFieldListCreate(FieldListCreate):
    type: Literal['EntityFieldList'] = Field(
        serialization_alias='@type', default='EntityFieldList')


class FieldListPatch(BDLBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    contains: Optional[List[
        Union[
            FieldListInputItemMnemonic,
            FieldListInputItemCleanName,
            FieldListInputItemId,
        ]
    ]] = None
