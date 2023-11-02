from __future__ import annotations

from typing import Any, Callable

import pytest

from tests.maybe.base import BaseTestContainer

from kontainer.core.const import undefined
from kontainer.maybe import Option


class TestOption(BaseTestContainer):
    container_type: type[Option] = Option

    @pytest.mark.parametrize(
        ("value", "other"), [(1, "b"), ("b", (1,)), (b"1", frozenset())]
    )
    def test_construct_with_other(self, value: Any, other: Any):
        container = self.container_type(value, other)
        assert isinstance(container, self.container_type)
        assert container._value == value
        assert container._other is undefined

    @pytest.mark.skip()
    def test_error_construct_only_undefined_with_other(self): ...

    @pytest.mark.skip()
    def test_error_construct_only_undefined_without_other(self): ...

    @pytest.mark.skip()
    def test_map_other(
        self, other: Any, func: Callable[[None], Any] | Callable[[], Any], result: Any
    ): ...

    @pytest.mark.skip()
    def test_map_others(
        self,
        other: Any,
        another: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    @pytest.mark.skip()
    def test_alt_value(self, value: Any, func: Callable[[None], Any], result: Any): ...

    @pytest.mark.skip()
    def test_alt_values(
        self,
        value: Any,
        other: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    @pytest.mark.skip()
    def test_alt_other(self, other: Any, func: Callable[[Any], Any], result: Any): ...

    @pytest.mark.skip()
    def test_alt_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ): ...

    @pytest.mark.skip()
    def test_bind_other(
        self, other: Any, func: Callable[[None], Any] | Callable[[], Any], result: Any
    ): ...

    @pytest.mark.skip()
    def test_bind_others(
        self,
        other: Any,
        another: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    @pytest.mark.skip()
    def test_lash_value(
        self, value: Any, func: Callable[[None], Any] | Callable[[], Any], result: Any
    ): ...

    @pytest.mark.skip()
    def test_lash_values(
        self,
        value: Any,
        other: Any,
        func: Callable[[None, Any], Any] | Callable[[Any], Any],
        result: Any,
    ): ...

    @pytest.mark.skip()
    def test_lash_other(self, other: Any, func: Callable[[Any], Any], result: Any): ...

    @pytest.mark.skip()
    def test_lash_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ): ...

    def test_switch(self):
        container = self.container_type(1)
        with pytest.raises(NotImplementedError):
            container.switch()
