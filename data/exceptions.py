""" ArboTopo - data: exceptions

These file contains the exceptions used in the data package.

copyright (C) 2016 Bram Rooseleer
"""

from exceptions import ArboTopoException


class DataException(ArboTopoException):
    """An exception raised when data is missing."""


class NoSuchFieldException(DataException):
    """An exception raised when a field is missing."""

    @classmethod
    def message_template(cls):
        return "Field '{field} is missing from '{name}' of type '{type}'."


class NoSuchDeviceException(DataException):
    """An exception raised a requested device does not exist."""

    @classmethod
    def message_template(cls):
        return "No device with name '{device}' in dataset '{dataset}'."


class NoSuchMeasurementException(DataException):
    """An exception raised a requested measurement does not exist."""

    @classmethod
    def message_template(cls):
        return "No measurement with name '{measurement}' in dataset '{dataset}'."
