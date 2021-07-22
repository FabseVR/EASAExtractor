from datetime import date
import os

PATTERN = "number,category,revision,issue_date,issued_by,,,holder_and_type"
DEFAULT_PATH = 'data/root'

def generate_csv(item_dict: dict):
    csv_out = ""
    for v in item_dict.values():
        v['holder_and_type'] = "; ".join(
            map(lambda x: f"{x[0]}: ({'+ '.join(x[1])})", v['holder_and_type'].items()))
        line = ",".join([v.get(k, "") for k in PATTERN.split(',')]) + "\n"

        csv_out += line
    return csv_out


def write_csv(csv_body: str, path: str = DEFAULT_PATH):
    filename = date.today().isoformat()+".csv"
    with open(os.path.join(path, filename), "w+") as fd:
        fd.write(csv_body)
