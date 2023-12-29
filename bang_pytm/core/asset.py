from .element import Element
from .control import Control
from .threat import Threat
from .data import Data


class Asset(Element):
    """
    As a threat model is built, assets will be assigned threats and controls
    that will provide information on what threats could be considered and what
    controls have been implemented for this element.
    """

    __controls: [Control] = []
    __threats: [Threat] = []
    __data: Data = None

    def __init__(self, name, desc: str = None, data: Data = None):
        self.data = data
        super().__init__(name, desc)
        # TO DO

    @property
    def data(self) -> Data:
        return self.__data

    @data.setter
    def data(self, val: Data) -> None:
        self.__data = val

    @property
    def threats(self) -> list[Threat]:
        """
        Threats that have been assigned to the Asset

        Threats must be unique, any specifics of what threats can be assigned
        to what assets can be found in Threat.
        """
        return self.__threats

    def add_threat(self, threat: Threat) -> None:
        self.__add_elem(threat, self.__threats)

    def remove_threat(self, threat: Threat) -> None:
        self.__remove_elem(threat, self.__threats)

    @property
    def controls(self) -> list[Control]:
        """
        Controls that have been assigned to the Asset

        Controls must be unique, any specifics of what controls can be assigned
        to what assets can be found in Control.
        """
        return self.__controls

    def add_control(self, control: Control) -> None:
        self.__add_elem(control, self.__controls)

    def remove_control(self, control: Control) -> None:
        self.__remove_elem(control, self.__controls)


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
