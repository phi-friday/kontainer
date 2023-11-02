from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Generator, Generic, NoReturn, overload

from typing_extensions import TypeVar

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import UndefinedError

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    OtherT2 = TypeVar("OtherT2", infer_variance=True)
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    AnotherT2 = TypeVar("AnotherT2", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Container"]


class Container(ABC, Generic[ValueT, OtherT]):
    __slots__ = ("_value", "_other")

    def __init__(
        self, value: ValueT | Undefined, other: OtherT | Undefined = undefined
    ) -> None:
        if value is undefined and other is undefined:
            error_msg = "Both value and other are undefined."
            raise UndefinedError(error_msg)

        self._value = value
        self._other = other

    @overload
    def __new__(cls, value: Undefined) -> NoReturn: ...

    @overload
    def __new__(cls, value: ValueT2 | Undefined) -> Container[ValueT2, Any]: ...

    @overload
    def __new__(cls, value: ValueT2) -> Container[ValueT2, Any]: ...

    @overload
    def __new__(cls, value: Undefined, other: Undefined) -> NoReturn: ...

    @overload
    def __new__(
        cls, value: Undefined, other: OtherT2 | Undefined
    ) -> NoReturn | Container[Any, OtherT2]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | Undefined, other: Undefined
    ) -> NoReturn | Container[ValueT2, Any]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | Undefined, other: OtherT2 | Undefined
    ) -> NoReturn | Container[ValueT2, OtherT2]: ...

    @overload
    def __new__(cls, value: Undefined, other: OtherT2) -> Container[Any, OtherT2]: ...

    @overload
    def __new__(cls, value: ValueT2, other: Undefined) -> Container[ValueT2, Any]: ...

    @overload
    def __new__(cls, value: ValueT2, other: OtherT2) -> Container[ValueT2, OtherT2]: ...

    def __new__(
        cls,
        value: ValueT2 | Undefined,  # noqa: ARG003
        other: OtherT2 | Undefined = undefined,  # noqa: ARG003
    ) -> Container[ValueT2, OtherT2]:
        return super().__new__(cls)  # type: ignore

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def __iter__(self) -> Generator[Any, Any, ValueT]: ...

    def __await__(self) -> Generator[Any, Any, ValueT]:
        return iter(self)

    @abstractmethod
    def map_value(
        self, func: Callable[[ValueT], AnotherT]
    ) -> Container[AnotherT, OtherT | Exception]: ...

    @abstractmethod
    def map_values(
        self, func: Callable[[ValueT, ElementT], AnotherT], value: ElementT
    ) -> Container[AnotherT, OtherT | Exception]: ...

    @abstractmethod
    def map_other(
        self, func: Callable[[OtherT], AnotherT]
    ) -> Container[ValueT, AnotherT | Exception]: ...

    @abstractmethod
    def map_others(
        self, func: Callable[[OtherT, ElementT], AnotherT], other: ElementT
    ) -> Container[ValueT, AnotherT | Exception]: ...

    @abstractmethod
    def alt_value(
        self, func: Callable[[ValueT], AnotherT]
    ) -> Container[OtherT, AnotherT | Exception]: ...

    @abstractmethod
    def alt_values(
        self, func: Callable[[ValueT, ElementT], AnotherT], value: ElementT
    ) -> Container[OtherT, AnotherT | Exception]: ...

    @abstractmethod
    def alt_other(
        self, func: Callable[[OtherT], AnotherT]
    ) -> Container[AnotherT, ValueT | Exception]: ...

    @abstractmethod
    def alt_others(
        self, func: Callable[[OtherT, ElementT], AnotherT], other: ElementT
    ) -> Container[AnotherT, ValueT | Exception]: ...

    @abstractmethod
    def bind_value(
        self, func: Callable[[ValueT], Container[AnotherT, AnotherT2]]
    ) -> Container[AnotherT, OtherT | AnotherT2 | Exception]: ...

    @abstractmethod
    def bind_values(
        self,
        func: Callable[[ValueT, ElementT], Container[AnotherT, AnotherT2]],
        value: ElementT,
    ) -> Container[AnotherT, OtherT | AnotherT2 | Exception]: ...

    @abstractmethod
    def bind_other(
        self, func: Callable[[OtherT], Container[AnotherT, AnotherT2]]
    ) -> Container[ValueT | AnotherT, AnotherT2 | Exception]: ...

    @abstractmethod
    def bind_others(
        self,
        func: Callable[[OtherT, ElementT], Container[AnotherT, AnotherT2]],
        other: ElementT,
    ) -> Container[ValueT | AnotherT, AnotherT2 | Exception]: ...

    @abstractmethod
    def lash_value(
        self, func: Callable[[ValueT], Container[AnotherT, AnotherT2]]
    ) -> Container[OtherT | AnotherT, AnotherT2 | Exception]: ...

    @abstractmethod
    def lash_values(
        self,
        func: Callable[[ValueT, ElementT], Container[AnotherT, AnotherT2]],
        value: ElementT,
    ) -> Container[OtherT | AnotherT, AnotherT2 | Exception]: ...

    @abstractmethod
    def lash_other(
        self, func: Callable[[OtherT], Container[AnotherT, AnotherT2]]
    ) -> Container[AnotherT, ValueT | AnotherT2 | Exception]: ...

    @abstractmethod
    def lash_others(
        self,
        func: Callable[[OtherT, ElementT], Container[AnotherT, AnotherT2]],
        value: ElementT,
    ) -> Container[AnotherT, ValueT | AnotherT2 | Exception]: ...

    @abstractmethod
    def switch(self) -> Container[OtherT, ValueT]: ...

    @abstractmethod
    def default(self, value: AnotherT) -> ValueT | AnotherT: ...

    @abstractmethod
    def map_default(self, func: Callable[[], AnotherT]) -> ValueT | AnotherT: ...
