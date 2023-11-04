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
    r"""Container

    map: (x, y) -> (X, y) or  (x, y) -> (x, Y)\
    bind: (x, y) -> (X, Y)
    """

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
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value -> new value -> (new value, other)

        Args:
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Container[AnotherT, OtherT]:
        """_summary_

        value, arg -> new value -> (new value, other)

        Args:
            value: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def map_other(
        self, func: Callable[[OtherT], AnotherT]
    ) -> Container[ValueT, AnotherT]:
        """_summary_

        other -> new other -> (value, new other)

        Args:
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def map_others(
        self, other: ElementT, func: Callable[[OtherT, ElementT], AnotherT]
    ) -> Container[ValueT, AnotherT]:
        """_summary_

        other, arg -> new other -> (value, new other)

        Args:
            other: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_value(
        self, func: Callable[[ValueT], Container[AnotherT, AnotherT2]]
    ) -> Container[AnotherT, AnotherT2]:
        """_summary_

        value -> new value, new other -> (new value, new other)

        Args:
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Container[AnotherT, AnotherT2]],
    ) -> Container[AnotherT, AnotherT2]:
        """_summary_

        value, arg -> new value, new other -> (new value, new other)

        Args:
            value: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_other(
        self, func: Callable[[OtherT], Container[AnotherT, AnotherT2]]
    ) -> Container[AnotherT, AnotherT2]:
        """_summary_

        other -> new value, new other -> (new value, new other)

        Args:
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def bind_others(
        self,
        other: ElementT,
        func: Callable[[OtherT, ElementT], Container[AnotherT, AnotherT2]],
    ) -> Container[AnotherT, AnotherT2]:
        """_summary_

        other, arg -> new value, new other -> (new value, new other)

        Args:
            other: _description_
            func: _description_

        Returns:
            _description_
        """

    @abstractmethod
    def switch(self) -> Container[OtherT, ValueT]: ...

    @abstractmethod
    def default(self, value: AnotherT) -> ValueT | AnotherT: ...

    @abstractmethod
    def map_default(self, func: Callable[[], AnotherT]) -> ValueT | AnotherT: ...

    @abstractmethod
    def default_other(self, other: AnotherT) -> OtherT | AnotherT: ...

    @abstractmethod
    def map_default_other(self, func: Callable[[], AnotherT]) -> OtherT | AnotherT: ...

    @abstractmethod
    def unwrap(self) -> ValueT: ...

    @abstractmethod
    def unwrap_other(self) -> OtherT: ...
