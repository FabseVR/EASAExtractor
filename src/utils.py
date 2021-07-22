import os
import re
import requests

from settings import get_default_value


def create_folder_structure(item_dict: dict, path: str = None):
    path = path or get_default_value('ROOT_FOLDER')
    for number, values in item_dict.items():
        item_folder = f"{values['issued_by']} {values['category']} {number}"
        item_dict[number]['folder'] = item_folder
        try:
            os.mkdir(os.path.join(path, item_folder))
        except OSError as e:
            # TODO: Handle exception appropriately
            print(e)


def retrieve_attachements(item_dict: dict, path: str = None):
    path = path or get_default_value('ROOT_FOLDER')
    for v in item_dict.values():
        retrieve_attachement(v['attachement'], v['folder'])


def retrieve_attachement(attachement: str, folder: str, path: str = None):
    path = path or get_default_value('ROOT_FOLDER')
    r = requests.get(attachement)
    if r.status_code == requests.codes.ok:
        filename = re.findall(r"\"(.*)\"", r.headers['Content-Disposition'])[0]
        with open(os.path.join(path, path, filename), "x+b") as pdf_file:
            pdf_file.write(r.content)
