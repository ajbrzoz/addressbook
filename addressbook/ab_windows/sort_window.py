import tkinter as tk

from addressbook.ab_windows.popup_window import *


class SortWindow(PopupWindow):
    """Class that creates a window for sorting data in address book"""

    def __init__(self, parent, title="Sort"):

        self.sort_category = tk.StringVar()
        self.sort_category.set("name")

        self.sort_order = tk.IntVar()

        super().__init__(parent, title)

    def body(self, master):

        self.resizable(width=False, height=False)

        ttk.Label(master, text="Choose sorting criteria:").grid(row=0, sticky="w", columnspan=4, padx=10, pady=5)
        self.create_criteria_entries(master)

        ttk.Label(master, text="Choose sorting order:").grid(row=4, sticky="w", columnspan=4, padx=10, pady=5)
        self.create_order_entries(master)

    def create_criteria_entries(self, master):

        cb_name = ttk.Radiobutton(master, text="Name", variable=self.sort_category, value="name")
        cb_name.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        cb_surname = ttk.Radiobutton(master, text="Surname", variable=self.sort_category, value="surname")
        cb_surname.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        cb_email = ttk.Radiobutton(master, text="E-mail", variable=self.sort_category, value="email")
        cb_email.grid(row=1, column=2, padx=10, pady=2, sticky="w")

        cb_phone = ttk.Radiobutton(master, text="Phone", variable=self.sort_category, value="phone")
        cb_phone.grid(row=1, column=3, padx=10, pady=2, sticky="w")

        cb_birthday = ttk.Radiobutton(master, text="Birthday", variable=self.sort_category, value="birthday")
        cb_birthday.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        cb_year = ttk.Radiobutton(master, text="Year of birth", variable=self.sort_category, value="year")
        cb_year.grid(row=2, column=1, padx=10, pady=2, sticky="w")

        cb_month = ttk.Radiobutton(master, text="Month of birth", variable=self.sort_category, value="month")
        cb_month.grid(row=2, column=2, padx=10, pady=2, sticky="w")

        cb_day = ttk.Radiobutton(master, text="Day of birth", variable=self.sort_category, value="day")
        cb_day.grid(row=2, column=3, padx=10, pady=2, sticky="w")

        cb_city = ttk.Radiobutton(master, text="City", variable=self.sort_category, value="city")
        cb_city.grid(row=3, column=0, padx=10, pady=2, sticky="w")

        cb_street1 = ttk.Radiobutton(master, text="Street name", variable=self.sort_category, value="streetname")
        cb_street1.grid(row=3, column=1, padx=10, pady=2, sticky="w")

        cb_street2 = ttk.Radiobutton(master, text="Street number", variable=self.sort_category, value="streetnumber")
        cb_street2.grid(row=3, column=2, padx=10, pady=2, sticky="w")

    def create_order_entries(self, master):

        rb_asc = ttk.Radiobutton(master, text="Ascending", variable=self.sort_order, value=0)
        rb_asc.grid(row=5, column=0, padx=10, pady=2, sticky="w")
        rb_desc = ttk.Radiobutton(master, text="Descending", variable=self.sort_order, value=1)
        rb_desc.grid(row=5, column=1, padx=10, pady=2, sticky="w")

    def apply(self):

        final_category = self.sort_category.get()
        final_order = self.sort_order.get()
        self.result = (final_category, final_order)
