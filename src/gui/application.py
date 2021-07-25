import tkinter as tk
from tkinter.constants import (
    BOTH,
    BOTTOM,
    HORIZONTAL,
    LEFT,
    RIGHT,
    TOP,
    VERTICAL,
    W,
    X,
    Y,
)

from gui.table import Table


class Application(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.scroll_x = tk.Scrollbar(self, orient=HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self, orient=VERTICAL)

        confirm_func = kwargs["confirm_func"]
        del kwargs["confirm_func"]

        self.tv_table = Table(
            self,
            **kwargs,
            table_args={
                "yscrollcommand": self.scroll_y.set,
                "xscrollcommand": self.scroll_x.set,
            },
        )

        self.frame_btns = tk.Frame(self)

        self.lbl_status = tk.Label(self.frame_btns, width=100, anchor=W)
        status = f"{len(self.tv_table.publications)} publications retrieved, {len(self.tv_table.get_selected_publications())} considered relevant"
        self.set_status(status)
        self.btn_settings = tk.Button(self.frame_btns, text="Settings")
        self.btn_confirm = tk.Button(
            self.frame_btns,
            text="Confirm",
            command=lambda: confirm_func(
                self.tv_table.get_selected_publications(), set_status=self.set_status
            ),
        )

        self.scroll_x.config(command=self.tv_table.xview)
        self.scroll_y.config(command=self.tv_table.yview)

        self.lbl_status.pack(side=LEFT, padx=10, pady=5)
        self.btn_confirm.pack(side=LEFT, padx=10)
        self.btn_settings.pack(side=RIGHT, padx=10)

        self.frame_btns.pack(side=BOTTOM, fill=X)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.tv_table.pack(side=TOP, expand=True, fill=BOTH)

    def set_btn_settings_command(self, command):
        self.btn_settings.config(command=command)

    def reload_application(self):
        self.tv_table.reload_rows()

    def set_status(self, value):
        self.lbl_status.configure(text="Status: " + value)
