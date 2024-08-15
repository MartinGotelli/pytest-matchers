from pytest_matchers.matchers import Eq, IsInstance
from pytest_matchers.utils.repr_utils import (
    capitalized,
    concat_matcher_repr,
    concat_reprs,
    non_capitalized,
)


def test_concat_matcher_repr():
    matcher = IsInstance(str)
    assert concat_matcher_repr(matcher) == "of 'str' instance"
    matcher = Eq(3)
    assert concat_matcher_repr(matcher) == "equal to 3"
    matcher = None
    assert concat_matcher_repr(matcher) is None


def test_concat_reprs():
    assert concat_reprs(None) == ""
    assert concat_reprs("I expect") == "I expect"
    assert concat_reprs("I expect", Eq(3)) == "I expect equal to 3"
    assert concat_reprs("I expect", Eq(3), Eq(4)) == "I expect equal to 3 and equal to 4"
    assert (
        concat_reprs("I expect", IsInstance(str), Eq(2), "be happy")
        == "I expect of 'str' instance and equal to 2 and be happy"
    )
    assert (
        concat_reprs("I expect", Eq(3), Eq(4), separator="or")
        == "I expect equal to 3 or equal to 4"
    )


def test_capitalized():
    assert capitalized("i expect") == "I expect"
    assert capitalized("I expect") == "I expect"
    assert capitalized("I KNOW") == "I KNOW"
    assert capitalized("") == ""


def test_non_capitalized():
    assert non_capitalized("i expect") == "i expect"
    assert non_capitalized("I expect") == "i expect"
    assert non_capitalized("I KNOW") == "i KNOW"
    assert non_capitalized("") == ""
