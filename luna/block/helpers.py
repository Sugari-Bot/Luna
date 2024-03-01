import operator
import re
from typing import List, Optional

SPLIT_REGEX = re.compile(r"(?<!\\)\|")
BOOL_LOOKUP = {"true": True, "false": False, "yes": True, "no": False}


def implicit_bool(string: str) -> Optional[bool]:
    return BOOL_LOOKUP.get(string.lower())


def parse_if(string: str) -> bool:
    value = implicit_bool(string)
    if value is not None:
        return value

    operators = {
        "!=": operator.ne,
        "==": operator.eq,
        ">=": operator.ge,
        "<=": operator.le,
        ">": operator.gt,
        "<": operator.lt,
    }

    for op, func in operators.items():
        if op in string:
            lhs, rhs = map(str.strip, string.split(op))
            try:
                return func(float(lhs), float(rhs))
            except ValueError:
                return func(lhs, rhs)

    return False


def helper_split(
    split_string: str,
    easy: bool = True,
    *,
    max_split: Optional[int] = None,
) -> Optional[List[str]]:
    args = (max_split,) if max_split is not None else ()
    if "|" in split_string:
        return SPLIT_REGEX.split(split_string, *args)
    if easy:
        if "~" in split_string:
            return split_string.split("~", *args)
        if "," in split_string:
            return split_string.split(",", *args)
    return


def parse_list_if(string: str) -> List[Optional[bool]]:
    split = helper_split(string, False)
    if split is None:
        return [parse_if(string)]
    return [parse_if(item) for item in split]
