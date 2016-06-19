""" ArboTopo - data: measurement

This class represents a measurement which gives information about (the position of) a TopoPoint.

copyright (C) 2016 Bram Rooseleer
"""


class Measurement:
    """An abstract measurement."""

    @staticmethod
    def create_measurement(device, **kwargs):
        """A factory function to create a measurement of the correct device with the given arguments."""
        cls = device.get_measurement_cls()
        return cls(**kwargs)

    def __init__(self, dataset, name, point, group=None, device=None, remarks=None, **kwargs):
        """Create a measurement for a dataset."""
        self.dataset = dataset
        self.name = name
        self.point = point
        self.group = group
        self.device = device
        self.remarks = remarks
        self.data = kwargs


class AbsoluteMeasurement(Measurement):
    """A measurement of an absolute position."""

    @property
    def x(self):
        """Return the x-coordinate of the measured point."""
        try:
            return self._x
        except AttributeError:
            self._calculate_position()
            return self._x

    @property
    def y(self):
        """Return the y-coordinate of the measured point."""
        try:
            return self._y
        except AttributeError:
            self._calculate_position()
            return self._y

    @property
    def z(self):
        """Return the z-coordinate of the measured point."""
        try:
            return self._z
        except AttributeError:
            self._calculate_position()
            return self._z

    def _calculate_position(self):
        """Calculate the position of the measured point."""
        (self._x, self_y, self_z) = self.device.calculate_position(self.data)


class RelativeMeasurement(Measurement):
    """A measurement of the difference between two positions."""

    def __init__(self, refpoint, **kwargs):
        """Create a relative measurement for a dataset."""
        Measurement.__init__(self, **kwargs)
        self.refpoint = refpoint

    @property
    def dx(self):
        """Return the x-difference between the two points (from ref to current)."""
        try:
            return self._dx
        except AttributeError:
            self._calculate_position()
            return self._dx

    @property
    def dy(self):
        """Return the y-difference between the two points (from ref to current)."""
        try:
            return self._dy
        except AttributeError:
            self._calculate_position()
            return self._dy

    @property
    def dz(self):
        """Return the z-difference between the two points (from ref to current)."""
        try:
            return self._dz
        except AttributeError:
            self._calculate_position()
            return self._dz

    def _calculate_position(self):
        """Calculate the different between the two points."""
        (self._dx, self_dy, self_dz) = self.device.calculate_difference(self.data)