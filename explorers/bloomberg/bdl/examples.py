from explorers.bloomberg.bdl.bdl_api_client import BDLClient
from explorers.bloomberg.bdl.resources.field_list import FieldListInputItemMnemonic
from explorers.bloomberg.bdl.resources.security_request import DataRequestCreate, RequestDataFieldList, \
    RequestSubmitTrigger, \
    RequestUniverse, MediaTypeWithFieldIdentifier
from explorers.bloomberg.bdl.resources.universe import UniverseInputItems, SecID


def create_test_maybank_request():
    client = BDLClient()
    response = client.create_per_security_request(
        # catalog id is by default account id, set the param to override
        request_object=DataRequestCreate(
            title="20240513MaybankTest",
            universe=RequestUniverse(
                contains=[
                    UniverseInputItems(
                        identifierType=SecID.TICKER,
                        identifierValue='MAY MK Equity'
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
                    FieldListInputItemMnemonic(
                        mnemonic='PRIMARY_EXCHANGE_NAME'),
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
            trigger=RequestSubmitTrigger(),
            formatting=MediaTypeWithFieldIdentifier(
                outputMediaType='application/json'
            )
        )
    )

    print(response)


def download_test_maybank_request():
    client = BDLClient()
    response = client.get_all_downloadable_responses(
        request_identifier='uYKDBWuyqyWn')
    key = response.contains[0].key

    client.get_download_response(file_key=key)


def json_test_maybank_request():
    client = BDLClient()
    response = client.get_all_downloadable_responses(
        request_identifier='uYKDBWuyqyWn')
    key = response.contains[0].key

    print(client.get_json_response(file_key=key))


def get_maybank_response_from_name():
    client = BDLClient()
    print(client.get_response_by_request(request_identifier='uYKDBWuyqyWn'))
