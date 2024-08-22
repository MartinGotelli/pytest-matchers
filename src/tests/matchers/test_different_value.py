from pytest_matchers.matchers.different_value import DifferentValue


def test_create():
    matcher = DifferentValue()
    assert isinstance(matcher, DifferentValue)


def test_repr():
    matcher = DifferentValue()
    assert repr(matcher) == "To be a different value"
    matcher = DifferentValue()
    assert matcher == 3
    assert repr(matcher) == "To be different to 3"
    matcher = DifferentValue()
    assert matcher == "string"
    assert repr(matcher) == "To be different to 'string'"


def test_matches():
    matcher = DifferentValue()
    assert matcher == 3
    assert matcher != 3
    assert matcher == 4
    assert matcher == "string"
    matcher = DifferentValue()
    assert matcher == "string"
    assert matcher != "string"
    assert matcher == 3
