from .element import Element
from .control import Control
from .threat import Threat
from .data import Data


class Flow(Element):
    """A flow from a source to a destination"""

    __src: Element = None
    __dst: Element = None
    __path: list[Element] = []
    __controls: [Control] = []
    __threats: [Threat] = []

    def __init__(
        self,
        name,
        desc: str = None,
        src: Element = None,
        dst: Element = None,
        path: list[Element] = [],
    ):
        self.src = src
        self.dst = dst
        if path == []:
            self.path = [src, dst]
        super().__init__(name, desc)
        # TO DO

    @property
    def src(self) -> Element:
        return self.__src

    @src.setter
    def src(self, elem: Element) -> None:
        self.__src = elem

    @property
    def dst(self) -> Element:
        return self.__dst

    @dst.setter
    def dst(self, elem: Element) -> None:
        self.__dst = elem

    @property
    def path(self) -> list[Element]:
        return self.__path

    @path.setter
    def path(self, vals: list[Element]) -> None:
        self.__path = vals

    @property
    def threats(self) -> list[Threat]:
        """
        Threats that have been assigned to the Flow

        Threats must be unique, any specifics of what threats can be assigned
        to what flows can be found in Threat.
        """
        return self.__threats

    def add_threat(self, threat: Threat) -> None:
        if threat not in self.__threats:
            self.__threats.append(threat)
        else:
            err = f"{threat} has already been added to {self.name}"
            raise AttributeError(err)

    def remove_threat(self, threat: Threat) -> None:
        if threat in self.__threats:
            self.__threats.remove(threat)
        else:
            err = f"{threat} has not been assigned to {self.name}"
            raise AttributeError(err)

    @property
    def controls(self) -> list[Control]:
        """
        Controls that have been assigned to the Flow

        Controls must be unique, any specifics of what controls can be assigned
        to what flows can be found in Control.
        """
        return self.__controls

    def add_control(self, control: Control) -> None:
        if control not in self.__controls:
            self.__controls.append(control)
        else:
            err = f"{control} has already been added to {self.name}"
            raise AttributeError(err)

    def remove_control(self, control: Control) -> None:
        if control in self.__controls:
            self.__threats.remove(control)
        else:
            err = f"{control} has not been assigned to {self.name}"
            raise AttributeError(err)


class WorkFlow(Flow):
    """A workflow from a source to a destination"""

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # TO DO


class DataFlow(Flow):
    """A dataflow from a source to a destination"""

    __data: Data = None

    def __init__(self, name, data: Data = None, **kwargs):
        self.data = data
        super().__init__(name, **kwargs)
        # TO DO

    @property
    def data(self) -> Data:
        return self.__data

    @data.setter
    def data(self, val: Data) -> None:
        self.__data = val
