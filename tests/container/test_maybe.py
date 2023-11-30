from __future__ import annotations

from typing import Any, Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.container.base import BaseTestContainer

from kontainer import undefined
from kontainer.container.maybe import Maybe, Null, Some

arbitrary = st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers()))


class TestMaybe(BaseTestContainer):
    container_type: type[Maybe] = Maybe


@pytest.mark.parametrize("null_value", [None, undefined])
def test_create_null(null_value: Any):
    null = Maybe(null_value)
    assert isinstance(null, Null)
    assert null.unwrap() is None


def test_switch_some():
    maybe = Maybe(1)
    assert isinstance(maybe, Some)
    result = maybe.switch()
    assert isinstance(result, Null)
    assert result.unwrap() is None


def test_switch_null():
    maybe = Maybe(None)
    assert isinstance(maybe, Null)
    result = maybe.switch()
    assert isinstance(result, Some)
    assert result.unwrap() is None


@given(arbitrary, arbitrary)
def test_default_some(value: Any, other: Any):
    maybe = Some(value)
    assert isinstance(maybe, Some)
    result = maybe.default(other)
    assert result == value


@given(arbitrary, arbitrary)
def test_default_null(value: Any, other: Any):
    maybe = Null(value)
    assert isinstance(maybe, Null)
    result = maybe.default(other)
    assert result == other


@given(arbitrary, arbitrary)
def test_map_default_some(value: Any, other: Any):
    maybe = Some(value)
    assert isinstance(maybe, Some)
    func = lambda: other
    result = maybe.map_default(func)
    assert result == value


@given(arbitrary, arbitrary)
def test_map_default_null(value: Any, other: Any):
    maybe = Null(value)
    assert isinstance(maybe, Null)
    func = lambda: other
    result = maybe.map_default(func)
    assert result == other


@given(arbitrary, arbitrary)
def test_map_null_value(value: Any, other: Any):
    null = Null(value)
    assert isinstance(null, Null)

    func: Callable[[Any], Any] = lambda x: other  # noqa: ARG005
    result = null.map_value(func)

    assert isinstance(result, Null)
    assert result.unwrap() is None


@given(arbitrary, arbitrary, arbitrary)
def test_map_null_values(value: Any, element: Any, other: Any):
    null = Null(value)
    assert isinstance(null, Null)

    func: Callable[[Any, Any], Any] = lambda x, y: other  # noqa: ARG005
    result = null.map_values(element, func)

    assert isinstance(result, Null)
    assert result.unwrap() is None


@given(arbitrary, arbitrary)
def test_bind_null_value(value: Any, other: Any):
    null = Null(value)
    assert isinstance(null, Null)

    func: Callable[[Any], Maybe[Any]] = lambda x: Some(other)  # noqa: ARG005
    result = null.bind_value(func)

    assert isinstance(result, Null)
    assert result.unwrap() is None


@given(arbitrary, arbitrary, arbitrary)
def test_bind_null_values(value: Any, element: Any, other: Any):
    null = Null(value)
    assert isinstance(null, Null)

    func: Callable[[Any, Any], Maybe[Any]] = lambda x, y: Some(other)  # noqa: ARG005
    result = null.bind_values(element, func)

    assert isinstance(result, Null)
    assert result.unwrap() is None


@given(arbitrary, st.one_of(st.just(Some), st.just(Null)))
def test_str(value: Any, container_type: type[Some | Null]):
    maybe = container_type(value)
    assert str(maybe) == str(value)


@given(st.one_of(arbitrary, st.none(), st.just(undefined)))
def test_repr(value: Any):
    format_text = "<{name}: value={value}>"
    maybe = Maybe(value)
    if isinstance(maybe, Some):
        name = "Some"
    elif isinstance(maybe, Null):
        name = "Null"
    else:
        name = "Maybe"

    if value is undefined:
        value = None

    assert repr(maybe) == format_text.format(name=name, value=repr(value))


@given(st.one_of(arbitrary, st.none(), st.just(undefined)))
def test_positive(value: Any):
    maybe = Maybe(value)
    if isinstance(maybe, Some):
        assert maybe.is_positive is True
    else:
        assert maybe.is_positive is False


@given(st.one_of(arbitrary, st.none(), st.just(undefined)))
def test_negative(value: Any):
    maybe = Maybe(value)
    if isinstance(maybe, Some):
        assert maybe.is_negative is False
    else:
        assert maybe.is_negative is True


@given(arbitrary)
def test_construct_using_alias_some(value: Any):
    maybe = Maybe.some(value)
    assert isinstance(maybe, Some)
    assert maybe.unwrap() == value


@given(arbitrary)
def test_construct_using_alias_null(value: Any):
    maybe = Maybe.null(value)
    assert isinstance(maybe, Null)
    assert maybe.unwrap() is None
