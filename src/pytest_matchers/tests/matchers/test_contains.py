from pytest_matchers.matchers import Contains


def test_create():
    matcher = Contains(20)
    assert isinstance(matcher, Contains)


def test_repr():
    matcher = Contains(20)
    assert repr(matcher) == "To contain 20"
    matcher = Contains("ab")
    assert repr(matcher) == "To contain 'ab'"


def test_concatenated_repr():
    matcher = Contains(20)
    assert matcher.concatenated_repr() == "containing 20"
    matcher = Contains("ab")
    assert matcher.concatenated_repr() == "containing 'ab'"


def test_matches_list():
    matcher = Contains(20)
    assert matcher == [10, 20, 30]
    assert matcher != [10, 21]
    assert matcher != "string"
    assert matcher != 20


def test_matches_string():
    matcher = Contains("ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher == "dabc"
    assert matcher == ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20
