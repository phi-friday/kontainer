from __future__ import annotations

from functools import wraps
from inspect import signature
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    ValueT1 = TypeVar("ValueT1", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    OtherT = TypeVar("OtherT", infer_variance=True)

__all__ = ["flip_func"]


def flip_func(
    func: Callable[[ValueT1, ValueT2], OtherT]
) -> Callable[[ValueT2, ValueT1], OtherT]:
    sig = signature(func)

    @wraps(func)
    def inner(*args: Any) -> OtherT:
        return func(*sig.bind(*args[::-1]).args)

    return inner
