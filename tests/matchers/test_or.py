from pytest_matchers.matchers import IsInstance, Or, Eq


def test_create():
    matcher = Or(Eq(1), Eq(2), Eq(3))
    assert isinstance(matcher, Or)
    matcher = Eq(1) | Eq(2) | Eq(3)
    assert isinstance(matcher, Or)


def test_repr():
    matcher = Or(Eq(1), IsInstance(int))
    assert repr(matcher) == "To be 1 or of 'int' instance"
    matcher = Or(Eq(1))
    assert repr(matcher) == "To be 1"
    matcher = IsInstance(int) | Eq(1)
    assert repr(matcher) == "Of 'int' instance or to be 1"


def test_matches():
    assert 1 == Eq(1) | Eq(1)
    assert 1 == Eq(1) | Eq(2)
    assert 1 == Eq(2) | Eq(1)
    assert 1 != Eq(2) | Eq(3)
    assert 1 != Eq(3) | Eq(2)
    assert Eq(1) | Eq(1) == Eq(1)


def test_matches_exact_value():
    matcher = Or(IsInstance(str), 8)
    assert matcher == 8
    assert matcher == 8.0
    assert matcher != 1
    assert matcher == "string"
    assert matcher != ["string"]
