from __future__ import annotations

import pickle
import sys
import traceback
from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from kontainer.core.exception import NestedError, RemoteError


def _build_error(error_type: type[Exception], *args: Any) -> Exception:
    return error_type(*args)


def _build_remote(error: Exception) -> tuple[RemoteError, tuple[Any, ...]]:
    remote = None
    info = None
    try:
        raise error
    except:  # noqa: E722
        info = sys.exc_info()
        remote = RemoteError(*info)

    if remote is None:
        raise ValueError("remote is None")

    return remote, info


def _build_nested(error: Exception) -> Exception:
    nested = None
    try:
        raise error
    except:  # noqa: E722
        nested = NestedError.catch()

    if nested is None:
        raise ValueError("nested is None")

    return nested


errors = st.builds(
    _build_error,
    st.one_of(st.just(ValueError), st.just(TypeError), st.just(NotImplementedError)),
    st.lists(
        st.one_of(st.integers(), st.text(), st.binary(), st.tuples(st.integers())),
        min_size=1,
        max_size=3,
    ),
)


@given(errors)
def test_construct_remote_error(error: Exception):
    remote, info = _build_remote(error)

    as_text = "".join(traceback.format_exception(*info))
    as_text = f'\n"""\n{as_text}"""'
    assert str(remote) == as_text


@given(errors)
def test_serialize_remote_error(error: Exception):
    remote, _ = _build_remote(error)
    assert isinstance(remote, RemoteError)
    dumps = pickle.dumps(remote)
    pickle.loads(dumps)  # noqa: S301


@given(errors)
def test_construct_nested_error(error: Exception):
    remote, _ = _build_remote(error)
    nested = NestedError(remote=remote)
    assert nested._remote is remote
    assert nested._remote_args == ()
    assert nested._remote_type is RemoteError
    assert nested.__cause__ is remote


@given(errors)
def test_catch_nested_error(error: Exception):
    nested = None
    try:
        raise error
    except:  # noqa: E722
        nested = NestedError.catch()

    if nested is None:
        raise ValueError("nested is None")

    assert isinstance(nested, type(error))
    assert nested.args == error.args
    assert nested.__cause__ is error


@given(errors)
def test_serialize_nested_error(error: Exception):
    nested = _build_nested(error)
    assert isinstance(nested, NestedError)

    dumps = pickle.dumps(nested)
    pickle.loads(dumps)  # noqa: S301


def test_unserialiable_nested_error():
    def _local_error() -> Exception:
        class LocalError(Exception): ...

        return LocalError(1)

    error = _local_error()
    nested = None
    try:
        raise error
    except:  # noqa: E722
        nested = NestedError.catch()

    if nested is None:
        raise ValueError("nested is None")

    assert isinstance(nested, type(error))
    assert nested.args == error.args
    assert nested.__cause__ is error

    dumps = pickle.dumps(nested)
    loads = pickle.loads(dumps)  # noqa: S301

    assert isinstance(loads, NestedError)
    assert isinstance(loads.__cause__, RemoteError)
    assert loads.args == error.args
