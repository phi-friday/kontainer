"""https://github.com/dbrattli/Expression/blob/main/expression/collections/seq.py"""
from __future__ import annotations

import builtins
import functools
import itertools
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, Iterator, overload

if TYPE_CHECKING:
    from typing_extensions import TypeVar, Unpack

    from kontainer import Option
    from kontainer.core.types import Container

    SourceT = TypeVar("SourceT", infer_variance=True)
    ResultT = TypeVar("ResultT", infer_variance=True)
    StateT = TypeVar("StateT", infer_variance=True)
    _T1 = TypeVar("_T1", infer_variance=True)
    _T2 = TypeVar("_T2", infer_variance=True)
    _T3 = TypeVar("_T3", infer_variance=True)
    _T4 = TypeVar("_T4", infer_variance=True)

__all__ = [
    "append",
    "delay",
    "filter",
    "fold",
    "fold_back",
    "head",
    "iter",
    "map",
    "mapi",
    "scan",
    "skip",
    "tail",
    "take",
    "unfold",
    "zip",
]


class SeqGen(Iterable):
    """Sequence from a generator function.

    We use this to allow multiple iterations over the same sequence
    generated by a generator function.
    """

    def __init__(self, gen: Callable[[], Iterable[Any]]) -> None:
        self.gen = gen

    def __iter__(self) -> Iterator[Any]:
        xs = self.gen()
        return builtins.iter(xs)


class Infinite(Iterable):
    """An infinite iterable.

    Where each iterator starts counting at 0.
    """

    def __init__(self, initializer: Callable[[int], Any]) -> None:
        self.initializer = initializer

    def __iter__(self) -> Iterator[Any]:
        return builtins.map(self.initializer, itertools.count(0, 1))


def unwrap(value: Container[SourceT, Any]) -> SourceT:
    return value.unwrap()


def append(
    *others: Iterable[SourceT]
) -> Callable[[Iterable[SourceT]], Iterable[SourceT]]:
    """Append sequence to other sequences.

    Wraps the given enumerations as a single concatenated enumeration.
    """

    def _(source: Iterable[SourceT]) -> Iterable[SourceT]:
        return _concat(source, *others)

    return _


def delay(generator: Callable[[], Iterable[SourceT]]) -> Iterable[SourceT]:
    """Delay sequence.

    Returns a sequence that is built from the given delayed
    specification of a sequence.

    The input function is evaluated each time an Iterator for the
    sequence is requested.

    Args:
        generator: The generating function for the sequence.
    """
    return SeqGen(generator)


def filter(  # noqa: A001
    source: Iterable[SourceT], predicate: Callable[[SourceT], bool]
) -> Iterable[SourceT]:
    """Filter sequence.

    Filters the sequence to a new sequence containing only the
    elements of the sequence for which the given predicate returns
    `True`.

    Args:
        source: (curried) The input sequence to to filter.
        predicate: A function to test whether each item in the
            input sequence should be included in the output.

    Returns:
        A partially applied filter function.
    """
    return builtins.filter(predicate, source)


def fold(
    source: Iterable[SourceT],
    folder: Callable[[StateT, SourceT], StateT],
    state: StateT,
) -> StateT:
    """Fold elements in sequence.

    Applies a function to each element of the collection,
    threading an accumulator argument through the computation. If
    the input function is f and the elements are i0...iN then
    computes f (... (f s i0)...) iN.

    Args:
        source: The input sequence to fold.
        folder: A function that updates the state with each element
            from the sequence.
        state: The initial state.

    Returns:
        Partially applied fold function that takes a source sequence and
        returns the state object after the folding function is applied
        to each element of the sequence.
    """
    return functools.reduce(folder, source, state)


def fold_back(
    source: Iterable[SourceT], folder: Callable[[SourceT, StateT], StateT]
) -> Callable[[StateT], StateT]:
    """Fold elements in sequence backwards.

    Applies a function to each element of the collection,
    starting from the end, threading an accumulator argument through
    the computation. If the input function is f and the elements are
    i0...iN then computes f i0 (... (f iN s)...).

    Args:
        source: The input sequence to fold backwards.
        folder: A function that updates the state with each element
            from the sequence.

    Returns:
        Partially applied fold_back function.
    """

    def _fold_back(state: StateT) -> StateT:
        """Partially applied fold_back function.

        Returns:
            The state object after the folding function is applied
            to each element of the sequence.
        """
        return functools.reduce(
            functools.partial(_star, func=folder), reversed(list(source)), state
        )

    return _fold_back


def head(source: Iterable[SourceT]) -> SourceT:
    """Return the first element of the sequence.

    Args:
        source: The input sequence.

    Returns:
        The first element of the sequence.

    Raises:
        Raises `ValueError` if the source sequence is empty.
    """
    for value in source:
        return value

    raise ValueError("Sequence contains no elements")


@overload
def init_infinite() -> Iterable[int]: ...


@overload
def init_infinite(initializer: Callable[[int], SourceT]) -> Iterable[SourceT]: ...


@overload
def init_infinite(initializer: None) -> Iterable[int]: ...


@overload
def init_infinite(
    initializer: Callable[[int], SourceT] | None
) -> Iterable[SourceT]: ...


def init_infinite(
    initializer: Callable[[int], SourceT] | None = None
) -> Iterable[SourceT]:
    """Generate infinite sequence.

    Generates a new sequence which, when iterated, will return
    successive elements by calling the given function. The results of
    calling the function will not be saved, that is the function will be
    reapplied as necessary to regenerate the elements. The function is
    passed the index of the item being generated.

    Iteration can continue up to `sys.maxsize`.
    """

    if initializer is None:
        return Infinite(_self)
    return Infinite(initializer)


def iter(source: Iterable[SourceT], action: Callable[[SourceT], None]) -> None:  # noqa: A001
    """Applies the given function to each element of the collection.

    Args:
        source: The input sequence to iterate.
        action: A function to apply to each element of the sequence.

    Returns:
        A partially applied iter function.
    """
    for x in source:
        action(x)


def map(  # noqa: A001
    source: Iterable[SourceT], mapper: Callable[[SourceT], ResultT]
) -> Iterable[ResultT]:
    """Map source sequence.

    Builds a new collection whose elements are the results of
    applying the given function to each of the elements of the
    collection.

    Args:
        source: The input sequence to map.
        mapper: A function to transform items from the input sequence.

    Returns:
        Partially applied map function.
    """

    def gen() -> Generator[ResultT, Any, Any]:
        for x in source:
            yield mapper(x)

    return SeqGen(gen)


@overload
def starmap(
    mapper: Callable[[_T1, _T2], ResultT]
) -> Callable[[Iterable[tuple[_T1, _T2]]], Iterable[ResultT]]: ...


@overload
def starmap(
    mapper: Callable[[_T1, _T2, _T3], ResultT]
) -> Callable[[Iterable[tuple[_T1, _T2, _T3]]], Iterable[ResultT]]: ...


@overload
def starmap(
    mapper: Callable[[_T1, _T2, _T3, _T4], ResultT]
) -> Callable[[Iterable[tuple[_T1, _T2, _T3, _T4]]], Iterable[ResultT]]: ...


def starmap(
    mapper: Callable[..., ResultT]
) -> Callable[[Iterable[Any]], Iterable[ResultT]]:
    """Starmap source sequence.

    Unpack arguments grouped as tuple elements. Builds a new collection
    whose elements are the results of applying the given function to the
    unpacked arguments to each of the elements of the collection.

    Args:
        mapper: A function to transform items from the input sequence.

    Returns:
        Partially applied map function.
    """

    return functools.partial(_starmap, func=mapper)


def map2(
    mapper: Callable[[_T1, _T2], ResultT]
) -> Callable[[Iterable[tuple[_T1, _T2]]], Iterable[ResultT]]:
    return starmap(mapper)


def map3(
    mapper: Callable[[_T1, _T2, _T3], ResultT]
) -> Callable[[Iterable[tuple[_T1, _T2, _T3]]], Iterable[ResultT]]:
    return starmap(mapper)


def mapi(
    source: Iterable[SourceT], mapping: Callable[[int, SourceT], ResultT]
) -> Iterable[ResultT]:
    """Map list with index.

    Builds a new collection whose elements are the results of
    applying the given function to each of the elements of the
    collection. The integer index passed to the function indicates
    the index (from 0) of element being transformed.

    Args:
        source: The input sequence to to map.
        mapping: The function to transform elements and their
            indices.

    Returns:
        The list of transformed elements.
    """
    return (*itertools.starmap(mapping, builtins.enumerate(source)),)


def scan(
    source: Iterable[SourceT],
    scanner: Callable[[StateT, SourceT], StateT],
    state: StateT,
) -> Iterable[StateT]:
    """Scan elements in sequence.

    Like fold, but computes on-demand and returns the sequence of
    intermediary and final results.

    Args:
        source: The input sequence.
        scanner: A function that updates the state with each element
        state: The initial state.
    """
    return itertools.accumulate(source, scanner, initial=state)


def skip(source: Iterable[SourceT], count: int) -> Iterable[SourceT]:
    """Skip elements from sequence.

    Returns a sequence that skips N elements of the underlying
    sequence and then yields the remaining elements of the sequence.

    Args:
        source: The input sequence.
        count: The number of items to skip.
    """

    def gen() -> Generator[SourceT, Any, Any]:
        for i, n in enumerate(source):
            if i >= count:
                yield n

    return SeqGen(gen)


def tail(source: Iterable[SourceT]) -> Iterable[SourceT]:
    """Return tail of sequence.

    Returns a sequence that skips 1 element of the underlying sequence
    and then yields the remaining elements of the sequence.
    """
    return skip(source, 1)


def take(source: Iterable[SourceT], count: int) -> Iterable[SourceT]:
    """Returns the first N elements of the sequence.

    Args:
        source: The source sequence.
        count: The number of items to take.

    Returns:
        The result sequence.
    """

    def gen() -> Generator[SourceT, Any, Any]:
        for i, n in enumerate(source):
            yield n

            if i == count - 1:
                break

    if count > 0:
        return SeqGen(gen)
    return ()


def unfold(
    state: StateT, generator: Callable[[StateT], Option[tuple[SourceT, StateT]]]
) -> Iterable[SourceT]:
    """Unfold sequence.

    Generates a list that contains the elements generated by the given
    computation. The given initial state argument is passed to the
    element generator.

    Args:
        state: The initial state.
        generator: A function that takes in the current state and
            returns an option tuple of the next element of the list
            and the next state value.

    Returns:
        A partially applied unfold function that takes the state and
        returns the result list.
    """
    while True:
        result = generator(state)
        value = result.unwrap()
        if value is None:
            break

        item, state = value
        yield item


def zip(  # noqa: A001
    source1: Iterable[SourceT]
) -> Callable[[Iterable[ResultT]], Iterable[tuple[SourceT, ResultT]]]:
    """Zip sequence with other.

    Combines the two sequences into a list of pairs. The two
    sequences need not have equal lengths: when one sequence is
    exhausted any remaining elements in the other sequence are
    ignored.

    Args:
        source1: The first input sequence.

    Returns:
        Partially applied zip function.
    """

    def _zip(source2: Iterable[ResultT]) -> Iterable[tuple[SourceT, ResultT]]:
        """Curried function.

        Combines the two sequences into a list of pairs. The two
        sequences need not have equal lengths: when one sequence is
        exhausted any remaining elements in the other sequence are
        ignored.

        Args:
            source2: The second input sequence.

        Returns:
            The result sequence.
        """
        return builtins.zip(source1, source2)

    return _zip


def _star(x: Any, y: Any, func: Callable[[Any, Any], Any]) -> Any:
    return func(x, y)


def _starmap(
    args: Iterable[tuple[Any, ...]], func: Callable[[Unpack[tuple[Any, ...]]], Any]
) -> Iterable[Any]:
    for arg in args:
        yield func(*arg)


def _concat(*iterables: Iterable[SourceT]) -> Iterable[SourceT]:
    def gen() -> Iterator[SourceT]:
        for it in iterables:
            yield from it

    return SeqGen(gen)


def _self(x: SourceT) -> SourceT:
    return x
