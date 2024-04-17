from .element import Element
from .data import Data
from .threat import Threat
from .control import Control
from typing import Dict, List


class Component(Element):

    """
    A component is very similar to an element, but it specifically refers to a
    component of the system being threat modeled (rather than an element of the
    threat model), i.e. assets and flows.
    """

    __controls: List[Control] = []
    __threats: List[Threat] = []
    __data: List[Data] = None

    def __init__(self, name: str, desc: str = None, data: List[Data] = []) -> None:
        if data != None and type(data) == list:
            self.data = data
        elif data!= None:
            self.data = [data]
        super().__init__(name, desc)

    @property
    def data(self) -> Data:
        return self.__data

    @data.setter
    def data(self, data: List[Data]) -> None:
        self.__data = data

    def remove_data(self, val: Data) -> None:
        self.__data.remove(val)

    def add_data(self, val: Data) -> None:
        self.__data.add(val)

    @property
    def threats(self) -> list[Threat]:
        """
        Threats that have been assigned to the Asset

        Threats must be unique, any specifics of what threats can be assigned
        to what assets can be found in Threat.
        """
        return self.__threats

    def add_threat(self, threat: Threat) -> None:
        self.__threats.append(threat)

    def remove_threat(self, threat: Threat) -> None:
        self.__threats.remove(threat)

    @property
    def controls(self) -> list[Control]:
        """
        Controls that have been assigned to the Asset

        Controls must be unique, any specifics of what controls can be assigned
        to what assets can be found in Control.
        """
        return self.__controls

    def add_control(self, control: Control) -> None:
        self.__controls.append(control)

    def remove_control(self, control: Control) -> None:
        self.__controls.remove(control)
