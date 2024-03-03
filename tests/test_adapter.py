from pytest import fixture

from luna import Interpreter
from luna.adapter import StringAdapter
from luna.block import LooseVariableGetterBlock


@fixture
def interpreter() -> Interpreter:
    blocks = [LooseVariableGetterBlock()]
    return Interpreter(blocks)


def test_string_adapter(interpreter: Interpreter) -> None:
    text = "Hello World, How are you"

    data = {"test": StringAdapter(text)}
    result = interpreter.process("{test}", data).body
    assert result == text

    result = interpreter.process("{test(1)}", data).body
    assert result == "Hello"

    result = interpreter.process("{test(3+)}", data).body
    assert result == "How are you"

    result = interpreter.process("{test(+2)}", data).body
    assert result == "Hello World,"
