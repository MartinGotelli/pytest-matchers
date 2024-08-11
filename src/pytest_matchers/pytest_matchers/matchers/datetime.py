from datetime import datetime

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.has_attribute import has_attribute_matcher
from pytest_matchers.utils.matcher_utils import (
    between_matcher,
    is_instance_matcher,
    matches_or_none,
)
from pytest_matchers.utils.repr_utils import concat_reprs


class Datetime(Matcher):  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        min_value: datetime = None,
        max_value: datetime = None,
        year: int = None,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None,
        second: int = None,
    ):
        self._is_instance_matcher = is_instance_matcher(datetime)
        self._limit_matcher = between_matcher(min_value, max_value, None, None, None)
        self._year_matcher = has_attribute_matcher("year", year, value_needed=True)
        self._month_matcher = has_attribute_matcher("month", month, value_needed=True)
        self._day_matcher = has_attribute_matcher("day", day, value_needed=True)
        self._hour_matcher = has_attribute_matcher("hour", hour, value_needed=True)
        self._minute_matcher = has_attribute_matcher("minute", minute, value_needed=True)
        self._second_matcher = has_attribute_matcher("second", second, value_needed=True)

    def matches(self, value: datetime) -> bool:
        return all(
            [
                matches_or_none(self._is_instance_matcher, value),
                matches_or_none(self._limit_matcher, value),
                matches_or_none(self._year_matcher, value),
                matches_or_none(self._month_matcher, value),
                matches_or_none(self._day_matcher, value),
                matches_or_none(self._hour_matcher, value),
                matches_or_none(self._minute_matcher, value),
                matches_or_none(self._second_matcher, value),
            ]
        )

    def __repr__(self) -> str:
        return concat_reprs(
            "To be a datetime",
            self._limit_matcher,
            self._year_matcher,
            self._month_matcher,
            self._day_matcher,
            self._hour_matcher,
            self._minute_matcher,
            self._second_matcher,
        )
