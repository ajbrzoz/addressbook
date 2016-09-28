"""This module contains AddressBook class used for storing, adding and modifying entries"""

from addressbook.ab_helpers import *
from addressbook.ab_person import *

import pickle
import time
import tkinter.messagebox


class AddressBook(list):
    """Class for creating and modifying address books"""

    def __init__(self):
        super().__init__()
        self.filename = None  # Used when working with opened file

    def __add__(self, other):
        return super().__add__(self.check(other))

    def __setitem__(self, index, obj):
        if isinstance(index, slice):
            return super().__setitem__(index, [self.check(o) for o in obj])
        else:
            return super().__setitem__(index, self.check(obj))

    def add_new(self, name, surname, email, phone):
        """Add a new person to the address book by creating a new Person instance.
        Before adding a new item the function checks if there is not anybody
        with such a name + surname combination in the address book. If so, the user is asked whether he/she wants to
        add the person anyway.

        Attributes:
            name (str): Person's name
            surname (str): Person's surname
            email (str): Person's email address
            phone (str): Person's phone number
        """

        item_added = False  # True if user decides to add the new object; if else, this value remains False

        name = name.title()
        surname = surname.title()

        c = str(surname + "_" + name)

        if len(self) > 0:
            item = search_base(self, personid=c)
            # duplicates found
            if item is not None:
                ask = tkinter.messagebox.askyesno("Duplicate found",
                                                  "There is already a person called {0} {1} in our base. "
                                                  "\nDo you want to add such a person anyway?".format(name,
                                                                                                      surname))
                if ask == "no":
                    return item_added

        # append the new object to AddressBook
        super().append(Person(name, surname, email, phone))

        item_added = True
        return item_added

    def append(self, obj):
        return super().append(self.check(obj))

    @staticmethod
    def check(obj):
        if not isinstance(obj, Person):
            raise TypeError(obj)
        else:
            return obj

    def extend(self, iterable):
        return super().extend([self.check(i) for i in iterable])

    def insert(self, index, obj):
        return super().insert(index, self.check(obj))

    def pickle_base(self, filename=None):
        """Save address book as a pickle file.

        Attributes:
            filename (str) - File saving name
        """

        abook_name = filename

        if filename is None:
            # default filename containing saving time
            abook_name = 'abook' + time.strftime('%Y-%m-%d') + '.pkl'
        elif not filename.endswith('.pkl'):
            abook_name = filename + '.pkl'

        abook_file = open(abook_name, 'wb')
        pickle.dump(self, abook_file, 2)
        abook_file.close()

        self.filename = abook_name

    def pickle_changes(self):
        """Save changes made to an opened file."""

        base_file = open(self.filename, 'wb')
        pickle.dump(self, base_file, 2)
        base_file.close()

    def sorting(self, att, reverse=None):
        """Sort the address book by a person's key value

        Attributes:
            att (str): Person's key
        """
        sorting(self, att, reverse=reverse)
