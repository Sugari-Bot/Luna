from typing import Optional

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context


class SubstringBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("substr", "substring")

    def __init__(self) -> None:
        super().__init__(True, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter is None or ctx.verb.payload is None:
            return None
        try:
            if "-" not in ctx.verb.parameter:
                return ctx.verb.payload[int(float(ctx.verb.parameter)) :]

            spl = ctx.verb.parameter.split("-")
            start = int(float(spl[0]))
            end = int(float(spl[1]))
            return ctx.verb.payload[start:end]
        except Exception:
            return
