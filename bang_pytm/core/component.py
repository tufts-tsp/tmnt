from .element import Element
from .data import Data
from .threat import Threat
from .control import Control


class Component(Element):

    """
    A component is very similar to an element, but it specifically refers to a
    component of the system being threat modeled (rather than an element of the
    threat model), i.e. assets and flows.
    """

    __controls: [Control] = []
    __threats: [Threat] = []
    __data: Data = None

    def __init__(self, name: str, desc: str = None, data: Data = None):
        data: Data = None
        super().__init__(name, desc)

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
