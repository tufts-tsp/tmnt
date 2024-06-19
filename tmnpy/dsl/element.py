import uuid
from typing import Self, Tuple, List
from .requirement import SecurityProperty


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

    def __init__(
        self,
        name: str,
        desc: str = "N/A",
    ):
        self.__id = uuid.uuid4()
        if not isinstance(name, str):
            raise ValueError("Element Name must be a string")
        self.__name = name
        if desc == None:
            desc = "N/A"
        if not isinstance(desc, str):
            raise ValueError("Element Description must be a string")
        self.__desc = desc

        self.__children = []
        self.__parent = []
        self.__security_property = SecurityProperty()

    def __repr__(self):
        return f"<{type(self).__name__}({self.name}) - {self.eid}>"

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    @property
    def eid(self) -> uuid.UUID:
        """Unique ID for the Element"""
        return self.__id

    @property
    def name(self) -> str:
        """Name of the Element"""
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        self.__name = val

    @property
    def desc(self) -> str:
        """Description of the Element"""
        return self.__desc

    @desc.setter
    def desc(self, val: str) -> None:
        self.__desc = val

    @property
    def parent(self) -> Self:
        """
        Parent Elements for the Element

        The parent(s) must be a different element (of any type) or it could be
        None
        """
        return self.__parent

    def add_parent(self, parent: Self, assign_child: bool = True) -> None:
        # If this assignment is from `add_child` it will be a tuple, and
        # we shouldn't assign a child as this will cause issues - user could
        # also specify using a tuple
        if not isinstance(parent, Self):
            raise ValueError("Must be of type tmnpy.dsl.Element")
        if assign_child:
            parent.add_child(self, assign_parent=False)

        if parent is self:
            err = f"{parent} is self, an element cannot be a parent of itself."
            raise ValueError(err)
        if parent in self.__children:
            err = f"{parent} cannot be both a child and parent of {self}."
            raise ValueError(err)
        if self.__parent != []:
            err = f"{self} already has a parent, {self.__parent}. Please remove if you want to replace it."
            raise ValueError(err)
        if parent.parent != []:
            raise ValueError("No grandparents allowed.")
        self.__parent = parent

    def remove_parent(self, remove_child=True) -> None:
        if remove_child:
            self.parent.remove_child(self, remove_parent=False)
        self.__parent = None

    @property
    def children(self) -> List[Self]:
        """
        Children for the Element

        Children can be any type of element, but they must be unique and an
        element cannot be its own child.
        """
        return self.__children

    def add_child(self, child: Self, assign_parent: bool =True) -> None:
        if not isinstance(child, Self):
            raise ValueError("Must be of type tmnpy.dsl.Element")
        if assign_parent and child.parent != []:
            raise AttributeError(
                "A different parent has already been assigned"
            )
        elif assign_parent:
            child.add_parent(self, False)

        if child is self:
            err = f"{child} cannot be a child of itself"
            raise AttributeError("An element cannot be a child of itself")
        elif child is self.__parent:
            err = f"{child} is already assigned as the parent of {self}"
            raise AttributeError(err)
        elif child.children != []:
            err = (
                f"{child} has children, meaning {self} would be a grandparent"
            )
            raise AttributeError(err)
        elif child in self.__children:
            err = f"{child} has already been assigned to {self}."
            raise AttributeError(err)
        self.__children.append(child)

    def remove_child(self, child: Self, remove_parent: bool =True) -> None:
        if child not in self.__children:
            err = f"{child} has not been assigned to {self}."
            raise AttributeError(err)
        if remove_parent:
            child.remove_parent(remove_child=False)
        self.__children.remove(child)

    @property
    def security_property(self) -> SecurityProperty:
        return self.__security_property

    @security_property.setter
    def security_property(self, val: SecurityProperty) -> None:
        if not isinstance(val, SecurityProperty):
            raise ValueError(
                "Security Property must be a SecurityProperty object"
            )
        self.__security_property = val
