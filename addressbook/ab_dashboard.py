"""This module contains DashboardBox class used for displaying AdressBook objects in table form"""

from addressbook.ab_windows.person_window import *
from addressbook.ab_helpers import *

import tkinter.messagebox
import tkinter.font as tkfont


class DashboardBox(object):
    """Class used for displaying AdressBook objects in table form"""

    col_names = ["name", "surname", "email", "phone", "city", "streetname", "streetnumber", "birthday",
                 "year", "month", "day", "id"]

    def __init__(self, abook, master):

        self.master = master

        self.data_list = []
        self.grab_data(abook)

        self.container = None
        self.tree = None
        self.abook = abook  # AddressBook object
        self.menu = None

        self.create_widgets(self.master)
        self.create_tree()
        self.create_menu()

    def create_widgets(self, master):

        self.container = ttk.Frame(master)
        self.container.pack(fill="both", expand=1)

        self.tree = ttk.Treeview(self.container, columns=self.col_names, show="headings")
        self.tree["displaycolumns"] = tuple(range(8))
        vscr = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        hscr = ttk.Scrollbar(self.container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vscr.set, xscrollcommand=hscr.set)

        self.tree.grid(column=0, row=0, sticky="nsew")
        vscr.grid(column=1, row=0, sticky="ns")
        hscr.grid(column=0, row=1, sticky="ew")

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Return>", self.modify_entry)
        self.tree.bind("<Button-3>", self.popup)
        self.tree.bind("<Delete>", self.remove_entry)
        self.tree.bind("<Home>", self.on_home)
        self.tree.bind("<End>", self.on_end)
        self.tree.bind("<Control-a>", self.select_all)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

    def create_tree(self):

        for col in self.col_names:
            name = col.replace("n", " n") if col in ("streetname", "streetnumber") else col
            head_width = tkfont.Font().measure(col)
            self.tree.heading(col, text=name.title(),
                              command=lambda c=col: self.sort_by(c, 0))

            self.tree.column(col, width=head_width, minwidth=head_width)

        for indx, item in enumerate(self.data_list):
            if indx % 2 == 0:
                i_tag = "even"
            else:
                i_tag = "odd"

            self.tree.insert("", "end", values=item, tags=(i_tag,))

            for ix, val in enumerate(item):
                col_width = tkfont.Font().measure(str(val))
                if self.tree.column(self.col_names[ix], "width") < col_width:
                    self.tree.column(self.col_names[ix], width=col_width, minwidth=col_width)

        # alternate colors of rows
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#fffdc1")

    def grab_data(self, abook):
        """Grab data from AddressBook item"""

        if len(abook) == 0:
            self.data_list = []
        else:
            for item in abook:
                self.data_list.append([item.__getattribute__(c) for c in self.col_names])

    def sort_by(self, col, order):
        """Sort data table by columns in either ascending or descending order"""

        data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        data.sort(key=lambda x: (x[0] == "None", int(x[0]) if x[0].isdigit() else x[0]), reverse=order)

        for i, item in enumerate(data):
            self.tree.move(item[1], '', i)
        self.tree.heading(col, command=lambda c=col:
            self.sort_by(c, not order))

        self.change_row_colors()    # reload rows' colors

    def change_row_colors(self):
        """Reload rows' colors"""

        children = self.tree.get_children()

        for i, iid in enumerate(children):
            if i % 2 == 0:
                self.tree.item(iid, tags=("even",))
            else:
                self.tree.item(iid, tags=("odd",))

    def create_menu(self):

        self.menu = tk.Menu(self.master, background="#fefdca", foreground="black",
               activebackground="#fcb040", activeforeground="black")
        self.menu.add_command(label="Modify Entry", command=self.modify_entry)
        self.menu.add_command(label="Remove Entry", command=self.remove_entry)

    def modify_entry(self, event=None):
        """Modify attributes of a Person object in AddressBook"""

        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")

        person_window = PersonWindow(self.master, self.abook, self.tree, values)

        # modified values for Person's attributes (if False, Person object will be removed)
        new_values = person_window.result

        # object in AddressBook corresponding to the chosen Treeview item
        abook_item = person_window.abook_item

        if new_values is False:
            self.remove_entry(abook_item, item=item)
        elif isinstance(new_values, dict):
            for col in new_values:
                self.tree.set(item, col, new_values[col])

    def on_double_click(self, event=None):
        """On double click, lauch the window for Person attributes modification"""

        if self.tree.selection():
            self.modify_entry()

    def on_end(self, event=None):
        """When 'End' key is pressed, focus on the last Treeview item"""

        last_item = self.tree.get_children()[-1]
        self.tree.selection_set(last_item)
        self.tree.see(last_item)

    def on_home(self, event=None):
        """When 'Home' key is pressed, focus on the first Treeview item"""

        first_item = self.tree.get_children()[0]
        self.tree.selection_set(first_item)
        self.tree.see(first_item)

    def popup(self, event=None):
        """Create a popup menu (launched on right click)"""

        iid = self.tree.identify_row(event.y)
        self.tree.selection_set(iid)
        self.menu.post(event.x_root, event.y_root)

    def remove_entry(self, abook_item=None, event=None, item=None):
        """Remove Person object from AddressBook"""

        if item is None:
            item = self.tree.selection()[0]

            # 'id' value of Person object
            item_id = self.tree.item(item, "values")[-1]

            # object in AddressBook corresponding to the chosen Treeview item (found by Person.id)
            abook_item = search_base(self.abook, id=int(item_id))[0]

        ask = tkinter.messagebox.askyesno("Remove Entry", "Do you want to remove this entry?")
        if ask:
            self.abook.remove(abook_item)
            self.tree.delete(item)
            self.change_row_colors()    # reload rows' colors

    def select_all(self, event=None):
        """Select all Treeview items"""

        self.tree.selection_set(self.tree.get_children())
