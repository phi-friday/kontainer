from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, overload

from kontainer.core.const import undefined
from kontainer.maybe import Result
from kontainer.utils.generator import unwrap_generator

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar

    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ParamT = ParamSpec("ParamT")

__all__ = ["catch"]


@overload
def catch(
    func: Callable[ParamT, Generator[Any, Any, ValueT2]]
) -> Callable[ParamT, Result[ValueT2, Exception]]: ...


@overload
def catch(
    func: Callable[ParamT, ValueT]
) -> Callable[ParamT, Result[ValueT, Exception]]: ...


def catch(
    func: Callable[ParamT, Generator[Any, Any, ValueT2]] | Callable[ParamT, ValueT]
) -> (
    Callable[ParamT, Result[ValueT2, Exception]]
    | Callable[ParamT, Result[ValueT, Exception]]
):
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Result[ValueT, Exception]:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, Generator):
                result = unwrap_generator(result)
        except Exception as exc:  # noqa: BLE001
            return Result(undefined, exc)
        return Result(result)

    return inner
