import os
import copy
import xml.etree.ElementTree as ET


class MetadataValueListHelper(object):
    """
    A helper class to have value list items behave like a python lists
    """
    def __init__(self, list_items):
        if isinstance(list_items, MetadataValueListConstructor):
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

    def sort(self):
        """
        Sort list items
        :return: list
        """
        return self.list_items.sort()

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
    sync = None

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

        if self.sync is not None:
            if self.sync:
                self.attributes["Sync"] = "TRUE"
            else:
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

        elements = root.findall(self.path)

        # if there is already exactly one element, take this one
        if len(elements) == 1:
            self.element = elements[0]
            return

        # if there is more than one, take the first one with a value, attribut or children.
        # if all are empty, just take the last one
        elif len(elements) > 1:
            for element in elements:
                if element.text.strip() != '' or element.attrib is not None or len(element.getchildren()) > 0:
                    break
            self.element = element
            return

        # otherwise build the tree
        else:

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


class MetadataValueListConstructor(MetadataItemConstructor):
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

        super(MetadataValueListConstructor, self).__init__(parent)

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

    def sort(self):
        """
        sort items
        :return:
        """
        return self.current_items.sort()


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
                child = MetadataParentItem(new_path, self.parent, child_elements, len(self.current_items))
                self.current_items.append(child)

    def new(self):
        new_path = "{}/{}".format(self.path, self.tag_name)
        child = MetadataParentItem(new_path, self.parent, self.child_elements, len(self.current_items)+1)
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


class MetadataParentItemConstructor(MetadataItemConstructor):
    """
    A helper object for more complex items like Contact, Online Resources and Locals
    This object will allow to add child elements to an item based on supplied element list
    """

    def __init__(self, parent, child_elements):
        self.parent = parent
        self.child_elements = child_elements
        super(MetadataParentItemConstructor, self).__init__(self.parent)

        i = 0
        while i < len(self.child_elements):
            for element in self.child_elements.keys():

                path = self.child_elements[element]["path"]

                if "_{}".format(element) not in self.__dict__.keys():
                    setattr(self, "_{}".format(element), self._create_item(path))
                    i = 0
                else:
                    i += 1

    def __setattr__(self, n, v):
        if n in ["path", "parent", "child_elements", "value", "attr_lang", "attr_country"]:
            self.__dict__[n] = v
        else:
            if n in self.child_elements.keys():
                element_type = self.child_elements[n]["type"]

                if element_type == "attribute":
                    key = self.child_elements[n]["key"]
                    if v is None or v == "":
                        self.__dict__["_{}".format(n)].element.attrib[key] = ""
                    else:
                        allowed_values = []
                        found = False
                        for value in self.child_elements[n]["values"]:
                            allowed_values.append(value[0])
                            if v == value[0]:
                                self.__dict__["_{}".format(n)].element.attrib[key] = value[1]
                                found = True
                        if not found:
                            raise TypeError("Value must be in {}".format(allowed_values))

                elif isinstance(v, (str, unicode)):
                    self.__dict__["_{}".format(n)].element.text = v
                elif v is None:
                    self.__dict__["_{}".format(n)].element.text = ""
                else:
                    raise RuntimeWarning("Input value must be of type String or None")
            else:
                self.__dict__[n] = v

    def __getattr__(self, name):

        if name != "child_elements" and name in self.child_elements.keys():

            element_type = self.child_elements[name]["type"]
            if element_type == "attribute":
                key = self.child_elements[name]["key"]
                values = self.child_elements[name]["values"]
                if key in self.__dict__["_{}".format(name)].element.attrib.keys():
                    v = self.__dict__["_{}".format(name)].element.attrib[key]
                    for value in values:
                        if v in value:
                            return value[0]
                else:
                    return None

            else:
                #return self.__dict__["_{}".format(name)].value
                return self.__dict__["_{}".format(name)].element.text # should be the same"

        else:
            return self.__dict__[name]

    def _create_item(self, tag_name):

        tags = tag_name.split("/")
        i = 0

        parent = self.element

        # search for tag
        while i < len(tags):
            tag = tags[i]
            p = None
            iterator = parent.iter()

            for item in iterator:
                # item exists already but is not the final one
                if item.tag == tag and i < len(tags)-1:
                    p = item
                    break
                # item exists already and is final one
                elif item.tag == tag and i == len(tags)-1:
                    return MetadataSubItemConstructor(item)
            # item does not yet exist
            if p is None:
                p = ET.Element(tag)
                parent.append(p)
                # if it is the final one
                if i == len(tags)-1:
                    return MetadataSubItemConstructor(p)

            parent = p
            i += 1


class MetadataSubItemConstructor(object):
    """
    A helper object for more complex items like Contact and Locals
    This object can be placed as single item inside a parent items
    """

    def __init__(self, element):

        self.element = element

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


####################################################


class MetadataItem(MetadataItemConstructor):
    """
    A simple metadata item
    Define path and position
    """
    def __init__(self, path, name, parent, sync=True):
        self.path = path
        self.name = name
        self.sync = sync
        super(MetadataItem, self).__init__(parent)


class MetadataValueList(MetadataValueListConstructor):
    """
    A list metadata item
    Define path, parent item position and item tag name
    """

    def __init__(self, tagname, path, name, parent=None, sync=True):
        self.name = name
        self.sync = sync
        super(MetadataValueList, self).__init__(parent, tagname=tagname, path=path)


class MetadataObjectList(MetadataObjectListConstructor):
    """
    A list metadata item
    Define path, parent item position and item tag name
    """

    child_elements = {}

    def __init__(self, tagname, path, parent, elements, sync=True):
        self.sync = sync
        super(MetadataObjectList, self).__init__(parent, tagname=tagname, path=path, child_elements=elements)


class MetadataParentItem(MetadataParentItemConstructor):
    """
        Just a shortcut MetadataContacts that predefines the paths and position
    """
    # TODO: Define Role, Country and Online Resource list
    def __init__(self, path, parent, elements, index=0):
        self.path = "{0!s}[{1:d}]".format(path, index)
        super(MetadataParentItem, self).__init__(parent, elements)
