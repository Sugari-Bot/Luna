import re
from typing import TypeVar

T = TypeVar("T")


pattern = re.compile(r"(?<!\\)([{():|}])")


def _sub_match(match: re.Match) -> str:
    return "\\" + match[1]


def escape_content(string: str) -> str:
    return pattern.sub(_sub_match, string)
