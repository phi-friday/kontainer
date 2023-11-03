from __future__ import annotations

from typing import Any, Callable

from hypothesis import given
from hypothesis import strategies as st

from kontainer import Maybe, Option, Result, pipe_bind, pipe_map
from kontainer.core.types import Container


@given(st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.integers())
def test_pipe_map_id(container_type: type[Container], x: int):
    container = container_type(x)
    new = pipe_map(container)
    value = new.unwrap()
    assert value == x


@given(st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.integers())
def test_pipe_map_fn(container_type: type[Container], x: int):
    container = container_type(x)
    new = pipe_map(container, lambda x: x + 1)
    value = new.unwrap()
    assert value == x + 1


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.integers(),
    st.integers(),
    st.integers(),
)
def test_pipe_map_fn_gn(container_type: type[Container], x: int, y: int, z: int):
    gn: Callable[[int], int] = lambda g: g * y
    fn: Callable[[int], int] = lambda x: x + z
    container = container_type(x)
    new = pipe_map(container, fn, gn)
    value = new.unwrap()
    assert value == gn(fn(x))


@given(st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.integers())
def test_pipe_bind_id(container_type: type[Container], x: int):
    container = container_type(x)
    new = pipe_map(container)
    value = new.unwrap()
    assert value == x


@given(st.one_of(st.just(Maybe), st.just(Option), st.just(Result)), st.integers())
def test_pipe_bind_fn(container_type: type[Container], x: int):
    container = container_type(x)
    new = pipe_bind(container, lambda x: container_type(x + 1))
    value = new.unwrap()
    assert value == x + 1


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.integers(),
    st.integers(),
    st.integers(),
)
def test_pipe_bind_fn_gn(container_type: type[Container], x: int, y: int, z: int):
    gn: Callable[[int], Container[int, Any]] = lambda g: container_type(g * y)
    fn: Callable[[int], Container[int, Any]] = lambda x: container_type(x + z)
    container = container_type(x)
    new = pipe_bind(container, fn, gn)
    value = new.unwrap()
    assert value == gn(fn(x).unwrap()).unwrap()
