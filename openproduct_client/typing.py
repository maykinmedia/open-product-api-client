from abc import ABCMeta
from typing import Literal, Required, TypedDict, dataclass_transform

import msgspec


@dataclass_transform(kw_only_default=True)
class ResourceMeta(msgspec.StructMeta, ABCMeta):
    """
    Configure the behaviour of the resource classes.

    The metaclass avoids having to repeat a bunch of keyword arguments when defining
    msgspec structs. In particular, we establish:

    * JSON typically uses camelCase, while python uses snake_case, so we set up a
      default rename.
    * Forbid positional arguments - many components have 15+ properties with the same
      types being present - enforcing keyword arguments helps readability and makes
      things more explicit.
    """

    def __new__(mcls, name, bases, namespace, **struct_config):
        struct_config.setdefault("rename", "camel")
        struct_config["kw_only"] = True
        cls = super().__new__(mcls, name, bases, namespace, **struct_config)
        return cls


class PaginationParams(msgspec.Struct, metaclass=ResourceMeta):
    page: int
    page_size: int


class PaginatedResponseBody[T](TypedDict):
    count: Required[int]
    next: Required[str | None]
    previous: Required[str | None]
    results: Required[list[T]]


class InvalidParam(TypedDict):
    name: str
    code: str
    reason: str


class ErrorResponseBody(TypedDict):
    type: str
    code: str
    title: str
    status: int
    detail: str
    instance: str


class ValidationErrorResponseBody(ErrorResponseBody):
    status: Literal[400]
    invalidParams: list[InvalidParam]
