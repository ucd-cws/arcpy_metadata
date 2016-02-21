__author__ = 'Thomas.Maschler'

from metadata_constructors import MetadataItemConstructor
from metadata_constructors import MetadataListConstructor
from metadata_constructors import MetadataItemsConstructor
from metadata_constructors import MetadataParentItemConstructor

from elements import contact_elements
from languages import languages



# ########## General Info

class MetadataItem(MetadataItemConstructor):
    def __init__(self, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataItem, self).__init__(parent)

# ########## Keywords

class MetadataList(MetadataListConstructor):

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
            "language": {
                "parent": "element",
                "path": "languageCode"},

            "country": {
                "parent": "element",
                "path": "countryCode"}
            }

        super(MetadataLanguage, self).__init__(self.parent, language_elements)

    def get_lang(self):
        lang = self._language.attributes
        if "value" in lang.keys():
            for key in languages:
                if languages[key][0] == lang["value"]:
                    return key
            return ""
        else:
            return ""


# #### locals

class MetadataLocal(MetadataParentItemConstructor):
    """
        A MetadataLocal Item
    """

    def __init__(self, parent, path, language, country):

        self.parent = parent
        self.path = "%s[@language='%s'][@country='%s']" % (path, language, country)

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
        self.path = "%s[%i]" % (path, index)
        super(MetadataContact, self).__init__(parent, contact_elements)



