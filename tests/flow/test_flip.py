from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kontainer import flip_func


@given(st.integers(), st.integers())
def test_flip_func(x: Any, y: Any):
    func = lambda x, y: (x, y)
    fliped = flip_func(func)

    new = fliped(x, y)
    assert isinstance(new, tuple)
    assert new == (y, x)


def test_flip_arg_require_error():
    func = lambda x,: (x,)
    with pytest.raises(TypeError, match="Too few parameters required by func: 1 < 2"):
        flip_func(func)  # type: ignore


def test_flip_arg_many_error():
    func = lambda x, y, z: (x, y, z)
    with pytest.raises(TypeError, match="Too many parameters required by func: 3 > 2"):
        flip_func(func)  # type: ignore
