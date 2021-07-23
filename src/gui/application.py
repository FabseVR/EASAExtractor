import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, HORIZONTAL, LEFT, RIGHT, TOP, VERTICAL, X, Y

from gui.table import create_table

class Application(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.scroll_x = tk.Scrollbar(self, orient=HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self, orient=VERTICAL)

        self.frame_btns = tk.Frame(self)
        self.btn_settings = tk.Button(self.frame_btns, text="Settings")

        self.btn_confirm = tk.Button(self.frame_btns, text="Confirm")

        self.tv_table = create_table(
            self,
            {"yscrollcommand": self.scroll_y.set, "xscrollcommand": self.scroll_x.set},
            kwargs
        )


        self.scroll_x.config(command=self.tv_table.xview)
        self.scroll_y.config(command=self.tv_table.yview)

        self.btn_settings.pack(side=LEFT)
        self.btn_confirm.pack(side=RIGHT)
        self.frame_btns.pack(side=BOTTOM)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.tv_table.pack(side=TOP, expand=True, fill=BOTH)

    def set_btn_settings_command(self, command):
        self.btn_settings.config(command=command)