contact_elements = {
    #"role_p": {
    #    "parent": "element",
    #    "path": "role"},

    "role": {
        "parent": "role_p",
        "path": "role/RoleCd",
        "type": "string"},

    "contact_name": {
        "parent": "element",
        "path": "rpIndName",
        "type": "string"},

    "position": {
        "parent": "element",
        "path": "rpPosName",
        "type": "string"},

    "organization": {
        "parent": "element",
        "path": "rpOrgName",
        "type": "string"},

    "contact_info": {
        "parent": "element",
        "path": "rpCntInfo",
        "type": "string"},

    #"address_p": {
    #    "parent": "contact_info",
    #    "path": "rpCntInfo/cntAddress"},

    "email": {
        "parent": "address_p",
        "path": "rpCntInfo/cntAddress/eMailAdd",
        "type": "string"},

    "address": {
        "parent": "address_p",
        "path": "rpCntInfo/cntAddress/delPoint",
        "type": "string"},

    "city": {
        "parent": "address_p",
        "path": "rpCntInfo/cntAddress/city",
        "type": "string"},

    "state": {
        "parent": "address_p",
        "path": "rpCntInfo/cntAddress/adminArea",
        "type": "string"},

    "zip": {
        "parent": "address_p",
        "path": "rpCntInfo/cntAddress/postCode",
        "type": "string"},

    "country": {
        "parent": "address_p",
        "path": "rpCntInfo/cntAddress/country",
        "type": "string"},

    "phone": {
        "parent": "contact_info",
        "path": "rpCntInfo/cntPhone",
        "type": "string"},

    "phone_nb": {
        "parent": "phone",
        "path": "rpCntInfo/voiceNum",
        "type": "string"},

    "fax_nb": {
        "parent": "phone",
        "path": "rpCntInfo/faxNum",
        "type": "string"},

    "hours": {
        "parent": "contact_info",
        "path": "rpCntInfo/cntHours",
        "type": "string"},

    "instructions": {
        "parent": "contact_info",
        "path": "rpCntInfo/cntInstr",
        "type": "string"},

    "online_resource": {
        "parent": "contact_info",
        "path": "rpCntInfo/cntOnlineRes",
        "type": "string"},

    "link": {
        "parent": "online_resource",
        "path": "rpCntInfo/cntOnlineRes/linkage",
        "type": "string"},

    "protocol": {
        "parent": "online_resource",
        "path": "rpCntInfo/cntOnlineRes/protocol",
        "type": "string"},

    "profile": {
        "parent": "online_resource",
        "path": "rpCntInfo/cntOnlineRes/appProfile",
        "type": "string"},

    "or_name": {
        "parent": "online_resource",
        "path": "rpCntInfo/cntOnlineRes/orName",
        "type": "string"},

    "or_desc": {
        "parent": "online_resource",
        "path": "rpCntInfo/cntOnlineRes/orDesc",
        "type": "string"},

    "or_function": {
        "parent": "element",
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

language_elements = {
    "language": {
        "parent": "element",
        "path": "languageCode",
        "type": "string"},

    "country": {
        "parent": "element",
        "path": "countryCode",
        "type": "string"}
}

online_resource_elements = {
    "link": {
        "parent": "element",
        "path": "linkage",
        "type": "string"},
    "protocol": {
        "parent": "element",
        "path": "protocol",
        "type": "string"},
    "profile": {
        "parent": "element",
        "path": "appProfile",
        "type": "string"},
    "or_name": {
        "parent": "element",
        "path": "orName",
        "type": "string"},
    "description": {
        "parent": "element",
        "path": "orDesc",
        "type": "string"},

    "function": {
        "parent": "element",
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
        "path": "dataIdInfo/idCitation/citRespParty",
        "type": "parent_item",
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
        "path": "",
        "type": "distInfo/distFormat/formatName"
    },

    "file_identifier": {
        "path": "mdFileID",
        "type": "string"},

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
        "path": "dataIdInfo/dataLang",
        "type": "language",
        "elements": language_elements},

    "last_update": {
        "path": "dataIdInfo/idCitation/date/reviseDate",
        "type": "date"},

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
        "path": "dataIdInfo/mdLang",
        "type": "language"},

    "min_scale": {
        "path": "Esri/scaleRange/minScale",
        "type": "integer"},

    "online_resource": {
        "path": "distInfo/distTranOps",
        "tagname": "onLineSrc",
        "type": "object_list",
        "elements": online_resource_elements},

    "place_keywords": {
        "path": "dataIdInfo/searchKeys[last()]",
        "tagname": "keyword",
        "type": "list"},

    "point_of_contact": {
        "path": "dataIdInfo/idPoC",
        "type": "parent_item",
        "elements": contact_elements},

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
        "path": "dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmEnd",
        "type": "date"},

    "temporal_extent_instance": {
        "path": "dataIdInfo/dataExt/tempEle/exTemp/TM_Instant/tmPosition",
        "type": "date"},

    "temporal_extent_start": {
        "path": "dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmBegin",
        "type": "date"},

    #"update_frequency": {
    #    "path": "dataIdInfo/resMaint/maintFreq/MaintFreqCd",
    #    "type": "string"},

    "update_frequency_description": {
        "path": "dataIdInfo/resMaint/usrDefFreq/duration",
        "type": "string"}

}



