from __future__ import annotations

import re
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer.container.result import Done, Error, Result
from kontainer.decorator import catch

arbitrary = st.one_of(
    st.integers(), st.text(), st.binary(), st.tuples(st.integers()), st.none()
)


class UserError(Exception): ...


@given(arbitrary)
def test_wrap_func(value: Any):
    @catch
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Done)
    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
def test_wrap_generator(value: Any):
    @catch
    def f() -> Any:
        for _ in range(10):
            yield
        return value

    maybe = f()
    assert isinstance(maybe, Done)

    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
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
    assert isinstance(maybe, Done)

    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
def test_wrap_error(value: Any):
    @catch
    def f() -> Any:
        raise Exception(str(value))  # noqa: TRY002

    maybe = f()
    assert isinstance(maybe, Error)

    with pytest.raises(Exception, match=re.escape(str(value))):
        maybe.unwrap()

    with pytest.raises(Exception, match=re.escape(str(value))):
        maybe.unwrap_error()


@given(arbitrary)
def test_wrap_nested(value: Any):
    @catch
    def f() -> Any:
        return Result(value)

    maybe = f()
    assert isinstance(maybe, Done)
    result = maybe.unwrap()
    assert result == value


@given(arbitrary)
def test_wrap_default(value: Any):
    @catch()
    def f() -> Any:
        raise ValueError(str(value))

    maybe = f()
    assert isinstance(maybe, Error)
    with pytest.raises(ValueError, match=re.escape(str(value))):
        maybe.unwrap_error()


@given(st.one_of(st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)))
def test_wrap_error_type_success(error_type: type[Exception]):
    @catch(error_type=error_type)
    def f() -> Any:
        raise error_type

    maybe = f()
    assert isinstance(maybe, Error)
    with pytest.raises(error_type):
        maybe.unwrap_error()


@given(st.one_of(st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)))
def test_wrap_error_type_failed(error_type: type[Exception]):
    @catch(error_type=error_type)
    def f() -> Any:
        raise UserError

    with pytest.raises(UserError):
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
    assert isinstance(left, Error)
    assert isinstance(right, Error)

    with pytest.raises(error_types[0], match=f"{value}"):
        left.unwrap_error()

    with pytest.raises(error_types[1], match=f"{value}"):
        right.unwrap_error()


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
        raise UserError

    for error in error_types:
        f = catch(error_type=error)(f)

    with pytest.raises(UserError):
        f()
