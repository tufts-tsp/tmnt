from .element import Element, Elements
from .actor import Actor

class Boundary(Element):

    """
    needs documentation
    """

    def __init__(
        self,
        name,
        elements: Elements | list = Elements(),
        **kwargs
    ):
        if isinstance(elements, list):
            elements = Elements(elements)
        elif not isinstance(elements, Elements):
            raise TypeError
        self.elements = elements
        super().__init__(name, **kwargs)


class Boundaries(Elements):
    def append(self, item: Element) -> None:
        if not isinstance(item, Boundary):
            raise TypeError(f"{item} is not of type tmnpy.dsl.Boundary.")
        for i in range(len(self.data)):
            if self.data[i] == item:
                raise ValueError(f"{item} is already in this list.")
        super().append(item)
        self.data = list(set(self.data))
