import tkinter.messagebox
import tkinter.simpledialog

from addressbook.ab_windows.files_window import *


class SaveFileWindow(FilesWindow):
    """Class that creates a window for saving address book files"""

    def __init__(self, parent, title="Save Address Book"):

        self.is_default = False     # True if the file will be saved with default name (current date and time)

        # available extensions for saving files (with corresponding names that will be displayed in menu)
        self.format_map = {"Python pickle (.pkl)": ".pkl",
                           "Python pickle (.pickle)": ".pickle",
                           "JSON file (.json)": ".json",
                           "Excel file (.xls)": ".xls"}
        self.format_var = tk.StringVar()
        self.format_var.set("Python pickle (.pkl)")

        super().__init__(parent, fname=os.getcwd(), title=title)

    def apply(self):

        self.result = self.e.get()

        types = re.compile(r".pkl|.pickle|.json$")

        # if filename entered by user contains file extension (.pkl, .pickle or .json)
        if re.search(types, self.result):
            self.fformat = os.path.splitext(self.result)[1]
        # if user entered only filename, the extension will be the one chosen from menu or the default one (.pkl)
        else:
            self.fformat = self.format_map[self.format_var.get()]

    def body(self, master):

        self.resizable(width=False, height=False)

        self.minsize(width=450, height=350)

        ttk.Label(master, text=self.msg).grid(row=0, column=0, pady=2, sticky="nwse")

        self.e = ttk.Entry(master, width=50, textvariable=self.e_var)
        self.e.grid(row=0, column=1, padx=3)

        ttk.Label(master, text="Choose format: ").grid(row=1, column=1, pady=2, sticky="nwse")

        format_menu = ttk.OptionMenu(master, self.format_var, "Python pickle (.pkl)", *self.format_map.keys(),
                                     command=self.on_left_click_menu)
        format_menu.grid(row=1, column=1, padx=3, sticky="ne")

        self.create_widgets(self.fname)
        self.create_tree()
        self.create_menu()

        self.tree.unbind("<Double-1>")

        return self.e

    def create_widgets(self, fname):

        super().create_widgets(fname)

    def buttons(self, master):

        box = ttk.Frame(master)

        w1 = ttk.Button(box, text="Save", width=10, command=self.ok, default="active")
        w1.pack(side="left", padx=5, pady=5)
        w2 = ttk.Button(box, text="Save As Default Name", width=20, command=self.save_default, default="active")
        w2.pack(side="left", padx=5, pady=5)
        w3 = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w3.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(row=4, pady=5)

    def ok(self, event=None):

        self.apply()

        if len(self.result) == 0:
            tkinter.messagebox.showinfo("No filename chosen",
                                        "You have to choose a filename.")

        elif os.path.isdir(self.result):
            os.chdir(self.result)
            self.files_container.destroy()
            self.create_widgets(self.result)
            self.create_tree()
            self.buttonbox()
        elif os.path.isfile(self.result):
            if self.result in [self.tree.set(child, 0) for child in self.tree.get_children()]:
                ask = tkinter.messagebox.askyesno("Replace file", "A file with this name already exists.\n"
                                                                  "Do you want to replace it?")
                if ask:
                    self.cancel()
            else:
                self.cancel()
        else:
            self.cancel()

    def on_left_click_menu(self, event=None):
        """Update data in entry box when option from menu has been chosen"""

        data = self.e.get()
        if len(data) > 0:
            filename, file_format = os.path.splitext(data)
            self.e_var.set(filename + self.format_map[self.format_var.get()])

    def save_default(self):

        self.is_default = True
        self.cancel()
