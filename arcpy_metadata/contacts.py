__author__ = 'Thomas.Maschler'

from __init__ import MetadataMulti


class MetadataContact(MetadataMulti):
    """
        A metadata item for groups of items (like tags). Define the root element (self.path) and then the name of the
        subitem to store there (self.tag_name) and you can use list-like methods to edit the group
    """

    tag_name = None
    current_items = []
    path = None

    def __init__(self, parent=None):  # , tagname=None, path=None):

        #if not self.tag_name:
        #    self.tag_name = tagname

        #if path:
        #    self.path = path

        self.name = "contact"
        self.role = None  # MetadataContactRole(parent=self)
        self.contact_name = None
        self.position = None
        self.organization = None
        self.address = None  # MetadataAddress
        self.phone = None  # MetadataPhone

        super(MetadataContact, self).__init__(parent, tagname="idPoC", path="dataIdInfo")

        self._refresh()

    def _refresh(self):
        self.current_items = self.parent.elements.find(self.path)

    def _add_item(self, item):
        """
            Adds an individual item to the section
            :param item: the text that will be added to the multi-item section, wrapped in the appropriate tag
                configured on parent object
            :return: None
        """

        element = xml.etree.ElementTree.Element(self.tag_name)
        element.text = item
        self.current_items.append(element)

    def get(self):
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

        return self.get()

    def extend(self, items):
        """
            An alias for "add" to make this more pythonic
            :param items: list of text items to add to this multi-item metadata section
            :return: None
        """

        self.add(items)
        return self.get()

    def append(self, item):
        """
            Adds a single item to the section, like a list append
            :param item:
            :return: None
        """
        self._add_item(item)
        return self.get()

    def remove(self, item):
        items_to_remove = []
        for i in self.current_items:
            if i.text == item:
                items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self.get()

    def removeall(self):
        items_to_remove = []
        for i in self.current_items:
            items_to_remove.append(i)

        for i in items_to_remove:
            self.current_items.remove(i)

        return self.get()
