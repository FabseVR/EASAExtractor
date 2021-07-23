from datetime import date
import os

from settings import get_default_value


def generate_csv(item_dict: dict):
    def fill_pattern(pattern: str, subpatterns: dict, terminals: dict):
        out = ""

        for p in pattern.split(",")[:-1]:
            if p in subpatterns:
                # If a subpattern has the attribute condition,
                # it will be replaced only if condition's value matches the pattern name
                if terminals.get(subpatterns[p].get('condition'), p) != p:
                    out += ","*subpatterns[p]["p"].count(",")
                else:
                    out += fill_pattern(subpatterns[p]["p"],
                                        subpatterns[p].get("subpatterns", {}), terminals)
            # Replace Terminals by their corresponding values
            elif p in terminals:
                out += f"{terminals[p]},"
            # Interpret other values as Literals
            else:
                out += f"{p},"

        return out

    pattern_json = get_default_value("PATTERN")
    out = ""

    for item in item_dict.values():
        item['holder_and_type'] = " ".join(
            map(lambda x: f"{x[0]}: ({';'.join(x[1])})", item['holder_and_type'].items()))
        out += fill_pattern(pattern_json["p"],
                            pattern_json["subpatterns"], item) + "\n"

    return out


def write_csv(csv_body: str, path: str = None):
    path = path or get_default_value("ROOT_FOLDER")
    filename = date.today().isoformat()+".csv"
    with open(os.path.join(path, filename), "w+") as fd:
        fd.write(csv_body)
