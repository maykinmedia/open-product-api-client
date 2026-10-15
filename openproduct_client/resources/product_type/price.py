from ape_pie import APIClient

from ...typing import PaginatedResponseBody
from ..base import BaseResourceMixin
from .types import Price, PriceParams


class PriceResource(BaseResourceMixin):
    http_client: APIClient
    base_path: str = "prijzen"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_iter = self._make_list_iter(self.list)

    def list(
        self, *, params: PriceParams | None = None
    ) -> PaginatedResponseBody[Price]:
        """
        Get all the available prices (based on query parameters).
        """
        breakpoint()
        response = self._get(self.base_path, params=params)
        return self.process_response(response)
