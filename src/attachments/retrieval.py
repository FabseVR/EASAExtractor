from typing import List, Tuple
from objects.publication import Publication
from settings import get_default_value
import requests, re, os
import logging


def retrieve_attachments(publications: List[Publication]):
    """Retrieves attachments for all Publication objects containing at_href.

    Args:
        publications (List[Publication]): List of Publication objects.
    """
    for p in publications:
        if p.at_href:
            p._at_path, p.at_name = retrieve_attachment(p.at_href, p.folder)


def retrieve_attachment(attachment: str, folder: str) -> Tuple[str, str]:
    """Retrieves and stores the PDF attachment in the given folder. 
    On failure, it returns None for _at_path and at_name

    Args:
        attachment (str): The attachment's link used in the get request.
        folder (str): The name of the folder (relative to ROOT_FOLDER) where the attachment will be stored.

    Returns:
        Tuple[str, str]: Absolute path of the attachment, the attachment filename
    """
    path = get_default_value("ROOT_FOLDER")

    try:
        r = requests.get(attachment, timeout=10)
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

    return None, None
