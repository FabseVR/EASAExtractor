from filtering.filter import _allow, _forbid, validate
from settings import get_default_value
from tests.utils import get_test_publications


def test_filter():
    input = get_test_publications()
    target = [
        ("2021-0174", False),
        ("2021-0173", False),
        ("2021-14-20", False),
        ("2021-13-10", False),
        ("2021-17", False),
        ("2021-0172", True),
        ("2021-0152", False),
        ("2015-0036", True),
        ("21-093", False),
    ]

    output = [(p.number, validate(p.__dict__)) for p in input]

    assert sorted(output) == sorted(target)

    # type: str
    # _forbid
    input = ("test", "value", {"test": {"forbidden": []}})
    target = {"test": {"forbidden": ["value"]}}

    output = _forbid(*input)

    assert output == target

    # Duplicates are not allowed
    output = _forbid(*input)

    assert output == target

    # _allow
    target = {"test": {"forbidden": []}}

    output = _allow(*input)

    assert output == target

    output = _allow(*input)

    assert output == target

    # type: list
    # _forbid
    input = ("test", "value", {"test": {"type": "list", "schema": {"forbidden": []}}})
    target = {"test": {"type": "list", "schema": {"forbidden": ["value"]}}}

    output = _forbid(*input)

    assert output == target

    # Duplicates are not allowed
    output = _forbid(*input)

    assert output == target

    # _allow
    target = {"test": {"type": "list", "schema": {"forbidden": []}}}

    output = _allow(*input)

    assert output == target

    output = _allow(*input)

    assert output == target
