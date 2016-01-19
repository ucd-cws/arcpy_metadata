from __future__ import print_function

import xml
import os
import xml.etree.ElementTree as ET

import arcpy

from version import *
from metadata_items import *


# TODO: Convert to using logging or logbook - probably logging to keep dependencies down

try:  # made as part of a larger package - using existing logger, but logging to screen for now if not in that package
    from log import write as logwrite
    from log import warning as logwarning
except ImportError:
    def logwrite(log_string, autoprint=1):  # match the signature of the expected log function
        print(log_string)


    def logwarning(log_string):
        print("WARNING: {0:s}".format(log_string))

installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
xslt = os.path.join(installDir, r"Metadata\Stylesheets\gpTools\exact copy of.xslt")
metadata_temp_folder = arcpy.env.scratchFolder  # a default temp folder to use - settable by other applications so they can set it once


class MetadataItem(object):
    '''
    A standard Metadata Item
    '''

    path = None
    value = ""

    def __init__(self, parent=None):
        self.parent = parent
        try:
            self.parent.elements
        except AttributeError:
            self.parent = parent.parent
        self.element = None
        self._require_tree_elements()

        # set current metadata value
        self.value = self.parent.elements.find(self.path).text
        self.attributes = self.parent.elements.find(self.path).attrib

    def _require_tree_elements(self):
        """
            Checks that the required elements for this item are in place. If they aren't, makes them
        """
        e_tree = self.path.split('/')
        root = self.parent.elements.getroot()

        done = False
        while not done:
            d = {}
            i = 0
            d[i] = root
            for e in e_tree:
                # remove index for multi items, looks goofy. Is there a better way?
                if "[" in e:
                    p = e.index('[')
                    e_name = e[:p]
                    e_attrib = e[p:][1:-1].split('][')
                else:
                    e_name = e
                    e_attrib = []
                i += 1
                d[i] = d[i-1].find(e)
                if d[i] is None:
                    child = ET.Element(e_name)
                    for attrib in e_attrib:
                        if attrib[0] == "@":
                            kv = attrib.split('=')
                            key = kv[0][1:]
                            value = kv[1][1:-1]
                            child.set(key, value)
                    d[i-1].append(child)
                    break
                elif i == len(e_tree):
                    self.element = d[i]
                    done = True

    def _write(self):

        # set value
        if self.value and self.parent:
            item = self.parent.elements.find(self.path)
            item.text = self.value  # set the value, it will be written later

        if self.attributes and self.parent:
            item = self.parent.elements.find(self.path)
            for attribute in self.attributes:
                item.set(attribute, self.attributes[attribute])  # set the value, it will be written later

        if not self.parent:
            raise ValueError(
                "Can't write values without being contained in a Metadata Editor list or without manually initializing self.parent to an instance of MetadataEditor")

    def set(self, value):
        self.value = value
        return self.get()

    def set_attrib(self, attribute, attri_value):
        self.attributes[attribute] = attri_value
        return self.get_attrib()

    def get(self):
        return self.value

    def get_attrib(self):
        return self.attributes

    def remove_attrib(self, attribute):
        try:
            del self.attributes[attribute]
        except KeyError:
            logwrite("Attribute %s does not exist" % attribute)

        return self.get_attrib()

    def append(self, value):
        self.value += str(value)
        return self.get()

    def prepend(self, value):
        self.value = str(value) + self.value
        return self.get()


class MetadataMulti(MetadataItem):
    """
        A metadata item for groups of items (like tags). Define the root element (self.path) and then the name of the
        subitem to store there (self.tag_name) and you can use list-like methods to edit the group
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

    def __iter__(self):
        return iter(self.current_items)

    def __getitem__(self, key):
        return self.current_items[key]

    def _add_item(self, item):
        """
            Adds an individual item to the section
            :param item: the text that will be added to the multi-item section, wrapped in the appropriate tag
                configured on parent object
            :return: None
        """

        element = ET.Element(self.tag_name)
        element.text = item
        self.current_items.append(element)

    def get(self):
        values = []
        for item in self.current_items:
            values.append(item.text)
        return values

    def add(self, items):
        """
        :param items:
        :return: self.get()
        """
        for item in items:
            self._add_item(item)

        return self.get()

    def extend(self, items):
        """
            An alias for "add" to make this more pythonic
            :param items: list of text items to add to this multi-item metadata section
            :return: None
        """

        self.add(items)
        return self.get()

    def append(self, item):
        """
            Adds a single item to the section, like a list append
            :param item:
            :return: None
        """
        self._add_item(item)
        return self.get()

    def remove(self, item):
        items_to_remove = []
        for i in self.current_items:
            if i.text == item:
                items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self.get()

    def removeall(self):
        items_to_remove = []
        for i in self.current_items:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self.get()


class MetadataItems(MetadataItem):
    """
        A helper objects for more complex items like Locals or Contacts.
        This object will allow to iterage though multiple items of the same type
    """

    def __init__(self, parent, path):
        self.path = os.path.dirname(path)
        self.tag_name = os.path.basename(path)
        super(MetadataItems, self).__init__(parent)
        self.path = path
        self.elements = self.parent.elements.findall(self.path)

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    # def get(self):
    #     values = []
    #     for element in self.elements:
    #         values.append(element.text)
    #     return values
    #
    # def _add_item(self,item):
    #     element = ET.Element(self.tag_name)
    #     element.text = item
    #     self.elements.append(element)
    #
    # def add(self, items):
    #     for item in items:
    #         self._add_item(item)
    #     return self.get()
    #
    # def extent(self, items):
    #     self.add(items)
    #
    # def append(self, item):
    #     self._add_item(item)
    #     return self.get()
    #
    # def remove(self, item):
    #     items_to_remove = []
    #     for i in self.elements:
    #         if i.text == item:
    #             items_to_remove.append(i)
    #     for i in items_to_remove:
    #         self.elements.remove(i)
    #     return self.get()
    #
    # def remove_all(self):
    #     items_to_remove = []
    #     for i in self.elements:
    #         items_to_remove.append(i)
    #     for i in items_to_remove:
    #         self.elements.remove(i)
    #
    #     return self.get()


class MetadataParentItem(MetadataItem):
    """
    A helper object for more complex items like Contact and Locals
    This object will allow to add child elements to an item
    """

    def __init__(self, parent):

        self.parent = parent
        super(MetadataParentItem, self).__init__(self.parent)

    def _create_item(self, iter, parent, tag_name):
        for i in iter:
            if i.tag == tag_name:
                return MetadataSubItem(i, parent, True)
        i = ET.Element(tag_name)
        return MetadataSubItem(i, parent)

    def _create_items(self, iter, parent, tag_name):
        items = []
        for i in iter:
            if i.tag == tag_name:
                items.append(i)

        if not items:
            items = [ET.Element(tag_name)]
            return MetadataSubItems(items, parent)
        else:
            return MetadataSubItems(items, parent, True)


class MetadataSubItem(object):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as single item inside a parent items
    """

    def __init__(self, element, parent, exists=False):

        self.parent = parent
        self.element = element

        if not exists:
            self.parent.append(element)

        self.attributes = self.element.attrib # {}

    def append(self, element):
        self.element.append(element)

    def get(self):
        return self.element.text

    def get_attrib(self):
        return self.attributes

    def set(self, value):
        self.element.text = value
        return self.get()

    def set_attrib(self, attributes):
        self.attributes.update(attributes)
        for attribute in self.attributes:
                self.element.set(attribute, self.attributes[attribute])
        return self.get_attrib()


class MetadataSubItems(object):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as multi item inside a parent item
    """

    def __init__(self, elements, parent, exists=False):
        self.elements = []
        self.parent = parent

        self.tag_name = elements[0].tag

        for element in elements:
            self.elements.append(MetadataSubItem(element, parent, exists))

    def append(self, item):
        element = ET.Element(self.tag_name)
        element.text = item
        self.elements.append(MetadataSubItem(element, self.parent, False))

    def add(self, items):
        for item in items:
            self.append(item)

    def get(self):
        elements = []
        for element in self.elements:
            elements.append(element.get())
        return elements

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        return self.elements[key]


class MetadataEditor(object):
    """
    The metadata editor
    Create an instance of this object for each metadata file you want to edit
    """

    def __init__(self, dataset=None, metadata_file=None, items=list(),
                 temp_folder=metadata_temp_folder):
        self.items = items
        self.metadata_file = metadata_file
        self.elements = xml.etree.ElementTree.ElementTree()
        self.temp_folder = temp_folder
        self.dataset = dataset

        self._gdb_datasets = ["FeatureClass", "Table", "RasterDataset", "RasterCatalog", "MosaicDataset"]
        self._simple_datasets = ["ShapeFile", "RasterDataset"]
        self._layers = ["FeatureLayer", "Layer"]

        if self.dataset:  # for both, we want to export the metadata out
            # export the metadata to the temporary location
            self.data_type = self.get_datatype()

            # for layers get the underlying dataset and start over
            if self.data_type in self._layers:
                desc = arcpy.Describe(self.dataset)
                self.data_type = desc.dataElement.dataType
                self.dataset = desc.dataElement.catalogPath

            self._workspace = self.get_workspace()
            self._workspace_type = self.get_workspace_type()

            # Datasets in Filesystem have metadata attached as XML file
            # we can directly write to it
            if self._workspace_type == 'FileSystem':
                if self.data_type in self._simple_datasets:
                    xml_file = self.dataset + ".xml"
                    #if no XML file exists create one and add most basic metadata item to it
                    if not os.path.exists(xml_file):
                        with open(xml_file, "w") as f:
                            f.write('<metadata xml:lang="en"></metadata>')
                    self.metadata_file = xml_file

                else:
                    raise TypeError("Datatype is not supported")

            # Metadata for GDB datasets are stored inside the GDB itself.
            # We need to first export them to a temporary file, modify them and then import them back
            else:
                if self.data_type in self._gdb_datasets:
                    metadata_filename = os.path.basename(self.dataset) + ".xml"
                    self.metadata_file = os.path.join(self.temp_folder, metadata_filename)
                    if os.path.exists(self.metadata_file):
                        os.remove(self.metadata_file)
                    logwrite("Exporting metadata to temporary file %s" % self.metadata_file)
                    arcpy.XSLTransform_conversion(self.dataset, xslt, self.metadata_file)
                else:
                    raise TypeError("Datatype is not supported")

        self.elements.parse(self.metadata_file)

        # create these all after the parsing happens so that if they have any self initialization, they can correctly perform it

        self.title = MetadataTitle(parent=self)
        self.abstract = MetadataAbstract(parent=self)
        self.purpose = MetadataPurpose(parent=self)
        self.tags = MetadataTags(parent=self)
        self.place_keywords = MetadataPlaceKeywords(parent=self)
        self.extent_description = MetadataExtentDescription(parent=self)
        self.temporal_extent_description = MetadataTemporalExtentDescription(parent=self)
        self.temporal_extent_instance = MetadataTemporalExtentInstance(parent=self)
        self.temporal_extent_start = MetadataTemporalExtentStart(parent=self)
        self.temporal_extent_end = MetadataTemporalExtentEnd(parent=self)
        self.min_scale = MetadataMinScale(parent=self)
        self.max_scale = MetadataMaxScale(parent=self)
        self.scale_resolution = MetadataScaleResolution(parent=self)
        self.last_update = MetadataLastUpdate(parent=self)
        self.update_frequency = MetadataUpdateFrequency(parent=self)
        self.update_frequency_description = MetadataUpdateFrequencyDescription(parent=self)
        self.credits = MetadataCredits(parent=self)
        self.citation = MetadataCitation(parent=self)
        self.limitation = MetadataLimitation(parent=self)
        self.supplemental_information = MetadataSupplementalInformation(parent=self)
        self.source = MetadataSource(parent=self)
        self.points_of_contact = MetadataPointsOfContact(parent=self)
        self.maintenance_contacts = MetadataMaintenanceContacts(parent=self)
        self.citation_contacts = MetadataCitationContacts(parent=self)

        self.language = MetadataDataLanguage(parent=self)
        self.metadata_language = MetadataMDLanguage(parent=self)

        self.locals = MetadataLocals(parent=self)

        self.items.extend([self.title, self.abstract, self.purpose, self.tags, self.place_keywords,
                           self.extent_description, self.temporal_extent_description, self.temporal_extent_instance,
                           self.temporal_extent_start, self.temporal_extent_end, self.min_scale, self.max_scale,
                           self.scale_resolution, self.last_update, self.update_frequency,
                           self.update_frequency_description, self.credits, self.citation, self.limitation, self.source,
                           self.points_of_contact, self.maintenance_contacts, self.citation_contacts, self.language,
                           self.metadata_language, self.locals, self.supplemental_information])

        if items:
            self.initialize_items()

    def get_datatype(self):
        # get datatype
        desc = arcpy.Describe(self.dataset)
        return desc.dataType

    def get_workspace(self):
        workspace = os.path.dirname(self.dataset)
        if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
            return workspace
        else:
            workspace = os.path.dirname(workspace)
            if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
                return workspace
            else:
                return os.path.dirname(self.dataset)

    def get_workspace_type(self):
        desc = arcpy.Describe(self._workspace)
        return desc.workspaceType

    def initialize_items(self):
        for item in self.items:
            item.parent = self

    def save(self):
        logwrite("Saving metadata", True)

        for item in self.items:
            item._write()

        self.elements.write(self.metadata_file)  # overwrites itself

        if self._workspace_type != 'FileSystem':
            arcpy.ImportMetadata_conversion(self.metadata_file, "FROM_ARCGIS", self.dataset,
                                            Enable_automatic_updates=True)

    def cleanup(self, delete_created_fc=False):
        try:
            logwrite("cleaning up from metadata operation")
            if self._workspace_type != 'FileSystem':
                if os.path.exists(self.metadata_file):
                    os.remove(self.metadata_file)

                xsl_extras = self.metadata_file + "_xslttransfor.log"
                if os.path.exists(xsl_extras):
                    os.remove(xsl_extras)

        except:
            logwarning("Unable to remove temporary metadata files")

    def finish(self):
        """
        Alias for saving and cleaning up
        :return:
        """

        self.save()
        self.cleanup()
