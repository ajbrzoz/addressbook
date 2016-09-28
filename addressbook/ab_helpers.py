"""This module provides helper functions"""

import os
import sys
from contextlib import contextmanager

from addressbook.ab_person import *
from addressbook.ab_parsers import *


def search(l, value, key):
    """Perform binary search on a list and return the item with the specified key value (or a list of items
    in case of multiple matching returns. If no item is found, it returns None.
    If the list is empty, it returns EmptyBase exception.

    Attributes:
        l (list): List to search through
        value (str): Key value to be found in a list
        key (keyword): Key the value of which is to be found
    """

    found = []

    def bsearch(l, item, low, high):
        while low <= high:
            mid = (low + high) // 2
            if l[mid].__getattribute__(key) == item:
                found.append(l[mid])
                a = mid + 1
                b = mid - 1
                while a in range(len(l)):
                    if l[a].__getattribute__(key) == item:
                        found.append(l[a])
                    a += 1
                while b in range(len(l)):
                    if l[b].__getattribute__(key) == item:
                        found.append(l[b])
                    b -= 1
                break
            elif l[mid].__getattribute__(key) is None or l[mid].__getattribute__(key) > item:
                return bsearch(l, item, low, mid - 1)
            else:
                return bsearch(l, item, mid + 1, high)

        if len(found) >= 1:
            return found[:]
        else:
            return None

    if len(l) > 0:
        return bsearch(l, value, 0, len(l) - 1)


def sorting(l, att, reverse=None):
    """Sort the AddressBook by a person's key value

    Attributes:
        att (str): Person's key
    """
    if reverse is None:
        return l.sort(key=lambda x: (x.__getattribute__(att) is None, x.__getattribute__(att)))
    return l.sort(key=lambda x: (x.__getattribute__(att) is None, x.__getattribute__(att)), reverse=True)


def search_base(l, **kwargs):
    """Search through the AddressBook to find the item with the specified key value
    (or a list of items in case of multiple matching returns. Since the 'search_base' uses the 'search' function,
    which is based on binary search, the AddressBook's items are sorted by the keyword attribute given in **kwargs
    before the search begins.

    Attributes:
        **kwargs (keyword=str): Key and value of the person being looked for
    """

    for (k, v) in kwargs.items():
        capit = ('name', 'surname', 'city')
        if k in capit:
            v = v.title()
        elif k == 'email':
            v = email_valid(v)
        elif k == 'streetname':
            v = street_parser(v, '')[0]
        elif k == 'phone':
            v = phone_parser(v)[0]
        elif k == 'birthday':
            y, m, d = date_parser(v)
            v = dt.date(y, m, d)
        elif k in ['year', 'month', 'day']:
            v = int(v)
        sorting(l, k)
        # found items (None, a Person object or list of objects)
        found = search(l, v, k)
        return found

def human_size(num):
    """Convert filesize in bytes to human readable format

    Attributes:
        num (int) - Filesize in bytes
    """
    suffix = 'B'
    for unit in ['', 'K', 'M', 'G']:
        if num < 1024.0:
            return "{0:.1f} {1}{2}".format(num, unit, suffix)
        num /= 1024.0


@contextmanager
def suppress_stdout():
    """Function used for temporary suppressing stdout. Adapted from Dave Smith's blog (http://thesmithfam.org)"""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


@contextmanager
def exc_catcher():
    """Function for dealing with exceptions that can be raised while working with AddressBook"""
    try:
        yield
    except EmptyBase as eb:
        print(eb)
    except WrongInput as wi:
        print(">> {}. Try again.".format(wi))
    except ItemNotFound as inf:
        print(">> {}".format(inf))
    except TypeError:
        print(">> Invalid input. Try again.")


@contextmanager
def keyboard_catcher():
    try:
        yield
    except KeyboardInterrupt:
        print("\n>> Shutdown requested on keyboard... exiting")
        sys.exit()
