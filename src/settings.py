import jstyleson, sys, os

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_PATH, 'DATA')

SETTINGS = os.path.join(BASE_PATH, 'settings.json')

def load_settings(path=SETTINGS):
    global settings
    settings = jstyleson.load(open(SETTINGS))


def change_settings(key, value):
    global settings
    settings[key] = value
    jstyleson.dump(settings, open(SETTINGS, "w"))

def get_default_value(key, type=None):
    global settings

    if key.startswith("P_"):
        return os.path.join(BASE_PATH, settings.get(key, ""))

    if type:
        return type(settings.get(key))
    return settings.get(key)


settings = {}
load_settings()
