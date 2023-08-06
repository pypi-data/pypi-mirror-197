import base64
import platform
from abc import ABC, abstractmethod
from typing import Dict, List

from gql import Client, gql
from gql.transport.exceptions import TransportServerError
from gql.transport.requests import RequestsHTTPTransport

from fir_api_cli import __app_name__, version

from .constants import FIR_API_URL, RETURN_ITEMS_LONG, RETURN_ITEMS_SHORT


def create_gql_client(url: str,
                      headers: Dict = None,
                      verify: bool = True,
                      retries: int = 3):
    """Create a gql client."""

    transport = RequestsHTTPTransport(
        url=url, headers=headers, verify=verify, retries=retries)

    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client


class Query(ABC):
    """Query interface."""

    def __init__(self, verbose: bool = False):
        if verbose:
            return_items = RETURN_ITEMS_LONG
        else:
            return_items = RETURN_ITEMS_SHORT
        self._return_items = return_items

    @abstractmethod
    def get_response(self,
                     client: Client,
                     query_parameters: Dict) -> List[Dict]:
        """Request response from GraphQL API endpoint."""


class ProductQuery(Query):
    """Class for defining queries for individual product."""

    def _get_query(self, query_parameters: Dict) -> str:

        product_filter = []

        for key, value in query_parameters.items():
            funct = self.MAPPER.get(key)
            if funct:
                product_filter.append(funct(self, value))
        return "{product(%s) {%s}}" % (
            ' '.join(product_filter), ' '.join(self._return_items)
        )

    def get_response(
            self,
            client: Client,
            query_parameters: Dict) -> List[Dict]:
        """Get response from the API with query parameters."""

        query = self._get_query(query_parameters)
        try:
            result = client.execute(gql(query))
        except TransportServerError as exc:
            raise exc

        return result

    def id_filter(self, id: str) -> str:
        """Product ID filter for API request."""
        return 'id: "%s"' % (id)

    @property
    def valid_query_parameters(self):
        return list(self.MAPPER.keys())

    MAPPER = {
        'id': id_filter
    }


class ProductsQuery(Query):
    """Class for defining queries for products."""

    def _get_query(self, query_parameters: Dict, end_cursor: str = None) -> str:

        product_filter = []

        if end_cursor:
            after = 'after: "%s"' % (end_cursor)
        else:
            after = ''

        for key, value in query_parameters.items():
            funct = self.MAPPER.get(key)
            if funct:
                product_filter.append(funct(self, value))
        return ("{products(first: 500 %s %s orderBy: { beginPosition: ASC }) "
                "{items{%s} totalCount pageInfo{hasNextPage hasPreviousPage "
                "startCursor endCursor}}}" % (
                    after, ' '.join(product_filter),
                    ' '.join(self._return_items))
                )

    def get_response(
            self,
            client: Client,
            query_parameters: Dict) -> List[Dict]:
        """Get response from the API with query parameters."""

        page_next = True
        end_cursor = None
        while page_next:
            query = self._get_query(query_parameters, end_cursor=end_cursor)
            try:
                result = client.execute(gql(query))
            except TransportServerError as exc:
                raise exc

            page_info = result['products']['pageInfo']
            end_cursor = page_info.get('endCursor')

            yield result
            page_next = page_info.get('hasNextPage')

    def platform_filter(self, platform: str) -> str:
        """Platform filter for API request."""
        return 'platformName: {equalsTo: "%s"}' % (platform)

    def begin_filter(self, date: str) -> str:
        """Begin position filter for API request."""
        return 'beginPosition: {greaterThanOrEqualsTo: "%s"}' % (date)

    def end_filter(self, date: str) -> str:
        """End position filter for API request."""
        return 'endPosition: {lessThanOrEqualsTo: "%s"}' % (date)

    def type_filter(self, product_type: str) -> str:
        """Product type filter for API request."""
        return 'productType: {equalsTo: "%s"}' % (product_type)

    def cloud_filter(self, ccover: float) -> str:
        """Cloud cover filter for API request."""
        return 'cloudCoverPercentage: {lessThanOrEqualsTo: %s}' % (ccover)

    def tile_filter(self, tile: str) -> str:
        """Tile number filter for API request."""
        return 'tileIdentifier: {equalsTo: "%s"}' % (tile)

    def relorbit_filter(self, orbit: int) -> str:
        """Relative orbit number filter for API request."""
        return 'relativeOrbitNumber: {equalsTo: %s}' % (orbit)

    @property
    def valid_query_parameters(self):
        return list(self.MAPPER.keys())

    MAPPER = {
        'platform': platform_filter,
        'begin_position': begin_filter,
        'end_position': end_filter,
        'product_type': type_filter,
        'cloud_cover': cloud_filter,
        'tile': tile_filter,
        'relative_orbit': relorbit_filter,
    }


class FIRHandler:
    """
    Main class for handling operations with the FIR API service.
    """

    def __init__(self, username: str, password: str, query_type: Query):
        self._url = FIR_API_URL
        self._username = username
        self._password = password
        self._query_type = query_type
        self._query_parameters = {}

        headers = self.get_headers()
        self._client = create_gql_client(self._url, headers)

    def create_query_parameters(self, query_param: Dict) -> None:
        """
        Creates a list of query parameters.

        Args:
            query_param (Dict): Key, value pairs of query parameters
                e.g. {'platform': 'Sentinel-2'}.
        """
        for k in query_param:
            if k not in self._query_type.valid_query_parameters:
                raise ValueError(f'Invalid parameter: {k}')
            self._query_parameters[k] = query_param.get(k)

    def query(self) -> Dict:
        """Return post request content based on query parameters."""

        try:
            response = self._query_type.get_response(
                self._client, query_parameters=self.query_parameters)
        except TransportServerError as exc:
            raise exc

        return response

    def get_headers(self, encoding: str = 'utf-8') -> Dict:
        """Return headers dictionary with authentication entry."""

        auth_string = base64.b64encode(
            f'{self._username}:{self._password}'.encode(encoding))
        auth_header = {
            'Authorization': f"Basic {auth_string.decode(encoding)}"}

        return {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': f'{__app_name__}/{version} '
                          f'{platform.python_implementation()}/'
                          f'{platform.python_version()} '
                          f'{platform.system()}/{platform.version()}',
            **auth_header
        }

    @property
    def url(self):
        """Return the url."""
        return self._url

    @property
    def query_parameters(self):
        """Return the query parameters."""
        return self._query_parameters
