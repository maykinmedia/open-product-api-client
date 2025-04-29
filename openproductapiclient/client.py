import logging
from typing import Tuple
from urllib.parse import urljoin
from .utils import get_filled_params

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

    def __make_get_request(self, client, url, **kwargs):
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

    def __products_api_get_request(self, url, **kwargs):
        """
        Retrieves products from products API.
        Filter-arguments can be passed as kwargs.
        """

        client = self.open_product_api_client
        response = self.__make_get_request(client, url, **kwargs)

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch products API."
        return results

    def get_products(
        self,
        *,
        aanmaak_datum: str | None = None,
        aanmaak_datum__gte: str | None = None,
        aanmaak_datum__lte: str | None = None,
        dataobject_attr: str | None = None,
        documenten__uuid: str | None = None,
        eind_datum: str | None = None,
        eind_datum__gte: str | None = None,
        eind_datum__lte: str | None = None,
        frequentie: str | None = None,
        gepubliceerd: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
        prijs: float | None = None,
        prijs_gte: float | None = None,
        prijs_lte: float | None = None,
        producttype__code: str | None = None,
        producttype__naam: str | None = None,
        producttype__uuid: str | None = None,
        start_datum: str | None = None,
        start_datum_gte: str | None = None,
        start_datum_lte: str | None = None,
        status: str | None = None,
        uniforme_product_naam: str | None = None,
        update_datum: str | None = None,
        update_datum__gte: str | None = None,
        update_datum__lte: str | None = None,
        verbruiksobject_attr: str | None = None,
    ) -> list:
        """
        Retrieves products from products API.
        """

        params = get_filled_params(locals())
        return self.__products_api_get_request("producten", **params)

    def get_product(self, uuid):
        """
        Retrieves a product from products API.
        Filter-arguments can be passed as kwargs.
        """

        return self.__products_api_get_request(f"producten/{uuid}/")

    # **************************
    # Product Type API endpoints
    # **************************

    def __producttypes_api_get_request(self, url, **kwargs):
        """
        Retrieves products from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        client = self.open_product_types_api_client
        response = self.__make_get_request(client, url, **kwargs)

        response.raise_for_status()
        results = response.json()

        if not results:
            return "Failed to fetch producttypes API."
        return results

    def get_product_types(
        self,
        *,
        aanmaak_datum: str | None = None,
        aanmaak_datum_gte: str | None = None,
        aanmaak_datum_lte: str | None = None,
        code: str | None = None,
        externe_code: str | None = None,
        gepubliceerd: bool | None = None,
        keywords: list[str] | None = None,
        letter: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        parameter: str | None = None,
        processen__uuid: str | None = None,
        toegestane_statussen: list[str] | None = None,
        uniforme_product_naam: str | None = None,
        update_datum: str | None = None,
        update_datum__gte: str | None = None,
        update_datum__lte: str | None = None,
        verbruiksobject_schema_naam: str | None = None,
        verzoektypen__uuid: str | None = None,
        zaaktypen__uuid: str | None = None,
    ) -> list:
        """
        Retrieves all product types from producttypes API.
        """

        params = get_filled_params(locals())
        return self.__producttypes_api_get_request("producttypen", **params)

    def get_product_type(self, uuid):
        """
        Retrieves a specific product type from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        return self.__producttypes_api_get_request(f"producttypen/{uuid}/")

    def get_themes(
        self,
        *,
        aanmaak_datum: str | None = None,
        aanmaak_datum__gte: str | None = None,
        aanmaak_datum__lte: str | None = None,
        gepubliceerd: bool | None = None,
        hoofd_thema__naam: str | None = None,
        hoofd_thema__uuid: str | None = None,
        naam: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        update_datum: str | None = None,
        update_datum__gte: str | None = None,
        update_datum__lte: str | None = None,
    ) -> list:
        """
        Retrieves all themes from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        params = get_filled_params(locals())
        return self.__producttypes_api_get_request("themas", **params)

    def get_theme(self, uuid, **kwargs):
        """
        Retrieves a theme from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        return self.__producttypes_api_get_request(f"themas/{uuid}/")

    def get_organizations(
        self,
        *,
        code: str | None = None,
        email__iexact: str | None = None,
        huisnummer__iexact: str | None = None,
        naam__iexact: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        postcode: str | None = None,
        stad: str | None = None,
        straat__iexact: str | None = None,
        telefoonnummer__contains: str | None = None,
    ) -> list:
        """
        Retrieves all organizations from producttypes API.
        Filter-arguments can be passed as kwargs.
        """

        params = get_filled_params(locals())
        return self.__producttypes_api_get_request("organisaties", **params)
