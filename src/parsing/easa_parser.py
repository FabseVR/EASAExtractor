import enum
from logging import exception
import logging
from typing import Dict, Tuple
from objects.publication import Publication
from settings import get_default_value
from datetime import date, timedelta
import xml.etree.ElementTree as ET
import requests
import re
import html


def category_factory(x):
    return {"category": x.text}


def number_factory(x):
    x = x.text
    if re.match(r"[A-Z]+-", x):
        _, _, x = x.partition("-")
    if x[-2] == "R":
        return {"number": x[:-2], "revision": x[-1]}
    return {"number": x, "revision": "0"}


def issue_date_factory(x):
    return {"issue_date": x.text}


def subject_factory(x):
    return {"subject": re.sub(r"\s+", r" ", x.text.strip())}


def type_designation_factory(x):
    def parse_types(x):
        x = re.split(r" / ", x)
        if len(x) == 1:
            x = re.split(r"/", x[0])
        else:

            def combine_pattern(x):
                p1 = re.findall(r"/([^/\s]+)", "/" + x)
                p2 = re.findall(r" (\w+)$", x)
                if p2:
                    p2 = p2[-1]
                    return [f"{p} {p2}" for p in p1]
                else:
                    return p1
                

            x = [t for types in map(combine_pattern, x) for t in types]
        return x

    x = re.split(r"/([^/:]+):", "/" + x.text)
    holders, types = x[1::2], x[2::2]
    types = map(parse_types, types)
    return {"holder_and_type": dict(zip(holders, types))}


def effective_date_factory(x):
    return {"effective_date": x.text or ""}


def ata_chapter_factory(x):
    return {"ata_chapter": x.text}


def issued_by_factory(x):
    country_to_association = {"US": "FAA", "EU": "EASA"}
    return {"issued_by": country_to_association.get(x.text, x.text)}


def attachments_factory(x):
    return {
        "at_href": next(
            filter(
                lambda x: x.endswith("pdf"),
                map(lambda x: x.find("uri").text, x.findall("attachment")),
            )
        )
    }


def request_items(*args):
    b_xml = request_xml(*args)
    if b_xml is None:
        return []

    s_xml = b_xml.decode("ascii", errors="ignore")
    return parse_xml(s_xml)


def parse_xml(s_xml):
    def xml_factory(elem):
        if elem.tag == "ad_class":
            return category_factory(elem)
        if elem.tag == "ad_number":
            return number_factory(elem)
        if elem.tag == "issue_date":
            return issue_date_factory(elem)
        if elem.tag == "subject":
            return subject_factory(elem)
        if elem.tag == "type_designation":
            return type_designation_factory(elem)
        if elem.tag == "effective_date":
            return effective_date_factory(elem)
        if elem.tag == "ata_chapter":
            return ata_chapter_factory(elem)
        if elem.tag == "issued_by":
            return issued_by_factory(elem)
        if elem.tag == "attachments":
            return attachments_factory(elem)
        else:
            return None

    s_xml = html.unescape(s_xml)
    s_xml = s_xml.replace("â", "-")  # Dirty fix

    publications = []

    try:
        root = ET.fromstring(s_xml)
    except ET.ParseError as e:
        logging.exception(e)
        return []

    for child in root:
        p = {}
        for item in child:
            p.update(xml_factory(item))
        publications.append(p)

    return publications


def request_xml(days: int = None):
    days = days or get_default_value("LAST_X_DAYS", int)
    url = get_default_value("WEBADDRESS")
    data = {
        "fi_action": "advanced",
        "fi_date_start": (date.today() - timedelta(days=days)).isoformat(),
    }
    try:
        r = requests.post(url, data=data)
        r = requests.get(
            url + "?format=xml&r=500", cookies={"PHPSESSID": r.cookies["PHPSESSID"]}
        )
        if r.status_code == requests.codes.ok:
            return r.content
    except Exception as e:
        logging.exception(e)
        return None
