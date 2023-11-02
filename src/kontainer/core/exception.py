from __future__ import annotations

__all__ = ["UndefinedError", "UndefinedRecreateWarning"]


class UndefinedError(Exception): ...


class UndefinedRecreateWarning(UserWarning): ...
