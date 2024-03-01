from typing import Optional
from urllib.parse import quote, quote_plus

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context


class URLEncodeBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("urlencode",)

    def __init__(self) -> None:
        super().__init__(True, payload=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.payload is None:
            return None

        method = quote_plus if ctx.verb.parameter == "+" else quote
        return method(ctx.verb.payload.encode("utf-8"))
