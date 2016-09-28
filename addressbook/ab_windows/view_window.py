import tkinter as tk

from addressbook.ab_windows.popup_window import *


class ViewWindow(PopupWindow):

    def __init__(self, parent, title="View"):

        self.keywords = ["name", "surname", "email", "phone", "city", "streetname", "streetnumber", "birthday"]
        self.cols = {k: tk.IntVar() for k in self.keywords}
        self.all_cols = tk.IntVar()

        super().__init__(parent, title)

    def body(self, master):

        self.resizable(width=False, height=False)

        ttk.Label(master, text="Choose columns to display:").grid(row=0, sticky="w", columnspan=4, padx=10, pady=5)

        self.create_criteria_entries(master)

        for c in self.cols:
            self.cols[c].set(1)

        self.all_cols.set(1)

    def create_criteria_entries(self, master):

        cb_name = ttk.Checkbutton(master, text="Name", variable=self.cols["name"])
        cb_name.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        cb_surname = ttk.Checkbutton(master, text="Surname", variable=self.cols["surname"])
        cb_surname.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        cb_email = ttk.Checkbutton(master, text="E-mail", variable=self.cols["email"])
        cb_email.grid(row=1, column=2, padx=10, pady=2, sticky="w")

        cb_phone = ttk.Checkbutton(master, text="Phone", variable=self.cols["phone"])
        cb_phone.grid(row=1, column=3, padx=10, pady=2, sticky="w")

        cb_city = ttk.Checkbutton(master, text="City", variable=self.cols["city"])
        cb_city.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        cb_street1 = ttk.Checkbutton(master, text="Street name", variable=self.cols["streetname"])
        cb_street1.grid(row=2, column=1, padx=10, pady=2, sticky="w")

        cb_street2 = ttk.Checkbutton(master, text="Street number", variable=self.cols["streetnumber"])
        cb_street2.grid(row=2, column=2, padx=10, pady=2, sticky="w")

        cb_birthday = ttk.Checkbutton(master, text="Birthday", variable=self.cols["birthday"])
        cb_birthday.grid(row=2, column=3, padx=10, pady=2, sticky="w")

        cb_all = ttk.Checkbutton(master, text="Choose all", variable=self.all_cols,
                                command=self.choose_all)
        cb_all.grid(row=3, column=0, padx=12, pady=2, sticky="w")

    def apply(self):

        self.result = [c for c in self.keywords if self.cols[c].get() == 1]

    def choose_all(self):
        """Select/unselect all columns"""

        for c in self.cols:
            self.cols[c].set(self.all_cols.get())
