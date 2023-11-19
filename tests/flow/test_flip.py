from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer import flip, flip_func


@given(st.integers(), st.integers())
def test_flip_func(x: Any, y: Any):
    func = lambda x, y: (x, y)
    fliped = flip_func(func)

    new = fliped(x, y)
    assert isinstance(new, tuple)
    assert new == (y, x)


@given(st.integers(), st.integers(), st.lists(st.integers()))
def test_filp(x: Any, y: Any, z: list[Any]):
    value = (x, y, *z)
    expect = (y, x, *z)
    result = flip(value)

    assert isinstance(result, tuple)
    assert expect == result


@given(st.integers(), st.integers(), st.lists(st.integers()))
def test_flip_var_args(x: Any, y: Any, z: list[Any]):
    @flip_func
    def f(*args: Any) -> Any:
        return args

    value = (x, y, *z)
    expect = (y, x, *z)
    result = f(*value)

    assert isinstance(result, tuple)
    assert expect == result


def test_flip_arg_require_error():
    func = lambda x,: (x,)
    with pytest.raises(TypeError, match="Too few parameters required by func: 1 < 2"):
        flip_func(func)  # type: ignore


def test_flip_keyword_arg_error():
    def func(x: Any, y: Any, *, a: Any) -> tuple[Any, Any, Any]:
        return (x, y, a)

    with pytest.raises(
        TypeError,
        match="only use functions that take positional parameters. a: KEYWORD_ONLY",
    ):
        flip_func(func)  # type: ignore


def test_flip_var_keyword_arg_error():
    def func(x: Any, y: Any, **kwargs: Any) -> tuple[Any, ...]:
        return (x, y, *kwargs)

    with pytest.raises(
        TypeError,
        match="only use functions that take positional parameters. "
        "kwargs: VAR_KEYWORD",
    ):
        flip_func(func)  # type: ignore
