import requests, re
from bs4 import BeautifulSoup

from watcher.parser import parse_response, request_items, request_local_items
from watcher.utils import add_closed_items, get_closed_items, is_closed_item, remove_outdated_items

LAST_X_DAYS = 14

remove_outdated_items()
html = request_local_items(LAST_X_DAYS)
response_dict = parse_response(html)
for item in filter(is_closed_item, response_dict):
    del response_dict[item]
#Apply Filtering
#Custom Selection
#...
add_closed_items(response_dict)