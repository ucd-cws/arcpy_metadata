__author__ = 'Thomas.Maschler'


from metadata_constructors import MetadataItem
from metadata_constructors import MetadataStringConstructor
from metadata_constructors import MetadataDateConstructor
from metadata_constructors import MetadataIntegerConstructor
from metadata_constructors import MetadataFloatConstructor
from metadata_constructors import MetadataListConstructor
from metadata_constructors import MetadataLanguageConstructor
from metadata_constructors import MetadataItems
from metadata_constructors import MetadataParentItem
from metadata_constructors import MetadataContactsConstructor
from metadata_constructors import MetadataContactConstructor

from languages import languages



# ########## General Info

class MetadataHelper(MetadataItem):
    def __init__(self, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataHelper, self).__init__(parent)

class MetadataString(MetadataStringConstructor):
    def __init__(self, value, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataString, self).__init__(value, path, name, parent)


class MetadataDate(MetadataDateConstructor):
    def __init__(self, value, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataDate, self).__init__(value, path, name, parent)


class MetadataInteger(MetadataIntegerConstructor):
    def __init__(self, value, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataInteger, self).__init__(value, path, name, parent)


class MetadataFloat(MetadataFloatConstructor):
    def __init__(self, value, path, name, parent):
        self.path = path
        self.name = name
        super(MetadataFloat, self).__init__(value, path, name, parent)

# ########## Keywords

class MetadataList(MetadataListConstructor):

    def __init__(self, tagname, path, name, parent=None):
        self.name = name
        super(MetadataList, self).__init__(parent, tagname=tagname, path=path)


class MetadataLanguage(MetadataLanguageConstructor):

    """
        Just a shortcut MetadataLanguage that predefines the paths
    """

    def __init__(self, path, name, parent):
        self.parent = parent
        self.name = name
        self.path = path

        super(MetadataLanguage, self).__init__(self.parent, self.path)




# #### locals

class MetadataLocal(MetadataParentItem):
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


class MetadataContacts(MetadataContactsConstructor):
    """
        Just a shortcut MetadataContacts that predefines the paths
    """

    def __init__(self, path, name, parent=None):
        self.name = name
        self.path = path
        super(MetadataContacts, self).__init__(parent, self.path)
        self._contacts = []
        for i in range(len(self.elements)):
            self.append(MetadataContact(self.path, parent, i))

    def new_contact(self):
        self.append(MetadataContact(self.path, self.parent, len(self._contacts)))

    def append(self, value):
        """
            Adds a single item to the section, like a list append
            :param value:
            :return: None
        """

        if value is None:
            value = MetadataContact(self.path, self.parent, len(self._contacts))
        elif not isinstance(value, MetadataContact):
            raise RuntimeError("Input value must be of type MetadataContact")

        self._contacts.append(value)
        self._write()
        super(MetadataContacts, self).append(value)


class MetadataContact(MetadataContactConstructor):
    """
        Just a shortcut MetadataContacts that predefines the paths and position
    """

    def __init__(self, path, parent=None, index=0):
        self.path = "%s[%i]" % (path, index)

        super(MetadataContact, self).__init__(parent)



