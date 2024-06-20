from .component import Component
from .element import Element


class Flow(Component):

    """
    A flow from a source to a destination
    """

    def __init__(
        self,
        name,

        src: Element,
        dst: Element,
        path: list[Element] = [],
        authentication: str = "",
        multifactor_authentication: bool = True,
        **kwargs,
    ):
        # self.src = self.__check_parent(src)
        # self.dst = self.__check_parent(dst)

        self.__src = src
        self.__dst = dst

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
        if not isinstance(elem, Element):
            err = "Destination element must be of type tmnpy.dsl.Element"
            raise ValueError(err)
        self.__src = elem

    @property
    def dst(self) -> Element:
        return self.__dst

    @dst.setter
    def dst(self, elem: Element) -> None:
        if not isinstance(elem, Element):
            err = "Destination element must be of type tmnpy.dsl.Element"
            raise ValueError(err)
        self.__dst = elem

    @property
    def path(self) -> list[Element]:
        return self.__path

    @path.setter
    def path(self, vals: list[Element]) -> None:
        for val in vals:
            if not isinstance(val, Element):
                err = "Path must consist of tmnpy.dsl.Element,"
                err += f" {val} is not of type tmnpy.dsl.Element"
                raise ValueError(err)
        self.__path = vals

    def __check_parent(self, obj):
        if obj.parent is None:
            return obj
        else:
            return obj.parent


class DataFlow(Flow):
    def __init__(
        self,
        name: str,
        protocol: str = "None",
        port: int | None = None,
        **kwargs,
    ) -> None:
        self.protocol = protocol
        self.port = port
        super().__init__(name, **kwargs)


class WorkFlow(Flow):
    def __init__(self, name, path: list[Element] = [], **kwargs):
        super().__init__(name, **kwargs)
