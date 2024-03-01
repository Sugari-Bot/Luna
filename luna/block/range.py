import random
from typing import Optional

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context


class RangeBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("rangef", "range")

    def __init__(self) -> None:
        super().__init__(True, payload=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.payload is None or ctx.verb.declaration is None:
            return None
        try:
            spl = ctx.verb.payload.split("-")
            random.seed(ctx.verb.parameter)
            if ctx.verb.declaration.lower() == "rangef":
                lower = float(spl[0])
                upper = float(spl[1])
                return str(random.randint(int(lower * 10), int(upper * 10)) / 10)
            else:
                lower = int(float(spl[0]))
                upper = int(float(spl[1]))
                return str(random.randint(lower, upper))
        except Exception:
            return None
