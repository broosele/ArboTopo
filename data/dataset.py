""" ArboTopo - data: dataset

This class represents a set of measurements and associated data.

copyright (C) 2016 Bram Rooseleer
"""

from data.storable import Storable
from data.exceptions import NoSuchDeviceException, NoSuchMeasurementException
from data.device import Device
from data.measurement import Measurement

class Dataset(Storable):
    """A set of measurements."""

    def __init__(self, datasets, name, parent=None, remarks=None):
        """Create a dataset."""
        self.name = name
        self.remarks = remarks
        self.children = {}
        self.devices = {}
        self.measurements = {}
        if name not in datasets:
            datasets[name] = self
        else:
            raise Exception("Dataset with name '{name}' already exists.".format(name=name))
        self._connect_parent_child(parent, datasets)

    def _connect_parent_child(self, parent_name, datasets):
        """Register the parent dataset with the given name as parent and self as its child. Postpone if needed."""
        if parent_name is None:
            self._set_parent(None)
        elif parent_name in datasets:
            self._set_parent(datasets[parent_name])

    def _set_parent(self, parent):
        """Set the parent dataset and self as its child."""
        self.parent = parent
        if parent is not None:
            parent._add_child(self)

    def _add_child(self, child):
        """Add a child (does not set the parent)."""
        if not child.name in self.children:
            self.children[child.name] = child

    def add_device(self, type, name, **kwargs):
        """Add a measurement device of the given type, with the given arguments."""
        if name in self.devices:
            raise Exception("Device with name '{name}' already exists in dataset '{dataset}'.".format(name=name, dataset=self.name))
        self.devices[name] = Device.create_device(type, name=name, **kwargs)

    def add_measurement(self, type, name, device, **kwargs):
        """Add a measurement of the given type, with the given arguments.."""
        if name in self.measurements:
            raise Exception("Measurement with name '{name}' already exists in dataset '{dataset}'.".format(name=name, dataset=self.name))
        device = self.get_device(device)
        self.measurements[name] = Measurement.create_measurement(type, name=name, device=device, **kwargs)

    def get_device(self, name):
        """Return the device with the given name. If is does not exist in self, look in parents."""
        if name in self.devices:
            return self.devices[name]
        elif self.parent is not None:
            return self.parent.get_device(name)
        else:
            raise Exception("No device '{name}' found in dataset {'dataset'}.".format(name=name, dataset=self.name))

    def get_device(self, name):
        """Return the device with the given name, if it exists."""
        try:
            return self.devices[name]
        except KeyError:
            raise NoSuchDeviceException(device=name, dataset=self.name)

     def get_measurement(self, name):
        """Return the measurement with the given name, if it exists."""
        try:
            return self.measurement[name]
        except KeyError:
            raise NoSuchMeasurementException(measurement=name, dataset=self.name)

    @property
    def substorables(self):
        return self.devices.values() + self.measurements.values()
