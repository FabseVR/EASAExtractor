import logging
import os
from settings import get_default_value


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
