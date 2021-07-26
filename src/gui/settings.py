import tkinter as tk
from tkinter import filedialog
from tkinter.constants import BOTH, END, NSEW, RIGHT, Y
from settings import change_settings, get_default_value
import json


class ScrollableText(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.scrollbar = tk.Scrollbar(self)
        self.text = tk.Text(self, yscrollcommand=self.scrollbar.set, **kwargs)

        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text.pack(expand=True, fill=BOTH)

    def insert(self, start, value):
        self.text.insert("0.0", value)

    def delete(self, *args):
        self.text.delete("0.0", END)

    def get(self):
        return json.loads(self.text.get("0.0", END))


setting_params = {
    "ROOT_FOLDER": {
        "text": "Working Directory:",
        "type_val": tk.Entry,
        "insert_val": lambda: get_default_value("ROOT_FOLDER"),
    },
    "WEBADDRESS": {
        "text": "Website:",
        "type_val": tk.Entry,
        "insert_val": lambda: get_default_value("WEBADDRESS"),
    },
    "LAST_X_DAYS": {
        "text": "Track publications of last X days:",
        "type_val": tk.Entry,
        "insert_val": lambda: get_default_value("LAST_X_DAYS"),
    },
    "PATTERN": {
        "text": "CSV-Pattern:",
        "type_val": ScrollableText,
        "insert_val": lambda: json.dumps(get_default_value("PATTERN"), indent=2),
        "weight": 1,
    },
    "FILTER": {
        "text": "Filter:",
        "type_val": ScrollableText,
        "insert_val": lambda: json.dumps(get_default_value("FILTER"), indent=2),
        "weight": 1,
    },
}


class Settings(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.labels = []
        self.entries = {}
        self.actions = []

        for i, (k, v) in enumerate(setting_params.items()):
            label = tk.Label(self, text=v["text"])
            label.grid(row=i, column=0, sticky=NSEW, padx=10, pady=5)
            self.labels.append(label)

            entry = v["type_val"](self)
            entry.grid(
                row=i,
                column=1,
                rowspan=1 + ("action" in v),
                sticky=NSEW,
                padx=10,
                pady=5,
            )
            self.entries[k] = entry

            self.grid_rowconfigure(i, weight=v.get("weight", 0))

        def change_dir(val):
            self.entries["ROOT_FOLDER"].delete(0,END)
            self.entries["ROOT_FOLDER"].insert(0, val)

        self.btn_select_dir = tk.Button(self, text="Choose", command=lambda : change_dir(filedialog.askdirectory()))
        self.btn_select_dir.grid(row=0, column=2, padx=10, pady=5)

        self.grid_columnconfigure(1, weight=1)

        self.reload_settings()

        def save_settings():
            for k, v in self.entries.items():
                change_settings(k, v.get())

        self.btn_save = tk.Button(self, text="Save", command=save_settings)
        self.btn_back = tk.Button(self, text="Back")

        self.btn_back.grid(row=i + 1, column=1)
        self.btn_save.grid(row=i + 1, column=2)

    def set_btn_back_command(self, command):
        self.btn_back.config(command=command)

    def reload_settings(self):
        for k, v in self.entries.items():
            v.delete(0,END)
            v.insert(0, setting_params[k]["insert_val"]())