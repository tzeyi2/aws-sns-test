from typing import Generic, Literal, TypeVar

from pydantic import Field

from explorers.bloomberg.bdl.resources.base import BDLBaseModel

TerminalIdentity = TypeVar('TerminalIdentity')


class TerminalIdentityBase(BDLBaseModel, Generic[TerminalIdentity]):
    userNumber: int


class BlpTerminalIdentity(TerminalIdentityBase, Generic[TerminalIdentity]):
    type: Literal['BlpTerminalIdentity'] = Field(
        alias="@type", default="BlpTerminalIdentity")
    serialNumber: int
    workStation: int


class BbaTerminalIdentity(TerminalIdentityBase, Generic[TerminalIdentity]):
    type: Literal['BbaTerminalIdentity'] = Field(
        alias="@type", default="BbaTerminalIdentity")
