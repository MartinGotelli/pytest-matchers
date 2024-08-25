from pytest_matchers import is_number, is_string, one_of
from pytest_matchers.matchers import StartsWith
from pytest_matchers.matchers.starts_with import starts_with_matcher


def test_create():
    matcher = StartsWith("a")
    assert isinstance(matcher, StartsWith)
    matcher = StartsWith([1, 2])
    assert isinstance(matcher, StartsWith)


def test_repr():
    matcher = StartsWith("a")
    assert repr(matcher) == "To start with 'a'"
    matcher = StartsWith([1, 2])
    assert repr(matcher) == "To start with [1, 2]"


def test_concatenated_repr():
    matcher = StartsWith("a")
    assert matcher.concatenated_repr() == "with start expected equal to 'a'"
    matcher = StartsWith([1, 2])
    assert matcher.concatenated_repr() == "with start expected equal to [1, 2]"


def test_matches_string():
    matcher = StartsWith("ab")
    assert matcher == "ab"
    assert matcher == "abc"
    assert matcher != "dabc"
    assert matcher != ["x", "ab", "y"]
    assert matcher != "ac"
    assert matcher != ["abc"]
    assert matcher != 20
    assert matcher != ["ab", "x"]


def test_matches_string_with_matcher():
    matcher = StartsWith(one_of("ab", "ac"))
    assert matcher == "ab"
    assert matcher == "ac"
    assert matcher == "abc"
    assert matcher == "acb"
    assert matcher != "dabc"
    assert matcher != ["ab", "x", "y"]
    assert matcher != "ad"
    assert matcher != 20


def test_matches_list():
    matcher = StartsWith([1, 3])
    assert matcher == [1, 3, 2]
    assert matcher == [1, 3]
    assert matcher != [1, 20, 1, 3, 30]
    assert matcher != [10, 20, 30]
    assert matcher != "string"
    assert matcher != 20


def test_matches_list_with_matcher():
    matcher = StartsWith(one_of([1], [2]))
    assert matcher == [1, 3, 2]
    assert matcher == [2, 3]
    assert matcher != [20, 1, 3, 30]


def test_matches_with_compound_matcher():
    matcher = StartsWith([is_string()])
    assert matcher == ["a", "b"]
    assert matcher == ["a"]
    assert matcher != [1, "a"]
    assert matcher != "abc"
    matcher = StartsWith([is_string(), is_number()])
    assert matcher == ["a", 1]
    assert matcher == ["x", 28, "z", 10]
    assert matcher != ["a"]
    assert matcher != [1, "a"]
    assert matcher != "abc"


def test_starts_with_matcher():
    matcher = starts_with_matcher("string")
    assert isinstance(matcher, StartsWith)
    assert matcher == "string"
    matcher = starts_with_matcher(None)
    assert matcher is None
