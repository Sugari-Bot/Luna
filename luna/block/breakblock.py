from typing import Optional

from luna.interface import Block
from luna.interpreter import Context

from .helpers import parse_if


class BreakBlock(Block):
    ACCEPTED_NAMES = ("break", "shortcircuit", "short")

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter and parse_if(ctx.verb.parameter):
            ctx.response.body = ctx.verb.payload if ctx.verb.payload else ""

        return ""
