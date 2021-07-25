from settings import get_default_value
import requests, re, os
import logging


def retrieve_attachments(publications: list, path: str = None):
    path = path or get_default_value("ROOT_FOLDER")
    for p in publications:
        p._at_path, p.at_name = retrieve_attachment(p.at_href, p.folder)


def retrieve_attachment(attachment: str, folder: str, path: str = None):
    path = path or get_default_value("ROOT_FOLDER")
    try:
        r = requests.get(attachment)
    except Exception as e:
        logging.exception(e)
        return None, None
    if r.status_code == requests.codes.ok:
        filename = re.findall(r"\"(.*)\"", r.headers["Content-Disposition"])[0]
        path = os.path.join(path, folder, filename)
        try:
            open(path, "x+b").write(r.content)
        except OSError as e:
            logging.warning(e)
        return path, filename
