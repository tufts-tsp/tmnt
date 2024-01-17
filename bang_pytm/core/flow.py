from .component import Component


class Flow(Component):
    """A flow from a source to a destination"""

    __src: Component = None
    __dst: Component = None
    __path: list[Component] = []

    def __init__(
        self,
        name,
        src: Component = None,
        dst: Component = None,
        path: list[Component] = [],
        flow_type: str = "DataFlow",
        **kwargs
    ):
        self.src = src
        self.dst = dst
        self.flow_type = flow_type
        if path == []:
            self.path = [src, dst]
        super().__init__(name, **kwargs)
        # TO DO

    @property
    def src(self) -> Component:
        return self.__src

    @src.setter
    def src(self, elem: Component) -> None:
        self.__src = elem

    @property
    def dst(self) -> Component:
        return self.__dst

    @dst.setter
    def dst(self, elem: Component) -> None:
        self.__dst = elem

    @property
    def path(self) -> list[Component]:
        return self.__path

    @path.setter
    def path(self, vals: list[Component]) -> None:
        self.__path = vals
