from addressbook.ab_abook import *
from addressbook.ab_converters import *
from addressbook.ab_dashboard import *
from addressbook.ab_windows.add_window import *
from addressbook.ab_windows.files_window import *
from addressbook.ab_windows.other_windows import *
from addressbook.ab_windows.save_file_window import *
from addressbook.ab_windows.search_window import *
from addressbook.ab_windows.sort_window import *
from addressbook.ab_windows.view_window import *

import os
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.ttk as ttk


class App(object):

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("AddressBook 0.1")

        self.main_menu = None
        self.file_menu = None
        self.edit_menu = None
        self.view_menu = None
        self.build_menu()

        self.abook = None   # address book (object of AddressBook class)

        self.dashboard = None

        style = ttk.Style()
        style.theme_settings("vista", {
            "Treeview": {
                "map": {
                    "background": [("focus", "#383a56")],
                    "foreground": [("focus", "white"),
                                   ("!disabled", "black")]
                }
            },
            "Treeview.Heading": {
                "map": {
                    "foreground": [("!disabled", "#312f44")],
                }
            },
            "TButton": {
                "configure": {"padding": 4}
            }
        })
        style.theme_use("vista")

        self.root.minsize(width=800, height=300)
        self.root.configure(bg="#121435")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Control-o>", self.open_addressbook)
        self.root.bind("<Control-n>", self.create_new_addressbook)

        self.root.mainloop()

    def build_menu(self):

        self.main_menu = tk.Menu(self.root)
        self.root.configure(menu=self.main_menu)

        # File menu
        self.file_menu = tk.Menu(self.main_menu, background="#fefdca", foreground="black",
                                    activebackground="#fcb040", activeforeground="black")
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New            Ctrl+N", command=self.create_new_addressbook)
        self.file_menu.add_command(label="Open          Ctrl+O", command=self.open_addressbook)
        self.file_menu.add_command(label="Save", command=self.save, state="disabled")
        self.file_menu.add_command(label="Save As       Ctrl+S", command=self.save_as, state="disabled")
        self.file_menu.add_command(label="Quit", command=self.on_closing)

        # Edit menu
        self.edit_menu = tk.Menu(self.main_menu, background="#fefdca", foreground="black",
                                    activebackground="#fcb040", activeforeground="black")
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Add New Entry           F2", command=self.add_new_entry, state="disabled")
        self.edit_menu.add_command(label="Remove All Entries     F3", command=self.remove_all, state="disabled")

        # Search option
        self.main_menu.add_command(label="Search", command=self.search, state="disabled")

        # Sorting option
        self.main_menu.add_command(label="Sort", command=self.sort_data, state="disabled")

        # View menu
        self.view_menu = tk.Menu(self.main_menu, background="#fefdca", foreground="black",
                                    activebackground="#fcb040", activeforeground="black")
        self.main_menu.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Display Columns        F6", command=self.display_cols, state="disabled")

    def add_new_entry(self, event=None):
        """Add a new entry to the address book"""

        AddWindow(self.root, self.abook, self.dashboard.tree)

    def display_cols(self):
        """Specify columns to display in the dashboard"""

        w = self.root.winfo_width() - 15

        view_window = ViewWindow(self.root)

        if view_window.result:
            if len(view_window.result) > 0:
                self.dashboard.tree["displaycolumns"] = view_window.result
                col_len = len(self.dashboard.tree["displaycolumns"])
                for c in self.dashboard.tree["displaycolumns"]:
                    self.dashboard.tree.column(c, width=w // col_len)

            # no columns chosen - dashboard remains unchanged
            else:
                tkinter.messagebox.showinfo("", "At least one column must be selected.")
        else:
            tkinter.messagebox.showinfo("", "At least one column must be selected.")

    def create_new_addressbook(self, event=None):
        """Create a new address book"""

        self.refresh_app(abook=AddressBook())

        # 'Save' option is not allowed for address book that has not been saved yet
        self.file_menu.entryconfig("Save", state="disabled")

    def on_closing(self):

        if self.dashboard is not None:
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

    def open_addressbook(self, event=None):
        """Open an existing address book"""

        open_window = FilesWindow(self.root, title="Open AddressBook")

        fname = open_window.result  # filename
        fformat = open_window.fformat   # file extension

        types = [".pkl", ".pickle", ".json"]    # available extensions: .pkl, .pickle, .json

        if not fname:
            pass

        else:

            try:
                if os.path.getsize(fname) == 0:
                    raise EmptyFile
                elif fformat not in types:
                    raise FormatError

                self.abook = open_base(fformat, fname)

                self.abook.filename = fname

                self.refresh_app(self.abook)

                self.file_menu.entryconfig("Save", state="active")

                self.root.title("{} - AddressBook 0.1".format(os.path.basename(fname)))

            except FileNotFoundError:
                answer = tkinter.messagebox.askyesno("File Error",
                                                     "No such file. Do you want to create a new AddressBook?")
                if answer == "yes":
                    self.refresh_app(abook=AddressBook())
                    self.file_menu.entryconfig("Save", state="active")
                    tkinter.messagebox.showinfo("New AddressBook", "New AddressBook created.")
                else:
                    tkinter.messagebox.showinfo("No AddressBook", "No AddressBook created.")

            except EmptyFile as ex:
                tkinter.messagebox.showerror("File Error", message=ex)
            except FormatError as ex:
                tkinter.messagebox.showerror("Format Error", message=ex)

    def refresh_app(self, abook):
        """Called while creating new address books or opening existing ones."""

        # destroy previous dashboard if there was one
        if self.dashboard is not None:
            self.dashboard.container.destroy()

        self.abook = abook
        self.dashboard = DashboardBox(self.abook, master=self.root)

        self.file_menu.entryconfig("Save As       Ctrl+S", state="active")
        self.main_menu.entryconfig("Search", state="active")
        self.main_menu.entryconfig("Sort", state="active")
        self.edit_menu.entryconfig("Add New Entry           F2", state="active")
        self.edit_menu.entryconfig("Remove All Entries     F3", state="active")
        self.view_menu.entryconfig("Display Columns        F6", state="active")

        self.root.bind("<Control-s>", self.save_as)
        self.root.bind("<F2>", self.add_new_entry)
        self.root.bind("<F3>", self.remove_all)
        self.root.bind("<F4>", self.search)
        self.root.bind("<F5>", self.sort_data)
        self.root.bind("<F6>", self.display_cols)

    def remove_all(self, event=None):
        """Remove all entries from the address book"""

        ask = tkinter.messagebox.askyesno("Remove All Entries", "Do you want to remove all entries?")
        if ask:
            self.abook.clear()
            for item in self.dashboard.tree.get_children():
                self.dashboard.tree.delete(item)
            self.refresh_app(self.abook)

    def save(self):
        """Save changes to already existing address book (without specifying the filename)"""

        if self.abook.filename.endswith(".pkl") or self.abook.filename.endswith(".pickle"):
            self.abook.pickle_changes()
        elif self.abook.filename.endswith(".json"):
            self.abook.json_changes()

        FileSavedMessage()

    def save_as(self, event=None):

        save_window = SaveFileWindow(self.root, title="Save AddressBook")

        fname = save_window.result  # filename (None when saving with a default name)
        fformat = save_window.fformat

        # user chooses not to save any changes
        if not fname and not save_window.is_default:
            return

        # save address book to filepath/filename chosen by user or save with a default name
        elif fformat == ".xls":
            to_excel(self, fname)
        else:
            self.abook.save_base(filename=fname, fileformat=fformat)
            
        FileSavedMessage()
        self.root.title("{} - AddressBook 0.1".format(os.path.basename(fname)))

    def search(self, event=None):

        SearchWindow(self.root, self.abook)

    def sort_data(self, event=None):

        sort_window = SortWindow(self.root)
        result = sort_window.result  # sorting category (item's attribute) and order

        if result is not None:
            category, order = sort_window.result
            self.dashboard.sort_by(category, order)
