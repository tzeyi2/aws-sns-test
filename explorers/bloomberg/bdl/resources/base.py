from datetime import datetime
from enum import Enum
from typing import Dict, Literal, Optional, Any

from pydantic import BaseModel, ConfigDict, Field


class StrEnum(str, Enum):
    def __repr__(self) -> str:
        return str.__repr__(self.value)


class BDLBaseModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    context: Optional[Dict] = Field(alias='@context', default=None)

    def model_dump_json_custom(self) -> Dict[str, Any]:
        """
        Returns a dict of the model where the fields are parsed into JSON compatible strings instead of objects.

        For example: datetime string instead of datetime object
        :return:
        """
        return super().model_dump(by_alias=True, exclude_none=True, mode='json')


class IssueModifiedMixin:
    issued: datetime
    modified: datetime


class PartialCollectionView(BDLBaseModel):
    type: Literal['PartialCollectionView'] = Field(
        alias="@type", default='PartialCollectionView')
    id: str = Field(alias="@id")
    first: str
    last: str
    next: Optional[str] = None
    previous: Optional[str] = None


class BDLResourceCollection(BDLBaseModel):
    id: str = Field(alias="@id")
    title: str
    identifier: str
    description: Optional[str] = None
    totalItems: int
    pageCount: int
    view: PartialCollectionView
