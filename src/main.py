from attachments.extraction import extract_attachments
from filtering.filter import validate
from gui.root import run_app
from csv_generator.generator import write_csv
from utils import configure_logging, make_dirs
from parsing.parser import request_items
from parsing.utils import add_closed_items, is_closed_item, remove_outdated_items
from attachments.retrieval import retrieve_attachments

def generate_func(publications, set_status):
    make_dirs(publications)
    set_status("Retrieve attachments.")
    retrieve_attachments(publications)
    set_status("Extracting information from PDF attachments.")
    extract_attachments(publications)
    add_closed_items([p.number for p in publications])
    set_status("Export values to csv file.")
    write_csv(publications)
    set_status("Done.")

def filter_func(publications):
    return list(map(lambda x: x.number, filter(lambda x: validate(x.__dict__), publications)))

if __name__ == '__main__':
    configure_logging()

    remove_outdated_items()
    publications = request_items()
    publications = list(filter(lambda x: not is_closed_item(x.number), publications))
    run_app(publications=publications, filter_func=filter_func, confirm_func=generate_func)
