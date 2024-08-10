from src.matchers import StartsWith


def test_create():
    matcher = StartsWith("a")
    assert isinstance(matcher, StartsWith)
    matcher = StartsWith([1, 2])
    assert isinstance(matcher, StartsWith)


def test_repr():
    matcher = StartsWith("a")
    assert repr(matcher) == "To start with 'a'"
    matcher = StartsWith([1, 2])
    assert repr(matcher) == "To start with [1, 2]"


def test_concatenated_repr():
    matcher = StartsWith("a")
    assert matcher.concatenated_repr() == "starting with 'a'"
    matcher = StartsWith([1, 2])
    assert matcher.concatenated_repr() == "starting with [1, 2]"


def test_matches_string():
    matcher = StartsWith("ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert not matcher == "dabc"
    assert not matcher == ["x", "ab", "y"]
    assert not matcher == "ac"
    assert not matcher == ["abc"]
    assert not matcher == 20
    assert not matcher == ["ab", "x"]


def test_matches_list():
    matcher = StartsWith([1, 3])
    assert matcher == [1, 3, 2]
    assert matcher == [1, 3]
    assert not matcher == [1, 20, 1, 3, 30]
    assert not matcher == [10, 20, 30]
    assert not matcher == "string"
    assert not matcher == 20
