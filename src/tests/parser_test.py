import json
from settings import get_default_value

from watcher.parser import parse_response
from watcher.utils import add_closed_items, get_closed_items, is_closed_item, remove_outdated_items


def test_parser():
    """Parser test based on a small real life scenario (9 publications). 
    The Target is hand-crafted .
    """
    with open(get_default_value("T_PARSER_TARGET")) as fd:
        target = json.load(fd)
    with open(get_default_value("T_PARSER_INPUT")) as fd:
        input = fd.read()
    output = parse_response(input)
    assert output.keys() == target.keys()
    for k in target:
        assert output[k] == target[k]

def test_parser_on_empty_str():
    output = parse_response("")
    assert not output

def test_utils():
    test_file = get_default_value("CLOSED_ITEMS_JSON")
    old_items = ["A", "B", "C", "E"]
    old_json = '{"2019-05-31": ["A", "B", "C", "E"]}'
    with open(test_file, "w") as fd:
        fd.write(old_json)

    items = get_closed_items(test_file)
    assert sorted(items) == sorted(old_items)

    items = ["A", "B", "C", "D"]
    add_closed_items(items, test_file)
    target = sorted(set(items) | set(old_items))
    output = get_closed_items(test_file)
    assert target == output

    new_items = ["A", "B", "F", "G"]
    target = ["A", "B"]
    output = sorted(filter(lambda x: is_closed_item(x, test_file), new_items))
    assert target == output

    remove_outdated_items(path=test_file)
    output = get_closed_items(test_file)
    target = ["A", "B", "C", "D"]

    assert target == output