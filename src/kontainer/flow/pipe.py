from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, overload

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    from kontainer.core.types import Container
    from kontainer.maybe import Maybe, Option, Result

    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT0 = TypeVar("ValueT0", infer_variance=True)
    ValueT1 = TypeVar("ValueT1", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ValueT3 = TypeVar("ValueT3", infer_variance=True)
    ValueT4 = TypeVar("ValueT4", infer_variance=True)
    ValueT5 = TypeVar("ValueT5", infer_variance=True)
    ValueT6 = TypeVar("ValueT6", infer_variance=True)
    ValueT7 = TypeVar("ValueT7", infer_variance=True)
    ValueT8 = TypeVar("ValueT8", infer_variance=True)
    ValueT9 = TypeVar("ValueT9", infer_variance=True)
    ValueT10 = TypeVar("ValueT10", infer_variance=True)

__all__ = ["pipe_map", "pipe_bind"]


@overload
def pipe_map(container: Option[ValueT], /) -> Option[ValueT]: ...


@overload
def pipe_map(
    container: Option[ValueT], func0: Callable[[ValueT], ValueT0], /
) -> Option[ValueT0]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    /,
) -> Option[ValueT1]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    /,
) -> Option[ValueT2]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    /,
) -> Option[ValueT3]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    /,
) -> Option[ValueT4]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    /,
) -> Option[ValueT5]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    /,
) -> Option[ValueT6]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    /,
) -> Option[ValueT7]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    /,
) -> Option[ValueT8]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    /,
) -> Option[ValueT9]: ...


@overload
def pipe_map(
    container: Option[ValueT],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    func10: Callable[[ValueT9], ValueT10],
    /,
) -> Option[ValueT10]: ...


@overload
def pipe_map(container: Result[ValueT, Any], /) -> Result[ValueT, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any], func0: Callable[[ValueT], ValueT0], /
) -> Result[ValueT0, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    /,
) -> Result[ValueT1, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    /,
) -> Result[ValueT2, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    /,
) -> Result[ValueT3, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    /,
) -> Result[ValueT4, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    /,
) -> Result[ValueT5, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    /,
) -> Result[ValueT6, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    /,
) -> Result[ValueT7, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    /,
) -> Result[ValueT8, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    /,
) -> Result[ValueT9, Any]: ...


@overload
def pipe_map(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    func10: Callable[[ValueT9], ValueT10],
    /,
) -> Result[ValueT10, Any]: ...


@overload
def pipe_map(container: Maybe[ValueT, Any], /) -> Maybe[ValueT, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any], func0: Callable[[ValueT], ValueT0], /
) -> Maybe[ValueT0, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    /,
) -> Maybe[ValueT1, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    /,
) -> Maybe[ValueT2, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    /,
) -> Maybe[ValueT3, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    /,
) -> Maybe[ValueT4, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    /,
) -> Maybe[ValueT5, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    /,
) -> Maybe[ValueT6, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    /,
) -> Maybe[ValueT7, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    /,
) -> Maybe[ValueT8, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    /,
) -> Maybe[ValueT9, Any]: ...


@overload
def pipe_map(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    func10: Callable[[ValueT9], ValueT10],
    /,
) -> Maybe[ValueT10, Any]: ...


@overload
def pipe_map(container: Container[ValueT, Any], /) -> Container[ValueT, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any], func0: Callable[[ValueT], ValueT0], /
) -> Container[ValueT0, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    /,
) -> Container[ValueT1, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    /,
) -> Container[ValueT2, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    /,
) -> Container[ValueT3, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    /,
) -> Container[ValueT4, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    /,
) -> Container[ValueT5, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    /,
) -> Container[ValueT6, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    /,
) -> Container[ValueT7, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    /,
) -> Container[ValueT8, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    /,
) -> Container[ValueT9, Any]: ...


@overload
def pipe_map(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], ValueT0],
    func1: Callable[[ValueT0], ValueT1],
    func2: Callable[[ValueT1], ValueT2],
    func3: Callable[[ValueT2], ValueT3],
    func4: Callable[[ValueT3], ValueT4],
    func5: Callable[[ValueT4], ValueT5],
    func6: Callable[[ValueT5], ValueT6],
    func7: Callable[[ValueT6], ValueT7],
    func8: Callable[[ValueT7], ValueT8],
    func9: Callable[[ValueT8], ValueT9],
    func10: Callable[[ValueT9], ValueT10],
    /,
) -> Container[ValueT10, Any]: ...


@overload
def pipe_map(
    container: Option[Any], /, *funcs: Callable[[Any], Any]
) -> Option[Any]: ...


@overload
def pipe_map(
    container: Result[Any, Any], /, *funcs: Callable[[Any], Any]
) -> Result[Any, Any]: ...


@overload
def pipe_map(
    container: Maybe[Any, Any], /, *funcs: Callable[[Any], Any]
) -> Maybe[Any, Any]: ...


@overload
def pipe_map(
    container: Container[Any, Any], /, *funcs: Callable[[Any], Any]
) -> Container[Any, Any]: ...


def pipe_map(
    container: Option[ValueT]
    | Result[ValueT, Any]
    | Maybe[ValueT, Any]
    | Container[ValueT, Any],
    /,
    *funcs: Callable[[Any], Any],
) -> Option[Any] | Result[Any, Any] | Maybe[Any, Any] | Container[Any, Any]:
    for func in funcs:
        container = container.map_value(func)
    return container


@overload
def pipe_bind(container: Option[ValueT], /) -> Option[ValueT]: ...


@overload
def pipe_bind(
    container: Option[ValueT], func0: Callable[[ValueT], Option[ValueT0]], /
) -> Option[ValueT0]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    /,
) -> Option[ValueT1]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    /,
) -> Option[ValueT2]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    /,
) -> Option[ValueT3]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    /,
) -> Option[ValueT4]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    func5: Callable[[ValueT4], Option[ValueT5]],
    /,
) -> Option[ValueT5]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    func5: Callable[[ValueT4], Option[ValueT5]],
    func6: Callable[[ValueT5], Option[ValueT6]],
    /,
) -> Option[ValueT6]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    func5: Callable[[ValueT4], Option[ValueT5]],
    func6: Callable[[ValueT5], Option[ValueT6]],
    func7: Callable[[ValueT6], Option[ValueT7]],
    /,
) -> Option[ValueT7]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    func5: Callable[[ValueT4], Option[ValueT5]],
    func6: Callable[[ValueT5], Option[ValueT6]],
    func7: Callable[[ValueT6], Option[ValueT7]],
    func8: Callable[[ValueT7], Option[ValueT8]],
    /,
) -> Option[ValueT8]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    func5: Callable[[ValueT4], Option[ValueT5]],
    func6: Callable[[ValueT5], Option[ValueT6]],
    func7: Callable[[ValueT6], Option[ValueT7]],
    func8: Callable[[ValueT7], Option[ValueT8]],
    func9: Callable[[ValueT8], Option[ValueT9]],
    /,
) -> Option[ValueT9]: ...


@overload
def pipe_bind(
    container: Option[ValueT],
    func0: Callable[[ValueT], Option[ValueT0]],
    func1: Callable[[ValueT0], Option[ValueT1]],
    func2: Callable[[ValueT1], Option[ValueT2]],
    func3: Callable[[ValueT2], Option[ValueT3]],
    func4: Callable[[ValueT3], Option[ValueT4]],
    func5: Callable[[ValueT4], Option[ValueT5]],
    func6: Callable[[ValueT5], Option[ValueT6]],
    func7: Callable[[ValueT6], Option[ValueT7]],
    func8: Callable[[ValueT7], Option[ValueT8]],
    func9: Callable[[ValueT8], Option[ValueT9]],
    func10: Callable[[ValueT9], Option[ValueT10]],
    /,
) -> Option[ValueT10]: ...


@overload
def pipe_bind(container: Result[ValueT, Any], /) -> Result[ValueT, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any], func0: Callable[[ValueT], Result[ValueT0, Any]], /
) -> Result[ValueT0, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    /,
) -> Result[ValueT1, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    /,
) -> Result[ValueT2, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    /,
) -> Result[ValueT3, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    /,
) -> Result[ValueT4, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    func5: Callable[[ValueT4], Result[ValueT5, Any]],
    /,
) -> Result[ValueT5, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    func5: Callable[[ValueT4], Result[ValueT5, Any]],
    func6: Callable[[ValueT5], Result[ValueT6, Any]],
    /,
) -> Result[ValueT6, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    func5: Callable[[ValueT4], Result[ValueT5, Any]],
    func6: Callable[[ValueT5], Result[ValueT6, Any]],
    func7: Callable[[ValueT6], Result[ValueT7, Any]],
    /,
) -> Result[ValueT7, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    func5: Callable[[ValueT4], Result[ValueT5, Any]],
    func6: Callable[[ValueT5], Result[ValueT6, Any]],
    func7: Callable[[ValueT6], Result[ValueT7, Any]],
    func8: Callable[[ValueT7], Result[ValueT8, Any]],
    /,
) -> Result[ValueT8, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    func5: Callable[[ValueT4], Result[ValueT5, Any]],
    func6: Callable[[ValueT5], Result[ValueT6, Any]],
    func7: Callable[[ValueT6], Result[ValueT7, Any]],
    func8: Callable[[ValueT7], Result[ValueT8, Any]],
    func9: Callable[[ValueT8], Result[ValueT9, Any]],
    /,
) -> Result[ValueT9, Any]: ...


@overload
def pipe_bind(
    container: Result[ValueT, Any],
    func0: Callable[[ValueT], Result[ValueT0, Any]],
    func1: Callable[[ValueT0], Result[ValueT1, Any]],
    func2: Callable[[ValueT1], Result[ValueT2, Any]],
    func3: Callable[[ValueT2], Result[ValueT3, Any]],
    func4: Callable[[ValueT3], Result[ValueT4, Any]],
    func5: Callable[[ValueT4], Result[ValueT5, Any]],
    func6: Callable[[ValueT5], Result[ValueT6, Any]],
    func7: Callable[[ValueT6], Result[ValueT7, Any]],
    func8: Callable[[ValueT7], Result[ValueT8, Any]],
    func9: Callable[[ValueT8], Result[ValueT9, Any]],
    func10: Callable[[ValueT9], Result[ValueT10, Any]],
    /,
) -> Result[ValueT10, Any]: ...


@overload
def pipe_bind(container: Maybe[ValueT, Any], /) -> Maybe[ValueT, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any], func0: Callable[[ValueT], Maybe[ValueT0, Any]], /
) -> Maybe[ValueT0, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    /,
) -> Maybe[ValueT1, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    /,
) -> Maybe[ValueT2, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    /,
) -> Maybe[ValueT3, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    /,
) -> Maybe[ValueT4, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    func5: Callable[[ValueT4], Maybe[ValueT5, Any]],
    /,
) -> Maybe[ValueT5, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    func5: Callable[[ValueT4], Maybe[ValueT5, Any]],
    func6: Callable[[ValueT5], Maybe[ValueT6, Any]],
    /,
) -> Maybe[ValueT6, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    func5: Callable[[ValueT4], Maybe[ValueT5, Any]],
    func6: Callable[[ValueT5], Maybe[ValueT6, Any]],
    func7: Callable[[ValueT6], Maybe[ValueT7, Any]],
    /,
) -> Maybe[ValueT7, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    func5: Callable[[ValueT4], Maybe[ValueT5, Any]],
    func6: Callable[[ValueT5], Maybe[ValueT6, Any]],
    func7: Callable[[ValueT6], Maybe[ValueT7, Any]],
    func8: Callable[[ValueT7], Maybe[ValueT8, Any]],
    /,
) -> Maybe[ValueT8, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    func5: Callable[[ValueT4], Maybe[ValueT5, Any]],
    func6: Callable[[ValueT5], Maybe[ValueT6, Any]],
    func7: Callable[[ValueT6], Maybe[ValueT7, Any]],
    func8: Callable[[ValueT7], Maybe[ValueT8, Any]],
    func9: Callable[[ValueT8], Maybe[ValueT9, Any]],
    /,
) -> Maybe[ValueT9, Any]: ...


@overload
def pipe_bind(
    container: Maybe[ValueT, Any],
    func0: Callable[[ValueT], Maybe[ValueT0, Any]],
    func1: Callable[[ValueT0], Maybe[ValueT1, Any]],
    func2: Callable[[ValueT1], Maybe[ValueT2, Any]],
    func3: Callable[[ValueT2], Maybe[ValueT3, Any]],
    func4: Callable[[ValueT3], Maybe[ValueT4, Any]],
    func5: Callable[[ValueT4], Maybe[ValueT5, Any]],
    func6: Callable[[ValueT5], Maybe[ValueT6, Any]],
    func7: Callable[[ValueT6], Maybe[ValueT7, Any]],
    func8: Callable[[ValueT7], Maybe[ValueT8, Any]],
    func9: Callable[[ValueT8], Maybe[ValueT9, Any]],
    func10: Callable[[ValueT9], Maybe[ValueT10, Any]],
    /,
) -> Maybe[ValueT10, Any]: ...


@overload
def pipe_bind(container: Container[ValueT, Any], /) -> Container[ValueT, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    /,
) -> Container[ValueT0, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    /,
) -> Container[ValueT1, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    /,
) -> Container[ValueT2, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    /,
) -> Container[ValueT3, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    /,
) -> Container[ValueT4, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    func5: Callable[[ValueT4], Container[ValueT5, Any]],
    /,
) -> Container[ValueT5, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    func5: Callable[[ValueT4], Container[ValueT5, Any]],
    func6: Callable[[ValueT5], Container[ValueT6, Any]],
    /,
) -> Container[ValueT6, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    func5: Callable[[ValueT4], Container[ValueT5, Any]],
    func6: Callable[[ValueT5], Container[ValueT6, Any]],
    func7: Callable[[ValueT6], Container[ValueT7, Any]],
    /,
) -> Container[ValueT7, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    func5: Callable[[ValueT4], Container[ValueT5, Any]],
    func6: Callable[[ValueT5], Container[ValueT6, Any]],
    func7: Callable[[ValueT6], Container[ValueT7, Any]],
    func8: Callable[[ValueT7], Container[ValueT8, Any]],
    /,
) -> Container[ValueT8, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    func5: Callable[[ValueT4], Container[ValueT5, Any]],
    func6: Callable[[ValueT5], Container[ValueT6, Any]],
    func7: Callable[[ValueT6], Container[ValueT7, Any]],
    func8: Callable[[ValueT7], Container[ValueT8, Any]],
    func9: Callable[[ValueT8], Container[ValueT9, Any]],
    /,
) -> Container[ValueT9, Any]: ...


@overload
def pipe_bind(
    container: Container[ValueT, Any],
    func0: Callable[[ValueT], Container[ValueT0, Any]],
    func1: Callable[[ValueT0], Container[ValueT1, Any]],
    func2: Callable[[ValueT1], Container[ValueT2, Any]],
    func3: Callable[[ValueT2], Container[ValueT3, Any]],
    func4: Callable[[ValueT3], Container[ValueT4, Any]],
    func5: Callable[[ValueT4], Container[ValueT5, Any]],
    func6: Callable[[ValueT5], Container[ValueT6, Any]],
    func7: Callable[[ValueT6], Container[ValueT7, Any]],
    func8: Callable[[ValueT7], Container[ValueT8, Any]],
    func9: Callable[[ValueT8], Container[ValueT9, Any]],
    func10: Callable[[ValueT9], Container[ValueT10, Any]],
    /,
) -> Container[ValueT10, Any]: ...


@overload
def pipe_bind(
    container: Option[Any], /, *funcs: Callable[[Any], Option[Any]]
) -> Option[Any]: ...


@overload
def pipe_bind(
    container: Result[Any, Any], /, *funcs: Callable[[Any], Result[Any, Any]]
) -> Result[Any, Any]: ...


@overload
def pipe_bind(
    container: Maybe[Any, Any], /, *funcs: Callable[[Any], Maybe[Any, Any]]
) -> Maybe[Any, Any]: ...


@overload
def pipe_bind(
    container: Container[Any, Any], /, *funcs: Callable[[Any], Container[Any, Any]]
) -> Container[Any, Any]: ...


def pipe_bind(
    container: Option[ValueT]
    | Result[ValueT, Any]
    | Maybe[ValueT, Any]
    | Container[ValueT, Any],
    /,
    *funcs: Callable[[Any], Any],
) -> Option[Any] | Result[Any, Any] | Maybe[Any, Any] | Container[Any, Any]:
    for func in funcs:
        container = container.bind_value(func)
    return container
