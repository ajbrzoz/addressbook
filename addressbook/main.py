#!/bin/env python

# Written by Anna Brzozowska, June 2016.

"""This the main module of AddressBook 1.0.

AddressBook 1.0 is a simple, (relatively) easy to use command-line contact manager that helps to
keep track of your contacts, including email addresses, phones, addresses and birthdays. It enables
users to create their own address books, save them (in pickle format) and restore data from existing ones.
Options include adding, modifying and removing entries, as well as sorting and searching through them.

"""

from addressbook.ab_gui import *

if __name__ == "__main__":
    main_app = App()
