from cerberus import Validator

from settings import change_settings, get_default_value


def validate(item: dict) -> bool:
    return Validator(allow_unknown=True).validate(item, get_default_value("FILTER"))


def _forbid(key: str, value: str, schema: dict) -> dict:
    """Adds 'value' to the list 'forbidden' of 'key' in the specified 'schema'.
    If the 'key' refers to a list, the 'value' will be added to the 'forbidden' of the list's schema.
    See: https://docs.python-cerberus.org/en/stable/validation-rules.html#forbidden
    See: https://docs.python-cerberus.org/en/stable/validation-rules.html#schema-list

    Args:
        key (str): Must be a valid key in schema
        value (str): Value to forbid
        schema (dict): cerberus validation schema

    Returns:
        dict: Updated 'schema'
    """
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


def _allow(key: str, value: str, schema: dict) -> dict:
    """Removes 'value' from the list 'forbidden' of 'key' in the specified 'schema'.
    If the 'key' refers to a list, the 'value' will be removed from the 'forbidden' of the list's schema.
    See: https://docs.python-cerberus.org/en/stable/validation-rules.html#forbidden
    See: https://docs.python-cerberus.org/en/stable/validation-rules.html#schema-list

    Args:
        key (str): Must be a valid key in schema
        value (str): Value to allow
        schema (dict): cerberus validation schema

    Returns:
        dict: Updated 'schema'
    """
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
