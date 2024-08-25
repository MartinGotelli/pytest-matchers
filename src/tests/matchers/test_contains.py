import pytest

from pytest_matchers import is_string, one_of
from pytest_matchers.matchers import Contains
from pytest_matchers.matchers.contains import contains_matcher


def test_create():
    matcher = Contains(20)
    assert isinstance(matcher, Contains)
    with pytest.raises(ValueError, match="At least one value must be provided"):
        Contains()
    matcher = Contains("ab", 10, [])
    assert isinstance(matcher, Contains)


def test_repr():
    matcher = Contains(20)
    assert repr(matcher) == "To contain 20"
    matcher = Contains("ab")
    assert repr(matcher) == "To contain 'ab'"
    matcher = Contains("ab", 10, [])
    assert repr(matcher) == "To contain 'ab', 10, []"


def test_concatenated_repr():
    matcher = Contains(20)
    assert matcher.concatenated_repr() == "containing something expected equal to 20"
    matcher = Contains("ab")
    assert matcher.concatenated_repr() == "containing something expected equal to 'ab'"
    matcher = Contains("ab", 10, [])
    assert (
        matcher.concatenated_repr()
        == "containing something expected equal to 'ab', and something equal to 10, "
        "and something equal to []"
    )
    matcher = Contains(is_string())
    assert matcher.concatenated_repr() == "containing something expected to be a string"


def test_matches_list():
    matcher = Contains(20)
    assert matcher == [10, 20, 30]
    assert matcher != [10, 21]
    assert matcher != "string"
    assert matcher != 20


def test_matches_list_with_matcher():
    matcher = Contains(is_string())
    assert matcher == ["string"]
    assert matcher == ["string", "another"]
    assert matcher == ["string", 20]
    assert matcher != [20]
    assert matcher != 20


def test_matches_string():
    matcher = Contains("ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher == "dabc"
    assert matcher == ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20


def test_matches_string_with_matcher():
    matcher = Contains(one_of("a", "b"))
    assert matcher == "a"
    assert matcher == "b"
    assert matcher == "ab"
    assert matcher == "ba"
    assert matcher == "abc"
    assert matcher == "dabc"
    assert matcher == ["x", "a", "b", "y"]
    assert matcher != "cdf"
    assert matcher != ["x", "c", "d", "f"]
    assert matcher != 20


def test_matches_multiple_values():
    matcher = Contains("a", "b")
    assert matcher == "ab"
    assert matcher == "ba"
    assert matcher == "abc"
    assert matcher == "dabc"
    assert matcher == ["x", "a", "b", "y"]
    assert matcher != "ac"
    matcher = Contains(*[10, 5])
    assert matcher == [10, 5, 30]
    assert matcher == [10, 5]
    assert matcher != [10, 6]


def test_matches_with_compound_matcher():
    matcher = Contains([is_string()])
    assert matcher == [["a"], "b"]
    assert matcher != ["a"]
    assert matcher != [[1], "a"]
    assert matcher != "abc"
    matcher = Contains([is_string(), is_string()])
    assert matcher != [["a"], "b"]
    assert matcher != [["a", 1], "b", "c"]
    assert matcher == ["b", ["a", "x"], "c"]


def test_contains_matcher():
    matcher = contains_matcher("string")
    assert isinstance(matcher, Contains)
    assert matcher == "string"
    matcher = contains_matcher(None)
    assert matcher is None
