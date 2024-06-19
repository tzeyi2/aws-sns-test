import logging
import os
import shutil
from json import JSONDecodeError
from urllib.parse import urljoin

from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests import RequestException
from requests_oauthlib import OAuth2Session

from explorers.bloomberg.bdl.resources.catalog import Catalog
from explorers.bloomberg.bdl.resources.field_list import (FieldListCollection,
                                                          FieldListCreate, FieldListPatch,
                                                          FieldListView)
from explorers.bloomberg.bdl.resources.request_response import RequestResponseView
from explorers.bloomberg.bdl.resources.security_request import (RequestCollectionView,
                                                                SecurityRequestCreate,
                                                                SecurityRequestPatch,
                                                                SecurityRequestViewAdapter)
from explorers.bloomberg.bdl.resources.triggers import (TriggerAdapterView,
                                                        TriggerCollection, TriggerCreate)
from explorers.bloomberg.bdl.resources.universe import (UniverseCollectionView,
                                                        UniverseCreate, UniversePatch,
                                                        UniverseView)

logger = logging.getLogger(__name__)


class BDLClient:
    BDL_CATALOG_ID = settings.BDL_ACCOUNT_ID

    def __init__(self, *args, **kwargs):
        client_id = settings.BDL_API_ACCESS_KEY
        client_secret = settings.BDL_API_SECRET
        oauth2_endpoint = settings.BDL_OAUTH_ENDPOINT

        host = kwargs.pop('host', None)
        if host:
            self.host = host
        else:
            self.host = settings.BDL_API_ENDPOINT

        session = kwargs.pop('session', None)
        if session:
            self.session = session
        else:
            self.session = OAuth2Session(
                client=BackendApplicationClient(client_id=client_id),
                auto_refresh_url=oauth2_endpoint,
                auto_refresh_kwargs={"client_id": client_id},
                token_updater=lambda x: x,
            )

            self.session.fetch_token(
                token_url=oauth2_endpoint, client_secret=client_secret
            )

        self.session.headers.update({"api-version": "2"})

    def _request(self, http_method, endpoint, query_params=None, json=None, **kwargs):
        full_endpoint = urljoin(self.host, endpoint)
        try:
            response = self.session.request(
                method=http_method, url=full_endpoint, params=query_params, json=json, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except (ValueError, JSONDecodeError) as e:
            logger.error(e)
        except RequestException:
            logger.error(response.json())

    def get(self, endpoint, query_params=None, json=None, **kwargs):
        return self._request("GET", endpoint, query_params, json, **kwargs)

    def post(self, endpoint: str, query_params=None, json=None, **kwargs, ):
        return self._request("POST", endpoint, query_params, json, **kwargs)

    def delete(self, endpoint: str, query_params=None, json=None, **kwargs):
        return self._request("DELETE", endpoint, query_params, json, **kwargs)

    def patch(self, endpoint: str, query_params=None, json=None, **kwargs):
        return self._request("PATCH", endpoint, query_params, json, **kwargs)

    def get_available_catalogs(self):
        response = self.get("eap/catalogs/")
        return Catalog(**response)

    def get_datasets_in_catalog(self, catalog_id=BDL_CATALOG_ID):
        response = self.get(f"eap/catalogs/{catalog_id}/")
        return response

    # Security Requests
    def get_all_security_requests(self, catalog_id=BDL_CATALOG_ID):
        response = self.get(f"eap/catalogs/{catalog_id}/requests/")

        return RequestCollectionView(**response)

    def get_per_security_request(self, request_name, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catalog_id}/requests/{request_name}")
        return SecurityRequestViewAdapter.validate_python(response)

    def create_per_security_request(self, request_object: SecurityRequestCreate, catalog_id=BDL_CATALOG_ID):
        response = self.post(
            f"eap/catalogs/{catalog_id}/requests/", json=request_object.model_dump_json_custom())
        return response

    def patch_security_request(self, request_name, patch: SecurityRequestPatch, catalog_id=BDL_CATALOG_ID):
        response = self.patch(
            f"eap/catalogs/{catalog_id}/requests/{request_name}", json=patch.model_dump_json_custom())
        return response

    def disable_security_request(self, request_name, catalog_id=BDL_CATALOG_ID):
        # A disable is PERMANENT, beware
        disable_patch = SecurityRequestPatch(enabled=False)
        return self.patch_security_request(catalog_id, request_name, disable_patch)

    def get_universe_for_security_request(self, request_name, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catalog_id}/requests/{request_name}/universe/")
        return UniverseView(**response)

    def get_field_list_for_security_request(self, request_name, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catalog_id}/requests/{request_name}/fieldList/")
        return FieldListView(**response)

    def get_trigger_for_security_request(self, request_name, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catalog_id}/requests/{request_name}/trigger/")
        return TriggerAdapterView.validate_python(response)

    def get_all_downloadable_responses(self, catalog_id=BDL_CATALOG_ID, prefix=None, limit=None, next_page=None,
                                       request_identifier=None, request_name=None, snapshot_start_datetime=None,
                                       snapshot_end_datetime=None):
        query_dict = {
            "prefix": prefix,
            "limit": limit,
            "next": next_page,
            "requestIdentifier": request_identifier,
            "requestName": request_name,
            "snapshotStartDateTime": snapshot_start_datetime,
            "snapshotEndDateTime": snapshot_end_datetime,
        }

        response = self.get(
            f"eap/catalogs/{catalog_id}/content/responses", query_params=query_dict)
        return RequestResponseView(**response)

    def get_response_by_request(self, request_identifier=None, request_name=None):
        """
        Returns JSON response if the file is JSON else downloads the file
        :param request_identifier:
        :param request_name:
        :return:
        """
        response = self.get_all_downloadable_responses(
            request_identifier=request_identifier, request_name=request_name)
        if not response.contains:
            logger.info('No responses found.')

        # this should only return 1 object
        response_object = response.contains[0]
        key = response_object.key
        header = response_object.headers

        if 'application/json' in header['Content-Type']:
            return self.get_json_response(key)

        else:
            return self.get_download_response(key)

    def get_json_response(self, file_key, catelog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catelog_id}/content/responses/{file_key}/")
        return response

    def get_download_response(self, file_key, catalog_id=BDL_CATALOG_ID):
        output_url = self.host + \
            f"/eap/catalogs/{catalog_id}/content/responses/{file_key}/"
        # - Download the file.
        with self.session.get(output_url, stream=True) as response:
            output_filename = file_key
            if 'content-encoding' in response.headers:
                if response.headers["content-encoding"] == "gzip":
                    output_filename = output_filename + '.gz'
                elif response.headers["content-encoding"] == "":
                    pass
                else:
                    raise RuntimeError(
                        'Unsupported content encoding received in the response')

            output_file_path = os.path.join(settings.BASE_DIR, output_filename)

            with open(output_file_path, 'wb') as output_file:
                logger.info(
                    'Loading file from: %s (can take a while) ...', output_url)
                shutil.copyfileobj(response.raw, output_file)

        logger.info('File downloaded: %s', output_filename)
        logger.debug('File location: %s', output_file_path)

    # Universe
    def get_all_per_security_universes(self, catalog_id=BDL_CATALOG_ID):
        response = self.get(f"eap/catalogs/{catalog_id}/universes/")
        return UniverseCollectionView(**response)

    def create_per_security_universe(self, universe: UniverseCreate, catalog_id=BDL_CATALOG_ID):
        response = self.post(
            f"eap/catalogs/{catalog_id}/universes/", json=universe.model_dump_json_custom())
        return response

    def get_per_security_universe(self, universe_identifier, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"/eap/catalogs/{catalog_id}/universes/{universe_identifier}/"
        )

        return UniverseView(**response)

    def update_per_security_universe(self, universe_identifier, universe_update: UniversePatch,
                                     catalog_id=BDL_CATALOG_ID):
        response = self.patch(f"eap/catalogs/{catalog_id}/universes/{universe_identifier}/",
                              json=universe_update.model_dump_json_custom())
        return response

    def delete_per_security_universe(self, universe_identifier, catalog_id=BDL_CATALOG_ID):
        response = self.delete(
            f"eap/catalogs/{catalog_id}/universes/{universe_identifier}/")
        return response

    # FieldList
    def get_all_field_lists(self, catalog_id=BDL_CATALOG_ID):
        response = self.get(f"/eap/catalogs/{catalog_id}/fieldLists/")
        return FieldListCollection(**response)

    def create_field_list(self, field_list: FieldListCreate, catalog_id=BDL_CATALOG_ID):
        response = self.post(
            f"/eap/catalogs/{catalog_id}/fieldLists/", json=field_list.model_dump_json_custom())
        return response

    def get_field_list(self, field_list_identifier, catalog_id=BDL_CATALOG_ID, page=None, page_size=None):
        query_dict = {
            'page': page,
            'pageSize': page_size,
        }
        response = self.get(
            f"/eap/catalogs/{catalog_id}/fieldLists/{field_list_identifier}/", query_params=query_dict)
        return FieldListView(**response)

    def update_field_list(self, field_list_identifier, patch_object: FieldListPatch, catalog_id=BDL_CATALOG_ID):
        response = self.patch(f"/eap/catalogs/{catalog_id}/fieldLists/{field_list_identifier}/",
                              json=patch_object.model_dump_json_custom())
        return response

    def delete_field_list(self, field_list_identifier, catalog_id=BDL_CATALOG_ID):
        response = self.delete(
            f"/eap/catalogs/{catalog_id}/fieldLists/{field_list_identifier}/")
        return response

    # Trigger Methods
    def list_all_triggers(self, catalog_id=BDL_CATALOG_ID, page=None, page_size=None):
        query_dict = {
            'page': page,
            'pageSize': page_size
        }

        response = self.get(
            f"eap/catalogs/{catalog_id}/triggers/", query_params=query_dict)
        return TriggerCollection(**response)

    def get_trigger(self, trigger_identifier, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catalog_id}/triggers/{trigger_identifier}")
        return TriggerAdapterView.validate_python(response)

    def create_trigger(self, trigger: TriggerCreate, catalog_id=BDL_CATALOG_ID):
        response = self.post(
            f"eap/catalogs/{catalog_id}/triggers/", json=trigger.dict_custom()
        )
        return response

    def delete_trigger(self, trigger_identifier, catalog_id=BDL_CATALOG_ID):
        response = self.delete(
            f"eap/catalogs/{catalog_id}/triggers/{trigger_identifier}"
        )
        return response

    def get_deleted_triggers(self, trigger_identifier, catalog_id=BDL_CATALOG_ID):
        response = self.get(
            f"eap/catalogs/{catalog_id}/deleted/triggers/{trigger_identifier}/"
        )
        return response
