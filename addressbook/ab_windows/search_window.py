import tkinter.messagebox
import tkinter.simpledialog

import addressbook.ab_dashboard
from addressbook.ab_windows.files_window import *
from addressbook.ab_windows.other_windows import *


class SearchWindow(object):
    """Class that creates a window for searching through address book"""

    def __init__(self, parent, abook):

        self.parent = None
        parent.update_idletasks()

        self.abook = abook
        self.dashboard = None

        self.top = tk.Toplevel(parent)
        self.top.focus_set()
        self.top.transient()
        self.top.title("Search")
        self.top.resizable(width=False, height=False)
        self.top.minsize(width=800, height=250)

        self.body_container = None
        self.body(self.top)

        self.search_criteria = {"name": None, "surname": None, "email": None, "phone": None,
                       "birthday": None, "year": None, "month": None, "day": None, "city": None,
                       "streetname": None, "streetnumber": None}

        self.entries = [e for e in self.body_container.grid_slaves() if isinstance(e, tk.Entry)]

    def body(self, master):

        ttk.Label(master, text="Choose searching criteria:").pack(side="top",
                                                                 anchor="nw",
                                                                 padx=8, pady=4)

        self.body_container = ttk.Frame(master)
        self.body_container.pack(side="left", anchor="nw", padx=8, pady=4)

        self.create_entries(self.body_container)

        self.buttons(self.body_container)

        self.create_dashboard(self.body_container)

    def buttons(self, master):

        w = ttk.Button(master, text="Search", width=10, command=self.ok, default="active")
        w.grid(row=3, column=3, padx=5, pady=10)
        w = ttk.Button(master, text="Cancel", width=10, command=self.cancel)
        w.grid(row=3, column=4, padx=5, pady=10)

        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)

    def cancel(self, event=None):

        self.top.destroy()

    def create_dashboard(self, master, abook=None):

        if abook is None:
            abook = []

        container = ttk.Frame(master)
        container.grid(row=4, column=0, columnspan=8, sticky="nswe", pady=3)

        self.dashboard = addressbook.ab_dashboard.DashboardBox(abook, container)

    def create_entries(self, container):

        ttk.Label(container, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
        e_name = KeywordEntry(container, "name", width=20)
        e_name.grid(row=0, column=1, padx=10, pady=2)

        ttk.Label(container, text="Surname:").grid(row=0, column=2, sticky="w", pady=2)
        e_surname = KeywordEntry(container, "surname", width=20)
        e_surname.grid(row=0, column=3, padx=10, pady=2)

        ttk.Label(container, text="Email:").grid(row=0, column=4, sticky="w", pady=2)
        e_email = KeywordEntry(container, "email", width=20)
        e_email.grid(row=0, column=5, padx=10, pady=2)

        ttk.Label(container, text="Phone:").grid(row=0, column=6, sticky="w", pady=2)
        e_phone = KeywordEntry(container, "phone", width=20)
        e_phone.grid(row=0, column=7, padx=10, pady=2)

        ttk.Label(container, text="Birthday:").grid(row=1, column=0, sticky="w", pady=2)
        e_birthday = KeywordEntry(container, "birthday", width=20)
        e_birthday.grid(row=1, column=1, padx=10, pady=2)

        ttk.Label(container, text="Year of birth:").grid(row=1, column=2, sticky="w", pady=2)
        e_year = KeywordEntry(container, "year", width=20)
        e_year.grid(row=1, column=3, padx=10, pady=2)

        ttk.Label(container, text="Month of birth:").grid(row=1, column=4, sticky="w", pady=2)
        e_month = KeywordEntry(container, "month", width=20)
        e_month.grid(row=1, column=5, padx=10, pady=2)

        ttk.Label(container, text="Day of birth:").grid(row=1, column=6, sticky="w", pady=2)
        e_day = KeywordEntry(container, "day", width=20)
        e_day.grid(row=1, column=7, padx=10, pady=2)

        ttk.Label(container, text="City:").grid(row=2, column=0, sticky="w", pady=2)
        e_city = KeywordEntry(container, "city", width=20)
        e_city.grid(row=2, column=1, padx=10, pady=2)

        ttk.Label(container, text="Street name:").grid(row=2, column=2, sticky="w", pady=2)
        e_street1 = KeywordEntry(container, "streetname", width=20)
        e_street1.grid(row=2, column=3, padx=10, pady=2)

        ttk.Label(container, text="Street number:").grid(row=2, column=4, sticky="w", pady=2)
        e_street2 = KeywordEntry(container, "streetnumber", width=20)
        e_street2.grid(row=2, column=5, padx=10, pady=2)

    def get_search_criteria(self):

        self.search_criteria.clear()
        for e in self.entries:
            data = e.get()
            if len(data) != 0:
                self.search_criteria[e.keyword] = data

    def ok(self, event=None):

        try:
            self.get_search_criteria()

            found = self.search_tree(self.abook)
            self.dashboard.tree.destroy()
            self.create_dashboard(self.body_container, abook=found)
            if found is None:
                tkinter.messagebox.showinfo("No results found", "No results found.", parent=self.top)

            self.search_criteria = dict.fromkeys(self.search_criteria, None)
        except WrongInput as ex:
            tkinter.messagebox.showinfo("Wrong input", ex, parent=self.top)

    def search_tree(self, abook):

        found = []

        for ix, item in enumerate(self.search_criteria.items()):
            pair_to_search = {item[0]: item[1]}
            if ix == 0:
                found = search_base(abook, **pair_to_search)
            else:
                found = search_base(found, **pair_to_search)
            if isinstance(found, Person):
                found = [found]
            elif found is None:
                break

        return found
