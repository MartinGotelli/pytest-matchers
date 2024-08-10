from pytest_matchers.matchers import And, Eq, IsInstance


def test_create():
    matcher = And(Eq(1), Eq(2), Eq(3))
    assert isinstance(matcher, And)
    matcher = Eq(1) & Eq(2) & Eq(3)
    assert isinstance(matcher, And)


def test_repr():
    matcher = And(Eq(1), IsInstance(int))
    assert repr(matcher) == "To be 1 and of 'int' instance"
    matcher = And(Eq(1))
    assert repr(matcher) == "To be 1"
    matcher = IsInstance(int) & Eq(1)
    assert repr(matcher) == "Of 'int' instance and to be 1"


def test_matches():
    assert 1 == Eq(1) & Eq(1)
    assert 1 != Eq(1) & Eq(2)
    assert 1 != Eq(2) & Eq(1)
    assert Eq(1) & Eq(1) == Eq(1)


def test_matches_exact_value():
    matcher = And(IsInstance(float), 8)
    assert matcher == 8.0
    assert matcher != 8
    assert matcher != 1
    assert matcher != "string"
    assert matcher != ["string"]
