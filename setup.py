from setuptools import setup

with open('arcpy_metadata/version.py') as fin: exec(fin.read())

setup(name="arcpy_metadata",
	version=__version__,
	description="Python metadata editing classes for ArcGIS feature classes",
	#scripts=[],
	packages=['arcpy_metadata',],
	author="Nick Santos, with contributions from other CWS staff",
	author_email="nrsantos@ucdavis.edu",
	url='https://github.com/ucd-cws/arcpy_metadata',
)
