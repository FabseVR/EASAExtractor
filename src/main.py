import requests, re
from bs4 import BeautifulSoup

from watcher.parser import parse_response, request_items, request_local_items

LAST_X_DAYS = 14

html = request_local_items(LAST_X_DAYS)
print(parse_response(html))
