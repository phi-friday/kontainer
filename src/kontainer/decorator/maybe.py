from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, overload

from kontainer.core.const import undefined
from kontainer.maybe import Maybe
from kontainer.utils.generator import unwrap_generator

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)
    OtherT = TypeVar("OtherT", infer_variance=True)
    ParamT = ParamSpec("ParamT")

__all__ = ["wrap"]


@overload
def wrap(
    func: Callable[ParamT, Generator[Any, Any, Maybe[ValueT, OtherT]]]
) -> Callable[ParamT, Maybe[ValueT, OtherT | Exception]]: ...


@overload
def wrap(
    func: Callable[ParamT, Generator[Any, Any, ValueT]]
) -> Callable[ParamT, Maybe[ValueT, Exception]]: ...


@overload
def wrap(
    func: Callable[ParamT, Maybe[ValueT, OtherT]]
) -> Callable[ParamT, Maybe[ValueT, OtherT | Exception]]: ...


@overload
def wrap(
    func: Callable[ParamT, ValueT]
) -> Callable[ParamT, Maybe[ValueT, Exception]]: ...


def wrap(
    func: Callable[ParamT, Generator[Any, Any, Maybe[ValueT, OtherT]]]
    | Callable[ParamT, Generator[Any, Any, ValueT]]
    | Callable[ParamT, Maybe[ValueT, OtherT]]
    | Callable[ParamT, ValueT],
) -> (
    Callable[ParamT, Maybe[ValueT, OtherT | Exception]]
    | Callable[ParamT, Maybe[ValueT, Exception]]
):
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Maybe[ValueT, Any]:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, Generator):
                result = unwrap_generator(result)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)
        if isinstance(result, Maybe):
            return Maybe(result._value, result._other)  # noqa: SLF001
        return Maybe(result)

    return inner
