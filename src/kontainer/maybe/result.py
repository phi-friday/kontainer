from __future__ import annotations

from functools import wraps
from inspect import isclass
from typing import TYPE_CHECKING, Any, Callable, Generic, NoReturn, overload

from typing_extensions import ParamSpec, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import KontainerTypeError
from kontainer.maybe.maybe import Maybe

ValueT = TypeVar("ValueT", infer_variance=True)
ErrorT = TypeVar("ErrorT", infer_variance=True, bound=Exception)
if TYPE_CHECKING:
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
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
        raise KontainerTypeError(
            "The type of value changed to other is not an error type."
        )

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
        if (
            other is not undefined
            and not isinstance(other, Exception)
            and not (isclass(other) and issubclass(other, Exception))
        ):
            error_msg = (
                f"{type(other).__name__!s}[{other!r}] is not undefind and error object"
            )
            raise TypeError(error_msg)
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
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Maybe[AnotherT, ErrorT | Exception]:
        return super().map_values(value, func)

    @_maybe_to_result
    @override
    def map_other(
        self, func: Callable[[ErrorT], OtherErrorT]
    ) -> Maybe[ValueT, OtherErrorT | Exception]:
        return super().map_other(func)

    @_maybe_to_result
    @override
    def map_others(
        self, other: ElementT, func: Callable[[ErrorT, ElementT], OtherErrorT]
    ) -> Maybe[ValueT, OtherErrorT | Exception]:
        return super().map_others(other, func)

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
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherErrorT]],
    ) -> Maybe[AnotherT, ErrorT | OtherErrorT | Exception]:
        return super().bind_values(value, func)

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
        other: ElementT,
        func: Callable[[ErrorT, ElementT], Result[AnotherT, OtherErrorT]],
    ) -> Maybe[ValueT | AnotherT, OtherErrorT | Exception]:
        return super().bind_others(other, func)

    @_wrap_type_error
    @_non_error_maybe_to_result
    @override
    def switch(self) -> Maybe[ErrorT, ValueT]:
        return super().switch()

    @override
    def default_other(self, other: Any) -> NoReturn:
        raise NotImplementedError

    @override
    def map_default_other(self, func: Callable[[], Any]) -> NoReturn:
        raise NotImplementedError

    @override
    def unwrap_other(self) -> NoReturn | None:
        if self._has_other():
            raise self._oth
