from typing import Optional
from .component import Component
from .element import Element


class Flow(Component):

    """
    A flow from a source to a destination
    """

    __src: Element
    __dst: Element

    def __init__(
        self,
        name,
        src: Element,
        dst: Element,
        **kwargs,
    ):
        self.__path = []

        self.src = src
        self.dst = dst
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


class DataFlow(Flow):
    __protocol: str
    __port: int | None
    __authentication: str
    __multifactor: bool

    def __init__(
        self,
        name: str,
        protocol: str = "Not Specified",
        port: Optional[int] = None,
        authentication: str = "Not Specified",
        multifactor_authentication: bool = True,
        **kwargs,
    ) -> None:
        self.protocol = protocol
        if port:
            self.port = port
        if authentication:
            self.authentication = authentication
        self.multifactor_authentication = multifactor_authentication
        super().__init__(name, **kwargs)

    @property
    def protocol(self) -> str:
        return self.__protocol

    @protocol.setter
    def protocol(self, value: str) -> None:
        self.__protocol = value

    @property
    def port(self) -> int | None:
        return self.__port

    @port.setter
    def port(self, value: int) -> None:
        self.__port = value

    @property
    def authentication(self) -> str | None:
        return self.__authentication

    @authentication.setter
    def authentication(self, value: str) -> None:
        self.__authentication = value

    @property
    def multifactor_authentication(self) -> bool:
        return self.__multifactor

    @multifactor_authentication.setter
    def multifactor_authentication(self, value: bool) -> None:
        self.__multifactor = value


class WorkFlow(Flow):
    __path: list

    def __init__(
        self,
        name,
        src: Element,
        dst: Element,
        path: list[Element] = [],
        **kwargs,
    ):
        super().__init__(name, src=src, dst=dst, **kwargs)
        if path == []:
            self.path = [src, dst]
        else:
            self.path = path

    @property
    def path(self) -> list[Element]:
        return self.__path

    @path.setter
    def path(self, vals: list[Element]) -> None:
        self.__path = []
        if self.src not in vals:
            vals = [self.src] + vals
        if self.dst not in vals:
            vals.append(self.dst)
        for val in vals:
            if not isinstance(val, Element):
                err = "Path must consist of tmnpy.dsl.Element,"
                err += f" {val} is not of type tmnpy.dsl.Element"
                raise ValueError(err)
            self.__path.append(val)
