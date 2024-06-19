from typing import List, Union

from pydantic import Field

from explorers.bloomberg.bdl.resources.base import BDLBaseModel


class Object(BDLBaseModel):
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    title: str
    description: str
    identifier: str


class CatalogMember(BDLBaseModel):
    id: str = Field(alias="@id")
    type: Union[str, List[str]] = Field(alias="@type")
    title: str
    description: str
    identifier: str
    subscriptionType: str


class Catalog(BDLBaseModel):
    id: str = Field(alias="@id")
    type: Union[str, List[str]] = Field(alias="@type")
    title: str
    description: str
    identifier: str
    contains: List[CatalogMember]


class CatalogResources(BDLBaseModel):
    id: str = Field(alias="@id")
    type: Union[str, List[str]] = Field(alias="@type")
    title: str
    description: str
    identifier: str
    contains: List[Object]
    subscriptionType: str
    defaultTimeZoneName: str
