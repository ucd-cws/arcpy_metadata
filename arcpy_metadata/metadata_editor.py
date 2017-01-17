import os
import arcpy
import xml
import six
import warnings
import traceback

from datetime import date
from datetime import datetime

from arcpy_metadata.metadata_constructors import MetadataItem
from arcpy_metadata.metadata_constructors import MetadataValueList
from arcpy_metadata.metadata_constructors import MetadataParentItem
from arcpy_metadata.metadata_constructors import MetadataObjectList
from arcpy_metadata.metadata_constructors import MetadataValueListHelper
from arcpy_metadata.metadata_constructors import MetadataObjectListHelper

from arcpy_metadata.metadata_items import MetadataLanguage

from arcpy_metadata.elements import elements
from arcpy_metadata.languages import languages

# turn on warnings for deprecation once
warnings.simplefilter('once', DeprecationWarning)
# Make warnings look nice
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '{}: {}\n'.format(category.__name__, message)
warnings.formatwarning = warning_on_one_line

# TODO: Convert to using logging or logbook - probably logging to keep dependencies down
try:  # made as part of a larger package - using existing logger, but logging to screen for now if not in that package
    from log import write as logwrite
    from log import warning as logwarning
except ImportError:
    def logwrite(log_string, autoprint=1):  # match the signature of the expected log function
        print(log_string)

    def logwarning(log_string):
        print("WARNING: {0:s}".format(log_string))


install_dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
xslt = os.path.join(install_dir, r"Metadata\Stylesheets\gpTools\exact copy of.xslt")
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
        self._simple_datasets = ["ShapeFile", "RasterDataset", "Layer"]
        self._layers = ["FeatureLayer"]

        if self.dataset:  # Check if dataset is set
            # export the metadata to the temporary location
            self.data_type = self.get_datatype()

            # for layers get the underlying dataset and start over
            if self.data_type in self._layers:
                desc = arcpy.Describe(self.dataset)
                self.data_type = desc.dataElement.dataType
                self.dataset = desc.dataElement.catalogPath  # overwrite path to dataset with layer's data source

            self._workspace = self.get_workspace()
            self._workspace_type = self.get_workspace_type()

            # Datasets in Filesystem have metadata attached as XML file
            # we can directly write to it
            if self._workspace_type == 'FileSystem':
                if self.data_type in self._simple_datasets:
                    xml_file = self.dataset + ".xml"
                    #if no XML file exists create one and add most basic metadata item to it
                    if not os.path.exists(xml_file):
                        self._create_xml_file(xml_file)
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
                    logwrite("Exporting metadata to temporary file {0!s}".format(self.metadata_file))
                    arcpy.XSLTransform_conversion(self.dataset, xslt, self.metadata_file)
                else:
                    raise TypeError("Datatype is not supported")

        elif self.metadata_file:  # Check if metadata file is set instead
            if self.metadata_file.endswith('.xml'):
                if not os.path.exists(self.metadata_file):
                    self._create_xml_file(self.metadata_file)
                self._workspace_type = 'FileSystem'
            else:
                raise TypeError("Metadata file is not an XML file. Check file extension")

        self.elements.parse(self.metadata_file)

        # create these all after the parsing happens so that if they have any self initialization, they can correctly perform it

        for name in elements.keys():
            if "sync" in elements[name].keys():
                sync = elements[name]["sync"]
            else:
                sync = True
            setattr(self, "_{0!s}".format(name), None)

            if elements[name]['type'] in ["string", "date", "integer", "float"]:
                setattr(self, "_{}".format(name), MetadataItem(elements[name]['path'], name, self, sync))
                if self.__dict__["_{}".format(name)].value is not None:
                    setattr(self, name, self.__dict__["_{}".format(name)].value.strip())
                else:
                    setattr(self, name, self.__dict__["_{}".format(name)].value)

            elif elements[name]['type'] == "list":
                setattr(self, "_{}".format(name), MetadataValueList(elements[name]["tagname"], elements[name]['path'], name, self, sync))
                #setattr(self, name, self.__dict__["_{}".format(name)].value)
                #setattr(self, name, ListValues(self.__dict__["_{}".format(name)], name))

            elif elements[name]['type'] == "language":
                setattr(self, "_{}".format(name), MetadataLanguage(elements[name]['path'], name, self, sync))
                if self.__dict__["_{}".format(name)].value is not None:
                    setattr(self, name, self.__dict__["_{}".format(name)].value.strip())
                else:
                    setattr(self, name, self.__dict__["_{}".format(name)].value)

            elif elements[name]['type'] == "parent_item":
                setattr(self, "_{}".format(name), MetadataParentItem(elements[name]['path'], self, elements[name]['elements']))
                setattr(self, name, self.__dict__["_{}".format(name)])

            elif elements[name]['type'] == "object_list":
                setattr(self, "_{}".format(name), MetadataObjectList(elements[name]["tagname"], elements[name]['path'], self, elements[name]['elements'], sync))
                #setattr(self, name, self.__dict__["_{}".format(name)])

            if elements[name] in self.__dict__.keys():
                self.items.append(getattr(self, "_{}".format(elements[name])))

        if items:
            self.initialize_items()


    @staticmethod
    def _create_xml_file(xml_file):
        with open(xml_file, "w") as f:
            logwrite("Create new file {0!s}".format(xml_file))
            f.write('<metadata xml:lang="en"></metadata>')


    def __setattr__(self, n, v):
        """
        Check if input value type matches required type for metadata element
        and write value to internal property
        :param n: string
        :param v: string
        :return:
        """

        if n in elements.keys():

            # Warn if property got deprecated, but only if call is made by user, not during initialization
            if "deprecated" in elements[n].keys() and traceback.extract_stack()[-2][2] != "__init__":
                warnings.warn("Call to deprecated property {}. {}".format(n, elements[n]["deprecated"]), category=DeprecationWarning)

            if elements[n]['type'] == "string":
                if isinstance(v, (str, six.text_type)):
                    self.__dict__["_{}".format(n)].value = v
                elif v is None:
                    self.__dict__["_{}".format(n)].value = ""
                else:
                    raise RuntimeWarning("Input value must be of type String")

            elif elements[n]['type'] == "date":
                if isinstance(v, date):
                    self.__dict__["_{}".format(n)].value = date.strftime(v, "%Y%m%d")

                elif isinstance(v, (str, six.text_type)):
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
                elif isinstance(v, (str, six.text_type)):
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
                    #self.__dict__[n].value = ListValues(self.__dict__["_{}".format(n)], v)
                    self.__dict__["_{}".format(n)].value = v
                elif isinstance(v, MetadataValueListHelper):
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

            elif elements[n]['type'] == "parent_item":
                if isinstance(v, MetadataParentItem):
                    self.__dict__["_{0!s}".format(n)] = v
                else:
                    raise RuntimeWarning("Input value must be a MetadataParentItem object")

            elif elements[n]['type'] == "object_list":
                if isinstance(v, list):
                    self.__dict__["_{}".format(n)].value = v
                elif isinstance(v, MetadataObjectList):
                    self.__dict__["_{}".format(n)].value = v
                else:
                    raise RuntimeWarning("Input value must be a MetadataOnlineResource object")

        else:
            self.__dict__[n] = v

    def __getattr__(self, n):
        """
        Type cast output values according to required element type
        :param n: string
        :return:
        """
        if n in elements.keys():

            # Warn if property got deprecated
            if "deprecated" in elements[n].keys():
                warnings.warn("Call to deprecated property {}. {}".format(n, elements[n]["deprecated"]), category=DeprecationWarning)

            if self.__dict__["_{}".format(n)].value == "" and elements[n]['type'] in ["integer", "float", "date"]:
                return None
            elif elements[n]['type'] == "integer":
                return int(self.__dict__["_{}".format(n)].value)
            elif elements[n]['type'] == "float":
                return float(self.__dict__["_{}".format(n)].value)
            elif elements[n]['type'] == "date":
                return datetime.strptime(self.__dict__["_{}".format(n)].value, "%Y%m%d").date()
            elif elements[n]['type'] == "parent_item":
                return self.__dict__["_{}".format(n)]
            elif elements[n]['type'] == "language":
                return self.__dict__["_{}".format(n)].get_lang()
            elif elements[n]['type'] == "list":
                return MetadataValueListHelper(self.__dict__["_{}".format(n)])
            elif elements[n]['type'] == "object_list":
                return MetadataObjectListHelper(self.__dict__["_{}".format(n)])
            else:
                return self.__dict__["_{}".format(n)].value
        else:
            return self.__dict__["_{}".format(n)]

    def get_datatype(self):
        """
        Get ArcGIS datatype datatype of current dataset
        :return:
        """
        # get datatype
        desc = arcpy.Describe(self.dataset)
        return desc.dataType

    def get_workspace(self):
        """
        Find the workspace for current dataset
        In case, base directory is not a workspace (ie when feature class is located in a feature dataset)
        check next lower base directory of current base directory until criteria matches
        :return:
        """
        workspace = self.dataset
        desc = arcpy.Describe(workspace)

        while 1 == 1:

            if desc.dataType == "Workspace" or desc.dataType == "Folder":
                return workspace
            else:
                workspace = os.path.dirname(workspace)
                if workspace == '' and arcpy.env.workspace:
                    return arcpy.env.workspace
                desc = arcpy.Describe(workspace)

    def get_workspace_type(self):
        """
        Get ArcGIS Workspace type for current dataset
        :return:
        """
        desc = arcpy.Describe(self._workspace)
        return desc.workspaceType

    def initialize_items(self):
        """
        Initialize all items
        :return:
        """
        for item in self.items:
            item.parent = self

    def rm_gp_history(self):
        """
        Remove all items form the geoprocessing history
        :return:
        """
        element = self.elements.find("Esri/DataProperties/lineage")
        if element is not None:
            i = 0
            children = element.findall("Process")
            for child in children:
                element.remove(child)
                i += 1
            logwrite("Remove {} item(s) from the geoprocessing history".format(i), True)
        else:
            logwrite("There are no items in the geoprocessing history", True)


    def save(self, Enable_automatic_updates=False):
        """
        Save pending edits to file
        If feature class, import temporary XML file back into GDB

        :param Enable_automatic_updates: boolean
        :return:
        """
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

    def cleanup(self):
        """
        Remove all temporary files
        :return:
        """
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
        :param Enable_automatic_updates: boolean
        :return:
        """
        self.save(Enable_automatic_updates)
        self.cleanup()
