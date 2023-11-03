from __future__ import annotations

from typing import Any, Callable, Iterable

from hypothesis import given  # type: ignore
from hypothesis import strategies as st

from kontainer import Maybe, Option, Result, bind_elements, map_elements
from kontainer.core.types import Container


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.lists(st.integers())
)
def test_pipe_map(container_type: type[Container], xs: list[int]):
    func: Callable[[int], int] = lambda x: x + 1
    xss = (container_type(x) for x in xs)
    ys = map_elements(xss, func)

    assert isinstance(ys, Iterable)
    assert list(ys) == [container_type(func(x)) for x in xs]


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.lists(st.integers())
)
def test_pipe_bind(container_type: type[Container], xs: list[int]):
    func: Callable[[int], Container[int, Any]] = lambda x: container_type(x + 1)
    xss = (container_type(x) for x in xs)
    ys = bind_elements(xss, func)

    assert isinstance(ys, Iterable)
    assert list(ys) == [func(x) for x in xs]


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.lists(st.integers())
)
def test_pipe_bind_eager(container_type: type[Container], xs: list[int]):
    func: Callable[[int], Container[int, Any]] = lambda x: container_type(x + 1)
    xss = (container_type(x) for x in xs)
    ys = bind_elements(xss, func, lazy=False)

    assert isinstance(ys, tuple)
    assert list(ys) == [func(x) for x in xs]


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.lists(st.integers())
)
def test_pipe_map_eager(container_type: type[Container], xs: list[int]):
    func: Callable[[int], int] = lambda x: x + 1
    xss = (container_type(x) for x in xs)
    ys = map_elements(xss, func, lazy=False)

    assert isinstance(ys, tuple)
    assert list(ys) == [container_type(func(x)) for x in xs]
