from parsing.easa_parser import parse_xml
from settings import get_default_value

from parsing.utils import add_closed_items, get_closed_items, is_closed_item, remove_outdated_items
from tests.utils import get_test_publications


def test_parser():
    """Parser test based on a small real life scenario (9 publications). 
    The Target is hand-crafted .
    """
    input = open(get_default_value("T_PARSER_INPUT"), "rb").read()
    input = input.decode('ascii', errors="ignore")
    target = get_test_publications(True)

    output = sorted(parse_xml(input), key=lambda x: x['number'])

    assert len(output) == len(target)
    for i in range(len(output)):
        assert output[i] == target[i]

    #parse_respone with empty str
    output = parse_xml("")
    assert not output

def test_utils():
    test_file = get_default_value("P_CLOSED_ITEMS_JSON")  

    #get_closed_items on predefined file    
    input = '{"2019-05-31": ["A", "B"], "2000-01-01":["A", "C", "D"]}'
    target = ["A", "B", "C", "D"]

    with open(test_file, "w") as fd:
        fd.write(input)
    output = get_closed_items()

    assert output == target

    #add_closed_items
    input = ["A", "B", "E", "F"]
    target = sorted(set(target) | set(input)) #["A", "B", "C", "D", "E", "F"]
    store = input

    add_closed_items(input)
    output = get_closed_items()

    assert target == output

    #add_closed_items, empty list
    input = []
    #target = target

    add_closed_items(input)
    output = get_closed_items()

    assert target == output

    #is_closed_item
    input = ["A", "B", "NotClosedA", "NotClosedB"]
    target = ["A", "B"]

    output = sorted(filter(lambda x: is_closed_item(x), input))

    assert target == output

    #remove_outdated_items
    input = test_file
    target = store #Items of add_closed_items test

    remove_outdated_items()
    output = get_closed_items()

    assert target == output