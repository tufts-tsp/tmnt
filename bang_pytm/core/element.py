import uuid

from bang_pytm.util import SecurityProperty

class Element(object):
    """
    The basic primitive of a threat model, which can be an asset, control, flow,
    or threat.

    Each element should be unique within the system, and it will consist of a
    name and unique ID. Additionally, elements can have a description to help
    identify what the element is as well as the potential map to a parent
    element or children elements.

    Parameters
    ----------
    name : str
        The name of the element
    desc : str or None, default None
        A short description about the element that helps to identify it's
        purpose and role within the threat model.
    """

    __id: uuid.UUID = None
    __name: str = None
    __desc: str = None
    __parent: list = []
    __children: list = []
    __security_property: SecurityProperty = None

    def __init__(
        self,
        name: str,
        desc: str = None,
    ):
        self.name = name
        self.__desc = desc

    def __repr__(self):
        return f"<{type(self).__name__}({self.name}) - {self.eid}>"

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    @property
    def eid(self) -> uuid.UUID:
        """Unique ID for the Element"""
        if self.__id == None:
            self.__id = uuid.uuid4()
        return self.__id

    @property
    def name(self) -> str:
        """Name of the Element"""
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        self.__name = val

    @property
    def description(self) -> str:
        """Description of the Element"""
        return self.__desc

    @description.setter
    def description(self, val: str) -> None:
        self.__desc = val

    @property
    def parent(self) -> object:
        """
        Parent Elements for the Element

        The parent(s) must be a different element (of any type) or it could be
        None
        """
        return self.__parent

    def set_parent(self, parent: object) -> None:

        if parent is self:
            raise ValueError("An element cannot be a parent of itself")
        if parent in self.__children:
            raise ValueError("An element cannot be both a parent and a child")
        
        self.__add_elem(parent, self.__parent)

    def remove_parent(self, parent: object) -> None:
        self.__remove_elem(parent, self.__parent)

    @property
    def children(self) -> object:
        """
        Children for the Element

        Children can be any type of element, but they must be unique and an
        element cannot be its own child.
        """
        return self.__children

    def add_child(self, child: object) -> None:

        if child is self:
            raise ValueError("An element cannot be a child of itself")
        if child is self.__parent:
            raise ValueError("An element cannot be both a parent and a child")
    
        self.__add_elem(child, self.__children)

    def remove_child(self, child: object) -> None:

        if child in self.__children:
            self.__remove_elem(child, self.__children)

    def __add_elem(self, elem: object, elems: list) -> None:
        if self == elem:
            err = "You cannot assign an element to itself."
            raise AttributeError(err)
        elif elem in elems:
            err = f"{elem} has already been assigned to {self}."
            raise AttributeError(err)
        elems.append(elem)

    def __remove_elem(self, elem: object, elems: list) -> None:
        if elem not in elems:
            err = f"{elem} has not been assigned to {self}."
            raise AttributeError(err)
        elems.remove(elem)

    @property
    def security_property(self) -> SecurityProperty:
        return self.__security_property
    
    @security_property.setter
    def security_property(self, val: SecurityProperty) -> None:
        self.__security_property = val