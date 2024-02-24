from .component import Component
from .element import Element

class Flow(Component):
    """A flow from a source to a destination"""

    __src: Element = None
    __dst: Element = None
    __path: list[Element] = []

    def __init__(
        self,
        name,
        src: Element = None,
        dst: Element = None,
        path: list[Element] = [],
        authentication: str = None,
        multifactor_authentication: bool = True,
        **kwargs
    ):
        """
        authentication : 

        """
        self.src = src
        self.dst = dst
        self.authentication = authentication
        self.multifactor_authentication = multifactor_authentication
        if path == []:
            self.path = [src, dst]
        super().__init__(name, **kwargs)
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


class DataFlow(Flow):

    def __init__(self, name: str, protocol: str = None, port: int = None, **kwargs) -> None:
        self.protocol = protocol
        self.port = port
        super().__init__(name, **kwargs)


class WorkFlow(Flow):

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)()