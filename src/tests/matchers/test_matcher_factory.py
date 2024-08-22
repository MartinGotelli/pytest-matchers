import pytest

from pytest_matchers.matchers import MatcherFactory
from pytest_matchers.matchers.matcher_factory import matcher


class FakeMatcher:
    def test_me(self) -> bool:
        return True

    def __repr__(self):
        return "Fake Matcher"


def test_register():
    MatcherFactory.matchers = {}
    MatcherFactory.register(FakeMatcher)
    assert MatcherFactory.matchers == {"FakeMatcher": FakeMatcher}


def test_get():
    MatcherFactory.matchers = {}
    with pytest.raises(KeyError):
        MatcherFactory.get("FakeMatcher")
    MatcherFactory.register(FakeMatcher)
    assert MatcherFactory.get("FakeMatcher") == FakeMatcher
    assert MatcherFactory.get("FakeMatcher")().test_me() is True
    assert MatcherFactory.get("FakeMatcher").__name__ == "FakeMatcher"
    assert repr(MatcherFactory.get("FakeMatcher")()) == "Fake Matcher"


def test_matcher_decorator():
    MatcherFactory.matchers = {}
    with pytest.raises(KeyError):
        MatcherFactory.get("FakeMatcher2")

    @matcher
    class FakeMatcher2:
        def test_me(self) -> bool:
            return True

        def __repr__(self):
            return "Fake Matcher 2"

    assert MatcherFactory.get("FakeMatcher2") == FakeMatcher2
    assert MatcherFactory.get("FakeMatcher2")().test_me() is True
    assert repr(MatcherFactory.get("FakeMatcher2")()) == "Fake Matcher 2"
