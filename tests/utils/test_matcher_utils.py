from pytest_matchers.matchers import (
    Anything,
    Between,
    Contains,
    EndsWith,
    Eq,
    IsInstance,
    Length,
    StartsWith,
)
from pytest_matchers.utils.matcher_utils import (
    as_matcher,
    between_matcher,
    contains_matcher,
    ends_with_matcher,
    is_instance_matcher,
    length_matcher,
    matches_or_none,
    partial_matches_or_none,
    starts_with_matcher,
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


def test_is_instance_matcher():
    matcher = is_instance_matcher(str)
    assert isinstance(matcher, IsInstance)
    assert matcher == "string"
    matcher = is_instance_matcher(None)
    assert matcher is None


def test_contains_matcher():
    matcher = contains_matcher("string")
    assert isinstance(matcher, Contains)
    assert matcher == "string"
    matcher = contains_matcher(None)
    assert matcher is None


def test_length_matcher():
    matcher = length_matcher(None, 2, 3)
    assert isinstance(matcher, Length)
    assert matcher == "ab"
    matcher = length_matcher(None, None, 3)
    assert isinstance(matcher, Length)
    assert matcher == [1, 2, 3]
    matcher = length_matcher(None, None, None)
    assert matcher is None


def test_starts_with_matcher():
    matcher = starts_with_matcher("string")
    assert isinstance(matcher, StartsWith)
    assert matcher == "string"
    matcher = starts_with_matcher(None)
    assert matcher is None


def test_ends_with_matcher():
    matcher = ends_with_matcher("string")
    assert isinstance(matcher, EndsWith)
    assert matcher == "string"
    matcher = ends_with_matcher(None)
    assert matcher is None


def test_between_matcher():
    matcher = between_matcher(1, 2, None, None, None)
    assert isinstance(matcher, Between)
    assert matcher == 1
    matcher = between_matcher(None, 2, True, None, None)
    assert isinstance(matcher, Between)
    assert matcher == 2
    matcher = between_matcher(1, None, None, False, None)
    assert isinstance(matcher, Between)
    assert matcher == 2
    matcher = between_matcher(None, None, True, None, None)
    assert matcher is None
