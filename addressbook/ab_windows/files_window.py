import glob
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox
import tkinter.simpledialog
from time import localtime, strftime

from addressbook.ab_helpers import *
from addressbook.ab_windows.popup_window import *


class FilesWindow(PopupWindow):
    """Class that creates a window for opening address book files"""

    def __init__(self, parent, title, fname=os.getcwd()):

        self.fname = fname
        self.directory = None
        self.filenames = []
        self.files_container = None
        self.lab = None
        self.lab_msg = None
        self.tree = None
        self.menu = None
        self.e_var = tk.StringVar()     # variable for filepath entry box

        self.fformat = tk.StringVar()   # file extension

        super().__init__(parent, title, msg="Enter a file path or filename: ")

    def apply(self):

        super().apply()
        self.fformat = os.path.splitext(self.result)[1]

    def body(self, master):

        self.resizable(width=False, height=False)

        self.minsize(width=450, height=350)

        ttk.Label(master, text=self.msg).grid(row=0, column=0, pady=2, sticky="nwse")

        self.e = ttk.Entry(master, width=50, textvariable=self.e_var)
        self.e.grid(row=0, column=1, padx=3)

        self.create_widgets(self.fname)
        self.create_tree()
        self.create_menu()

        return self.e

    def buttonbox(self):

        self.buttons(self.files_container)

    def buttons(self, master):

        box = ttk.Frame(master)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default="active")
        w.pack(side="left", padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(row=4, pady=5)

    def cancel(self, event=None):

        self.fname = None   # reset 'fname' attribute no matter whether entry box is empty or not
        super().cancel()

    def create_widgets(self, fname):

        if os.path.isdir(fname):
            self.directory = fname

        elif os.path.isfile(fname):
            self.directory = os.path.dirname(fname)

        self.lab_msg = "Current directory:   {}\n".format(self.directory)

        self.files_container = ttk.Frame(self)
        self.files_container.pack(side="bottom", fill="both", expand=1, padx=5)

        self.lab = ttk.Label(self.files_container, text=self.msg)
        self.lab.grid(column=0, row=1, sticky='w', pady=5)

        self.tree = ttk.Treeview(self.files_container, columns=["Filename", "Size", "Last modified"],
                                 show="headings")
        vscr = ttk.Scrollbar(self.files_container, orient="vertical", command=self.tree.yview)
        hscr = ttk.Scrollbar(self.files_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vscr.set, xscrollcommand=hscr.set)

        self.tree.grid(column=0, row=2, sticky="nsew")
        vscr.grid(column=1, row=2, sticky="ns")
        hscr.grid(column=0, row=3, sticky="ew")

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<ButtonRelease-1>", self.on_left_click)
        self.tree.bind("<Button-3>", self.popup)
        self.tree.bind("<Delete>", self.delete_file)

        self.files_container.grid_columnconfigure(0, weight=1)
        self.files_container.grid_rowconfigure(0, weight=1)

    def create_tree(self):

        types = ("*.pkl", "*.pickle", "*.json")
        for ftype in types:
            self.filenames.extend(glob.glob(os.path.join(self.directory, ftype)))

        if len(self.filenames) == 0:
            self.lab.config(text=self.lab_msg + "\nNo address book found in this location.")
        else:
            self.lab.config(text=self.lab_msg +
                                 "\n{} address books found in this location".format(len(self.filenames)))

            for col in ("Filename", "Size", "Last modified"):
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by(c, 0))
                self.tree.column(col, width=tkfont.Font().measure(col))

            for ix, name in enumerate(self.filenames):
                if ix % 2 == 0:
                    i_tag = "even"
                else:
                    i_tag = "odd"

                short_name = os.path.basename(name)
                size = human_size(os.stat(name).st_size)
                modified = strftime("%Y-%m-%d %H:%M", localtime(os.stat(name).st_mtime))
                self.tree.insert("", "end", values=(short_name, size, modified), tags=(i_tag,))

        # alternate colors of rows
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#fffdc1")

    def change_row_colors(self):

        children = self.tree.get_children()

        for i, iid in enumerate(children):
            if i % 2 == 0:
                self.tree.item(iid, tags=("even",))
            else:
                self.tree.item(iid, tags=("odd",))

    def create_menu(self):

        self.menu = tk.Menu(self.master, background="#fefdca", foreground="black",
               activebackground="#fcb040", activeforeground="black")
        self.menu.add_command(label="Open File", command=self.on_double_click)
        self.menu.add_command(label="Delete File", command=self.delete_file)

    def delete_file(self, event=None):
        """Delete selected file"""

        item = self.tree.selection()[0]
        fname = self.tree.item(item, "values")[0]
        ask = tkinter.messagebox.askyesno("Delete", "Do you want to delete this file?")
        if ask:
            os.unlink(fname)
            self.tree.delete(item)
            self.change_row_colors()  # reload rows' colors

    def ok(self, event=None):

        self.apply()
        if os.path.isdir(self.result):
            os.chdir(self.result)
            self.files_container.destroy()
            self.create_widgets(self.result)
            self.create_tree()
            self.buttonbox()
        elif os.path.isfile(self.result):
            self.cancel()

    def on_double_click(self, event=None):
        """On double click open file from list of files in chosen directory"""

        if self.tree.selection():
            item = self.tree.selection()[0]             # item clicked
            fname = self.tree.item(item, "values")[0]   # get filename
            self.fformat = os.path.splitext(fname)[1]   # get file format
            self.e_var.set(fname)                       # set filename to entry
            self.result = fname
            self.cancel()

    def on_left_click(self, event=None):
        """On left click choose file from list of files in chosen directory"""

        item = self.tree.selection()
        if isinstance(item, tuple):
            fname = self.tree.item(item, "values")[0]
            self.e_var.set(fname)

    def popup(self, event=None):
        """Create a popup menu (launched on right click)"""

        iid = self.tree.identify_row(event.y)
        self.tree.selection_set(iid)
        self.menu.post(event.x_root, event.y_root)

    def sort_by(self, col, order):
        """Sort data table by columns in either ascending or descending order"""

        data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        data.sort(key=lambda x: (x[0] == "None", int(x[0]) if x[0].isdigit() else x[0]), reverse=order)

        for i, item in enumerate(data):
            self.tree.move(item[1], "", i)
        self.tree.heading(col, command=lambda c=col:
        self.sort_by(c, not order))

        self.change_row_colors()    # reload rows' colors
