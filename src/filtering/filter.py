from cerberus import Validator

from settings import change_settings, get_default_value

def validate_items(item_dict: dict):
    return [
        k
        for k, v in item_dict.items()
        if validate_item(v)
    ]

def validate_item(item: dict):
    return Validator(allow_unknown=True).validate(item, get_default_value("FILTER"))


def forbid_value(key, value):
    schema = get_default_value("FILTER")
    if not value in schema[key]["forbidden"]:
        schema[key]["forbidden"].append(value)
        change_settings("FILTER", schema)


def allow_value(key, value):
    schema = get_default_value("FILTER")
    if value in schema[key]["forbidden"]:
        schema[key]["forbidden"].remove(value)
        change_settings("FILTER", schema)