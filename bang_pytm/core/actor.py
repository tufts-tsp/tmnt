from .element import Element


class Actor(Element):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO
