from luna.interface import Adapter
from luna.utils import escape_content
from luna.verb import Verb


class StringAdapter(Adapter):
    __slots__ = ("string", "escape_content")

    def __init__(self, string: str, *, escape_content: bool = False) -> None:
        self.string = string
        self.escape_content = escape_content

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} string={repr(self.string)}>"

    def get_value(self, verb: Verb) -> str:
        return self.return_value(self.handle(verb))

    def handle(self, verb: Verb) -> str:
        if verb.parameter is None:
            return self.string
        try:
            if "+" not in verb.parameter:
                index = int(verb.parameter) - 1
                splitter = " " if verb.payload is None else verb.payload
                return self.string.split(splitter)[index]
            else:
                index = int(verb.parameter.replace("+", "")) - 1
                splitter = " " if verb.payload is None else verb.payload
                if verb.parameter.startswith("+"):
                    return splitter.join(self.string.split(splitter)[: index + 1])
                elif verb.parameter.endswith("+"):
                    return splitter.join(self.string.split(splitter)[index:])
                else:
                    return self.string.split(splitter)[index]
        except Exception:
            return self.string

    def return_value(self, string: str) -> str:
        return escape_content(string) if self.escape_content else string
