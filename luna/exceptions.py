from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter, Response

__all__ = (
    "LunaError",
    "WorkloadExceededError",
    "ProcessError",
    "StopError",
)


class LunaError(Exception):
    pass


class WorkloadExceededError(LunaError):
    pass


class ProcessError(LunaError):
    def __init__(
        self,
        error: Exception,
        response: Response,
        interpreter: Interpreter,
    ) -> None:
        self.original = error
        self.response = response
        self.interpreter = interpreter
        super().__init__(error)


class StopError(LunaError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
