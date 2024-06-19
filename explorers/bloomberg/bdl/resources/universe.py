from typing import List, Literal, Optional

from pydantic import Field

from explorers.bloomberg.bdl.resources.base import (BDLBaseModel, BDLResourceCollection,
                                                    IssueModifiedMixin, StrEnum)


class SecID(StrEnum):
    AUSTRIAN = "AUSTRIAN"
    ISIN = "ISIN"
    BB_GLOBAL = "BB_GLOBAL"
    BB_UNIQUE = "BB_UNIQUE"
    BELGIUM = "BELGIUM"
    ISRAELI = "ISRAELI"
    CEDEL = "CEDEL"
    ITALY = "ITALY"
    CATS = "CATS"
    CINS = "CINS"
    JAPAN = "JAPAN"
    COMMON_NUMBER = "COMMON_NUMBER"
    CUSIP = "CUSIP"
    LUXEMBOURG = "LUXEMBOURG"
    CZECH = "CZECH"
    SEDOL = "SEDOL"
    IRISH = "IRISH"
    DUTCH = "DUTCH"
    SPAIN = "SPAIN"
    TICKER = "TICKER"
    EUROCLEAR = "EUROCLEAR"
    VALOREN = "VALOREN"
    FRENCH = "FRENCH"
    WPK = "WPK"
    LEGAL_ENTITY_IDENTIFIER = "LEGAL_ENTITY_IDENTIFIER"


class UniverseSummary(BDLBaseModel, IssueModifiedMixin):
    id: str = Field(alias="@id")
    type: Literal['Universe'] = Field(default="Universe", alias="@type")
    title: str
    identifier: str
    description: str


class UniverseCollectionView(BDLResourceCollection):
    type: Literal['UniverseCollection'] = Field(
        default="UniverseCollection", alias="@type")
    contains: List[UniverseSummary]


class FieldOverride(BDLBaseModel):
    type: Literal['FieldOverride'] = Field(
        default="FieldOverride", alias="@type")
    mnemonic: Optional[str] = None
    cleanName: Optional[str] = None
    override: str


class UniverseInputItems(BDLBaseModel):
    type: Literal['Identifier'] = Field(default="Identifier", alias="@type")
    identifierType: SecID
    identifierValue: str
    fieldOverrides: Optional[List[FieldOverride]] = None


class UniverseCreate(BDLBaseModel):
    type: Literal['Universe'] = Field(default="Universe", alias="@type")
    identifier: str
    title: str
    description: Optional[str]
    contains: List[UniverseInputItems]


class UniverseItem(BDLBaseModel):
    type: Literal['Identifier', 'UniverseLookup'] = Field(alias="@type")
    identifierType: SecID
    identifierValue: str
    fieldOverrides: Optional[List[FieldOverride]] = None
    ignoredFieldOverrides: Optional[List[FieldOverride]] = None


class UniversePatch(BDLBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    contains: Optional[List[UniverseInputItems]] = None


class UniverseView(BDLResourceCollection, IssueModifiedMixin):
    type: Literal['Universe'] = Field(default="Universe", alias="@type")
    referencedByActiveRequests: bool
    contains: List[UniverseItem]
    securityOverridesDefined: bool
