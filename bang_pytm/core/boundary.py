from .element import Element
from .actor import Actor



class Boundary(Element):
    
    """
    needs documentation
    """
    
    def __init__(self, 
                 name, 
                 boundary_owner: Actor = None, 
                 **kwargs):
        
        if not isinstance(boundary_owner, Actor) and boundary_owner is not None:
            raise ValueError("Boundary Owner must be an Actor object")
        self.boundary_owner = boundary_owner

        super().__init__(name, **kwargs)
