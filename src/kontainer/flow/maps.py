from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterable, Literal, overload

from kontainer.maybe import Maybe, Option, Result

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    from kontainer.core.types import Container

    ValueT = TypeVar("ValueT", infer_variance=True)
    OtherT = TypeVar("OtherT", infer_variance=True)

__all__ = ["map_elements"]


@overload
def map_elements(
    func: Callable[[ValueT], OtherT], values: Iterable[ValueT], /
) -> Iterable[Maybe[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Maybe[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Maybe[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT], values: Iterable[ValueT], /, *, lazy: bool = ...
) -> Iterable[Maybe[OtherT, Any]] | tuple[Maybe[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Option] = ...,
) -> Iterable[Option[OtherT]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Option] = ...,
    lazy: Literal[False] = ...,
) -> tuple[Option[OtherT], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Option] = ...,
    lazy: Literal[True],
) -> Iterable[Option[OtherT]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Option] = ...,
    lazy: bool = ...,
) -> Iterable[Option[OtherT]] | tuple[Option[OtherT], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Result] = ...,
) -> Iterable[Result[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Result] = ...,
    lazy: Literal[False],
) -> tuple[Result[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Result] = ...,
    lazy: Literal[True],
) -> Iterable[Result[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Result] = ...,
    lazy: bool = ...,
) -> Iterable[Result[OtherT, Any]] | tuple[Result[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Maybe] = ...,
) -> Iterable[Maybe[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Maybe] = ...,
    lazy: Literal[False],
) -> tuple[Maybe[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Maybe] = ...,
    lazy: Literal[True],
) -> Iterable[Maybe[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Maybe] = ...,
    lazy: bool = ...,
) -> Iterable[Maybe[OtherT, Any]] | tuple[Maybe[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Container] = ...,
) -> Iterable[Container[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Container] = ...,
    lazy: Literal[False],
) -> tuple[Container[OtherT, Any], ...]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Container] = ...,
    lazy: Literal[True],
) -> Iterable[Container[OtherT, Any]]: ...


@overload
def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Container] = ...,
    lazy: bool = ...,
) -> Iterable[Container[OtherT, Any]] | tuple[Container[OtherT, Any], ...]: ...


def map_elements(
    func: Callable[[ValueT], OtherT],
    values: Iterable[ValueT],
    /,
    *,
    container_type: type[Container] = Maybe,
    lazy: bool = True,
) -> Iterable[Container[OtherT, Any]] | tuple[Container[OtherT, Any], ...]:
    result = (container_type(x).map_value(func) for x in values)
    if lazy:
        return result
    return tuple(result)
