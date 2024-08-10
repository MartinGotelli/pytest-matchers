from pytest_matchers.matchers import IsInstance


def test_create():
    matcher = IsInstance(str)
    assert isinstance(matcher, IsInstance)


def test_repr():
    matcher = IsInstance(str)
    assert repr(matcher) == "To be instance of 'str'"
    matcher = IsInstance(object)
    assert repr(matcher) == "To be instance of 'object'"


def test_concatenated_repr():
    matcher = IsInstance(str)
    assert matcher.concatenated_repr() == "of 'str' instance"
    matcher = IsInstance(object)
    assert matcher.concatenated_repr() == "of 'object' instance"


def test_matches():
    assert "string" == IsInstance(str)
    assert IsInstance(str) == "string"
    assert "string" == IsInstance(object)
    assert "string" != IsInstance(int)
    assert 3 == IsInstance(int)
    assert 3 != IsInstance(str)
    assert "string" != IsInstance(int)
