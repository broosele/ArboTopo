""" ArboTopo - data: storable

This class represents an object which can be stored in a file.

copyright (C) 2016 Bram Rooseleer
"""

from data.exceptions import NoSuchFieldException


class Storable:
    """An abstract parent class for classes which can be stored in a file and loaded from a file.

    The fields of the object that need to be stored are the key word arguments used in the __init__ function. Their
    value can be retrieved or set by using the [] operator.
    """

    def __init__(self, name, **kwargs):
        """Create a Storable item."""
        self.name = name
        self.storage_fields = kwargs

    @property
    def data_type(self):
        """Return the type of stored data."""
        return self.__class__.__name__

    def __setitem__(self, name, value):
        """Set or add a field that will be stored."""
        self.storage_fields[name] = value

    def __getitem__(self, name):
        """Retrieve the stored field with the given name."""
        try:
            return self.storage_fields[name]
        except KeyError:
            raise NoSuchFieldException(field=name, name=self.name, type=self.data_type)

    def get_content(self):
        """Return a tuple containing data type, name and fields."""
        return self.data_type, self.name, self.storage_fields, self.substorables

    @property
    def substorables(self):
        """Return a list of storables hierarchically contained in this one."""
        return []