"""
A module containing all the exceptions that can be raised by Vezzo.
"""


class UnableToParseVersionString(Exception):
    """
    Raised when Vezzo is unable to parse a version string.
    """


class UnableToGenerateVersionOutputString(Exception):
    """
    Raised when Vezzo is unable to generate a version output string when running
    the command to get the version string.
    """
