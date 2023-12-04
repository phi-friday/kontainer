from __future__ import annotations

from typing import Any, Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.container.base import BaseTestContainer

from kontainer import undefined
from kontainer.container.result import Done, Error, Result
from kontainer.core.exception import KontainerTypeError
from kontainer.utils.generator import unwrap_generator

arbitrary_value = st.one_of(
    st.integers(), st.text(), st.binary(), st.tuples(st.integers())
)
arbitrary_error = st.one_of(
    st.builds(Exception, arbitrary_value),
    st.builds(ValueError, arbitrary_value),
    st.builds(TypeError, arbitrary_value),
    st.builds(IndexError, arbitrary_value),
)
arbitrary = st.one_of(arbitrary_value, arbitrary_error)


class _Const: ...


class TestResult(BaseTestContainer):
    container_type = Result


@given(arbitrary_error)
def test_create_error(error: Any):
    result = Result(error)
    assert isinstance(result, Error)


@given(arbitrary)
def test_unwrap_error(value: Any):
    error = Error(value)
    assert isinstance(error, Error)

    if isinstance(value, Exception):
        with pytest.raises(type(value)):
            error.unwrap()
    else:
        with pytest.raises(
            KontainerTypeError, match="error container does not hold an error"
        ):
            error.unwrap()


@given(arbitrary_error)
def test_unwrap_error_func(value: Any):
    error = Error(value)
    assert isinstance(error, Error)
    with pytest.raises(type(value)):
        error.unwrap_error()


@given(arbitrary_value)
def test_unwrap_error_without_error(value: Any):
    assert not isinstance(value, Exception)
    error = Error(value)
    assert isinstance(error, Error)
    with pytest.raises(
        KontainerTypeError, match="error container does not hold an error"
    ):
        error.unwrap_error()


@given(arbitrary_value)
def test_unwrap_error_done(value: Any):
    done = Done(value)
    assert isinstance(done, Done)
    with pytest.raises(KontainerTypeError, match="Not an error container"):
        done.unwrap_error()


@given(arbitrary_error, arbitrary_value)
def test_unwrap_error_or(value: Any, other: Any):
    error = Error(value)
    assert isinstance(error, Error)
    with pytest.raises(type(value)):
        error.unwrap_error_or(other)


@given(arbitrary_value, arbitrary_value)
def test_unwrap_error_or_without_error(value: Any, other: Any):
    error = Error(value)
    assert isinstance(error, Error)
    result = error.unwrap_error_or(other)
    assert result == other


@given(arbitrary_value, arbitrary_value)
def test_unwrap_error_or_done(value: Any, other: Any):
    done = Done(value)
    assert isinstance(done, Done)
    assert done.unwrap_error_or(other) == other


@given(arbitrary_error, arbitrary_value)
def test_unwrap_error_or_else(value: Any, other: Any):
    error = Error(value)
    func = lambda: other
    assert isinstance(error, Error)
    with pytest.raises(type(value)):
        error.unwrap_error_or_else(func)


@given(arbitrary_value, arbitrary_value)
def test_unwrap_error_or_else_without_error(value: Any, other: Any):
    error = Error(value)
    func = lambda: other
    assert isinstance(error, Error)
    result = error.unwrap_error_or_else(func)
    assert result == other


@given(arbitrary_value, arbitrary_value)
def test_unwrap_error_or_else_done(value: Any, other: Any):
    done = Done(value)
    func = lambda: other
    assert isinstance(done, Done)
    assert done.unwrap_error_or_else(func) == other


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


@given(arbitrary_value, arbitrary_value)
def test_default_done(value: Any, other: Any):
    result = Done(value)
    assert isinstance(result, Done)
    default = result.default(other)
    assert default == value


@given(arbitrary_value, arbitrary_value)
def test_default_error(value: Any, other: Any):
    maybe = Error(value)
    assert isinstance(maybe, Error)
    default = maybe.default(other)
    assert default == other


@given(arbitrary_value, arbitrary_value)
def test_map_default_done(value: Any, other: Any):
    result = Done(value)
    assert isinstance(result, Done)
    func = lambda: other
    default = result.map_default(func)
    assert default == value


@given(arbitrary_value, arbitrary_value)
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
    if isinstance(value, Exception):
        with pytest.raises(type(value)):
            result.unwrap()
    else:
        with pytest.raises(
            KontainerTypeError, match="error container does not hold an error"
        ):
            result.unwrap()


@given(arbitrary, arbitrary, arbitrary)
def test_map_error_values(value: Any, element: Any, other: Any):
    null = Error(value)
    assert isinstance(null, Error)

    func: Callable[[Any, Any], Any] = lambda x, y: other  # noqa: ARG005
    result = null.map_values(element, func)

    assert isinstance(result, Error)
    if isinstance(value, Exception):
        with pytest.raises(type(value)):
            result.unwrap()
    else:
        with pytest.raises(
            KontainerTypeError, match="error container does not hold an error"
        ):
            result.unwrap()


@given(arbitrary, arbitrary)
def test_bind_error_value(value: Any, other: Any):
    null = Error(value)
    assert isinstance(null, Error)

    func: Callable[[Any], Result[Any, Any]] = lambda x: Done(other)  # noqa: ARG005
    result = null.bind_value(func)

    assert isinstance(result, Error)
    if isinstance(value, Exception):
        with pytest.raises(type(value)):
            result.unwrap()
    else:
        with pytest.raises(
            KontainerTypeError, match="error container does not hold an error"
        ):
            result.unwrap()


@given(arbitrary, arbitrary, arbitrary)
def test_bind_error_values(value: Any, element: Any, other: Any):
    null = Error(value)
    assert isinstance(null, Error)

    func: Callable[[Any, Any], Result[Any, Any]] = lambda x, y: Done(other)  # noqa: ARG005
    result = null.bind_values(element, func)

    assert isinstance(result, Error)
    if isinstance(value, Exception):
        with pytest.raises(type(value)):
            result.unwrap()
    else:
        with pytest.raises(
            KontainerTypeError, match="error container does not hold an error"
        ):
            result.unwrap()


@given(arbitrary_value)
def test_str_done(value: Any):
    maybe = Done(value)
    assert str(maybe) == str(value)


@given(arbitrary_value)
def test_str_error(value: Any):
    maybe = Error(value)
    assert str(maybe) == str(undefined)


@given(arbitrary)
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


@given(arbitrary_error)
def test_iter_error(value: Exception):
    def func() -> Any:
        error = Error(value)
        result = yield from error
        return result

    generator = func()
    with pytest.raises(type(value)):
        unwrap_generator(generator)


@given(arbitrary_error)
@pytest.mark.anyio()
async def test_await_error(value: Exception):
    async def func() -> Any:
        error = Error(value)
        return await error

    coroutine = func()
    with pytest.raises(type(value)):
        await coroutine


@given(arbitrary)
def test_positive(value: Any):
    result = Result(value)
    if isinstance(result, Done):
        assert result.is_positive is True
    else:
        assert result.is_positive is False


@given(arbitrary)
def test_negative(value: Any):
    result = Result(value)
    if isinstance(result, Done):
        assert result.is_negative is False
    else:
        assert result.is_negative is True


@given(arbitrary_value)
def test_construct_using_alias_done(value: Any):
    result = Result.done(value)
    assert isinstance(result, Done)
    assert result.unwrap() == value


@given(arbitrary_error)
def test_construct_using_alias_error(value: Any):
    result = Result.error(value)
    assert isinstance(result, Error)
    with pytest.raises(type(value)):
        result.unwrap()


@given(arbitrary_value)
def test_done_check(value: Any):
    result = Result.done(value)
    assert isinstance(result, Done)
    assert result.is_done(result)


@given(arbitrary_error)
def test_error_check(value: Any):
    result = Result.error(value)
    assert isinstance(result, Error)
    assert result.is_error(result)


@given(arbitrary_error)
def test_unwrap_error_or_with(value: Any):
    error = Error(value)
    func = lambda x: repr(x)
    assert isinstance(error, Error)
    assert error.unwrap_error_or_with(func) == repr(value)


@given(arbitrary_value)
def test_unwrap_error_or_with_without_error(value: Any):
    error = Error(value)
    func = lambda x: repr(x)
    assert isinstance(error, Error)
    result = error.unwrap_error_or_with(func)
    assert result == repr(value)


@given(arbitrary_value)
def test_unwrap_error_or_with_done(value: Any):
    done = Done(value)
    func = lambda x: str(x)
    assert isinstance(done, Done)
    with pytest.raises(KontainerTypeError, match="Not an error container"):
        done.unwrap_error_or_with(func)


@given(arbitrary)
def test_ensure_positive(value: Any):
    done = Result.done(value)
    new = done.ensure_positive()
    assert isinstance(new, Done)
    assert done.unwrap() == new.unwrap()


def test_ensure_positive_error():
    error = Result.error(ValueError())
    with pytest.raises(KontainerTypeError):
        error.ensure_positive()


def test_ensure_negative():
    error = Result.error(ValueError())
    new = error.ensure_negative()
    assert isinstance(new, Error)


def test_ensure_negative_error():
    done = Result.done(None)
    with pytest.raises(KontainerTypeError):
        done.ensure_negative()
