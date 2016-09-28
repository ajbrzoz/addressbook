import tkinter.messagebox
import tkinter.simpledialog

from addressbook.ab_windows.files_window import *


class SaveFileWindow(FilesWindow):
    """Class that creates a window for saving address book files"""

    def __init__(self, parent, title="Save Address Book"):

        self.is_default = False     # True if the file will be saved with default name (current date and time)

        super().__init__(parent, fname=os.getcwd(), title=title)

    def create_widgets(self, fname):

        super().create_widgets(fname)
        self.tree.bind("<Double-1>", self.ok)

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

        box.grid(row=3, pady=5)

    def ok(self, event=None):

        self.apply()

        if os.path.isdir(self.result):
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

    def save_default(self):

        self.is_default = True
        self.cancel()
