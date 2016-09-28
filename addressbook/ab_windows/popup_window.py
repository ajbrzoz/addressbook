import tkinter.simpledialog
import tkinter.ttk as ttk


class PopupWindow(tkinter.simpledialog.Dialog):
    """Basic Dialog window class, most of the application's windows inherit from"""

    def __init__(self, parent, title, msg=None):
        parent.update_idletasks()

        self.msg = msg
        self.e = None

        super().__init__(parent, title)


    def body(self, master):
        self.resizable(width=False, height=False)

        ttk.Label(master, text=self.msg, bg="#506e86").grid(row=0)

        self.e = ttk.Entry(master)

        self.e.grid(row=0, column=1)

        return self.e

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = ttk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default="active")
        w.pack(side="left", padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        data = self.e.get()
        self.result = data
