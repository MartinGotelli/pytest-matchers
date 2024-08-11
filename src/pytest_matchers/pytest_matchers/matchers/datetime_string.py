from datetime import datetime

from pytest_matchers.matchers import IsString, Matcher
from pytest_matchers.utils.matcher_utils import between_matcher, matches_or_none
from pytest_matchers.utils.repr_utils import concat_reprs


class DatetimeString(Matcher):
    def __init__(
        self,
        expected_format: str,
        *,
        min_value: datetime | str = None,
        max_value: datetime | str = None,
    ):
        self._expected_format = expected_format
        self._between_matcher = between_matcher(
            self._as_datetime(min_value, "min_value"),
            self._as_datetime(max_value, "max_value"),
            None,
            None,
            None,
        )

    def _as_datetime(self, value: datetime | str, value_name: str) -> datetime | None:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, self._expected_format)
            except ValueError as error:
                raise ValueError(
                    f"Invalid datetime string format for {value_name}: {value}"
                ) from error
        if isinstance(value, datetime):
            return datetime.strptime(
                datetime.strftime(value, self._expected_format),
                self._expected_format,
            )
        return None

    def matches(self, value: str) -> bool:
        return IsString() == value and self._matches_format_and_limit(value)

    def _matches_format_and_limit(self, value: str) -> bool:
        try:
            date_time = datetime.strptime(value, self._expected_format)
            return matches_or_none(self._between_matcher, date_time)
        except ValueError:
            return False

    def __repr__(self) -> str:
        return concat_reprs(
            f"To be a datetime string with format {repr(self._expected_format)}",
            self._between_matcher,
        )
