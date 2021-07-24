import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER
from gui.filtermenu import FilterMenu

from gui.frame import CHECKER

tv_columns = {
    "checked": "Checked",
    "number": "Number",
    "category": "Category",
    "revision": "Revision",
    "issued_by": "Issued By",
    "issue_date": "Issue Date",
    "subject": "Subject",
    "holder_and_type": "Approval Holders / Type Designation",
    "effective_date": "Effective Date",
}
tv_columns_inv = {v: k for k, v in tv_columns.items()}

column_params = {
    "default": {
        "column": {"anchor": CENTER, "stretch": False, "width": 90, "minwidth": 90}
    },
    "Checked": {
        "text": "",
        "column": {"width": 20, "stretch": 0},
    },
    "Category": {
        "text": "Type",
        "column": {"width": 60, "minwidth": 60},
    },
    "Revision": {
        "text": "Rev.",
        "column": {"width": 40, "minwidth": 40},
    },
    "Issued By": {"text": "By", "column": {"minwidth": 50, "width": 50}},
    "Subject": {
        "column": {"width": 200, "minwidth": 70, "anchor": "w", "stretch": True}
    },
    "Approval Holders / Type Designation": {
        "column": {"width": 200, "minwidth": 140, "anchor": "w", "stretch": True}
    },
    "Effective Date": {
        "text": "Eff. Date",
    },
}


class Table(ttk.Treeview):
    def __init__(self, master, item_dict, filter_func, table_args):
        super().__init__(
            master,
            columns=tv_columns,
            show="headings",
            selectmode="browse",
            column=list(tv_columns.values()),
            **table_args,
        )
        self.item_dict = item_dict
        self.filter_func = filter_func
        self.relevant_items = filter_func(item_dict)
        self.filtermenu = FilterMenu(self, self.reload_rows)

        self.load_column_params()
        self.insert_rows()

        def tv_select_event(event):
            focus = self.focus()
            if focus == self.identify_row(event.y):
                is_checked = CHECKER(self.item(focus)["values"][0])
                self.set(focus, column="Checked", value=~is_checked)

        def show_filtermenu(event):
            iid = self.identify_row(event.y)
            col = self.identify_column(event.x)
            if iid and col:
                self.focus(iid)
                self.selection_set(iid)

                col_id = int(col[1:]) - 1
                if col_id == 0:
                    return

                checked = CHECKER(self.item(iid)["values"][0])
                row_id = self.item(iid)["values"][1]
                key = tv_columns_inv[self["columns"][col_id]]

                self.filtermenu.popup(
                    (event.x_root, event.y_root),
                    key=key,
                    value=self.item_dict[row_id][key],
                    checked=bool(checked),
                )

        self.bind("<ButtonRelease-1>", tv_select_event)
        self.bind("<ButtonRelease-3>", show_filtermenu)

    def load_column_params(self):
        for c in self["columns"]:
            c_params = column_params.get(c, {})

            c_heading = c_params.get("text", c)
            self.heading(c, text=c_heading, anchor=CENTER)

            d_column = {}
            c_column = c_params.get("column", {})
            d_column.update(**column_params["default"]["column"])
            d_column.update(**c_column)
            self.column(c, **d_column)

    def insert_rows(self):
        def insert_loop(item_dict, checked, offset=0):
            for i, v in enumerate(item_dict.values()):
                values = {k: v.get(k, "") for k in tv_columns.keys()}
                values["checked"] = checked
                values["holder_and_type"] = " ".join(
                    map(
                        lambda x: f"{x[0]}: ({', '.join(x[1])})",
                        values["holder_and_type"].items(),
                    )
                )
                # Order by column index
                _, values = zip(
                    *sorted(
                        values.items(),
                        key=lambda x: list(tv_columns.keys()).index(x[0]),
                    )
                )
                self.insert(parent="", index=offset + i, values=values)

        insert_loop(
            {k: v for k, v in self.item_dict.items() if k in self.relevant_items},
            CHECKER.CHECKED,
        )
        insert_loop(
            {k: v for k, v in self.item_dict.items() if k not in self.relevant_items},
            CHECKER.UNCHECKED,
            len(self.relevant_items),
        )

    def reload_rows(self):
        self.delete(*self.get_children())
        self.relevant_items = self.filter_func(self.item_dict)
        self.insert_rows()
