from datetime import date
import os

from settings import get_default_value

def generate_csv(item_dict: dict):
    pattern = get_default_value("PATTERN")
    csv_out = ""
    for v in item_dict.values():
        v['holder_and_type'] = "; ".join(
            map(lambda x: f"{x[0]}: ({'+ '.join(x[1])})", v['holder_and_type'].items()))
        line = ",".join([v.get(k, "") or "" for k in pattern.split(',')]) + "\n"

        csv_out += line
    return csv_out


def write_csv(csv_body: str, path: str = None):
    path = path or get_default_value("ROOT_FOLDER")
    filename = date.today().isoformat()+".csv"
    with open(os.path.join(path, filename), "w+") as fd:
        fd.write(csv_body)
