__author__ = 'Thomas.Maschler'

from arcpy_metadata.metadata_constructors import MetadataItemConstructor
from arcpy_metadata.metadata_constructors import MetadataListConstructor
from arcpy_metadata.metadata_constructors import MetadataItemsConstructor
from arcpy_metadata.metadata_constructors import MetadataParentItemConstructor

from arcpy_metadata.elements import contact_elements
from arcpy_metadata.languages import languages



# ########## General Info


class MetadataItem(MetadataItemConstructor):
    """
    A simple metadata item
    Define path and position
    """
    def __init__(self, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataItem, self).__init__(parent)

# ########## Keywords

class MetadataList(MetadataListConstructor):
    """
    A list metadata item
    Define path, parent item position and item tag name
    """

    def __init__(self, tagname, path, name, parent=None):
        self.name = name
        super(MetadataList, self).__init__(parent, tagname=tagname, path=path)


class MetadataLanguage(MetadataParentItemConstructor):

    """
        A MetadataParentItem for Language settings
        Each Language Item has two children
         - Language
         - Country
        Predefined language pairs are stored in the global language_code dictionary
    """

    def __init__(self, path, name, parent):
        self.parent = parent
        self.name = name
        self.path = path

        language_elements = {
            "attr_lang": {
                "parent": "element",
                "path": "languageCode"},

            "attr_country": {
                "parent": "element",
                "path": "countryCode"}
            }

        super(MetadataLanguage, self).__init__(self.parent, language_elements)

    def get_lang(self):
        lang = self._attr_lang.attributes
        if "value" in lang.keys():
            for key in languages:
                if languages[key][0] == lang["value"]:
                    return key
            return ""
        else:
            return ""

    def __setattr__(self, n, v):
        if n in ["path", "parent", "child_elements", "name", "value"]:
            self.__dict__[n] = v
        elif n == "attr_lang":
            if v == "" or v is None:
                self._attr_lang.attributes = {}
            else:
                self._attr_lang.attributes = v
        elif n == "attr_country":
            if v == "" or v is None:
                self._attr_country.attributes = {}
            else:
                self._attr_country.attributes = v
        else:
            if n in self.child_elements.keys():
                if isinstance(v, (str, unicode)):
                    self.__dict__["_{}".format(n)].element.text = v
                elif v is None:
                    self.__dict__["_{}".format(n)].element.text = ""
                else:
                    raise RuntimeWarning("Input value must be of type String or None")
            else:
                self.__dict__[n] = v

    def __getattr__(self, name):

        if name != "child_elements" and name in self.child_elements.keys():
                return self.__dict__["_{}".format(name)].element.text
        #elif name == "value":
        #    return self.element
        elif name == "attr_lang":
            return self._attr_lang.attributes
        elif name == "attr_country":
            return self._attr_country.attributes
        else:
            return self.__dict__[name]

# #### locals

class MetadataLocal(MetadataParentItemConstructor):
    """
        A MetadataLocal Item
    """

    def __init__(self, parent, path, language, country):

        self.parent = parent
        self.path = "{0!s}[@language='{1!s}'][@country='{2!s}']".format(path, language, country)

        super(MetadataLocal, self).__init__(self.parent)

        self.attributes = {}
        self.title = self._create_item(self.element.iter(), self.element, "resTitle")
        self.abstract = self._create_item(self.element.iter(), self.element, "idAbs")


class MetadataLocals(MetadataItemsConstructor):
    """
        A MetadataLocals Item for Localized Titles and Abstracts
        Each Local Item has two children
         - Title
         - Abstract
        and a language and country attribute to define the local language
        Predefined language pairs are stored in the global language_code dictionary
        There can be many MetadataLocals instances
    """

    def __init__(self, path, name, parent=None):

        self.parent = parent

        self.name = name
        self.path = path

        super(MetadataLocals, self).__init__(parent, self.path)
        self._locals = {}

        for element in self.elements:
            attrib = element.attrib

            found = False
            for lang in languages:
                if languages[lang][0] == attrib["language"]:
                    found = True
                    break

            if found:
                self._locals[lang] = (MetadataLocal(self.parent, self.path, attrib["language"], attrib["country"]))

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

    def new_local(self, lang):

        if lang in languages.keys():
            language = languages[lang][0]
            country = languages[lang][1]
        else:
            raise KeyError

        self._locals[lang] = (MetadataLocal(self.parent, self.path, language, country))
        self._write()


class MetadataContact(MetadataParentItemConstructor):
    """
        Just a shortcut MetadataContacts that predefines the paths and position
    """
    # TODO: Define Role, Country and Online Resource list
    def __init__(self, path, name, parent=None, index=0):
        self.name = name
        self.path = "{0!s}[{1:d}]".format(path, index)
        super(MetadataContact, self).__init__(parent, contact_elements)



