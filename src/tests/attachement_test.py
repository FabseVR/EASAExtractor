from utils import create_folder_structure

def test_folder_structure():
    test_dict = {
        "00": {
            "issued_by": "TEST",
            "category": "TEST"
        }
    }
    create_folder_structure(test_dict)

    assert test_dict["00"]["folder"]
    assert test_dict["00"]["folder"] == "TEST TEST 00"