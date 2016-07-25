# TODO: Add category item
# category = dataIdInfo/tpCat/TopicCatCd

elements = {
            "abstract": {
                "path": "dataIdInfo/idAbs",
                "type": "string"},

            "alternative_title": {
                "path": "dataIdInfo/idCitation/resAltTitle",
                "type": "string"},

            "citation": {
                "path": "dataIdInfo/idCitation/otherCitDet",
                "type": "string"},

            "citation_contact": {
                "path": "dataIdInfo/idCitation/citRespParty",
                "type": "contact"},

            "credits": {
                "path": "dataIdInfo/idCredit",
                "type": "string"},

            "distance_resolution": {  # TODO: Allow to add units
                "path": "dataIdInfo/dataScale/scaleDist/value",
                "type": "string"},

            "download": {  # TODO: Allow to add multiple download links with names
                "path": "distInfo/distTranOps/onLineSrc/linkage",
                "type": "string"},

            "extent_description": {
                "path": "dataIdInfo/dataExt/exDesc",
                "type": "string"},

            "external_link": {
                "path": "dataIdInfo/idCitation/citOnlineRes/linkage",
                "type": "string"},

            "language": {
                "path": "dataIdInfo/dataLang",
                "type": "language"},

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
                "type": "contact"},

            "max_scale": {
                "path": "Esri/scaleRange/maxScale",
                "type": "integer"},

            "metadata_language": {
                "path": "dataIdInfo/mdLang",
                "type": "language"},

            "min_scale": {
                "path": "Esri/scaleRange/minScale",
                "type": "integer"},

            "place_keywords": {
                "path": "dataIdInfo/searchKeys[last()]",
                "tagname": "keyword",
                "type": "list"},

            "point_of_contact": {
                "path": "dataIdInfo/idPoC",
                "type": "contact"},

            "purpose": {
                "path": "dataIdInfo/idPurp",
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
                "type": "string"},

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

contact_elements = {
            "role_p": {
                "parent": "element",
                "path": "role"},

            #"role": {
            #    "parent": "role_p",
            #    "path": "RoleCd"},

            "contact_name": {
                "parent": "element",
                "path": "rpIndName"},

            "position": {
                "parent": "element",
                "path": "rpPosName"},

            "organization": {
                "parent": "element",
                "path": "rpOrgName"},

            "contact_info": {
                "parent": "element",
                "path": "rpCntInfo"},

            "address_p": {
                "parent": "contact_info",
                "path": "cntAddress"},

            "email": {
                "parent": "address_p",
                "path": "eMailAdd"},

            "address": {
                "parent": "address_p",
                "path": "delPoint"},

            "city": {
                "parent": "address_p",
                "path": "city"},

            "state": {
                "parent": "address_p",
                "path": "adminArea"},

            "zip": {
                "parent": "address_p",
                "path": "postCode"},

            "country": {
                "parent": "address_p",
                "path": "country"},

            "phone": {
                "parent": "contact_info",
                "path": "cntPhone"},

            "phone_nb": {
                "parent": "phone",
                "path": "voiceNum"},

            "fax_nb": {
                "parent": "phone",
                "path": "faxNum"},

            "hours": {
                "parent": "contact_info",
                "path": "cntHours"},

            "instructions": {
                "parent": "contact_info",
                "path": "cntInstr"},

            "online_resource": {
                "parent": "contact_info",
                "path": "cntOnlineRes"},

            "link": {
                "parent": "online_resource",
                "path": "linkage"},

            "protocol": {
                "parent": "online_resource",
                "path": "protocol"},

            "profile": {
                "parent": "online_resource",
                "path": "appProfile"},

            "or_name": {
                "parent": "online_resource",
                "path": "orName"},

            "or_desc": {
                "parent": "online_resource",
                "path": "orDesc"},

            "or_function": {
                "parent": "online_resource",
                "path": "orFunct"} #,

            #"or_function_cd": {
            #    "parent": "or_function",
            #    "path": "OnFunctCd"}
            }

language_elements = {
            "language": {
                "parent": "element",
                "path": "languageCode"},

            "country": {
                "parent": "element",
                "path": "countryCode"}
            }



