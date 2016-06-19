""" ArboTopo - exceptions

These file contains the base exceptions used in the ArboTopo program.

copyright (C) 2016 Bram Rooseleer
"""


class ArboTopoException(Exception):
    """An exception caused by the program itself.

    All exceptions thrown by this program should be of this type.
    """

    def __init__(self, **kwargs):
        """Create a ArboTopoException. The given keyword arguments are used to fill in the message template."""
        self.kwargs = kwargs

    @classmethod
    def message_template(cls):
        """Return the message template. Fields provided when creating the exception can be used."""
        raise NotImplementedError()

    def __str__(self):
        """Return the message for this exception."""
        return self.message_template().format(**self.kwargs)