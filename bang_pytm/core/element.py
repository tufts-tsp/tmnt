import uuid

class Element(object):
    """
    An element of a threat model, which can be an asset, control, flow, or 
    threat.

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

    To Do
    -----
    1. Add forced type checking
    """

    __id : uuid.UUID = None
    __name : str = None
    __desc : str = None
    __parent : object = None
    __children : list = []

    def __init__(self, 
                 name: str, 
                 desc: str = None,
                 ):
        self.name = name
        self.__desc = desc

    def __repr__(self):
        return "<{0}.{1}({2}) at {3}>".format(
            self.__module__, type(self).__name__, self.name, hex(id(self))
        )

    def __str__(self):
        return "{0}({1})".format(type(self).__name__, self.name)

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
        Parent Element for the Element

        The parent must be a different element (of any type) or it could be None
        """
        return self.__parent
    
    @parent.setter
    def parent(self, val: object) -> None:
        if self == val:
            err = "You cannot assign an element to be it's own parent."
            raise AttributeError(err)
        self.__parent = val

    @property
    def children(self) -> object:
        """
        Children for the Element
        
        Children can be any type of element, but they must be unique and an 
        element cannot be its own child.
        """
        return self.__parent
    
    def add_child(self, child: object) -> None:
        if self == child:
            err = "You cannot assign an element to be it's own child."
            raise AttributeError(err)
        elif child in self.__children:
            err = f"{child} has already been assigned as a child for {self}."
            raise AttributeError(err)
        self.__children.append(child)

    def remove_child(self, child: object) -> None:
        if child not in self.__children:
            err = f"{child} has not been assigned as a child for {self}."
            raise AttributeError(err)
        self.__children.remove(child)

    





