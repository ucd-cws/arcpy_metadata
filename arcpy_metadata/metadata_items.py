__author__ = 'Thomas.Maschler'

from arcpy_metadata.metadata_constructors import MetadataParentItemConstructor
from arcpy_metadata.languages import languages


# ########## General Info


# #### locals

class MetadataLanguage(MetadataParentItemConstructor):

    """
        A MetadataParentItem for Language settings
        Each Language Item has two children
         - Language
         - Country
        Predefined language pairs are stored in the global language_code dictionary
    """

    def __init__(self, path, name, parent, sync=True):
        self.parent = parent
        self.name = name
        self.path = path
        self.sync = sync

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
        if n in ["path", "parent", "child_elements", "name", "value", "sync"]:
            self.__dict__[n] = v
        elif n == "attr_lang":
            if v == "" or v is None:
                self._attr_lang.attributes = {}
            else:
                self._attr_lang.attributes = v
                if self.sync:
                    self._attr_lang.attributes["Sync"] = "TRUE"
                else:
                    self._attr_lang.attributes["Sync"] = "FALSE"
        elif n == "attr_country":
            if v == "" or v is None:
                self._attr_country.attributes = {}
            else:
                self._attr_country.attributes = v
                if self.sync:
                    self._attr_country.attributes["Sync"] = "TRUE"
                else:
                    self._attr_country.attributes["Sync"] = "FALSE"
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











