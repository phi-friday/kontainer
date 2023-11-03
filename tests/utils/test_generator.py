from __future__ import annotations

from typing import Any, Generator

import pytest

from kontainer.utils.generator import create_generator, unwrap_generator


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_create_generator(value: Any):
    generator = create_generator(value)
    assert isinstance(generator, Generator)

    error = None
    next(generator)
    try:
        next(generator)
    except StopIteration as exc:
        error = exc

    assert isinstance(error, StopIteration)
    assert error.value == value


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_uwrap_generator(value: Any):
    generator = create_generator(value)
    assert isinstance(generator, Generator)

    result = unwrap_generator(generator)
    assert result == value
