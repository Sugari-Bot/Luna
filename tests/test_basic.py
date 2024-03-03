import time
from typing import List

import pytest

from luna import Interpreter
from luna.adapter import StringAdapter
from luna.block import (
    AssignmentBlock,
    BreakBlock,
    FiftyFiftyBlock,
    MathBlock,
    RandomBlock,
    RangeBlock,
    StrfBlock,
    StrictVariableGetterBlock,
)


@pytest.fixture
def interpreter() -> Interpreter:
    blocks = [
        BreakBlock(),
        MathBlock(),
        RandomBlock(),
        RangeBlock(),
        StrfBlock(),
        AssignmentBlock(),
        FiftyFiftyBlock(),
        StrictVariableGetterBlock(),
    ]
    return Interpreter(blocks)


def test_random(interpreter: Interpreter) -> None:
    # Test simple random
    test = "{random:Hello,Goodbye}"
    expect = ["Hello", "Goodbye"]
    assert seen_all(interpreter, test, expect)

    # Test that it wont crash with a false block
    test = "{random:{ahad},one,two}"
    expect = ["{ahad}", "one", "two"]
    assert seen_all(interpreter, test, expect)

    # Test that inner blocks can use , to sep and outer use ~ without tripping
    # Also testing embedded random
    test = "{random:{random:1,2} cakes~No cakes}"
    expect = ["1 cakes", "2 cakes", "No cakes"]
    assert seen_all(interpreter, test, expect)

    # Test random being able to use a var
    test = "{assign(li):1,2,3,4}{random:{li}}"
    expect = ["1", "2", "3", "4"]
    assert seen_all(interpreter, test, expect)


def test_fifty(interpreter: Interpreter) -> None:
    # Test simple 5050
    test = "Hi{5050: :)}"
    expect = ["Hi", "Hi :)"]
    assert seen_all(interpreter, test, expect)

    # Test simple embedded 5050
    test = "Hi{5050: :){5050: :(}}"
    expect = ["Hi", "Hi :)", "Hi :) :("]
    assert seen_all(interpreter, test, expect)


def test_range(interpreter: Interpreter) -> None:
    # Test simple range
    test = "{range:1-2} cows"
    expect = ["1 cows", "2 cows"]
    assert seen_all(interpreter, test, expect)

    # Test simple float range
    test = "{rangef:1.5-2.5} cows"
    result = interpreter.process(test).body
    assert result is not None
    assert "." in result


def test_math(interpreter: Interpreter) -> None:
    test = "{math:100/2}"
    expect = "50"
    assert interpreter.process(test).body == expect

    test = "{math:100**100**100}"  # should 'fail'
    assert interpreter.process(test).body == test


def test_misc(interpreter: Interpreter) -> None:
    # Test using a variable to get a variable
    data = {
        "pointer": StringAdapter("message"),
        "message": StringAdapter("Hello"),
    }
    test = "{{pointer}}"
    assert interpreter.process(test, data).body == "Hello"

    test = r"\{{pointer}\}"
    assert interpreter.process(test, data).body == r"\{message\}"

    test = "{break(10==10):Override.} This is my actual tag!"
    assert interpreter.process(test, data).body == "Override."


def test_cuddled_strf(interpreter: Interpreter) -> None:
    huggle_wuggle = time.strftime("%y%y%y%y")
    assert interpreter.process("{strf:%y%y%y%y}").body == huggle_wuggle


def test_basic_strf(interpreter: Interpreter) -> None:
    year = time.strftime("%Y")
    assert interpreter.process("Hehe, it's {strf:%Y}").body == f"Hehe, it's {year}"


def seen_all(
    interpreter: Interpreter,
    string: str,
    outcomes: List[str],
    tries: int = 100,
) -> bool:
    unique_outcomes = set(outcomes)
    seen_outcomes = set()
    for _ in range(tries):
        outcome = interpreter.process(string).body
        seen_outcomes.add(outcome)

    return unique_outcomes == seen_outcomes
