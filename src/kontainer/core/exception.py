from __future__ import annotations

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


class KontainerValueError(KontainerError, ValueError): ...


class KontainerTypeError(KontainerError, TypeError): ...
