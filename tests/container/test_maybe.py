from __future__ import annotations

from typing import Any

import pytest
from typing_extensions import override

from tests.container.base import BaseTestContainer

from kontainer.container import Maybe


def _error(x: Any) -> None:
    raise ValueError(x)


def _errors(x: Any, y: Any) -> None:
    error_msg = f"{x}:{y}"
    raise ValueError(error_msg)


class TestMaybe(BaseTestContainer):
    container_type: type[Maybe] = Maybe

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
    def test_bind_value_error(self): ...

    @override
    def test_bind_values_error(self): ...
