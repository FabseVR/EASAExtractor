import re, os
from filtering.filter import validate

from settings import get_default_value

# PDF Parser
def parse_easa_pattern(text: str):
    foreign_ad, supersedure = None, None

    text = re.sub(r"\n(?=\S)", r"", text)
    # Returns key-value pairs for each occurence of ^key:value$
    kv = dict(re.findall(r"^ *([^:\n]+)\s*:\s*(.+)", text, re.MULTILINE))

    if "Foreign AD" in kv:
        if kv["Foreign AD"].lower() == "not applicable":
            foreign_ad = "None"
        else:
            foreign_ad = kv["Foreign AD"]

    if "Supersedure" in kv:
        supersedure = kv["Supersedure"]

    return foreign_ad, supersedure, foreign_ad and supersedure


def parse_faa_pattern(text: str):
    foreign_ad = None

    text = re.sub(r"\n(?=\S)", r"", text)
    kv = dict(re.findall(r"^\s*\([a-z]\) +(.+)\s+(.+)", text, re.MULTILINE))

    if "Affected ADs" in kv:
        if kv["Affected ADs"].lower() == "none.":
            foreign_ad = "None"
        else:
            foreign_ad = kv["Affected ADs"]

    return foreign_ad, None, foreign_ad is not None


class Publication:
    def __init__(
        self,
        number,
        category,
        revision,
        issued_by,
        issue_date,
        subject,
        holder_and_type,
        effective_date,
        at_href,
        **kwargs,
    ):
        self.number = number
        self.category = category
        self.revision = revision
        self.issued_by = issued_by
        self.issue_date = issue_date
        self.subject = subject
        self.holder_and_type = holder_and_type
        self.holder = list(self.holder_and_type.keys())
        self.types = [
            t for holder_types in self.holder_and_type.values() for t in holder_types
        ]
        self.effective_date = effective_date

        self.at_href = at_href
        self.at_name = None
        self._at_path = None

        self.foreign_ad = None
        self.supersedure = None

        self.folder = f"{self.issued_by} {self.category} {self.number}"

        if self.issued_by == "EASA":
            self.parse_pattern = parse_easa_pattern
        elif self.issued_by == "FAA":
            self.parse_pattern = parse_faa_pattern
        else:
            self.parse_pattern = lambda _: (None, None, True)

    @property
    def at_path(self):
        if not self.at_name:
            return None
        if not self._at_path:
            self._at_path = os.path.join(
                get_default_value("ROOT_FOLDER"), self.folder, self.at_name
            )
        return self._at_path

    def __eq__(self, x: object) -> bool:
        __ignored__ = ["parse_pattern"]
        for k, v in vars(self).items():
            if k in __ignored__:
                continue
            if v != x.get(k):
                return False
        return True

    def get(self, x, default=None):
        try:
            return self.__getattribute__(x)
        except AttributeError:
            return default

    def get_as_str(self, x, sep1=" ", sep2="; "):
        try:
            v = self.__getattribute__(x)
        except AttributeError:
            return

        if isinstance(v, dict):
            v = sep1.join(map(lambda x: f"{x[0]} ({sep2.join(x[1])})", v.items()))
        elif isinstance(v, list):
            v = sep2.join(v)
        elif v is None:
            v = ""
        elif type(v) != str:
            v = str(v)
        return v

    # UI FilterMenu
    def get_menu_values(self, x):
        value = self.get(x)
        out = []
        if not value:
            return
        if x == "holder_and_type":
            for k, v in value.items():
                out.append(("holder", k, validate({"holder": [k]})))
                out.extend([("types", t, validate({"types": [t]})) for t in v])
        else:
            out.append((x, value, validate({x: value})))
        return out
