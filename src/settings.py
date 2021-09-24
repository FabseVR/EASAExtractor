import jstyleson, sys, os


def load_settings(path=None):
    global settings, constants, BASE_PATH, SETTINGS, CONSTANTS
    """
    if not path:
        if getattr(sys, "frozen", False):
            BASE_PATH = sys._MEIPASS
        else:
            BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        BASE_PATH = os.path.join(BASE_PATH, "DATA")
    else:
        BASE_PATH = path
    """
    BASE_PATH = path or os.path.expanduser("~/.easaextract/")

    SETTINGS = os.path.join(BASE_PATH, "settings.json")
    CONSTANTS = os.path.join(BASE_PATH, "constant.json")
    settings = jstyleson.load(open(SETTINGS))
    constants = jstyleson.load(open(CONSTANTS))


def change_settings(key, value):
    if key in settings:
        settings[key] = value
        jstyleson.dump(settings, open(SETTINGS, "w"))
    elif key in constants:
        constants[key] = value
        jstyleson.dump(constants, open(CONSTANTS, "w"))


def get_default_value(key, type=None):
    if key in constants:
        d = constants
    else:
        d = settings

    if key.startswith("P_"):
        return os.path.join(BASE_PATH, d.get(key, ""))

    if type:
        return type(d.get(key))
    return d.get(key)


settings = {}
constants = {}
load_settings()
