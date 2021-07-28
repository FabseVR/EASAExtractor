import json
import os
from objects.publication import Publication

from settings import get_default_value

def get_test_publications(as_dict=False):
    target = sorted(json.load(open(get_default_value("T_PARSER_TARGET"))).values(), key=lambda x: x["number"])
    if not as_dict:
        target = [Publication(**v) for v in target]
    return target

def clear_path(path):
    for p in os.listdir(path):
        p = os.path.join(path, p)
        if os.path.isfile(p):
            os.remove(p)
        else:
            try:
                os.rmdir(p)
            except OSError as e:
                clear_path(p)
    os.rmdir(path)

def retrieve_attachments(publications: list):
    for p in publications:
        p.attachment = "test"