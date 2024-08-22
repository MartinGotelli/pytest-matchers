import os

from pytest_matchers import plugin

os.environ["PYTEST_MATCHERS_WARNINGS"] = "False"


def pytest_configure(config):
    config.pluginmanager.register(plugin)


class CustomEqual:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, CustomEqual) and self.value == other.value

    def __ne__(self, other):
        return isinstance(other, CustomEqual) and self.value != other.value

    def __hash__(self):
        return hash(self.value)
