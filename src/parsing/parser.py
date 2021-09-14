from objects.publication import Publication
from parsing import easa_parser


def request_items(type, *args) -> list:
    """Send POST request to the EASA website to retrieve recent publications

    Args:
        days (int): Days from today to determine the 'filter by date' start

    Returns:
        list: Parsed publications
    """
    if type == "EASA":
        return list(map(lambda kwargs: Publication(**kwargs), easa_parser.request_items(*args)))
    else:
        return None