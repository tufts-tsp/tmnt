from .component import Component
from .data import Data


class Asset(Component):
    """
    As a threat model is built, assets will be assigned threats and controls
    that will provide information on what threats could be considered and what
    controls have been implemented for this component.
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO


class Lambda(Asset):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO


class ExternalEntity(Asset):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO


class Datastore(Asset):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO


class Process(Asset):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO
