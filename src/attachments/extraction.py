import logging
from PyPDF2 import PdfFileReader
from objects.publication import Publication

from settings import get_default_value


def extract_attachments(publications: dict):
    for p in publications:
        extract_values_from_pdf(p)


def extract_values_from_pdf(p: Publication):
    if p.at_path is None:
        return
    try:
        pdf_reader = PdfFileReader(open(p.at_path, "rb"))
    except FileNotFoundError as e:
        logging.warning(e)
        return
    for i in range(pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        foreign_ad, supersedure, done = p.parse_pattern(page)
        #Avoids overwriting values
        p.foreign_ad = p.foreign_ad or foreign_ad
        p.supersedure = p.supersedure or supersedure
        if done:
            break
