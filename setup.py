from setuptools import setup

from arcpy_metadata import version

setup(name="arcpy_metadata",
	version=version.__version__,
	description="Python metadata editing classes for ArcGIS feature classes",
	#scripts=[],
	packages=['arcpy_metadata',],
	author=version.__author__,
	author_email="nrsantos@ucdavis.edu",
	url='https://github.com/ucd-cws/arcpy_metadata',
)

