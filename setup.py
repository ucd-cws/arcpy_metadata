from setuptools import setup

from arcpy_metadata import version

setup(name="arcpy_metadata",
	version=version.__version__,
	description="Python metadata editing classes for ArcGIS feature classes.",
	long_description="""Version 1.x supports ArcGIS Pro and versions below that are for ArcMap.
	Version 1.x also supports reading and editing from Server and Portal (including ArcGIS Online).
	See all metadata elements at https://github.com/ucd-cws/arcpy_metadata""",
	#scripts=[],
	packages=['arcpy_metadata',],
	install_requires=[
        'python>=3.6',
        'arcpy>=2.6',  # when the metadata export tools were introduced in Pro
        'lxml>=2.0' # they changed how the tree behaves here - this was updated to use the new behavior
	],
	author=version.__author__,
	url='https://github.com/ucd-cws/arcpy_metadata',
)

