"""This module contains AddressBook class used for storing, adding and modifying entries"""

from addressbook.ab_converters import to_json
from addressbook.ab_helpers import *
from addressbook.ab_person import *

import json
import pickle
import re
import time


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

        Attributes:
            name (str): Person's name
            surname (str): Person's surname
            email (str): Person's email address
            phone (str): Person's phone number
        """

        # append the new object to AddressBook
        super().append(Person(name, surname, email, phone))

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

    def json_changes(self):
        """Save changes made to an opened file."""

        self.save_to_json(self.filename)

    def pickle_changes(self):
        """Save changes made to an opened file."""

        self.save_to_pickle(self.filename)

    def save_base(self, filename=None, fileformat=".pkl"):

        abook_name = filename
        types = re.compile(r".pkl|.pickle|.json$")

        if filename is None:
            # default filename containing saving time
            abook_name = "abook" + time.strftime("%Y-%m-%d") + ".pkl"
        elif not re.search(types, filename):
            abook_name = filename + ".pkl"

        if fileformat == ".json":
            self.save_to_json(abook_name)
        else:
            self.save_to_pickle(abook_name)

        self.filename = abook_name

    def save_to_json(self, abook_name):

        with open(abook_name, "w", encoding="utf-8") as abook_file:
            json.dump(self, abook_file, default=to_json)

    def save_to_pickle(self, abook_name):

        with open(abook_name, "wb") as abook_file:
            pickle.dump(self, abook_file)

    def sorting(self, att, reverse=None):
        """Sort the address book by a person's key value

        Attributes:
            att (str): Person's key
        """
        sorting(self, att, reverse=reverse)
