from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from luna.interpreter import Context


__all__ = ("Block", "VerbRequiredBlock")


class Block:
    ACCEPTED_NAMES = ()

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} at {hex(id(self))}>"

    @classmethod
    def will_accept(cls, ctx: Context) -> bool:
        if ctx.verb.declaration is None:
            return False
        dec = ctx.verb.declaration.lower()
        return dec in cls.ACCEPTED_NAMES

    def pre_process(self, _ctx: Context) -> None:
        pass

    def process(self, ctx: Context) -> Optional[str]:
        raise NotImplementedError

    def post_process(self, _ctx: Context) -> None:
        pass


class VerbRequiredBlock(Block):
    def __init__(
        self,
        implicit: bool = False,
        *,
        parameter: bool = False,
        payload: bool = False,
    ) -> None:
        self.implicit = implicit
        self.parameter = parameter
        self.payload = payload
        self.check = (lambda x: x) if implicit else (lambda x: x is not None)

    def will_accept(self, ctx: Context) -> bool:
        verb = ctx.verb
        if self.payload and not self.check(verb.payload):
            return False
        if self.parameter and not self.check(verb.parameter):
            return False
        return super().will_accept(ctx)
