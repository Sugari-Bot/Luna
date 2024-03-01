import random
from typing import Optional

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context


class RandomBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("random", "#", "rand")

    def __init__(self) -> None:
        super().__init__(True, payload=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.payload is None:
            return None

        spl = ctx.verb.payload.split("~" if "~" in ctx.verb.payload else ",")
        random.seed(ctx.verb.parameter)

        return random.choice(spl)
