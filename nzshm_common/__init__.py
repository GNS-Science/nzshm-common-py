__author__ = "GNS Science"
__email__ = 'nshm@gns.cri.nz'
__version__ = '0.8.0'

from .location import location

# Common classes at the top level for convenience
from .location.coded_location import CodedLocation, CodedLocationBin
from .location.types import LatLon
