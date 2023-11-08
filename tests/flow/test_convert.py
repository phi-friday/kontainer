from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer import Maybe, Result, toggle
from kontainer.container.maybe import Null
from kontainer.container.result import Error
from kontainer.core.exception import KontainerTypeError


@given(st.integers())
def test_maybe_to_result(value: Any):
    maybe = Maybe(value)
    result = toggle(maybe)

    assert isinstance(result, Result)
    assert maybe.unwrap() == result.unwrap()


@given(st.integers())
def test_result_to_maybe(value: Any):
    result = Result(value)
    maybe = toggle(result)

    assert isinstance(maybe, Maybe)
    assert maybe.unwrap() == result.unwrap()


def test_error_to_null():
    error = Result(Exception())
    maybe = toggle(error)

    assert isinstance(maybe, Null)


def test_null_to_error():
    null = Maybe(None)
    result = toggle(null)

    assert isinstance(result, Error)


def test_invalid_type_error():
    value: Any = None

    with pytest.raises(KontainerTypeError):
        toggle(value)
