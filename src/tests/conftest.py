from settings import get_default_value, load_settings
from tests.utils import clear_path

import pytest

SETTINGS = "tests/data/settings.json"


@pytest.hookimpl()
def pytest_sessionstart(session):
    load_settings(SETTINGS)


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    clear_path(get_default_value("ROOT_FOLDER"))
