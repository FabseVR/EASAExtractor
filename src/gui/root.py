import tkinter as tk
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

    def confirm_wrapper(*args,set_status):
        def wrapper_status(*args):
            set_status(*args)
            root.update()
        confirm_func(*args, wrapper_status)
        root.after(1000, root.destroy)

    app = ApplicationWrapper(root, confirm_func=confirm_wrapper, **kwargs)
    app.pack(expand=True, fill=BOTH)
    root.mainloop()
