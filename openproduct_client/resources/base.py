from __future__ import annotations

import json
import logging
from collections.abc import Callable, Generator, Mapping
from typing import Any, ParamSpec, TypeVar

import requests
from ape_pie import APIClient
from msgspec import Struct, structs

from ..exceptions import (
    BadRequest,
    Forbidden,
    InvalidJSONResponse,
    NonJSONResponse,
    NotFound,
    ResponseError,
    StructuredErrorResponse,
    Unauthorized,
)
from ..typing import PaginatedResponseBody

logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


def _is_error_response(data: Any) -> bool:
    """Check if response data matches error response structure."""
    if not isinstance(data, dict):
        return False
    required_keys = {"type", "code", "title", "status", "detail", "instance"}
    return required_keys.issubset(data.keys())


def _is_validation_error_response(data: Any) -> bool:
    """Check if response data matches validation error response structure."""
    if not _is_error_response(data):
        return False
    return data.get("status") == 400 and "invalidParams" in data


class BaseResourceMixin[T]:
    http_client: APIClient

    def __init__(self, http_client: APIClient):
        self.http_client = http_client

    @staticmethod
    def process_response(response: requests.Response) -> T:
        response_data = None
        try:
            content_type = response.headers.get("Content-Type", "")

            if not content_type.lower().startswith("application/json"):
                raise NonJSONResponse(response)

            response_data = response.json()
        except (requests.exceptions.JSONDecodeError, json.JSONDecodeError) as exc:
            raise InvalidJSONResponse(response) from exc

        match response.status_code:
            case code if code >= 200 and code < 300 and response_data:
                return response_data
            case code if code >= 400 and code < 500 and response_data:
                exc_class = StructuredErrorResponse
                is_valid_error = _is_error_response(response_data)

                match code:
                    case 400:
                        if _is_validation_error_response(response_data):
                            raise BadRequest(response, response_data)
                        exc_class = BadRequest
                    case 401:
                        exc_class = Unauthorized
                    case 403:
                        exc_class = Forbidden
                    case 404:
                        exc_class = NotFound
                    case _:
                        pass

                if is_valid_error:
                    raise exc_class(response, response_data)
                # JSON body, but not in expected schema. Fall through to
                # generic ErrorResponse
            case _:
                pass

        raise ResponseError(response, msg="Error response")

    def _paginator(
        self,
        paginated_data: PaginatedResponseBody[T],
        max_requests: int | None = None,
    ) -> Generator[T, Any, None]:
        def row_iterator(
            _data: PaginatedResponseBody[T], num_requests=0
        ) -> Generator[T, Any, None]:
            yield from _data["results"]

            if next_url := _data.get("next"):
                if max_requests and num_requests >= max_requests:
                    logger.info(
                        "Number of requests while retrieving paginated "
                        "results reached maximum (%s), returning results. "
                        "Next URL: %s",
                        max_requests,
                        next_url,
                    )
                    return

                response = self.http_client.get(next_url)
                num_requests += 1
                response.raise_for_status()
                data = response.json()

                yield from row_iterator(data, num_requests)

        return row_iterator(paginated_data)

    def _get(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Struct | None = None,
    ) -> requests.Response:
        query_params = structs.asdict(params) if params else None
        return self.http_client.request(
            "get", path, headers=headers, params=query_params
        )

    def _post(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Struct | None = None,
        data: Any = None,
    ) -> requests.Response:
        query_params = structs.asdict(params) if params else None
        return self.http_client.request(
            "post",
            path,
            headers=headers,
            json=data,
            params=query_params,
        )

    def _put(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Struct | None = None,
        data: Any = None,
    ) -> requests.Response:
        query_params = structs.asdict(params) if params else None
        return self.http_client.request(
            "put", path, headers=headers, json=data, params=query_params
        )

    def _delete(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Struct | None = None,
    ) -> requests.Response:
        query_params = structs.asdict(params) if params else None
        return self.http_client.request(
            "delete",
            path,
            headers=headers,
            params=query_params,
        )

    def _patch(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Struct | None = None,
        data: Any = None,
    ) -> requests.Response:
        query_params = structs.asdict(params) if params else None
        return self.http_client.request(
            "patch",
            path,
            headers=headers,
            params=query_params,
            json=data,
        )

    def _options(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Struct | None = None,
    ) -> requests.Response:
        query_params = structs.asdict(params) if params else None
        return self.http_client.request(
            "delete",
            path,
            headers=headers,
            params=query_params,
        )

    def _make_list_iter(self, f: Callable[P, PaginatedResponseBody[T]]):
        """Create a fully paginated iterator for the resource list() method."""

        def inner(
            *args: P.args, max_requests: int | None = None, **kwargs: P.kwargs
        ) -> Generator[T, Any, None]:
            return self._paginator(f(*args, **kwargs), max_requests=max_requests)

        return inner
