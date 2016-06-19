""" ArboLib - data: algorithm

The Algorithm class of this module is an abstract implementation of a class used to create TopoPoints from a Dataset.

copyright (C) 2016 Bram Rooseleer
"""


class Algorithm:
    """An abstract algorithm to interprete measurement data and create the resulting TopoPoints."""

    def __init__(self, dataset):
        """Create an algorithm with the dataset of which it should be executed."""
        self.dataset = dataset
        self._recalculate()

    def _recalculate(self):
        """Recalculate the TopoPoints."""
        raise NotImplementedError()

    def get_topo_points(self):
        """Return the calculated topo points."""
        raise NotImplementedError()