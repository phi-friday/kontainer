from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar

import pytest
import sniffio
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from kontainer.core.types import Container

BOLD_RED = "\x1b[31;1m"
RED = "\x1b[31;20m"
RESET = "\x1b[0m"


class _Const: ...


const = _Const()


def _func_as_container(
    func: Callable[..., Any], container_type: type[Container]
) -> Callable[..., Container]:
    def inner(*args: Any) -> Container[Any, Any]:
        result = func(*args)
        if isinstance(result, container_type):
            return result
        return container_type(result)

    return inner


def _generate_getter(value: Any) -> Callable[[], Any]:
    def inner() -> Any:
        return value

    return inner


def _add_one(x: int) -> int:
    return x + 1


def _add_suffix(x: str) -> str:
    return x + "suffix"


def _add_bsuffix(x: bytes) -> bytes:
    return x + b"suffix"


def _concat_tuples(x: tuple[Any, ...]) -> tuple[Any, ...]:
    return (*x, 123)


def _get_func(value: Any) -> Callable[[Any], Any]:
    if isinstance(value, int):
        return _add_one
    if isinstance(value, str):
        return _add_suffix
    if isinstance(value, bytes):
        return _add_bsuffix
    if isinstance(value, tuple):
        return _concat_tuples

    raise NotImplementedError


def _concat_values(x: Any, y: Any) -> tuple[Any, Any]:
    return (x, y)


@st.composite
def value_func_result(draw: st.DrawFn):
    value = draw(
        st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers()))
    )
    func = _get_func(value)
    result = func(value)
    return (value, func, result)


@st.composite
def values_func_result(draw: st.DrawFn):
    value = draw(
        st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers()))
    )
    other = draw(
        st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers()))
    )
    result = _concat_values(value, other)
    return (value, other, _concat_values, result)


arbitrary = st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers()))


class BaseTestContainer(ABC):
    container_type: ClassVar[type[Container]]

    def test_container_type(self):
        assert issubclass(self.container_type, Container)

    @given(arbitrary)
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_construct(self, value: Any):
        container = self.container_type(value)
        assert isinstance(container, self.container_type)
        assert container._value == value

    @given(arbitrary)
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_eq(self, value: Any):
        left, right = self.container_type(value), self.container_type(value)
        assert left == right

    @given(st.lists(arbitrary, min_size=2, max_size=2, unique=True))
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_ne(self, values: list[Any]):
        value, other = values
        assert value != other

        left, right = self.container_type(value), self.container_type(other)
        assert left != right

    @given(arbitrary)
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_hash(self, value: Any):
        container = self.container_type(value)
        assert hash(container) == hash((self.container_type, value))

    @given(arbitrary)
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_iter(self, value: Any):
        container = self.container_type(value)
        iter_container = iter(container)

        try:
            while True:
                next(iter_container)
        except StopIteration as exc:
            assert exc.value == value  # noqa: PT017

    @pytest.mark.anyio()
    @pytest.mark.parametrize("value", list(range(10)))
    async def test_await(self, value: Any):
        current = sniffio.current_async_library()
        if current == "trio":
            return

        container = self.container_type(value)
        result = await container
        assert result == value

    @given(value_func_result())
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_map_value(self, values: Any):
        value, func, result = values
        container = self.container_type(value)
        new = container.map_value(func)
        assert new._value == result

    @given(values_func_result())
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_map_values(self, values: Any):
        value, other, func, result = values
        container = self.container_type(value)
        new = container.map_values(other, func)
        result = func(value, other)
        assert new._value == result

    @given(value_func_result())
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_bind_value(self, values: Any):
        value, func, result = values
        func = _func_as_container(func, self.container_type)

        container = self.container_type(value)
        new = container.bind_value(func)
        assert isinstance(new, self.container_type)
        assert new._value == result

    @given(values_func_result())
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_bind_values(self, values: Any):
        value, other, func, result = values
        func = _func_as_container(func, self.container_type)

        container = self.container_type(value)
        new = container.bind_values(other, func)
        assert isinstance(new, self.container_type)
        assert new._value == result

    @given(arbitrary)
    @settings(suppress_health_check=[HealthCheck.differing_executors])
    def test_unwrap(self, value: Any):
        container = self.container_type(value)
        result = container.unwrap()
        assert result == value

    @abstractmethod
    def test_map_value_error(self): ...

    @abstractmethod
    def test_map_values_error(self): ...

    @abstractmethod
    def test_bind_value_error(self): ...

    @abstractmethod
    def test_bind_values_error(self): ...

    def test_warn(self):
        for key in dir(self):
            if not key.startswith("test_"):
                continue

            method = getattr(self, key)
            marks: list[pytest.Mark] | None = getattr(method, "pytestmark", None)

            if not marks:
                continue

            for mark in marks:
                if mark.name != "skip":
                    continue
                break
            else:
                continue

            warnings.warn(
                f"\n[{BOLD_RED}{self.container_type.__name__}{RESET}] The test method "
                f"{RED}{key!r}{RESET} was skipped because it was undefined.",
                stacklevel=1,
            )
