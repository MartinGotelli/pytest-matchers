from typing import Any

from src.matchers import IsInstance, IsList, IsString, Matcher, Or


def is_instance(match_type) -> IsInstance:
    return IsInstance(match_type)


def is_list(match_type=None, **kwargs) -> IsList | IsInstance:
    if match_type is None and not kwargs:
        return is_instance(list)
    return IsList(match_type, **kwargs)


def is_string(**kwargs) -> IsString:
    return IsString(**kwargs)


def one_of(*values: Matcher | Any) -> Or:
    return Or(*values)
