import sys

if sys.version_info.major == 2:
    raise EnvironmentError("arcpy_metadata 1.x is for Python 3 and ArcGIS Pro only. For ArcMap/Python 2, please install the latest version in the 0.x series (e.g. `pip install arcpy_metadata<1.0`)")

from arcpy_metadata.version import __author__
from arcpy_metadata.version import __version__
from arcpy_metadata.metadata_editor import MetadataEditor







