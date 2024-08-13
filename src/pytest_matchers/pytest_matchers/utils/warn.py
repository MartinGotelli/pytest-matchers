import os
import warnings
from typing import Type


def _warnings_enabled() -> bool:
    return os.environ.get("PYTEST_MATCHERS_WARNINGS", "True") == "True"


def warn(warning: str, category: Type[Warning] = UserWarning) -> None:
    if _warnings_enabled():
        warnings.warn(warning, category)
