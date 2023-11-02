from __future__ import annotations

from typing import Any

import pytest

from tests.maybe.base import BaseTestContainer

from kontainer.maybe import Maybe


class TestMaybe(BaseTestContainer):
    container_type = Maybe

    @pytest.mark.parametrize("value", [1, "b", b"1"])
    def test_construct_without_other(self, value: Any):
        super().test_construct_without_other(value)

    @pytest.mark.parametrize(
        ("value", "other"), [(1, "b"), ("b", (1,)), (b"1", frozenset())]
    )
    def test_construct_with_other(self, value: Any, other: Any):
        super().test_construct_with_other(value, other)
