import os
import xml.etree.ElementTree as ET
from languages import languages
from datetime import date




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
        obj = int.__new__(cls, value)
        obj.parent = parent
        return obj


class FloatConstructor(float):
    def __new__(cls, value, path, name, parent):
        obj = float.__new__(cls, value)
        obj.parent = parent
        return obj


class DateConstructor(date):
    def __new__(cls, value, path, name, parent):
        obj = date.__new__(cls, value)
        obj.parent = parent
        return obj


class StringConstructor(str):
    def __new__(cls, value, path, name, parent):
        obj = str.__new__(cls, value)
        obj.parent = parent
        return obj


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



class List(MetadataItem, list):

    def __init__(self, parent=None):
        super(List, self).__init__(parent)


class MetadataListConstructor(List):
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

        return self._get()

    def removeall(self):
        items_to_remove = []
        for i in self.current_items:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self._get()


class MetadataItems(MetadataItem):
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

    # def get(self):
    #     values = []
    #     for element in self.elements:
    #         values.append(element.text)
    #     return values
    #
    # def _add_item(self,item):
    #     element = ET.Element(self.tag_name)
    #     element.text = item
    #     self.elements.append(element)
    #
    # def add(self, items):
    #     for item in items:
    #         self._add_item(item)
    #     return self.get()
    #
    # def extent(self, items):
    #     self.add(items)
    #
    # def append(self, item):
    #     self._add_item(item)
    #     return self.get()
    #
    # def remove(self, item):
    #     items_to_remove = []
    #     for i in self.elements:
    #         if i.text == item:
    #             items_to_remove.append(i)
    #     for i in items_to_remove:
    #         self.elements.remove(i)
    #     return self.get()
    #
    # def remove_all(self):
    #     items_to_remove = []
    #     for i in self.elements:
    #         items_to_remove.append(i)
    #     for i in items_to_remove:
    #         self.elements.remove(i)
    #
    #     return self.get()


class MetadataParentItem(MetadataItem):
    """
    A helper object for more complex items like Contact and Locals
    This object will allow to add child elements to an item
    """

    def __init__(self, parent):

        self.parent = parent
        super(MetadataParentItem, self).__init__(self.parent)

    def _create_item(self, iter, parent, tag_name):
        for i in iter:
            if i.tag == tag_name:
                return MetadataSubItem(i, parent, True)
        i = ET.Element(tag_name)
        return MetadataSubItem(i, parent)

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

        self.attributes = self.element.attrib # {}

    def append(self, element):
        self.element.append(element)

    def get(self):
        return self.element.text

    def get_attrib(self):
        return self.attributes

    def set(self, value):
        self.element.text = value
        return self.get()

    def set_attrib(self, attributes):
        self.attributes.update(attributes)
        for attribute in self.attributes:
                self.element.set(attribute, self.attributes[attribute])
        return self.get_attrib()


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
            self._language.set_attrib({"value": languages[value][0]})
            self._country.set_attrib({"value": languages[value][1]})
        else:
            raise AttributeError

        return self.get()

    def get(self):
        lang = self._language.get_attrib()
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