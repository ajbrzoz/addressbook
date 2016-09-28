"""This module contains exceptions used by address_book"""


class BaseError(Exception):
    """Base class for exceptions in this module."""
    pass


class EmptyBase(BaseError):
    """Exception raised if the address book is empty."""

    def __str__(self):
        return "The address book is empty."


class EmptyFile(BaseError):
    def __str__(self):
        return "The file is empty."


class FormatError(ValueError):
    pass


class ItemNotFound(BaseError):
    """Exception raised if an item cannot be found.

    Attributes:
        searit : Item being looked for
    """

    def __init__(self, searit):
        Exception.__init__(self)
        self.searit = searit

    def __str__(self):
        return "{0} has not been found in the base.".format(self.searit)


class Multiple(BaseError):
    """Exception raised for multiple results of a search

    Attributes:
        number (int): Number of items found

    """

    def __init__(self, number):
        self.number = number

    def __str__(self):
        return "In the base, there are {0} people with such a value.".format(self.number)


class WrongInput(ValueError):
    """Exception raised for errors in input.
    """
    pass
