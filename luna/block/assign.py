from typing import Optional

from luna.adapter.string import StringAdapter
from luna.interface.block import VerbRequiredBlock
from luna.interpreter import Context


class AssignmentBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("=", "assign", "let", "var")

    def __init__(self) -> None:
        super().__init__(False, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter is None:
            return None
        ctx.response.variables[ctx.verb.parameter] = StringAdapter(
            str(ctx.verb.payload)
        )
        return ""
