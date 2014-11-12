from __future__ import print_function

__version__ = '0.2.5'
__author__ = 'nickrsan'

import xml
import os
import tempfile
import re

import arcpy

# TODO: Convert to using logging or logbook - probably logging to keep dependencies down
# TODO: For shapefiles can we skip the export step and just edit the xml in place??

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

metadata_temp_folder = None  # a default temp folder to use - settable by other applications so they can set it once


class MetadataItem(object):

	path = None
	value = ""

	def __init__(self, parent=None):
		self.parent = parent

		try:
			self._require_tree_elements()
		except RuntimeError:
			pass  # it's ok - it just means the path wasn't set yet - this will get run again in _set_path


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

	def _require_tree_elements(self):
		"""
			Checks that the required elements for this item are in place. If they aren't, makes them
		"""

		if not self.parent or not self.path:
			raise ValueError("MetadataItem must be assigned to a parent MetadataEditor and must have a path assigned before a require check can be performed")

		if self.parent.elements.find(self.path) is not None:  # if it already exists, easy - return now
			return True

		temp_path = re.sub("\[.*?\]", "", self.path)
		path_elements = temp_path.split("/")

		indices = range(len(path_elements))
		indices.reverse()
		for position in indices:  # go backward so we can determine where the closest element is
			attempt_elements = path_elements[:position]  # get all elements preceding the current one
			path = ""
			for item in attempt_elements:
				path += item + "/"
			path = path[:-1]  # chop off the trailing slash

			main_element = self.parent.elements.find(path)  # try finding the top level element
			if main_element is not None:  # if we found it
				create_elements = path_elements[position:]  # get the remaining elements
				parent_element = main_element
				for sub_element in range(len(create_elements)):  # and start creating the elements
					new_sub = xml.etree.ElementTree.SubElement(parent_element, create_elements[sub_element])  # create each sub_element in turn, then make it the new parent for the next iteration
					parent_element = new_sub
				# at this point all necessary parts of the tree for this item should be created
				break

		else:  # if we didn't break out of the loop by finding a fitting top level element
			raise RuntimeError("Could not create necessary parts of Metadata tree to edit elements - check the path specified on your metadata item to make sure it correctly references root positions (idinfo at the start)")


class MetadataMulti(MetadataItem):
	"""
		A metadata item for groups of items (like tags). Define the root element (self.path) and then the name of the subitem to store there (self.tag_name) and you can use list-like methods to edit the group
	"""

	tag_name = None
	current_items = []
	path = None

	def __init__(self, parent=None, tagname=None, path=None):

		if not self.tag_name:
			self.tag_name = tagname

		if path:
			self.path = path

		super(MetadataMulti, self).__init__(parent)

		self._refresh()

	def _refresh(self):
		self.current_items = self.parent.elements.find(self.path)

	def _add_item(self, item):
		"""
			Adds an individual item to the section
		:param item: the text that will be added to the multi-item section, wrapped in the appropriate tag configured on parent object
		:return: None
		"""
		element = xml.etree.ElementTree.Element(self.tag_name)
		element.text = item
		self.current_items.append(element)

	def add(self, items):
		"""

		:param items:
		:return: None
		"""
		for item in items:
			self._add_item(item)

	def extend(self, items):
		"""
			An alias for "add" to make this more pythonic
			:param items: list of text items to add to this multi-item metadata section
			:return: None
		"""

		self.add(items)

	def append(self, item):
		"""
			Adds a single item to the section, like a list append
		:param item:
		"""
		self._add_item(item)


class MetadataAbstract(MetadataItem):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		self.name = "abstract"
		self.path = "idinfo/descript/abstract"
		super(MetadataAbstract, self).__init__(parent)


class MetadataPurpose(MetadataItem):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		self.name = "purpose"
		self.path = "idinfo/descript/purpose"
		super(MetadataPurpose, self).__init__(parent)


class MetadataTags(MetadataMulti):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		self.name = "tags"
		super(MetadataTags, self).__init__(parent, tagname="themekey", path="idinfo/keywords/theme[last()]")


class MetadataTitle(MetadataItem):
	"""
		Just a shortcut MetadataItem that predefines the paths
	"""
	def __init__(self, parent=None):
		self.path = "idinfo/citation/citeinfo/title"
		self.name = "title"
		super(MetadataTitle, self).__init__(parent)


class MetadataEditor(object):
	def __init__(self, feature_class=None, feature_layer=None, metadata_file=None, items=list(), temp_folder=metadata_temp_folder):
		self.items = items
		self.metadata_file = metadata_file
		self.elements = xml.etree.ElementTree.ElementTree()
		self.feature_class = feature_class
		self.feature_layer = feature_layer
		self.temp_folder = temp_folder
		self.created_temp_folder = False

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
			metadata_filename = arcpy.CreateScratchName("pisces", "metadata", "xml", self.temp_folder)
			self.metadata_file = os.path.join(self.temp_folder, metadata_filename)
			logwrite("Exporting metadata to temporary file %s" % self.metadata_file)
			arcpy.ExportMetadata_conversion(self.feature_class, translation_file, self.metadata_file)

		self.elements.parse(self.metadata_file)

		# create these all after the parsing happens so that if they have any self initialization, they can correctly perform it
		self.abstract = MetadataAbstract(parent=self)
		self.purpose = MetadataPurpose(parent=self)
		self.tags = MetadataTags(parent=self)
		self.title = MetadataTitle(parent=self)

		self.items.extend([self.abstract, self.purpose, self.tags, self.title])

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