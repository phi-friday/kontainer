from __future__ import annotations

from typing import Any

import pytest

from kontainer.utils import func

PARAMS = [(1, 2, 3, 4), ("b", 1, b"", ()), (4, 5, 3, "text", b"")]


@pytest.mark.parametrize("values", [(1, 2, 3), ("b", 1, b""), (4,)])
def test_identity(values: tuple[Any, ...]):
    value = func.identity(values)
    assert value == values


@pytest.mark.parametrize("values", PARAMS)
def test_first(values: tuple[Any, ...]):
    value = func.first(values)
    assert value == values[0]


@pytest.mark.parametrize("values", PARAMS)
def test_second(values: tuple[Any, ...]):
    value = func.second(values)
    assert value == values[1]


@pytest.mark.parametrize("values", PARAMS)
def test_third(values: tuple[Any, ...]):
    value = func.third(values)
    assert value == values[2]


@pytest.mark.parametrize("values", PARAMS)
def test_fourth(values: tuple[Any, ...]):
    value = func.fourth(values)
    assert value == values[3]
