import tkinter.messagebox
import tkinter.simpledialog

from addressbook.ab_windows.other_windows import *
from addressbook.ab_windows.popup_window import *


class AddWindow(PopupWindow):
    """Class that creates a window for adding new objects to the address book"""

    def __init__(self, parent, abook, tree, title="Add New Entry"):

        self.abook = abook
        self.tree = tree
        self.entries = None

        super().__init__(parent, title)

    def body(self, master):

        ttk.Label(master, text="Name: *").grid(row=0, column=0, sticky="w", pady=5)
        e_name = KeywordEntry(master, "name", width=20)
        e_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(master, text="Surname: *").grid(row=0, column=2, sticky="w", pady=5)
        e_surname = KeywordEntry(master, "surname", width=20)
        e_surname.grid(row=0, column=3, padx=10, pady=5)

        ttk.Label(master, text="Email: *").grid(row=1, column=0, sticky="w", pady=5)
        e_email = KeywordEntry(master, "email", width=20)
        e_email.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(master, text="Phone: *").grid(row=1, column=2, sticky="w", pady=5)
        e_phone = KeywordEntry(master, "phone", width=20)
        e_phone.grid(row=1, column=3, padx=10, pady=5)

        ttk.Label(master, text="Birthday:").grid(row=2, column=0, sticky="w", pady=5)
        e_birthday = KeywordEntry(master, "birthday", width=20)
        e_birthday.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(master, text="City:").grid(row=2, column=2, sticky="w", pady=5)
        e_city = KeywordEntry(master, "city", width=20)
        e_city.grid(row=2, column=3, padx=10, pady=5)

        ttk.Label(master, text="Street name:").grid(row=3, column=0, sticky="w", pady=5)
        e_street1 = KeywordEntry(master, "streetname", width=20)
        e_street1.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(master, text="Street number:").grid(row=3, column=2, sticky="w", pady=5)
        e_street2 = KeywordEntry(master, "streetnumber", width=20)
        e_street2.grid(row=3, column=3, padx=10, pady=5)

        ttk.Label(master, text="* This field must be filled in.").grid(row=4, sticky="w", columnspan=4, padx=5, pady=7)

        self.entries = [e_name, e_surname, e_email, e_phone, e_city, e_street1, e_street2, e_birthday]

    def apply(self):

        self.result = {e.keyword: e.get() for e in self.entries}

        try:
            for keyword in ["name", "surname", "email", "phone"]:
                if not self.result[keyword]:
                    raise WrongInput("The {} field cannot be empty".format(keyword.capitalize()))

            self.abook.add_new(self.result["name"], self.result["surname"],
                               self.result["email"], self.result["phone"])

            for keyword in ["birthday", "city", "streetname", "streetnumber"]:
                if self.result[keyword]:
                    setattr(self.abook[-1], keyword, self.result[keyword])

            new_name = self.result["name"].capitalize()
            new_surname = self.result["surname"].capitalize()
            tkinter.messagebox.showinfo("New item",
                                        "{0} {1} has been added to the base.".format(new_name, new_surname))
            self.refresh_tree(self.tree)

            self.cancel()

        except WrongInput as ex:
            tkinter.messagebox.showinfo("Wrong input", str(ex) + ". The item cannot be added.")

    def refresh_tree(self, tree):

        new_item = self.abook[-1]
        col_names = ["name", "surname", "email", "phone", "city", "streetname", "streetnumber", "birthday", "id"]

        data = [new_item.__getattribute__(c) for c in col_names]

        tree.insert('', 'end', values=data)

    def ok(self, event=None):
        self.apply()
