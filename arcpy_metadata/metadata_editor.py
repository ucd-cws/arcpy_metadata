import os
import arcpy

# TODO: reduce dependencies from arcpy
# it is actually only needed to extract metadata from GDB items
# everything else can be done with out the module since metadata are access directly
# if it is a feature class, arcpy can be loaded on demand using importlib
# from importlib import import_module

from arcpy_metadata.metadata_items import MetadataItem
from arcpy_metadata.metadata_items import MetadataList
from arcpy_metadata.metadata_items import MetadataLanguage
from arcpy_metadata.metadata_items import MetadataContact
from arcpy_metadata.metadata_items import MetadataLocals

import xml
import six

from arcpy_metadata.elements import elements
from arcpy_metadata.languages import languages

from datetime import date
from datetime import datetime

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


class MetadataEditor(object):
    """
    The metadata editor
    Create an instance of this object for each metadata file you want to edit
    """

    def __init__(self, dataset=None, metadata_file=None, items=None,
                 temp_folder=metadata_temp_folder):
        if items is None:
            items = list()
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

        for name in elements.keys():
            setattr(self, "_%s" % name, None)

            if elements[name]['type'] in ["string", "date", "integer", "float"]:
                setattr(self, "_{}".format(name), MetadataItem(elements[name]['path'], name, self))
                if self.__dict__["_{}".format(name)].value is not None:
                    setattr(self, name, self.__dict__["_{}".format(name)].value.strip())
                else:
                    setattr(self, name, self.__dict__["_{}".format(name)].value)

            elif elements[name]['type'] == "list":
                setattr(self, "_{}".format(name), MetadataList(elements[name]["tagname"], elements[name]['path'], name, self))
                setattr(self, name, self.__dict__["_{}".format(name)].value)

            elif elements[name]['type'] == "language":
                setattr(self, "_{}".format(name), MetadataLanguage(elements[name]['path'], name, self))
                if self.__dict__["_{}".format(name)].value is not None:
                    setattr(self, name, self.__dict__["_{}".format(name)].value.strip())
                else:
                    setattr(self, name, self.__dict__["_{}".format(name)].value)

            elif elements[name]['type'] == "local":
                setattr(self, name, MetadataLocals(elements[name]['path'], name, self))

            elif elements[name]['type'] == "contact":
                setattr(self, "_{}".format(name), MetadataContact(elements[name]['path'], name, self))
                setattr(self, name, self.__dict__["_{}".format(name)])

            if elements[name] in self.__dict__.keys():
                self.items.append(getattr(self, "_{}".format(elements[name])))

        if items:
            self.initialize_items()

    def __setattr__(self, n, v):

        if n in elements.keys():
            if elements[n]['type'] == "string":
                if isinstance(v, str) or isinstance(v, six.text_type):
                    self.__dict__["_{}".format(n)].value = v
                elif v is None:
                    self.__dict__["_{}".format(n)].value = ""
                else:
                    raise RuntimeWarning("Input value must be of type String")

            elif elements[n]['type'] == "date":
                if isinstance(v, date):
                    self.__dict__["_{}".format(n)].value = date.strftime(v, "%Y%m%d")

                elif isinstance(v, str) or isinstance(v, six.text_type):
                    try:
                        new_value = datetime.strptime(v, "%Y%m%d").date()
                        self.__dict__["_{}".format(n)].value = date.strftime(new_value, "%Y%m%d")

                    except ValueError:
                        RuntimeWarning("Input value must be of type a Date or a String ('yyyymmdd')")
                elif v is None:
                    self.__dict__["_{}".format(n)].value = ""
                else:
                    raise RuntimeWarning("Input value must be of type a Date or a Sting ('yyyymmdd')")

            elif elements[n]['type'] == "integer":
                if isinstance(v, int):
                    self.__dict__["_{}".format(n)].value = str(v)
                elif isinstance(v, str):
                    try:
                        new_value = int(v)
                        self.__dict__["_{}".format(n)].value = str(new_value)
                    except ValueError:
                        RuntimeWarning("Input value must be of type Integer")
                elif v is None:
                    self.__dict__["_{}".format(n)].value = ""
                else:
                    raise RuntimeWarning("Input value must be of type Integer")

            elif elements[n]['type'] == "float":
                if isinstance(v, float):
                    self.__dict__["_{}".format(n)].value = str(v)
                elif isinstance(v, str) or isinstance(v, six.text_type):
                    try:
                        new_value = float(v)
                        self.__dict__["_{}".format(n)].value = str(new_value)
                    except ValueError:
                        RuntimeWarning("Input value must be of type Float")
                elif v is None:
                    self.__dict__["_{}".format(n)].value = ""
                else:
                    raise RuntimeWarning("Input value must be of type Float")

            elif elements[n]['type'] == "list":
                if isinstance(v, list):
                    self.__dict__["_{}".format(n)].value = v
                else:
                    raise RuntimeWarning("Input value must be of type List")

            elif elements[n]['type'] == "language":
                if v in languages.keys():
                    #self.__dict__["_{}".format(n)].value = v
                    self.__dict__["_{}".format(n)].attr_lang = {"value": languages[v][0]}
                    self.__dict__["_{}".format(n)].attr_country = {"value": languages[v][1]}
                    a = 1
                elif v is None:
                    self.__dict__["_{}".format(n)].value = ""
                else:
                    raise RuntimeWarning("Input value must be in {}, an empty String or None".format(str(languages.keys())))

            elif elements[n]['type'] == "local":
                if isinstance(v, MetadataLocals):
                    self.__dict__["_%s" % n] = v
                else:
                    raise RuntimeWarning("Input value must be of type MetadataLocals")

            elif elements[n]['type'] == "contact":
                # if isinstance(v, list):
                #     is_contact = True
                #     for i in v:
                #         print type(i)
                #         if not isinstance(i, MetadataContact):
                #             is_contact = False
                #             break
                #     if is_contact:
                #         self.__dict__["_%s" % n].value = v
                #     else:
                #         raise RuntimeWarning("Input value must be of a List of MetadataContact object")
                # elif v is None:
                #     self.__dict__["_%s" % n].value = []
                if isinstance(v, MetadataContact):
                    self.__dict__["_%s" % n] = v
                else:
                    raise RuntimeWarning("Input value must be a MetadataContact object")

        else:
            self.__dict__[n] = v

    def __getattr__(self, n):
        if n in elements.keys():
            if self.__dict__["_{}".format(n)].value == "" and elements[n]['type'] in ["integer", "float", "date"]:
                return None
            elif elements[n]['type'] == "integer":
                return int(self.__dict__["_{}".format(n)].value)
            elif elements[n]['type'] == "float":
                return float(self.__dict__["_{}".format(n)].value)
            elif elements[n]['type'] == "date":
                return datetime.strptime(self.__dict__["_{}".format(n)].value, "%Y%m%d").date()
            elif elements[n]['type'] == "contact":
                return self.__dict__["_{}".format(n)]
            elif elements[n]['type'] == "language":
                return self.__dict__["_{}".format(n)].get_lang()
            else:
                return self.__dict__["_{}".format(n)].value
        else:
            return self.__dict__["_{}".format(n)]

    def get_datatype(self):
        # get datatype
        desc = arcpy.Describe(self.dataset)
        return desc.dataType

    def get_workspace(self):
        workspace = self.dataset
        desc = arcpy.Describe(workspace)

        while 1 == 1:

            if desc.dataType == "Workspace" or desc.dataType == "Folder":
                return workspace
            else:
                workspace = os.path.dirname(workspace)
                desc = arcpy.Describe(workspace)

    def get_workspace_type(self):
        desc = arcpy.Describe(self._workspace)
        return desc.workspaceType

    def initialize_items(self):
        for item in self.items:
            item.parent = self

    def save(self, Enable_automatic_updates=False):
        logwrite("Saving metadata", True)

        for item in self.items:
            try:
                print(item.value)
            except:
                print(item)

        self.elements.write(self.metadata_file)  # overwrites itself

        if self._workspace_type != 'FileSystem':
            arcpy.ImportMetadata_conversion(self.metadata_file, "FROM_ARCGIS", self.dataset,
                                            Enable_automatic_updates=Enable_automatic_updates)

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

    def finish(self, Enable_automatic_updates=False):
        """
        Alias for saving and cleaning up
        :return:
        """

        self.save(Enable_automatic_updates)
        self.cleanup()
