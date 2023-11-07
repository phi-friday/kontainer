from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, NoReturn, overload

from typing_extensions import Self, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import KontainerTypeError, KontainerValueError
from kontainer.core.types import Container

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    ErrorT = TypeVar("ErrorT", infer_variance=True, bound=Exception)
    AnotherT1 = TypeVar("AnotherT1", infer_variance=True)
    AnotherT2 = TypeVar("AnotherT2", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Result"]


class Result(Container[ValueT, OtherT], Generic[ValueT, OtherT]):
    @override
    def __init__(self, value: ValueT) -> None:
        self._value = value

    @overload
    def __new__(cls, value: ErrorT) -> Result[Any, ErrorT]: ...

    @overload
    def __new__(cls, value: ValueT) -> Result[ValueT, Any]: ...

    @overload
    def __new__(
        cls, value: ValueT | ErrorT
    ) -> Result[ValueT, Any] | Result[Any, ErrorT]: ...

    @override
    def __new__(
        cls, value: ValueT | ErrorT
    ) -> Result[ValueT, Any] | Result[Any, ErrorT]:
        if isinstance(value, Exception):
            return Error(value)
        return Done(value)

    @override
    def __repr__(self) -> str:
        container_type = type(self)
        if issubclass(container_type, Done):
            name = "Done"
        elif issubclass(container_type, Error):
            name = "Error"
        else:
            name = "Maybe"
        return f"<{name}: value={self._value!r}>"

    @override
    def __str__(self) -> str:
        return str(self._value)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Result) and other._value == self._value

    @override
    def __hash__(self) -> int:
        return hash((Result, self._value))

    @override
    def map_value(
        self, func: Callable[[ValueT], AnotherT1]
    ) -> Result[AnotherT1, OtherT]:
        raise NotImplementedError

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT1]
    ) -> Result[AnotherT1, OtherT]:
        raise NotImplementedError

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT1, OtherT]]
    ) -> Result[AnotherT1, OtherT]:
        raise NotImplementedError

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT1, OtherT]],
    ) -> Result[AnotherT1, OtherT]:
        raise NotImplementedError

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        raise NotImplementedError

    @override
    def default(self, value: Any) -> ValueT:
        raise NotImplementedError

    @override
    def map_default(self, func: Callable[[], Any]) -> ValueT:
        raise NotImplementedError

    @override
    def unwrap(self) -> ValueT:
        raise NotImplementedError

    def unwrap_error(self) -> NoReturn:
        if not isinstance(self, Error):
            raise KontainerValueError("Not an error container")

        if not isinstance(self._other, Exception):
            raise KontainerTypeError("error container does not hold an error")

        raise self._other


class Done(Result[ValueT, OtherT], Generic[ValueT, OtherT]):
    @override
    def __new__(cls, value: ValueT) -> Self:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(
        self, func: Callable[[ValueT], AnotherT1]
    ) -> Result[AnotherT1, OtherT]:
        return Done(func(self._value))

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT1]
    ) -> Result[AnotherT1, OtherT]:
        return Done(func(self._value, value))

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT1, AnotherT2]]
    ) -> Result[AnotherT1, AnotherT2]:
        return func(self._value)

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT1, AnotherT2]],
    ) -> Result[AnotherT1, AnotherT2]:
        return func(self._value, value)

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        return Error(self._value)

    @override
    def default(self, value: Any) -> ValueT:
        return self._value

    @override
    def map_default(self, func: Callable[[], Any]) -> ValueT:
        return self._value

    @override
    def unwrap(self) -> ValueT:
        return self._value


class Error(Result[ValueT, OtherT], Generic[ValueT, OtherT]):
    __slots__ = ("_value", "_other")

    @override
    def __init__(self, value: OtherT) -> None:
        self._value = undefined if value is undefined else value
        self._other = value

    @overload
    def __new__(cls, value: Undefined) -> Result[Any, Any]: ...

    @overload
    def __new__(cls, value: OtherT) -> Result[ValueT, OtherT]: ...

    @overload
    def __new__(
        cls, value: OtherT | Undefined
    ) -> Result[ValueT, OtherT] | Result[Any, Any]: ...

    @override
    def __new__(
        cls, value: OtherT | Undefined
    ) -> Result[ValueT, OtherT] | Result[Any, Any]:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(
        self, func: Callable[[ValueT], AnotherT1]
    ) -> Result[AnotherT1, OtherT]:
        return Error(self._other)

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT1]
    ) -> Result[AnotherT1, OtherT]:
        return Error(self._other)

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT1, AnotherT2]]
    ) -> Result[AnotherT1, AnotherT2]:
        return Error(self._other)  # type: ignore

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT1, AnotherT2]],
    ) -> Result[AnotherT1, AnotherT2]:
        return Error(self._other)  # type: ignore

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        return Done(self._other)

    @override
    def default(self, value: AnotherT1) -> AnotherT1:
        return value

    @override
    def map_default(self, func: Callable[[], AnotherT1]) -> AnotherT1:
        return func()

    @override
    def unwrap(self) -> NoReturn:
        raise KontainerValueError("does not have a value.")
