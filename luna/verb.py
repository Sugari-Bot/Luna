from typing import Optional

__all__ = ("Verb",)


class Verb:
    __slots__ = (
        "declaration",
        "parameter",
        "payload",
        "parsed_string",
        "dec_depth",
        "dec_start",
        "skip_next",
        "parsed_length",
    )

    def __init__(
        self,
        verb_string: Optional[str] = None,
        *,
        limit: int = 2000,
    ) -> None:
        self.declaration: Optional[str] = None
        self.parameter: Optional[str] = None
        self.payload: Optional[str] = None
        if verb_string:
            self.__parse(verb_string, limit)

    def __str__(self) -> str:
        response = "{"
        if self.declaration is not None:
            response += self.declaration
        if self.parameter is not None:
            response += f"({self.parameter})"
        if self.payload is not None:
            response += ":" + self.payload
        return response + "}"

    def __repr__(self) -> str:
        attrs = ("declaration", "parameter", "payload")
        inner = " ".join(f"{attr}={getattr(self, attr)!r}" for attr in attrs)
        return f"<Verb {inner}>"

    def __parse(self, verb_string: str, limit: int) -> None:
        self.parsed_string = verb_string[1:-1][:limit]
        self.parsed_length = len(self.parsed_string)
        self.dec_depth = 0
        self.dec_start = 0
        self.skip_next = False

        for i, v in enumerate(self.parsed_string):
            if self.skip_next:
                self.skip_next = False
                continue
            elif v == "\\":
                self.skip_next = True
                continue

            if v == ":" and not self.dec_depth:
                self.set_payload()
                return
            elif self._parse_paranthesis_parameter(i, v):
                return
        self.set_payload()

    def _parse_paranthesis_parameter(self, i: int, v: str) -> bool:
        if v == "(":
            self.open_parameter(i)
        elif v == ")" and self.dec_depth:
            return self.close_parameter(i)
        return False

    def set_payload(self) -> None:
        res = self.parsed_string.split(":", 1)
        if len(res) == 2:
            self.payload = res[1]
        self.declaration = res[0]

    def open_parameter(self, i: int) -> None:
        self.dec_depth += 1
        if not self.dec_start:
            self.dec_start = i
            self.declaration = self.parsed_string[:i]

    def close_parameter(self, i: int) -> bool:
        self.dec_depth -= 1
        if self.dec_depth == 0:
            self.parameter = self.parsed_string[self.dec_start + 1 : i]
            try:
                if self.parsed_string[i + 1] == ":":
                    self.payload = self.parsed_string[i + 2 :]
            except IndexError:
                pass
            return True
        return False
