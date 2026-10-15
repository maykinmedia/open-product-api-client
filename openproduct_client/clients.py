from typing import Any

from ape_pie import APIClient
from ape_pie.typing import ConfigAdapter

from .resources.product_type import (
    ContentLabelResource,
    PriceResource,
    ProductTypeResource,
    ThemeResource,
)


class BaseClient(APIClient):
    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        request_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        if request_kwargs is None:
            request_kwargs = {}
        if "headers" not in request_kwargs:
            request_kwargs["headers"] = {}
        if token:
            request_kwargs["headers"]["Authorization"] = f"Token {token}"

        # TODO
        # language is not supported in all the endpoints, it's ignored though
        if (lang_header_name := kwargs.get("language_header")) and (
            current_lang := kwargs.get("current_language")
        ):
            request_kwargs["headers"][lang_header_name] = current_lang

        super().__init__(base_url=base_url, request_kwargs=request_kwargs)

    @classmethod
    def configure_from(cls, adapter: ConfigAdapter, **kwargs):
        base_url = adapter.get_client_base_url()
        session_kwargs = adapter.get_client_session_kwargs()
        return cls(base_url, request_kwargs=session_kwargs, **kwargs)


class OpenProductClient(BaseClient):
    pass


class OpenProductTypeClient(BaseClient):
    product_type: ProductTypeResource
    theme: ThemeResource
    content_label: ContentLabelResource
    price: PriceResource

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        request_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        if request_kwargs is None:
            request_kwargs = {}
        if "headers" not in request_kwargs:
            request_kwargs["headers"] = {}
        if token:
            request_kwargs["headers"]["Authorization"] = f"Token {token}"

        # TODO
        # language is not supported in all the endpoints, it's ignored though
        if (lang_header_name := kwargs.get("language_header")) and (
            current_lang := kwargs.get("current_language")
        ):
            request_kwargs["headers"][lang_header_name] = current_lang

        super().__init__(base_url=base_url, request_kwargs=request_kwargs)

        self.theme = ThemeResource(self)
        self.content_label = ContentLabelResource(self)
        self.product_type = ProductTypeResource(self)
        self.price = PriceResource(self)
