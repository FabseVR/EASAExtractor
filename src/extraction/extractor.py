from PyPDF2 import PdfFileReader
import re
import os

from settings import get_default_value

def update_item_dict(item_dict: dict):
    path = get_default_value("ROOT_FOLDER")
    for v in item_dict.values():
        v.update(**extract_values_from_pdf(os.path.join(path, v['folder'], v['attachement'])))
    
def extract_values_from_pdf(file: str) -> dict:
    pdf_reader = PdfFileReader(open(file, "rb")) 
    foreign_ad = None
    supersedure = None
    for i in range(pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        page = re.sub(r"\n(?=\S)", r"", page)
        #Returns key-value pairs for each occurence of ^key:value$
        kv = dict(re.findall(r"^ *([^:\n]+)\s*:\s*(.+)", page, re.MULTILINE))
        foreign_ad = foreign_ad or kv.get("Foreign AD")
        supersedure = supersedure or kv.get("Supersedure")
        if foreign_ad and supersedure:
            break
    return {"foreign_ad": foreign_ad, "supersedure": supersedure}
