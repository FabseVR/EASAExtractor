import json
from attachments.extraction import extract_attachments
from settings import get_default_value
from tests.utils import get_test_publications
from utils import make_dirs
import os

def test_folder_structure():
    input = get_test_publications()
    target = json.load(open(get_default_value("T_EXTRACTION_TARGET")))

    make_dirs(input, get_default_value("T_TEMP_FOLDER"))

    for p in input:
        assert p.folder == target[p.number]["folder"]
        assert os.path.isdir(os.path.join(get_default_value("ROOT_FOLDER"), p.folder))

def test_attachement_extraction():
    target = json.load(open(get_default_value("T_EXTRACTION_TARGET")))
    input = get_test_publications()
    for p in input:
        p.at_name = target[p.number]["at_name"]
    
    extract_attachments(input)

    for p in input:
        assert p.foreign_ad == target[p.number]["foreign_ad"]
        assert p.supersedure == target[p.number]["supersedure"]
    