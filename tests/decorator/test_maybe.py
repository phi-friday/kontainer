from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer.decorator import wrap
from kontainer.maybe import Maybe


@given(st.integers())
def test_wrap_func(value: Any):
    @wrap
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Maybe)
    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_generator(value: Any):
    @wrap
    def f() -> Any:
        for _ in range(10):
            yield
        return value

    maybe = f()
    assert isinstance(maybe, Maybe)

    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_yield_from(value: Any):
    maybe_list = [Maybe(x) for x in range(10)]

    @wrap
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


@given(st.integers())
def test_wrap_error(value: Any):
    @wrap
    def f() -> Any:
        raise Exception(value)  # noqa: TRY002

    maybe = f()
    assert isinstance(maybe, Maybe)

    with pytest.raises(ValueError, match="does not have a value."):
        maybe.unwrap()

    other = maybe.unwrap_other()
    assert isinstance(other, Exception)
    assert other.args[0] == value


@given(st.integers())
def test_wrap_nested(value: Any):
    @wrap
    def f() -> Any:
        return Maybe(value)

    maybe = f()
    assert isinstance(maybe, Maybe)
    result = maybe.unwrap()
    assert result == value
