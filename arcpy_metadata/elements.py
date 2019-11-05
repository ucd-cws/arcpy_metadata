contact_elements = {

    "role": {
        "path": "role/RoleCd",
        "type": "attribute",
        "key": "value",
        "values": [("resource provider", "001"),
                   ("custodian", "002"),
                   ("owner", "003"),
                   ("user", "004"),
                   ("distributer", "005"),
                   ("originator", "006"),
                   ("point of contact", "007"),
                   ("principal investigator", "008"),
                   ("processor", "009"),
                   ("publisher", "010"),
                   ("author", "011")]},

    "contact_name": {
        "path": "rpIndName",
        "type": "string"},

    "position": {
        "path": "rpPosName",
        "type": "string"},

    "organization": {
        "path": "rpOrgName",
        "type": "string"},

    "contact_info": {
        "path": "rpCntInfo",
        "type": "string"},

    "email": {
        "path": "rpCntInfo/cntAddress/eMailAdd",
        "type": "string"},

    "address_type": {
        "path": "rpCntInfo/cntAddress",
        "type": "attribute",
        "key": "addressType",
        "values": [("postal", "postal"),
                   ("physical", "physical"),
                   ("both", "both")]},

    "address": {
        "path": "rpCntInfo/cntAddress/delPoint",
        "type": "string"},

    "city": {
        "path": "rpCntInfo/cntAddress/city",
        "type": "string"},

    "state": {
        "path": "rpCntInfo/cntAddress/adminArea",
        "type": "string"},

    "zip": {
        "path": "rpCntInfo/cntAddress/postCode",
        "type": "string"},

    "country": {
        "path": "rpCntInfo/cntAddress/country",
        "type": "string"},  # TODO: make this a dropdown list for ISO2 code. Write to value

    "phone_nb": {
        "path": "rpCntInfo/voiceNum",
        "type": "string"},

    "fax_nb": {
        "path": "rpCntInfo/faxNum",
        "type": "string"},

    "hours": {
        "path": "rpCntInfo/cntHours",
        "type": "string"},

    "instructions": {
        "path": "rpCntInfo/cntInstr",
        "type": "string"},

    # TODO: Make Online Resources a sub elemennt list
    "link": {
        "path": "rpCntInfo/cntOnlineRes/linkage",
        "type": "string"},

    "protocol": {
        "path": "rpCntInfo/cntOnlineRes/protocol",
        "type": "string"},

    "profile": {
        "path": "rpCntInfo/cntOnlineRes/appProfile",
        "type": "string"},

    "or_name": {
        "path": "rpCntInfo/cntOnlineRes/orName",
        "type": "string"},

    "or_desc": {
        "path": "rpCntInfo/cntOnlineRes/orDesc",
        "type": "string"},

    "or_function": {
        "path": "orFunct/OnFunctCd",
        "type": "attribute",
        "key": "value",
        "values": [("download", "001"),
                   ("information", "002"),
                   ("offline access", "003"),
                   ("order", "004"),
                   ("search", "005")]
    }
}

online_resource_elements = {
    "link": {
        "path": "linkage",
        "type": "string"},
    "protocol": {
        "path": "protocol",
        "type": "string"},
    "profile": {
        "path": "appProfile",
        "type": "string"},
    "name": {
        "path": "orName",
        "type": "string"},
    "description": {
        "path": "orDesc",
        "type": "string"},

    "function": {
        "path": "orFunct/OnFunctCd",
        "type": "attribute",
        "key": "value",
        "values": [("download", "001"),
                   ("information", "002"),
                   ("offline access", "003"),
                   ("order", "004"),
                   ("search", "005")]
    },
}

elements = {
    "abstract": {
        "path": "dataIdInfo/idAbs",
        "type": "string"},

    "alternate_title": {
        "path": "dataIdInfo/idCitation/resAltTitle",
        "type": "string"},

    # TODO: Add category item
    # category = dataIdInfo/tpCat/TopicCatCd

    "citation": {
        "path": "dataIdInfo/idCitation/otherCitDet",
        "type": "string"},

    "citation_contact": {
        "path": "dataIdInfo/idCitation",
        "tagname": "citRespParty",
        "type": "object_list",
        "elements": contact_elements},

    "credits": {
        "path": "dataIdInfo/idCredit",
        "type": "string"},

    "dataset_uri": {
        "path": "dataSetURI",
        "type": "string"},

    "distance_resolution": {  # TODO: Allow to add units
        "path": "dataIdInfo/dataScale/scaleDist/value",
        "type": "string"},

    "download": {  #
        "path": "distInfo/distTranOps/onLineSrc/linkage",
        "type": "string",
        "deprecated": "Use online_resource instead"},

    "extent_description": {
        "path": "dataIdInfo/dataExt/exDesc",
        "type": "string"},

    "external_link": {
        "path": "dataIdInfo/idCitation/citOnlineRes/linkage",
        "type": "string"},

    "format": {
        "path": "distInfo/distFormat/formatName",
        "type": "string"
    },

    "file_identifier": {
        "path": "mdFileID",
        "type": "string",
        #"sync": False,
        "unsupported": ["FeatureClass", "Table", "RasterDataset", "RasterCatalog", "MosaicDataset"]
    },

    "identifier_code1": {
        "path": "dataIdInfo/idCitation/citId/identCode",
        "type": "string"},

    "identifier_code2": {
        "path": "dataIdInfo/idCitation/citId/identAuth/citId/identCode",
        "type": "string"},

    "identifier_code3": {
        "path": "dataIdInfo/idCitation/citId/identAuth/citId/identAuth/citId/identCode",
        "type": "string"},

    "identifier_code4": {
        "path": "dqInfo/dataLineage/dataSource/srcRefSys/identAuth/citId/identCode",
        "type": "string"},

    "language": {
        "path": "dataIdInfo/dataLang/languageCode",
        "type": "attribute",
        "key": "value",
        "values": [("english", "eng"),
                   ("spanish", "spa"),
                   ("french", "fre")]
    },

    "last_update": {
        "path": "dataIdInfo/idCitation/date/reviseDate",
        "type": "datetime"},

    "license": {
        "path": "dataIdInfo/resConst/LegConsts/useLimit",
        "type": "string"},

    "limitation": {  #TODO: does read correctly when entered though ArcGIS Online. They are stored in a seperated resConst element
        "path": "dataIdInfo/resConst/Consts/useLimit",
        "type": "string"},

    #"locals": {
    #    "path": "Esri/locales/locale",
    #    "type": "local"},

    "maintenance_contact": {
        "path": "dataIdInfo/maintCont",
        "type": "parent_item",
        "elements": contact_elements},

    "max_scale": {
        "path": "Esri/scaleRange/maxScale",
        "type": "integer"},

    "metadata_language": {
        "path": "dataIdInfo/mdLang/languageCode",
        "type": "attribute",
        "key": "value",
        "values": [("english", "eng"),
                   ("spanish", "spa"),
                   ("french", "fre")]
    },

    "meta_style": {
        "path": "Esri/ArcGISstyle",
        "type": "string"},

    "meta_create_date": {
        "path": "Esri/CreaDate",
        "type": "date"},

    "meta_create_time": {
        "path": "Esri/CreaTime",
        "type": "time"},

    "meta_modification_date": {
        "path": "Esri/ModDate",
        "type": "date"},

    "meta_modification_time": {
        "path": "Esri/ModTime",
        "type": "time"},

    "meta_format": {
        "path": "Esri/ArcGISFormat",
        "type": "string"},

    "meta_profile": {
        "path": "Esri/ArcGISProfile",
        "type": "string"},

    "meta_publish_status": {
        "path": "Esri/PublishStatus",
        "type": "string"},

    "min_scale": {
        "path": "Esri/scaleRange/minScale",
        "type": "integer"},

    "online_resource": {
        "path": "distInfo/distTranOps",
        "tagname": "onLineSrc",
        "type": "object_list",
        "elements": online_resource_elements},

    "place_keywords": {
        "path": "dataIdInfo/placeKeys",
        "tagname": "keyword",
        "type": "list"},

    "point_of_contact": {
        "path": "dataIdInfo/idPoC",
        "type": "parent_item",
        "elements": contact_elements},

    "pub_date": {
        "path": "dataIdInfo/idCitation/date/pubDate",
        "type": "datetime"},

    "purpose": {
        "path": "dataIdInfo/idPurp",
        "type": "string"},

    "resource_label": {
        "path": "eainfo/detailed/enttyp/enttypl",
        "type": "string"},

    "scale_resolution": {
        "path": "dataIdInfo/dataScale/equScale/rfDenom",
        "type": "integer"},

    "source": {
        "path": "dqInfo/dataLineage/dataSource/srcDesc",
        "type": "string"},

    "supplemental_information": {
        "path": "dataIdInfo/suppInfo",
        "type": "string"},

    "title": {
        "path": "dataIdInfo/idCitation/resTitle",
        #"path": "Esri/DataProperties/itemProps/itemName",
        "type": "string",
        "sync": False},

    "tags": {
        "path": "dataIdInfo/searchKeys[last()]",
        "tagname": "keyword",
        "type": "list"},

    "temporal_extent_description": {
        "path": "dataIdInfo/dataExt/tempDesc",
        "type": "string"},

    "temporal_extent_end": {
        "path": "dataIdInfo/dataExt/tempEle/TempExtent/exTemp/TM_Period/tmEnd",
        "type": "datetime"},

    "temporal_extent_instance": {
        "path": "dataIdInfo/dataExt/tempEle/TempExtent/exTemp/TM_Instant/tmPosition",
        "type": "datetime"},

    "temporal_extent_start": {
        "path": "dataIdInfo/dataExt/tempEle/TempExtent/exTemp/TM_Period/tmBegin",
        "type": "datetime"},

    "update_frequency": {
        "path": "dataIdInfo/resMaint/maintFreq/MaintFreqCd",
        "type": "attribute",
        "key": "value",
        "values": [("continual", "001"),
                   ("daily", "002"),
                   ("weekly", "003"),
                   ("fortnightly", "004"),
                   ("monthly", "005")]},

    "update_frequency_description": {
        "path": "dataIdInfo/resMaint/usrDefFreq/duration",
        "type": "string"}

}
