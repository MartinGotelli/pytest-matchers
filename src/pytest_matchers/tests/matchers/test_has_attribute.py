from unittest.mock import MagicMock

from pytest_matchers import is_list, is_string
from pytest_matchers.matchers.has_attribute import HasAttribute, has_attribute_matcher


class WithAttributeMethod:
    @staticmethod
    def attribute_name():  # pragma: no cover
        return "expected_value"


def test_create():
    matcher = HasAttribute("attribute_name")
    assert isinstance(matcher, HasAttribute)
    matcher = HasAttribute("attribute_name", "expected_value")
    assert isinstance(matcher, HasAttribute)


def test_repr():
    matcher = HasAttribute("attribute_name")
    assert repr(matcher) == "To have attribute 'attribute_name'"
    matcher = HasAttribute("attribute_name", "expected_value")
    assert repr(matcher) == "To have attribute 'attribute_name' and equal to 'expected_value'"
    matcher = HasAttribute("attribute_name", 42)
    assert repr(matcher) == "To have attribute 'attribute_name' and equal to 42"
    matcher = HasAttribute("attribute_name", is_string())
    assert repr(matcher) == "To have attribute 'attribute_name' and to be a string"


def test_concatenated_repr():
    matcher = HasAttribute("attribute_name")
    assert matcher.concatenated_repr() == "with 'attribute_name'"
    matcher = HasAttribute("attribute_name", "expected_value")
    assert matcher.concatenated_repr() == "with 'attribute_name' being 'expected_value'"
    matcher = HasAttribute("attribute_name", 42)
    assert matcher.concatenated_repr() == "with 'attribute_name' being 42"
    matcher = HasAttribute("attribute_name", is_string())
    assert matcher.concatenated_repr() == "with 'attribute_name' expecting to be a string"


def test_matches():
    mock = MagicMock(attribute_name="expected_value")
    matcher = HasAttribute("attribute_name")
    assert matcher == mock
    assert matcher == WithAttributeMethod
    assert matcher != 3
    assert matcher != "string"
    matcher = HasAttribute("attribute_name", "expected_value")
    assert matcher == mock
    assert matcher != WithAttributeMethod
    assert matcher != WithAttributeMethod()


def test_matches_with_expect_value_as_matcher():
    int_list_mock = MagicMock(attribute_name=[1, 2, 3])
    str_mock = MagicMock(attribute_name="string")
    matcher = HasAttribute("attribute_name", is_list(int))
    assert matcher == int_list_mock
    assert matcher != str_mock
    assert matcher != [1, 2, 3]
    matcher = HasAttribute("attribute_name", is_list(int, length=3))
    assert matcher == int_list_mock
    assert matcher != str_mock
    matcher = HasAttribute("attribute_name", is_list(int, length=2))
    assert matcher != int_list_mock
    assert matcher != str_mock
    matcher = HasAttribute("attribute_name", is_string())
    assert matcher != int_list_mock
    assert matcher == str_mock


def test_has_attribute_matcher():
    matcher = has_attribute_matcher("attribute_name", None)
    assert isinstance(matcher, HasAttribute)
    matcher = has_attribute_matcher("attribute_name", None, value_needed=True)
    assert matcher is None
    matcher = has_attribute_matcher("attribute_name", "expected_value")
    assert isinstance(matcher, HasAttribute)
    matcher = has_attribute_matcher("attribute_name", "expected_value", value_needed=True)
    assert isinstance(matcher, HasAttribute)
    matcher = has_attribute_matcher(None, None)
    assert matcher is None
