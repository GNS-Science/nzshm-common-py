"""
This module contains common type definitions.

When imported from an external package, the types defined here should also be
available at the top level of the package, e.g.:

    >>> from nzshm_common import LatLon
"""

from typing import NamedTuple


class LatLon(NamedTuple):
    """
    A lightweight type for `(latitude, longitude)` pairs.

    Examples:
        >>> wlg = LatLon(-41.3, 174.78)
        >>> wlg
        LatLon(latitude=-41.3, longitude=174.78)
        >>> wlg.latitude
        -41.3
        >>> wlg[0]
        -41.3
    """

    latitude: float
    longitude: float


LatLon.__module__ = "nzshm_common"
