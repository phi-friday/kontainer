from __future__ import annotations

from typing import Any, Callable

from hypothesis import given
from hypothesis import strategies as st

from kontainer import (
    Maybe,
    Option,
    Result,
    pipe_bind,
    pipe_iter_bind,
    pipe_iter_map,
    pipe_map,
)
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
    new = pipe_bind(container)
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


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.lists(st.integers(), min_size=1, max_size=100),
)
def test_pipe_iter_map_id(container_type: type[Container], xs: list[int]):
    ys = map(container_type, xs)
    zs = pipe_iter_map(ys)
    assert [z.unwrap() for z in zs] == xs


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.lists(st.integers(), min_size=1, max_size=100),
)
def test_pipe_iter_map_fn(container_type: type[Container], xs: list[int]):
    ys = (container_type(x) for x in xs)
    zs = pipe_iter_map(ys, lambda x: x + 1)
    assert [z.unwrap() for z in zs] == [x + 1 for x in xs]


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.lists(st.integers(), min_size=1, max_size=100),
    st.integers(),
    st.integers(),
)
def test_pipe_iter_map_fn_gn(
    container_type: type[Container], xs: list[int], y: int, z: int
):
    gn: Callable[[int], int] = lambda g: g * y
    fn: Callable[[int], int] = lambda x: x + z
    ys = (container_type(x) for x in xs)
    zs = pipe_iter_map(ys, fn, gn)
    assert [z.unwrap() for z in zs] == [gn(fn(x)) for x in xs]


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.lists(st.integers(), min_size=1, max_size=100),
)
def test_pipe_iter_bind_id(container_type: type[Container], xs: list[int]):
    ys = (container_type(x) for x in xs)
    zs = pipe_iter_bind(ys)
    assert [z.unwrap() for z in zs] == xs


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.lists(st.integers(), min_size=1, max_size=100),
)
def test_pipe_iter_bind_fn(container_type: type[Container], xs: list[int]):
    ys = (container_type(x) for x in xs)
    zs = pipe_iter_bind(ys, lambda x: container_type(x + 1))
    assert [z.unwrap() for z in zs] == [x + 1 for x in xs]


@given(
    st.one_of(st.just(Maybe), st.just(Option), st.just(Result)),
    st.lists(st.integers(), min_size=1, max_size=100),
    st.integers(),
    st.integers(),
)
def test_pipe_iter_bind_fn_gn(
    container_type: type[Container], xs: list[int], y: int, z: int
):
    gn: Callable[[int], Container[int, Any]] = lambda g: container_type(g * y)
    fn: Callable[[int], Container[int, Any]] = lambda x: container_type(x + z)
    ys = (container_type(x) for x in xs)
    zs = pipe_iter_bind(ys, fn, gn)
    assert [z.unwrap() for z in zs] == [gn(fn(x).unwrap()).unwrap() for x in xs]
