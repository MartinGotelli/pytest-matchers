from pytest_matchers import is_number, is_string, one_of
from pytest_matchers.matchers import EndsWith
from pytest_matchers.matchers.ends_with import ends_with_matcher


def test_create():
    matcher = EndsWith("a")
    assert isinstance(matcher, EndsWith)
    matcher = EndsWith([1, 2])
    assert isinstance(matcher, EndsWith)


def test_repr():
    matcher = EndsWith("a")
    assert repr(matcher) == "To end with 'a'"
    matcher = EndsWith([1, 2])
    assert repr(matcher) == "To end with [1, 2]"


def test_concatenated_repr():
    matcher = EndsWith("a")
    assert matcher.concatenated_repr() == "with ending expected equal to 'a'"
    matcher = EndsWith([1, 2])
    assert matcher.concatenated_repr() == "with ending expected equal to [1, 2]"


def test_matches_string():
    matcher = EndsWith("bc")
    assert matcher == "abc"
    assert matcher == "bc"
    assert matcher != "dabcx"
    assert matcher != ["x", "bc", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20
    assert matcher != ["x", "bc"]


def test_matches_string_with_matcher():
    matcher = EndsWith(one_of("ab", "ac"))
    assert matcher == "ab"
    assert matcher == "ac"
    assert matcher != "abc"
    assert matcher == "bac"
    assert matcher == "cab"
    assert matcher != "dabc"
    assert matcher != ["x", "bc", "y"]


def test_matches_list():
    matcher = EndsWith([1, 3])
    assert matcher == [2, 1, 3]
    assert matcher == [1, 3]
    assert matcher != [1, 20, 1, 3, 30]
    assert matcher != [10, 20, 30]
    assert matcher != "string"
    assert matcher != 20


def test_matches_list_with_matcher():
    matcher = EndsWith(one_of([1], [2]))
    assert matcher == [1, 3, 2]
    assert matcher == [2]
    assert matcher == [2, 1]
    assert matcher != [1, 2, 3]
    assert matcher != "string"
    assert matcher != 20


def test_matches_with_compound_matcher():
    matcher = EndsWith([is_string()])
    assert matcher == ["a", "b"]
    assert matcher == ["a"]
    assert matcher != ["a", 1]
    assert matcher != "abc"
    matcher = EndsWith([is_string(), is_number()])
    assert matcher == ["a", 1]
    assert matcher == ["x", 28, "z", 10]
    assert matcher != ["a"]
    assert matcher != [1, "a"]
    assert matcher != "abc"


def test_ends_with_matcher():
    matcher = ends_with_matcher("string")
    assert isinstance(matcher, EndsWith)
    assert matcher == "string"
    matcher = ends_with_matcher(None)
    assert matcher is None
