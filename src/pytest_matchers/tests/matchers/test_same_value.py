from pytest_matchers.matchers.same_value import SameValue


def test_create():
    matcher = SameValue()
    assert isinstance(matcher, SameValue)


def test_repr():
    matcher = SameValue()
    assert repr(matcher) == "To be the same value"
    matcher = SameValue()
    assert matcher == 3
    assert repr(matcher) == "To be the same value as 3"
    matcher = SameValue()
    assert matcher == "string"
    assert repr(matcher) == "To be the same value as 'string'"


def test_matches():
    matcher = SameValue()
    assert matcher == 3
    assert matcher == 3
    assert matcher != 4
    assert matcher != "string"
    matcher = SameValue()
    assert matcher == "string"
    assert matcher == "string"
    assert matcher != 3
