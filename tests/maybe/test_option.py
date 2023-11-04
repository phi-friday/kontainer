from __future__ import annotations

from typing import Any, Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.maybe.base import BaseTestContainer

from kontainer.core.const import undefined
from kontainer.maybe import Option


class TestOption(BaseTestContainer):
    container_type: type[Option] = Option

    @given(
        st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers())),
        st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers())),
    )
    def test_construct_with_other(self, value: Any, other: Any):
        container = self.container_type(value, other)
        assert isinstance(container, self.container_type)
        assert container._value == value
        assert container._other is undefined

    # TODO: remove skip
    @pytest.mark.skip()
    def test_error_construct_only_undefined_with_other(self): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_error_construct_only_undefined_without_other(self): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_map_other(
        self, other: Any, func: Callable[[None], Any] | Callable[[], Any], result: Any
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_map_others(
        self,
        other: Any,
        another: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_alt_value(self, value: Any, func: Callable[[None], Any], result: Any): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_alt_values(
        self,
        value: Any,
        other: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_alt_other(self, other: Any, func: Callable[[Any], Any], result: Any): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_alt_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_bind_other(
        self, other: Any, func: Callable[[None], Any] | Callable[[], Any], result: Any
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_bind_others(
        self,
        other: Any,
        another: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_lash_value(
        self, value: Any, func: Callable[[None], Any] | Callable[[], Any], result: Any
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_lash_values(
        self,
        value: Any,
        other: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_lash_other(self, other: Any, func: Callable[[Any], Any], result: Any): ...

    # TODO: remove skip
    @pytest.mark.skip()
    def test_lash_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ): ...

    def test_switch(self):
        container = self.container_type(1)
        with pytest.raises(NotImplementedError):
            container.switch()

    def test_default_other(self):
        container = self.container_type(1)
        with pytest.raises(NotImplementedError):
            container.default_other(1)

    @pytest.mark.skip()
    def test_non_default_other(self): ...

    def test_map_default_other(self):
        container = self.container_type(1)
        with pytest.raises(NotImplementedError):
            container.map_default_other(lambda: 1)

    @pytest.mark.skip()
    def test_map_non_default_other(self, func: Callable[[], Any]): ...

    @pytest.mark.skip()
    def test_unwrap_error(self): ...

    @pytest.mark.parametrize("null", [None, undefined])
    def test_unwrap_null(self, null: Any):
        container = self.container_type(null)
        assert container.unwrap() is None

    def test_unwrap_other(self):
        container = self.container_type(undefined)
        with pytest.raises(NotImplementedError):
            container.unwrap_other()

    @pytest.mark.skip()
    def test_unwrap_other_error(self): ...
