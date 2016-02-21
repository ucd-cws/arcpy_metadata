Arcpy Metadata Editor (arcpy_metadata)
==============
Whether you create it or not, metadata is a critical part of GIS analysis. ArcGIS includes a built-in GUI metadata editor, but has scant access to metadata properties from Python. The arcpy_metadata package provides this access, allowing large Python packages that generate their own geospatial outputs in ArcGIS to properly document the data.

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/410cbc590b3c463489fd3a7c786f1f04/badge.svg)](https://www.quantifiedcode.com/app/project/410cbc590b3c463489fd3a7c786f1f04)

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

Change date items (takes both date objects and formated string (yyyymmdd)

```python
from datetime import date
today = date.today()
metadata.last_update = today
metadata.last_update = "20160221"
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

Saving the changes back to the file

```python
metadata.finish()  # save the metadata back to the original source feature class and cleanup. Without calling finish(), your edits are NOT saved!
```
The code is based on a set of core classes that provide set/append/prepend operations, and we would love pull requests that add classes or attributes to cover additional portions of metadata specs.


Supported items
---------------

|Item description|Internal name|Type|Location in ArcCatalog|Path in ArcGIS XML file|
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
|Scale Resolution|scale_resolution|String|Resource/ Details/ Scale Resolution|dataIdInfo/dataScale/equScale/rfDenom|
|Last Update|last_update|Date|Overview/ Citation/ Dates/ Revised|dataIdInfo/idCitation/date/reviseDate|
|Update Frequency|update_frequency|String|Resource/ Maintenance/ Update Frequency|dataIdInfo/resMaint/maintFreq/MaintFreqCd|
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

Contact items
---------------
|Item description|Internal name|Type|Relative path in ArcGIS XML file|
|---|---|---|---|
|Role|role|String|role/RoleCd|
|Contact Name|contact_name|String|rpIndName|
|Position|position|String|rpPosName|
|Organization|organization|String|rpOrgName|
|Email|email|String|rpCntInfo/eMailAdd|
|Address|address|String|rpCntInfo/cntAddress/delPoint|
|City|city|String|rpCntInfo/cntAddress/City|
|State|state|String|rpCntInfo/cntAddress/adminArea|
|Zip|zip|String|rpCntInfo/cntAddress/postCode|
|Country|country|String|rpCntInfo/cntAddress/country|
|Phone Nb|phone_nb|String|rpCntInfo/cntPhone/voiceNum|
|Fax Nb|fax_nb|String|rpCntInfo/cntPhone/faxNum|
|Hours|hours|String|rpCntInfo/cntHours|
|Instructions|instructions|String|rpCntInfo/cntInstr|
|Website Link|link|String|rpCntInfo/cntOnlineRes/linkage|
|Protocol|protocol|String|rpCntInfo/cntOnlineRes/protocol|
|Profile|profile|String|rpCntInfo/cntOnlineRes/appProfile|
|Website Name|or_name|String|rpCntInfo/cntOnlineRes/orName|
|Website Description|or_desc|String|rpCntInfo/cntOnlineRes/orDesc|
|Website Function|or_function_cd|String|rpCntInfo/cntOnlineRes/orFunct/OnFunctCd|


Under the hood
---------------
arcpy_metadata uses the strategy of exporting the metadata from the layer, then edits the xml export based on your method calls. When you're done, use finish() to save your data back to the source.


Known limitations
---------------
Does not yet support all metadata items.

Currently only works with 32-bit Python. Module crashes under 64-bit Python due to a bug in arcpy (v10.3.1), when using arcpy.XSLTransform_conversion().


Acknowledgements
----------------
arcpy_metadata is a project of the [UC Davis Center for Watershed Sciences](https://watershed.ucdavis.edu) with contributions from the [World Resources Institute](www.wri.org). It was initially created as part of a larger project funded by the California Department of Fish and Wildlife [Biogeographic Data Branch](http://www.dfg.ca.gov/biogeodata/) and further developed for [Global Forest Watch](www.globalforestwatch.org). We thank our donors for their support and their commitment to high quality geospatial data.
