""" ArboTopo - data: device

These classes represent measurement devices.

copyright (C) 2016 Bram Rooseleer
"""

from datetime import date
from math import sin, cos
from data.measurement import AbsoluteMeasurement, RelativeMeasurement
from data.declination import get_declination


class Device:
    """An abstract measurement device."""

    @staticmethod
    def create_device(type, **kwargs):
        """A factory function to create a device of the correct type with the given arguments."""
        for cls in Device.__subclasses__():
            if cls.get_type() == type:
                break
        else:
            raise Exception("Device of type '{type}' unknown.".format(type=type))
        return cls(**kwargs)

    def __init__(self, name, model=None, remarks=None, **kwargs):
        """Create a measurement device."""
        self.name = name
        self.model = model
        self.remarks = remarks
        self.properties = kwargs
        self.type = self.__class__.get_type()

    @classmethod
    def get_type(cls):
        """Return the device type name."""
        return cls.__name__

    @classmethod
    def get_measurement_cls(cls):
        """Return the measurement class (abstract)."""
        raise NotImplementedError()


class AbsoluteDevice(Device):
    """A device for absolute measurements."""

    def calculate_position(self, data):
        """Calculates the absolute position (abstract)."""

    @classmethod
    def get_measurement_cls(cls):
        """Return the measurement class."""
        return AbsoluteMeasurement


class GPS(AbsoluteDevice):
    """A GPS device."""

    def __init__(self, **kwargs):
        """Create a GPS device."""
        AbsoluteDevice.__init__(self, **kwargs)

    def calculate_position(self, data):
        """Calculates the absolute position.

        data needs to be a dict with x, y, z and maptype fields.
        """
        raise NotImplementedError()


class RelativeDevice(Device):
    """A device for relative measurements."""

    def calculate_difference(self, data):
        """Calculates the relative position (abstract)."""
        raise NotImplementedError()

    @classmethod
    def get_measurement_cls(cls):
        """Return the measurement class."""
        return RelativeMeasurement


class DCIDevice(RelativeDevice):
    """A relative device that measures distance, compass and inclination."""

    def __init__(self, angleref='hor', year=2016, month=1, latitude=None, longitude=None, height=0, declination=None, **kwargs):
        """Create a classic device."""
        RelativeDevice.__init__(self, **kwargs)
        self.angleref = angleref
        if declination is None:
            if latitude is not None and longitude is not None:
                declination = get_declination(latitude, longitude, height, date(year, month, 1))
            else:
                declination = 0
        self.declination = declination

    def calculate_difference(self, data):
        """Calculates the relative position.

        data needs to be a dict with distance, inclination and compass fields.
        """
        distance = data['distance']
        if self.angleref == 'hor':
            slope = data['inclination']
        elif self.angleref == 'ver':
            slope = 90 - data['inclination']
        compass = data['compass'] + self.declination
        z  = sin(slope)*distance
        xy = cos(slope)*distance
        y  = cos(compass)*xy
        x  = sin(compass)*xy
        return (x, y, z)


class DistoX(DCIDevice):
    """A disto-X device."""

    def __init__(self, calibration_date=None, **kwargs):
        """Create a disto-X device."""
        RelativeDevice.__init__(self, **kwargs)
        self.calibration_date = calibration_date


class Classic(RelativeDevice):
    """A classic measurement device (measurement tape, compass, inclinometer)."""

    def __init__(self, **kwargs):
        """Create a classic device."""
        RelativeDevice.__init__(self,  **kwargs)