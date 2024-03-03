from luna import Verb


def test_basic() -> None:
    parsed = Verb("{hello:world}")
    assert type(parsed) is Verb
    assert parsed.declaration == "hello"
    assert parsed.payload == "world"

    bare = Verb("{user}")
    assert bare.parameter is None
    assert bare.payload is None
    assert bare.declaration == "user"

    bare = Verb("{user(hello)}")
    assert bare.parameter == "hello"
    assert bare.payload is None
    assert bare.declaration == "user"
