from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer import undefined
from kontainer.container import Maybe
from kontainer.decorator import optional

arbitrary = st.one_of(
    st.integers(), st.text(), st.binary(), st.tuples(st.integers()), st.none()
)


@given(arbitrary)
def test_wrap_func(value: Any):
    @optional
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Maybe)
    result = maybe.unwrap()
    assert result == value


@pytest.mark.parametrize("null", [undefined, None])
def test_wrap_null(null: Any):
    @optional
    def f() -> None:
        return null

    maybe = f()
    assert isinstance(maybe, Maybe)
    result = maybe.unwrap()
    assert result is None


@given(arbitrary)
def test_wrap_generator(value: Any):
    @optional
    def f() -> Any:
        for _ in range(10):
            yield
        return value

    maybe = f()
    assert isinstance(maybe, Maybe)

    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
def test_wrap_yield_from(value: Any):
    maybe_list = [Maybe(x) for x in range(10)]

    @optional
    def f() -> Any:
        for x in maybe_list:
            y = yield from x
            assert isinstance(y, int)
            assert y == x.unwrap()
        return value

    maybe = f()
    assert isinstance(maybe, Maybe)

    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
def test_wrap_nested(value: Any):
    @optional
    def f() -> Any:
        return Maybe(value)

    maybe = f()
    assert isinstance(maybe, Maybe)
    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
def test_wrap_async(value: Any):
    maybe = Maybe(value)

    @optional
    async def f() -> Any:
        return await maybe

    result = f()
    assert isinstance(result, Maybe)
    assert result.unwrap() == value


@given(arbitrary)
def test_wrap_async_nested(value: Any):
    maybe = Maybe(value)

    @optional
    async def f() -> Any:
        new = await maybe
        return Maybe(new)

    result = f()
    assert isinstance(result, Maybe)
    assert result.unwrap() == value


@given(arbitrary)
def test_wrap_async_more_nested(value: Any):
    maybe = Maybe(value)

    @optional
    async def f() -> Any:
        new = await maybe
        return Maybe(new)

    @optional
    async def g() -> Any:
        left = await maybe
        right = await f()
        return Maybe((left, right))

    result = g()
    assert isinstance(result, Maybe)
    assert result.unwrap() == (value, value)
