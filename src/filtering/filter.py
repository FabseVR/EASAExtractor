from cerberus import Validator

from settings import change_settings, get_default_value


def validate(item: dict):
    return Validator(allow_unknown=True).validate(item, get_default_value("FILTER"))


def _forbid(key, value, schema):
    if schema[key].get("type") == "list":
        s = schema[key]["schema"]
    else:
        s = schema[key]
    if not value in s["forbidden"]:
        s["forbidden"].append(value)
    return schema


def forbid(key, value):
    schema = _forbid(key, value, get_default_value("FILTER"))
    change_settings("FILTER", schema)


def _allow(key, value, schema):
    if schema[key].get("type") == "list":
        s = schema[key]["schema"]
    else:
        s = schema[key]
    if value in s["forbidden"]:
        s["forbidden"].remove(value)
    return schema


def allow(key, value):
    schema = _allow(key, value, get_default_value("FILTER"))
    change_settings("FILTER", schema)
