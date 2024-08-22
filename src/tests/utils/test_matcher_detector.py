from pytest_matchers import is_instance
from pytest_matchers.utils.matcher_detector import MatcherDetector


def test_uses_matcher():
    detector = MatcherDetector(3)
    assert not detector.uses_matchers()
    detector = MatcherDetector(is_instance(int))
    assert detector.uses_matchers()


def test_uses_matcher_in_a_list():
    detector = MatcherDetector([3, 4])
    assert not detector.uses_matchers()
    detector = MatcherDetector([3, is_instance(int)])
    assert detector.uses_matchers()


def test_uses_matcher_in_a_tuple():
    detector = MatcherDetector((3, 4))
    assert not detector.uses_matchers()
    detector = MatcherDetector((3, is_instance(int)))
    assert detector.uses_matchers()


def test_uses_matcher_in_a_set():
    detector = MatcherDetector({3, 4})
    assert not detector.uses_matchers()
    detector = MatcherDetector({3, is_instance(int)})
    assert detector.uses_matchers()


def test_uses_matcher_in_a_dict():
    detector = MatcherDetector({"a": 3, "b": 4})
    assert not detector.uses_matchers()
    detector = MatcherDetector({"a": 3, "b": is_instance(int)})
    assert detector.uses_matchers()


def test_uses_matcher_in_nested_iterables():
    detector = MatcherDetector({"a": [3, 4], "b": (5, 6)})
    assert not detector.uses_matchers()
    detector = MatcherDetector({"a": [3, is_instance(int)], "b": (5, 6)})
    assert detector.uses_matchers()
    detector = MatcherDetector({"a": [3, 4], "b": (5, is_instance(int))})
    assert detector.uses_matchers()
    detector = MatcherDetector({"a": {3: is_instance(int)}})
    assert detector.uses_matchers()
    detector = MatcherDetector([{"a": 3}, {"b": is_instance(int)}])
    assert detector.uses_matchers()
