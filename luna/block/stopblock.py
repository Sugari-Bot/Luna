from typing import Optional

from luna.exceptions import StopError
from luna.interface import VerbRequiredBlock
from luna.interpreter import Context

from .helpers import parse_if


class StopBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("stop", "halt", "error")

    def __init__(self) -> None:
        super().__init__(True, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter and parse_if(ctx.verb.parameter):
            raise StopError("" if ctx.verb.payload is None else ctx.verb.payload)
        return ""
