from pytest_matchers.matchers import Eq, IsInstance, Not


def test_create():
    matcher = Not(Eq(1))
    assert isinstance(matcher, Not)
    matcher = ~Eq(1)
    assert isinstance(matcher, Not)
    matcher = Not(6)
    assert isinstance(matcher, Not)


def test_repr():
    matcher = Not(Eq(1))
    assert repr(matcher) == "Not to be 1"
    matcher = ~Eq(1)
    assert repr(matcher) == "Not to be 1"
    matcher = Not(6)
    assert repr(matcher) == "Not to be 6"
    matcher = Not(IsInstance(int))
    assert repr(matcher) == "Not of 'int' instance"
    matcher = Not(Not(IsInstance(int)))
    assert repr(matcher) == repr(IsInstance(int))


def test_invert():
    matcher = ~Not(IsInstance(int))
    assert isinstance(matcher, IsInstance)
    matcher = Not(Not(IsInstance(int)))
    assert isinstance(matcher, IsInstance)
    matcher = Not(Not(1))
    assert isinstance(matcher, Eq)


def test_matches():
    matcher = Not(Eq(1))
    assert 1 != matcher
    assert 2 == matcher
    matcher = ~IsInstance(str)
    assert 1 == matcher
    assert "string" != matcher
