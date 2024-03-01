import random
from typing import Optional

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context


class FiftyFiftyBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("5050", "50", "?")

    def __init__(self) -> None:
        super().__init__(True, payload=True)

    def process(self, ctx: Context) -> Optional[str]:
        return random.choice(["", ctx.verb.payload])
