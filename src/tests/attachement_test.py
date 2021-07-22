from utils import create_folder_structure
from tests.utils import clear_path
import pytest

TEST_ROOT = "tests/data/root"

def test_folder_structure():
    test_dict = {
        "00": {
            "issued_by": "TEST",
            "category": "TEST"
        }
    }
    create_folder_structure(test_dict, TEST_ROOT)

    assert test_dict["00"]["path"]
    assert test_dict["00"]["path"] == "TEST TEST 00"

@pytest.fixture(scope="session", autouse=True)
def clean_up(request):
    def clear_path_finalizer():
        clear_path(TEST_ROOT)
    request.addfinalizer(clear_path_finalizer)