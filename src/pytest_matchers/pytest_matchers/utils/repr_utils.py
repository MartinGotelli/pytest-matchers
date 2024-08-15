from pytest_matchers.matchers import Matcher


def _repr(extra_repr: str | Matcher | None) -> str:
    if isinstance(extra_repr, Matcher):
        return extra_repr.concatenated_repr()
    return extra_repr


def concat_matcher_repr(matcher: Matcher | None) -> str:
    return _repr(matcher)


def concat_reprs(
    base_repr: str | Matcher | None,
    *extra_reprs: str | Matcher | None,
    separator: str = "and",
) -> str:
    base_repr = str(base_repr) if base_repr else ""
    extra_repr = f" {separator} ".join(
        [_repr(extra_repr) for extra_repr in extra_reprs if extra_repr]
    )
    if not base_repr and extra_repr:
        return capitalized(extra_repr)
    if extra_repr:
        return f"{base_repr} {extra_repr}"
    return base_repr


def capitalized(string: str):
    if not string:
        return string
    return string[0].upper() + string[1:]


def non_capitalized(string: str):
    if not string:
        return string
    return string[0].lower() + string[1:]
