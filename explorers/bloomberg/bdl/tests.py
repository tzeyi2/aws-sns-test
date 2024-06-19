import datetime
from datetime import date, time, timezone
from unittest.mock import patch

import requests
from django.test import SimpleTestCase
from requests import Response, Session

from explorers.bloomberg.bdl.bdl_api_client import BDLClient
from explorers.bloomberg.bdl.resources.field_list import (DataFieldListCreate,
                                                          FieldListCollection,
                                                          FieldListCreate,
                                                          FieldListInputItemCleanName,
                                                          FieldListInputItemId,
                                                          FieldListInputItemMnemonic,
                                                          FieldListPatch, FieldListType,
                                                          FieldListView)
from explorers.bloomberg.bdl.resources.request_formats import (ActionsFormat,
                                                               BvalSnapshotFormat,
                                                               DataFormat, HistoryFormat,
                                                               PricingSnapshotFormat)
from explorers.bloomberg.bdl.resources.runtime_options import (
    ActionsDurationDateRange, ActionsRuntimeOptions, DurationDateRange,
    HistoryRuntimeOptions, IntervalDateTimeRange, Period,
    PricingSnapshotRuntimeOptions, TickHistoryRuntimeOptions)
from explorers.bloomberg.bdl.resources.security_request import (
    ActionsFilter, ActionsRequestCreate, ActionsRequestGet,
    BvalPricingSourceOptions, BvalSnapshotRequestCreate,
    BvalSnapshotRequestGet, BvalSnapshotTier, DataPricingSourceOptions,
    DataRequestCreate, DataRequestGet, EntityRequestCreate, EntityRequestGet,
    HistoryPricingSourceOptions, HistoryRequestCreate, HistoryRequestGet,
    PricingSnapshotPricingSourceOptions, PricingSnapshotRequestCreate,
    PricingSnapshotRequestGet, PricingSourceDetail,
    RequestBvalSnapshotFieldList, RequestBvalSnapshotTrigger,
    RequestCollectionView, RequestDataFieldList, RequestEntityFieldList,
    RequestHistoryFieldList, RequestPricingSnapshotTrigger,
    RequestScheduledTrigger, RequestSubmitTrigger, RequestUniverse,
    TickHistoryMediaTypeFormat, TickHistoryRequestCreate,
    TickHistoryRequestGet)
from explorers.bloomberg.bdl.resources.terminal_identity import BlpTerminalIdentity
from explorers.bloomberg.bdl.resources.triggers import (BvalSnapshotTriggerCreate,
                                                        BvalSnapshotTriggerGet,
                                                        PricingSnapshotTriggerCreate,
                                                        PricingSnapshotTriggerGet,
                                                        ScheduledTriggerCreate,
                                                        ScheduledTriggerGet,
                                                        SubmitTriggerCreate,
                                                        SubmitTriggerGet,
                                                        TriggerCollection,
                                                        TriggerFrequency)
from explorers.bloomberg.bdl.resources.universe import (FieldOverride, SecID,
                                                        UniverseCollectionView,
                                                        UniverseInputItems)


def get_200_response(payload) -> Response:
    r = requests.Response()
    r.status_code = 200
    r.json = lambda: payload
    return r


# Create your tests here.
class TestBDLResource(SimpleTestCase):
    def setUp(self):
        self.client = BDLClient(
            session=requests.Session(), host="http://test/")
        self.maxDiff = None

    @patch.object(Session, 'request')
    def test_get_submit_trigger(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/triggers/oneshot/"
            },
            "@id": "",
            "@type": "SubmitTrigger",
            "title": "Instant Trigger",
            "description": "Submit trigger to schedule request instantly",
            "identifier": "oneshot",
            "referencedByActiveRequests": False,
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_trigger(
            catalog_id='', trigger_identifier='')
        self.assertEqual(type(response), SubmitTriggerGet)

    @patch.object(Session, 'request')
    def test_get_scheduled_trigger(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/triggers/dailyMorning/"
            },
            "@id": "",
            "@type": "ScheduledTrigger",
            "title": "Daily Morning Trigger",
            "description": "Schedule based trigger for prior day end-of-day data",
            "identifier": "dailyMorning",
            "referencedByActiveRequests": True,
            "frequency": "weekday",
            "startDate": "2018-03-05",
            "startTime": "04:00:00",
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z"
        }
        mock_response.return_value = get_200_response(payload)
        response = self.client.get_trigger(
            catalog_id='', trigger_identifier='')
        self.assertEqual(type(response), ScheduledTriggerGet)

    @patch.object(Session, 'request')
    def test_get_bval_snapshot_trigger(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/triggers/dailyBvalNY4PM/"
            },
            "@id": "",
            "@type": "BvalSnapshotTrigger",
            "identifier": "dailyBvalNY4PM",
            "title": "Daily BVAL NY4PM snapshot",
            "description": "Daily job for the New York 4PM BVAL snapshot",
            "snapshotTime": "16:00:00",
            "snapshotTimeZoneName": "America/New_York",
            "snapshotDate": "2020-10-22",
            "frequency": "daily",
            "referencedByActiveRequests": True,
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z"
        }
        mock_response.return_value = get_200_response(payload)
        response = self.client.get_trigger(
            catalog_id='', trigger_identifier='')
        self.assertEqual(type(response), BvalSnapshotTriggerGet)

    @patch.object(Session, 'request')
    def test_get_pricing_snapshot_trigger(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/triggers/dailySnap4PM/"
            },
            "@id": "",
            "@type": "PricingSnapshotTrigger",
            "identifier": "dailySnap4PM",
            "title": "Daily 4PM snapshot",
            "description": "Daily job for the 4PM snapshot",
            "snapshotTime": "16:00:00",
            "snapshotTimeZoneName": "Europe/London",
            "snapshotDate": "2021-02-11",
            "frequency": "daily",
            "referencedByActiveRequests": True,
            "issued": "2021-02-11T18:43:26.000000Z",
            "modified": "2021-02-11T18:44:27.000000Z"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_trigger(
            catalog_id='', trigger_identifier='')
        self.assertEqual(type(response), PricingSnapshotTriggerGet)

    def test_create_submit_trigger(self):
        trigger = SubmitTriggerCreate(
            title="Early Morning Daily",
            identifier="dailyMorning",
            description="First run of daily data jobs",
        )

        payload = {
            "@type": "SubmitTrigger",
            "identifier": "dailyMorning",
            "title": "Early Morning Daily",
            "description": "First run of daily data jobs"
        }

        self.assertDictEqual(trigger.model_dump_json_custom(), payload)

    def test_create_scheduled_trigger(self):
        trigger = ScheduledTriggerCreate(
            title="Early Morning Daily",
            identifier="dailyMorning",
            description="First run of daily data jobs",
            frequency=TriggerFrequency.Once,
            startDate=date(year=2019, month=8, day=24),
            startTime=time(hour=14, minute=15, second=22, tzinfo=timezone.utc),
        )

        payload = {
            "@type": "ScheduledTrigger",
            "identifier": "dailyMorning",
            "title": "Early Morning Daily",
            "description": "First run of daily data jobs",
            "frequency": "once",
            "startDate": "2019-08-24",
            "startTime": "14:15:22Z"
        }

        self.assertDictEqual(trigger.model_dump_json_custom(), payload)

    def test_create_bval_trigger(self):
        trigger = BvalSnapshotTriggerCreate(
            title="Daily BVAL NY4PM snapshot",
            identifier="dailyBvalNY4PM",
            description="Daily job for the New York 4PM BVAL snapshot",
            frequency=TriggerFrequency.Once,
            snapshotDate=date(year=2019, month=8, day=24),
            snapshotTime=time(hour=14, minute=15, second=22,
                              tzinfo=timezone.utc),
            snapshotTimeZoneName="string",
        )

        payload = {
            "@type": "BvalSnapshotTrigger",
            "identifier": "dailyBvalNY4PM",
            "title": "Daily BVAL NY4PM snapshot",
            "description": "Daily job for the New York 4PM BVAL snapshot",
            "snapshotTime": "14:15:22Z",
            "snapshotTimeZoneName": "string",
            "snapshotDate": "2019-08-24",
            "frequency": "once"
        }

        self.assertDictEqual(trigger.model_dump_json_custom(), payload)

    def test_create_pricing_trigger(self):
        trigger = PricingSnapshotTriggerCreate(
            title="Daily 4PM snapshot",
            identifier="dailySnap4PM",
            description="Daily job for the 4PM snapshot",
            frequency=TriggerFrequency.Once,
            snapshotDate=date(year=2019, month=8, day=24),
            snapshotTime=time(hour=14, minute=15, second=22,
                              tzinfo=timezone.utc),
            snapshotTimeZoneName="string",
        )

        payload = {
            "@type": "PricingSnapshotTrigger",
            "identifier": "dailySnap4PM",
            "title": "Daily 4PM snapshot",
            "description": "Daily job for the 4PM snapshot",
            "snapshotTime": "14:15:22Z",
            "snapshotTimeZoneName": "string",
            "snapshotDate": "2019-08-24",
            "frequency": "once"
        }
        self.assertDictEqual(trigger.model_dump_json_custom(), payload)

    def test_get_list_triggers(self):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/triggers/"
            },
            "@id": "",
            "@type": "TriggerCollection",
            "title": "Available triggers",
            "description": "A collection of triggers.",
            "identifier": "triggers",
            "totalItems": 4,
            "pageCount": 1,
            "contains": [
                {
                    "@id": "firstOfMonth/",
                    "@type": "ScheduledTrigger",
                    "title": "First calendar day of the month",
                    "description": "Schedule based trigger for start-of-month jobs.",
                    "identifier": "firstOfMonth",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "dailyMorning/",
                    "@type": "ScheduledTrigger",
                    "title": "Daily Morning Trigger",
                    "description": "Schedule based trigger for prior day end-of-day data",
                    "identifier": "dailyMorning",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "dailyBvalNY4PM/",
                    "@type": "BvalSnapshotTrigger",
                    "title": "Daily BVAL NY4PM snapshot",
                    "description": "Daily job for the New York 4PM BVAL snapshot",
                    "identifier": "dailyBvalNY4PM",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "dailySnap4PM/",
                    "@type": "PricingSnapshotTrigger",
                    "identifier": "dailySnap4PM",
                    "title": "Daily 4PM snapshot",
                    "description": "Daily job for the 4PM snapshot",
                    "issued": "2021-02-11T18:43:26.000000Z",
                    "modified": "2021-02-11T18:44:27.000000Z"
                }
            ],
            "view": {
                "@type": "PartialCollectionView",
                "@id": "?page=1",
                "first": "?page=1",
                "last": "?page=1"
            }
        }

        trigger_collection = TriggerCollection(**payload)
        self.assertEqual(len(trigger_collection.contains), 4)

    @patch.object(Session, 'request')
    def test_get_actions_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "ActionsRequest",
            "title": "End-of-day corporate actions for processing pipeline for portfolio",
            "description": "Daily morning data for prior end-of-day corporate actions data for current portfolio",
            "name": "portfolioActionsData",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z",
            "lastRunDateTime": "2017-06-01T18:44:27.000000Z",
            "nextRunDateTime": "2017-06-02T18:44:27.000000Z",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "enabled": True,
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/",
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "runtimeOptions": {
                "@type": "ActionsRuntimeOptions",
                "dateRange": {
                    "@type": "ActionsDurationDateRange",
                    "days": 7
                },
                "actionsDate": "both"
            },
            "formatting": {
                "@type": "MediaType",
                "outputMediaType": "application/json"
            }
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), ActionsRequestGet)

    @patch.object(Session, 'request')
    def test_get_bval_snapshot_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "BvalSnapshotRequest",
            "title": "Sample BVAL Snapshot Request",
            "description": "Tier 1 BVAL Snapshot Request",
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z",
            "lastRunDateTime": "2017-06-01T18:44:27.000000Z",
            "nextRunDateTime": "2017-06-02T18:44:27.000000Z",
            "name": "dailyBvalNY4PM",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "snapshotTier": 1,
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/fieldList/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "formatting": {
                "@type": "MediaType",
                "outputMediaType": "text/csv"
            },
            "enabled": True,
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), BvalSnapshotRequestGet)

    @patch.object(Session, 'request')
    def test_get_data_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "DataRequest",
            "title": "End-of-day data for processing pipeline for portfolio",
            "description": "Daily morning data for prior end-of-day data for current portfolio",
            "name": "endOfDayPortfolioData",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z",
            "lastRunDateTime": "2017-06-01T18:44:27.000000Z",
            "nextRunDateTime": "2017-06-02T18:44:27.000000Z",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/fieldList/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "formatting": {
                "@type": "MediaType",
                "outputMediaType": "text/csv"
            },
            "pricingSourceOptions": {
                "@type": "DataPricingSourceOptions",
                "exclusive": False,
                "prefer": {
                    "mnemonic": "BGN"
                },
                "skip": [
                    {
                        "mnemonic": "BVAL"
                    },
                    {
                        "mnemonic": "EXCH"
                    }
                ]
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "enabled": True,
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), DataRequestGet)

    @patch.object(Session, 'request')
    def test_get_entity_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "EntityRequest",
            "title": "Entity-level data",
            "description": "Retrieve entity-level data",
            "name": "entityLevelRequest",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "issued": "2022-01-20T13:28:26.000000Z",
            "modified": "2022-01-20T13:44:27.000000Z",
            "lastRunDateTime": "2022-01-20T13:44:27.000000Z",
            "nextRunDateTime": "2022-01-21T13:44:27.000000Z",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/fieldList/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "formatting": {
                "@type": "MediaType",
                "outputMediaType": "text/csv"
            },
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), EntityRequestGet)

    @patch.object(Session, 'request')
    def test_get_history_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "HistoryRequest",
            "title": "Historic data for verification process",
            "description": "Pull historic data to input into reconciliation pipeline.",
            "name": "historicVerification",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z",
            "lastRunDateTime": "2017-06-01T18:44:27.000000Z",
            "nextRunDateTime": "2017-06-02T18:44:27.000000Z",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/fieldList/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "formatting": {
                "@type": "HistoryFormat",
                "dateFormat": "yyyymmdd",
                "fileType": "unixFileType"
            },
            "pricingSourceOptions": {
                "@type": "HistoryPricingSourceOptions",
                "exclusive": False,
                "prefer": {
                    "mnemonic": "BGN"
                },
                "includeSourceInOutput": True
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "runtimeOptions": {
                "@type": "HistoryRuntimeOptions",
                "dateRange": {
                    "@type": "DurationDateRange",
                    "days": 30
                },
                "historyPriceCurrency": "GBP",
                "period": "weekly"
            },
            "enabled": True,
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), HistoryRequestGet)

    @patch.object(Session, 'request')
    def test_get_pricing_snapshot_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "PricingSnapshotRequest",
            "title": "IntradaySnap for portfolio",
            "description": "IntradaySnap data for current portfolio",
            "name": "portfolioPricingData",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "issued": "2021-02-11T18:43:26.000000Z",
            "modified": "2021-02-11T18:44:27.000000Z",
            "lastRunDateTime": "2021-02-11T18:44:27.000000Z",
            "nextRunDateTime": "2021-02-12T18:44:27.000000Z",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "formatting": {
                "@type": "PricingSnapshotFormat",
                "columnHeader": True,
                "delimiter": ",",
                "fileType": "unixFileType"
            },
            "pricingSourceOptions": {
                "@type": "PricingSnapshotPricingSourceOptions",
                "exclusive": False,
                "prefer": {
                    "mnemonic": "BGN"
                }
            },
            "runtimeOptions": {
                "@type": "PricingSnapshotRuntimeOptions",
                "maxEmbargo": 30
            },
            "enabled": True,
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), PricingSnapshotRequestGet)

    @patch.object(Session, 'request')
    def test_get_tick_history_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/"
            },
            "@id": "",
            "@type": "TickHistoryRequest",
            "title": "Intraday Execution Prices",
            "description": "Pull 3 hours of execution prices, along with matching bid and ask prices.",
            "name": "intradayExecutionPrices",
            "identifier": "eFGDJPCAdqm",
            "frequency": "daily",
            "issued": "2021-08-25T17:00:00.000000Z",
            "modified": "2021-08-25T17:00:00.000000Z",
            "lastRunDateTime": "2021-08-25T17:00:00.000000Z",
            "nextRunDateTime": "2021-08-26T17:00:00.000000Z",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/universe/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/requests/eFGDJPCAdqm/trigger/",
            "formatting": {
                "@type": "MediaType",
                "outputMediaType": "application/x-tar;archive-media-type=parquet"
            },
            "pricingSourceOptions": {
                "@type": "TickHistoryPricingSourceOptions",
                "exclusive": False,
                "prefer": {
                    "mnemonic": "BGN"
                }
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 12345678,
                "serialNumber": 123,
                "workStation": 12
            },
            "runtimeOptions": {
                "@type": "TickHistoryRuntimeOptions",
                "dateTimeRange": {
                    "@type": "IntervalDateTimeRange",
                    "startDateTime": "2021-08-25T09:00:00Z",
                    "endDateTime": "2021-08-25T12:00:00Z"
                },
                "tickType": "trades"
            },
            "enabled": True,
            "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/eFGDJPCAdqm/"
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_per_security_request('test', 'test')
        self.assertEqual(type(response), TickHistoryRequestGet)

    def test_create_actions_request_basic(self):
        payload = {
            "@type": "ActionsRequest",
            "title": "End-of-day corporate actions for processing pipeline for portfolio",
            "identifier": "portfolioActionsData",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101"
                    }
                ]
            },
            "trigger": {
                "@type": "ScheduledTrigger",
                "frequency": "once"
            }
        }

        test_object = ActionsRequestCreate(
            identifier="portfolioActionsData",
            title="End-of-day corporate actions for processing pipeline for portfolio",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101"
                    )
                ]
            ),
            trigger=RequestScheduledTrigger(
                frequency=TriggerFrequency.Once
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_actions_request_advanced(self):
        payload = {
            "@type": "ActionsRequest",
            "name": "portfolioActionsData",
            "identifier": "r2023022813301609afc1",
            "description": "Daily morning data for prior end-of-day corporate actions data for current portfolio",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "AAPL US Equity"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "AMZN US Equity"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "MSFT US Equity"
                    }
                ]
            },
            "trigger": {
                "@type": "SubmitTrigger"
            },
            "actionsFilter": {
                "actionEventTypeMnemonics": [
                    "CORPORATE_EVENTS",
                    "MUNI"
                ],
                "actionMnemonics": [
                    "ACQUIS",
                    "BANCR"
                ]
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 234566,
                "serialNumber": 234,
                "workStation": 12
            },
            "formatting": {
                "@type": "ActionsFormat",
                "dateFormat": "yyyymmdd"
            },
            "runtimeOptions": {
                "@type": "ActionsRuntimeOptions",
                "dateRange": {
                    "@type": "ActionsDurationDateRange",
                    "days": 7
                },
                "actionsDate": "both"
            }
        }

        test_object = ActionsRequestCreate(
            identifier="r2023022813301609afc1",
            name="portfolioActionsData",
            description="Daily morning data for prior end-of-day corporate actions data for current portfolio",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="AAPL US Equity"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="AMZN US Equity"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="MSFT US Equity"
                    ),
                ]
            ),
            trigger=RequestSubmitTrigger(),
            actionsFilter=ActionsFilter(
                actionEventTypeMnemonics=[
                    "CORPORATE_EVENTS",
                    "MUNI"
                ],
                actionMnemonics=[
                    "ACQUIS",
                    "BANCR"
                ]
            ),
            terminalIdentity=BlpTerminalIdentity(
                userNumber=234566,
                serialNumber=234,
                workStation=12
            ),
            formatting=ActionsFormat(
                dateFormat="yyyymmdd"
            ),
            runtimeOptions=ActionsRuntimeOptions(
                dateRange=ActionsDurationDateRange(
                    days=7
                ),
                actionsDate='both'
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_actions_request_linked_resource(self):
        payload = {
            "@type": "ActionsRequest",
            "name": "portfolioActionsData",
            "identifier": "r2023022813301609afc1",
            "description": "Daily morning data for prior end-of-day corporate actions data for current portfolio",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/"
        }

        test_object = ActionsRequestCreate(
            name="portfolioActionsData",
            identifier="r2023022813301609afc1",
            description="Daily morning data for prior end-of-day corporate actions data for current portfolio",
            universe="https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            trigger="https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/"
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_basic_bvalsnapshot(self):
        payload = {
            "@type": "BvalSnapshotRequest",
            "title": "Sample BVAL Snapshot Request",
            "identifier": "portfolioData",
            "snapshotTier": 1,
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101"
                    }
                ]
            },
            "fieldList": {
                "@type": "BvalSnapshotFieldList",
                "contains": [
                    {
                        "mnemonic": "MARKET_SECTOR_DES"
                    },
                    {
                        "cleanName": "idBbGlobal"
                    }
                ]
            },
            "trigger": {
                "@type": "BvalSnapshotTrigger",
                "snapshotTime": "16:00:00",
                "snapshotTimeZoneName": "America/New_York",
                "snapshotDate": "2020-10-22",
                "frequency": "once"
            }
        }

        test_object = BvalSnapshotRequestCreate(
            title="Sample BVAL Snapshot Request",
            identifier="portfolioData",
            snapshotTier=BvalSnapshotTier.Tier_1,
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101"
                    )
                ]
            ),
            fieldList=RequestBvalSnapshotFieldList(
                contains=[
                    FieldListInputItemMnemonic(mnemonic="MARKET_SECTOR_DES"),
                    FieldListInputItemCleanName(cleanName="idBbGlobal")
                ]
            ),
            trigger=RequestBvalSnapshotTrigger(
                snapshotTime=time(16, 0, 0),
                snapshotTimeZoneName="America/New_York",
                snapshotDate=date(2020, 10, 22),
                frequency=TriggerFrequency.Once
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_advanced_bval_snapshot(self):
        payload = {
            "@type": "BvalSnapshotRequest",
            "name": "portfolioData",
            "identifier": "r2023022813301609afc1",
            "description": "Tier 1 BVAL Snapshot Request",
            "snapshotTier": 1,
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "BB_GLOBAL",
                        "identifierValue": "BBG00QB6RKV8"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "BB_GLOBAL",
                        "identifierValue": "BBG00LVGP8V4"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "BB_GLOBAL",
                        "identifierValue": "BBG00DQC3PR8"
                    }
                ]
            },
            "fieldList": {
                "@type": "BvalSnapshotFieldList",
                "contains": [
                    {
                        "mnemonic": "BVAL_BID_PRICE"
                    },
                    {
                        "mnemonic": "BVAL_BID_YIELD"
                    },
                    {
                        "mnemonic": "BVAL_MID_PRICE"
                    },
                    {
                        "mnemonic": "BVAL_MID_YIELD"
                    },
                    {
                        "mnemonic": "BVAL_ASK_PRICE"
                    },
                    {
                        "mnemonic": "BVAL_ASK_YIELD"
                    }
                ]
            },
            "trigger": {
                "@type": "BvalSnapshotTrigger",
                "snapshotTime": "16:00:00",
                "snapshotTimeZoneName": "America/New_York",
                "snapshotDate": "2020-10-22",
                "frequency": "daily"
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 234566,
                "serialNumber": 234,
                "workStation": 12
            },
            "formatting": {
                "@type": "BvalSnapshotFormat",
                "columnHeader": True,
                "dateFormat": "yyyymmdd",
                "delimiter": ",",
                "fileType": "unixFileType",
                "outputFormat": "variableOutputFormat"
            },
            "pricingSourceOptions": {
                "@type": "BvalPricingSourceOptions",
                "pricingSource": "BVIC"
            }
        }

        test_object = BvalSnapshotRequestCreate(
            identifier="r2023022813301609afc1",
            name="portfolioData",
            description="Tier 1 BVAL Snapshot Request",
            snapshotTier=BvalSnapshotTier.Tier_1,
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.BB_GLOBAL,
                        identifierValue="BBG00QB6RKV8"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.BB_GLOBAL,
                        identifierValue="BBG00LVGP8V4"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.BB_GLOBAL,
                        identifierValue="BBG00DQC3PR8"
                    ),
                ]
            ),
            trigger=RequestBvalSnapshotTrigger(
                snapshotTime=time(16, 0, 0),
                snapshotTimeZoneName="America/New_York",
                snapshotDate=date(2020, 10, 22),
                frequency=TriggerFrequency.Daily
            ),
            fieldList=RequestBvalSnapshotFieldList(
                contains=[
                    FieldListInputItemMnemonic(mnemonic="BVAL_BID_PRICE"),
                    FieldListInputItemMnemonic(mnemonic="BVAL_BID_YIELD"),
                    FieldListInputItemMnemonic(mnemonic="BVAL_MID_PRICE"),
                    FieldListInputItemMnemonic(mnemonic="BVAL_MID_YIELD"),
                    FieldListInputItemMnemonic(mnemonic="BVAL_ASK_PRICE"),
                    FieldListInputItemMnemonic(mnemonic="BVAL_ASK_YIELD"),
                ]
            ),
            terminalIdentity=BlpTerminalIdentity(
                userNumber=234566,
                serialNumber=234,
                workStation=12
            ),
            formatting=BvalSnapshotFormat(
                columnHeader=True,
                dateFormat="yyyymmdd",
                delimiter=",",
                fileType="unixFileType",
                outputFormat="variableOutputFormat"
            ),
            pricingSourceOptions=BvalPricingSourceOptions(
                pricingSource="BVIC"
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_bval_snapshot_linked(self):
        payload = {
            "@type": "BvalSnapshotRequest",
            "name": "portfolioData",
            "identifier": "r2023022813301609afc1",
            "description": "Tier 1 BVAL Snapshot Request",
            "snapshotTier": 1,
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/analyticsTeamFields/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/endOfDayPortfolioTrigger/"
        }

        test_object = BvalSnapshotRequestCreate(
            name="portfolioData",
            identifier="r2023022813301609afc1",
            description="Tier 1 BVAL Snapshot Request",
            snapshotTier=BvalSnapshotTier.Tier_1,
            universe="https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            fieldList="https://api.bloomberg.com/eap/catalogs/1234/fieldLists/analyticsTeamFields/",
            trigger="https://api.bloomberg.com/eap/catalogs/1234/triggers/endOfDayPortfolioTrigger/"
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_basic_data_request(self):
        payload = {
            "@type": "DataRequest",
            "title": "End-of-day data for processing pipeline for portfolio",
            "identifier": "portfolioData",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101"
                    }
                ]
            },
            "fieldList": {
                "@type": "DataFieldList",
                "contains": [
                    {
                        "mnemonic": "ID_BB_GLOBAL"
                    },
                    {
                        "cleanName": "pxBid"
                    }
                ]
            },
            "trigger": {
                "@type": "ScheduledTrigger",
                "frequency": "once"
            }
        }

        test_object = DataRequestCreate(
            title="End-of-day data for processing pipeline for portfolio",
            identifier="portfolioData",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101"
                    )
                ]
            ),
            fieldList=RequestDataFieldList(
                contains=[
                    FieldListInputItemMnemonic(mnemonic="ID_BB_GLOBAL"),
                    FieldListInputItemCleanName(cleanName="pxBid"),
                ]
            ),
            trigger=RequestScheduledTrigger(
                frequency=TriggerFrequency.Once
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_axiata_data_request(self):
        payload = {
            "@type": "DataRequest",
            "title": "arvintest",
            "identifier": "arvintest",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "AXIATA MK EQUITY"
                    },
                ]
            },
            "fieldList": {
                "@type": "DataFieldList",
                "contains": [
                    {
                        "mnemonic": "PX_LAST"
                    },
                    {
                        "mnemonic": "CUR_MKT_CAP"
                    },
                    {
                        "mnemonic": "CURRENT_FULL_FISCAL_YEAR_END"
                    },
                    {
                        "mnemonic": "CURR_ENTP_VAL"
                    },
                    {
                        "mnemonic": "BS_CASH_NEAR_CASH_ITEM"
                    },
                    {
                        "mnemonic": "SHORT_AND_LONG_TERM_DEBT"
                    },
                    {
                        "mnemonic": "ARD_TOT_SHARE_EQY_EXCL_MINORITY"
                    },
                    {
                        "mnemonic": "TOTAL_EQUITY"
                    },
                    {
                        "mnemonic": "INDUSTRY_SECTOR"
                    },
                    {
                        "mnemonic": "GICS_SECTOR_NAME"
                    },
                    {
                        "mnemonic": "GICS_INDUSTRY_NAME"
                    },
                    {
                        "mnemonic": "PRIMARY_EXCHANGE_NAME"
                    },
                    {
                        "mnemonic": "ID_ISIN"
                    },
                    {
                        "mnemonic": "SALES_REV_TURN"
                    },
                    {
                        "mnemonic": "SCOPE_1_GHG_CO2_EMISSIONS"
                    },
                    {
                        "mnemonic": "GHG_SCOPE_1"
                    },
                    {
                        "mnemonic": "SCOPE_2_GHG_CO2_EMISSIONS"
                    },
                    {
                        "mnemonic": "GHG_SCOPE_2"
                    },
                    {
                        "mnemonic": "CRNCY"
                    },
                ]
            },
            "trigger": {
                "@type": "ScheduledTrigger",
                "frequency": "once"
            }
        }

        test_object = DataRequestCreate(
            title="arvintest",
            identifier="arvintest",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue='AXIATA MK EQUITY'
                    )
                ]
            ),
            fieldList=RequestDataFieldList(
                contains=[
                    FieldListInputItemMnemonic(mnemonic='PX_LAST'),
                    FieldListInputItemMnemonic(mnemonic='CUR_MKT_CAP'),
                    FieldListInputItemMnemonic(
                        mnemonic='CURRENT_FULL_FISCAL_YEAR_END'),
                    FieldListInputItemMnemonic(mnemonic='CURR_ENTP_VAL'),
                    FieldListInputItemMnemonic(
                        mnemonic='BS_CASH_NEAR_CASH_ITEM'),
                    FieldListInputItemMnemonic(
                        mnemonic='SHORT_AND_LONG_TERM_DEBT'),
                    FieldListInputItemMnemonic(
                        mnemonic='ARD_TOT_SHARE_EQY_EXCL_MINORITY'),
                    FieldListInputItemMnemonic(mnemonic='TOTAL_EQUITY'),
                    FieldListInputItemMnemonic(mnemonic='INDUSTRY_SECTOR'),
                    FieldListInputItemMnemonic(mnemonic='GICS_SECTOR_NAME'),
                    FieldListInputItemMnemonic(mnemonic='GICS_INDUSTRY_NAME'),
                    FieldListInputItemMnemonic(
                        mnemonic='PRIMARY_EXCHANGE_NAME'),
                    FieldListInputItemMnemonic(mnemonic='ID_ISIN'),
                    FieldListInputItemMnemonic(mnemonic='SALES_REV_TURN'),
                    FieldListInputItemMnemonic(
                        mnemonic='SCOPE_1_GHG_CO2_EMISSIONS'),
                    FieldListInputItemMnemonic(mnemonic='GHG_SCOPE_1'),
                    FieldListInputItemMnemonic(
                        mnemonic='SCOPE_2_GHG_CO2_EMISSIONS'),
                    FieldListInputItemMnemonic(mnemonic='GHG_SCOPE_2'),
                    FieldListInputItemMnemonic(mnemonic='CRNCY'),
                ]

            ),
            trigger=RequestScheduledTrigger(
                frequency=TriggerFrequency.Once
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_advanced_data_request(self):
        payload = {
            "@type": "DataRequest",
            "name": "portfolioData",
            "identifier": "r2023022813301609afc1",
            "description": "Daily morning data for prior end-of-day data for current portfolio",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "ISIN",
                        "identifierValue": "US78378X1072"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101",
                        "fieldOverrides": [
                            {
                                "@type": "FieldOverride",
                                "mnemonic": "LQA_MODEL_AS_OF_DATE",
                                "override": "20190103"
                            },
                            {
                                "@type": "FieldOverride",
                                "cleanName": "lqaBidAskSpread",
                                "override": "0.2"
                            }
                        ]
                    }
                ]
            },
            "fieldList": {
                "@type": "DataFieldList",
                "contains": [
                    {
                        "cleanName": "pxBid"
                    },
                    {
                        "mnemonic": "ID_BB_GLOBAL"
                    },
                    {
                        "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"
                    }
                ]
            },
            "trigger": {
                "@type": "ScheduledTrigger",
                "frequency": "weekday",
                "startDate": "2018-03-05",
                "startTime": "04:00:00"
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 234566,
                "serialNumber": 234,
                "workStation": 12
            },
            "formatting": {
                "@type": "DataFormat",
                "columnHeader": True,
                "dateFormat": "yyyymmdd",
                "delimiter": ",",
                "fileType": "unixFileType",
                "outputFormat": "variableOutputFormat"
            },
            "pricingSourceOptions": {
                "@type": "DataPricingSourceOptions",
                "prefer": {
                    "mnemonic": "BVAL"
                },
                "exclusive": False,
                "skip": [
                    {
                        "mnemonic": "BVAL"
                    },
                    {
                        "mnemonic": "CBBT"
                    }
                ]
            }
        }

        test_object = DataRequestCreate(
            name="portfolioData",
            identifier="r2023022813301609afc1",
            description="Daily morning data for prior end-of-day data for current portfolio",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.ISIN,
                        identifierValue="US78378X1072"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101",
                        fieldOverrides=[
                            FieldOverride(
                                mnemonic="LQA_MODEL_AS_OF_DATE", override="20190103"),
                            FieldOverride(
                                cleanName="lqaBidAskSpread", override="0.2"
                            ),
                        ]
                    )
                ]
            ),
            fieldList=RequestDataFieldList(
                contains=[
                    FieldListInputItemCleanName(cleanName="pxBid"),
                    FieldListInputItemMnemonic(mnemonic="ID_BB_GLOBAL"),
                    FieldListInputItemId(
                        id="https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/")
                ]
            ),
            trigger=RequestScheduledTrigger(
                frequency=TriggerFrequency.Weekday,
                startDate=date(2018, 3, 5),
                startTime=time(4, 0, 0)
            ),
            terminalIdentity=BlpTerminalIdentity(
                userNumber=234566,
                serialNumber=234,
                workStation=12
            ),
            formatting=DataFormat(
                columnHeader=True,
                dateFormat="yyyymmdd",
                delimiter=",",
                fileType="unixFileType",
                outputFormat="variableOutputFormat"
            ),
            pricingSourceOptions=DataPricingSourceOptions(
                prefer=PricingSourceDetail(mnemonic="BVAL"),
                exclusive=False,
                skip=[
                    PricingSourceDetail(mnemonic="BVAL"),
                    PricingSourceDetail(mnemonic="CBBT")
                ]
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_data_request_linked(self):
        payload = {
            "@type": "DataRequest",
            "name": "portfolioData",
            "identifier": "r2023022813301609afc1",
            "description": "Daily morning data for prior end-of-day data for current portfolio",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/analyticsTeamFields/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/"
        }

        test_object = DataRequestCreate(
            name="portfolioData",
            identifier="r2023022813301609afc1",
            description="Daily morning data for prior end-of-day data for current portfolio",
            universe="https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            fieldList="https://api.bloomberg.com/eap/catalogs/1234/fieldLists/analyticsTeamFields/",
            trigger="https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/"
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_advanced_entity_request(self):
        payload = {
            "@type": "EntityRequest",
            "title": "Entity-level data",
            "description": "Retrieve entity-level data",
            "identifier": "entityLevelRequest",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "MSFT US Equity"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "LEGAL_ENTITY_IDENTIFIER",
                        "identifierValue": "5493006MHB84DD0ZWV18"
                    }
                ]
            },
            "fieldList": {
                "@type": "EntityFieldList",
                "contains": [
                    {
                        "mnemonic": "ID_BB_COMPANY"
                    },
                    {
                        "mnemonic": "LEI_NAME"
                    },
                    {
                        "mnemonic": "CNTRY_OF_DOMICILE"
                    },
                    {
                        "mnemonic": "LEGAL_ENTITY_IDENTIFIER"
                    },
                    {
                        "mnemonic": "COMPANY_TAX_IDENTIFIER"
                    }
                ]
            },
            "trigger": {
                "@type": "SubmitTrigger"
            }
        }

        test_object = EntityRequestCreate(
            title="Entity-level data",
            description="Retrieve entity-level data",
            identifier="entityLevelRequest",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="MSFT US Equity"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.LEGAL_ENTITY_IDENTIFIER,
                        identifierValue="5493006MHB84DD0ZWV18"
                    )
                ]
            ),
            fieldList=RequestEntityFieldList(
                contains=[
                    FieldListInputItemMnemonic(mnemonic="ID_BB_COMPANY"),
                    FieldListInputItemMnemonic(mnemonic="LEI_NAME"),
                    FieldListInputItemMnemonic(mnemonic="CNTRY_OF_DOMICILE"),
                    FieldListInputItemMnemonic(
                        mnemonic="LEGAL_ENTITY_IDENTIFIER"),
                    FieldListInputItemMnemonic(
                        mnemonic="COMPANY_TAX_IDENTIFIER"),
                ]
            ),
            trigger=RequestSubmitTrigger(),
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_linked_entity_request(self):
        payload = {
            "@type": "EntityRequest",
            "name": "entityLevelRequest",
            "identifier": "r2023022813301609afc1",
            "description": "Retrieve entity-level data",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/companiesAndEntities/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/entityLevelFields/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/"
        }

        test_object = EntityRequestCreate(
            name='entityLevelRequest',
            identifier='r2023022813301609afc1',
            description='Retrieve entity-level data',
            universe='https://api.bloomberg.com/eap/catalogs/1234/universes/companiesAndEntities/',
            fieldList='https://api.bloomberg.com/eap/catalogs/1234/fieldLists/entityLevelFields/',
            trigger='https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/'

        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_advanced_history_request(self):
        payload = {
            "@type": "HistoryRequest",
            "name": "historicVerification",
            "identifier": "r2023022813301609afc1",
            "description": "Pull historic data to input into reconciliation pipeline.",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "ISIN",
                        "identifierValue": "US78378X1072"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101",
                        "fieldOverrides": [
                            {
                                "@type": "FieldOverride",
                                "mnemonic": "LQA_MODEL_AS_OF_DATE",
                                "override": "20190103"
                            },
                            {
                                "@type": "FieldOverride",
                                "cleanName": "lqaBidAskSpread",
                                "override": "0.2"
                            }
                        ]
                    }
                ]
            },
            "fieldList": {
                "@type": "HistoryFieldList",
                "contains": [
                    {
                        "cleanName": "pxBid"
                    },
                    {
                        "mnemonic": "ID_BB_GLOBAL"
                    },
                    {
                        "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"
                    }
                ]
            },
            "trigger": {
                "@type": "ScheduledTrigger",
                "frequency": "weekday",
                "startDate": "2018-03-05",
                "startTime": "04:00:00"
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 234566,
                "serialNumber": 234,
                "workStation": 12
            },
            "runtimeOptions": {
                "@type": "HistoryRuntimeOptions",
                "dateRange": {
                    "@type": "DurationDateRange",
                    "days": 30
                },
                "historyPriceCurrency": "GBP",
                "period": "weekly"
            },
            "formatting": {
                "@type": "HistoryFormat",
                "dateFormat": "yyyymmdd",
                "fileType": "unixFileType"
            },
            "pricingSourceOptions": {
                "@type": "HistoryPricingSourceOptions",
                "exclusive": False,
                "prefer": {
                    "mnemonic": "BGN"
                },
                "includeSourceInOutput": True
            }
        }

        test_object = HistoryRequestCreate(
            name="historicVerification",
            identifier="r2023022813301609afc1",
            description="Pull historic data to input into reconciliation pipeline.",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.ISIN,
                        identifierValue="US78378X1072"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101",
                        fieldOverrides=[
                            FieldOverride(
                                mnemonic="LQA_MODEL_AS_OF_DATE",
                                override="20190103"
                            ),
                            FieldOverride(
                                cleanName="lqaBidAskSpread",
                                override="0.2"
                            )
                        ]
                    )
                ]
            ),
            fieldList=RequestHistoryFieldList(
                contains=[
                    FieldListInputItemCleanName(cleanName="pxBid"),
                    FieldListInputItemMnemonic(mnemonic="ID_BB_GLOBAL"),
                    FieldListInputItemId(
                        id="https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/")
                ]
            ),
            trigger=RequestScheduledTrigger(
                frequency=TriggerFrequency.Weekday,
                startDate=date(2018, 3, 5),
                startTime=time(4, 0, 0)
            ),
            terminalIdentity=BlpTerminalIdentity(
                userNumber=234566,
                serialNumber=234,
                workStation=12
            ),
            runtimeOptions=HistoryRuntimeOptions(
                dateRange=DurationDateRange(
                    days=30
                ),
                historyPriceCurrency="GBP",
                period=Period.weekly
            ),
            formatting=HistoryFormat(
                dateFormat="yyyymmdd",
                fileType="unixFileType",
            ),
            pricingSourceOptions=HistoryPricingSourceOptions(
                exclusive=False,
                prefer=PricingSourceDetail(
                    mnemonic="BGN"
                ),
                includeSourceInOutput=True
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_linked_history_request(self):
        payload = {
            "@type": "HistoryRequest",
            "name": "historicVerification",
            "identifier": "r2023022813301609afc1",
            "description": "Pull historic data to input into reconciliation pipeline.",
            "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/",
            "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/analyticsTeamFields/",
            "trigger": "https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/",
            "runtimeOptions": {
                "@type": "HistoryRuntimeOptions",
                "dateRange": {
                    "@type": "DurationDateRange",
                    "days": 30
                },
                "historyPriceCurrency": "GBP",
                "period": "weekly"
            }
        }

        test_object = HistoryRequestCreate(
            name="historicVerification",
            identifier="r2023022813301609afc1",
            description="Pull historic data to input into reconciliation pipeline.",
            universe='https://api.bloomberg.com/eap/catalogs/1234/universes/quantsUSTop500/',
            fieldList='https://api.bloomberg.com/eap/catalogs/1234/fieldLists/analyticsTeamFields/',
            trigger='https://api.bloomberg.com/eap/catalogs/bbg/triggers/submit/',
            runtimeOptions=HistoryRuntimeOptions(
                dateRange=DurationDateRange(
                    days=30
                ),
                historyPriceCurrency="GBP",
                period=Period.weekly
            ),
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_advanced_pricing_snapshot_request(self):
        payload = {
            "@type": "PricingSnapshotRequest",
            "name": "portfolioData",
            "identifier": "r2023022813301609afc1",
            "description": "Daily morning data for prior end-of-day data for current portfolio",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "ISIN",
                        "identifierValue": "US78378X1072"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101",
                        "fieldOverrides": [
                            {
                                "@type": "FieldOverride",
                                "mnemonic": "PRICING_SOURCE",
                                "override": "BGN"
                            }
                        ]
                    }
                ]
            },
            "trigger": {
                "@type": "PricingSnapshotTrigger",
                "snapshotTime": "16:00:00",
                "snapshotTimeZoneName": "Europe/London",
                "snapshotDate": "2021-02-11",
                "frequency": "daily"
            },
            "terminalIdentity": {
                "@type": "BlpTerminalIdentity",
                "userNumber": 234566,
                "serialNumber": 234,
                "workStation": 12
            },
            "formatting": {
                "@type": "PricingSnapshotFormat",
                "columnHeader": True,
                "delimiter": ",",
                "fileType": "unixFileType"
            },
            "pricingSourceOptions": {
                "@type": "PricingSnapshotPricingSourceOptions",
                "prefer": {
                    "mnemonic": "US"
                },
                "exclusive": False
            },
            "runtimeOptions": {
                "@type": "PricingSnapshotRuntimeOptions",
                "maxEmbargo": 30
            }
        }

        test_object = PricingSnapshotRequestCreate(
            name="portfolioData",
            identifier="r2023022813301609afc1",
            description="Daily morning data for prior end-of-day data for current portfolio",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.ISIN,
                        identifierValue="US78378X1072"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101",
                        fieldOverrides=[
                            FieldOverride(
                                mnemonic="PRICING_SOURCE", override="BGN")
                        ]
                    )
                ]
            ),
            trigger=RequestPricingSnapshotTrigger(
                snapshotTime=time(16, 0, 0),
                snapshotTimeZoneName="Europe/London",
                snapshotDate=date(2021, 2, 11),
                frequency=TriggerFrequency.Daily
            ),
            terminalIdentity=BlpTerminalIdentity(
                userNumber=234566,
                serialNumber=234,
                workStation=12
            ),
            formatting=PricingSnapshotFormat(
                columnHeader=True,
                delimiter=',',
                fileType='unixFileType',
            ),
            pricingSourceOptions=PricingSnapshotPricingSourceOptions(
                prefer=PricingSourceDetail(mnemonic="US"),
                exclusive=False
            ),
            runtimeOptions=PricingSnapshotRuntimeOptions(
                maxEmbargo=30
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def test_create_tick_history_request(self):
        payload = {
            "@type": "TickHistoryRequest",
            "name": "intradayExecutionPrices",
            "identifier": "r2023022813301609afc1",
            "description": "Pull 3 hours of execution prices, along with matching bid and ask prices.",
            "universe": {
                "@type": "Universe",
                "contains": [
                    {
                        "@type": "Identifier",
                        "identifierType": "TICKER",
                        "identifierValue": "SPX Index"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "ISIN",
                        "identifierValue": "US78378X1072"
                    },
                    {
                        "@type": "Identifier",
                        "identifierType": "CUSIP",
                        "identifierValue": "459200101"
                    }
                ]
            },
            "trigger": {
                "@type": "SubmitTrigger"
            },
            "formatting": {
                "@type": "MediaType",
                "outputMediaType": "application/x-tar;archive-media-type=parquet"
            },
            "runtimeOptions": {
                "@type": "TickHistoryRuntimeOptions",
                "dateTimeRange": {
                    "@type": "IntervalDateTimeRange",
                    "startDateTime": "2021-08-25T09:00:00Z",
                    "endDateTime": "2021-08-25T12:00:00Z"
                },
                "tickType": "trades"
            }
        }

        test_object = TickHistoryRequestCreate(
            name="intradayExecutionPrices",
            identifier="r2023022813301609afc1",
            description="Pull 3 hours of execution prices, along with matching bid and ask prices.",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue="SPX Index"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.ISIN,
                        identifierValue="US78378X1072"
                    ),
                    UniverseInputItems(
                        identifierType=SecID.CUSIP,
                        identifierValue="459200101",
                    )
                ]
            ),
            trigger=RequestSubmitTrigger(),
            formatting=TickHistoryMediaTypeFormat(
                outputMediaType="application/x-tar;archive-media-type=parquet"
            ),
            runtimeOptions=TickHistoryRuntimeOptions(
                dateTimeRange=IntervalDateTimeRange(
                    startDateTime=datetime.datetime(
                        2021, 8, 25, 9, 0, 0, tzinfo=timezone.utc),
                    endDateTime=datetime.datetime(
                        2021, 8, 25, 12, 0, 0, tzinfo=timezone.utc),
                ),
                tickType="trades"
            )
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    @patch.object(Session, 'request')
    def test_get_all_per_security_universes(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/universes/"
            },
            "@id": "",
            "@type": "UniverseCollection",
            "title": "Available universes",
            "description": "A collection of universes.",
            "identifier": "universes",
            "totalItems": 6,
            "pageCount": 3,
            "contains": [
                {
                    "@id": "complianceRestrictedList/",
                    "@type": "Universe",
                    "title": "Restricted securities",
                    "description": "Securities that need legal/compliance authorization before trading.",
                    "identifier": "complianceRestrictedList",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "quantsUSTop500/",
                    "@type": "Universe",
                    "title": "Quants top 500 US equities by market cap",
                    "description": "Quant desk US equity research universe",
                    "identifier": "quantsUSTop500",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                }
            ],
            "view": {
                "@type": "PartialCollectionView",
                "@id": "?page=2",
                "first": "?page=1",
                "last": "?page=3",
                "next": "?page=3",
                "previous": "?page=1"
            }
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_all_per_security_universes('test')
        self.assertEqual(type(response), UniverseCollectionView)

    @patch.object(Session, 'request')
    def test_get_all_per_security_request(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/requests/"
            },
            "@id": "",
            "@type": "RequestCollection",
            "title": "Available requests",
            "description": "Requests for catalog 1234",
            "identifier": "requests",
            "totalItems": 6,
            "pageCount": 1,
            "contains": [
                {
                    "@id": "monthEndAnalysisData/",
                    "@type": "DataRequest",
                    "title": "",
                    "name": "MonthEndData",
                    "enabled": "True",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "frequency": "daily",
                    "description": "Month-end data for quant desk analysis",
                    "identifier": "monthEndAnalysisData",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/monthEndAnalysisData/",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z",
                    "nextRunDateTime": "2017-06-02T18:44:27.000000Z"
                },
                {
                    "@id": "historicVerification/",
                    "@type": "HistoryRequest",
                    "title": "Historic data for verification process",
                    "frequency": "adhoc",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "description": "Pull historic data to input into reconciliation pipeline.",
                    "identifier": "historicVerification",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/historicVerification/",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "portfolioActionsData/",
                    "@type": "ActionsRequest",
                    "name": "EndOfDayCorpActionsData",
                    "title": "Month-end data",
                    "enabled": "True",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "frequency": "daily",
                    "description": "Daily morning data for prior end-of-day corporate actions data for current portfolio",
                    "identifier": "portfolioActionsData",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/portfolioActionsData/",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z",
                    "lastRunDateTime": "2017-06-01T18:44:27.000000Z",
                    "nextRunDateTime": "2017-06-02T18:44:27.000000Z"
                },
                {
                    "@id": "portfolioBvalData/",
                    "@type": "BvalSnapshotRequest",
                    "name": "BVALSnapshotData",
                    "title": "",
                    "enabled": "True",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "frequency": "daily",
                    "description": "Tier 1 BVAL Snapshot Request",
                    "identifier": "portfolioBvalData",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/portfolioBvalData/",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z",
                    "nextRunDateTime": "2017-06-02T18:44:27.000000Z"
                },
                {
                    "@id": "portfolioPricingData/",
                    "@type": "PricingSnapshotRequest",
                    "title": "IntradaySnap for Portfolio",
                    "enabled": "False",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "frequency": "weekly",
                    "description": "IntradaySnap data for current portfolio",
                    "identifier": "portfolioPricingData",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/portfolioPricingData/",
                    "issued": "2021-02-11T18:43:26.000000Z",
                    "modified": "2021-02-11T18:44:27.000000Z",
                    "lastRunDateTime": "2021-02-11T18:44:27.000000Z"
                },
                {
                    "@id": "tickHistoryData/",
                    "@type": "TickHistoryRequest",
                    "name": "TickHistoryData",
                    "title": "",
                    "enabled": "True",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "frequency": "daily",
                    "description": "Sample Tick History Request",
                    "identifier": "tickHistoryData",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/tickHistoryData/",
                    "issued": "2021-08-25T10:00:00.000000Z",
                    "modified": "2021-08-25T10:00:00.000000Z"
                },
                {
                    "@id": "entityLevelRequest/",
                    "@type": "EntityRequest",
                    "title": "EntityData",
                    "enabled": "True",
                    "universe": "https://api.bloomberg.com/eap/catalogs/1234/universes/complianceRestrictedList/",
                    "fieldList": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/",
                    "trigger": "https://api.bloomberg.com/eap/catalogs/1234/triggers/daily/",
                    "frequency": "daily",
                    "description": "Retrieve entity-level data",
                    "identifier": "entityLevelRequest",
                    "dataset": "https://api.bloomberg.com/eap/catalogs/1234/datasets/entityLevelRequest/",
                    "issued": "2022-01-20T13:28:26.000000Z",
                    "modified": "2022-01-20T13:44:27.000000Z",
                    "nextRunDateTime": "2021-08-26T10:00:00.000000Z"
                }
            ],
            "view": {
                "@type": "PartialCollectionView",
                "@id": "?page=1",
                "first": "?page=1",
                "last": "?page=1"
            }
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_all_security_requests('')
        self.assertEqual(type(response), RequestCollectionView)

    @patch.object(Session, 'request')
    def test_get_all_field_list(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/"
            },
            "@id": "",
            "@type": "FieldListCollection",
            "title": "Available field lists",
            "description": "A collection of field lists.",
            "identifier": "fieldLists",
            "totalItems": 2,
            "pageCount": 1,
            "contains": [
                {
                    "@id": "dataWarehouseFields/",
                    "@type": "DataFieldList",
                    "title": "Data Warehouse Fields",
                    "description": "Fields required for the data warehouse processing pipeline.",
                    "identifier": "dataWarehouseFields",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "analyticsTeamFields/",
                    "@type": "DataFieldList",
                    "title": "Analytics Team Fields",
                    "description": "Categorizations (country, asset class, industry) and quantitative scores (ratings, moving averages, ratios).",
                    "identifier": "analyticsTeamFields",
                    "issued": "2017-06-01T18:43:26.000000Z",
                    "modified": "2017-06-01T18:44:27.000000Z"
                },
                {
                    "@id": "fixedIncomeValuation/",
                    "@type": "BvalSnapshotFieldList",
                    "title": "Fixed Income Valuation",
                    "description": "Bloomberg Evaluated Pricing for Fixed Income securities.",
                    "identifier": "fixedIncomeValuation",
                    "issued": "2018-03-01T11:35:12.000000Z",
                    "modified": "2018-03-01T11:36:24.000000Z"
                },
                {
                    "@id": "closingPriceHistory/",
                    "@type": "HistoryFieldList",
                    "title": "Closing Price History",
                    "description": "Time series of official closing price and last price.",
                    "identifier": "closingPriceHistory",
                    "issued": "2018-10-11T15:51:34.000000Z",
                    "modified": "2018-10-11T15:52:47.000000Z"
                }
            ],
            "view": {
                "@type": "PartialCollectionView",
                "@id": "?page=1",
                "first": "?page=1",
                "last": "?page=1"
            }
        }
        mock_response.return_value = get_200_response(payload)
        response = self.client.get_all_field_lists('')
        self.assertEqual(type(response), FieldListCollection)
        self.assertEqual(len(response.contains), 4)
        self.assertEqual(
            response.contains[0].type, FieldListType.DataFieldList)

    def test_create_data_field_list(self):
        payload = {
            "@type": "DataFieldList",
            "identifier": "dataWarehouseFields",
            "title": "Data Warehouse Fields",
            "description": "Fields required for the data warehouse processing pipeline.",
            "contains": [
                {
                    "cleanName": "pxBid"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/idBbGlobal/"
                }
            ]
        }

        test_object = DataFieldListCreate(
            identifier="dataWarehouseFields",
            title="Data Warehouse Fields",
            description="Fields required for the data warehouse processing pipeline.",
            contains=[
                FieldListInputItemCleanName(cleanName="pxBid"),
                FieldListInputItemId(
                    id="https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"),
                FieldListInputItemId(
                    id="https://api.bloomberg.com/eap/catalogs/bbg/fields/idBbGlobal/")
            ]
        )

        test_object_generic = FieldListCreate(
            type=FieldListType.DataFieldList,
            identifier="dataWarehouseFields",
            title="Data Warehouse Fields",
            description="Fields required for the data warehouse processing pipeline.",
            contains=[
                FieldListInputItemCleanName(cleanName="pxBid"),
                FieldListInputItemId(
                    id="https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"),
                FieldListInputItemId(
                    id="https://api.bloomberg.com/eap/catalogs/bbg/fields/idBbGlobal/")
            ]
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())
        self.assertDictEqual(
            payload, test_object_generic.model_dump_json_custom())

    @patch.object(Session, 'request')
    def test_get_field_list(self, mock_response):
        payload = {
            "@context": {
                "@vocab": "https://api.bloomberg.com/eap/ontology#",
                "@base": "https://api.bloomberg.com/eap/catalogs/1234/fieldLists/dataWarehouseFields/"
            },
            "@id": "",
            "@type": "DataFieldList",
            "title": "Add asset class to data processing fields",
            "description": "Add asset class to data processing fields",
            "identifier": "dataWarehouseFields",
            "referencedByActiveRequests": True,
            "issued": "2017-06-01T18:43:26.000000Z",
            "modified": "2017-06-01T18:44:27.000000Z",
            "totalItems": 4,
            "pageCount": 1,
            "contains": [
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/name/",
                    "identifier": "name",
                    "cleanName": "name",
                    "mnemonic": "NAME",
                    "title": "Name",
                    "dlCommercialModelCategory": "Open Source",
                    "loadingSpeed": "Hare",
                    "type": "Character"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/idBbGlobal/",
                    "identifier": "idBbGlobal",
                    "cleanName": "idBbGlobal",
                    "mnemonic": "ID_BB_GLOBAL",
                    "title": "Financial Instrument Global Identifier",
                    "dlCommercialModelCategory": "Open Source",
                    "loadingSpeed": "Hare",
                    "type": "Character"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/",
                    "identifier": "pxLast",
                    "cleanName": "pxLast",
                    "mnemonic": "PX_LAST",
                    "title": "Last Price",
                    "dlCommercialModelCategory": "Pricing - Intraday",
                    "loadingSpeed": "Hare",
                    "type": "Price"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/marketSectorDes/",
                    "identifier": "marketSectorDes",
                    "cleanName": "marketSectorDes",
                    "mnemonic": "MARKET_SECTOR_DES",
                    "title": "Market Sector Description",
                    "dlCommercialModelCategory": "Open Source",
                    "loadingSpeed": "Hare",
                    "type": "Character"
                }
            ],
            "view": {
                "@type": "PartialCollectionView",
                "@id": "?page=1",
                "first": "?page=1",
                "last": "?page=1"
            }
        }

        mock_response.return_value = get_200_response(payload)
        response = self.client.get_field_list('', '')
        self.assertEqual(type(response), FieldListView)
        self.assertEqual(len(response.contains), 4)
        self.assertEqual(response.contains[0].type, 'Character')

    def test_update_field_list(self):
        payload = {
            "title": "Add asset class to data processing fields",
            "description": "Add asset class to data processing fields",
            "contains": [
                {
                    "cleanName": "pxBid"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"
                },
                {
                    "@id": "https://api.bloomberg.com/eap/catalogs/bbg/fields/idBbGlobal/"
                },
                {
                    "mnemonic": "MARKET_SECTOR_DES"
                }
            ]
        }

        test_object = FieldListPatch(
            title="Add asset class to data processing fields",
            description="Add asset class to data processing fields",
            contains=[
                FieldListInputItemCleanName(cleanName="pxBid"),
                FieldListInputItemId(
                    id="https://api.bloomberg.com/eap/catalogs/bbg/fields/pxLast/"),
                FieldListInputItemId(
                    id="https://api.bloomberg.com/eap/catalogs/bbg/fields/idBbGlobal/"),
                FieldListInputItemMnemonic(mnemonic="MARKET_SECTOR_DES")
            ]
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())

    def create_submit_trigger(self):
        payload = {
            "@type": "SubmitTrigger",
            "identifier": "dailyMorning",
            "title": "Early Morning Daily",
            "description": "First run of daily data jobs"
        }

        test_object = SubmitTriggerCreate(
            identifier="dailyMorning",
            title="Early Morning Daily",
            description="First run of daily data jobs"
        )

        self.assertDictEqual(payload, test_object.model_dump_json_custom())
