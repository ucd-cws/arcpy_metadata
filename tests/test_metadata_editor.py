from __future__ import print_function

import unittest
import os
import sys
import distutils
from distutils import dir_util
import tempfile
import arcpy
import gc
import inspect # allow to test arcpy_metadata even when it is not installed as module
from datetime import date
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import arcpy_metadata as md

# import test element dictionary
from test_elements import test_elements


class TestMetadataWriteRead(unittest.TestCase):
    """
    To start with, let's just get a simple test in that tests the code from the perspective of how someone might use it.
    We'll do that by running the example code, which should certainly run.
    """

    def __init__(self, testcases):
        self.temp_data_folder = None
        super(TestMetadataWriteRead, self).__init__(testcases)

    def setUp(self):
        original_test_data_folder = os.path.join(os.path.dirname(__file__), "test_data")
        self.temp_data_folder = tempfile.mkdtemp("arcpy_metadata_unit_tests")
        distutils.dir_util.copy_tree(original_test_data_folder, self.temp_data_folder)

    def tearDown(self):
        arcpy.env.workspace = self.temp_data_folder
        done = True
        # delete all datasets
        datasets = arcpy.ListDatasets()
        for dataset in datasets:
            arcpy.Delete_management(dataset)

        # delete all workspaces
        workspaces = arcpy.ListWorkspaces()
        for workspace in workspaces:

            #clear all locks
            arcpy.Exists(workspace)
            arcpy.Compact_management(workspace)
            arcpy.Exists(workspace)
            try:
                arcpy.Delete_management(workspace)
            except arcpy.ExecuteError:
                print("cannot delete {} due to lock".format(workspace))
                done = False

        # delete directory with all remaining files
        if done:
            distutils.dir_util.remove_tree(self.temp_data_folder)


    @staticmethod
    def _write_metadata(data_set):
        """
        Write test values to metadata
        :param data_set: 
        :return: 
        """
        metadata = md.MetadataEditor(data_set, loglevel="DEBUG")
        # also has a feature_layer parameter if you're working with one, but edits get saved back to the source feature class

        for key in test_elements.keys():
            if hasattr(metadata, key):
                # write simple elements directly to property
                if not isinstance(test_elements[key], (list, dict, )):
                    setattr(metadata, key, test_elements[key])

                # for nested elements loop over children and write to properties of parent element
                if isinstance(test_elements[key], dict):
                    item = getattr(metadata, key)
                    for k in test_elements[key].keys():
                        setattr(item, k, test_elements[key][k])

                # for list elements loop either over children and write to properties of parent element or write entire list to property
                if isinstance(test_elements[key], list):
                    if isinstance(test_elements[key][0], dict):
                        item = getattr(metadata, key)
                        i = 0
                        while len(item) < len(test_elements[key]):
                            item.new()
                        while len(item) > len(test_elements[key]):
                            item.pop()
                        for element in test_elements[key]:
                            for k in element.keys():
                                setattr(item[i], k, test_elements[key][i][k])
                            i += 1
                    else:
                        setattr(metadata, key, test_elements[key])

            else:
                print("{} does not exist. SKIP".format(key))

        metadata.save()  # save the metadata back to the original source feature class and cleanup. Without calling finish(), your edits are NOT saved!

        del metadata
        gc.collect()

    def _read_metadata(self, dataset):
        """
        Read previously saved metadata and compare with orininal values
        :param dataset: 
        :return: 
        """
        metadata = md.MetadataEditor(dataset, loglevel="DEBUG")

        # Loop over all elements listed in test_elements to check if values were correctly saved
        for key in test_elements.keys():
            if hasattr(metadata, key):
                item = getattr(metadata, key)

                # simple elements (text, numeric, date)
                if not isinstance(test_elements[key], (list, dict)):

                    # convert date back to string
                    if isinstance(item, (datetime, date)):
                        if len(test_elements[key]) == 8:
                            test_date = datetime.strptime(test_elements[key], "%Y%m%d")
                        else:
                            test_date = datetime.strptime(test_elements[key], "%Y-%m-%dT%H:%M:%S")

                        print("{}: before = {}; after = {}".format(key,test_date,item))

                        self.assertEqual(item, test_date,
                                     'Value for element {} was not correctly saved'.format(key))

                    else:
                        print("{}: before = {}; after = {}".format(key, test_elements[key], item))
                        self.assertEqual(item, test_elements[key],
                                     'Value for element {} was not correctly saved'.format(key))

                # parent items (eg contacts)
                elif isinstance(test_elements[key], dict):
                    for k in test_elements[key].keys():
                        child = test_elements[key][k]
                        print("{}.{}: before = {}; after = {}".format(key, k, child, getattr(item, k)))
                        self.assertEqual(getattr(item, k), child,
                                         'Value for element {}.{} was not correctly saved'.format(key, k))

                # lists
                elif isinstance(test_elements[key], list):
                    # nested lists
                    if isinstance(test_elements[key][0], dict):

                        # make sure both lists are sorted in the same way
                        keys = test_elements[key][0].keys()
                        sorted_items = sorted(item, key=lambda x: (getattr(x, keys[0]), getattr(x, keys[1])))
                        sorted_elements = sorted(test_elements[key], key=lambda x: (x[keys[0]], x[keys[1]]))

                        i = 0
                        for sub_element in sorted_elements:
                            for k in sub_element:
                                child = sub_element[k]
                                print("{}[{}].{}: before = {}; after = {}".format(key, i, k, child, getattr(sorted_items[i], k)))
                                self.assertEqual(getattr(sorted_items[i], k), child,
                                                 'Value for element {}[{}].{} was not correctly saved'.format(key, i, k))
                            i += 1
                    # simple lists
                    else:
                        print("{}: before = {}; after = {}".format(key, test_elements[key], item))
                        self.assertEqual(item.sort(), test_elements[key].sort(),
                                         'Value for element {} was not correctly saved'.format(key))

            else:
                print("{} does not exist. SKIP".format(key))

        del metadata
        gc.collect()

    # TODO: make sure, GDB locks get properly remove to be able to run all test directly after another.
    #       Deleting the metadata object and running the Garbage Collector doesn't seem to do anything
    #       Right now you have to run test separately ( Makes sense, since you have to check the metadata manually)

    def test_shapefile_no_meta(self):
        print('\n----------------------')
        print("Shp without metadata")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, "simple_poly_no_metadata.shp"))
        self._read_metadata(os.path.join(self.temp_data_folder, "simple_poly_no_metadata.shp"))

    def test_shapefile_with_meta(self):
        print('\n----------------------')
        print("Shp with metadata")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, "simple_poly_w_base_metadata.shp"))
        self._read_metadata(os.path.join(self.temp_data_folder, "simple_poly_w_base_metadata.shp"))

    def test_shapefile_without_xml(self):
        print('\n----------------------')
        print("Shp without XML File")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, "simple_poly_no_xml.shp"))
        self._read_metadata(os.path.join(self.temp_data_folder, "simple_poly_no_xml.shp"))

    def test_feature_class_no_meta(self):
        print('\n----------------------')
        print("FC without metadata")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, "test.gdb", "root_poly"))
        self._read_metadata(os.path.join(self.temp_data_folder, "test.gdb", "root_poly"))

    def test_feature_class_with_meta(self):
        print('\n----------------------')
        print("FC in dataset with metadata")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, "test.gdb", "dataset", "dataset_poly"))
        self._read_metadata(os.path.join(self.temp_data_folder, "test.gdb", "dataset", "dataset_poly"))

    def test_gdb_table(self):
        print('\n----------------------')
        print("Table no metadata")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, "test.gdb", "root_table"))
        self._read_metadata(os.path.join(self.temp_data_folder, "test.gdb", "root_table"))

    def test_fc_layer(self):
        print('\n----------------------')
        print("Feature class layer")
        print('----------------------')
        arcpy.MakeFeatureLayer_management(os.path.join(self.temp_data_folder, "test.gdb", "root_poly"), "layer")
        self._write_metadata("layer")
        self._read_metadata("layer")

    def test_layer_file(self):
        print('\n----------------------')
        print("Layer file metadata")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, r"layer.lyr"))
        self._read_metadata(os.path.join(self.temp_data_folder, r"layer.lyr"))

    def test_raster_dataset(self):
        print('\n----------------------')
        print("Raster dataset")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, r"test.gdb\simple_raster"))
        self._read_metadata(os.path.join(self.temp_data_folder, r"test.gdb\simple_raster"))

    def test_raster_file(self):
        print('\n----------------------')
        print("Raster file")
        print('----------------------')
        self._write_metadata(os.path.join(self.temp_data_folder, r"simple_raster.tif"))
        self._read_metadata(os.path.join(self.temp_data_folder, r"simple_raster.tif"))



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMetadataWriteRead)
    unittest.TextTestRunner(verbosity=2).run(suite)

#     unittest.main()