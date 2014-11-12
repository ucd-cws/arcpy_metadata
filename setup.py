__author__ = 'nickrsan'
from arcpy_metadata import __version__ as meta_version

from distutils.core import setup

setup(name="Arcpy Metadata Editor (arcpy_metadata)",
	version=meta_version,
	description="Python metadata editing classes for ArcGIS feature classes",
	#scripts=[],
	packages=['arcpy_metadata',],
	author="Nick Santos, with contributions from other CWS staff",
	author_email="nrsantos@ucdavis.edu",
	url='https://github.com/ucd-cws/arcpy_metadata',
)
