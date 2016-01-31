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
            "language": {
                "path": "dataIdInfo/dataLang",
                "type": "language"},

            "last_update": {
                "path": "dataIdInfo/idCitation/date/reviseDate",
                "type": "string"},

            "limitation": {
                "path": "dataIdInfo/resConst/Consts/useLimit",
                "type": "string"},

            "locals": {
                "path": "Esri/locales/locale",
                "type": "local"},

            "maintenance_contacts": {
                "path": "dataIdInfo/maintCont",
                "type": "contact"},

            "max_scale": {
                "path": "max_scale",
                "type": "string"},

            "metadata_language": {
                "path": "dataIdInfo/mdLang",
                "type": "language"},

            "min_scale": {
                "path": "min_scale",
                "type": "string"},

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
                "type": "string"},

            "temporal_extent_instance": {
                "path": "dataIdInfo/dataExt/tempEle/exTemp/TM_Instant/tmPosition",
                "type": "string"},

            "temporal_extent_start": {
                "path": "dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmBegin",
                "type": "string"},

            "update_frequency": {
                "path": "dataIdInfo/resMaint/maintFreq/MaintFreqCd",
                "type": "string"},

            "update_frequency_description": {
                "path": "dataIdInfo/resMaint/usrDefFreq/duration",
                "type": "string"},
            }







