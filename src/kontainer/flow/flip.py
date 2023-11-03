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
    length = len(sig.parameters)
    if length < 2:  # noqa: PLR2004
        error_msg = f"Too few parameters required by func: {length} < 2"
        raise TypeError(error_msg)
    if len(sig.parameters) > 2:  # noqa: PLR2004
        error_msg = f"Too many parameters required by func: {length} > 2"
        raise TypeError(error_msg)

    @wraps(func)
    def inner(*args: Any) -> OtherT:
        return func(*sig.bind(*args[::-1]).args)

    return inner
