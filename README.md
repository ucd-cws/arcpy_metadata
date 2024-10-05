## DEVELOPMENT HAS MOVED
Future development of this library will now be at [https://github.com/Office-of-Digital-Services/arcpy_metadata](https://github.com/Office-of-Digital-Services/arcpy_metadata), where the library is being maintained.

This repository will be wound down in the future.






# Arcpy Metadata Editor (arcpy_metadata)
Whether you create it or not, metadata is a critical part of GIS analysis. ArcGIS includes a built-in GUI metadata editor, but has scant access to metadata properties from Python. The arcpy_metadata package provides this access, allowing large Python packages that generate their own geospatial outputs in ArcGIS to properly document the data.

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/410cbc590b3c463489fd3a7c786f1f04/badge.svg)](https://www.quantifiedcode.com/app/project/410cbc590b3c463489fd3a7c786f1f04)

## Getting arcpy_metadata
arcpy_metadata is pure Python and its only dependency is arcpy (installed with ArcGIS). It's available on the Python Package Index so you can get arcpy_metadata via pip (pip install arcpy_metadata).
 
If you don't have or don't know how to use pip, you can install arcpy_metadata by cloning/downloading this repository and running setup.py install in the root folder

## Using arcpy_metadata

Creating the Metadata Editor

Edit existing metadata for Shapefiles, Rasters, FeatureClasses, RasterDatasets, MosaicDatasets or Layers
```python
import arcpy_metadata as md
metadata = md.MetadataEditor(path_to_some_feature_class)  # currently supports Shapefiles, FeatureClasses, RasterDatasets and Layers
```


Edit or create an XML file directly
```python
import arcpy_metadata as md
metadata = md.MetadataEditor(metadata_file="path/to/metadata_file.xml")  # currently supports Shapefiles, FeatureClasses, RasterDatasets and Layers
```


Choose your log level
```python
metadata = md.MetadataEditor(path_to_some_feature_class, loglevel="DEBUG")  # use any of CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET, dafault is INFO

```

Get text items (returns string)

```python
title = metadata.title
abstract = metadata.abstract
```

Change text items

```python
metadata.title = "The new title"
metadata.abstract = "This is the abstract"
```

Get list items (returns list)

```python
tags = metadata.tags
for tag in tags:
    print tag
```

Change list items

```python
metadata.tags = ["tag1", "tag2"]
metadata.tags[1] = "another tag"
metadata.tags.append("new tag")
metadata.tags.insert(0, "first tag")
metadata.tags.remove("tag1")
metadata.tags.pop()
```

Get numeric items (return int or float)

```python
min_scale = metadata.min_scale
max_scale = metadata.max_scale
```

Change numeric items 

```python
metadata.min_scale = 500000
metadata.max_scale = 500
```

Get date items (returns date object)

```python
last_update = metadata.last_update
last_update_year = metadata.last_update.year
```

Change date items (excepts datetime objects and formated string (yyyymmdd, yyyy-mm-ddThh:mm:ss)

```python
from datetime import date
today = date.today()
metadata.last_update = today
metadata.last_update = "20160221"
```

Add and edit field definitions
```python
metadata.fields.new()  # add the new field
metadata.fields[-1].name = "MyFieldName" # the item at index -1 will be the new one
metadata.fields[-1].definition = "Here I am describing how the field was created and how to use and interpret its values for a reader"

# or find an existing field and update its definition
search_for_field = "OBJECTID"
for field in metadata.fields:
    if field.name == search_for_field:
        field.definition = "Some updated information about the field defintiion"
        break  # not necessary, but faster as it stops searching once you've found the field

```

Get contact items (returns contact object)

```python
contact = metadata.point_of_contact
contact_name = metadata.point_of_contact.contact_name
contact_email = metadata.point_of_contact.email
```

Change contact items (all contact items are string)

```python
metadata.point_of_contact.contact_name = "First and Last Name"
metadata.point_of_contact.email = "email@address.com"
```

Edited nested lists
```python
# make sure you have the right number of elements
# add new ones
while metadata.online_resource < 3:
    metadata.online_resource.new()
# or delete spare once
while metadata.online_resource > 3:
	metadata.online_resource.pop()
	
metadata.online_resource[0].name = "First download link"
metadata.online_resource[0].link = "http://somelink"
metadata.online_resource[0].function = "download"
metadata.online_resource[1].name = "Second download link"
metadata.online_resource[1].link = "http://someotherlink"
metadata.online_resource[1].function = "download"
metadata.online_resource[2].name = "Third download link"
metadata.online_resource[2].link = "http://yetanotherdownloadlink"
metadata.online_resource[2].function = "download"
```
Remove all items from the geoprocessing history
```python
metadata.rm_gp_history()
```

Saving the changes back to the file

```python
metadata.save() # save the metadata back to file.
metadata.cleanup() # remove all temporary files.
```
or
```
metadata.finish()  # save() and cleanup() as one call
```
If you want to enable automatic updates of your metadata (feature classes only) call.
```python
metadata.finish(True) 
```

## Supported items

|Item description|Internal name|Type|Catalog Edit View|Path in ArcGIS XML file|
|---|---|---|---|---|
|Title|title|String|Overview/ Item Description/ Title|dataIdInfo/idCitation/resTitle|
|Abstract|abstract|String|Overview/ Item Description/ Description|dataIdInfo/idAbs|
|Purpose|purpose|String|Overview/ Item Description/ Summery|dataIdInfo/idPurp|
|Tags|tags|List|Overview/ Item Description/ Tags|dataIdInfo/searchKeys/keyword|
|Place Keywords|place_keywords|List|Overview/ Topics & Keywords/ Place Keyword|dataIdInfo/placeKeys/keyword|
|Extent Description|extent_description|String|Resource/ Extents/ Extent/ Description|dataIdInfo/dataExt/exDesc|
|Temporal Extent Description|temporal_extent_description|String|   |dataIdInfo/dataExt/tempDesc|
|Temporal Extent Instance|temporal_extent_instance|Date|Resource/ Extents/ Temporal Instance Extent/ Instance Date|dataIdInfo/dataExt/tempEle/exTemp/TM_Instant/tmPosition|
|Temporal Extent Start Date|temporal_extent_start|Date|Resource/ Extents/ Temporal Period Extent/ Begin Date|dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmBegin|
|Temporal Extent End Date|temporal_extent_end|Date|Resource/ Extents/ Temporal Period Extent/ End Date|dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmEnd|
|Minimum Scale|min_scale|Integer|Item Description/ Appropriate Scale Range/ Min Scale|Esri/scaleRange/minScale|
|Maximum Scale|max_scale|Integer|Item Description/ Appropriate Scale Range/ Max Scale|Esri/scaleRange/maxScale|
|Scale Resolution|scale_resolution|Integer|Resource/ Details/ Scale Resolution|dataIdInfo/dataScale/equScale/rfDenom|
|Last Update|last_update|Date|Overview/ Citation/ Dates/ Revised|dataIdInfo/idCitation/date/reviseDate|
|Update Frequency Description|update_frequency_description|String|Resource/ Maintenance/ Custom Frequency|dataIdInfo/resMaint/usrDefFreq/duration|
|Credits|credits|String|Overview/ Item Description/ Credits|dataIdInfo/idCredit|
|Citation|citation|String|Overview/ Citation/ Other Details|dataIdInfo/idCitation/otherCitDet|
|Limitation|limitation|String|Overview/ Item Description/ Use Limitation|dataIdInfo/resConst/Consts/useLimit|
|Supplemental Information|supplemental_information|String|Resource/ Supplemental Information|dataIdInfo/suppInfo|
|Source|source|String|Resource/ Lineage/ Data Source/ Source Description|dqInfo/dataLineage/dataSource/srcDesc|
|Points of contact|point_of_contact|ContactObj|Resource/ Details/ Points of Contact/ Contact/|dataIdInfo/idPoC|
|Maintenance Contacts|maintenance_contact|ContactObj|Resource/ Maintenance/ Maintenance Contact/|dataIdInfo/maintCont|
|Citation Contacts|citation_contact|ContactObj|Overview/ Citation Contact/ Contact/|dataIdInfo/idCitation/citRespParty|
|Language|language|String|Resource/ Detail/ Languages/ Language|dataIdInfo/dataLang|
|Metadata Language|metadata_language|String|Metadata/ Detail/ Language|dataIdInfo/mdLang|
|Alternate Title|alternate_title|String|Overview/Citation/Titles/Alternate Title|dataIdInfo/idCitation/resAltTitle|
|Identifier Code (1)|identifier_code1|String|Overview/Citation/Identifier/Code|dataIdInfo/idCitation/citId/identCode|
|Identifier Code (2)|identifier_code2|String|Overview/Citation/Identifier/Authority Citation/Identifier/Code|dataIdInfo/idCitation/citId/identAuth/citId/identCode|
|Identifier Code (3)|identifier_code3|String|Overview/Citation/Identifier/Authority Citation/Identifier/Authority Citation/Identifier/Code|dataIdInfo/idCitation/citId/identAuth/citId/identAuth/citId/identCode|
|Identifier Code (4)|identifier_code4|String|Resource/Lineage/Data Source/Reference System/Authority Citation/Identifier/Code|dqInfo/dataLineage/dataSource/srcRefSys/identAuth/citId/identCode|
|Metadata File Identifier|file_identifier|String|Metadata/Details/File Idnetifier|mdFileID|
|Dataset URI|dataset_uri|String|Metadata/Details/Dataset URI|dataSetURI|
|Resource Label|resource_label|String|Resource/Fields/Details/Label|eainfo/detailed/enttyp/enttypl|
|Format|format|String|Resource/Distribution/Distribution Format/Format Name|distInfo/distFormat/formatName|
|Field|attr|FieldObj|Resource/Fields/Entity and Attribute Information/Details|eainfo/detailed/attr|

### Field items
|Item description|Internal name|Type|Relative path in ArcGIS XML file|
|---|---|---|---|
|Field Name|name|String|./attrlabl|
|Field Definition|definition|String|./attrdef|


### Contact items
|Item description|Internal name|Type|Relative path in ArcGIS XML file|
|---|---|---|---|
|Contact Name|contact_name|String|./rpIndName|
|Position|position|String|./rpPosName|
|Organization|organization|String|./rpOrgName|
|Email|email|String|./rpCntInfo/eMailAdd|
|Address|address|String|./rpCntInfo/cntAddress/delPoint|
|City|city|String|rpCntInfo/./cntAddress/City|
|State|state|String|rpCntInfo/./cntAddress/adminArea|
|Zip|zip|String|rpCntInfo/./cntAddress/postCode|
|Country|country|String|./rpCntInfo/cntAddress/country|
|Phone Nb|phone_nb|String|./rpCntInfo/cntPhone/voiceNum|
|Fax Nb|fax_nb|String|./rpCntInfo/cntPhone/faxNum|
|Hours|hours|String|./rpCntInfo/cntHours|
|Instructions|instructions|String|./rpCntInfo/cntInstr|
|Website Link|link|String|./rpCntInfo/cntOnlineRes/linkage|
|Protocol|protocol|String|./rpCntInfo/cntOnlineRes/protocol|
|Profile|profile|String|./rpCntInfo/cntOnlineRes/appProfile|
|Website Name|or_name|String|./rpCntInfo/cntOnlineRes/orName|
|Website Description|or_desc|String|./rpCntInfo/cntOnlineRes/orDesc|

### Online Resource Items
|Item description|Internal name|Type|Relative path in ArcGIS XML file|
|---|---|---|---|
|Link|link|String|./linkage|
|Protocol|protocol|String|./protocol|
|Profile|profile|String|./appProfile|
|Name|name|String|./orName|
|Description|description|String|./orDesc|
|Function|function|String|./orFunct/OnFunctCd|

Don't see the item you need? Read more about how to extend arcpy_metadata to work with other metadata elements it doesn't yet handle in [CONTRIBUTING.md](CONTRIBUTING.md).

## Python and ArcGIS Support
arcpy_metadata version 1.x supports Python 3 and ArcGIS Pro only.

arcpy_metadata version 0.x runs on Python 2 and 3, which means it can, at a basic level, be used both with ArcMap and ArcGIS Pro. When 0.x was developed, ArcGIS Pro didn't yet have some of the metadata export functions that arcpy_metadata relies on though, so, as of version 0.5, you *must* specify a path to a metadata XML file, or use a dataset that already has its metadata in an accessible XML format (e.g. Shapefile), if you want to use that branch in ArcGIS Pro. Otherwise, for ArcGIS Pro, upgrade to version 1.x.

## Under the hood
arcpy_metadata uses the strategy of exporting the metadata from the layer, then edits the xml export based on your method calls. When you're done, use finish() to save your data back to the source.


## Known limitations
Does not yet support all metadata items. Work is in progress to support server-based dataset editing.

### Legacy ArcMap Versions
arcpy_metadata version 0.x only works with 32-bit Python. We use arcpy.XSLTransform_conversion() to extract metadata from geodatabases. 64bit arcpy python bindings for background processing [do not support](http://desktop.arcgis.com/en/arcmap/latest/analyze/executing-tools/64bit-background.htm) tools inside the metadata conversion toolset. arcpy_metadata version 1.x for ArcGIS Pro does
not have these limitations.


## How to contribute or extend arcpy_metadata
Contributions are well come! Please fork and submit pull requests.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to extend arcpy_metadata to new attributes


## Acknowledgements
arcpy_metadata is maintained by Nick Santos at the California Department of Technology.

arcpy_metadata was initially a project of the [UC Davis Center for Watershed Sciences](https://watershed.ucdavis.edu) and received significant contributions from the [World Resources Institute](https://www.wri.org). It was created as part of a larger project funded by the California Department of Fish and Wildlife [Biogeographic Data Branch](http://www.dfg.ca.gov/biogeodata/) and further developed for [Global Forest Watch](https://www.globalforestwatch.org). We thank our funders for their support and their commitment to high quality geospatial data.

