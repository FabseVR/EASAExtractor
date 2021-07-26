import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH
from gui.application import Application
from gui.settings import Settings

class ApplicationWrapper(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.application = Application(self, **kwargs)
        self.settings = Settings(self)

        def show_application():
            self.settings.forget()
            self.application.reload_application()
            self.application.pack(expand=True, fill=BOTH)

        def show_settings():
            self.application.forget()
            self.settings.reload_settings()
            self.settings.pack(expand=True, fill=BOTH)

        self.application.set_btn_settings_command(show_settings)
        self.settings.set_btn_back_command(show_application)

        self.application.pack(expand=True, fill=BOTH)

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
        return [elm for elm in root.style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

    root.style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))

    def confirm_wrapper(*args,set_status):
        def wrapper_status(*args):
            set_status(*args)
            root.update()
        confirm_func(*args, wrapper_status)
        root.after(1000, root.destroy)

    app = ApplicationWrapper(root, confirm_func=confirm_wrapper, **kwargs)
    app.pack(expand=True, fill=BOTH)
    root.mainloop()
