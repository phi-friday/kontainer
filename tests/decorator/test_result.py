from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer.decorator import catch
from kontainer.maybe import Result


class Error(Exception): ...


@given(st.integers())
def test_wrap_func(value: Any):
    @catch
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Result)
    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_generator(value: Any):
    @catch
    def f() -> Any:
        for _ in range(10):
            yield
        return value

    maybe = f()
    assert isinstance(maybe, Result)

    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_yield_from(value: Any):
    maybe_list = [Result(x) for x in range(10)]

    @catch
    def f() -> Any:
        for x in maybe_list:
            y = yield from x
            assert isinstance(y, int)
            assert y == x.unwrap()
        return value

    maybe = f()
    assert isinstance(maybe, Result)

    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_error(value: Any):
    @catch
    def f() -> Any:
        raise Exception(value)  # noqa: TRY002

    maybe = f()
    assert isinstance(maybe, Result)

    with pytest.raises(ValueError, match="does not have a value."):
        maybe.unwrap()

    with pytest.raises(Exception, match=f"{value}"):
        maybe.unwrap_other()


@given(st.integers())
def test_wrap_nested(value: Any):
    @catch
    def f() -> Any:
        return Result(value)

    maybe = f()
    assert isinstance(maybe, Result)
    result = maybe.unwrap()
    assert result == value


@given(st.integers())
def test_wrap_default(value: Any):
    @catch()
    def f() -> Any:
        raise ValueError(value)

    maybe = f()
    assert isinstance(maybe, Result)
    with pytest.raises(ValueError, match=f"{value}"):
        maybe.unwrap_other()


@given(st.one_of(st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)))
def test_wrap_error_type_success(error_type: type[Exception]):
    @catch(error_type=error_type)
    def f() -> Any:
        raise error_type

    maybe = f()
    assert isinstance(maybe, Result)
    with pytest.raises(error_type):
        maybe.unwrap_other()


@given(st.one_of(st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)))
def test_wrap_error_type_failed(error_type: type[Exception]):
    @catch(error_type=error_type)
    def f() -> Any:
        raise Error

    with pytest.raises(Error):
        f()


@given(
    st.lists(
        st.one_of(
            st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)
        ),
        min_size=2,
        max_size=2,
        unique=True,
    ),
    st.integers(),
)
def test_wrap_nested_error_type_success(error_types: list[type[Exception]], value: Any):
    def f() -> Any:
        raise error_types[0](value)

    def g() -> Any:
        raise error_types[1](value)

    for error in error_types:
        f = catch(error_type=error)(f)
    for error in error_types:
        g = catch(error_type=error)(g)

    left, right = f(), g()
    assert isinstance(left, Result)
    assert isinstance(right, Result)

    with pytest.raises(error_types[0], match=f"{value}"):
        left.unwrap_other()

    with pytest.raises(error_types[1], match=f"{value}"):
        right.unwrap_other()


@given(
    st.lists(
        st.one_of(
            st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)
        ),
        min_size=2,
        max_size=2,
        unique=True,
    )
)
def test_wrap_nested_error_type_failed(error_types: list[type[Exception]]):
    def f() -> Any:
        raise Error

    for error in error_types:
        f = catch(error_type=error)(f)

    with pytest.raises(Error):
        f()
