from typing import Any, Type

from src.matchers import IsInstance, IsList, IsNumber, IsString, Matcher, Or


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
