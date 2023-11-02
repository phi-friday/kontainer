from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import TypeVar, TypeVarTuple, Unpack

    ValueT1 = TypeVar("ValueT1", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ArgsT = TypeVarTuple("ArgsT")

__all__ = ["identity", "flip", "first", "second", "third", "fourth"]


def identity(value: ValueT1) -> ValueT1:
    return value


def flip(values: tuple[ValueT1, ValueT2]) -> tuple[ValueT2, ValueT1]:
    return (values[1], values[0])


def first(values: tuple[ValueT1, Unpack[tuple[Any, ...]]]) -> ValueT1:
    return values[0]


def second(values: tuple[Any, ValueT1, Unpack[tuple[Any, ...]]]) -> ValueT1:
    return values[1]


def third(values: tuple[Any, Any, ValueT1, Unpack[tuple[Any, ...]]]) -> ValueT1:
    return values[2]


def fourth(values: tuple[Any, Any, Any, ValueT1, Unpack[tuple[Any, ...]]]) -> ValueT1:
    return values[3]
