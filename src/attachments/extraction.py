import logging
from typing import List
from PyPDF2 import PdfFileReader
from objects.publication import Publication

from settings import get_default_value


def extract_attachments(publications: List[Publication]):
    """If a publication includes PDF attachments (stored at at_path), 
    these attachments will be used to get information about foreign_ad and supersedure.

    Args:
        publications (List[Publication]): List of Publication objects
    """
    for p in publications:
        if p.at_path is not None:
            extract_values_from_pdf(p)


def extract_values_from_pdf(p: Publication):
    """If the PDF attachment can be read successfully, 
    the content will be parsed to identify foreign_ad and supersedure. 
    One or both might become None if no value can be found.

    Args:
        p (Publication): A Publication object where at_path is not None
    """
    try:
        pdf_reader = PdfFileReader(open(p.at_path, "rb"))
    except FileNotFoundError as e:
        logging.warning(e)
        return
    for i in range(pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        foreign_ad, supersedure, done = p.parse_pattern(page)
        # Avoids overwriting values
        p.foreign_ad = p.foreign_ad or foreign_ad
        p.supersedure = p.supersedure or supersedure
        if done:
            break
