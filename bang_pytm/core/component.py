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

    __controls: list[Control] = []
    __threats: list[Threat] = []
    __data: list[Data] = []

    def __init__(self, name: str, desc: str = None, data_list: list[Data] = []) -> None:
  
        self.data = data_list

        super().__init__(name, desc)

    @property
    def data(self) -> Data:
        return self.__data

    @data.setter
    def data(self, val: list[Data]) -> None:
        if not isinstance(val, list) or not all(isinstance(item, Data) for item in val):
            raise ValueError("Value must be a list of Data objects")
        self.__data = val
    
    def add_data(self, val: Data) -> None:

        if not isinstance(val, Data):
            raise ValueError("Value must be a Data object")
        
        self.__data.append(val)

    def remove_data(self, val: Data) -> None:

        if val is None:
            raise ValueError("No data value specified to remove")
        
        if not isinstance(val, Data):
            raise ValueError("Value must be a Data object")
        
        self.__data.remove(val)

    def add_data(self, val: Data) -> None:
        self.__data.append(val)

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
