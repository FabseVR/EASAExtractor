import tkinter as tk
from tkinter import ttk
from tkinter.constants import ANCHOR, BOTH, CENTER, HORIZONTAL, LEFT, VERTICAL, X, Y
from enum import Enum

class CHECKER(Enum):
    CHECKED = "\u2612"
    UNCHECKED = "\u2610"

    def __invert__(self):
        return CHECKER.UNCHECKED if self else CHECKER.CHECKED

    def __bool__(self):
        return self == CHECKER.CHECKED

    def __str__(self):
        return self.value

    def __lt__(self, b):
        return self == CHECKER.CHECKED and b == CHECKER.UNCHECKED

    def as_tag(self):
        return "CHECKED" if bool(self) else "UNCHECKED"

def create_gui(relevant_items, ignored_items):
    relevant_selection = []

    W,H = 1600,400
    root = tk.Tk()
    root.geometry(f"{W}x{H}")

    scrollbar = tk.Scrollbar(root)
    scrollbar2 = tk.Scrollbar(root, orient=HORIZONTAL)
    def confirm_selection(selection):
        _, s = zip(*filter(lambda x: CHECKER(x[0]) == CHECKER.CHECKED, map(lambda x: tv_relevant.item(x)['values'][:2], tv_relevant.get_children())))
        selection.extend(s)
        root.destroy()
        
    btn_confirm = tk.Button(text="Confirm & Close", command=lambda : confirm_selection(relevant_selection))
    btn_confirm.pack(side="bottom")

    scrollbar.pack(side="right", fill="y")
    scrollbar2.pack(side="bottom", fill="x")
    tv_relevant = ttk.Treeview(root, columns=('Checked', 'Number', 'Category', 'Revision', 'Issued By', 'Issue Date', 'Subject', 'Approval Holders / Type Designation', 'Effective Date'), show='headings', yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set, selectmode='browse')
    params ={
        'default': {
            'column': {'anchor': CENTER, 'stretch': False, 'width': 90}
        },
        'Checked': {
            'text': '',
            'column': {'width':20, 'stretch':0},
        },
        'Category': {
            'text': 'Type',
            'column': {'width': 60, 'minwidth':60},
        },
        'Revision': {
            'text': 'Rev.',
            'column': {'width': 40, 'minwidth': 40},
        },
        'Issued By': {
            'text': 'By',
            'column': {'minwidth': 50, 'width': 50}
        },
        'Subject': {
            'column': {'width': 200, 'anchor': 'w', 'stretch': True}
        },
        'Approval Holders / Type Designation': {
            'column': {'width': 200, 'anchor': 'w', 'stretch': True}
        },
        'Effective Date': {
            'text': 'Eff. Date',
        }

    }
    for c in tv_relevant['columns']:
        c_params = params.get(c, {})
        c_heading = c_params.get('text', c)
        tv_relevant.heading(c, text=c_heading, anchor=CENTER)
        d_column = {}
        d_column.update(**params['default']['column'])
        c_column = c_params.get('column', {})
        d_column.update(**c_column)
        tv_relevant.column(c, **d_column)

    def treeview_select(event):
        iid = tv_relevant.focus()
        is_checked = CHECKER(tv_relevant.item(iid)['values'][0])
        tv_relevant.set(iid, column='Checked', value=~is_checked)
    tv_relevant.bind('<<TreeviewSelect>>', treeview_select)

    scrollbar.config(command=tv_relevant.yview)
    scrollbar2.config(command=tv_relevant.xview)
    for i, v in enumerate(relevant_items.values()):
        tv_relevant.insert(parent='', index=i, values=[CHECKER.CHECKED, *list(v.values())[:-1]])
    for i, v in enumerate(ignored_items.values()):
        tv_relevant.insert(parent='', index=i, values=[CHECKER.UNCHECKED, *list(v.values())[:-1]])

    tv_relevant.pack(expand=True, fill=BOTH)
    root.mainloop()
    return relevant_selection