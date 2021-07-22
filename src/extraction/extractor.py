from PyPDF2 import PdfFileReader
import re
import os

from settings import get_default_value


def update_item_dict(item_dict: dict):
    path = get_default_value("ROOT_FOLDER")
    for v in item_dict.values():
        v.update(
            **extract_values_from_pdf(os.path.join(path, v['folder'], v['attachement']), v['issued_by']))


def extract_values_from_pdf(file: str, style: str) -> dict:
    _supported_styles = ["EASA", "FAA"]

    def parse_easa_pattern(text, d):
        text = re.sub(r"\n(?=\S)", r"", text)
        # Returns key-value pairs for each occurence of ^key:value$
        kv = dict(re.findall(r"^ *([^:\n]+)\s*:\s*(.+)", text, re.MULTILINE))
        if not d["foreign_ad"]:
            d["foreign_ad"] = kv.get("Foreign AD")
        if not d["supersedure"]:
            d["supersedure"] = kv.get("Supersedure")
        return d["foreign_ad"] and d["supersedure"]

    def parse_faa_pattern(text, d):
        text = re.sub(r"\n(?=\S)", r"", text)
        kv = dict(re.findall(r"^\s*\([a-z]\) +(.+)\s+(.+)", text, re.MULTILINE))
        if not d["foreign_ad"]:
            d["foreign_ad"] = kv.get("Affected ADs")
        return d["foreign_ad"] is not None

    out = {"foreign_ad": None, "supersedure": None}
    if style not in _supported_styles:
        return out

    pdf_reader = PdfFileReader(open(file, "rb"))
    for i in range(pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        if style == "EASA":
            done = parse_easa_pattern(page, out)
        elif style == "FAA":
            done = parse_faa_pattern(page, out)
        if done:
            break
    return out
