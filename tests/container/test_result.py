from __future__ import annotations

from typing import Any, Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.container.base import BaseTestContainer

from kontainer import undefined
from kontainer.container.result import Done, Error, Result
from kontainer.core.exception import KontainerTypeError, KontainerValueError

arbitrary = st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers()))


class _Const: ...


class TestResult(BaseTestContainer):
    container_type = Result


@given(st.builds(Exception, arbitrary))
def test_create_error(error: Any):
    result = Result(error)
    assert isinstance(result, Error)


@given(arbitrary)
def test_unwrap_error(value: Any):
    error = Error(value)
    assert isinstance(error, Error)
    with pytest.raises(KontainerValueError):
        error.unwrap()


@given(
    st.one_of(
        st.builds(ValueError, arbitrary),
        st.builds(TypeError, arbitrary),
        st.builds(IndexError, arbitrary),
    )
)
def test_unwrap_error_func(value: Any):
    error = Error(value)
    assert isinstance(error, Error)
    with pytest.raises(type(value)):
        error.unwrap_error()


@given(arbitrary)
def test_unwrap_error_without_error(value: Any):
    assert not isinstance(value, Exception)
    error = Error(value)
    assert isinstance(error, Error)
    with pytest.raises(KontainerTypeError):
        error.unwrap_error()


@given(arbitrary)
def test_unwrap_done(value: Any):
    done = Done(value)
    assert isinstance(done, Done)
    with pytest.raises(KontainerTypeError):
        done.unwrap_error()


def test_switch_done():
    value = _Const()
    result = Result(value)
    assert isinstance(result, Done)
    error = result.switch()
    assert isinstance(error, Error)
    assert error._value is undefined
    assert error._other is value


def test_switch_error():
    error = Exception()
    result = Result(error)
    assert isinstance(result, Error)
    result = result.switch()
    assert isinstance(result, Done)
    assert result.unwrap() is error


@given(arbitrary, arbitrary)
def test_default_done(value: Any, other: Any):
    result = Done(value)
    assert isinstance(result, Done)
    default = result.default(other)
    assert default == value


@given(arbitrary, arbitrary)
def test_default_error(value: Any, other: Any):
    maybe = Error(value)
    assert isinstance(maybe, Error)
    default = maybe.default(other)
    assert default == other


@given(arbitrary, arbitrary)
def test_map_default_done(value: Any, other: Any):
    result = Done(value)
    assert isinstance(result, Done)
    func = lambda: other
    default = result.map_default(func)
    assert default == value


@given(arbitrary, arbitrary)
def test_map_default_error(value: Any, other: Any):
    result = Error(value)
    assert isinstance(result, Error)
    func = lambda: other
    default = result.map_default(func)
    assert default == other


@given(arbitrary, arbitrary)
def test_map_error_value(value: Any, other: Any):
    error = Error(value)
    assert isinstance(error, Error)

    func: Callable[[Any], Any] = lambda x: other  # noqa: ARG005
    result = error.map_value(func)

    assert isinstance(result, Error)
    with pytest.raises(KontainerValueError):
        result.unwrap()


@given(arbitrary, arbitrary, arbitrary)
def test_map_error_values(value: Any, element: Any, other: Any):
    null = Error(value)
    assert isinstance(null, Error)

    func: Callable[[Any, Any], Any] = lambda x, y: other  # noqa: ARG005
    result = null.map_values(element, func)

    assert isinstance(result, Error)
    with pytest.raises(KontainerValueError):
        result.unwrap()


@given(arbitrary, arbitrary)
def test_bind_error_value(value: Any, other: Any):
    null = Error(value)
    assert isinstance(null, Error)

    func: Callable[[Any], Result[Any, Any]] = lambda x: Done(other)  # noqa: ARG005
    result = null.bind_value(func)

    assert isinstance(result, Error)
    with pytest.raises(KontainerValueError):
        result.unwrap()


@given(arbitrary, arbitrary, arbitrary)
def test_bind_error_values(value: Any, element: Any, other: Any):
    null = Error(value)
    assert isinstance(null, Error)

    func: Callable[[Any, Any], Result[Any, Any]] = lambda x, y: Done(other)  # noqa: ARG005
    result = null.bind_values(element, func)

    assert isinstance(result, Error)
    with pytest.raises(KontainerValueError):
        result.unwrap()


@given(arbitrary)
def test_str_done(value: Any):
    maybe = Done(value)
    assert str(maybe) == str(value)


@given(arbitrary)
def test_str_error(value: Any):
    maybe = Error(value)
    assert str(maybe) == str(undefined)


@given(st.one_of(arbitrary, st.none(), st.builds(Exception, arbitrary)))
def test_repr(value: Any):
    format_text = "<{name}: value={value}>"
    maybe = Result(value)
    if isinstance(maybe, Done):
        name = "Done"
    elif isinstance(maybe, Error):
        name = "Error"
    else:
        name = "Result"

    if isinstance(value, Exception):
        value = undefined

    assert repr(maybe) == format_text.format(name=name, value=repr(value))
