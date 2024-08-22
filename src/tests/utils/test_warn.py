import os
from unittest.mock import patch

from pytest_matchers.utils.warn import warn


@patch("pytest_matchers.utils.warn.warnings.warn")
def test_warn(mock_warn):
    with patch.dict(os.environ, {"PYTEST_MATCHERS_WARNINGS": "True"}):
        warn("A warning")
        mock_warn.assert_called_with("A warning", UserWarning)


@patch("pytest_matchers.utils.warn.warnings.warn")
def test_warn_with_category(mock_warn):
    with patch.dict(os.environ, {}, clear=True):
        warn("Another warning", DeprecationWarning)
        mock_warn.assert_called_with("Another warning", DeprecationWarning)


@patch("pytest_matchers.utils.warn.warnings.warn")
def test_warnings_disabled(mock_warn):
    with patch.dict(os.environ, {"PYTEST_MATCHERS_WARNINGS": "False"}):
        warn("A warning")
        mock_warn.assert_not_called()

    with patch.dict(os.environ, {"PYTEST_MATCHERS_WARNINGS": "True"}):
        warn("A warning")
        mock_warn.assert_called_with("A warning", UserWarning)
