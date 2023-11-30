from __future__ import annotations

import warnings

import pytest

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import UndefinedRecreateWarning


def test_recreate_undefined():
    new = object.__new__(Undefined)
    with pytest.warns(UndefinedRecreateWarning):
        new.__init__()


def test_undefined_eq():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UndefinedRecreateWarning)
        new = object.__new__(Undefined)
        new.__init__()

    assert undefined != new


def test_construct_undefined():
    new = Undefined()
    assert new is undefined


def test_undefined_repr():
    assert repr(undefined) == "undefined"


def test_undefined_str():
    assert str(undefined) == "undefined"
