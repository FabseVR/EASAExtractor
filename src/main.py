import requests, re
from bs4 import BeautifulSoup
from tests.utils import clear_path
from utils import create_folder_structure, retrieve_attachement, retrieve_attachements

from watcher.parser import parse_response, request_items, request_local_items
from watcher.utils import add_closed_items, get_closed_items, is_closed_item, remove_outdated_items

LAST_X_DAYS = 14

remove_outdated_items()
html = request_local_items(LAST_X_DAYS)
item_dict = parse_response(html)
for item in filter(is_closed_item, item_dict):
    del item_dict[item]
#Apply Filtering
#Custom Selection
create_folder_structure(item_dict)
#...
#retrieve_attachements(item_dict)
#add_closed_items(item_dict)