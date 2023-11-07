from __future__ import annotations

from itertools import accumulate
from typing import Callable, Iterable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer import Maybe, flowtools


@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_flow_starmap(xs: list[tuple[int, int]]):
    mapper: Callable[[int, int], int] = lambda x, y: x + y
    ys = flowtools.starmap(mapper)(xs)

    assert isinstance(ys, Iterable)
    assert list(ys) == [x + y for (x, y) in xs]


@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_flow_map2(xs: list[tuple[int, int]]):
    mapper: Callable[[int, int], int] = lambda x, y: x + y
    ys = flowtools.map2(mapper)(xs)

    assert isinstance(ys, Iterable)
    assert list(ys) == [x + y for (x, y) in xs]


@given(st.lists(st.tuples(st.integers(), st.integers(), st.integers())))
def test_flow_map3(xs: list[tuple[int, int, int]]):
    mapper: Callable[[int, int, int], int] = lambda x, y, z: x + y + z
    ys = flowtools.map3(mapper)(xs)

    assert isinstance(ys, Iterable)
    assert list(ys) == [x + y + z for (x, y, z) in xs]


@given(st.lists(st.integers()))
def test_flow_mapi(xs: list[int]):
    mapper: Callable[[int, int], int] = lambda i, x: x + i
    ys = flowtools.mapi(xs, mapper)

    assert isinstance(ys, Iterable)
    assert list(ys) == [x + i for i, x in enumerate(xs)]


@given(st.lists(st.integers(), min_size=1))
def test_flow_head(xs: list[int]):
    value = flowtools.head(xs)
    assert value == xs[0]


def test_flow_head_empty_source():
    with pytest.raises(ValueError, match="Sequence contains no elements"):
        flowtools.head(())


@given(st.lists(st.integers(), min_size=1), st.integers())
def test_seq_fold_pipe(xs: list[int], s: int):
    folder: Callable[[int, int], int] = lambda s, v: s + v
    value = flowtools.fold(xs, folder, s)
    assert value == sum(xs) + s


@given(st.integers(max_value=100))
def test_flow_unfold(x: int):
    def unfolder(state: int) -> Maybe[tuple[int, int]]:
        if state < x:
            return Maybe((state, state + 1))
        return Maybe(None)

    result = flowtools.unfold(0, unfolder)
    assert list(result) == list(range(x))


@given(st.lists(st.integers(), min_size=1), st.integers())
def test_flow_scan_pipe(xs: list[int], s: int):
    func: Callable[[int, int], int] = lambda s, v: s + v
    value = flowtools.scan(xs, func, s)

    expected: Iterable[int] = accumulate(xs, func, initial=s)
    assert list(value) == list(expected)


@given(st.lists(st.integers()))
def test_flow_concat_1(xs: list[int]):
    value = flowtools._concat(xs)
    assert list(value) == xs


@given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
def test_flow_append_3(xs: list[int], ys: list[int], zs: list[int]):
    value = flowtools.append(ys, zs)(xs)

    assert list(value) == xs + ys + zs


@given(st.lists(st.integers()), st.integers(min_value=0))
def test_flow_skip(xs: list[int], x: int):
    try:
        zs = flowtools.skip(xs, x)
        assert list(zs) == xs[x:]
    except ValueError:
        assert x > len(xs)


@given(st.lists(st.integers()), st.integers(min_value=0))
def test_flow_take(xs: list[int], x: int):
    try:
        zs = flowtools.take(xs, x)
        assert list(zs) == xs[:x]
    except ValueError:
        assert x > len(xs)


def test_flow_take_is_lazy():
    xs = flowtools.init_infinite()
    ys = flowtools.take(xs, 5)
    assert list(ys) == [0, 1, 2, 3, 4]


@given(st.lists(st.integers()))
def test_flow_delay(xs: list[int]):
    ran = False

    def generator() -> list[int]:
        nonlocal ran
        ran = True
        return list(xs)

    ys = flowtools.delay(generator)
    assert not ran

    assert list(ys) == xs
    assert ran


@given(st.lists(st.integers()))
def test_flow_infinite(xs: list[int]):
    ys = flowtools.zip(flowtools.init_infinite())(xs)

    expected = list(enumerate(xs))
    assert expected == list(ys)


def test_flow_infinite_even():
    ys = flowtools.take(flowtools.init_infinite(lambda x: x * 2), 5)

    assert list(ys) == [0, 2, 4, 6, 8]


@given(st.lists(st.integers(), min_size=1))
def test_flow_tail(xs: list[int]):
    ys = flowtools.tail(xs)
    zs = list(ys)

    assert len(xs) == len(zs) + 1
    assert xs[1:] == zs


def test_curry_one():
    @flowtools.curry
    def add(a: int) -> int:
        return a

    assert add(3)() == 3


def test_curry_two():
    @flowtools.curry
    def add(a: int, b: int) -> int:
        return a + b

    assert add(3)(4) == 7


def test_curry2_two():
    @flowtools.curry2
    def add(a: int, b: int) -> int:
        return a + b

    assert add(3)(4)() == 7


def test_curry2_three():
    @flowtools.curry2
    def add(a: int, b: int, c: int) -> int:
        return a + b + c

    assert add(3)(4)(5) == 12


def test_curry3_three():
    @flowtools.curry3
    def add(a: int, b: int, c: int) -> int:
        return a + b + c

    assert add(3)(4)(5)() == 12


def test_curry3_four():
    @flowtools.curry3
    def add(a: int, b: int, c: int, d: int) -> int:
        return a + b + c + d

    assert add(3)(4)(5)(6) == 18
