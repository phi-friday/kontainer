from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, Generic, NoReturn, overload

from typing_extensions import ParamSpec, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import UndefinedError
from kontainer.core.types import Container
from kontainer.utils.generator import create_generator

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    OtherT2 = TypeVar("OtherT2", infer_variance=True)
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    AnotherT2 = TypeVar("AnotherT2", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)
    ParamT = ParamSpec("ParamT")

__all__ = ["Maybe"]


def _wrap_undefined_error(
    func: Callable[ParamT, Maybe[ValueT, OtherT]]
) -> Callable[ParamT, Maybe[ValueT, OtherT | Exception]]:
    @wraps(func)
    def inner(
        *args: ParamT.args, **kwargs: ParamT.kwargs
    ) -> Maybe[ValueT, OtherT | Exception]:
        try:
            return func(*args, **kwargs)
        except UndefinedError as exc:
            return Maybe(undefined, exc)

    return inner


class Maybe(Container[ValueT, OtherT], Generic[ValueT, OtherT]):
    @overload
    def __new__(cls, value: Undefined) -> NoReturn: ...

    @overload
    def __new__(cls, value: ValueT2 | Undefined) -> Maybe[ValueT2, Any]: ...

    @overload
    def __new__(cls, value: ValueT2) -> Maybe[ValueT2, Any]: ...

    @overload
    def __new__(cls, value: Undefined, other: Undefined) -> NoReturn: ...

    @overload
    def __new__(
        cls, value: Undefined, other: OtherT2 | Undefined
    ) -> NoReturn | Maybe[Any, OtherT2]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | Undefined, other: Undefined
    ) -> NoReturn | Maybe[ValueT2, Any]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | Undefined, other: OtherT2 | Undefined
    ) -> NoReturn | Maybe[ValueT2, OtherT2]: ...

    @overload
    def __new__(cls, value: Undefined, other: OtherT2) -> Maybe[Any, OtherT2]: ...

    @overload
    def __new__(cls, value: ValueT2, other: Undefined) -> Maybe[ValueT2, Any]: ...

    @overload
    def __new__(cls, value: ValueT2, other: OtherT2) -> Maybe[ValueT2, OtherT2]: ...

    @override
    def __new__(
        cls, value: ValueT2 | Undefined, other: OtherT2 | Undefined = undefined
    ) -> Maybe[ValueT2, OtherT2]:
        return super().__new__(cls, value, other)  # type: ignore

    def _has_value(self) -> bool:
        return self._value is not undefined

    def _has_other(self) -> bool:
        return self._other is not undefined

    @property
    def _val(self) -> ValueT:
        if self._has_value():
            return self._value  # type: ignore
        raise ValueError("does not have a value.")

    @property
    def _oth(self) -> OtherT:
        if self._has_other():
            return self._other  # type: ignore
        raise ValueError("does not have a other.")

    @override
    def __repr__(self) -> str:
        name = type(self).__name__
        if self._has_value():
            if self._has_other():
                return f"<{name!s}: value={self._value!r}, other={self._other!r}>"
            return f"<{name!s}: value={self._value!r}>"
        return f"<{name!s}: other={self._other!r}>"

    @override
    def __str__(self) -> str:
        return str(self._val)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Maybe):
            return False

        if self._has_value() is not other._has_value():
            return False

        return self._value == other._value

    @override
    def __hash__(self) -> int:
        return hash(self._val)

    @override
    def __iter__(self) -> Generator[Any, Any, ValueT]:
        if (
            not self._has_value()
            and self._has_other()
            and isinstance(self._oth, Exception)
        ):
            raise self._oth
        return create_generator(self._val)

    @_wrap_undefined_error
    @override
    def map_value(
        self, func: Callable[[ValueT], AnotherT]
    ) -> Maybe[AnotherT, OtherT | Exception]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        try:
            result = func(self._val)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return Maybe(result, self._other)

    @_wrap_undefined_error
    @override
    def map_values(
        self, func: Callable[[ValueT, ElementT], AnotherT], value: ElementT
    ) -> Maybe[AnotherT, OtherT | Exception]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        try:
            result = func(self._val, value)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return Maybe(result, self._other)

    @_wrap_undefined_error
    @override
    def map_other(
        self, func: Callable[[OtherT], AnotherT]
    ) -> Maybe[ValueT, AnotherT | Exception]:
        if not self._has_other():
            return Maybe(self._value)

        try:
            result = func(self._oth)
        except Exception as exc:  # noqa: BLE001
            return Maybe(self._value, exc)

        return Maybe(self._value, result)

    @_wrap_undefined_error
    @override
    def map_others(
        self, func: Callable[[OtherT, ElementT], AnotherT], other: ElementT
    ) -> Maybe[ValueT, AnotherT | Exception]:
        if not self._has_other():
            return Maybe(self._value)

        try:
            result = func(self._oth, other)
        except Exception as exc:  # noqa: BLE001
            return Maybe(self._value, exc)

        return Maybe(self._value, result)

    @_wrap_undefined_error
    @override
    def alt_value(
        self, func: Callable[[ValueT], AnotherT]
    ) -> Maybe[OtherT, AnotherT | Exception]:
        if not self._has_value():
            return Maybe(self._other)

        try:
            result = func(self._val)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return Maybe(self._other, result)

    @_wrap_undefined_error
    @override
    def alt_values(
        self, func: Callable[[ValueT, ElementT], AnotherT], value: ElementT
    ) -> Maybe[OtherT, AnotherT | Exception]:
        if not self._has_value():
            return Maybe(self._other)

        try:
            result = func(self._val, value)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return Maybe(self._other, result)

    @_wrap_undefined_error
    @override
    def alt_other(
        self, func: Callable[[OtherT], AnotherT]
    ) -> Maybe[AnotherT, ValueT | Exception]:
        if not self._has_other():
            return Maybe(undefined, self._value)

        try:
            result = func(self._oth)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return Maybe(result, self._value)

    @_wrap_undefined_error
    @override
    def alt_others(
        self, func: Callable[[OtherT, ElementT], AnotherT], other: ElementT
    ) -> Maybe[AnotherT, ValueT | Exception]:
        if not self._has_other():
            return Maybe(undefined, self._value)

        try:
            result = func(self._oth, other)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return Maybe(result, self._value)

    @_wrap_undefined_error
    @override
    def bind_value(
        self, func: Callable[[ValueT], Maybe[AnotherT, AnotherT2]]
    ) -> Maybe[AnotherT, OtherT | AnotherT2 | Exception]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        try:
            nested = self.map_value(func)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return nested._val  # noqa: SLF001

    @_wrap_undefined_error
    @override
    def bind_values(
        self,
        func: Callable[[ValueT, ElementT], Maybe[AnotherT, AnotherT2]],
        value: ElementT,
    ) -> Maybe[AnotherT, OtherT | AnotherT2 | Exception]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        try:
            nested = self.map_values(func, value)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        return nested._val  # noqa: SLF001

    @_wrap_undefined_error
    @override
    def bind_other(
        self, func: Callable[[OtherT], Maybe[AnotherT, AnotherT2]]
    ) -> Maybe[ValueT | AnotherT, AnotherT2 | Exception]:
        if not self._has_other():
            return Maybe(self._value, undefined)

        try:
            nested = self.map_other(func)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        result = nested._oth  # noqa: SLF001
        if isinstance(result, Exception):
            return Maybe(undefined, result)

        return result

    @_wrap_undefined_error
    @override
    def bind_others(
        self,
        func: Callable[[OtherT, ElementT], Maybe[AnotherT, AnotherT2]],
        other: ElementT,
    ) -> Maybe[ValueT | AnotherT, AnotherT2 | Exception]:
        if not self._has_other():
            return Maybe(self._value, undefined)

        try:
            nested = self.map_others(func, other)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        result = nested._oth  # noqa: SLF001
        if isinstance(result, Exception):
            return Maybe(undefined, result)

        return result

    @_wrap_undefined_error
    @override
    def lash_value(
        self, func: Callable[[ValueT], Maybe[AnotherT, AnotherT2]]
    ) -> Maybe[OtherT | AnotherT, AnotherT2 | Exception]:
        if not self._has_value():
            return Maybe(self._other, undefined)

        try:
            nested = self.alt_value(func)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        result = nested._oth  # noqa: SLF001
        if isinstance(result, Exception):
            return Maybe(undefined, result)

        return result

    @_wrap_undefined_error
    @override
    def lash_values(
        self,
        func: Callable[[ValueT, ElementT], Maybe[AnotherT, AnotherT2]],
        value: ElementT,
    ) -> Maybe[OtherT | AnotherT, AnotherT2 | Exception]:
        if not self._has_value():
            return Maybe(self._other, undefined)

        try:
            nested = self.alt_values(func, value)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        result = nested._oth  # noqa: SLF001
        if isinstance(result, Exception):
            return Maybe(undefined, result)

        return result

    @_wrap_undefined_error
    @override
    def lash_other(
        self, func: Callable[[OtherT], Maybe[AnotherT, AnotherT2]]
    ) -> Maybe[AnotherT, ValueT | AnotherT2 | Exception]:
        if not self._has_other():
            return Maybe(undefined, self._value)

        try:
            nested = self.alt_other(func)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        result = nested._val  # noqa: SLF001
        if isinstance(result, Exception):
            return Maybe(undefined, result)

        return result

    @_wrap_undefined_error
    @override
    def lash_others(
        self,
        func: Callable[[OtherT, ElementT], Maybe[AnotherT, AnotherT2]],
        value: ElementT,
    ) -> Maybe[AnotherT, ValueT | AnotherT2 | Exception]:
        if not self._has_other():
            return Maybe(undefined, self._value)

        try:
            nested = self.alt_others(func, value)
        except Exception as exc:  # noqa: BLE001
            return Maybe(undefined, exc)

        result = nested._val  # noqa: SLF001
        if isinstance(result, Exception):
            return Maybe(undefined, result)

        return result

    @override
    def switch(self) -> Maybe[OtherT, ValueT]:
        return Maybe(self._other, self._value)

    @override
    def default(self, value: AnotherT) -> ValueT | AnotherT:
        if self._has_value():
            return self._val
        return value

    @override
    def map_default(self, func: Callable[[], AnotherT]) -> ValueT | AnotherT:
        if self._has_value():
            return self._val
        return func()
