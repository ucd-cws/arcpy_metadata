from __future__ import print_function

__version__ = '0.2'
__author__ = 'nickrsan'

import xml
import os
import tempfile

import arcpy

# TODO: Add a log silent flag, or have it use standard logging?

try:  # made as part of a larger package - using existing logger, but logging to screen for now if not in that package
	from log import write as logwrite
	from log import warning as logwarning
except ImportError:

	def logwrite(log_string, autoprint=1):  # match the signature of the expected log function
		print(log_string)

	def logwarning(log_string):
		print("WARNING: {0:s}".format(log_string))

translators_folder = os.path.join(arcpy.GetInstallInfo()['InstallDir'], "Metadata", "Translator")
translation_file = os.path.join(translators_folder, "ARCGIS2FGDC.xml")

metadata_temp_folder = None  # a default temp folder to use


class MetadataItem(object):
	def __init__(self, parent=None):
		self.value = ""
		self.parent = parent
		self.path = None

	def _write(self):
		if self.value and self.parent:
			item = self.parent.elements.find(self.path)
			item.text = self.value  # set the value, it will be written later
		elif not self.parent:
			raise ValueError("Can't write values without being contained in a Metadata Editor list or without manually initializing self.parent to an instance of MetadataEditor")

	def set(self, value):
		self.value = value

	def get(self):
		return self.value

	def append(self, value):
		self.value += str(value)

	def prepend(self, value):
		self.value = str(value) + self.value


class MetadataMulti(MetadataItem):
	"""
		A metadata item for groups of items (like tags). Define the root element (self.path) and then the name of the subitem to store there (self.tag_name) and you can use list-like methods to edit the group
	"""

	def __init__(self, parent=None, tagname=None):
		super(MetadataMulti, self).__init__(parent)

		if not self.tag_name:
			self.tag_name = tagname

		self.current_items = self.parent.elements.find(self.path)

	def _add_item(self, item):
		element = xml.etree.ElementTree.Element(self.tag_name)
		element.text = item
		self.current_items.append(element)

	def add(self, items):
		for item in items:
			addition = _add_item

		self.current_items.append(addition)

	def extend(self, items):
		"""
			An alias for "add" to make this more pythonic
		"""

		self.add(items)

	def append(self, item):
		self._add_item(item)


class MetadataAbstract(MetadataItem):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		super(MetadataAbstract, self).__init__(parent)
		self.name = "abstract"
		self.path = "idinfo/descript/abstract"


class MetadataPurpose(MetadataItem):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		super(MetadataPurpose, self).__init__(parent)
		self.name = "purpose"
		self.path = "idinfo/descript/purpose"


class MetadataTags(MetadataMulti):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		self.name = "tags"
		self.tag_name = "themekey"
		self.path = "idinfo/keywords/theme[last()]"
		super(MetadataTags, self).__init__(parent)


class MetadataTitle(MetadataItem):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		super(MetadataTitle, self).__init__(parent)

		self.path = "idinfo/citation/citeinfo/title"
		self.name = "title"


class MetadataEditor(object):
	def __init__(self, feature_class=None, feature_layer=None, metadata_file=None, items=list(), temp_folder=metadata_temp_folder):
		self.items = items
		self.metadata_file = metadata_file
		self.elements = xml.etree.ElementTree.ElementTree()
		self.feature_class = feature_class
		self.feature_layer = feature_layer
		self.temp_folder = temp_folder
		self.created_temp_folder = False

		self.abstract = MetadataAbstract(parent=self)
		self.purpose = MetadataPurpose(parent=self)
		self.tags = MetadataTags(parent=self)
		self.title = MetadataTitle(parent=self)

		self.items.extend([self.abstract, self.purpose, self.tags, self.title])

		if self.feature_class and self.feature_layer:
			raise ValueError("MetadataEditor can only use either feature_class or feature_layer - do not provide both")

		if not self.temp_folder:
			self.temp_folder = tempfile.mkdtemp("arcpy_metadata")
			self.created_temp_folder = True

		if self.feature_layer:  # if we are using a feature layer, we'll turn  it into an in_memory feature class for the remainder
			logwrite("Copying layer to a feature class")
			self.feature_class = arcpy.CreateScratchName("pisces_metadata_temp", "", "", arcpy.env.workspace)
			arcpy.CopyFeatures_management(self.feature_layer, self.feature_class)  # copy the features over

		if self.feature_class:  # for both, we want to export the metadata out
			# export the metadata to the temporary location
			metadata_filename = arcpy.CreateScratchName("pisces", "metadata", "xml", temp_folder)
			self.metadata_file = os.path.join(temp_folder, metadata_filename)
			logwrite("Exporting metadata to temporary file %s" % self.metadata_file)
			arcpy.ExportMetadata_conversion(self.feature_class, translation_file, self.metadata_file)

		self.elements.parse(self.metadata_file)

		if items:
			self.initialize_items()

	def initialize_items(self):
		for item in self.items:
			item.parent = self

	def save(self, to_feature_class=True):
		logwrite("Saving metadata", True)

		for item in self.items:
			item._write()

		self.elements.write(self.metadata_file)  # overwrites itself

		if to_feature_class and self.feature_class:  # if we want to save it out to the feature class and feature class is defined
			arcpy.ImportMetadata_conversion(self.metadata_file, "FROM_FGDC", self.feature_class, Enable_automatic_updates=False)  # Leave Enable_automatic_updates as False because it will undo some of what we set and we just exported off of this dataset anyway!
		if self.feature_layer:  # if we started with a feature layer, we need to recreate it with our new metadata
			arcpy.Delete_management(self.feature_layer)  # delete the existing feature layer
			arcpy.MakeFeatureLayer_management(self.feature_class, self.feature_layer)  # and turn our temporary feature class into the feature layer

	def cleanup(self, delete_created_fc=False):
		try:
			logwrite("cleaninup up from metadata operation")
			if os.path.exists(self.metadata_file):
				os.remove(self.metadata_file)

			xsl_extras = self.metadata_file + "_xslttransfor.log"
			if os.path.exists(xsl_extras):
				os.remove(xsl_extras)

			if self.feature_layer and delete_created_fc:  # for people who passed in a feature layer, do we want to delete the exported feature class?
				arcpy.Delete_management(self.feature_class)

			if self.created_temp_folder:
				os.remove(self.temp_folder)
		except:
			logwarning("Unable to remove temporary metadata files")

	def finish(self):
		"""
			Alias for saving and cleaning up
		:return:
		"""

		self.save()
		self.cleanup()