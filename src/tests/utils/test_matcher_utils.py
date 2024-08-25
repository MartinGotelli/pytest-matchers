from pytest_matchers.matchers import (
    Anything,
    Eq,
)
from pytest_matchers.utils.matcher_utils import (
    as_matcher,
    matches_or_none,
    partial_matches_or_none,
)


def test_as_matcher():
    matcher = as_matcher(1)
    assert isinstance(matcher, Eq)
    assert matcher == 1
    matcher = as_matcher("string")
    assert isinstance(matcher, Eq)
    assert matcher == "string"
    matcher = as_matcher(Eq(1))
    assert isinstance(matcher, Eq)
    assert matcher == 1
    matcher = as_matcher(Anything())
    assert isinstance(matcher, Anything)
    assert matcher == "something"


def test_matches_or_none():
    assert matches_or_none(None, 1)
    assert matches_or_none(Eq(1), 1)
    assert not matches_or_none(Eq(1), 2)


def test_partial_matches_or_none():
    matcher = Eq(1)
    partial_matcher = partial_matches_or_none(matcher)
    assert partial_matcher(1)
    assert not partial_matcher(2)
    matcher = None
    partial_matcher = partial_matches_or_none(matcher)
    assert partial_matcher(1)
    assert partial_matcher(2)
