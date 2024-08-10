from pytest_matchers.matchers import Eq


def test_create():
    matcher = Eq(1)
    assert isinstance(matcher, Eq)


def test_matches():
    """What do you want to understand? It's completely unnecessary this matcher"""
    assert 1 == Eq(1)
    assert 1 != Eq(2)
    assert Eq(1) == 1


def test_repr():
    assert repr(Eq(1)) == "To be 1"
    assert repr(Eq("string")) == "To be 'string'"
