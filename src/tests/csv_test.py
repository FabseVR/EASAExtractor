import json, os
from csv_generator.generator import generate_csv, write_csv
from settings import get_default_value
from tests.utils import get_test_publications

def test_csv():
    extract = json.load(open(get_default_value("T_EXTRACTION_TARGET")))
    input = get_test_publications()
    for p in input:
        p.foreign_ad = extract[p.number]["foreign_ad"]
        p.supersedure = extract[p.number]["supersedure"]
    target = open(get_default_value("T_CSV_TARGET"))

    filename = write_csv(input, get_default_value("T_TEMP_FOLDER"))
    output = open(os.path.join(get_default_value("T_TEMP_FOLDER"), filename))
    
    for output_line in output:
        target_line = target.readline()
        assert output_line.strip() == target_line.strip()