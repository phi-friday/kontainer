from __future__ import annotations

from typing import Any

import pytest

from tests.maybe.base import BaseTestContainer

from kontainer.core.const import undefined
from kontainer.maybe import Option


class TestOption(BaseTestContainer):
    container_type = Option

    @pytest.mark.parametrize("value", [1, "b", b"1"])
    def test_construct_without_other(self, value: Any):
        super().test_construct_without_other(value)

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
