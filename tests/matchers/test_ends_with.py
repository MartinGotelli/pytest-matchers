from src.matchers import EndsWith


def test_create():
    matcher = EndsWith("a")
    assert isinstance(matcher, EndsWith)
    matcher = EndsWith([1, 2])
    assert isinstance(matcher, EndsWith)


def test_repr():
    matcher = EndsWith("a")
    assert repr(matcher) == "To end with 'a'"
    matcher = EndsWith([1, 2])
    assert repr(matcher) == "To end with [1, 2]"


def test_concatenated_repr():
    matcher = EndsWith("a")
    assert matcher.concatenated_repr() == "ending with 'a'"
    matcher = EndsWith([1, 2])
    assert matcher.concatenated_repr() == "ending with [1, 2]"


def test_matches_string():
    matcher = EndsWith("bc")
    assert matcher == "abc"
    assert matcher == "bc"
    assert not matcher == "dabcx"
    assert not matcher == ["x", "bc", "y"]
    assert not matcher == "ac"
    assert not matcher == ["abc"]
    assert not matcher == 20
    assert not matcher == ["x", "bc"]


def test_matches_list():
    matcher = EndsWith([1, 3])
    assert matcher == [2, 1, 3]
    assert matcher == [1, 3]
    assert not matcher == [1, 20, 1, 3, 30]
    assert not matcher == [10, 20, 30]
    assert not matcher == "string"
    assert not matcher == 20
