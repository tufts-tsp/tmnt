from .element import Element
from .actor import Actor

from collections import UserList


class Boundary(Element):

    """
    needs documentation
    """

    def __init__(
        self, 
        name, 
        elements: list[Element] = [], 
        physical_access: list[Actor] = [],  
        **kwargs
    ):
        self.elements = elements
        self.physical_access = physical_access
        super().__init__(name, **kwargs)


class Boundaries(UserList):
    def append(self, item: Boundary) -> None:
        if not isinstance(item, Boundary):
            raise TypeError(f"{item} is not of type tmnpy.dsl.Boundary.")
        for i in range(len(self.data)):
            if self.data[i] == item:
                raise ValueError(f"{item} is already in this list.")
        super().append(item)

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
