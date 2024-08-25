import pytest

from pytest_matchers.matchers import String


def test_create():
    matcher = String()
    assert isinstance(matcher, String)
    matcher = String(starts_with="a", ends_with="b", contains="c")
    assert isinstance(matcher, String)
    matcher = String(length=1)
    assert isinstance(matcher, String)

    with pytest.raises(
        ValueError,
        match="Cannot specify length with min_length or max_length",
    ):
        String(min_length=1, max_length=4, length=2)


def test_repr():
    matcher = String()
    assert repr(matcher) == "To be a string"
    matcher = String(contains="ab")
    assert repr(matcher) == "To be a string containing something expected equal to 'ab'"
    matcher = String(starts_with="ab")
    assert repr(matcher) == "To be a string with start expected equal to 'ab'"
    matcher = String(ends_with="bc")
    assert repr(matcher) == "To be a string with ending expected equal to 'bc'"
    matcher = String(length=1)
    assert repr(matcher) == "To be a string with length of 1"
    matcher = String(min_length=1, max_length=3)
    assert repr(matcher) == "To be a string with length between 1 and 3"
    matcher = String(
        contains="ab",
        starts_with="ab",
        ends_with="bc",
        min_length=1,
        max_length=8,
    )
    assert (
        repr(matcher) == "To be a string with length between 1 and 8 and "
        "containing something expected equal to 'ab'"
        " and with start expected equal to 'ab' and with ending expected equal to 'bc'"
    )


def test_matches_type():
    matcher = String()
    assert matcher == "string"
    assert matcher != 20
    assert matcher != ["string"]


def test_matches_exact_length():
    matcher = String(length=1)
    assert matcher == "a"
    assert matcher != ""
    assert matcher != "ab"
    assert matcher != "string"


def test_matches_min_and_max_length():
    matcher = String(min_length=1, max_length=3)
    assert matcher == "a"
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher != ""
    assert matcher != "abcd"


def test_matches_contains():
    matcher = String(contains="ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher == "dabc"
    assert matcher != ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20


def test_matches_starts_with():
    matcher = String(starts_with="ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher != "dabc"
    assert matcher != ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20


def test_matches_ends_with():
    matcher = String(ends_with="bc")
    assert matcher == "abc"
    assert matcher == "bc"
    assert matcher != "dabcx"
    assert matcher != ["x", "bc", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20
    assert matcher != ["x", "bc"]
