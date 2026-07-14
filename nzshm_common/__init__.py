__author__ = "GNS Science"
__email__ = 'nshm@gns.cri.nz'

from ._version import __version__

# Common classes at the top level for convenience
from .location.coded_location import CodedLocation, CodedLocationBin
from .location.types import LatLon
