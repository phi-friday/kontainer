from __future__ import annotations

import warnings

import pytest

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import UndefinedRecreateWarning


def test_recreate_undefined():
    with pytest.warns(UndefinedRecreateWarning):
        Undefined()


def test_undefined_eq():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UndefinedRecreateWarning)
        new = Undefined()

    assert undefined != new


def test_undefined_repr():
    assert repr(undefined) == "undefined"


def test_undefined_str():
    assert str(undefined) == "undefined"
