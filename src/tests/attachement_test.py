from settings import get_default_value
from utils import create_folder_structure

def test_folder_structure():
    test_dict = {
        "00": {
            "issued_by": "TEST",
            "category": "TEST"
        }
    }
    create_folder_structure(test_dict, get_default_value("T_TEMP_FOLDER"))

    assert test_dict["00"]["folder"]
    assert test_dict["00"]["folder"] == "TEST TEST 00"