Arcpy Metadata Editor (arcpy_metadata)
==============
Whether you create it or not, metadata is a critical part of GIS analysis. ArcGIS includes a built-in GUI metadata editor, but has scant access to metadata properties from Python. The arcpy_metadata package provides this access, allowing large Python packages that generate their own geospatial outputs in ArcGIS to properly document the data.

Getting arcpy_metadata
----------------------
arcpy_metadata is pure Python and its only dependency is arcpy (installed with ArcGIS). It's available on the Python Package Index so you can get arcpy_metadata via pip (pip install arcpy_metadata).
 
If you don't have or don't know how to use pip, you can install arcpy_metadata by cloning/downloading this repository and running setup.py install in the root folder

Using arcpy_metadata
--------------------

Creating the Metadata Editor

```python
import arcpy_metadata as md
metadata = md.MetadataEditor(path_to_some_feature_class)  # currently supports Shapefiles, FeatureClasses, RasterDatasets and Layers
```

Get simple items

```python
metadata.title.get()
metadata.abstract.get()
```

Change simple items

```python
metadata.title.set("The new title")
metadata.abstract.set("This is the abstract")
```

Adding text to a simple item

```python
metadata.abstract.append("\nThis is the second line of the abstract")
metadata.abstract.prepend("This line is goes right before the first line\n")
```

Adding new items to multi items

```python
metadata.tags.append("New Keyword")
metadata.tags.add(["Another keyword", "One more keyword"])
```

Removing items from multi items

```python
metadata.tags.remove("New Keyword")
metadata.tags.removeall()
```

Lists

```python
list = metadata.language.get_list_values()
metadata.language.set(list[0])
```

Complex items

```python
metadata.points_of_contact.add()
metadata.points_of_contact[0].contact_name.set("Contact name")

metadata.points_of_contact[0].email.get()
metadata.points_of_contact[0].email[0].set("email1@domain.org")
metadata.points_of_contact[0].email.append("emai2@domain.org")
```

Saving the changes back to the file

```python
metadata.finish()  # save the metadata back to the original source feature class and cleanup. Without calling finish(), your edits are NOT saved!
```
The code is based on a set of core classes that provide set/append/prepend operations, and we would love pull requests that add classes or attributes to cover additional portions of metadata specs.


Supported items
---------------

|Item Description|internal name|type|location in Arc Catalog|path in ArcGIS XML file|
|---|---|---|---|---|
|Title|title|simple|Overview/ Item Description/ Title|dataIdInfo/idCitation/resTitle|
|Abstract|abstract|simple|Overview/ Item Description/ Description|dataIdInfo/idAbs|
|Locales|locals|complex|Overview/Locales/#language/..|Esri/locales/locale|
|Purpose|purpose|simple|Overview/ Item Description/ Summery|dataIdInfo/idPurp|
|Tags|tags|multi|Overview/ Item Description/ Tags|dataIdInfo/searchKeys/keyword|
|Place Keywords|place_keywords|multi|Overview/ Topics & Keywords/ Place Keyword|dataIdInfo/placeKeys/keyword|
|Extent Description|extent_description|simple|Resource/ Extents/ Extent/ Description|dataIdInfo/dataExt/exDesc|
|Temporal Extent Description|temporal_extent_description|simple|   |dataIdInfo/dataExt/tempDesc|
|Temporal Extent Instance|temporal_extent_instance|simple|Resource/ Extents/ Temporal Instance Extent/ Instance Date|dataIdInfo/dataExt/tempEle/exTemp/TM_Instant/tmPosition|
|Temporal Extent Start Date|temporal_extent_start|simple|Resource/ Extents/ Temporal Period Extent/ Begin Date|dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmBegin|
|Temporal Extent End Date|temporal_extent_end|simple|Resource/ Extents/ Temporal Period Extent/ End Date|dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmEnd|
|Minimum Scale|min_scale|simple|Item Description/ Appropriate Scale Range/ Min Scale|Esri/scaleRange/minScale|
|Maximum Scale|max_scale|simple|Item Description/ Appropriate Scale Range/ Max Scale|Esri/scaleRange/maxScale|
|Last Update|last_update|simple|Overview/ Citation/ Dates/ Revised|dataIdInfo/idCitation/date/reviseDate|
|Update Frequency|update_frequency|list|Resource/ Maintenance/ Update Frequency|dataIdInfo/resMaint/maintFreq/MaintFreqCd|
|Update Frequency Description|update_frequency_description|simple|Resource/ Maintenance/ Custom Frequency|dataIdInfo/resMaint/usrDefFreq/duration|
|Credits|credits|simple|Overview/ Item Description/ Credits|dataIdInfo/idCredit|
|Citation|citation|simple|Overview/ Citation/ Other Details|dataIdInfo/idCitation/otherCitDet|
|Limitation|limitation|simple|Overview/ Item Description/ Use Limitation|dataIdInfo/resConst/Consts/useLimit|
|Source|source|simple|Resource/ Lineage/ Data Source/ Source Description|dqInfo/dataLineage/dataSource/srcDesc|
|Points of contact|points_of_contact|complex|Resource/ Points of Contact/ Contact/...|dataIdInfo/idPoC|
|Maintenance Contacts|maintenance_contacts|complex|Resource/ Maintenance/ Maintenance Contact/...|dataIdInfo/maintCont|
|Citation Contacts|citation_contacts|complex|Overview/ Citation Contact/ Contact/...|dataIdInfo/idCitation/citRespParty|
|Language|language|list|Resource/ Detail/ Languages/ Language|dataIdInfo/dataLang|
|Metadata Language|metadata_language|list|Metadata/ Detail/ Language|dataIdInfo/mdLang|



Under the hood
---------------
arcpy_metadata uses the strategy of exporting the metadata from the layer, then edits the xml export based on your method calls. When you're done, use finish() to save your data back to the source.

Acknowledgements
----------------
arcpy_metadata is a project of the [UC Davis Center for Watershed Sciences](https://watershed.ucdavis.edu) with contributions from the [World Resources Institute](www.wri.org). It was initially created as part of a larger project funded by the California Department of Fish and Wildlife [Biogeographic Data Branch](http://www.dfg.ca.gov/biogeodata/) and further developed for [Global Forest Watch](www.globalforestwatch.org). We thank our donors for their support and their commitment to high quality geospatial data.
