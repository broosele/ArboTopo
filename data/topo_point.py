""" ArboTopo - data: topo point

This class represents a geographical place.

copyright (C) 2016 Bram Rooseleer
"""


class TopoPoint:
    """A class containing information about a topo point."""

    def __init__(self, name, p, l=None, r=None, t=None, b=None, remarks=None, **kwargs):
        """Create a topo point with the following parameters.

        -name:          the name of the topo point
        -p:             the 3D point defininf the position of the topo point
        -l, r, t, b:    the points (left, right, top, bottom) defining a section of the cave trough the topo point
        -remarks:       some extra textual information about the topo point

        """
        self.name = name
        self.p = p
        self.l = l
        self.r = r
        self.t = t
        self.b = b
        self.remarks = remarks
        self.properties = kwargs
