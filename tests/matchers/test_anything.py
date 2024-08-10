from src.matchers.anything import Anything


def test_create():
    matcher = Anything()
    assert isinstance(matcher, Anything)


def test_repr():
    matcher = Anything()
    assert repr(matcher) == "To be anything"


def test_matches():
    matcher = Anything()
    assert matcher == 1
    assert matcher == "string"
    assert matcher == ["string"]
    assert matcher == {"key": "value"}
    assert matcher == object
    assert matcher == len
