__author__ = 'Thomas.Maschler'


from __init__ import MetadataItem
from __init__ import MetadataString
from __init__ import MetadataMulti
from __init__ import MetadataItems
from __init__ import MetadataParentItem


language_codes = {"english": ["eng", "US"],
                  "french": ["fre", "FR"],
                  "spanish": ["spa", "ES"]}


# ########## General Info

class MetadataStringHelper(MetadataItem):
    def __init__(self, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataStringHelper, self).__init__(parent)


class MetadataTitle(MetadataString):
    """
        Just a shortcut MetadataItem that predefines the paths
    """

    def __init__(self, value=None, parent=None, path="dataIdInfo/idCitation/resTitle", name="title"):
        self.path = path
        self.name = name

        super(MetadataTitle, self).__init__(value, parent)


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


# ########## Keywords

# TODO: Add category item
# category = dataIdInfo/tpCat/TopicCatCd

class MetadataTags(MetadataMulti):
    """
        Just a shortcut MetadataMulti that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "tags"
        super(MetadataTags, self).__init__(parent, tagname="keyword", path="dataIdInfo/searchKeys[last()]")


class MetadataPlaceKeywords(MetadataMulti):
    """
        Just a shortcut MetadataMulti that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "place_keywords"
        super(MetadataPlaceKeywords, self).__init__(parent, tagname="keyword", path="dataIdInfo/placeKeys[last()]")


class MetadataLanguage(MetadataParentItem):
    """
        A MetadataParentItem for Language settings
        Each Language Item has two children
         - Language
         - Country
        Predefined language pairs are stored in the global language_code dictionary
    """

    def __init__(self, parent, path):

        self.parent = parent
        self.path = path

        super(MetadataLanguage, self).__init__(self.parent)

        self._language = self._create_item(self.element.iter(), self.element, "languageCode")
        self._country = self._create_item(self.element.iter(), self.element, "countryCode")

    def set(self, value):
        if value in language_codes.keys():
            self._language.set_attrib({"value": language_codes[value][0]})
            self._country.set_attrib({"value": language_codes[value][1]})
        else:
            raise AttributeError

        return self.get()

    def get(self):
        lang = self._language.get_attrib()
        for key in language_codes:
            if language_codes[key][0] == lang["value"]:
                return key

    def get_list_values(self):
        return language_codes.keys()


class MetadataDataLanguage(MetadataLanguage):

    """
        Just a shortcut MetadataLanguage that predefines the paths
    """

    def __init__(self, parent):
        self.parent = parent
        self.name = "language"
        self.path = "dataIdInfo/dataLang"

        super(MetadataDataLanguage, self).__init__(self.parent, self.path)


class MetadataMDLanguage(MetadataLanguage):

    """
        Just a shortcut MetadataLanguage that predefines the paths
    """

    def __init__(self, parent):
        self.parent = parent
        self.name = "metadata_language"
        self.path = "dataIdInfo/mdLang"

        super(MetadataMDLanguage, self).__init__(self.parent, self.path)


# #### locals

class MetadataLocal(MetadataParentItem):
    """
        A MetadataLocal Item
    """

    def __init__(self, parent, language, country):

        self.parent = parent
        self.path = "Esri/locales/locale[@language='%s'][@country='%s']" % (language, country)

        super(MetadataLocal, self).__init__(self.parent)

        self.attributes = {}
        self.title = self._create_item(self.element.iter(), self.element, "resTitle")
        self.abstract = self._create_item(self.element.iter(), self.element, "idAbs")


class MetadataLocals(MetadataItems):
    """
        A MetadataLocals Item for Localized Titles and Abstracts
        Each Local Item has two children
         - Title
         - Abstract
        and a language and country attribute to define the local language
        Predefined language pairs are stored in the global language_code dictionary
        There can be many MetadataLocals instances
    """

    def __init__(self, parent=None):

        self.parent = parent

        self.name = "locals"
        self.path = "Esri/locales/locale"

        super(MetadataLocals, self).__init__(parent, self.path)
        self._locals = {}

        for element in self.elements:
            attrib = element.attrib

            found = False
            for lang in language_codes:
                if language_codes[lang][0] == attrib["language"]:
                    found = True
                    break

            if found:
                self._locals[lang] = (MetadataLocal(self.parent, attrib["language"], attrib["country"]))

    def __iter__(self):
        return iter(self._locals)

    def __getitem__(self, key):
        return self._locals[key]

    def _write(self):
        items_to_remove = []
        for element in self.elements:
            items_to_remove.append(element)

        for element in items_to_remove:
            self.elements.remove(element)

        for lang in self._locals:
            self.elements.append(self._locals[lang])

    def add(self, lang):

        if lang in language_codes.keys():
            language = language_codes[lang][0]
            country = language_codes[lang][1]
        else:
            raise KeyError

        self._locals[lang] = (MetadataLocal(self.parent, language, country))
        self._write()


# ########## Geographic and Temporal Extent

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


# ######### Updates

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


# ###### Credits, Citation, Source and Limitations

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


class MetadataScaleResolution(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """
    def __init__(self, parent=None):
        self.name = "scale_resolution"
        self.path = "dataIdInfo/dataScale/equScale/rfDenom"
        super(MetadataScaleResolution, self).__init__(parent)


class MetadataSupplementalInformation(MetadataItem):
    """
        Just a shortcut MetadataItem that predefines the paths
    """
    def __init__(self, parent=None):
        self.name = "supplemental_information"
        self.path = "dataIdInfo/suppInfo"
        super(MetadataSupplementalInformation, self).__init__(parent)

# ##############  Contact


class MetadataContact(MetadataParentItem):

    # TODO: Define Role, Country and Online Resource list
    """
        A MetadatContact Item
        Each Contact Item has several children
         - Role (list)
         - Contact Name
         - Position
         - Organization
         - Contact Info
         - Email (many)
         - Address
         - City
         - State
         - ZIP
         - Country (list)
         - Phone number (many)
         - Fax number (many)
         - Hours
         - Instructions
         - Link
         - Protocol
         - Profile
         - Online Resource Name
         - Online Resource Function
         - Online Resource Code (list)

        and a language and country attribute to define the local language
        Predefined language pairs are stored in the global language_code dictionary
        There can be many MetadataLocals instances
    """

    def __init__(self, parent):

        self.parent = parent

        super(MetadataContact, self).__init__(self.parent)

        self._role = self._create_item(self.element.iter(), self.element, "role")
        self.role = self._create_item(self.element.iter(), self._role, "RoleCd")
        self.contact_name = self._create_item(self.element.iter(), self.element, "rpIndName")
        self.position = self._create_item(self.element.iter(), self.element, "rpPosName")
        self.organization = self._create_item(self.element.iter(), self.element, "rpOrgName")
        self.contact_info = self._create_item(self.element.iter(), self.element, "rpCntInfo")
        self._address = self._create_item(self.element.iter(), self.contact_info, "cntAddress")
        self.email = self._create_items(self.element.iter(), self.contact_info, "eMailAdd")
        self.address = self._create_items(self.element.iter(), self._address, "delPoint")
        self.city = self._create_item(self.element.iter(), self._address, "City")
        self.state = self._create_item(self.element.iter(), self._address, "adminArea")
        self.zip = self._create_item(self.element.iter(), self._address, "postCode")
        self.country = self._create_item(self.element.iter(), self._address, "country")
        self._phone = self._create_item(self.element.iter(), self.contact_info, "cntPhone")
        self.phone_nb = self._create_items(self.element.iter(), self._phone, "voiceNum")
        self.fax_nb = self._create_items(self.element.iter(), self._phone, "faxNum")
        self.hours = self._create_item(self.element.iter(), self.contact_info, "cntHours")
        self.instructions = self._create_item(self.element.iter(), self.contact_info, "cntInstr")
        self._online_resource = self._create_item(self.element.iter(), self.contact_info, "cntOnlineRes")
        self.link = self._create_item(self.element.iter(), self._online_resource, "linkage")
        self.protocol = self._create_item(self.element.iter(), self._online_resource, "protocol")
        self.profile = self._create_item(self.element.iter(), self._online_resource, "appProfile")
        self.or_name = self._create_item(self.element.iter(), self._online_resource, "orName")
        self.or_desc = self._create_item(self.element.iter(), self._online_resource, "orDesc")
        self.or_function = self._create_item(self.element.iter(), self._online_resource, "orFunct")
        self.or_function_cd = self._create_item(self.element.iter(), self.or_function, "OnFunctCd")


class MetadataContacts(MetadataItems):
    """
        Extend the MetadataItems object
        use self._contacts instead of self._elements
    """

    def __init__(self, parent=None, path=None):

        self.parent = parent
        self.path = path
        super(MetadataContacts, self).__init__(parent, self.path)
        self._contacts = []

    def __iter__(self):
        return iter(self._contacts)

    def __getitem__(self, key):
        return self._contacts[key]

    def _write(self):
        items_to_remove = []
        for element in self.elements:
            items_to_remove.append(element)

        for element in items_to_remove:
            self.elements.remove(element)

        for contact in self._contacts:
            self.elements.append(contact)


class MetadataPointsOfContact(MetadataContacts):
    """
        Just a shortcut MetadataContacts that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "point_of_contact"
        self.path = "dataIdInfo/idPoC"
        super(MetadataPointsOfContact, self).__init__(parent, self.path)
        self._contacts = []
        for i in range(len(self.elements)):
            self._contacts.append(MetadataPointOfContact(parent, i))

    def add(self):
        self._contacts.append(MetadataPointOfContact(self.parent, len(self._contacts)))
        self._write()


class MetadataPointOfContact(MetadataContact):
    """
        Just a shortcut MetadataContacts that predefines the paths and position
    """

    def __init__(self, parent=None, index=0):
        self.path = "dataIdInfo/idPoC[%i]" % index

        super(MetadataPointOfContact, self).__init__(parent)


class MetadataMaintenanceContacts(MetadataContacts):
    """
        Just a shortcut MetadataContacts that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "maintenance_contact"
        self.path = "dataIdInfo/maintCont"
        super(MetadataMaintenanceContacts, self).__init__(parent, self.path)
        self._contacts = []
        for i in range(len(self.elements)):
            self._contacts.append(MetadataPointOfContact(parent, i))

    def add(self):
        self._contacts.append(MetadataMaintenanceContact(self.parent, len(self._contacts)))
        self._write()


class MetadataMaintenanceContact(MetadataContact):
    """
        Just a shortcut MetadataContact that predefines the paths and position
    """

    def __init__(self, parent=None, index=0):
        self.path = "dataIdInfo/maintCont[%i]" % index

        super(MetadataMaintenanceContact, self).__init__(parent)


class MetadataCitationContacts(MetadataContacts):
    """
        Just a shortcut MetadataContacts that predefines the paths
    """

    def __init__(self, parent=None):
        self.name = "citation_contact"
        self.path = "dataIdInfo/idCitation/citRespParty"
        super(MetadataCitationContacts, self).__init__(parent, self.path)
        self._contacts = []
        for i in range(len(self.elements)):
            self._contacts.append(MetadataPointOfContact(parent, i))

    def add(self):
        self._contacts.append(MetadataMaintenanceContact(self.parent, len(self._contacts)))
        self._write()


class MetadataCitationContact(MetadataContact):
    """
        Just a shortcut MetadataContact that predefines the paths and position
    """

    def __init__(self, parent=None, index=0):
        self.path = "dataIdInfo/idCitation/citRespParty[%i]" % index

        super(MetadataCitationContact, self).__init__(parent)
