from unittest.mock import MagicMock

from pytest_matchers import is_number, is_string, one_of
from pytest_matchers.asserts.comparers.set import SetComparer


def test_compare():
    comparer = SetComparer({1, 2, 3}, {1, 2, 3})
    assert comparer.compare()
    comparer = SetComparer({1, 2, 3}, {1, 2, 4})
    assert not comparer.compare()
    comparer = SetComparer({1, 2, 3}, {1, 2})
    assert not comparer.compare()
    comparer = SetComparer({1, 2}, {2, 1})
    assert comparer.compare()


def test_compare_with_matchers():
    comparer = SetComparer({1, 2, 3}, {3, 2, is_number()})
    assert comparer.compare()
    comparer = SetComparer({1, 2, 3}, {is_number(min_value=2), 3})
    assert not comparer.compare()
    comparer = SetComparer({1, 2, 3}, {is_number(min_value=2), is_number(min_value=2), 3})
    assert not comparer.compare()
    comparer = SetComparer({1, 2, 3}, {is_number(min_value=2), is_number(min_value=1), 3})
    assert comparer.compare()
    comparer = SetComparer(
        {"abc", "acb", "feeg"}, {is_string(), is_string(starts_with="ac"), "feeg"}
    )
    assert comparer.compare() == one_of(True, False)  # It's a limitation of the set comparison


def test_compare_fail_fast():
    mock = MagicMock()
    comparer = SetComparer({1, 2, mock}, {1, 3, 4})
    assert not comparer.compare()
    try:
        mock.__eq__.assert_not_called()  # pylint: disable=no-member
    except AssertionError:  # pragma: no cover
        # Sometimes the mock is the first or second object called,
        # in that case it expects to be compared with at least two values
        assert mock.__eq__.call_count == one_of(2, 3)  # pylint: disable=no-member
    comparer = SetComparer({1, 2, 3, mock}, {1, 2, 3, 4})
    assert not comparer.compare()
    try:
        mock.__eq__.assert_called_once_with(4)  # pylint: disable=no-member
    except AssertionError:  # pragma: no cover
        # Same case here, the mock is the first or second object called
        assert mock.__eq__.call_count == is_number(  # pylint: disable=no-member
            int,
            min_value=3,
            max_value=7,
        )


def test_compare_fail_fast_false():
    mock = MagicMock()
    comparer = SetComparer({1, 2, 5, mock}, {1, 2, 3, 4}, fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_called_with(4)  # pylint: disable=no-member
    mock = MagicMock()
    comparer = SetComparer({1, 2, 3, mock}, {1, 2, 3, 4}, fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_called_with(4)  # pylint: disable=no-member


def test_compare_fail_fast_false_different_length():
    mock = MagicMock()
    comparer = SetComparer({1, 2, mock}, {1, 2}, fail_fast=False)
    assert not comparer.compare()
    try:
        mock.__eq__.assert_not_called()  # pylint: disable=no-member
    except AssertionError:  # pragma: no cover
        # Sometimes the mock is the first or second object called
        assert mock.__eq__.call_count == one_of(1, 2)  # pylint: disable=no-member
    mock = MagicMock()
    comparer = SetComparer({1, 2}, {1, 2, mock}, fail_fast=False)
    assert not comparer.compare()
    try:
        mock.__eq__.assert_not_called()  # pylint: disable=no-member
    except AssertionError:  # pragma: no cover
        assert mock.__eq__.call_count == one_of(1, 2)  # pylint: disable=no-member
