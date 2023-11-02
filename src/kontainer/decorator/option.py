from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, overload

from kontainer.maybe import Option
from kontainer.utils.generator import unwrap_generator

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ParamT = ParamSpec("ParamT")

__all__ = ["optional"]


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, None]]
) -> Callable[ParamT, Option[Any]]: ...


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, ValueT2 | None]]
) -> Callable[ParamT, Option[ValueT2]]: ...


@overload
def optional(
    func: Callable[ParamT, Generator[Any, Any, ValueT2]]
) -> Callable[ParamT, Option[ValueT2]]: ...


@overload
def optional(func: Callable[ParamT, None]) -> Callable[ParamT, Option[Any]]: ...


@overload
def optional(
    func: Callable[ParamT, ValueT | None]
) -> Callable[ParamT, Option[ValueT]]: ...


@overload
def optional(func: Callable[ParamT, ValueT]) -> Callable[ParamT, Option[ValueT]]: ...


def optional(
    func: Callable[ParamT, Generator[Any, Any, None]]
    | Callable[ParamT, Generator[Any, Any, ValueT2 | None]]
    | Callable[ParamT, Generator[Any, Any, ValueT2]]
    | Callable[ParamT, None]
    | Callable[ParamT, ValueT | None]
    | Callable[ParamT, ValueT],
) -> (
    Callable[ParamT, Option[Any]]
    | Callable[ParamT, Option[ValueT2]]
    | Callable[ParamT, Option[ValueT]]
):
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Option[Any]:
        result = func(*args, **kwargs)
        if isinstance(result, Generator):
            result = unwrap_generator(result)
        return Option(result)

    return inner
