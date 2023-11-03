from __future__ import annotations

from typing import Any

import pytest

from kontainer import undefined
from kontainer.decorator import catch
from kontainer.maybe import Result


@pytest.mark.parametrize("value", list(range(5)))
def test_wrap_func(value: Any):
    @catch
    def f() -> Any:
        return value

    maybe = f()
    assert isinstance(maybe, Result)
    result = maybe.default(undefined)
    assert result == value


@pytest.mark.parametrize("value", list(range(5)))
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


@pytest.mark.parametrize("value", list(range(5)))
def test_wrap_yield_from(value: Any):
    maybe_list = [Result(x) for x in range(10)]

    @catch
    def f() -> Any:
        for x in maybe_list:
            y = yield from x
            assert isinstance(y, int)
            assert y == x.default(undefined)
        return value

    maybe = f()
    assert isinstance(maybe, Result)

    result = maybe.unwrap()
    assert result == value


@pytest.mark.parametrize("value", list(range(5)))
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
