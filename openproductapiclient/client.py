import logging
from typing import Tuple
from urllib.parse import urljoin

from requests.exceptions import HTTPError
from zgw_consumers.client import build_client as build_zgw_client

from .utils import (
    ListProductsParams,
    ListProductTypesParams,
    ListThemesParams,
    ListOrganizationsParams,
    format_list_params,
)
import uuid
from zgw_consumers import service

logger = logging.getLogger(__name__)


class OpenProductClient:
    def __init__(
        self, open_product_api_service: service, open_product_types_api_client: service
    ):
        self.open_product_api_client = build_zgw_client(
            service=open_product_api_service
        )
        self.open_product_types_api_client = build_zgw_client(
            service=open_product_types_api_client
        )

    def is_healthy(self) -> Tuple[bool, str]:
        """
        Checks whether the API(s) are functioning
         properly using test-requests.
        """

        try:
            products_response = self.open_product_api_client.head("")
            producttypes_response = self.open_product_types_api_client.head("sdd")

            if products_response.ok and producttypes_response.ok:
                return True
        except HTTPError as e:
            logger.warning(f"Server did not return a valid response ({e}).")

        return False, "Server did not return a valid response."

    def _make_get_request(self, client, url, **kwargs):
        """
        Makes a get request to a given client with
        a given url and arguments.
        """

        return client.request(
            "get",
            urljoin(base=client.base_url, url=url),
            params=kwargs,
        )

    # **************************
    # Product API endpoints
    # **************************

    def _products_api_get_request(self, url, **kwargs):
        """
        Retrieves products from products API.
        Filter-arguments can be passed as kwargs.
        """

        client = self.open_product_api_client
        response = self._make_get_request(client, url, **kwargs)

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch products API."
        return results

    def list_products(self, **params: ListProductsParams) -> list:
        """
        Retrieves products from products API.
        """

        formatted_params = format_list_params(params)

        return self._products_api_get_request("producten", **formatted_params)

    def retrieve_product(self, uuid: str | uuid.UUID):
        """
        Retrieves a product from products API.
        Filter-arguments can be passed as kwargs.
        """

        return self._products_api_get_request(f"producten/{uuid}/")

    # **************************
    # Product Type API endpoints
    # **************************

    def _producttypes_api_get_request(self, url, **kwargs):
        """
        Retrieves products from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        client = self.open_product_types_api_client
        response = self._make_get_request(client, url, **kwargs)

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch producttypes API."
        return results

    def list_product_types(self, **params: ListProductTypesParams) -> list:
        """
        Retrieves all product types from producttypes API.
        """

        formatted_params = format_list_params(params)
        return self._producttypes_api_get_request("producttypen", **formatted_params)

    def retrieve_product_type(self, uuid: str | uuid.UUID):
        """
        Retrieves a specific product type from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        return self._producttypes_api_get_request(f"producttypen/{uuid}/")

    def list_themes(self, **params: ListThemesParams) -> list:
        """
        Retrieves all themes from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        formatted_params = format_list_params(params)
        return self._producttypes_api_get_request("themas", **formatted_params)

    def retrieve_theme(self, uuid: str | uuid.UUID, **kwargs):
        """
        Retrieves a theme from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        return self._producttypes_api_get_request(f"themas/{uuid}/")

    def list_organizations(self, **params: ListOrganizationsParams) -> list:
        """
        Retrieves all organizations from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        formatted_params = format_list_params(params)
        return self._producttypes_api_get_request("organisaties", **formatted_params)
