from .element import Element
from .actor import Actor

class Boundary(Element):
    def __init__(self, name, boundary_owner: Actor = None, **kwargs):
        self.boundary_owner = boundary_owner
        super().__init__(name, **kwargs)
