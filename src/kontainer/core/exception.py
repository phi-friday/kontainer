from __future__ import annotations

import pickle
import sys
import traceback
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self

__all__ = [
    "KontainerError",
    "KontainerWarning",
    "UndefinedError",
    "UndefinedRecreateWarning",
    "KontainerValueError",
    "KontainerTypeError",
    "RemoteError",
    "NestedError",
]


class KontainerError(Exception): ...


class KontainerWarning(UserWarning): ...


class UndefinedError(KontainerError): ...


class UndefinedRecreateWarning(KontainerWarning): ...


class KontainerValueError(ValueError, KontainerError): ...


class KontainerTypeError(TypeError, KontainerError): ...


class RemoteError(KontainerError):
    def __init__(
        self,
        error_type: type[BaseException] | None,
        error: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        error_as_text = "".join(traceback.format_exception(error_type, error, tb))
        self.error = f'\n"""\n{error_as_text}"""'

    def __str__(self) -> str:
        return self.error

    def __reduce__(self) -> tuple[Any, ...]:
        return _rebuild_remote_error, (self.error,)


class NestedError(KontainerError):
    def __init__(self, *args: object, remote: RemoteError, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._init(remote)

    def _init(self, remote: RemoteError) -> None:
        self._remote = remote
        self._remote_type: type[BaseException] = RemoteError
        self._remote_args: tuple[Any, ...] = ()
        self.__cause__ = remote

    @classmethod
    def create(
        cls,
        error_type: type[BaseException] | None,
        error: BaseException | None,
        tb: TracebackType | None,
    ) -> Self:
        remote = RemoteError(error_type=error_type, error=error, tb=tb)
        args = () if error is None else error.args

        if error_type is None:
            new = cls(*args, remote=remote)
        else:
            new_type = cls.new(error_type)
            new = new_type(*args, remote=remote)

        new.__cause__ = error

        if error_type is None or error is None:
            return new

        try:
            pickle.dumps(error_type)
            pickle.dumps(error.args)
        except:  # noqa: E722
            return new
        else:
            new._remote_type = error_type  # noqa: SLF001
            new._remote_args = error.args  # noqa: SLF001
        return new

    @classmethod
    def catch(cls) -> Exception:
        info = sys.exc_info()
        try:
            return cls.create(*info)
        except:  # noqa: E722
            error = info[1]
            if error is None:
                raise ValueError("there is no error")  # noqa: B904, TRY200
            if not isinstance(error, Exception):
                raise error  # noqa: B904
            return error

    @staticmethod
    def new(error_type: type[BaseException]) -> type[NestedError]:
        class _NestedError(NestedError, error_type):
            def __init__(self, *args: Any, remote: RemoteError, **kwargs: Any) -> None:
                super(error_type, self).__init__(*args, **kwargs)
                NestedError._init(self, remote)

        return _NestedError

    def __reduce__(self) -> tuple[Any, ...]:
        return _rebuild_nested_error, (
            self._remote,
            self._remote_type,
            self._remote_args,
            self.args,
        )


def _rebuild_remote_error(text: str) -> RemoteError:
    new = RemoteError(None, None, None)
    new.error = text
    return new


def _rebuild_nested_error(
    remote: RemoteError,
    error_type: type[BaseException] | None,
    error_args: tuple[Any, ...] | None,
    args: tuple[Any, ...],
) -> NestedError:
    if error_type is None or error_type is RemoteError:
        new = NestedError(*args, remote=remote)
    else:
        new_type = NestedError.new(error_type)
        new = new_type(*args, remote=remote)

    if error_type is None or error_args is None:
        return new

    if error_type is RemoteError:
        new.__cause__ = remote
        return new

    new._remote_type = error_type  # noqa: SLF001
    new._remote_args = error_args  # noqa: SLF001
    cause = error_type(*error_args)
    cause.__cause__ = remote
    new.__cause__ = cause
    return new
