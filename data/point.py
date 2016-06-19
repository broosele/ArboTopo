""" ArboTopo - data: point

This class represents a point in 3D space with some information about the error on it.

Errors are always considered to be uncorrelated and gaussian.

copyright (C) 2016 Bram Rooseleer
"""

from math import sqrt


class Point:
    """A inmutable point in 3D space."""

    def __init__(self, x, y, z, error_x=None, error_y=None, error_z=None):
        """Create a point."""
        self._x = x
        self._y = y
        self._z = z
        self._error_x = error_x
        self._error_y = error_y
        self._error_z = error_z

    @property
    def x(self):
        """Return the x-coordinate."""
        return self._x

    @property
    def y(self):
        """Return the y-coordinate."""
        return self._y

    @property
    def z(self):
        """Return the z-coordinate."""
        return self._z

    @property
    def error_x(self):
        """Return the (std of the) error on the x-coordinate."""
        return self._error_x

    @property
    def error_y(self):
        """Return the (std of the) error on the y-coordinate."""
        return self._error_y

    @property
    def error_z(self):
        """Return the (std of the) error on the z-coordinate."""
        return self._error_z

    @property
    def d(self):
        """Return the (euclidian) size of this 3D vector."""
        return sqrt(self._x**2+self._y**2+self._z**2)

    @property
    def error_d(self):
        """Return the size of the total error on the on this 3D vector."""
        try:
            return sqrt(self._x**2+self._y**2+self._z**2)
        except TypeError:
            return None

    def xyz(self):
        """Return a tuple with the x, y and z-coordinates."""
        return (self._x, self._y, self._z)

    def __mul__(self, other):
        """Return the multiplication of this Point with the given numerical."""
        if not isinstance(other, (int, float)):
            raise TypeError("Point can only be multiplied by numerical.")
        try:
            error_x = other*self._error_x
        except TypeError:
            error_x = None
        try:
            error_y = other*self._error_y
        except TypeError:
            error_y = None
        try:
            error_z = other*self._error_z
        except TypeError:
            error_z = None
        return Point(x=self._x*other, y=self._y*other, z=self._z*other, error_x=error_x, error_y=error_y, error_z=error_z)

    def __rmul__(self, other):
        """Return the multiplication of this Point with the given numerical."""
        return other*self

    def __add__(self, other):
        """Return the addition of this Point with the given Point."""
        if not isinstance(other, Point):
            raise TypeError("Point can only be added to another Point.")
        try:
            error_x = sqrt(other._error_x**2+self._error_x**2)
        except TypeError:
            error_x = None
        try:
            error_y = sqrt(other._error_y**2+self._error_y**2)
        except TypeError:
            error_y = None
        try:
            error_z = sqrt(other._error_z**2+self._error_z**2)
        except TypeError:
            error_z = None
        return Point(x=self._x+other._x, y=self._y+other._y, z=self._z+other._z, error_x=error_x, error_y=error_y, error_z=error_z)

    def __sub__(self, other):
        """Return the subtraction of this Point by the given Point."""
        if not isinstance(other, Point):
            raise TypeError("Point can only be subtracted by another Point.")
        return self + (-other)

    def __neg__(self):
        """Return the negated version of this Point."""
        return Point(x=-self._x, y=-self._y, z=-self._z, error_x=self._error_x, error_y=self._error_y, error_z=self._error_z)

    def __pos__(self):
        """Return self."""
        return self