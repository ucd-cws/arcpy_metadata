from setuptools import setup

from arcpy_metadata import version

setup(name="arcpy_metadata",
	version=version.__version__,
	description="Python metadata editing classes for ArcGIS feature classes. WARNING: Version 0.4 deprecates the .get() and .set() methods used in prior versions of arcpy_metadata. you can now set values using normal Python, such as by setting metadata.title = \"feature class title\"",
	#scripts=[],
	packages=['arcpy_metadata',],
	author=version.__author__,
	author_email="nrsantos@ucdavis.edu",
	url='https://github.com/ucd-cws/arcpy_metadata',
)

