from __future__ import annotations

from discord.ext.commands import Cooldown

from .interpreter import Interpreter, Response

__all__ = (
    "LunaError",
    "WorkloadExceededError",
    "ProcessError",
    "EmbedParseError",
    "BadColourArgumentError",
    "StopError",
    "CooldownExceededError",
)


class LunaError(Exception):
    pass


class WorkloadExceededError(LunaError):
    pass


class ProcessError(LunaError):
    def __init__(
        self, error: Exception, response: Response, interpreter: Interpreter
    ) -> None:
        self.original: Exception = error
        self.response: Response = response
        self.interpreter: Interpreter = interpreter
        super().__init__(error)


class EmbedParseError(LunaError):
    pass


class BadColourArgumentError(EmbedParseError):
    def __init__(self, argument: str) -> None:
        self.argument = argument
        super().__init__(f'Colour "{argument}" is invalid.')


class StopError(LunaError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class CooldownExceededError(StopError):
    def __init__(
        self, message: str, cooldown: Cooldown, key: str, retry_after: float
    ) -> None:
        self.cooldown = cooldown
        self.key = key
        self.retry_after = retry_after
        super().__init__(message)
