import os
import xml.etree.ElementTree as ET
from languages import languages
from datetime import date
from elements import contact_elements


class MetadataItem(object):
    '''
    A standard Metadata Item
    '''

    path = None
    value = ""

    def __init__(self, parent=None):
        self.parent = parent
        try:
            self.parent.elements
        except AttributeError:
            self.parent = parent.parent
        self.element = None
        self._require_tree_elements()

        # set current metadata value
        self.value = self.parent.elements.find(self.path).text
        self._attributes = None
        self.attributes = self.parent.elements.find(self.path).attrib

    #def __repr__(self):
    #    return self.value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        if isinstance(value, dict):
            self._attributes = value
        else:
            raise RuntimeWarning("Must be of type dict")

    def _require_tree_elements(self):
        """
            Checks that the required elements for this item are in place. If they aren't, makes them
        """
        e_tree = self.path.split('/')
        root = self.parent.elements.getroot()

        done = False
        while not done:
            d = {}
            i = 0
            d[i] = root
            for e in e_tree:
                # remove index for multi items, looks goofy. Is there a better way?
                if "[" in e:
                    p = e.index('[')
                    e_name = e[:p]
                    e_attrib = e[p:][1:-1].split('][')
                else:
                    e_name = e
                    e_attrib = []
                i += 1
                d[i] = d[i-1].find(e)
                if d[i] is None:
                    child = ET.Element(e_name)
                    for attrib in e_attrib:
                        if attrib[0] == "@":
                            kv = attrib.split('=')
                            key = kv[0][1:]
                            value = kv[1][1:-1]
                            child.set(key, value)
                    d[i-1].append(child)
                    break
                elif i == len(e_tree):
                    self.element = d[i]
                    done = True

    def _write(self):

        # set value
        if self.value and self.parent:
            item = self.parent.elements.find(self.path)
            item.text = self.value  # set the value, it will be written later

        if self.attributes and self.parent:
            item = self.parent.elements.find(self.path)
            for attribute in self.attributes:
                item.set(attribute, self.attributes[attribute])  # set the value, it will be written later

        if not self.parent:
            raise ValueError(
                "Can't write values without being contained in a Metadata Editor list or without manually initializing self.parent to an instance of MetadataEditor")


class IntegerConstructor(int):
    def __new__(cls, value, path, name, parent):
        if value is None:
            obj = int.__new__(cls, 0)
        else:
            obj = int.__new__(cls, value)
        obj.parent = parent
        return obj

#    def __init__(self, value, path, name, parent):
#        super(IntegerConstructor, self).__init__(value)


class FloatConstructor(float):
    def __new__(cls, value, path, name, parent):
        if value is None:
            obj = float.__new__(cls, 0.0)
        else:
            obj = float.__new__(cls, value)
        obj.parent = parent
        return obj

#    def __init__(self, value, path, name, parent):
#        super(FloatConstructor, self).__init__(value)


class DateConstructor(date):
    def __new__(cls, value, path, name, parent):
        if value is None:
            obj = date.__new__(cls, 1900, 1, 1)
        else:
            obj = date.__new__(cls, value[0], value[1], value[2])
        obj.parent = parent
        return obj

#    def __init__(self, value, path, name, parent):
#        super(DateConstructor, self).__init__(value[0], value[1], value[2])


class StringConstructor(str):
    def __new__(cls, value, path, name, parent):
        obj = str.__new__(cls, value)
        obj.parent = parent
        return obj

#    def __init__(self, value, path, name, parent):
#        super(StringConstructor, self).__init__()


class SubStringConstructor(str):
    def __new__(cls, element, parent, exists):
        obj = str.__new__(cls, "")
        obj.parent = parent
        return obj

#    def __init__(self, element, parent, exists):
#        super(SubStringConstructor, self).__init__()


class MetadataDateConstructor(MetadataItem, DateConstructor):

    def __init__(self, value=None, path=None, name=None, parent=None):
        super(MetadataDateConstructor, self).__init__(parent)


class MetadataIntegerConstructor(MetadataItem, IntegerConstructor):

    def __init__(self, value=None, path=None, name=None, parent=None):
        super(MetadataIntegerConstructor, self).__init__(parent)


class MetadataFloatConstructor(MetadataItem, FloatConstructor):

    def __init__(self, value=None, path=None, name=None, parent=None):
        super(MetadataFloatConstructor, self).__init__(parent)


class MetadataStringConstructor(MetadataItem, StringConstructor):

    def __init__(self, value=None, path=None, name=None, parent=None):
        super(MetadataStringConstructor, self).__init__(parent)


class ListConstructor(MetadataItem, list):

    def __init__(self, parent=None):
        super(ListConstructor, self).__init__(parent)


class DictConstructor(MetadataItem, dict):

    def __init__(self, parent=None):
        super(DictConstructor, self).__init__(parent)


class MetadataListConstructor(ListConstructor):
    """
        A metadata item for groups of items (like tags). Define the root element (self.path) and then the name of the
        subitem to store there (self.tag_name) and you can use list-like methods to edit the group
    """

    tag_name = None
    current_items = []
    path = None

    def __init__(self, parent=None, tagname=None, path=None):

        if not self.tag_name:
            self.tag_name = tagname

        if path:
            self.path = path

        super(MetadataListConstructor, self).__init__(parent)

        self._refresh()

    def __iter__(self):
        return iter(self.current_items)

    def __getitem__(self, key):
        return self.current_items[key]

    def _refresh(self):
        self.current_items = self.parent.elements.find(self.path)
        for item in self.current_items:
            super(MetadataListConstructor, self).append(item.text)

    def _add_item(self, item):
        """
            Adds an individual item to the section
            :param item: the text that will be added to the multi-item section, wrapped in the appropriate tag
                configured on parent object
            :return: None
        """

        element = ET.Element(self.tag_name)
        element.text = item
        self.current_items.append(element)

    def _get(self):
        values = []
        for item in self.current_items:
            values.append(item.text)
        return values

    def add(self, items):
        """
        :param items:
        :return: self.get()
        """
        for item in items:
            self._add_item(item)

        return self._get()

    def extend(self, items):
        """
            An alias for "add" to make this more pythonic
            :param items: list of text items to add to this multi-item metadata section
            :return: None
        """

        self.add(items)
        return self._get()

    def append(self, item):
        """
            Adds a single item to the section, like a list append
            :param item:
            :return: None
        """
        self._add_item(item)
        super(MetadataListConstructor, self).append(item)

    def remove(self, item):
        items_to_remove = []
        for i in self.current_items:
            if i.text == item:
                items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        super(MetadataListConstructor, self).remove(item)
        return self

    def removeall(self):
        items_to_remove = []

        for i in self.current_items:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        for i in items_to_remove:
            super(MetadataListConstructor, self).remove(i.text)

        return self


class MetadataItems(ListConstructor):
    """
        A helper objects for more complex items like Locals or Contacts.
        This object will allow to iterage though multiple items of the same type
    """

    def __init__(self, parent, path):
        self.path = os.path.dirname(path)
        self.tag_name = os.path.basename(path)
        super(MetadataItems, self).__init__(parent)
        self.path = path
        self.elements = self.parent.elements.findall(self.path)

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        return self.elements[key]


class MetadataParentItem(MetadataItem):
    """
    A helper object for more complex items like Contact and Locals
    This object will allow to add child elements to an item
    """

    def __init__(self, parent):

        self.parent = parent

        super(MetadataParentItem, self).__init__(self.parent)

    def _create_item(self, iter, parent, tag_name, item_type=None):
        for i in iter:
            if i.tag == tag_name:
                if item_type == "string":
                    return MetadataSubString(i, parent, True)
                else:
                    return MetadataSubItem(i, parent, True)
        i = ET.Element(tag_name)
        if item_type == "string":
            return MetadataSubString(i, parent)
        else:
            return MetadataSubItem(i, parent, True)

    def _create_items(self, iter, parent, tag_name):
        items = []
        for i in iter:
            if i.tag == tag_name:
                items.append(i)

        if not items:
            items = [ET.Element(tag_name)]
            return MetadataSubItems(items, parent)
        else:
            return MetadataSubItems(items, parent, True)

    def __setattr__(self, name, value):

        if name in contact_elements.keys():
            if contact_elements[name]['type'] == "string":
                if isinstance(value, MetadataSubString):
                    self.__dict__["_{}".format(name)] = value
                elif "_{}".format(name) in self.__dict__.keys():
                    if isinstance(value, str):
                        self.__dict__["_{}".format(name)].element.text = value
                    else:
                        raise RuntimeWarning("Input value must be of type String")
                else:
                    raise RuntimeWarning("No such item exists")
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):

        if name in contact_elements.keys():
            return self.__dict__["_{}".format(name)].element.text
        else:
            return self.__dict__[name]


class MetadataSubItem(object):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as single item inside a parent items
    """

    def __init__(self, element, parent, exists=False):

        self.parent = parent
        self.element = element

        if not exists:
            self.parent.append(element)

        self._attributes = None
        self.attributes = self.element.attrib # {}

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        if isinstance(value, dict):
            for attribute in value:
                self.element.set(attribute, value[attribute])
            self._attributes = self.element.attrib
        else:
            raise RuntimeWarning("Must be of type dict")

    def append(self, element):
        self.element.append(element)


class MetadataSubString(MetadataSubItem, SubStringConstructor):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as single item inside a parent items
    """

    def __init__(self, element, parent, exists=False):

        super(MetadataSubString, self).__init__(element, parent, exists)


class MetadataSubItems(object):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as multi item inside a parent item
    """

    def __init__(self, elements, parent, exists=False):
        self.elements = []
        self.parent = parent

        self.tag_name = elements[0].tag

        for element in elements:
            self.elements.append(MetadataSubItem(element, parent, exists))

    def append(self, item):
        element = ET.Element(self.tag_name)
        element.text = item
        self.elements.append(MetadataSubItem(element, self.parent, False))

    def add(self, items):
        for item in items:
            self.append(item)

    def get(self):
        elements = []
        for element in self.elements:
            elements.append(element.get())
        return elements

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        return self.elements[key]


class MetadataLanguageConstructor(MetadataParentItem):
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

        super(MetadataLanguageConstructor, self).__init__(self.parent)

        self._language = self._create_item(self.element.iter(), self.element, "languageCode")
        self._country = self._create_item(self.element.iter(), self.element, "countryCode")

    def set(self, value):
        if value in languages.keys():
            self._language.attributes = {"value": languages[value][0]}
            self._country.attributes = {"value": languages[value][1]}
        else:
            raise AttributeError

        return self.get()

    def get(self):
        lang = self._language.attributes
        for key in languages:
            if languages[key][0] == lang["value"]:
                return key

    def get_list_values(self):
        return languages.keys()


class MetadataContactConstructor(MetadataParentItem):

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

        super(MetadataContactConstructor, self).__init__(self.parent)

        i = 0


        while i < len(contact_elements):

            for subitem in contact_elements.keys():

                if contact_elements[subitem]["parent"] == "element" and "_{}".format(subitem) not in self.__dict__.keys():
                    setattr(self,
                            subitem,
                            self._create_item(self.element.iter(),
                                              self.element,
                                              contact_elements[subitem]["path"],
                                              contact_elements[subitem]["type"]))
                    i = 0


                elif "_{}".format(contact_elements[subitem]["parent"]) in self.__dict__.keys() and \
                        "_{}".format(subitem) not in self.__dict__.keys():
                    setattr(self,
                            subitem,
                            self._create_item(self.element.iter(),
                                              self.__dict__["_{}".format(contact_elements[subitem]["parent"])],
                                              contact_elements[subitem]["path"],
                                              contact_elements[subitem]["type"]))
                    i = 0
                else:
                    i += 1


class MetadataContactsConstructor(MetadataItems):
    """
        Extend the MetadataItems object
        use self._contacts instead of self._elements
    """

    def __init__(self, parent=None, path=None):

        self.parent = parent
        self.path = path
        super(MetadataContactsConstructor, self).__init__(parent, self.path)
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

    def remove(self, value):
        self._contacts.remove(value)
        self._write()
        super(MetadataContactsConstructor, self).remove(value)