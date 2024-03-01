from typing import Optional

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context


class ReplaceBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("replace",)

    def __init__(self) -> None:
        super().__init__(True, payload=True, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter is None or ctx.verb.payload is None:
            return None

        try:
            before, after = ctx.verb.parameter.split(",", 1)
            return ctx.verb.payload.replace(before, after)
        except ValueError:
            return None


class PythonBlock(VerbRequiredBlock):
    def __init__(self) -> None:
        super().__init__(True, payload=True, parameter=True)

    def will_accept(self, ctx: Context) -> bool:
        if ctx.verb.declaration is None:
            return False
        return ctx.verb.declaration.lower() in {
            "contains",
            "in",
            "index",
        }

    def process(self, ctx: Context) -> Optional[str]:
        if (
            ctx.verb.declaration is None
            or ctx.verb.parameter is None
            or ctx.verb.payload is None
        ):
            return None
        dec = ctx.verb.declaration.lower()
        if dec == "contains":
            return str(bool(ctx.verb.parameter in ctx.verb.payload.split())).lower()
        elif dec == "in":
            return str(bool(ctx.verb.parameter in ctx.verb.payload)).lower()
        else:
            try:
                return str(ctx.verb.payload.strip().split().index(ctx.verb.parameter))
            except ValueError:
                return "-1"
