import tkinter.messagebox
import tkinter.simpledialog

from addressbook.ab_windows.files_window import *


class FileSavedMessage(object):

    def __init__(self):

        tkinter.messagebox.showinfo("File saved", "The file has been saved.")


class KeywordEntry(ttk.Entry):

    def __init__(self, master, keyword, **kw):

        self.keyword = keyword
        super().__init__(master=master, **kw)


class KeywordCheckbutton(ttk.Checkbutton):

    def __init__(self, master, keyword, **kw):

        self.keyword = keyword
        super().__init__(master=master, **kw)


class OrderCheckbutton(ttk.Radiobutton):

    def __init__(self, master, keyword, **kw):

        self.keyword = keyword
        super().__init__(master=master, **kw)
