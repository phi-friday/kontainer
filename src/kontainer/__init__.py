from __future__ import annotations

from typing import Any

from kontainer.core.const import undefined
from kontainer.decorator import catch, optional, wrap
from kontainer.flow import (
    bind_elements,
    compose_funcs,
    flip_func,
    flowtools,
    map_elements,
    pipe_bind,
    pipe_map,
)
from kontainer.maybe import Maybe, Option, Result

__all__ = [
    "flowtools",
    "Maybe",
    "Option",
    "Result",
    "wrap",
    "optional",
    "catch",
    "pipe_bind",
    "pipe_map",
    "map_elements",
    "bind_elements",
    "compose_funcs",
    "flip_func",
    "undefined",
    "__version__",
]

__version__: str


def __getattr__(name: str) -> Any:
    from importlib.metadata import version

    if name == "__version__":
        return version("kontainer")

    error_msg = f"The attribute named {name!r} is undefined."
    raise AttributeError(error_msg)
