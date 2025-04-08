import logging
from typing import Tuple
from urllib.parse import urljoin

from requests.exceptions import HTTPError

from zgw_consumers.client import build_client as build_zgw_client

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, open_product_api_service, open_product_types_api_client):
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
            # TODO: Actually do this
            # We do a head request to actually hit a protected endpoint without
            # getting a whole bunch of data.
            self.get_products()
            self.get_product_types()
            return (True, "")
        except HTTPError as e:
            message = f"Server did not return a valid response ({e})."
        except Exception as e:
            logger.exception(e)
            message = str(e)

        return (False, message)

    # **************************
    # Product API endpoints
    # **************************

    def __products_api_get_request(self, url, **kwargs):
        """
        Retrieves products from products API.
        Filter-arguments can be passed as kwargs.
        """

        response = self.open_product_api_client.request(
            "get",
            urljoin(base=self.open_product_api_client.base_url, url=url),
            params=kwargs,
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch products API."
        return results

    # def get_products(self, *, aanmaak_datum: str|None = None) -> list:
    def get_products(self, **kwargs) -> list:
        """
        Retrieves products from products API.
        Filter-arguments can be passed as kwargs.
        """

        results = self.__products_api_get_request("producten", **kwargs)

        if not results:
            return "Failed to fetch products API."
        return results

    def get_product(self, id, **kwargs):
        """
        Retrieves a product from products API.
        Filter-arguments can be passed as kwargs.
        """

        results = self.__products_api_get_request(f"producten/{id}/", **kwargs)

        if not results:
            return "Failed to fetch products API."
        return results

    # **************************
    # Product Type API endpoints
    # **************************

    def get_product_types(self, **kwargs) -> list:
        """
        Retrieves all product types from producttypes API.
        Filter-argumentscan be passed as kwargs.
        """

        response = self.open_product_types_api_client.request(
            "get",
            urljoin(
                base=self.open_product_types_api_client.base_url, url="producttypen"
            ),
            params=kwargs,
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch producttypes API."
        return results

    def get_product_type(self, id, **kwargs):
        """
        Retrieves a specific product type from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        response = self.open_product_types_api_client.request(
            "get",
            urljoin(
                base=self.open_product_types_api_client.base_url,
                url=f"producttypen/{id}/",
            ),
            params=kwargs,
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch producttype from producttypes API."
        return results

    def get_themes(self, **kwargs) -> list:
        """
        Retrieves all themes from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        response = self.open_product_types_api_client.request(
            "get",
            urljoin(
                base=self.open_product_types_api_client.base_url,
                url="themas",
            ),
            params=kwargs,
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch themes from producttypes API."
        return results

    def get_theme(self, id, **kwargs):
        """
        Retrieves a theme from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        response = self.open_product_types_api_client.request(
            "get",
            urljoin(
                base=self.open_product_types_api_client.base_url,
                url=f"themas/{id}",
            ),
            params=kwargs,
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch theme from producttypes API."
        return results

    def get_organizations(self, **kwargs) -> list:
        """
        Retrieves all organizations from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        response = self.open_product_types_api_client.request(
            "get",
            urljoin(
                base=self.open_product_types_api_client.base_url,
                url="organisaties",
            ),
            params=kwargs,
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch organizations from producttypes API."
        return results
