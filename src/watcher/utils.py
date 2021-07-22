import json
from datetime import date, timedelta

from settings import get_default_value


def get_closed_items(path: str = None) -> list:
    """Returns a sorted list of all closed items (numbers) stored locally.

    Args:
        path (str, optional): Path to the local JSON file. Defaults to CLOSED_ITEMS_JSON.

    Returns:
        list: Sorted list of items (number)
    """
    path = path or get_default_value("CLOSED_ITEMS_JSON")

    with open(path) as fd:
        items = json.load(fd)
    return sorted(set([it for it_list in items.values() for it in it_list]))


def add_closed_items(items: list, path: str = None):
    """Adds a list of items (numbers) to the locally stored JSON file.

    Args:
        items (list): Item numbers as str
        path (str, optional): Path to the local JSON file. Defaults to CLOSED_ITEMS_JSON.
    """
    path = path or get_default_value("CLOSED_ITEMS_JSON")

    with open(path, "r") as fd:
        items_json = json.load(fd)
    key = date.today().isoformat()
    if key in items_json:
        items_json[key].append(items)
    else:
        items_json[key] = items
    with open(path, "w") as fd:
        json.dump(items_json, fd)


def is_closed_item(item: str, path: str = None) -> bool:
    path = path or get_default_value("CLOSED_ITEMS_JSON")
    return item in get_closed_items(path)


def remove_outdated_items(MAX_DAYS: int = 90, path: str = None):
    """Removes items that are older than MAX_DAYS to keep memory clean.

    Args:
        MAX_DAYS (int, optional): Largest amount of days items are stored. Defaults to 90.
        path (str, optional): Path to the local JSON file. Defaults to CLOSED_ITEMS_JSON.
    """
    def is_older_than_max_days(x):
        return date.fromisoformat(x) < (date.today() - timedelta(days=MAX_DAYS))
    path = path or get_default_value("CLOSED_ITEMS_JSON")

    with open(path, "r") as fd:
        items_json = json.load(fd)
    for item in list(filter(is_older_than_max_days, items_json)):
        del items_json[item]
    with open(path, "w") as fd:
        json.dump(items_json, fd)
