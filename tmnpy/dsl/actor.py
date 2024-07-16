from .element import Element, Elements
from .component import Component, Components

from typing import Optional, Set


class Actor(Element):

    """
    An actor is a person, organization, or other entity that is not governed by
    machine logic. Actors can have physical access to components, such as if
    they are on on-site administrator, or no access if they are remote.
    Additionally, actors should be specified if they are internal to the
    organization that is building the threat model, e.g. a software developer,
    or if they are external, such as a contractor or a third-party that
    provides some service. An external actor is not an external service, such
    as externally managed source control, which instead is an external entity.

    Parameters
    ----------
    name : str
        Name of actor
    actor_type : str
        Options: Individual, Organization ... User can specify
    physical_access: Components
        What components within the threat model does this actor has physical
        access to.
    internal : bool
        Are they an internal or external actor?
    **kwargs : dict, optional
        Extra arguments to `Element`: refer to each metric documentation for a
        list of all possible arguments.

    See Also
    --------
    ExternalEntity :
        An external entity that is not directly addressed in the threat model.

    Notes
    -----
    Because the line between an `ExternalEntity` and `Actor(internal=False)`
    is not clear in many cases these will be treated similarly in the threat
    and control assignment process.
    """

    def __init__(
        self,
        name,
        actor_type: Optional[str] = None,
        internal: bool = False,
        physical_access: Components = Components(),
        **kwargs,
    ):
        if not isinstance(actor_type, str) and actor_type is not None:
            raise TypeError("Actor Type must be a string or None")
        else:
            self.actor_type = actor_type

        if not isinstance(internal, bool):
            raise TypeError("Internal must be a boolean")
        else:
            self.internal = internal
        if isinstance(physical_access, list):
            physical_access = Components(physical_access)
        elif not isinstance(physical_access, Components):
            raise TypeError
        self.physical_access = physical_access

        super().__init__(name, **kwargs)


class Actors(Elements):
    def append(self, item: Element) -> None:
        if not isinstance(item, Actor):
            raise TypeError(f"{item} is not of type tmnpy.dsl.Actor.")
        for i in range(len(self.data)):
            if self.data[i] == item:
                raise ValueError(f"{item} is already in this list.")
        super().append(item)
        self.data = list(set(self.data))
