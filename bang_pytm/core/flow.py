from .component import Component
from .element import Element



class Flow(Component):
    
    """
    A flow from a source to a destination
    """

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

        self.src = self.__check_parent(src)
        self.dst = self.__check_parent(dst)

        self.authentication = authentication
        self.multifactor_authentication = multifactor_authentication
        
        if path == []:
            self.path = [src, dst]
        else:
            self.path = path
        super().__init__(name, **kwargs)

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
        self.__path = [self.__check_parent(val) for val in vals]

    def __check_parent(self, obj):
        if obj.parent is None:
            return obj
        else:
            return obj.parent


class DataFlow(Flow):

    def __init__(self, name: str, protocol: str = None, port: int = None, **kwargs) -> None:
        self.protocol = protocol
        self.port = port
        super().__init__(name, **kwargs)


class WorkFlow(Flow):

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)()