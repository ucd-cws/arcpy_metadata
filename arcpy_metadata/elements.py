# TODO: Add category item
# category = dataIdInfo/tpCat/TopicCatCd

elements = {
            "abstract": {
                "path": "dataIdInfo/idAbs",
                "type": "string"},

            "citation": {
                "path": "dataIdInfo/idCitation/otherCitDet",
                "type": "string"},

            "citation_contacts": {
                "path": "dataIdInfo/idCitation/citRespParty",
                "type": "contact"},

            "credits": {
                "path": "dataIdInfo/idCredit",
                "type": "string"},

            "extent_description": {
                "path": "dataIdInfo/dataExt/exDesc",
                "type": "string"},

            #"language": {
            #    "path": "dataIdInfo/dataLang",
            #    "type": "language"},

            "last_update": {
                "path": "dataIdInfo/idCitation/date/reviseDate",
                "type": "date"},

            "limitation": {
                "path": "dataIdInfo/resConst/Consts/useLimit",
                "type": "string"},

            #"locals": {
            #    "path": "Esri/locales/locale",
            #    "type": "local"},

            "maintenance_contacts": {
                "path": "dataIdInfo/maintCont",
                "type": "contact"},

            "max_scale": {
                "path": "Esri/scaleRange/maxScale",
                "type": "integer"},

            #"metadata_language": {
            #    "path": "dataIdInfo/mdLang",
            #    "type": "language"},

            "min_scale": {
                "path": "Esri/scaleRange/minScale",
                "type": "integer"},

            "place_keywords": {
                "path": "dataIdInfo/searchKeys[last()]",
                "tagname": "keyword",
                "type": "string"},

            "points_of_contact": {
                "path": "dataIdInfo/idPoC",
                "type": "contact"},

            "purpose": {
                "path": "dataIdInfo/idPurp",
                "type": "string"},

            "scale_resolution": {
                "path": "dataIdInfo/dataScale/equScale/rfDenom",
                "type": "string"},

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

            "update_frequency": {
                "path": "dataIdInfo/resMaint/maintFreq/MaintFreqCd",
                "type": "string"},

            "update_frequency_description": {
                "path": "dataIdInfo/resMaint/usrDefFreq/duration",
                "type": "string"},
            }

contact_elements = {
            "role_p": {
                "type": "string", #
                "parent":"element",
                "path": "role"},

            "role": {
                "type": "string",
                "parent": "role_p",
                "path": "RoleCd"},

            "contact_name": {
                "type": "string",
                "parent": "element",
                "path": "rpIndName"},

            "position": {
                "type": "string",
                "parent": "element",
                "path": "rpPosName"},

            "organization": {
                "type": "string",
                "parent": "element",
                "path": "rpOrgName"},

            "contact_info": {
                "type": "string",
                "parent": "element",
                "path": "rpCntInfo"},

            "address_p": {
                "type": "string", #
                "parent": "contact_info",
                "path": "cntAddress"},

            "email": {
                "type": "string",
                "parent": "contact_info",
                "path": "eMailAdd"},

            "address": {
                "type": "string",
                "parent": "address_p",
                "path": "delPoint"},

            "city": {
                "type": "string",
                "parent": "address_p",
                "path": "City"},

            "state": {
                "type": "string",
                "parent": "address_p",
                "path": "adminArea"},

            "zip": {
                "type": "string",
                "parent": "address_p",
                "path": "postCode"},

            "country": {
                "type": "string",
                "parent": "address_p",
                "path": "country"},

            "phone": {
                "type": "string", #
                "parent": "contact_info",
                "path": "cntPhone"},

            "phone_nb": {
                "type": "string",
                "parent": "phone",
                "path": "voiceNum"},

            "fax_nb": {
                "type": "string",
                "parent": "phone",
                "path": "faxNum"},

            "hours": {
                "type": "string",
                "parent": "contact_info",
                "path": "cntHours"},

            "instructions": {
                "type": "string",
                "parent": "contact_info",
                "path": "cntInstr"},

            "online_resource": {
                "type": "string", #
                "parent": "contact_info",
                "path": "cntOnlineRes"},

            "link": {
                "type": "string",
                "parent": "online_resource",
                "path": "linkage"},

            "protocol": {
                "type": "string",
                "parent": "online_resource",
                "path": "protocol"},

            "profile": {
                "type": "string",
                "parent": "online_resource",
                "path": "appProfile"},

            "or_name": {
                "type": "string",
                "parent": "online_resource",
                "path": "orName"},

            "or_desc": {
                "type": "string",
                "parent": "online_resource",
                "path": "orDesc"},

            "or_function": {
                "type": "string",
                "parent": "online_resource",
                "path": "orFunct"},

            "or_function_cd": {
                "type": "string",
                "parent": "or_function",
                "path": "OnFunctCd"}
            }





