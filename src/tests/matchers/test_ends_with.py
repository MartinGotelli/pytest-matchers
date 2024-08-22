from pytest_matchers.matchers import EndsWith


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
    assert matcher != "dabcx"
    assert matcher != ["x", "bc", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20
    assert matcher != ["x", "bc"]


def test_matches_list():
    matcher = EndsWith([1, 3])
    assert matcher == [2, 1, 3]
    assert matcher == [1, 3]
    assert matcher != [1, 20, 1, 3, 30]
    assert matcher != [10, 20, 30]
    assert matcher != "string"
    assert matcher != 20
