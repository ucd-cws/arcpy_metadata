from setuptools import setup

from arcpy_metadata import version

setup(name="arcpy_metadata",
	version=version.__version__,
	description="Python metadata editing classes for ArcGIS feature classes.",
	long_description="""WARNING: Version 0.4 deprecates the .get() and .set() methods used in prior versions of arcpy_metadata. You can now set values using normal Python, such as by setting metadata.title = \"feature class title\".
	
	See all metadata elements at https://github.com/ucd-cws/arcpy_metadata""",
	#scripts=[],
	packages=['arcpy_metadata',],
	install_requires=[
		'six',
	],
	author=version.__author__,
	author_email="nrsantos@ucdavis.edu",
	url='https://github.com/ucd-cws/arcpy_metadata',
)

