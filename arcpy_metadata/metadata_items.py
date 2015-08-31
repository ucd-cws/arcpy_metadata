__author__ = 'Thomas.Maschler'

from __init__ import MetadataItem
from __init__ import MetadataMulti


class MetadataTitle(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.path = "dataIdInfo/idCitation/resTitle"
        self.name = "title"
        super(MetadataTitle, self).__init__(parent)

class MetadataAbstract(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "abstract"
        self.path = "dataIdInfo/idAbs"
        super(MetadataAbstract, self).__init__(parent)


class MetadataPurpose(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "purpose"
        self.path = "dataIdInfo/idPurp"
        super(MetadataPurpose, self).__init__(parent)


class MetadataTags(MetadataMulti):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "tags"
        super(MetadataTags, self).__init__(parent, tagname="keyword", path="dataIdInfo/searchKeys[last()]")


class MetadataPlaceKeywords(MetadataMulti):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "place_keywords"
        super(MetadataPlaceKeywords, self).__init__(parent, tagname="keyword", path="dataIdInfo/placeKeys[last()]")


class MetadataExtentDescription(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "extent_description"
        self.path = "dataIdInfo/dataExt/exDesc"
        super(MetadataExtentDescription, self).__init__(parent)


class MetadataTemporalExtentDescription(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "temporal_extent_description"
        self.path = "dataIdInfo/dataExt/tempDesc"  # CHECK AGAIN IF THIS IS RIGHT
        super(MetadataTemporalExtentDescription, self).__init__(parent)


class MetadataTemporalExtentInstance(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "temporal_extent_instance"
        self.path = "dataIdInfo/dataExt/tempEle/exTemp/TM_Instant/tmPosition"
        super(MetadataTemporalExtentInstance, self).__init__(parent)


class MetadataTemporalExtentStart(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "temporal_extent_start"
        self.path = "dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmBegin"
        super(MetadataTemporalExtentStart, self).__init__(parent)


class MetadataTemporalExtentEnd(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "temporal_extent_end"
        self.path = "dataIdInfo/dataExt/tempEle/exTemp/TM_Period/tmEnd"
        super(MetadataTemporalExtentEnd, self).__init__(parent)


class MetadataMinScale(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "min_scale"
        self.path = "Esri/scaleRange/minScale"
        super(MetadataMinScale, self).__init__(parent)


class MetadataMaxScale(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "max_scale"
        self.path = "Esri/scaleRange/maxScale"
        super(MetadataMaxScale, self).__init__(parent)


class MetadataLastUpdate(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "last_update"
        self.path = "dataIdInfo/idCitation/date/reviseDate"
        super(MetadataLastUpdate, self).__init__(parent)


class MetadataUpdateFrequency(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "update_frequency"
        self.path = "dataIdInfo/resMaint/maintFreq/MaintFreqCd"
        super(MetadataUpdateFrequency, self).__init__(parent)


class MetadataUpdateFrequencyDescription(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "update_frequency_description"
        self.path = "dataIdInfo/resMaint/usrDefFreq/duration"
        super(MetadataUpdateFrequencyDescription, self).__init__(parent)


class MetadataCredits(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "credits"
        self.path = "dataIdInfo/idCredit"
        super(MetadataCredits, self).__init__(parent)


class MetadataCitation(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation"
        self.path = "dataIdInfo/idCitation/otherCitDet"
        super(MetadataCitation, self).__init__(parent)


class MetadataLimitation(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "limitation"
        self.path = "dataIdInfo/resConst/Consts/useLimit"
        super(MetadataLimitation, self).__init__(parent)


class MetadataSource(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "source"
        self.path = "dqInfo/dataLineage/dataSource/srcDesc"
        super(MetadataSource, self).__init__(parent)

#The following items have special attributs and need a seperate Metadata Item class

# title_local = Esri, locales, locale, resTitle
# description_local = Esri, locales, locale, idAbs
# language = dataIdInfo, dataLang, languageCode
# lang_country = dataIdInfo, dataLang, languageCode
# category = dataIdInfo, tpCat, TopicCatCd
#
# contact_wri_name = dataIdInfo, idPoC, rpIndName
# contact_wri_org = dataIdInfo, idPoC, rpOrgName
# contact_wri_pos = dataIdInfo, idPoC, rpPosName
# contact_wri_role = dataIdInfo, idPoC, role, RoleCd
# contact_wri_adress = dataIdInfo,idPoC, rpCntInfo, cntAddress, delPoint
# contact_wri_city = dataIdInfo, idPoC, rpCntInfo, cntAddress, City
# contact_wri_state = dataIdInfo, idPoC, rpCntInfo, cntAddress, adminArea
# contact_wri_postalcode = dataIdInfo, idPoC, rpCntInfo, cntAddress, postCode
# contact_wri_email = dataIdInfo, idPoC, rpCntInfo, cntAddress, eMailAdd
# contact_wri_country = dataIdInfo, idPoC, rpCntInfo, cntAddress, country
# contact_wri_phone = dataIdInfo, idPoC, rpCntInfo, cntPhone, voiceNum
#
# contact_tec_name = dataIdInfo, maintCont, rpIndName
# contact_tec_org = dataIdInfo, maintCont, rpOrgName
# contact_tec_pos = dataIdInfo, maintCont, rpPosName
# contact_tec_role = dataIdInfo, maintCont, role, RoleCd
# contact_tec_adress = dataIdInfo, maintCont, rpCntInfo, cntAddress, delPoint
# contact_tec_city = dataIdInfo, maintCont, rpCntInfo, cntAddress, City
# contact_tec_state = dataIdInfo, maintCont, rpCntInfo, cntAddress, adminArea
# contact_tec_postalcode = dataIdInfo, maintCont, rpCntInfo, cntAddress, postCode
# contact_tec_email = dataIdInfo, maintCont, rpCntInfo, cntAddress, eMailAdd
# contact_tec_country = dataIdInfo, maintCont, rpCntInfo, cntAddress, country
# contact_tec_phone = dataIdInfo, maintCont, rpCntInfo, cntPhone, voiceNum
#
# contact_owner_name = dataIdInfo, idCitation, citRespParty, rpIndName
# contact_owner_org = dataIdInfo, idCitation, citRespParty, rpOrgName
# contact_owner_pos = dataIdInfo, idCitation, citRespParty, rpPosName
# contact_owner_rol = dataIdInfo, idCitation, citRespParty, role, RoleCd
# contact_owner_adress = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntAddress, delPoint
# contact_owner_city = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntAddress, City
# contact_owner_state = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntAddress, adminArea
# contact_owner_postalcode = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntAddress, postCode
# contact_owner_email = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntAddress, eMailAdd
# contact_owner_country = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntAddress, country
# contact_owner_phone = dataIdInfo, idCitation, citRespParty, rpCntInfo, cntPhone, voiceNum