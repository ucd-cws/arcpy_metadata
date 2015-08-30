from __future__ import print_function

__version__ = '0.3.0'
__author__ = 'nickrsan, thomas.maschler'

import xml
import os
import re

import arcpy

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
    path = None
    value = ""

    def __init__(self, parent=None):
        self.parent = parent

        try:
            self._require_tree_elements()
        except RuntimeError:
            pass  # it's ok - it just means the path wasn't set yet - this will get run again in _set_path

        self._create_item()

    def _create_item(self):
        # check if element exist, if not add to element tree
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
                    e = e[:p]
                i += 1
                d[i] = d[i-1].find(e)
                if d[i] is None:
                    child = xml.etree.ElementTree.Element(e)
                    d[i-1].append(child)
                    break
                elif i == len(e_tree):
                    done = True

    def _write(self):

        # set value
        if self.value and self.parent:
            item = self.parent.elements.find(self.path)
            item.text = self.value  # set the value, it will be written later
        elif not self.parent:
            raise ValueError(
                "Can't write values without being contained in a Metadata Editor list or without manually initializing self.parent to an instance of MetadataEditor")

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
            raise ValueError(
                "MetadataItem must be assigned to a parent MetadataEditor and must have a path assigned before a require check can be performed")

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
                    new_sub = xml.etree.ElementTree.SubElement(parent_element, create_elements[
                        sub_element])  # create each sub_element in turn, then make it the new parent for the next iteration
                    parent_element = new_sub
                # at this point all necessary parts of the tree for this item should be created
                break

        else:  # if we didn't break out of the loop by finding a fitting top level element
            raise RuntimeError(
                "Could not create necessary parts of Metadata tree to edit elements - check the path specified on your metadata item to make sure it correctly references root positions (idinfo at the start)")


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
        self.path = "dataIdInfo/idAbs"
        super(MetadataAbstract, self).__init__(parent)


class MetadataPurpose(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "purpose"
        self.path = "dataIdInfo/idPurp"
        super(MetadataPurpose, self).__init__(parent)


class MetadataTags(MetadataMulti):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "tags"
        super(MetadataTags, self).__init__(parent, tagname="keyword", path="dataIdInfo/searchKeys[last()]")


class MetadataTitle(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.path = "dataIdInfo/idCitation/resTitle"
        self.name = "title"
        super(MetadataTitle, self).__init__(parent)


class MetadataEditor(object):
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
        self.abstract = MetadataAbstract(parent=self)
        self.purpose = MetadataPurpose(parent=self)
        self.tags = MetadataTags(parent=self)
        self.title = MetadataTitle(parent=self)

        self.items.extend([self.abstract, self.purpose, self.tags, self.title])

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

