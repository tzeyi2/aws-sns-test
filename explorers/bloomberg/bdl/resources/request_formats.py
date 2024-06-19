from typing import Literal, Optional

from pydantic import Field

from explorers.bloomberg.bdl.resources.base import BDLBaseModel


class OutputFormat(BDLBaseModel):
    fileType: Optional[Literal['unixFileType', 'windowsFileType']] = None


class HistoryFormat(OutputFormat):
    type: Literal['HistoryFormat'] = Field(
        alias="@type", default='HistoryFormat')
    dateFormat: Optional[str] = None


class ActionsFormat(OutputFormat):
    type: Literal['ActionsFormat'] = Field(
        alias="@type", default='ActionsFormat')
    dateFormat: Optional[str] = None


class BvalSnapshotFormat(OutputFormat):
    type: Literal['BvalSnapshotFormat'] = Field(
        alias="@type", default='BvalSnapshotFormat')
    columnHeader: Optional[bool] = True
    dateFormat: Optional[str] = 'mmddyyyy'
    delimiter: Optional[Literal['|', ',', ';']] = None
    outputFormat: Optional[Literal['bulkListOutputFormat',
                                   'fixedOutputFormat', 'variableOutputFormat']] = None


class PricingSnapshotFormat(OutputFormat):
    type: Literal['PricingSnapshotFormat'] = Field(
        alias="@type", default='PricingSnapshotFormat')
    columnHeader: Optional[bool] = True
    delimiter: Optional[Literal['|', ',', ';']] = None


class DataFormat(BDLBaseModel):
    type: Literal['DataFormat'] = Field(alias="@type", default='DataFormat')
    fileType: Optional[Literal['unixFileType',
                               'windowsFileType']] = 'unixFileType'
    columnHeader: Optional[bool] = True
    dateFormat: Optional[str] = 'mmddyyyy'
    delimiter: Optional[Literal['|', ',', ';']] = None
    outputFormat: Optional[Literal['bulkListOutputFormat',
                                   'fixedOutputFormat', 'variableOutputFormat']] = None
    encoding: Optional[Literal['UTF-8', 'ASCII']] = None


class EntityFormat(OutputFormat):
    type: Literal['EntityFormat'] = Field(
        alias="@type", default='EntityFormat')
    columnHeader: Optional[bool] = True
    dateFormat: Optional[str] = 'mmddyyyy'
    delimiter: Optional[Literal['|', ',', ';']] = None
    outputFormat: Optional[Literal['bulkListOutputFormat',
                                   'fixedOutputFormat', 'variableOutputFormat']] = None
