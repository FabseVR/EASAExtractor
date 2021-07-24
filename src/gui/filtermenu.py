import tkinter as tk
from tkinter.constants import END

from filtering.filter import allow_value, forbid_value, validate_item, validate_items


class FilterMenu(tk.Menu):
    def __init__(self, master, callback):
        super().__init__(master, tearoff=0)
        self.callback = callback

    def popup(self, pos, key, value, checked):
        def add_command(key, value):
            print(key, value, {key: value})
            filter_state = validate_item({key: value})
            print(filter_state)
            label = ("Ignore: " if filter_state else "Allow: ") + value
            self.add_command(label=label, command=lambda: reload_filters(key, value, filter_state))

        def reload_filters(key, value, state):
            if state:
                forbid_value(key, value)
            else:
                allow_value(key, value)
            self.callback()

        self.delete(0, END)
        if key == "holder_and_type":
            for holder, v in value.items():
                add_command(key, holder)
                for type in v:
                    add_command(key, type)
        else:
            add_command(key, value)
        self.tk_popup(*pos)
