import uuid
from collections.abc import Sequence

from ape_pie import APIClient

from ...typing import PaginatedResponseBody
from ..base import BaseResourceMixin
from .types import ContentParams, ProductType, ProductTypeContent, ProductTypeParams


class ProductTypeResource(BaseResourceMixin):
    http_client: APIClient
    base_path: str = "producttypen"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_iter = self._make_list_iter(self.list)

    def list(
        self, *, params: ProductTypeParams | None = None
    ) -> PaginatedResponseBody[ProductType]:
        """
        Get all the available product types (based on query parameters).
        """
        response = self._get(self.base_path, params=params)
        return self.process_response(response)

    def retrieve(self, /, uuid: str | uuid.UUID) -> ProductType:
        """
        Get a specific product type based on its uuid.
        """
        response = self._get(f"{self.base_path}/{uuid!s}")
        return self.process_response(response)

    def list_content(
        self, uuid: str | uuid.UUID, *, params: ContentParams | None = None
    ) -> Sequence[ProductTypeContent]:
        """
        Get the content of a product type based on uuid (and query parameters).
        """
        response = self._get(f"{self.base_path}/{uuid!s}/content", params=params)
        return self.process_response(response)
