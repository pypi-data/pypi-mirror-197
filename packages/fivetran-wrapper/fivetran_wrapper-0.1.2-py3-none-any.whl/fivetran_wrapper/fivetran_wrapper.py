"""
Wrapper for simple and easy interaction with Fivetran service API
"""
from typing import Optional
import logging
from requests import request, Response
from requests.auth import HTTPBasicAuth
from error_wrapper import ErrorWrapper
from .constant_sets import ReturnCodes, ResponseKeys, DataKeys


COMPLETE_STATUSES = (200, 201)
REQUEST_HEADERS = {'Content-Type': 'application/json'}


class BaseFivetranWrapper(ErrorWrapper):
    """
    Base wrapper with init and API request method
    """
    response: Optional[Response] = None
    data: Optional[dict] = None
    request_url: Optional[str] = None
    return_code: Optional[str] = None
    return_message: Optional[str] = None
    cursor: Optional[str] = None

    def __init__(self,
                 base_url: str,
                 api_key: str,
                 api_secret: str,
                 report_prefix: str = None,
                 exception_name_in_detail: bool = False,
                 logger: Optional[logging.Logger] = None,
                 auto_logging: bool = False,):
        super().__init__(
            report_prefix, exception_name_in_detail, logger, auto_logging)
        self.headers = REQUEST_HEADERS
        self.base_url = base_url
        self._auth = HTTPBasicAuth(api_key, api_secret)

    def clear_instance(self):
        """
        Clear API request life cycle variables and state flags. Uses before
        each request
        :return:
        """
        self.clear_instance_error()
        self.data = None
        self.request_url = None
        self.return_code = None
        self.return_message = None
        self.cursor = None

    def api_request(self, method: str, entry_point: str, **kwargs):
        """
        API request and handle exceptions, errors and response data
        :param method: HTTP method
        :param entry_point: API entry point
        :param kwargs:
        :return:
        """
        self.clear_instance()
        try:
            self.response = request(
                method=method,
                url=f'{self.base_url}/{entry_point}',
                headers=self.headers,
                auth=self._auth,
                **kwargs
            )
        except Exception as e:
            self.raise_instance_exception(e)
        else:
            self.request_url = f'{method.upper()} {self.response.request.url}'
            try:
                data = self.response.json()
            except Exception as e:
                self.raise_instance_exception(e)
            else:
                if data is None:
                    self.raise_instance_error(
                        f'Service return {self.response.status_code} '
                        f'and no data!')
                else:
                    self.return_code = data.get(ResponseKeys.CODE.value)
                    self.return_message = data.get(ResponseKeys.MESSAGE.value)
                    if self.return_code is None:
                        self.raise_instance_error(
                            f'Service return {self.response.status_code} '
                            f'and not recognized data: {data}')
                    elif self.return_code == ReturnCodes.SUCCESS.value:
                        self.data = data.get(ResponseKeys.DATA.value)
                        if self.data is not None:
                            self.cursor = self.data.get(DataKeys.CURSOR.value)
                    else:
                        self.raise_instance_error(
                            f"Service return {self.response.status_code}, "
                            f"data code: {self.return_code}, "
                            f"message: {self.return_message}")


class FivetranWrapperPropertyGroup:

    def __init__(self, wrapper: BaseFivetranWrapper):
        self._wrapper = wrapper


class FivetranWrapperConnectorTypes(FivetranWrapperPropertyGroup):

    def paginated_list(self, cursor: str = None, limit: int = None):
        """
        Returns all available source types within your Fivetran account
        :param cursor: The paging cursor
        :param limit: The number of records to fetch per page, accepts a number
        in the range 1..1000. The default value is 100
        :return:
        """
        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = limit
        self._wrapper.api_request(
            'GET', 'metadata/connector-types', params=params)

    def get(self, connector_type_id: str):
        """
        Returns metadata of configuration parameters and authorization
        parameters for a specified connector type
        :param connector_type_id:
        :return: The connector type identifier within the Fivetran system
        """
        self._wrapper.api_request(
            'GET', f'metadata/connector-types/{connector_type_id}')


class FivetranWrapperGroups(FivetranWrapperPropertyGroup):

    def paginated_list(self, cursor: str = None, limit: int = None):
        """
        Returns a list of all groups within your Fivetran account
        :param cursor: The paging cursor
        :param limit: The number of records to fetch per page, accepts a number
        in the range 1..1000. The default value is 100
        :return:
        """
        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = limit
        self._wrapper.api_request('GET', 'groups', params=params)

    def new(self, name: str):
        """
        Creates a new group in your Fivetran account
        :param name: group name
        :return: Dict with new group properties
        """
        self._wrapper.api_request('POST', 'groups', json={'name': name})

    def get(self, group_id: str):
        """
        Returns a group object if a valid identifier was provided
        :param group_id: The unique identifier for the group within the
        Fivetran system
        :return:
        """
        self._wrapper.api_request('GET', f'groups/{group_id}')

    def delete(self, group_id: str):
        """
        Deletes a group from your Fivetran account
        :param group_id: The unique identifier for the group within your
        Fivetran account
        :return:
        """
        self._wrapper.api_request('DELETE', f'groups/{group_id}')

    def patch(self, group_id: str, name: str):
        """
        Updates information for an existing group within your Fivetran account
        :param group_id: The unique identifier for the group within the
        Fivetran system
        :param name: The group name within the account. The name must start
        with a letter or underscore and can only contain letters, numbers, or
        underscores
        :return:
        """
        self._wrapper.api_request(
            'PATCH', f'groups/{group_id}', json={'name': name})


class FivetranWrapperDestinations(FivetranWrapperPropertyGroup):

    def new(self, destination_data: dict):
        """
        Creates a new destination within a specified group in your Fivetran
        account
        :param destination_data: Destination config
        :return:
        """
        self._wrapper.api_request(
            'POST', 'destinations', json=destination_data)

    def get(self, destination_id: str):
        """
        Returns a destination object if a valid identifier was provided
        :param destination_id: The unique identifier for the destination
        within your Fivetran account
        :return:
        """
        self._wrapper.api_request('GET', f'destinations/{destination_id}')

    def delete(self, destination_id: str):
        """
        Deletes a destination from your Fivetran account
        :param destination_id: The unique identifier for the destination
        within your Fivetran account
        :return:
        """
        self._wrapper.api_request('DELETE', f'destinations/{destination_id}')

    def patch(self, destination_id: str, destination_data: dict):
        """
        Updates information for an existing destination within your Fivetran
        account
        :param destination_id: The unique identifier for the destination
        within your Fivetran account
        :param destination_data: Config changes
        :return:
        """
        self._wrapper.api_request(
            'PATCH', f'destinations/{destination_id}', json=destination_data)

    def start_tests(self, destination_id: str, trust_certificates: bool = True,
                    trust_fingerprints: bool = True):
        """
        Runs the setup tests for an existing destination within your Fivetran account
        :param destination_id: The unique identifier for the destination
        within your Fivetran account
        :param trust_certificates: Specifies whether we should trust the
        certificate automatically. The default value is FALSE.
        :param trust_fingerprints: Specifies whether we should trust the SSH
        fingerprint automatically. The default value is FALSE
        :return:
        """
        self._wrapper.api_request(
            'POST',
            f'destinations/{destination_id}/test',
            json={"trust_certificates": trust_certificates,
                  "trust_fingerprints": trust_fingerprints}
        )


class FivetranWrapperConnectors(FivetranWrapperPropertyGroup):

    def paginated_list(self, group_id: str, cursor: str = None,
                       limit: int = None, schema: str = None):
        """
        :param group_id:
        :param cursor: The paging cursor
        :param limit: The number of records to fetch per page, accepts a number
        in the range 1..1000. The default value is 100
        :param schema: optional filter. When used, the response will only
        contain information for the connector with the specified schema
        :return:
        """
        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = limit
        if schema:
            params['schema'] = schema
        self._wrapper.api_request(
            'GET', f'groups/{group_id}/connectors', params=params)

    def new(self, connector_data: dict):
        """
        Creates a new connector within a specified group in your Fivetran
        account. Runs setup tests and returns testing results
        :param connector_data: Connector config
        :return:
        """
        self._wrapper.api_request('POST', 'connectors', json=connector_data)

    def patch(self, connector_id: str, connector_data: dict):
        """
        Updates the information for an existing connector within your Fivetran
        account
        :param connector_id: The unique identifier for the connector within
        the Fivetran system
        :param connector_data: Config changes
        :return:
        """
        self._wrapper.api_request(
            'PATCH', f'connectors/{connector_id}', json=connector_data)

    def sync(self, connector_id: str, force: bool = False):
        """
        Triggers a data sync for an existing connector within your Fivetran
        account without waiting for the next scheduled sync
        :param connector_id: The unique identifier for the connector within
        the Fivetran system
        :param force: If force is true and the connector is currently syncing,
        it will stop the sync and re-run it. If force is false, the connector
        will sync only if it isn't currently syncing. The default value
        is false
        :return:
        """
        self._wrapper.api_request('POST', f'connectors/{connector_id}/sync',
                                  json={'force': force})

    def resync(self, connector_id: str, scope: dict = None):
        """
        Triggers a full historical sync of a connector or multiple schema
        tables within a connector
        :param connector_id: The unique identifier for the connector within
        the Fivetran system
        :param scope: A map containing an array of tables to re-sync for each
        schema, must be non-empty. The parameter is optional
        :return:
        """
        self._wrapper.api_request('POST', f'connectors/{connector_id}/resync',
                                  json={'scope': scope} if scope else None)

    def get(self, connector_id: str):
        """
        Returns a connector object if a valid identifier was provided
        :param connector_id: The unique identifier for the connector within
        the Fivetran system
        :return:
        """
        self._wrapper.api_request('GET', f'connectors/{connector_id}')

    def connect_card(self, connector_id: str, redirect_uri: str,
                     hide_setup_guide: bool = True):
        """
        Connect Cards are embeddable pop-up windows that collect credentials
        directly from your end users to set up Fivetran connectors
        :param connector_id: The unique identifier for the connector within
        the Fivetran system
        :param redirect_uri: The URI on your site where we will redirect the
        end user after successful setup. The URI must start with the https or
        http prefix
        :param hide_setup_guide: An optional parameter that lets you hide the
        embedded setup guide in the Connect Card window
        :return:
        """
        self._wrapper.api_request(
            'POST', f'connectors/{connector_id}/connect-card',
            json={
                'connect_card_config': {
                    'redirect_uri': redirect_uri,
                    'hide_setup_guide': hide_setup_guide
                    }
            }
        )

    def remove(self, connector_id: str):
        """
        Deletes a connector from your Fivetran account
        :param connector_id: The unique identifier for the connector within
        the Fivetran system
        :return:
        """
        self._wrapper.api_request('DELETE', f'connectors/{connector_id}')


class FivetranWrapper(BaseFivetranWrapper):

    def __init__(self,
                 base_url: str,
                 api_key: str,
                 api_secret: str,
                 report_prefix: str = None,
                 exception_name_in_detail: bool = False,
                 logger: Optional[logging.Logger] = None,
                 auto_logging: bool = False,):
        super().__init__(
            base_url, api_key, api_secret, report_prefix,
            exception_name_in_detail, logger, auto_logging
        )
        self._connectors = FivetranWrapperConnectors(self)
        self._groups = FivetranWrapperGroups(self)
        self._destinations = FivetranWrapperDestinations(self)
        self._connector_types = FivetranWrapperConnectorTypes(self)

    @property
    def connectors(self):
        """
        Get connector management methods
        :return:
        """
        return self._connectors

    @property
    def groups(self):
        """
        Get group management methods
        :return:
        """
        return self._groups

    @property
    def destinations(self):
        """
        Get destination management methods
        :return:
        """
        return self._destinations

    @property
    def connector_types(self):
        """
        Get connector metadata management methods
        :return:
        """
        return self._connector_types
