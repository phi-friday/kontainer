from __future__ import annotations

from inspect import signature
from typing import TYPE_CHECKING, Any, Callable, Generator, Generic, NoReturn, overload

from typing_extensions import TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.maybe.maybe import Maybe
from kontainer.utils.generator import create_generator

ValueT = TypeVar("ValueT", infer_variance=True)
if TYPE_CHECKING:
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Option"]


class Option(Maybe[ValueT, None], Generic[ValueT]):
    @override
    def __init__(
        self, value: ValueT | None | Undefined, other: Any = undefined
    ) -> None:
        self._value = None if value is undefined else value
        self._other = undefined

    @overload
    def __new__(cls, value: Undefined) -> Option[Any]: ...

    @overload
    def __new__(cls, value: None) -> Option[Any]: ...

    @overload
    def __new__(cls, value: None | Undefined) -> Option[Any]: ...

    @overload
    def __new__(cls, value: ValueT2 | None) -> Option[ValueT2]: ...

    @overload
    def __new__(cls, value: ValueT2 | Undefined) -> Option[ValueT2]: ...

    @overload
    def __new__(cls, value: ValueT2 | None | Undefined) -> Option[ValueT2]: ...

    @overload
    def __new__(cls, value: ValueT2) -> Option[ValueT2]: ...

    @overload
    def __new__(
        cls, value: ValueT2 | None | Undefined, other: Any = undefined
    ) -> Option[ValueT2]: ...

    @override
    def __new__(
        cls, value: ValueT2 | None | Undefined, other: Any = undefined
    ) -> Option[ValueT2]:
        return super().__new__(cls, value)  # type: ignore

    def _has_value(self) -> bool:
        return self._value is not undefined and self._value is not None

    def _has_other(self) -> bool:
        return False

    @property
    def _val(self) -> ValueT | None:
        if self._has_value():
            return self._value  # type: ignore
        return None

    @override
    def __iter__(self) -> Generator[Any, Any, ValueT | None]:
        return create_generator(self._val)

    @override
    def __await__(self) -> Generator[Any, Any, ValueT | None]:
        return super().__await__()

    @override
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Option[AnotherT]:
        if not self._has_value() or self._val is None:
            return Option(undefined)

        result = func(self._val)
        return Option(result)

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Option[AnotherT]:
        if not self._has_value() or self._val is None:
            return Option(undefined)

        result = func(self._val, value)
        return Option(result)

    @override
    def map_other(
        self, func: Callable[[None], AnotherT] | Callable[[], AnotherT]
    ) -> Option[ValueT | AnotherT]:
        if self._has_value():
            return Option(self._val)

        try:
            signature(func).bind(None)
        except TypeError:
            args = ()
        else:
            args = (None,)

        result = func(*args)
        return Option(result)

    @override
    def map_others(
        self,
        other: ElementT,
        func: Callable[[None, ElementT], AnotherT] | Callable[[ElementT], AnotherT],
    ) -> Option[ValueT | AnotherT]:
        if self._has_value():
            return Option(self._val)

        try:
            signature(func).bind(None, other)
        except TypeError:
            args = (other,)
        else:
            args = (None, other)

        result = func(*args)  # type: ignore
        return Option(result)

    @override
    def alt_value(
        self, func: Callable[[None], AnotherT] | Callable[[], AnotherT]
    ) -> Option[ValueT | AnotherT]:
        return self.map_other(func)

    @override
    def alt_values(
        self,
        value: ElementT,
        func: Callable[[None, ElementT], AnotherT] | Callable[[ElementT], AnotherT],
    ) -> Option[ValueT | AnotherT]:
        return self.map_others(value, func)

    @override
    def alt_other(self, func: Callable[[ValueT], AnotherT]) -> Option[AnotherT]:
        return self.map_value(func)

    @override
    def alt_others(
        self, other: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Option[AnotherT]:
        return self.map_values(other, func)

    @override
    def bind_value(
        self, func: Callable[[ValueT], Option[AnotherT]]
    ) -> Option[AnotherT]:
        if not self._has_value():
            return Option(undefined)

        nested = self.map_value(func)
        result = nested._val  # noqa: SLF001
        if result is None:
            return Option(None)
        return result

    @override
    def bind_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], Option[AnotherT]]
    ) -> Option[AnotherT]:
        if not self._has_value():
            return Option(undefined)

        nested = self.map_values(value, func)
        result = nested._val  # noqa: SLF001
        if result is None:
            return Option(None)
        return result

    @override
    def bind_other(
        self, func: Callable[[None], Option[AnotherT]] | Callable[[], Option[AnotherT]]
    ) -> Option[ValueT | AnotherT]:
        if self._has_value():
            return Option(self._val)

        nested = self.map_other(func)
        result = nested._val  # noqa: SLF001
        if result is None:
            return Option(None)
        if not isinstance(result, Option):
            raise NotImplementedError
        return result

    @override
    def bind_others(
        self,
        other: ElementT,
        func: Callable[[None, ElementT], Option[AnotherT]]
        | Callable[[ElementT], Option[AnotherT]],
    ) -> Option[ValueT | AnotherT]:
        if self._has_value():
            return Option(self._val)

        nested = self.map_others(other, func)
        result = nested._val  # noqa: SLF001
        if result is None:
            return Option(None)
        if not isinstance(result, Option):
            raise NotImplementedError
        return result

    @override
    def lash_value(
        self, func: Callable[[None], Option[AnotherT]] | Callable[[], Option[AnotherT]]
    ) -> Option[ValueT | AnotherT]:
        return self.bind_other(func)

    @override
    def lash_values(
        self,
        value: ElementT,
        func: Callable[[None, ElementT], Option[AnotherT]]
        | Callable[[ElementT], Option[AnotherT]],
    ) -> Option[ValueT | AnotherT]:
        return self.bind_others(value, func)

    @override
    def lash_other(
        self, func: Callable[[ValueT], Option[AnotherT]]
    ) -> Option[AnotherT]:
        return self.bind_value(func)

    @override
    def lash_others(
        self, value: ElementT, func: Callable[[ValueT, ElementT], Option[AnotherT]]
    ) -> Option[AnotherT]:
        return self.bind_values(value, func)

    @override
    def switch(self) -> NoReturn:
        raise NotImplementedError

    @override
    def default_other(self, other: Any) -> NoReturn:
        raise NotImplementedError

    @override
    def map_default_other(self, func: Callable[[], Any]) -> NoReturn:
        raise NotImplementedError

    @override
    def unwrap(self) -> ValueT | None:
        return self._val

    @override
    def unwrap_other(self) -> NoReturn:
        raise NotImplementedError
