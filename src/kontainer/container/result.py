from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, NoReturn, overload

from typing_extensions import Self, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import KontainerTypeError
from kontainer.core.types import Container

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    ErrorT = TypeVar("ErrorT", infer_variance=True, bound=Exception)
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Result"]


class Result(Container[ValueT, OtherT], Generic[ValueT, OtherT]):
    @override
    def __init__(self, value: ValueT) -> None:
        self._value = value

    @overload
    def __new__(cls, value: ErrorT) -> Result[Any, ErrorT]: ...

    @overload
    def __new__(cls, value: type[ErrorT]) -> Result[Any, type[ErrorT]]: ...

    @overload
    def __new__(cls, value: ValueT) -> Result[ValueT, Any]: ...

    @overload
    def __new__(
        cls, value: ValueT | ErrorT | type[ErrorT]
    ) -> Result[ValueT, Any] | Result[Any, ErrorT] | Result[Any, type[ErrorT]]: ...

    @override
    def __new__(
        cls, value: ValueT | ErrorT | type[ErrorT]
    ) -> Result[ValueT, Any] | Result[Any, ErrorT] | Result[Any, type[ErrorT]]:
        if isinstance(value, Exception) or (
            isinstance(value, type) and issubclass(value, Exception)
        ):
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
            name = "Result"  # pragma: no cover
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
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def map_container(
        self, value: Result[ElementT, Any], func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherT]]
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def bind_container(
        self,
        value: Result[ElementT, Any],
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
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
            raise KontainerTypeError("Not an error container")

        if not isinstance(self._other, Exception):
            raise KontainerTypeError("error container does not hold an error")

        raise self._other


class Done(Result[ValueT, OtherT], Generic[ValueT, OtherT]):
    @override
    def __new__(cls, value: ValueT) -> Self:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Result[AnotherT, OtherT]:
        return Done(func(self._value))

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return Done(func(self._value, value))

    @override
    def map_container(
        self, value: Result[ElementT, Any], func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return value.bind_value(lambda x: self.map_values(x, func))

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherT]]
    ) -> Result[AnotherT, OtherT]:
        return func(self._value)

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return func(self._value, value)

    @override
    def bind_container(
        self,
        value: Result[ElementT, Any],
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return value.bind_value(lambda x: self.bind_values(x, func))

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
        self._value = value if value is undefined else undefined
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
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def map_container(
        self, value: Result[ElementT, Any], func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherT]]
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def bind_container(
        self,
        value: Result[ElementT, Any],
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        return Done(self._other)

    @override
    def default(self, value: AnotherT) -> AnotherT:
        return value

    @override
    def map_default(self, func: Callable[[], AnotherT]) -> AnotherT:
        return func()

    @override
    def unwrap(self) -> NoReturn:
        self.unwrap_error()
