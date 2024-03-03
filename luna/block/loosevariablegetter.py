from typing import Optional

from luna.interface import Block
from luna.interpreter import Context


class LooseVariableGetterBlock(Block):
    def will_accept(self, _ctx: Context) -> bool:
        return True

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.declaration and ctx.verb.declaration in ctx.response.variables:
            return ctx.response.variables[ctx.verb.declaration].get_value(ctx.verb)
        else:
            return None
