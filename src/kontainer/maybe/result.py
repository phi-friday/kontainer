from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generic, NoReturn, overload

from typing_extensions import ParamSpec, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.maybe.maybe import Maybe

if TYPE_CHECKING:
    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ErrorT = TypeVar("ErrorT", infer_variance=True, bound=Exception)
    ErrorT2 = TypeVar("ErrorT2", infer_variance=True, bound=Exception)
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    OtherErrorT = TypeVar("OtherErrorT", infer_variance=True, bound=Exception)
    ElementT = TypeVar("ElementT", infer_variance=True)
    ParamT = ParamSpec("ParamT")


__all__ = ["Result"]


def _wrap_type_error(
    func: Callable[ParamT, Result[ValueT, ErrorT]]
) -> Callable[ParamT, Result[ValueT, ErrorT | TypeError]]:
    @wraps(func)
    def inner(
        *args: ParamT.args, **kwargs: ParamT.kwargs
    ) -> Result[ValueT, ErrorT | TypeError]:
        try:
            return func(*args, **kwargs)
        except TypeError as exc:
            return Result(undefined, exc)

    return inner


def _maybe_to_result(
    func: Callable[ParamT, Maybe[ValueT, ErrorT]]
) -> Callable[ParamT, Result[ValueT, ErrorT]]:
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Result[ValueT, ErrorT]:
        result = func(*args, **kwargs)
        return Result(result._value, result._other)  # noqa: SLF001

    return inner


def _non_error_maybe_to_result(
    func: Callable[ParamT, Maybe[ValueT, Any]]
) -> Callable[ParamT, Result[ValueT, Exception]]:
    @wraps(func)
    def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Result[ValueT, Exception]:
        result = func(*args, **kwargs)
        if result._other is undefined:  # noqa: SLF001
            return Result(result._value)  # noqa: SLF001
        if isinstance(result._other, Exception):  # noqa: SLF001
            return Result(result._value, result._other)  # noqa: SLF001
        raise TypeError("The type of value changed to other is not an error type.")

    return inner


class Result(Maybe[ValueT, ErrorT], Generic[ValueT, ErrorT]):
    @overload
    def __new__(cls, value: Undefined) -> NoReturn: ...

    @overload
    def __new__(cls, value: ValueT2 | Undefined) -> Result[ValueT2, Exception]: ...

    @overload
    def __new__(cls, value: ValueT2) -> Result[ValueT2, Exception]: ...

    @overload
    def __new__(cls, value: Undefined, other: Undefined) -> NoReturn: ...

    @overload
    def __new__(
        cls, value: Undefined, other: ErrorT2 | Undefined
    ) -> NoReturn | Result[Any, ErrorT2]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | Undefined, other: Undefined
    ) -> NoReturn | Result[ValueT2, Exception]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | Undefined, other: ErrorT2 | Undefined
    ) -> NoReturn | Result[ValueT2, ErrorT2]: ...

    @overload
    def __new__(cls, value: Undefined, other: ErrorT2) -> Result[Any, ErrorT2]: ...

    @overload
    def __new__(
        cls, value: ValueT2, other: Undefined
    ) -> Result[ValueT2, Exception]: ...

    @overload
    def __new__(cls, value: ValueT2, other: ErrorT2) -> Result[ValueT2, ErrorT2]: ...

    @override
    def __new__(
        cls, value: ValueT2 | Undefined, other: ErrorT2 | Undefined = undefined
    ) -> Result[ValueT2, ErrorT2]:
        return super().__new__(cls, value, other)  # type: ignore

    @_maybe_to_result
    @override
    def map_value(
        self, func: Callable[[ValueT], AnotherT]
    ) -> Maybe[AnotherT, ErrorT | Exception]:
        return super().map_value(func)

    @_maybe_to_result
    @override
    def map_values(
        self, func: Callable[[ValueT, ElementT], AnotherT], value: ElementT
    ) -> Maybe[AnotherT, ErrorT | Exception]:
        return super().map_values(func, value)

    @_maybe_to_result
    @override
    def map_other(
        self, func: Callable[[ErrorT], OtherErrorT]
    ) -> Maybe[ValueT, OtherErrorT | Exception]:
        return super().map_other(func)

    @_maybe_to_result
    @override
    def map_others(
        self, func: Callable[[ErrorT, ElementT], OtherErrorT], other: ElementT
    ) -> Maybe[ValueT, OtherErrorT | Exception]:
        return super().map_others(func, other)

    @_maybe_to_result
    @override
    def alt_value(
        self, func: Callable[[ValueT], OtherErrorT]
    ) -> Maybe[ErrorT, OtherErrorT | Exception]:
        return super().alt_value(func)

    @_maybe_to_result
    @override
    def alt_values(
        self, func: Callable[[ValueT, ElementT], OtherErrorT], value: ElementT
    ) -> Maybe[ErrorT, OtherErrorT | Exception]:
        return super().alt_values(func, value)

    @_wrap_type_error
    @_non_error_maybe_to_result
    @override
    def alt_other(
        self, func: Callable[[ErrorT], AnotherT]
    ) -> Maybe[AnotherT, ValueT | Exception]:
        return super().alt_other(func)

    @_wrap_type_error
    @_non_error_maybe_to_result
    @override
    def alt_others(
        self, func: Callable[[ErrorT, ElementT], AnotherT], other: ElementT
    ) -> Maybe[AnotherT, ValueT | Exception]:
        return super().alt_others(func, other)

    @_maybe_to_result
    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherErrorT]]
    ) -> Maybe[AnotherT, ErrorT | OtherErrorT | Exception]:
        return super().bind_value(func)

    @_maybe_to_result
    @override
    def bind_values(
        self,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherErrorT]],
        value: ElementT,
    ) -> Maybe[AnotherT, ErrorT | OtherErrorT | Exception]:
        return super().bind_values(func, value)

    @_maybe_to_result
    @override
    def bind_other(
        self, func: Callable[[ErrorT], Result[AnotherT, OtherErrorT]]
    ) -> Maybe[ValueT | AnotherT, OtherErrorT | Exception]:
        return super().bind_other(func)

    @_maybe_to_result
    @override
    def bind_others(
        self,
        func: Callable[[ErrorT, ElementT], Result[AnotherT, OtherErrorT]],
        other: ElementT,
    ) -> Maybe[ValueT | AnotherT, OtherErrorT | Exception]:
        return super().bind_others(func, other)

    @_maybe_to_result
    @override
    def lash_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherErrorT]]
    ) -> Maybe[ErrorT | AnotherT, OtherErrorT | Exception]:
        return super().lash_value(func)

    @_maybe_to_result
    @override
    def lash_values(
        self,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherErrorT]],
        value: ElementT,
    ) -> Maybe[ErrorT | AnotherT, OtherErrorT | Exception]:
        return super().lash_values(func, value)

    @_wrap_type_error
    @_non_error_maybe_to_result
    @override
    def lash_other(
        self, func: Callable[[ErrorT], Result[AnotherT, OtherErrorT]]
    ) -> Maybe[AnotherT, ValueT | OtherErrorT | Exception]:
        return super().lash_other(func)

    @_wrap_type_error
    @_non_error_maybe_to_result
    @override
    def lash_others(
        self,
        func: Callable[[ErrorT, ElementT], Result[AnotherT, OtherErrorT]],
        value: ElementT,
    ) -> Maybe[AnotherT, ValueT | OtherErrorT | Exception]:
        return super().lash_others(func, value)

    @_wrap_type_error
    @_non_error_maybe_to_result
    @override
    def switch(self) -> Maybe[ErrorT, ValueT]:
        return super().switch()
