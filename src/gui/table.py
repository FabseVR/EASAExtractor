import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER
from gui.filtermenu import FilterMenu
from gui.checkbox import CHECKBOX

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
    def __init__(self, master, publications, filter_func, table_args):
        super().__init__(
            master,
            columns=tv_columns,
            show="headings",
            selectmode="browse",
            column=list(tv_columns.values()),
            **table_args,
        )
        self.publications = publications
        self.filter_func = filter_func
        self.relevant_items = filter_func(publications)
        self.filtermenu = FilterMenu(self, self.reload_rows)

        self.load_column_params()
        self.insert_rows()

        self.tag_configure("UNCHECKED", foreground="#666")

        def tv_select_event(event):
            focus = self.focus()
            if focus and focus == self.identify_row(event.y):
                checked = ~CHECKBOX(self.set(focus, "Checked"))
                self.set(focus, column="Checked", value=checked)
                self.item(focus, tags=checked.as_tag())

        def show_filtermenu(event):
            iid = self.identify_row(event.y)
            col = self.identify_column(event.x)
            if iid and col:
                self.focus(iid)
                self.selection_set(iid)

                col_id = int(col[1:]) - 1
                if col_id == 0:
                    return

                row_id = self.set(iid, "Number")
                key = tv_columns_inv[self["columns"][col_id]]

                self.filtermenu.popup(
                    (event.x_root, event.y_root),
                    items=list(filter(lambda x: x.number == row_id, self.publications))[
                        0
                    ].get_menu_values(key),
                )

        self.bind("<ButtonRelease-1>", tv_select_event)
        self.bind("<ButtonRelease-3>", show_filtermenu)

    def load_column_params(self):
        def sort_by_column(column, reverse=False):
            l = sorted(
                [
                    (
                        ~CHECKBOX(self.set(iid, "Checked"))
                        if reverse
                        else CHECKBOX(self.set(iid, "Checked")),
                        self.set(iid, column),
                        iid,
                    )
                    for iid in self.get_children()
                ],
                reverse=reverse,
            )
            for i, (_, _, k) in enumerate(l):
                self.move(k, "", i)

            self.heading(
                column, command=lambda _c=column: sort_by_column(_c, not reverse)
            )

        for c in self["columns"]:
            c_params = column_params.get(c, {})

            c_heading = c_params.get("text", c)

            self.heading(
                c,
                text=c_heading,
                anchor=CENTER,
                command=lambda _c=c: sort_by_column(_c),
            )

            d_column = {}
            c_column = c_params.get("column", {})
            d_column.update(**column_params["default"]["column"])
            d_column.update(**c_column)
            self.column(c, **d_column)

    def insert_rows(self):
        def insert_loop(publications, checked, offset=0):
            for i, p in enumerate(publications):
                values = {k: p.get_as_str(k) for k in tv_columns.keys()}
                values["checked"] = checked

                # Order by column index
                _, values = zip(
                    *sorted(
                        values.items(),
                        key=lambda x: list(tv_columns.keys()).index(x[0]),
                    )
                )
                self.insert(
                    parent="",
                    index=offset + i,
                    values=values,
                    tags=[checked.as_tag()],
                )

        insert_loop(
            [p for p in self.publications if p.number in self.relevant_items],
            CHECKBOX.CHECKED,
        )
        insert_loop(
            [p for p in self.publications if p.number not in self.relevant_items],
            CHECKBOX.UNCHECKED,
            len(self.relevant_items),
        )

    def reload_rows(self):
        self.delete(*self.get_children())
        self.relevant_items = self.filter_func(self.publications)
        self.insert_rows()

    def get_selected_publications(self):
        selected_items = list(
            map(
                lambda x: self.set(x, "Number"), self.tag_has(CHECKBOX.CHECKED.as_tag())
            )
        )
        return [p for p in self.publications if p.number in selected_items]
