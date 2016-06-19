""" ArboTopo - data: declination calculation

This file contains code to calculate the magnetic declination. Thanks to Christopher Weiss for the code.

copyright (C) 2016 Bram Rooseleer
"""

import data.geomag

gm = None
"""The data object to calculate the declination."""


def get_declination(latitude, longitude, altitude, date):
    """Return the magnetic declination for the latitude, longitude (both decimal degr.), altitude (meter) and date."""
    global gm
    if gm is None:
        gm = data.geomag.GeoMag()
    return gm.GeoMag(latitude, longitude, altitude/0.3048, date).dec
