import pytest

from pytest_matchers.matchers import Between, Eq
from pytest_matchers.matchers.between import between_matcher


def test_create():
    matcher = Between(1, 2)
    assert isinstance(matcher, Between)
    matcher = Between(1, None, inclusive=False)
    assert isinstance(matcher, Between)
    matcher = Between(1, 2, min_inclusive=False)
    assert isinstance(matcher, Between)
    matcher = Between(1, 2, max_inclusive=False)
    assert isinstance(matcher, Between)
    matcher = Between(1, 1)
    assert isinstance(matcher, Eq)
    with pytest.raises(
        ValueError,
        match="Cannot specify inclusive and min_inclusive or max_inclusive",
    ):
        Between(1, 2, inclusive=True, min_inclusive=True)
    with pytest.raises(
        ValueError,
        match="At least one of min or max must be specified",
    ):
        Between(None, None)


def test_repr():
    matcher = Between(1, 2)
    assert repr(matcher) == "To be between 1 and 2"
    matcher = Between(1, 2, inclusive=False)
    assert repr(matcher) == "To be between 1 and 2 exclusive"
    matcher = Between(1, 2, min_inclusive=False)
    assert repr(matcher) == "To be greater than 1 and lower or equal than 2"
    matcher = Between(1, 2, max_inclusive=False)
    assert repr(matcher) == "To be greater or equal than 1 and lower than 2"
    matcher = Between(1, None)
    assert repr(matcher) == "To be greater or equal than 1"
    matcher = Between(None, 2, max_inclusive=False)
    assert repr(matcher) == "To be lower than 2"
    matcher = Between(1, 1)
    assert repr(matcher) == "To be 1"
    matcher = Between(0, None)
    assert repr(matcher) == "To be greater or equal than 0"
    matcher = Between(None, 0)
    assert repr(matcher) == "To be lower or equal than 0"


def test_concatenated_repr():
    matcher = Between(1, 2)
    assert matcher.concatenated_repr() == "between 1 and 2"
    matcher = Between(1, 2, inclusive=False)
    assert matcher.concatenated_repr() == "between 1 and 2 exclusive"
    matcher = Between(1, 2, min_inclusive=False)
    assert matcher.concatenated_repr() == "greater than 1 and lower or equal than 2"
    matcher = Between(1, 2, max_inclusive=False)
    assert matcher.concatenated_repr() == "greater or equal than 1 and lower than 2"
    matcher = Between(1, None)
    assert matcher.concatenated_repr() == "greater or equal than 1"
    matcher = Between(None, 2, max_inclusive=False)
    assert matcher.concatenated_repr() == "lower than 2"
    matcher = Between(1, 1)
    assert matcher.concatenated_repr() == "equal to 1"
    matcher = Between(0, None)
    assert matcher.concatenated_repr() == "greater or equal than 0"
    matcher = Between(None, 0)
    assert matcher.concatenated_repr() == "lower or equal than 0"


def test_matches_float_inclusive():
    matcher = Between(1, 2)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 2
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_string_inclusive():
    matcher = Between("a", "d")
    assert matcher == "a"
    assert matcher == "c"
    assert matcher == "d"
    assert matcher == "ca"
    assert matcher != "da"
    assert matcher != "z"
    assert matcher != 20
    assert matcher != ["a", "b"]


def test_matches_float_exclusive():
    matcher = Between(1, 2, inclusive=False)
    assert matcher == 1.5
    assert matcher != 1
    assert matcher != 2
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_float_min_exclusive():
    matcher = Between(1, 2, min_inclusive=False)
    assert matcher == 1.5
    assert matcher == 2
    assert matcher != 1
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_float_max_exclusive():
    matcher = Between(1, 2, max_inclusive=False)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher != 2
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_without_min():
    matcher = Between(None, 2)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 2
    assert matcher != 2.1
    assert matcher != "string"


def test_matches_without_max():
    matcher = Between(1, None)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 2
    assert matcher == 30000
    assert matcher != 0
    assert matcher != "string"


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
