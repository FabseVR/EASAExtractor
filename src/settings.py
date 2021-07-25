import jstyleson

SETTINGS = 'data/settings.json'

def load_settings(path=SETTINGS):
    global settings
    with open(path) as fd:
        settings = jstyleson.load(fd)


def change_settings(key, value):
    global settings
    settings[key] = value
    with open(SETTINGS, "w") as fd:
        jstyleson.dump(settings, fd)


def get_default_value(key, type=None):
    global settings
    if type:
        return type(settings.get(key))
    return settings.get(key)


settings = {}
load_settings()
