import json

from watcher.parser import parse_response


def test_parser():
    """Parser test based on a small real life scenario (9 publications). 
    The Target is hand-crafted .
    """
    with open("tests/data/test.json") as fd:
        target = json.load(fd)
    with open("tests/data/test.html") as fd:
        input = fd.read()
    output = parse_response(input)
    assert output.keys() == target.keys()
    for k in target:
        assert output[k] == target[k]

def test_parser_on_empty_str():
    output = parse_response("")
    assert output == {}