from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, overload

from kontainer.core.const import undefined
from kontainer.maybe import Maybe
from kontainer.utils.generator import unwrap_generator

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ParamT = ParamSpec("ParamT")

__all__ = ["wrap"]


@overload
def wrap(
    func: Callable[ParamT, Generator[Any, Any, ValueT2]]
) -> Callable[ParamT, Maybe[ValueT2, Exception]]: ...


@overload
def wrap(
    func: Callable[ParamT, ValueT]
) -> Callable[ParamT, Maybe[ValueT, Exception]]: ...


def wrap(
    func: Callable[ParamT, Generator[Any, Any, ValueT2]] | Callable[ParamT, ValueT]
) -> (
    Callable[ParamT, Maybe[ValueT2, Exception]]
    | Callable[ParamT, Maybe[ValueT, Exception]]
):
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Maybe[ValueT, Exception]:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, Generator):
                result = unwrap_generator(result)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)
        return Maybe(result)

    return inner
