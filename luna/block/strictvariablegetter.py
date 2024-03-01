from typing import Optional

from luna.interface import Block
from luna.interpreter import Context


class StrictVariableGetterBlock(Block):

    def will_accept(self, ctx: Context) -> bool:
        return ctx.verb.declaration in ctx.response.variables

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.declaration:
            return ctx.response.variables[ctx.verb.declaration].get_value(ctx.verb)
