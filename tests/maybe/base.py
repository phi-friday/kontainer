from __future__ import annotations

import warnings
from typing import Any, Callable, ClassVar

import pytest

from kontainer.core.const import undefined
from kontainer.core.exception import UndefinedError
from kontainer.core.types import Container

BOLD_RED = "\x1b[31;1m"
RED = "\x1b[31;20m"
RESET = "\x1b[0m"


def _func_as_value_container(
    func: Callable[..., Any], container_type: type[Container]
) -> Callable[..., Container]:
    def inner(*args: Any) -> Container[Any, Any]:
        result = func(*args)
        if isinstance(result, container_type):
            return result
        return container_type(result)

    return inner


def _func_as_other_container(
    func: Callable[..., Any], container_type: type[Container]
) -> Callable[..., Container]:
    def inner(*args: Any) -> Container[Any, Any]:
        result = func(*args)
        if isinstance(result, container_type):
            return result
        return container_type(undefined, result)

    return inner


def _generate_getter(value: Any) -> Callable[[], Any]:
    def inner() -> Any:
        return value

    return inner


class _Const: ...


const = _Const()


class BaseTestContainer:
    container_type: ClassVar[type[Container]]

    def test_container_type(self):
        assert issubclass(self.container_type, Container)

    @pytest.mark.parametrize("value", [1, "b", b"1"])
    def test_construct_without_other(self, value: Any):
        container = self.container_type(value)
        assert isinstance(container, self.container_type)
        assert container._value == value
        assert container._other is undefined

    @pytest.mark.parametrize(
        ("value", "other"), [(1, "b"), ("b", (1,)), (b"1", frozenset())]
    )
    def test_construct_with_other(self, value: Any, other: Any):
        container = self.container_type(value, other)
        assert isinstance(container, self.container_type)
        assert container._value == value
        assert container._other == other

    def test_error_construct_only_undefined_without_other(self):
        with pytest.raises(UndefinedError):
            self.container_type(undefined)

    def test_error_construct_only_undefined_with_other(self):
        with pytest.raises(UndefinedError):
            self.container_type(undefined, undefined)

    @pytest.mark.parametrize("value", [1, "b", b"b", ()])
    def test_eq(self, value: Any):
        left, right = self.container_type(value), self.container_type(value)
        assert left == right

    @pytest.mark.parametrize(
        ("value", "other"), [(1, 2), ("b", "a"), (b"b", b"q"), ((), (1,))]
    )
    def test_ne(self, value: Any, other: Any):
        assert value != other

        left, right = self.container_type(value), self.container_type(other)
        assert left != right

    @pytest.mark.parametrize("value", [1, "b", b"b", ()])
    def test_hash(self, value: Any):
        container = self.container_type(value)
        assert hash(container) == hash(value)

    @pytest.mark.parametrize("value", [1, "b", b"b", ()])
    def test_iter(self, value: Any):
        container = self.container_type(value)
        iter_container = iter(container)

        try:
            while True:
                next(iter_container)
        except StopIteration as exc:
            assert exc.value == value  # noqa: PT017

    @pytest.mark.parametrize("value", [1, "b", b"b", ()])
    @pytest.mark.anyio()
    async def test_await(self, anyio_backend: Any, value: Any):
        if anyio_backend == "trio" or (
            isinstance(anyio_backend, tuple)
            and anyio_backend
            and anyio_backend[0] == "trio"
        ):
            pytest.skip()
        container = self.container_type(value)
        result = await container
        assert result == value

    @pytest.mark.parametrize(
        ("value", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_map_value(self, value: Any, func: Callable[[Any], Any], result: Any):
        container = self.container_type(value)
        new = container.map_value(func)
        assert new._value == result

    @pytest.mark.parametrize(
        ("value", "other", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_map_values(
        self, value: Any, other: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        container = self.container_type(value)
        new = container.map_values(func, other)
        assert new._value == result

    @pytest.mark.parametrize(
        ("other", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_map_other(self, other: Any, func: Callable[[Any], Any], result: Any):
        container = self.container_type(undefined, other)
        new = container.map_other(func)
        assert new._other == result

    @pytest.mark.parametrize(
        ("other", "another", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_map_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        container = self.container_type(undefined, other)
        new = container.map_others(func, another)
        assert new._other == result

    @pytest.mark.parametrize(
        ("value", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_alt_value(self, value: Any, func: Callable[[Any], Any], result: Any):
        container = self.container_type(value)
        new = container.alt_value(func)
        assert new._other == result

    @pytest.mark.parametrize(
        ("value", "other", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_alt_values(
        self, value: Any, other: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        container = self.container_type(value)
        new = container.alt_values(func, other)
        assert new._other == result

    @pytest.mark.parametrize(
        ("other", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_alt_other(self, other: Any, func: Callable[[Any], Any], result: Any):
        container = self.container_type(undefined, other)
        new = container.alt_other(func)
        assert new._value == result

    @pytest.mark.parametrize(
        ("other", "another", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_alt_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        container = self.container_type(undefined, other)
        new = container.alt_others(func, another)
        assert new._value == result

    @pytest.mark.parametrize(
        ("value", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_bind_value(self, value: Any, func: Callable[[Any], Any], result: Any):
        func = _func_as_value_container(func, self.container_type)

        container = self.container_type(value)
        new = container.bind_value(func)
        assert isinstance(new, self.container_type)
        assert new._value == result

    @pytest.mark.parametrize(
        ("value", "other", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_bind_values(
        self, value: Any, other: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        func = _func_as_value_container(func, self.container_type)

        container = self.container_type(value)
        new = container.bind_values(func, other)
        assert isinstance(new, self.container_type)
        assert new._value == result

    @pytest.mark.parametrize(
        ("other", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_bind_other(self, other: Any, func: Callable[[Any], Any], result: Any):
        func = _func_as_other_container(func, self.container_type)

        container = self.container_type(undefined, other)
        new = container.bind_other(func)
        assert isinstance(new, self.container_type)
        assert new._other == result

    @pytest.mark.parametrize(
        ("other", "another", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_bind_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        func = _func_as_other_container(func, self.container_type)

        container = self.container_type(undefined, other)
        new = container.bind_others(func, another)
        assert isinstance(new, self.container_type)
        assert new._other == result

    @pytest.mark.parametrize(
        ("value", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_lash_value(self, value: Any, func: Callable[[Any], Any], result: Any):
        func = _func_as_other_container(func, self.container_type)

        container = self.container_type(value)
        new = container.lash_value(func)
        assert isinstance(new, self.container_type)
        assert new._other == result

    @pytest.mark.parametrize(
        ("value", "other", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_lash_values(
        self, value: Any, other: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        func = _func_as_other_container(func, self.container_type)

        container = self.container_type(value)
        new = container.lash_values(func, other)
        assert isinstance(new, self.container_type)
        assert new._other == result

    @pytest.mark.parametrize(
        ("other", "func", "result"),
        [
            (1, lambda x: x + 1, 2),
            ("text", lambda x: x + "suffix", "textsuffix"),
            (b"text", lambda x: x + b"suffix", b"textsuffix"),
            ((), lambda x: (*x, 123), (123,)),
        ],
    )
    def test_lash_other(self, other: Any, func: Callable[[Any], Any], result: Any):
        func = _func_as_value_container(func, self.container_type)

        container = self.container_type(undefined, other)
        new = container.lash_other(func)
        assert isinstance(new, self.container_type)
        assert new._value == result

    @pytest.mark.parametrize(
        ("other", "another", "func", "result"),
        [
            (1, 2, lambda x, y: x * y, 2),
            ("text", "suffix", lambda x, y: x + y, "textsuffix"),
            (b"text", b"suffix", lambda x, y: x + y, b"textsuffix"),
            ((), (123,), lambda x, y: (*x, *y), (123,)),
        ],
    )
    def test_lash_others(
        self, other: Any, another: Any, func: Callable[[Any, Any], Any], result: Any
    ):
        func = _func_as_value_container(func, self.container_type)

        container = self.container_type(undefined, other)
        new = container.lash_others(func, another)
        assert isinstance(new, self.container_type)
        assert new._value == result

    @pytest.mark.parametrize(("value", "other"), [(1, 2), (1, "b"), (b"b", 11)])
    def test_switch(self, value: Any, other: Any):
        container = self.container_type(value, other)
        new = container.switch()
        assert isinstance(new, self.container_type)
        assert container._value == new._other
        assert container._other == new._value

    @pytest.mark.parametrize("value", list(range(10)))
    def test_default(self, value: Any):
        container = self.container_type(undefined, Exception())
        default = container.default(value)
        assert default == value

    @pytest.mark.parametrize("value", list(range(10)))
    def test_non_default(self, value: Any):
        result = const
        container = self.container_type(result)
        default = container.default(value)
        assert default != value
        assert default == result

    @pytest.mark.parametrize("func", [_generate_getter(x) for x in range(10)])
    def test_map_default(self, func: Callable[[], Any]):
        container = self.container_type(undefined, Exception())
        result = func()
        default = container.map_default(func)
        assert default == result

    @pytest.mark.parametrize("func", [_generate_getter(x) for x in range(10)])
    def test_map_non_default(self, func: Callable[[], Any]):
        value = func()
        result = const
        container = self.container_type(result)
        default = container.map_default(func)
        assert default != value
        assert default == result

    def test_warn(self):
        for key in dir(self):
            if not key.startswith("test_"):
                continue

            method = getattr(self, key)
            marks: list[pytest.Mark] | None = getattr(method, "pytestmark", None)

            if not marks:
                continue

            for mark in marks:
                if mark.name != "skip":
                    continue
                break
            else:
                continue

            warnings.warn(
                f"\n[{BOLD_RED}{self.container_type.__name__}{RESET}] The test method "
                f"{RED}{key!r}{RESET} was skipped because it was undefined.",
                stacklevel=1,
            )
