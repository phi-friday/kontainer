from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

__all__ = [
    "KontainerError",
    "KontainerWarning",
    "UndefinedError",
    "UndefinedRecreateWarning",
    "KontainerValueError",
    "KontainerTypeError",
]


class KontainerError(Exception): ...


class KontainerWarning(UserWarning): ...


class UndefinedError(KontainerError): ...


class UndefinedRecreateWarning(KontainerWarning): ...


class KontainerValueError(ValueError, KontainerError): ...


class KontainerTypeError(TypeError, KontainerError): ...
