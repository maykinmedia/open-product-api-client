from collections.abc import Sequence

from ape_pie import APIClient

from ..base import BaseResourceMixin
from .types import ContentThemeParams, Theme, ThemeParams


class ThemeResource(BaseResourceMixin):
    http_client: APIClient
    base_path: str = "themas"

    def list(self, *, params: ThemeParams | None = None) -> Sequence[Theme]:
        """
        Get all the available themes (based on query parameters).
        """
        response = self._get(self.base_path, params=params)
        return self.process_response(response)

    def get_content(self, *, theme_uuid: str, params: ContentThemeParams | None = None):
        """
        Get the content of a specific theme based on its uuid (and query paramaters).
        """
        endpoint = f"{self.base_path}/{theme_uuid}/content-elementen"
        response = self._get(endpoint, params=params)
        return self.process_response(response)
