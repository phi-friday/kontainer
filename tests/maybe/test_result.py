from __future__ import annotations

from typing import Any, Callable

import pytest

from tests.maybe.base import BaseTestContainer

from kontainer import undefined
from kontainer.maybe import Result


class TestResult(BaseTestContainer):
    container_type = Result

    @pytest.mark.parametrize(
        ("value", "other"),
        [
            (ValueError(1), Exception(4)),
            (TypeError(2), ValueError(5)),
            (Exception(3), TypeError(6)),
        ],
    )
    def test_switch(self, value: Any, other: Any):
        return super().test_switch(value, other)

    def test_default_other(self):
        container = self.container_type(1, Exception())
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

    @pytest.mark.parametrize("other", [Exception(1), ValueError(2), TypeError(3)])
    def test_unwrap_other(self, other: Exception):
        container = self.container_type(undefined, other)
        with pytest.raises(type(other)):
            container.unwrap_other()

    @pytest.mark.skip()
    def test_unwrap_other_error(self): ...
