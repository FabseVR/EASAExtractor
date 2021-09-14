from genericpath import exists
import json
import logging
import os
from settings import CONSTANTS, SETTINGS, get_default_value

DEFAULT_SETTINGS = {
  "ROOT_FOLDER": "",
  "WEBADDRESS": "https://ad.easa.europa.eu/search/advanced/result/",
  "LAST_X_DAYS": "14",
  "PATTERN": {
    "p": "category,ASB,,LTA,,FAA,,EASA,,effective_date,,,,,,,supersedure,foreign_ad,holder_and_type,",
    "subpatterns": {
      "ASB": { "p": "number,revision,issue_date,", "condition": "issued_by" },
      "LTA": { "p": "number,revision,issue_date,", "condition": "issued_by" },
      "FAA": { "p": "number,revision,issue_date,", "condition": "issued_by" },
      "EASA": { "p": "number,revision,issue_date,", "condition": "issued_by" }
    }
  },
  "FILTER": {
    "number": { "forbidden": [] },
    "category": { "forbidden": [] },
    "revision": { "forbidden": [] },
    "issued_by": { "allowed": ["FAA", "EASA"], "forbidden": [] },
    "issue_date": { "forbidden": [] },
    "subject": { "forbidden": [] },
    "holder": { "type": "list", "schema": { "forbidden": [] } },
    "types": { "type": "list", "schema": { "forbidden": [] } },
    "effective_date": { "forbidden": [] },
    "attachment": { "forbidden": [] }
  }
}
DEFAULT_CONSTANT = {
  "P_CLOSED_ITEMS_JSON": "closed_items.json",
  "P_LOGGING_PATH": "logs.log"
}


def make_dirs(publications: list, path: str = None):
    path = path or get_default_value("ROOT_FOLDER")
    for p in publications:
        try:
            os.mkdir(os.path.join(path, p.folder))
        except FileExistsError as e:
            logging.warning(e)


def configure_logging():
    logging.basicConfig(
        filename=get_default_value("P_LOGGING_PATH"),
        format="%(asctime)s: %(message)s"
    )

def create_data_path(update=False):
    data_path = os.path.expanduser('~/.easaextract/')
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # init closed_items.json as valid JSON {}
    closed_items = os.path.join(data_path, 'closed_items.json')
    if not os.path.exists(closed_items):
        open(closed_items, 'x+').write('{}')

    # init settings.json with default values
    settings = os.path.join(data_path, 'settings.json')
    if not os.path.exists(settings):
        json.dump(DEFAULT_SETTINGS, open(settings, 'x+'))
    elif update:
        old_settings = json.load(open(settings))
        d = DEFAULT_SETTINGS
        d.update(**old_settings)
        json.dump(d, open(settings, 'w'))

    #init constant with default values
    constant = os.path.join(data_path, 'constant.json')
    if not os.path.exists(constant):
        json.dump(DEFAULT_CONSTANT, open(constant, 'x+'))
    elif update:
      old_constant = json.load(open(constant))
      d = DEFAULT_CONSTANT
      d.update(**old_constant)
      json.dump(d, open(constant, 'w'))

    # init logs.log as empty file
    logs = os.path.join(data_path, 'logs.log')
    if not os.path.exists(logs):
        open(logs, 'x')