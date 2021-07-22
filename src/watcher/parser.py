from typing import Dict, Tuple
import requests
import re
import bs4
from bs4 import BeautifulSoup
from datetime import date, timedelta

web_address = "https://ad.easa.europa.eu/search/advanced/result/"
local_file = "tests/data/test.html"


def request_items(days: int) -> str:
    """Send POST request to the EASA website to retrieve recent publications

    Args:
        days (int): Days from today to determine the 'filter by date' start

    Returns:
        str: Response as HTML
    """
    payload = {
        "fi_action": "advanced",
        "fi_date_start": (date.today() - timedelta(days=days)).isoformat(),
    }
    r = requests.post(web_address, data=payload)
    if r.status_code == requests.codes.ok:
        return r.text
    return ""


def request_local_items(days: int) -> str:
    """Dummy function, that returns a static example file. For testing purposes only!

    Args:
        days (int): Not relevant, just to keep the format

    Returns:
        str: Response as HTML
    """
    with open(local_file) as fd:
        return fd.read()


def parse_response(response: str):
    """Parses the table included into the HTML file into a dict, containing all relevant information.

    Args:
        response (str): HTML Response

    Returns:
        dict: Parsed table with number as key.

    Example: 
    {
        '2021-0174': {
            'category': 'AD',
            'revision': '0', 
            'issued_by': 'EU', 
            'issue_date': '2021-07-21', 
            'subject': 'Rotorcraft Flight Manual – Supplements / One-Engine Inoperative Performance Limitations – Amendment', 
            'holder_and_type': {'AIRBUS HELICOPTERS': ['SA 330 / AS 332 / EC 225']},
            'effective_date': '2021-08-04', 
            'attachement': 'https://ad.easa.europa.eu/blob/EASA_AD_2021_0174.pdf/AD_2021-0174_1'
        },
        ...
    }
    """
    def default_str_factory(val: str) -> str:
        """Basic string manipulation. Strips unnecessary padding."""
        return re.sub(r"\s+", r" ", val.strip())

    def default_factory(val: bs4.element.Tag) -> str:
        return default_str_factory(val.text)

    def number_factory(number: bs4.element.Tag) -> Tuple[str, str]:
        """Splits the actual number into number and revision. 
        It checks the following rules:
        1) If the number starts with a letter (isalpha), the number starts with a country tag. 
        Remove everything until the first occurence of '-'.
        2) If the second last character is a 'R', the number ends with a revision number.
        Remove the last two charactes and return the last char as revision number.


        Args:
            number (bs4.element.Tag): Table Column 'Number' <td>

        Returns:
            Tuple[str, str]: Number, Revision as described above
        """
        number = default_factory(number)
        if number[0].isalpha():
            _, _, number = number.partition('-')
        if number[-2] == 'R':
            return number[:-2], number[-1]
        return number, '0'

    def issued_by_factory(issued_by: bs4.element.Tag):
        """Transfers the actual issued_by value (<img>) into the corresponding string.
        TODO: Map EU -> EASA and US -> FAA

        Args:
            issued_by (bs4.element.Tag): Table Column 'Issued by' <td>

        Returns:
            str: The country code ('US', 'EU', ...)
        """
        return issued_by.find('img')['alt']

    def subject_factory(subject: bs4.element.Tag) -> Tuple[str, str]:
        """Splits the actual subject into subject and a category tag. 
        If the subject defaults to a description with no tags, the subject will stay unchanged and the category is "AD".
        Otherwise, the tag will be the third child (index 2) and the description will be the fourth.

        Args:
            subject (bs4.element.Tag): Table Column 'Subject' <td>

        Returns:
            Tuple[str, str]: Subject, Category as defined above.
            Category can be any value from the range ["AD", "EAD", "PAD", "SIB", "PSD", "SD"]
        """
        if len(subject.contents) == 1:
            return default_factory(subject), "AD"
        return default_str_factory(subject.contents[2]), subject.contents[1]['alt']

    def holder_and_types_factory(holder_and_types: bs4.element.Tag) -> Dict[str, list]:
        """Transfers the tree structure of the Approval Holder tag into a dict, 
        where holder is the key and the types are the values.

        Args:
            holder_and_types (bs4.element.Tag): Table Column 'Approval Holder / Type Designation'

        Returns:
            Dict[str, dict]: (holder, type(s))-dictionary
        """
        tree = holder_and_types.find_all('li', class_='tc_holder')
        holder_dict = {
            default_str_factory(h.contents[0]): [
                default_factory(t) for t in h.find_all('li')
            ] for h in tree
        }
        return holder_dict

    def attachment_factory(attachments: bs4.element.Tag) -> str:
        """Extracts the href link to the (first) attached pdf-file.

        Args:
            attachments (bs4.element.Tag): Table Column 'Attachement'

        Returns:
            str: HTTP-link of the attachement.
        """
        return attachments.find('li', class_='file_pdf').a['href']

    response_dict = {}

    table = BeautifulSoup(response, 'html.parser').find(
        'table', class_='ad-list')
    if not table:
        return {}
    for row in table.find_all('tr'):
        values = row.find_all('td')
        if len(values) != 7:
            continue

        number, revision = number_factory(values[0])
        issued_by = issued_by_factory(values[1])
        issue_date = default_factory(values[2])
        subject, category = subject_factory(values[3])
        holder_and_type = holder_and_types_factory(values[4])
        effective_date = default_factory(values[5])
        attachement = attachment_factory(values[6])

        response_dict[number] = {
            'category': category,
            'revision': revision,
            'issued_by': issued_by,
            'issue_date': issue_date,
            'subject': subject,
            'holder_and_type': holder_and_type,
            'effective_date': effective_date,
            'attachement': attachement
        }
    return response_dict
