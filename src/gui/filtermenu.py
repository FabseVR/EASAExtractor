import tkinter as tk
from tkinter.constants import END

from filtering.filter import allow, forbid, validate


class FilterMenu(tk.Menu):
    def __init__(self, master, callback):
        super().__init__(master, tearoff=0)
        self.callback = callback

    def popup(self, pos, items):
        def wrapper(func, *args):
            func(*args)
            self.callback()

        self.delete(0, END)

        for key, val, valid in items:
            label = ("Ignore: " if valid else "Allow: ") + val
            command = forbid if valid else allow
            self.add_command(label=label, command=lambda _c=command, _k=key, _v=val: wrapper(lambda: _c(_k, _v)))

        self.tk_popup(*pos)
