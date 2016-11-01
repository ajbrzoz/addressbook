"""This module contains Person class used for creating and modifying entries in the address book"""

from addressbook.ab_parsers import *

import datetime as dt
import itertools


class Person(object):
    """Class for creating and modifying entries in the addressbook"""

    new_id = itertools.count()

    def __init__(self, name, surname, email, phone, mode="PL"):
        """
        Attributes:
            name (str): Person's name
            surname (str): Person's surname
            email (str): Person's e-mail address
            phone (str): Person's phone number
            mode ('PL'/'US'): Defines the style of presenting the phone number
        """

        # Person's id incremented with every new Person object appended to AddressBook instance
        self.id = next(Person.new_id)

        self.name = name.lower().title()
        self.surname = surname.lower().title()
        self.email = email_valid(email)

        self.phone, self.phone_area, self.phone_num = phone_parser(phone, mode)

        # Person's id based on combined surname and name. Used for comparison of two objects and for searching.
        self.personid = str(self.surname.title() + "_" + self.name.title())
        # Person's birthday. Optional. Can be set separately.
        self.birthday = None
        # Year of birth. Extracted from the birthday. Used for calculating age.
        self.year = None
        # Month of birth. Extracted from the birthday. Used for sorting purposes.
        self.month = None
        # Day of birth. Extracted from the birthday. Used for sorting purposes.
        self.day = None
        # Person's city. Optional. Can be set separately.
        self.city = None
        # Person's street name. Optional. Can be set separately.
        self.streetname = None
        # Person's street number. Optional. Can be set separately.
        self.streetnumber = None

    def __eq__(self, other):

        if hasattr(other, "personid"):
            return self.personid.__eq__(other.personid)

    def __lt__(self, other):

        return self.personid < other.personid

    def __ne__(self, other):

        if hasattr(other, "personid"):
            return self.personid.__ne__(other.personid)

    def __repr__(self):

        return "<{0}: {1}, {2}, {3}, {4}>".format(self.__class__.__name__, self.name, self.surname, self.email,
                                                  self.phone)

    def __setattr__(self, key, value, conversion=False):
        """Before setting an attribute check if the corresponding value's format is valid

            conversion (bool) - False by default. True when the Person object is being loaded from JSON file
                                (when there is no need for parsing values all over again)

        """

        if conversion is False:
            # capitalize first letters of non-numeric values (eg. name surname), except for e-mails
            if isinstance(value, str) and key != "email":
                value = value.title()

            if key == "email":
                value = email_valid(value)

            elif key == "phone":
                a, b, c = phone_parser(value)
                return (super().__setattr__(key, a),
                        super().__setattr__("phone_area", b),
                        super().__setattr__("phone_num", c))

            elif key == "street":
                # specifying both street name and number is obligatory in this case
                if value.replace(" ", "").isalpha():
                    raise WrongInput("You have not chosen a street name.")
                if value.isdecimal():
                    raise WrongInput("You have not chosen a street number.")

                a, b = street_parser(value)
                return (super().__setattr__("streetname", a),
                        super().__setattr__("streetnumber", b))

            elif key == "streetname" and value is not None:
                a, b = street_parser(value, self.streetnumber or " ")
                return (super().__setattr__(key, a),
                        super().__setattr__("streetnumber", b))

            elif key == "streetnumber" and value is not None:
                a, b = street_parser(self.streetname or " ", value)
                if b.isalpha():
                    raise WrongInput("Wrong street number format")
                return (super().__setattr__(key, b),
                        super().__setattr__("streetname", a))

            elif key == "birthday" and value is not None:
                y, m, d = date_parser(value)
                try:
                    birthday = dt.date(y, m, d)
                    return (super().__setattr__(key, birthday),
                            super().__setattr__("year", birthday.year),
                            super().__setattr__("month", birthday.month),
                            super().__setattr__("day", birthday.day))
                except ValueError as ex:
                    raise WrongInput(ex.__str__())

        return super().__setattr__(key, value)
