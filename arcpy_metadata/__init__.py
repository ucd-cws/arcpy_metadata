from __future__ import print_function

import xml
import os
import xml.etree.ElementTree as ET

import arcpy

from version import *
from metadata_items import *

import inspect
import types


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
        self._attributes = None
        self.attributes = self.parent.elements.find(self.path).attrib

    #def __repr__(self):
    #    return self.value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        if isinstance(value, dict):
            self._attributes = value
        else:
            raise RuntimeWarning("Must be of type dict")

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


class String(str):
    def __new__(cls, value, parent):
        print("Hier der wert: %s" % value)
        obj = str.__new__(cls, value)
        obj.parent = parent
        return obj


class MetadataString(MetadataItem, String):

    def __init__(self, value, parent=None):
        super(MetadataString, self).__init__(parent)
        self.value = value
        self._write()


class MetadataList(MetadataItem, list):

    def __init__(self, parent=None):
        super(MetadataList, self).__init__(parent)


class MetadataMulti(MetadataList):
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

    def __iter__(self):
        return iter(self.current_items)

    def __getitem__(self, key):
        return self.current_items[key]

    def _refresh(self):
        self.current_items = self.parent.elements.find(self.path)
        for item in self.current_items:
            super(MetadataMulti, self).append(item.text)

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

    def _get(self):
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

        return self._get()

    def extend(self, items):
        """
            An alias for "add" to make this more pythonic
            :param items: list of text items to add to this multi-item metadata section
            :return: None
        """

        self.add(items)
        return self._get()

    def append(self, item):
        """
            Adds a single item to the section, like a list append
            :param item:
            :return: None
        """
        self._add_item(item)
        super(MetadataMulti, self).append(item)


    def remove(self, item):
        items_to_remove = []
        for i in self.current_items:
            if i.text == item:
                items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self._get()

    def removeall(self):
        items_to_remove = []
        for i in self.current_items:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self._get()


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

        self._title = None
        helper = MetadataStringHelper("dataIdInfo/idCitation/resTitle", "title", self)
        self.title = MetadataTitle(value=helper.value, parent=self)
        self._abstract = None
        self.abstract = MetadataAbstract(parent=self)
        self._purpose = None
        self.purpose = MetadataPurpose(parent=self)
        self._tags = None
        self.tags = MetadataTags(parent=self)
        self._place_keywords = None
        self.place_keywords = MetadataPlaceKeywords(parent=self)
        self._extent_description = None
        self.extent_description = MetadataExtentDescription(parent=self)
        self._temporal_extent_description = None
        self.temporal_extent_description = MetadataTemporalExtentDescription(parent=self)
        self._temporal_extent_instance = None
        self.temporal_extent_instance = MetadataTemporalExtentInstance(parent=self)
        self._temporal_extent_start = None
        self.temporal_extent_start = MetadataTemporalExtentStart(parent=self)
        self._temporal_extent_end = None
        self.temporal_extent_end = MetadataTemporalExtentEnd(parent=self)
        self._min_scale = None
        self.min_scale = MetadataMinScale(parent=self)
        self._max_scale = None
        self.max_scale = MetadataMaxScale(parent=self)
        self._scale_resolution = None
        self.scale_resolution = MetadataScaleResolution(parent=self)
        self._last_update = None
        self.last_update = MetadataLastUpdate(parent=self)
        self._update_frequency = None
        self.update_frequency = MetadataUpdateFrequency(parent=self)
        self._update_frequency_description = None
        self.update_frequency_description = MetadataUpdateFrequencyDescription(parent=self)
        self._credits = None
        self.credits = MetadataCredits(parent=self)
        self._citation = None
        self.citation = MetadataCitation(parent=self)
        self._limitation = None
        self.limitation = MetadataLimitation(parent=self)
        self._supplemental_information = None
        self.supplemental_information = MetadataSupplementalInformation(parent=self)
        self._source = None
        self.source = MetadataSource(parent=self)
        self._points_of_contact = None
        self.points_of_contact = MetadataPointsOfContact(parent=self)
        self._maintenance_contacts = None
        self.maintenance_contacts = MetadataMaintenanceContacts(parent=self)
        self._citation_contacts = None
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

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):

        if isinstance(value, MetadataTitle):
            self._title = value
        else:
            self._title = MetadataTitle(value, self)

    @property
    def abstract(self):
        return self._abstract

    @abstract.setter
    def abstract(self, value):
        if isinstance(value, MetadataAbstract):
            self._abstract = value
        else:
            self._abstract.value = value

    @property
    def purpose(self):
        return self._purpose

    @purpose.setter
    def purpose(self, value):
        if isinstance(value, MetadataPurpose):
            self._purpose = value
        else:
            self._purpose.value = value
####
    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if isinstance(value, MetadataTags):
            self._tags = value
        elif isinstance(value, list):
            self._tags.removeall()
            self._tags.add(value)
        else:
            raise RuntimeWarning("Input value must be of type list")

######
    @property
    def place_keywords(self):
        return self._place_keywords

    @place_keywords.setter
    def place_keywords(self, value):
        if isinstance(value, MetadataPlaceKeywords):
            self._place_keywords = value
        elif isinstance(value, list):
            self._place_keywords.removeall()
            self._place_keywords.add(value)
        else:
            raise RuntimeWarning("Input value must be of type list")

######
    @property
    def extent_description(self):
        return self._extent_description

    @extent_description.setter
    def extent_description(self, value):
        if isinstance(value, MetadataExtentDescription):
            self._extent_description = value
        else:
            self._extent_description.value = value

######
    @property
    def temporal_extent_description(self):
        return self._temporal_extent_description

    @temporal_extent_description.setter
    def temporal_extent_description(self, value):
        if isinstance(value, MetadataTemporalExtentDescription):
            self._temporal_extent_description = value
        else:
            self._temporal_extent_description.value = value

######
    @property
    def temporal_extent_instance(self):
        return self._temporal_extent_instance

    @temporal_extent_instance.setter
    def temporal_extent_instance(self, value):
        if isinstance(value, MetadataTemporalExtentInstance):
            self._temporal_extent_instance = value
        else:
            self._temporal_extent_instance.value = value

######
    @property
    def temporal_extent_start(self):
        return self._temporal_extent_start

    @temporal_extent_start.setter
    def temporal_extent_start(self, value):
        if isinstance(value, MetadataTemporalExtentStart):
            self._temporal_extent_start = value
        else:
            self._temporal_extent_start.value = value


######
    @property
    def temporal_extent_end(self):
        return self._temporal_extent_end

    @temporal_extent_end.setter
    def temporal_extent_end(self, value):
        if isinstance(value, MetadataTemporalExtentEnd):
            self._temporal_extent_end = value
        else:
            self._temporal_extent_start.value = value

######
    @property
    def min_scale(self):
        return self._min_scale

    @min_scale.setter
    def min_scale(self, value):
        if isinstance(value, MetadataMinScale):
            self._min_scale = value
        else:
            self._min_scale.value = value

######
    @property
    def max_scale(self):
        return self._max_scale

    @max_scale.setter
    def max_scale(self, value):
        if isinstance(value, MetadataMaxScale):
            self._max_scale = value
        else:
            self._max_scale.value = value

######
    @property
    def scale_resolution(self):
        return self._scale_resolution

    @scale_resolution.setter
    def scale_resolution(self, value):
        if isinstance(value, MetadataScaleResolution):
            self._scale_resolution = value
        else:
            self._scale_resolution.value = value

######
    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, value):
        if isinstance(value, MetadataLastUpdate):
            self._last_update = value
        else:
            self._last_update.value = value

######
    @property
    def update_frequency(self):
        return self._update_frequency

    @update_frequency.setter
    def update_frequency(self, value):
        if isinstance(value, MetadataUpdateFrequency):
            self._update_frequency = value
        else:
            self._update_frequency.value = value

######
    @property
    def update_frequency_description(self):
        return self._update_frequency_description

    @update_frequency_description.setter
    def update_frequency_description(self, value):
        if isinstance(value, MetadataUpdateFrequencyDescription):
            self._update_frequency_description = value
        else:
            self._update_frequency_description.value = value

######
    @property
    def credits(self):
        return self._credits

    @credits.setter
    def credits(self, value):
        if isinstance(value, MetadataCredits):
            self._credits = value
        else:
            self._credits.value = value

######
    @property
    def citation(self):
        return self._citation

    @citation.setter
    def citation(self, value):
        if isinstance(value, MetadataCitation):
            self._citation = value
        else:
            self._citation.value = value

######
    @property
    def limitation(self):
        return self._limitation

    @limitation.setter
    def limitation(self, value):
        if isinstance(value, MetadataLimitation):
            self._limitation = value
        else:
            self._limitation.value = value

######
    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if isinstance(value, MetadataSource):
            self._source = value
        else:
            self._source.value = value

######
    @property
    def points_of_contact(self):
        return self._points_of_contact

    @points_of_contact.setter
    def points_of_contact(self, value):
        if isinstance(value, MetadataPointsOfContact):
            self._points_of_contact = value
        elif isinstance(value, list):
            self._points_of_contact.removeall()
            self._points_of_contact.add(value)
        else:
            raise RuntimeWarning("Input value must be of type list")

######
    @property
    def maintenance_contacts(self):
        return self._maintenance_contacts

    @maintenance_contacts.setter
    def maintenance_contacts(self, value):
        if isinstance(value, MetadataMaintenanceContacts):
            self._maintenance_contacts = value
        elif isinstance(value, list):
            self._maintenance_contacts.removeall()
            self._maintenance_contacts.add(value)
        else:
            raise RuntimeWarning("Input value must be of type list")

######
    @property
    def citation_contacts(self):
        return self._citation_contacts

    @citation_contacts.setter
    def citation_contacts(self, value):
        if isinstance(value, MetadataCitationContacts):
            self._citation_contacts = value
        elif isinstance(value, list):
            self._citation_contacts.removeall()
            self._citation_contacts.add(value)
        else:
            raise RuntimeWarning("Input value must be of type list")

######
    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        if isinstance(value, MetadataLanguage):
            self._language = value
        else:
            self._language.value = value

######
    @property
    def metadata_language(self):
        return self._metadata_language

    @metadata_language.setter
    def metadata_language(self, value):
        if isinstance(value, MetadataMDLanguage):
            self._metadata_language = value
        else:
            self._metadata_language.value = value

######
    @property
    def locals(self):
        return self._locals

    @locals.setter
    def locals(self, value):
        if isinstance(value, MetadataLocals):
            self._locals = value
        elif isinstance(value, list):
            self._locals.removeall()
            self._locals.add(value)
        else:
            raise RuntimeWarning("Input value must be of type list")

######
    @property
    def supplemental_information(self):
        return self._supplemental_information

    @supplemental_information.setter
    def supplemental_information(self, value):
        if isinstance(value, MetadataSupplementalInformation):
            self._supplemental_information = value
        else:
            self._supplemental_information.value = value



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
            print(item)

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
