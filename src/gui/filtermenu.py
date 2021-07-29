import tkinter as tk
from tkinter.constants import END
from typing import List, Tuple

from filtering.filter import allow, forbid


class FilterMenu(tk.Menu):
    """A mutable FilterPopupMenu."""

    def __init__(self, master, callback):
        super().__init__(master, tearoff=0)
        self.callback = callback

    def popup(self, pos: Tuple[int, int], items: List[Tuple[str, str, bool]]):
        """Creates a PopupMenu based on 'items'.
        Selecting an item will allow/forbid the value for the given key during validation.

        Args:
            pos (Tuple[int, int]): Position of the popup menu (global coordinates regarding root)
            items (List[Tuple[str, str, bool]]): List of (key, value, valid),
            stateing whether 'value' is a valid value for 'key' or not.
        """

        def wrapper(func, *args):
            func(*args)
            self.callback()

        self.delete(0, END)

        for key, val, valid in items:
            label = ("Ignore: " if valid else "Allow: ") + val
            command = forbid if valid else allow
            self.add_command(
                label=label,
                command=lambda _c=command, _k=key, _v=val: wrapper(lambda: _c(_k, _v)),
            )

        self.tk_popup(*pos)
