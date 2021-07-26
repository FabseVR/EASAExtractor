from datetime import date
import os

from settings import get_default_value


def generate_csv(publications: list):
    def fill_pattern(pattern: str, subpatterns: dict, publication: dict):
        out = ""

        for p in pattern.split(",")[:-1]:
            terminal = publication.get_as_str(p)
            if p in subpatterns:
                # If a subpattern has the attribute condition,
                # it will be replaced only if condition's value matches the pattern name
                if publication.get(subpatterns[p].get('condition'), p) != p:
                    out += ","*subpatterns[p]["p"].count(",")
                else:
                    out += fill_pattern(subpatterns[p]["p"],
                                        subpatterns[p].get("subpatterns", {}), publication)
            # Replace Terminals by their corresponding values
            elif terminal is not None:
                #Drop commas to avoid conflicts with csv format
                escaped_terminal = terminal.replace(",", "")    
                out += f"{escaped_terminal},"
            # Interpret other values as Literals
            else:
                out += f"{p},"

        return out

    pattern_json = get_default_value("PATTERN")
    out = ""

    for p in publications:
        out += fill_pattern(pattern_json["p"], pattern_json["subpatterns"], p) + "\n"
    return out


def write_csv(publications: list, path: str = None):
    path = path or get_default_value("ROOT_FOLDER")
    filename = date.today().isoformat()+".csv"
    filepath = os.path.join(path, filename)
    i = 1
    while os.path.isfile(filepath):
        filename = date.today().isoformat()+f"_{i}.csv"
        filepath = os.path.join(path, filename)
        i += 1
    csv_body = generate_csv(publications)
    open(filepath, "x+").write(csv_body)
    return filename
