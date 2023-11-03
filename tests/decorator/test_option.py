from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer import undefined
from kontainer.decorator import optional
from kontainer.maybe import Option


@given(st.integers())
def test_wrap_func(value: Any):
    @optional
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Option)
    result = maybe.unwrap()
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


@given(st.integers())
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


@given(st.integers())
def test_wrap_yield_from(value: Any):
    maybe_list = [Option(x) for x in range(10)]

    @optional
    def f() -> Any:
        for x in maybe_list:
            y = yield from x
            assert isinstance(y, int)
            assert y == x.unwrap()
        return value

    maybe = f()
    assert isinstance(maybe, Option)

    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_nested(value: Any):
    @optional
    def f() -> Any:
        return Option(value)

    maybe = f()
    assert isinstance(maybe, Option)
    result = maybe.unwrap()
    assert result == value
