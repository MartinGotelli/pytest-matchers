from unittest.mock import MagicMock

from pytest_matchers.matchers.has_attribute import HasAttribute


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
    assert repr(matcher) == "To have attribute 'attribute_name' and to be 'expected_value'"
    matcher = HasAttribute("attribute_name", 42)
    assert repr(matcher) == "To have attribute 'attribute_name' and to be 42"


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
