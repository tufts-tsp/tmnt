import uuid
from typing import Self, Tuple, List, Optional, Set
from collections import UserList

class Element(object):
    """
    The basic primitive of a threat model, which can be an `Asset`,
    `Mitigation`, `Flow`, `Issue`, `Actor` or `Boundary`.

    Each element should be unique within the system, identified by it's name.
    Additionally, elements can have a description to help identify what the
    element is as well as the potential map to a parent element or children
    elements.

    Parameters
    ----------
    name : str
    desc : str, optional

    Attributes
    ----------
    name : str
        The name of the `Element`
    desc : str
        A short description about the `Element` that helps to identify it's
        purpose and role within the threat model.
    children : Set[Element]
        An unique set of elements that are children of the `Element`. These
        will be elements that exist within the parent `Element`, such as a
        server that has a datastore and a process.
    parent : Element
        The parent `Element` for this `Element`. The parent will be the `Element` that this `Element` exists within.

    Methods
    -------
    add_child : Add a new child to the `Element`'s children
    remove_child : Remove a child from the `Element`'s children

    See Also
    --------
    :func:`tmnpy.dsl.Actor`
    :func:`tmnpy.dsl.Asset`
    :func:`tmnpy.dsl.Boundary`
    :func:`tmnpy.dsl.Flow`
    :func:`tmnpy.dsl.Issue`
    :func:`tmnpy.dsl.Mitigation`
    """

    def __init__(
        self,
        name: str,
        desc: Optional[str] = None,
    ):
        self.name = name
        self.desc = desc
        self.__children = set()
        self.__parent = None

    def __repr__(self):
        return f"<{type(self).__name__}({self.name})>"

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Element) and self.name == value.name and type(self).__name__ == type(value).__name__:
            return True
        return False

    def __hash__(self):
        return hash((type(self).__name__, self.name))

    @property
    def name(self) -> str:
        """Name of the Element"""
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        if not isinstance(val, str):
            raise TypeError("Element Name must be a string")
        self.__name = val

    @property
    def desc(self) -> Optional[str]:
        """Description of the Element"""
        return self.__desc

    @desc.setter
    def desc(self, val: str | None) -> None:
        if not isinstance(val, str) and val != None:
            raise TypeError("Element Description must be a string")
        self.__desc = val

    @property
    def parent(self) -> Self | None:
        """
        Parent Element. The parent(s) must be a different element (or any child
        type) or it could be None. When you set the parent it will also set
        this element as a child of the parent. When you delete the parent,
        this element will be removed as a child.
        """
        return self.__parent

    @parent.setter
    def parent(self, parent: Self) -> None:
        if not isinstance(parent, Element):
            raise TypeError("A parent must be type tmnpy.dsl.element.Element")
        if parent == self:
            err = f"{parent} is self, an element cannot be a parent of itself."
            raise ValueError(err)
        if parent in self.children:
            err = f"{parent} cannot be both a child and parent of {self}."
            raise ValueError(err)
        # if parent.parent != None:
        #     raise ValueError("No grandparents allowed.")
        if self.__parent != None:
            self.__parent.remove_child(self)
        self.__parent = parent
        if self not in parent.children:
            parent.add_child(self)

    @parent.deleter
    def parent(self) -> None:
        parent = self.__parent
        self.__parent = None
        if isinstance(parent, Element) and self in parent.children:
            parent.remove_child(self)

    @property
    def children(self) -> Set[Self]:
        """
        Children Elements. Children can be of type Element (or any child type).
        When you assigned children, this will be treated as an unique set of
        Elements, i.e., a set.

        See Also
        --------
        add_child : Add a new child to the Element's children
        remove_child : Remove a child from the Element's children
        """
        return self.__children

    @children.setter
    def children(self, children: List[Self] | Set[Self]) -> None:
        if not isinstance(children, list) and not isinstance(children, set):
            raise TypeError("Children must be a list or set of Elements")
        for child in children:
            if not isinstance(child, Element):
                e = f"{child} must be type tmnpy.dsl.element.Element"
                raise TypeError(e)
            if child == self:
                raise ValueError(f"{self} cannot be a child of itself")
            if child == self.parent:
                raise ValueError(f"{child} is parent of {self}")
            if child.parent != self:
                child.parent = self
        self.__children = set(children)

    @children.deleter
    def children(self) -> None:
        for child in self.__children:
            del child.parent
        self.__children = set()

    def add_child(self, child: Self) -> None:
        """add_child allows you to add a single child to an Element."""
        children = self.children
        children.add(child)
        self.children = children

    def remove_child(self, child: Self) -> None:
        """remove_child allows you to remove a single child to an Element."""
        children = self.children
        children.remove(child)
        self.children = children
        if child.parent != None:
            del child.parent

class Elements(UserList):

    def __init__(self, initlist: Optional[Element | list[Element]] = None) -> None:
        self.data = []
        if initlist is not None:
            if isinstance(initlist, list):
                for d in initlist:
                    self.append(d)
            elif isinstance(initlist, Elements):
                self.data[:] = initlist.data[:]
            else:
                self.append(initlist)
        self.data = list(set(self.data))

    def append(self, item: Element) -> None:
        if not isinstance(item, Element):
            raise TypeError(f"{item} is not type tmnpy.dsl.element.Element.")
        for i in range(len(self.data)):
            if self.data[i] == item:
                raise ValueError(f"{item} is already in this list.")
        super().append(item)
        self.data = list(set(self.data))

    def index(self, name: str, *args) -> int:
        ctype = None
        if args:
            ctype = args[0]
        for i in range(len(self.data)):
            if name == self.data[i].name and ctype == None:
                return i
            elif name == self.data[i].name and ctype == type(self.data[i]):
                return i
        raise ValueError(f"{name} is not in list.")

    def subset(self, element_type: type[Element]):
        values = Elements()
        for i in range(len(self.data)):
            if element_type == type(self.data[i]):
                values.append(self.data[i])
        return values
