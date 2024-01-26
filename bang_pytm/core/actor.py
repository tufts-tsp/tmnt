from bang_pytm.core.descriptors import varString
from bang_pytm.core.tm import TM
from .element import Element

class Actor(Element):
    """a person or organization that is represented in the threat model"""

    id = varString("", doc="")

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO
        TM._actors.append(self)
