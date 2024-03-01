from datetime import datetime, timezone
from typing import Optional

from luna.interface import Block
from luna.interpreter import Context


class StrfBlock(Block):
    ACCEPTED_NAMES = ("strf", "unix")

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.declaration is None:
            return None

        if ctx.verb.declaration.lower() == "unix":
            return str(int(datetime.now(timezone.utc).timestamp()))
        if not ctx.verb.payload:
            return None
        if ctx.verb.parameter:
            if ctx.verb.parameter.isdigit():
                try:
                    t = datetime.fromtimestamp(int(ctx.verb.parameter))
                except Exception:
                    return None
            else:
                try:
                    t = datetime.fromisoformat(ctx.verb.parameter)
                except ValueError:
                    return None
        else:
            t = datetime.now()
        if not t.tzinfo:
            t = t.replace(tzinfo=timezone.utc)
        return t.strftime(ctx.verb.payload)
