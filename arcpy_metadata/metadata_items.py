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


# ############## Point of Contact

class MetadataPointOfContactRole(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_role"
        self.path = "dataIdInfo/idPoC/role/RoleCd"
        super(MetadataPointOfContactRole, self).__init__(parent)
        self.attributes = {"value": "005"}


class MetadataPointOfContactName(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_name"
        self.path = "dataIdInfo/idPoC/rpIndName"
        super(MetadataPointOfContactName, self).__init__(parent)


class MetadataPointOfContactPosition(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_position"
        self.path = "dataIdInfo/idPoC/rpPosName"
        super(MetadataPointOfContactPosition, self).__init__(parent)


class MetadataPointOfContactOrganization(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_organization"
        self.path = "dataIdInfo/idPoC/rpOrgName"
        super(MetadataPointOfContactOrganization, self).__init__(parent)


class MetadataPointOfContactAddressType(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_address_type"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']"
        super(MetadataPointOfContactAddressType, self).__init__(parent)
        self.attributes = {"addressType": "postal"}


class MetadataPointOfContactAddress(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_address"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']/delPoint"
        super(MetadataPointOfContactAddress, self).__init__(parent)


class MetadataPointOfContactZIP(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_zip"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']/postCode"
        super(MetadataPointOfContactZIP, self).__init__(parent)


class MetadataPointOfContactCity(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_city"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']/city"
        super(MetadataPointOfContactCity, self).__init__(parent)


class MetadataPointOfContactState(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_state"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']/adminArea"
        super(MetadataPointOfContactState, self).__init__(parent)


class MetadataPointOfContactCountry(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_country"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']/country"
        super(MetadataPointOfContactCountry, self).__init__(parent)


class MetadataPointOfContactEmail(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_email"
        self.path = "dataIdInfo/idPoC/cntAddress[@addressType='postal']/eMailAdd"
        super(MetadataPointOfContactEmail, self).__init__(parent)


class MetadataPointOfContactPhone(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "poc_phone"
        self.path = "dataIdInfo/idPoC/cntPhone/voiceNum"
        super(MetadataPointOfContactPhone, self).__init__(parent)


# ############# Data Maintenance Contact
class MetadataDataMaintenanceRole(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_role"
        self.path = "dataIdInfo/maintCont/role/RoleCd"
        super(MetadataDataMaintenanceRole, self).__init__(parent)
        self.attributes = {"value": "005"}


class MetadataDataMaintenanceName(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_name"
        self.path = "dataIdInfo/maintCont/rpIndName"
        super(MetadataDataMaintenanceName, self).__init__(parent)


class MetadataDataMaintenancePosition(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_role"
        self.path = "dataIdInfo/maintCont/rpPosName"
        super(MetadataDataMaintenancePosition, self).__init__(parent)


class MetadataDataMaintenanceOrganization(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_organization"
        self.path = "dataIdInfo/maintCont/rpOrgName"
        super(MetadataDataMaintenanceOrganization, self).__init__(parent)


class MetadataDataMaintenanceAddressType(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_address_type"
        self.path = "dataIdInfo/maintCont/cntAddress"
        super(MetadataDataMaintenanceAddressType, self).__init__(parent)
        self.attributes = {"addressType": "postal"}


class MetadataDataMaintenanceAddress(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_address"
        self.path = "dataIdInfo/maintCont/cntAddress/delPoint"
        super(MetadataDataMaintenanceAddress, self).__init__(parent)


class MetadataDataMaintenanceZIP(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_zip"
        self.path = "dataIdInfo/maintCont/cntAddress/postCode"
        super(MetadataDataMaintenanceZIP, self).__init__(parent)


class MetadataDataMaintenanceCity(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_city"
        self.path = "dataIdInfo/maintCont/cntAddress/city"
        super(MetadataDataMaintenanceCity, self).__init__(parent)


class MetadataDataMaintenanceState(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_state"
        self.path = "dataIdInfo/maintCont/cntAddress/adminArea"
        super(MetadataDataMaintenanceState, self).__init__(parent)


class MetadataDataMaintenanceCountry(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_country"
        self.path = "dataIdInfo/maintCont/cntAddress/country"
        super(MetadataDataMaintenanceCountry, self).__init__(parent)


class MetadataDataMaintenanceEmail(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_email"
        self.path = "dataIdInfo/maintCont/cntAddress/eMailAdd"
        super(MetadataDataMaintenanceEmail, self).__init__(parent)


class MetadataDataMaintenancePhone(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_phone"
        self.path = "dataIdInfo/maintCont/cntPhone/voiceNum"
        super(MetadataDataMaintenancePhone, self).__init__(parent)


# ############### Citation Contact

class MetadataCitationContactRole(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_role"
        self.path = "dataIdInfo/idCitation/citRespParty/role/RoleCd"
        super(MetadataCitationContactRole, self).__init__(parent)
        self.attributes = {"value": "010"}


class MetadataCitationContactName(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_name"
        self.path = "dataIdInfo/idCitation/citRespParty/rpIndName"
        super(MetadataCitationContactName, self).__init__(parent)


class MetadataCitationContactPosition(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_role"
        self.path = "dataIdInfo/idCitation/citRespParty/rpPosName"
        super(MetadataCitationContactPosition, self).__init__(parent)


class MetadataCitationContactOrganization(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_organization"
        self.path = "dataIdInfo/idCitation/citRespParty/rpOrgName"
        super(MetadataCitationContactOrganization, self).__init__(parent)


class MetadataCitationContactAddressType(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_address_type"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress"
        super(MetadataCitationContactAddressType, self).__init__(parent)
        self.attributes = {"addressType": "postal"}


class MetadataCitationContactAddress(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_address"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress/delPoint"
        super(MetadataCitationContactAddress, self).__init__(parent)


class MetadataCitationContactZIP(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_zip"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress/postCode"
        super(MetadataCitationContactZIP, self).__init__(parent)


class MetadataCitationContactCity(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_city"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress/city"
        super(MetadataCitationContactCity, self).__init__(parent)


class MetadataCitationContactState(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_state"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress/adminArea"
        super(MetadataCitationContactState, self).__init__(parent)


class MetadataCitationContactCountry(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_country"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress/country"
        super(MetadataCitationContactCountry, self).__init__(parent)


class MetadataCitationContactEmail(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_email"
        self.path = "dataIdInfo/idCitation/citRespParty/cntAddress/eMailAdd"
        super(MetadataCitationContactEmail, self).__init__(parent)


class MetadataCitationContactPhone(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_phone"
        self.path = "dataIdInfo/idCitation/citRespParty/cntPhone/voiceNum"
        super(MetadataCitationContactPhone, self).__init__(parent)











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