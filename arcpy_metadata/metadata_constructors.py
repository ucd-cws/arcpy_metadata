import os
import copy
import xml.etree.ElementTree as ET


class MetadataValueListHelper(object):
    """
    A helper class to have value list items behave like a python lists
    """
    def __init__(self, list_items):
        if isinstance(list_items, MetadataListConstructor):
            self.list_items = list_items
        else:
            raise TypeError("Must be an instance of MetadataListConstructor")

    def __getitem__(self, index):
        return self.list_items.current_items[index].text

    def __setitem__(self, index, value):
        self.list_items.current_items[index].text = value

    def __repr__(self):
        return repr(self.list_items.value)

    def __len__(self):
        return len(self.list_items.current_items)

    def append(self, value):
        """
        Append given item to list
        :param value:
        :return:
        """
        self.list_items.append(value)

    def remove(self, value):
        """
        Remove given item from list
        :param value:
        :return:
        """
        self.list_items.remove(value)

    def pop(self):
        """
        Remove last list item
        :return: object
        """
        return self.list_items.pop()


class MetadataObjectListHelper(object):
    """
    A helper class to have value list items behave like a python lists
    """
    def __init__(self, list_objects):
        if isinstance(list_objects, MetadataObjectListConstructor):
            self.list_objects = list_objects
        else:
            raise TypeError("Must be an instance of MetadataObjectListConstructor")

    def __getitem__(self, index):
        return self.list_objects.current_items[index]

    def __setitem__(self, index, value):
        self.list_objects.current_items[index] = value

    def __repr__(self):
        return repr(self.list_objects.current_items)

    def __len__(self):
        return len(self.list_objects.current_items)

    def new(self):
        """
        Add a new object to the list
        :return:
        """
        self.list_objects.new()

    def remove(self, value):
        """
        Remove given item from list
        :param value:
        :return:
        """
        self.list_objects.remove(value)

    def pop(self):
        """
        Remove last list item
        :return: object
        """
        return self.list_objects.pop()


class MetadataItemConstructor(object):
    '''
    A standard Metadata Item
    '''

    path = None
    value = ""
    sync = True

    def __init__(self, parent=None):
        self.parent = parent
        try:
            self.parent.elements
        except AttributeError:
            self.parent = parent.parent
        self.element = None
        self._require_tree_elements()

        # set current metadata value and attributes
        if self.parent.elements.find(self.path).text is not None:
            self.value = self.parent.elements.find(self.path).text.strip()
        else:
            self.value = self.parent.elements.find(self.path).text
        self.attributes = self.parent.elements.find(self.path).attrib
        self.attributes["Sync"] = "FALSE"

    @property
    def attributes(self):
        return self.parent.elements.find(self.path).attrib

    @attributes.setter
    def attributes(self, v):
        if isinstance(v, dict):
            if self.parent:
                item = self.parent.elements.find(self.path)
                for attribute in v:
                    item.set(attribute, v[attribute])  # set the value, it will be written later
            if not self.parent:
                raise ValueError(
                    "Can't write values without being contained in a Metadata Editor list or without manually initializing self.parent to an instance of MetadataEditor")
        else:
            raise RuntimeWarning("Must be of type dict")

    @property
    def value(self):
        return self.parent.elements.find(self.path).text

    @value.setter
    def value(self, v):
        if self.parent:
            item = self.parent.elements.find(self.path)
            item.text = v  # set the value, it will be written later
        if not self.parent:
            raise ValueError(
                "Can't write values without being contained in a Metadata Editor list or without manually initializing"
                " self.parent to an instance of MetadataEditor")


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


class MetadataListConstructor(MetadataItemConstructor):
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

        self.current_items = []
        values = []
        for item in self.parent.elements.find(self.path):
            values.append(item.text)
        self.value = values

    @property
    def value(self):
        v = []
        for item in self.current_items:
            v.append(item.text)
        return v

    @value.setter
    def value(self, v):
        self._removeall()
        if v is None or v == "":
            pass
        elif isinstance(v, (list, MetadataValueListHelper)):
            for value in v:
                self.append(value)
        else:
            raise RuntimeWarning("Input value must be a List or None")

    def append(self, item):
        """
            Adds an individual item to the section
            :param item: the text that will be added to the multi-item section, wrapped in the appropriate tag
                configured on parent object
            :return:
        """

        element = ET.Element(self.tag_name)
        element.text = item
        self.current_items.append(element)
        self.element._children = self.current_items

    def pop(self):
        """
        Remove the last element in element tree
        :return: object
        """

        item_to_remove = None

        for i in self.current_items:
            item_to_remove = i

        j = copy.deepcopy(item_to_remove)

        if item_to_remove is not None:
            self.current_items.remove(item_to_remove)

        return j

    def remove(self, item):
        """
        Remove the given item from element tree
        :param item:
        :return:
        """
        items_to_remove = []

        for i in self.current_items:
            if i.text == item:
                items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

    def _removeall(self):
        """
        removes all items from element tree
        :return:
        """
        items_to_remove = []

        for i in self.current_items:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)


class MetadataObjectListConstructor(MetadataItemConstructor):
    """
        A metadata item for groups of items (like tags). Define the root element (self.path) and then the name of the
        subitem to store there (self.tag_name) and you can use list-like methods to edit the group
    """

    tag_name = None
    current_items = []
    path = None

    def __init__(self, parent=None, tagname=None, path=None, child_elements=None):

        self.child_elements = child_elements

        if not self.tag_name:
            self.tag_name = tagname

        if path:
            self.path = path

        super(MetadataObjectListConstructor, self).__init__(parent)

        self.current_items = []
        for item in self.parent.elements.find(self.path):
            if item.tag == self.tag_name:
                new_path = "{}/{}".format(self.path, tagname)
                child = MetadataLO(new_path, self.parent, child_elements, len(self.current_items))
                self.current_items.append(child)

    def new(self):
        new_path = "{}/{}".format(self.path, self.tag_name)
        child = MetadataLO(new_path, self.parent, self.child_elements, len(self.current_items)+1)
        self.current_items.append(child)

    def pop(self):
        """
        Remove the last element in element tree
        :return: object
        """

        item_to_remove = None

        for i in self.current_items:
            item_to_remove = i

        #j = copy.deepcopy(item_to_remove)

        if item_to_remove is not None:
            for item in self.parent.elements.find(self.path):
                if item == item_to_remove.element:
                    self.parent.elements.find(self.path).remove(item)
            self.current_items.remove(item_to_remove)

        return item_to_remove

    def remove(self, item):
        """
        Remove the given item from element tree
        :param item:
        :return:
        """

        for i in self.parent.elements.find(self.path):
            if i == item.element:
                self.parent.elements.find(self.path).remove(i)
        self.current_items.remove(item)

    def _removeall(self):
        """
        removes all items from element tree
        :return:
        """
        items_to_remove = []

        for item in self.current_items:
            items_to_remove.append(item)

        for item in items_to_remove:
            for i in self.parent.elements.find(self.path):
                if i == item.element:
                    self.parent.elements.find(self.path).remove(i)
            self.current_items.remove(item)


class MetadataItemsConstructor(MetadataItemConstructor):
    """
        A helper objects for more complex items like Locals or Contacts.
        This object will allow to iterage though multiple items of the same type
    """

    def __init__(self, parent, path):
        self.path = os.path.dirname(path)
        self.tag_name = os.path.basename(path)
        super(MetadataItemsConstructor, self).__init__(parent)
        self.path = path
        self.elements = self.parent.elements.findall(self.path)
        self.value = self.elements

    @property
    def value(self):
        return self.elements

    @value.setter
    def value(self, v):
        if not hasattr(self, 'elements'):
            self.elements = self.parent.elements.findall(self.path)

        self._removeall()
        if v is None:
            pass
        elif isinstance(v, list):
            for value in v:
                self._append(value)
        else:
            raise RuntimeWarning("Input value must be a List or None")

    def _append(self, element):
        """
            Adds an individual item to the section
            :param item: the text that will be added to the multi-item section, wrapped in the appropriate tag
                configured on parent object
            :return: None
        """
        self.elements.append(element)

    def _removeall(self):
        items_to_remove = []

        for i in self.elements:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.elements.remove(i)


class MetadataParentItemConstructor(MetadataItemConstructor):
    """
    A helper object for more complex items like Contact and Locals
    This object will allow to add child elements to an item
    """

    def __init__(self, parent, child_elements):
        self.parent = parent
        self.child_elements = child_elements
        super(MetadataParentItemConstructor, self).__init__(self.parent)

        i = 0
        while i < len(self.child_elements):
            for element in self.child_elements.keys():
                if self.child_elements[element]["parent"] == "element" and \
                                "_{}".format(element) not in self.__dict__.keys():
                    setattr(self, "_{}".format(element),
                            self._create_item(self.element.iter(), self.element, self.child_elements[element]["path"]))
                    setattr(self, element, self.__dict__["_{}".format(element)].value)
                    i = 0

                elif "_{}".format(self.child_elements[element]["parent"]) in self.__dict__.keys() and \
                                "_{}".format(element) not in self.__dict__.keys():
                    setattr(self, "_{}".format(element),
                            self._create_item(self.element.iter(),
                                              self.__dict__["_{}".format(self.child_elements[element]["parent"])],
                                              self.child_elements[element]["path"]))
                    setattr(self, element, self.__dict__["_{}".format(element)].value)
                    i = 0

                else:
                    i += 1
        #self.value = self.element

    def __setattr__(self, n, v):
        if n in ["path", "parent", "child_elements", "name", "value", "attr_lang", "attr_country"]:
            self.__dict__[n] = v
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
        else:
            return self.__dict__[name]

    @staticmethod
    def _create_item(iterator, parent, tag_name):
        for i in iterator:
            if i.tag == tag_name:
                return MetadataSubItemConstructor(i, parent, True)
        i = ET.Element(tag_name)
        return MetadataSubItemConstructor(i, parent)


class MetadataSubItemConstructor(object):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as single item inside a parent items
    """

    def __init__(self, element, parent, exists=False):

        self.parent = parent
        self.element = element

        if not exists:
            self.parent.append(element)

        if self.element.text is not None:
            self.value = self.element.text.strip()
        else:
            self.value = self.element.text
        self.attributes = self.element.attrib # {}

    @property
    def attributes(self):
        return self.element.attrib

    @attributes.setter
    def attributes(self, v):
        if isinstance(v, dict):
            for attribute in v:
                self.element.set(attribute, v[attribute])
        else:
            raise RuntimeWarning("Must be of type dict")

    @property
    def value(self):
        return self.element.text

    @value.setter
    def value(self, v):
        if isinstance(v, (str, unicode)):
            self.element.text = v
        elif v is None:
            self.element.text = ""
        else:
            raise RuntimeWarning("Must be of type String or None")

    def append(self, element):
        self.element.append(element)


class MetadataLO(MetadataParentItemConstructor):
    """
        Just a shortcut MetadataContacts that predefines the paths and position
    """
    # TODO: Define Role, Country and Online Resource list
    def __init__(self, path, parent, child_elements, index=0):
        self.path = "{0!s}[{1:d}]".format(path, index)
        super(MetadataLO, self).__init__(parent, child_elements)
