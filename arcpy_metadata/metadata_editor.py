import os
import arcpy
from metadata_items import *
import xml

from elements import elements
from languages import languages

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

        for name in elements.keys():
            setattr(self, "_%s" % name, None)

            if elements[name]['type'] == "string":
                helper = MetadataHelper(elements[name]['path'], name, self)
                setattr(self, name, MetadataString(helper.value, elements[name]['path'], name, self))

            elif elements[name]['type'] == "date":
                helper = MetadataHelper(elements[name]['path'], name, self)
                setattr(self, name, MetadataDate(helper.value, elements[name]['path'], name, self))

            elif elements[name]['type'] == "integer":
                helper = MetadataHelper(elements[name]['path'], name, self)
                setattr(self, name, MetadataInteger(helper.value, elements[name]['path'], name, self))

            elif elements[name]['type'] == "float":
                helper = MetadataHelper(elements[name]['path'], name, self)
                setattr(self, name, MetadataFloat(helper.value, elements[name]['path'], name, self))

            elif elements[name]['type'] == "list":
                setattr(self, name, MetadataList(elements[name]["tagname"], elements[name]['path'], name, self))

            elif elements[name]['type'] == "language":
                setattr(self, name, MetadataLanguage(elements[name]['path'], name, self))

            elif elements[name]['type'] == "local":
                setattr(self, name, MetadataLocals(elements[name]['path'], name, self))

            elif elements[name]['type'] == "contact":
                setattr(self, name, MetadataContacts(elements[name]['path'], name, self))

            if elements[name] in self.__dict__.keys():
                self.items.append(getattr(self, elements[name]))

        if items:
            self.initialize_items()

    def __setattr__(self, name, value):
        if name in elements.keys():
            if elements[name]['type'] == "string":
                if isinstance(value, MetadataString):
                    self.__dict__["_%s" % name] = value
                elif isinstance(value, str):
                    self.__dict__["_%s" % name] = MetadataString(value, elements[name]["path"], name, self)
                    for i in self.items:
                        if i.name == name:
                            i.value = value
                else:
                    raise RuntimeWarning("Input value must be of type String")

            elif elements[name]['type'] == "date":
                if isinstance(value, MetadataDate):
                    self.__dict__["_%s" % name] = value
                elif isinstance(value, date):
                    self.__dict__["_%s" % name] = MetadataString(value, elements[name]["path"], name, self)
                    for i in self.items:
                        if i.name == name:
                            i.value = date.strftime(value, "%Y%m%d")
                elif isinstance(value, str):
                    try:
                        new_value = datetime.strptime(value, "%Y%m%d").date()
                        self.__dict__["_%s" % name] = MetadataString(new_value, elements[name]["path"], name, self)
                        for i in self.items:
                            if i.name == name:
                                i.value = value
                    except:
                        RuntimeWarning("Input value must be of type a Date or a String ('yyyymmdd')")
                else:
                    raise RuntimeWarning("Input value must be of type a Date or a Sting ('yyyymmdd')")

            elif elements[name]['type'] == "integer":
                if isinstance(value, MetadataInteger):
                    self.__dict__["_%s" % name] = value
                elif isinstance(value, int):
                    self.__dict__["_%s" % name] = MetadataString(value, elements[name]["path"], name, self)
                    for i in self.items:
                        if i.name == name:
                            i.value = value
                elif isinstance(value, str):
                    try:
                        new_value = int(value)
                        self.__dict__["_%s" % name] = MetadataString(new_value, elements[name]["path"], name, self)
                        for i in self.items:
                            if i.name == name:
                                i.value = new_value
                    except:
                        RuntimeWarning("Input value must be of type a Date or a String ('yyyymmdd')")
                else:
                    raise RuntimeWarning("Input value must be of type a Date or a Sting ('yyyymmdd')")

            elif elements[name]['type'] == "float":
                if isinstance(value, MetadataFloat):
                    self.__dict__["_%s" % name] = value

            elif elements[name]['type'] == "list":
                if isinstance(value, MetadataList):
                    self.__dict__["_%s" % name] = value
                elif isinstance(value, list):
                    self.__dict__["_%s" % name].removeall()
                    self.__dict__["_%s" % name].add(value)
                else:
                    raise RuntimeWarning("Input value must be of type list")

            elif elements[name]['type'] == "language":
                if isinstance(value, MetadataLanguage):
                    self.__dict__["_%s" % name] = value
                elif value in languages.keys():
                    pass
                else:
                    raise RuntimeWarning("Input value must be in %s" % str(languages.keys()))

            elif elements[name]['type'] == "local":
                if isinstance(value, MetadataLocals):
                    self.__dict__["_%s" % name] = value
                else:
                    raise RuntimeWarning("Input value must be of type MetadataLocals")

            elif elements[name]['type'] == "contact":
                if isinstance(value, MetadataContacts):
                    self.__dict__["_%s" % name] = value
                else:
                    raise RuntimeWarning("Input value must be of type MetadataContacts")

        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if name in elements.keys():
            return self.__dict__["_%s" % name]
        else:
            return self.__dict__[name]

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
            try:
                print(item.value)
            except:
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