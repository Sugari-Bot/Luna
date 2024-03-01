from typing import Optional

from luna.interface import VerbRequiredBlock
from luna.interpreter import Context

from .helpers import helper_split, parse_if, parse_list_if


def parse_into_output(payload: str, result: bool) -> Optional[str]:
    try:
        output = helper_split(payload, False)
        if output and len(output) == 2:
            if result:
                return output[0]
            else:
                return output[1]
        elif result:
            return payload
        else:
            return ""
    except Exception:
        return


class AnyBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("any", "or")

    def __init__(self) -> None:
        super().__init__(True, payload=True, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter and ctx.verb.payload:
            result = any(parse_list_if(ctx.verb.parameter) or [])
            return parse_into_output(ctx.verb.payload, result)


class AllBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("all", "and")

    def __init__(self) -> None:
        super().__init__(True, payload=True, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter and ctx.verb.payload:
            result = all(parse_list_if(ctx.verb.parameter) or [])
            return parse_into_output(ctx.verb.payload, result)


class IfBlock(VerbRequiredBlock):
    ACCEPTED_NAMES = ("if",)

    def __init__(self) -> None:
        super().__init__(True, payload=True, parameter=True)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter and ctx.verb.payload:
            result = parse_if(ctx.verb.parameter)
            return parse_into_output(ctx.verb.payload, result)
