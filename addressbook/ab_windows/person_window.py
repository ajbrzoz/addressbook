import tkinter.messagebox
import tkinter.simpledialog

from addressbook.ab_windows.add_window import *


class PersonWindow(AddWindow):
    """Class that creates a window for modifying attributes of objects in the address book and removing the objects"""

    def __init__(self, parent, abook, tree, values):

        self.values = values

        self.name_var, self.surname_var, self.email_var, self.phone_var = [tk.StringVar() for n in range(4)]
        self.birthday_var, self.city_var, self.street1_var, self.street2_var = [tk.StringVar() for n in range(4)]

        self.variables = [self.name_var, self.surname_var, self.email_var, self.phone_var,
                     self.city_var, self.street1_var, self.street2_var, self.birthday_var]

        self.abook = abook

        # object in AddressBook corresponding to the chosen Treeview item (found by Person.id)
        self.abook_item = search_base(self.abook, id=int(self.values[-1]))[0]

        super().__init__(parent, abook, tree, title="{} {}".format(self.values[0], self.values[1]))

    def body(self, master):

        super().body(master)

        for en, var, val in zip(self.entries, self.variables, self.values):
            en.configure(textvariable=var)
            var.set(val)

    def buttonbox(self):

        box = ttk.Frame(self)

        w = ttk.Button(box, text="Save changes", width=14, command=self.ok, default="active")
        w.pack(side="left", padx=5, pady=5)
        w = ttk.Button(box, text="Remove entry", width=14, command=self.remove_entry)
        w.pack(side="left", padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=14, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        self.result = {e.keyword: e.get() for e in self.entries}
        try:
            for keyword, val in self.result.items():
                if keyword in ["name", "surname", "email", "phone"] and not val:
                    raise WrongInput("The {} field cannot be empty".format(keyword.capitalize()))
                if val != "None":
                    setattr(self.abook_item, keyword, self.result[keyword])
            self.cancel()
        except WrongInput as ex:
            tkinter.messagebox.showinfo("Wrong input", str(ex))

    def remove_entry(self):
        self.result = False
        self.cancel()
