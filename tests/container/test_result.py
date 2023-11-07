from __future__ import annotations

from typing import Any, Callable

import pytest
from typing_extensions import override

from tests.container.base import BaseTestContainer

from kontainer.container import Result
from kontainer.core.types import Container


def _error(x: Any) -> None:
    raise ValueError(x)


def _errors(x: Any, y: Any) -> None:
    error_msg = f"{x}:{y}"
    raise ValueError(error_msg)


def _func_as_container(
    func: Callable[..., Any], container_type: type[Container]
) -> Callable[..., Container]:
    def inner(*args: Any) -> Container[Any, Any]:
        result = func(*args)
        if isinstance(result, container_type):
            return result
        return container_type(result)

    return inner


class TestResult(BaseTestContainer):
    container_type = Result

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
