import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, LEFT, RIGHT, W, X
from gui.application import Application
from gui.settings import Settings


class ApplicationWrapper(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.frame_btns = tk.Frame(self)

        self.lbl_status = tk.Label(self.frame_btns, width=100, anchor=W)
        self.btn_r = tk.Button(self.frame_btns)
        self.btn_c = tk.Button(self.frame_btns)

        self.application = Application(self, **kwargs)
        self.settings = Settings(self)

        def show_application():
            self.settings.forget()
            self.application.reload_application(command_back=show_settings)
            self.application.pack(expand=True, fill=BOTH)

        def show_settings():
            self.application.forget()
            self.settings.reload_settings(command_back=show_application)
            self.settings.pack(expand=True, fill=BOTH)

        self.lbl_status.pack(side=LEFT, padx=10, pady=5)
        self.btn_c.pack(side=LEFT, padx=10)
        self.btn_r.pack(side=RIGHT, padx=10)

        self.frame_btns.pack(side=BOTTOM, fill=X)

        show_application()

    def set_btn_c(self, **kwargs):
        self.btn_c.configure(**kwargs)

    def set_btn_r(self, **kwargs):
        self.btn_r.configure(**kwargs)

    def set_status(self, value):
        self.lbl_status.configure(text="Status: " + value)


def run_app(confirm_func, **kwargs):
    root = tk.Tk()
    root.geometry("1800x600")

    root.style = ttk.Style()

    # color bug fix (ttk::treeview tag configure not working since upgrade to 8.6.9)
    # Source: https://core.tcl-lang.org/tk/tktview/509cafafae48cba46796e12d0503a335f0dcfe0b
    def fixed_map(option):
        # Returns the style map for 'option' with any styles starting with
        # ("!disabled", "!selected", ...) filtered out

        # style.map() returns an empty list for missing options, so this should
        # be future-safe
        return [
            elm
            for elm in root.style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")
        ]

    root.style.map(
        "Treeview",
        foreground=fixed_map("foreground"),
        background=fixed_map("background"),
    )

    def confirm_wrapper(*args, set_status):
        def wrapper_status(*args):
            set_status(*args)
            root.update()

        confirm_func(*args, wrapper_status)
        root.after(1000, root.destroy)

    app = ApplicationWrapper(root, confirm_func=confirm_wrapper, **kwargs)
    app.pack(expand=True, fill=BOTH)
    root.mainloop()
