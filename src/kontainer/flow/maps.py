from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterable, Literal, overload

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    from kontainer.core.types import Container
    from kontainer.maybe import Maybe, Option, Result

    ValueT = TypeVar("ValueT", infer_variance=True)
    OtherT = TypeVar("OtherT", infer_variance=True)
    AnotherT = TypeVar("AnotherT", infer_variance=True)

__all__ = ["map_elements", "bind_elements"]


@overload
def map_elements(
    values: Iterable[Option[ValueT]], func: Callable[[ValueT], OtherT], /
) -> Iterable[Option[OtherT]]: ...


@overload
def map_elements(
    values: Iterable[Option[ValueT]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[False] = ...,
) -> tuple[Option[OtherT], ...]: ...


@overload
def map_elements(
    values: Iterable[Option[ValueT]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Option[OtherT]]: ...


@overload
def map_elements(
    values: Iterable[Option[ValueT]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: bool = ...,
) -> Iterable[Option[OtherT]] | tuple[Option[OtherT], ...]: ...


@overload
def map_elements(
    values: Iterable[Result[ValueT, Any]], func: Callable[[ValueT], OtherT], /
) -> Iterable[Result[OtherT, Exception]]: ...


@overload
def map_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Result[OtherT, Exception], ...]: ...


@overload
def map_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Result[OtherT, Exception]]: ...


@overload
def map_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: bool = ...,
) -> Iterable[Result[OtherT, Exception]] | tuple[Result[OtherT, Exception], ...]: ...


@overload
def map_elements(
    values: Iterable[Maybe[ValueT, Any]], func: Callable[[ValueT], OtherT], /
) -> Iterable[Maybe[OtherT, Any | Exception]]: ...


@overload
def map_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Maybe[OtherT, Any | Exception], ...]: ...


@overload
def map_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Maybe[OtherT, Any | Exception]]: ...


@overload
def map_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: bool = ...,
) -> (
    Iterable[Maybe[OtherT, Any | Exception]]
    | tuple[Maybe[OtherT, Any | Exception], ...]
): ...


@overload
def map_elements(
    values: Iterable[Container[ValueT, Any]], func: Callable[[ValueT], OtherT], /
) -> Iterable[Container[OtherT, Any]]: ...


@overload
def map_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Container[OtherT, Any], ...]: ...


@overload
def map_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Container[OtherT, Any]]: ...


@overload
def map_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: bool = ...,
) -> Iterable[Container[OtherT, Any]] | tuple[Container[OtherT, Any], ...]: ...


def map_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], OtherT],
    /,
    *,
    lazy: bool = True,
) -> Iterable[Container[OtherT, Any]] | tuple[Container[OtherT, Any], ...]:
    result = (x.map_value(func) for x in values)
    if lazy:
        return result
    return tuple(result)


@overload
def bind_elements(
    values: Iterable[Option[ValueT]], func: Callable[[ValueT], Option[OtherT]], /
) -> Iterable[Option[OtherT]]: ...


@overload
def bind_elements(
    values: Iterable[Option[ValueT]],
    func: Callable[[ValueT], Option[OtherT]],
    /,
    *,
    lazy: Literal[False] = ...,
) -> tuple[Option[OtherT], ...]: ...


@overload
def bind_elements(
    values: Iterable[Option[ValueT]],
    func: Callable[[ValueT], Option[OtherT]],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Option[OtherT]]: ...


@overload
def bind_elements(
    values: Iterable[Option[ValueT]],
    func: Callable[[ValueT], Option[OtherT]],
    /,
    *,
    lazy: bool = ...,
) -> Iterable[Option[OtherT]] | tuple[Option[OtherT], ...]: ...


@overload
def bind_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], Result[OtherT, Any]],
    /,
) -> Iterable[Result[OtherT, Exception]]: ...


@overload
def bind_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], Result[OtherT, Any]],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Result[OtherT, Exception], ...]: ...


@overload
def bind_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], Result[OtherT, Any]],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Result[OtherT, Exception]]: ...


@overload
def bind_elements(
    values: Iterable[Result[ValueT, Any]],
    func: Callable[[ValueT], Result[OtherT, Any]],
    /,
    *,
    lazy: bool = ...,
) -> Iterable[Result[OtherT, Exception]] | tuple[Result[OtherT, Exception], ...]: ...


@overload
def bind_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], Maybe[OtherT, Any]],
    /,
) -> Iterable[Maybe[OtherT, Any | Exception]]: ...


@overload
def bind_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], Maybe[OtherT, Any]],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Maybe[OtherT, Any | Exception], ...]: ...


@overload
def bind_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], Maybe[OtherT, Any]],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Maybe[OtherT, Any | Exception]]: ...


@overload
def bind_elements(
    values: Iterable[Maybe[ValueT, Any]],
    func: Callable[[ValueT], Maybe[OtherT, Any]],
    /,
    *,
    lazy: bool = ...,
) -> (
    Iterable[Maybe[OtherT, Any | Exception]]
    | tuple[Maybe[OtherT, Any | Exception], ...]
): ...


@overload
def bind_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], Container[OtherT, Any]],
    /,
) -> Iterable[Container[OtherT, Any]]: ...


@overload
def bind_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], Container[OtherT, Any]],
    /,
    *,
    lazy: Literal[False],
) -> tuple[Container[OtherT, Any], ...]: ...


@overload
def bind_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], Container[OtherT, Any]],
    /,
    *,
    lazy: Literal[True],
) -> Iterable[Container[OtherT, Any]]: ...


@overload
def bind_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], Container[OtherT, Any]],
    /,
    *,
    lazy: bool = ...,
) -> Iterable[Container[OtherT, Any]] | tuple[Container[OtherT, Any], ...]: ...


def bind_elements(
    values: Iterable[Container[ValueT, Any]],
    func: Callable[[ValueT], Container[OtherT, Any]],
    /,
    *,
    lazy: bool = True,
) -> Iterable[Container[OtherT, Any]] | tuple[Container[OtherT, Any], ...]:
    result = (x.bind_value(func) for x in values)
    if lazy:
        return result
    return tuple(result)
