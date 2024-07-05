from .element import Element

from collections import UserList
from typing import Optional


class Actor(Element):

    """
    a person or organization that is represented in the threat model
    """

    def __init__(
        self,
        name,
        actor_type: Optional[str] = None,
        physical_access: bool = False,
        **kwargs,
    ):
        """
        Actor

        actor_type : str
            Options: Individual, Organization ... User can specify
        associated_assets : List[Asset]
            In the case of external orgs/individuals these would be External Entity
        admin_assets : List[Asset]
            Should be a subset of associated_assets, i.e. if you are adding
            admin asset that is not present in associated it should be added to
            it as well
        """

        if not isinstance(physical_access, bool):
            raise TypeError("Physical Access must be a boolean")
        else:
            self.physical_access = physical_access

        if not isinstance(actor_type, str) and actor_type is not None:
            raise TypeError("Actor Type must be a string or None")
        else:
            self.actor_type = actor_type

        super().__init__(name, **kwargs)


class Actors(UserList):
    def append(self, item: Actor) -> None:
        if not isinstance(item, Actor):
            raise TypeError(f"{item} is not of type tmnpy.dsl.Actor.")
        for i in range(len(self.data)):
            if self.data[i] == item:
                raise ValueError(f"{item} is already in this list.")
        super().append(item)

    def index(self, name: str, *args) -> int:
        ctype = None
        if args:
            ctype = args[0]
        for i in range(len(self.data)):
            if name == self.data[i].name and ctype == None:
                return i
            elif name == self.data[i].name and ctype == type(self.data[i]):
                return i
        raise ValueError(f"{name} is not in list.")
