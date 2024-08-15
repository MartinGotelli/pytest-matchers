from typing import Any, Callable, Type

from pytest_matchers.matchers import (
    Anything,
    Between,
    Case,
    Datetime,
    DatetimeString,
    Dict,
    DifferentValue,
    HasAttribute,
    If,
    IsInstance,
    IsList,
    IsNumber,
    IsString,
    JSON,
    Matcher,
    Or,
    SameValue,
)


def anything() -> Anything:
    return Anything()


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


def is_datetime(
    min_value: Any = None,
    max_value: Any = None,
    year: int = None,
    month: int = None,
    day: int = None,
    hour: int = None,
    minute: int = None,
    second: int = None,
) -> Datetime:
    return Datetime(min_value, max_value, year, month, day, hour, minute, second)


def is_datetime_string(
    expected_format: str,
    *,
    min_value: Any = None,
    max_value: Any = None,
) -> DatetimeString:
    return DatetimeString(expected_format, min_value=min_value, max_value=max_value)


def same_value() -> SameValue:
    return SameValue()


def different_value() -> DifferentValue:
    return DifferentValue()


def if_true(
    condition: Callable | bool | Any,
    then: Matcher | Any = None,
    or_else: Matcher | Any = None,
) -> If:
    return If(condition, then, or_else)


def if_false(
    condition: Callable | bool | Any,
    then: Matcher | Any = None,
    or_else: Matcher | Any = None,
) -> If:
    return if_true(condition, or_else, then)  # pylint: disable=arguments-out-of-order


def case(
    case_value: Any,
    expectations: dict[Any, Matcher | Any],
    default_expectation: Matcher | Any | None = None,
) -> Case:
    return Case(case_value, expectations, default_expectation)


def is_dict(matching: dict = None, *, exclude: list[Any] = None) -> Dict:
    return Dict(matching, exclude=exclude)


def is_json(matching: dict = None, *, exclude: list[Any] = None) -> JSON:
    return JSON(matching, exclude=exclude)
