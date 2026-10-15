from ape_pie import APIClient

from ...typing import PaginatedResponseBody, PaginationParams
from ..base import BaseResourceMixin
from .types import ContentLabels


class ContentLabelResource(BaseResourceMixin):
    http_client: APIClient
    base_path: str = "contentlabels"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_iter = self._make_list_iter(self.list)

    def list(
        self, *, params: PaginationParams | None = None
    ) -> PaginatedResponseBody[ContentLabels]:
        """
        Get all the available content labels (based on query parameters).
        """
        response = self._get(self.base_path, params=params)
        return self.process_response(response)
