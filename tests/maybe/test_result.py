from __future__ import annotations

from inspect import isclass
from typing import Any, Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st
from typing_extensions import override

from tests.maybe.base import BaseTestContainer

from kontainer import catch, undefined
from kontainer.core.exception import KontainerTypeError
from kontainer.core.types import Container
from kontainer.maybe import Result


def _error(x: Any) -> None:
    raise ValueError(x)


def _errors(x: Any, y: Any) -> None:
    error_msg = f"{x}:{y}"
    raise ValueError(error_msg)


def _func_as_value_container(
    func: Callable[..., Any], container_type: type[Container]
) -> Callable[..., Container]:
    def inner(*args: Any) -> Container[Any, Any]:
        result = func(*args)
        if isinstance(result, container_type):
            return result
        return container_type(result)

    return inner


def _func_as_other_container(
    func: Callable[..., Any], container_type: type[Container]
) -> Callable[..., Container]:
    def inner(*args: Any) -> Container[Any, Any]:
        result = func(*args)
        if isinstance(result, container_type):
            return result
        return container_type(undefined, result)

    return inner


class TestResult(BaseTestContainer):
    container_type = Result

    @given(
        st.integers(),
        st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
    )
    @override
    def test_construct_with_other(self, value: Any, other: Any):
        container = self.container_type(value, other)
        assert isinstance(container, self.container_type)
        assert container._value == value
        assert container._other == other
        assert isinstance(container._other, Exception) or (
            isclass(container._other) and issubclass(container._other, Exception)
        )

    @given(
        st.integers(),
        st.lists(
            st.one_of(
                st.just(Exception),
                st.just(ValueError),
                st.just(TypeError),
                st.just(IndexError),
                st.just(ImportError),
            ),
            unique=True,
            min_size=2,
            max_size=2,
        ),
    )
    @override
    def test_map_other(self, value: Any, error_types: list[type[Exception]]):
        error_type, other_error_type = error_types
        error = error_type(value)

        def func(x: Any) -> Any:
            return other_error_type(str(x))

        container = self.container_type(undefined, error)
        new = container.map_other(func)
        assert isinstance(new._other, other_error_type)

    @given(
        st.integers(),
        st.integers(),
        st.lists(
            st.one_of(
                st.just(Exception),
                st.just(ValueError),
                st.just(TypeError),
                st.just(IndexError),
                st.just(ImportError),
            ),
            unique=True,
            min_size=2,
            max_size=2,
        ),
    )
    @override
    def test_map_others(
        self, value: Any, other: Any, error_types: list[type[Exception]]
    ):
        error_type, other_error_type = error_types
        error = error_type(value)

        def func(x: Any, y: Any) -> Any:
            return other_error_type(f"{x}:{y}")

        container = self.container_type(undefined, error)
        new = container.map_others(other, func)
        assert isinstance(new._other, other_error_type)

    @given(
        st.integers(),
        st.lists(
            st.one_of(
                st.just(Exception),
                st.just(ValueError),
                st.just(TypeError),
                st.just(IndexError),
                st.just(ImportError),
            ),
            unique=True,
            min_size=2,
            max_size=2,
        ),
    )
    @override
    def test_bind_other(self, other: Any, error_types: list[type[Exception]]):
        error_type, other_error_type = error_types

        @catch
        def func(x: Any) -> Any:
            raise other_error_type(str(x))

        container = self.container_type(undefined, error_type(other))
        new = container.bind_other(func)
        assert isinstance(new, self.container_type)
        assert isinstance(new._other, other_error_type)

    @given(
        st.integers(),
        st.integers(),
        st.lists(
            st.one_of(
                st.just(Exception),
                st.just(ValueError),
                st.just(TypeError),
                st.just(IndexError),
                st.just(ImportError),
            ),
            unique=True,
            min_size=2,
            max_size=2,
        ),
    )
    @override
    def test_bind_others(
        self, other: Any, another: Any, error_types: list[type[Exception]]
    ):
        error_type, other_error_type = error_types

        @catch
        def func(x: Any, y: Any) -> Any:
            raise other_error_type(f"{x}:{y}")  # noqa: EM102

        container = self.container_type(undefined, error_type(other))
        new = container.bind_others(another, func)
        assert isinstance(new, self.container_type)
        assert isinstance(new._other, other_error_type)

    @given(
        st.builds(
            lambda x, y: x(y),
            st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
            st.integers(),
        ),
        st.builds(
            lambda x, y: x(y),
            st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
            st.integers(),
        ),
    )
    @override
    def test_switch(self, value: Any, other: Any):
        return super().test_switch(value, other)

    @override
    def test_default_other(self):
        container = self.container_type(1, Exception())
        with pytest.raises(NotImplementedError):
            container.default_other(1)

    @pytest.mark.skip()
    @override
    def test_non_default_other(self): ...

    @override
    def test_map_default_other(self):
        container = self.container_type(1)
        with pytest.raises(NotImplementedError):
            container.map_default_other(lambda: 1)

    @pytest.mark.skip()
    @override
    def test_map_non_default_other(self, func: Callable[[], Any]): ...

    @given(
        st.builds(
            lambda x, y: x(y),
            st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
            st.integers(),
        )
    )
    @override
    def test_unwrap_other(self, other: Exception):
        container = self.container_type(undefined, other)
        with pytest.raises(type(other)):
            container.unwrap_other()

    @pytest.mark.skip()
    @override
    def test_unwrap_other_error(self): ...

    @given(st.integers())
    @override
    def test_switch_non_error_value(self, value: Any):
        result = self.container_type(value, Exception())
        new = result.switch()
        with pytest.raises(KontainerTypeError):
            new.unwrap_other()

    @given(
        st.one_of(
            st.integers(),
            st.text(),
            st.binary(),
            st.tuples(st.integers()),
            st.just(undefined),
        ),
        st.one_of(
            st.integers(),
            st.text(),
            st.binary(),
            st.tuples(st.integers()),
            st.just(undefined),
        ),
        st.one_of(
            st.just(Exception),
            st.just(ValueError),
            st.just(TypeError),
            st.just(IndexError),
            st.just(ImportError),
        ),
    )
    @override
    def test_repr(self, value: Any, other: Any, error_type: type[Exception]):
        other = error_type(other)
        container = self.container_type(value, other)
        name = self.container_type.__name__
        text = repr(container)
        if value is undefined:
            assert text == f"<{name!s}: other={other!r}>"
        elif other is undefined:
            assert text == f"<{name!s}: value={value!r}>"
        else:
            assert text == f"<{name!s}: value={value!r}, other={other!r}>"

    @given(
        st.one_of(
            st.integers(),
            st.text(),
            st.binary(),
            st.tuples(st.integers()),
            st.just(undefined),
        ),
        st.one_of(
            st.integers(),
            st.text(),
            st.binary(),
            st.tuples(st.integers()),
            st.just(undefined),
        ),
        st.one_of(
            st.just(Exception),
            st.just(ValueError),
            st.just(TypeError),
            st.just(IndexError),
            st.just(ImportError),
        ),
    )
    @override
    def test_str(self, value: Any, other: Any, error_type: type[Exception]):
        other = error_type(other)
        container = self.container_type(value, other)
        assert str(container) == str(value)

    @override
    def test_map_value_error(self):
        container = self.container_type(1)
        with pytest.raises(ValueError, match="1"):
            container.map_value(_error)

    @override
    def test_map_values_error(self):
        container = self.container_type(1)
        with pytest.raises(ValueError, match="1:2"):
            container.map_values(2, _errors)

    @override
    def test_map_other_error(self):
        container = self.container_type(1, Exception(3))
        with pytest.raises(ValueError, match="3"):
            container.map_other(_error)

    @override
    def test_map_others_error(self):
        container = self.container_type(1, Exception(3))
        with pytest.raises(ValueError, match="3:2"):
            container.map_others(2, _errors)

    @override
    def test_bind_value_error(self): ...

    @override
    def test_bind_values_error(self): ...

    @override
    def test_bind_other_error(self): ...

    @override
    def test_bind_others_error(self): ...
