from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generator, Generic, NoReturn, overload

from typing_extensions import ParamSpec, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import KontainerValueError
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
        raise KontainerValueError("does not have a value.")

    @property
    def _oth(self) -> OtherT:
        if self._has_other():
            return self._other  # type: ignore
        raise KontainerValueError("does not have a other.")

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
        return str(self._value)

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

    @override
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Maybe[AnotherT, OtherT]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        result = func(self._val)
        return Maybe(result, self._other)

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Maybe[AnotherT, OtherT]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        result = func(self._val, value)
        return Maybe(result, self._other)

    @override
    def map_other(self, func: Callable[[OtherT], AnotherT]) -> Maybe[ValueT, AnotherT]:
        if not self._has_other():
            return Maybe(self._value, undefined)

        result = func(self._oth)
        return Maybe(self._value, result)

    @override
    def map_others(
        self, other: ElementT, func: Callable[[OtherT, ElementT], AnotherT]
    ) -> Maybe[ValueT, AnotherT]:
        if not self._has_other():
            return Maybe(self._value, undefined)

        result = func(self._oth, other)
        return Maybe(self._value, result)

    @override
    def bind_value(
        self, func: Callable[[ValueT], Maybe[AnotherT, AnotherT2]]
    ) -> Maybe[AnotherT, OtherT | AnotherT2]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        nested = Maybe(self._value, self._other).map_value(func)
        return nested.unwrap()

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Maybe[AnotherT, AnotherT2]],
    ) -> Maybe[AnotherT, OtherT | AnotherT2]:
        if not self._has_value():
            return Maybe(undefined, self._other)

        nested = Maybe(self._value, self._other).map_values(value, func)
        return nested.unwrap()

    @override
    def bind_other(
        self, func: Callable[[OtherT], Maybe[AnotherT, AnotherT2]]
    ) -> Maybe[ValueT | AnotherT, AnotherT2]:
        if not self._has_other():
            return Maybe(self._value, undefined)

        nested = Maybe(self._value, self._other).map_other(func)
        return nested.unwrap_other()

    @override
    def bind_others(
        self,
        other: ElementT,
        func: Callable[[OtherT, ElementT], Maybe[AnotherT, AnotherT2]],
    ) -> Maybe[ValueT | AnotherT, AnotherT2]:
        if not self._has_other():
            return Maybe(self._value, undefined)

        nested = Maybe(self._value, self._other).map_others(other, func)
        return nested.unwrap_other()

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

    @override
    def default_other(self, other: AnotherT) -> OtherT | AnotherT:
        if self._has_other():
            return self._oth
        return other

    @override
    def map_default_other(self, func: Callable[[], AnotherT]) -> OtherT | AnotherT:
        if self._has_other():
            return self._oth
        return func()

    @override
    def unwrap(self) -> ValueT:
        return self._val

    @override
    def unwrap_other(self) -> OtherT:
        return self._oth
