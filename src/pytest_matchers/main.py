from typing import Any, Type

from pytest_matchers.matchers import (
    Between,
    HasAttribute,
    IsInstance,
    IsList,
    IsNumber,
    IsString,
    Matcher,
    Or,
)


def is_instance(match_type: Type) -> IsInstance:
    return IsInstance(match_type)


def is_list(match_type: Type = None, **kwargs) -> IsList | IsInstance:
    if match_type is None and not kwargs:
        return is_instance(list)
    return IsList(match_type, **kwargs)


def is_string(**kwargs) -> IsString:
    return IsString(**kwargs)


def is_number(match_type: Type = None, **kwargs) -> IsNumber:
    return IsNumber(match_type, **kwargs)


def one_of(*values: Matcher | Any) -> Or:
    return Or(*values)


def has_attribute(attribute_name: str, expected_value: Any = None) -> HasAttribute:
    return HasAttribute(attribute_name, expected_value)


def between(
    min_value: Any,
    max_value: Any,
    *,
    inclusive: bool = None,
    min_inclusive: bool = None,
    max_inclusive: bool = None,
) -> Between:
    return Between(min_value, max_value, inclusive, min_inclusive, max_inclusive)
