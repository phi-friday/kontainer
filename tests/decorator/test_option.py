from __future__ import annotations

from typing import Any

import pytest

from kontainer import undefined
from kontainer.decorator import optional
from kontainer.maybe import Option


@pytest.mark.parametrize("value", list(range(5)))
def test_wrap_func(value: Any):
    @optional
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Option)
    result = maybe.default(undefined)
    assert result == value


@pytest.mark.parametrize("null", [undefined, None])
def test_wrap_null(null: Any):
    @optional
    def f() -> None:
        return null

    maybe = f()
    assert isinstance(maybe, Option)
    result = maybe.unwrap()
    assert result is None


@pytest.mark.parametrize("value", list(range(5)))
def test_wrap_generator(value: Any):
    @optional
    def f() -> Any:
        for _ in range(10):
            yield
        return value

    maybe = f()
    assert isinstance(maybe, Option)

    result = maybe.unwrap()
    assert result == value


@pytest.mark.parametrize("value", list(range(5)))
def test_wrap_yield_from(value: Any):
    maybe_list = [Option(x) for x in range(10)]

    @optional
    def f() -> Any:
        for x in maybe_list:
            y = yield from x
            assert isinstance(y, int)
            assert y == x.default(undefined)
        return value

    maybe = f()
    assert isinstance(maybe, Option)

    result = maybe.unwrap()
    assert result == value
