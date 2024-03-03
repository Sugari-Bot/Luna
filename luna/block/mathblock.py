from typing import Optional

import expr

from luna.interface import Block
from luna.interpreter import Context


class MathBlock(Block):
    ACCEPTED_NAMES = ("math", "m", "+", "calc")

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.payload is None:
            return None
        try:
            return str(expr.evaluate(ctx.verb.payload.strip(" "), max_safe_number=9e99))
        except expr.ParsingError:
            return None
