import pytest

from pytest_matchers.matchers import IsString


def test_create():
    matcher = IsString()
    assert isinstance(matcher, IsString)
    matcher = IsString(starts_with="a", ends_with="b", contains="c")
    assert isinstance(matcher, IsString)
    matcher = IsString(length=1)
    assert isinstance(matcher, IsString)

    with pytest.raises(
        ValueError,
        match="Cannot specify length with min_length or max_length",
    ):
        IsString(min_length=1, max_length=4, length=2)


def test_repr():
    matcher = IsString()
    assert repr(matcher) == "To be string"
    matcher = IsString(contains="ab")
    assert repr(matcher) == "To be string containing 'ab'"
    matcher = IsString(starts_with="ab")
    assert repr(matcher) == "To be string starting with 'ab'"
    matcher = IsString(ends_with="bc")
    assert repr(matcher) == "To be string ending with 'bc'"
    matcher = IsString(length=1)
    assert repr(matcher) == "To be string with length of 1"
    matcher = IsString(min_length=1, max_length=3)
    assert repr(matcher) == "To be string with length between 1 and 3"
    matcher = IsString(
        contains="ab",
        starts_with="ab",
        ends_with="bc",
        min_length=1,
        max_length=8,
    )
    assert (
        repr(matcher) == "To be string with length between 1 and 8 and containing 'ab'"
        " and starting with 'ab' and ending with 'bc'"
    )


def test_matches_type():
    matcher = IsString()
    assert matcher == "string"
    assert matcher != 20
    assert matcher != ["string"]


def test_matches_exact_length():
    matcher = IsString(length=1)
    assert matcher == "a"
    assert matcher != ""
    assert matcher != "ab"
    assert matcher != "string"


def test_matches_min_and_max_length():
    matcher = IsString(min_length=1, max_length=3)
    assert matcher == "a"
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher != ""
    assert matcher != "abcd"


def test_matches_contains():
    matcher = IsString(contains="ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher == "dabc"
    assert matcher != ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20


def test_matches_starts_with():
    matcher = IsString(starts_with="ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher != "dabc"
    assert matcher != ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20


def test_matches_ends_with():
    matcher = IsString(ends_with="bc")
    assert matcher == "abc"
    assert matcher == "bc"
    assert matcher != "dabcx"
    assert matcher != ["x", "bc", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20
    assert matcher != ["x", "bc"]
