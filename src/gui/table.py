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
    def __init__(self, master, publications, filter_relevant, filter_open, table_args):
        super().__init__(
            master,
            columns=tv_columns,
            show="headings",
            selectmode="browse",
            column=list(tv_columns.values()),
            **table_args,
        )
        self.publications = publications
        self.filter_relevant = filter_relevant
        self.filter_open = filter_open
        self.open_items = filter_open(publications)
        self.relevant_items = filter_relevant(self.open_items)
        self.filtermenu = FilterMenu(self, self.reload_rows)

        self.load_column_params()
        self.insert_rows()

        self.tag_configure("UNCHECKED_OPEN", foreground="gray")
        self.tag_configure("UNCHECKED_CLOSED", foreground="#8DBD8D")
        self.tag_configure("CHECKED_CLOSED", foreground="#0DBD0D")

        def tv_select_event(event):
            focus = self.focus()
            if focus and focus == self.identify_row(event.y):
                checked = ~CHECKBOX[self.item(focus)["tags"][0]]
                self.set(focus, column="Checked", value=checked.as_icon())
                self.item(focus, tags=[checked])

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
            # Sort by value
            l = sorted(
                [
                    (
                        CHECKBOX[self.item(iid)["tags"][0]],
                        self.set(iid, column),
                        iid,
                    )
                    for iid in self.get_children()
                ],
                reverse=reverse,
                key=lambda x: x[1:],
            )
            # Keep order of checked/unchecked items
            l = sorted(l, key=lambda x: x[0])

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
                values["checked"] = checked.as_icon()

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
                    tags=[checked],
                )

        insert_loop(
            [p for p in self.publications if p in self.relevant_items],
            CHECKBOX.CHECKED_OPEN,
        )
        insert_loop(
            [
                p
                for p in self.publications
                if p not in self.relevant_items and p in self.open_items
            ],
            CHECKBOX.UNCHECKED_OPEN,
            len(self.relevant_items),
        )
        insert_loop(
            [p for p in self.publications if p not in self.open_items],
            CHECKBOX.UNCHECKED_CLOSED,
            len(self.open_items),
        )

    def reload_rows(self):
        self.delete(*self.get_children())
        self.open_items = self.filter_open(self.publications)
        self.relevant_items = self.filter_relevant(self.open_items)
        self.insert_rows()

    def get_selected_publications(self):
        selected_items = list(
            map(
                lambda x: self.set(x, "Number"),
                self.tag_has(CHECKBOX.CHECKED_OPEN)
                + self.tag_has(CHECKBOX.CHECKED_CLOSED),
            )
        )
        return [p for p in self.publications if p.number in selected_items]
