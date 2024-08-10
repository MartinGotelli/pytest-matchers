from pytest_matchers.matchers import Eq, IsInstance
from pytest_matchers.utils.repr_utils import concat_matcher_repr, concat_reprs


def test_concat_matcher_repr():
    matcher = IsInstance(str)
    assert concat_matcher_repr(matcher) == "of 'str' instance"
    matcher = Eq(3)
    assert concat_matcher_repr(matcher) == "to be 3"
    matcher = None
    assert concat_matcher_repr(matcher) is None


def test_concat_reprs():
    assert concat_reprs(None) is None
    assert concat_reprs("I expect") == "I expect"
    assert concat_reprs("I expect", Eq(3)) == "I expect to be 3"
    assert concat_reprs("I expect", Eq(3), Eq(4)) == "I expect to be 3 and to be 4"
    assert (
        concat_reprs("I expect", IsInstance(str), Eq(2), "be happy")
        == "I expect of 'str' instance and to be 2 and be happy"
    )
    assert concat_reprs("I expect", Eq(3), Eq(4), separator="or") == "I expect to be 3 or to be 4"
