import tkinter as tk
from tkinter.constants import (
    BOTH,
    BOTTOM,
    HORIZONTAL,
    RIGHT,
    TOP,
    VERTICAL,
    X,
    Y,
)

from gui.table import Table


class Application(tk.Frame):
    """A horizontally and vertically scrollable Table"""

    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.scroll_x = tk.Scrollbar(self, orient=HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self, orient=VERTICAL)

        self.confirm_func = kwargs["confirm_func"]
        del kwargs["confirm_func"]

        self.tv_table = Table(
            self,
            **kwargs,
            table_args={
                "yscrollcommand": self.scroll_y.set,
                "xscrollcommand": self.scroll_x.set,
            },
        )

        status = f"{len(self.tv_table.publications)} publications retrieved, {len(self.tv_table.get_selected_publications())} considered relevant"
        self.master.set_status(status)

        self.scroll_x.config(command=self.tv_table.xview)
        self.scroll_y.config(command=self.tv_table.yview)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.tv_table.pack(side=TOP, expand=True, fill=BOTH)

    def reload(self, command_back):
        self.master.set_btn_c(
            text="Confirm",
            command=lambda: self.confirm_func(
                self.tv_table.get_selected_publications(),
                set_status=self.master.set_status,
            ),
        )
        self.master.set_btn_r(text="Settings", command=command_back)
        self.tv_table.reload_rows()
