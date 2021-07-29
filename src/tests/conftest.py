from settings import get_default_value, load_settings
from tests.utils import clear_path

import pytest
import os

BASE_PATH = "tests/DATA/"


@pytest.hookimpl()
def pytest_sessionstart(session):
    load_settings(BASE_PATH)
    os.mkdir(get_default_value("T_TEMP_FOLDER"))


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    clear_path(get_default_value("T_TEMP_FOLDER"))
