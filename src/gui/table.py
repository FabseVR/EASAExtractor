import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER

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
    "Subject": {"column": {"width": 200, "minwidth": 70, "anchor": "w", "stretch": True}},
    "Approval Holders / Type Designation": {
        "column": {"width": 200, "minwidth": 140, "anchor": "w", "stretch": True}
    },
    "Effective Date": {
        "text": "Eff. Date",
    },
}


def create_table(master, table_args, row_args):
    table = ttk.Treeview(
        master,
        columns=tv_columns,
        show="headings",
        selectmode="browse",
        column=list(tv_columns.values()),
        **table_args,
    )
    load_column_params(table)
    insert_rows(table, **row_args)

    def tv_select_event(event):
        iid = table.focus()
        is_checked = CHECKER(table.item(iid)["values"][0])
        table.set(iid, column="Checked", value=~is_checked)

    table.bind("<<TreeviewSelect>>", tv_select_event)

    return table


def load_column_params(table):
    for c in table["columns"]:
        c_params = column_params.get(c, {})

        c_heading = c_params.get("text", c)
        table.heading(c, text=c_heading, anchor=CENTER)

        d_column = {}
        c_column = c_params.get("column", {})
        d_column.update(**column_params["default"]["column"])
        d_column.update(**c_column)
        table.column(c, **d_column)


def insert_rows(table, relevant_items, ignored_items):
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
                    values.items(), key=lambda x: list(tv_columns.keys()).index(x[0])
                )
            )
            table.insert(parent="", index=offset + i, values=values)

    insert_loop(relevant_items, CHECKER.CHECKED)
    insert_loop(ignored_items, CHECKER.UNCHECKED, len(relevant_items))
