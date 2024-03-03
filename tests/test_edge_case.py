import pytest

from luna import Interpreter
from luna.adapter import StringAdapter
from luna.block import (
    AllBlock,
    AnyBlock,
    AssignmentBlock,
    BreakBlock,
    FiftyFiftyBlock,
    IfBlock,
    LooseVariableGetterBlock,
    MathBlock,
    PythonBlock,
    RandomBlock,
    RangeBlock,
    ReplaceBlock,
    StopBlock,
    StrfBlock,
    SubstringBlock,
)
from luna.exceptions import WorkloadExceededError


@pytest.fixture
def interpreter() -> Interpreter:
    blocks = [
        MathBlock(),
        RandomBlock(),
        RangeBlock(),
        AnyBlock(),
        IfBlock(),
        AllBlock(),
        BreakBlock(),
        StrfBlock(),
        StopBlock(),
        AssignmentBlock(),
        FiftyFiftyBlock(),
        LooseVariableGetterBlock(),
        SubstringBlock(),
        PythonBlock(),
        ReplaceBlock(),
    ]
    return Interpreter(blocks)


def test_recursion(interpreter: Interpreter) -> None:
    script = """{=(recursion):lol}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {=(recursion):{recursion}{recursion}}
        {recursion}
        """
    data = {"target": StringAdapter("Basic Username")}
    with pytest.raises(WorkloadExceededError):
        interpreter.process(script, data, charlimit=2000)
