import logging
import requests
from bs4 import BeautifulSoup
from objects.publication import Publication
from parsing import easa_parser

from settings import get_default_value


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