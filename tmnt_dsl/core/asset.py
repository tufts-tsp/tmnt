from .component import Component
from .data import Data
from .boundary import Boundary
from enum import Enum


class Machine(Enum):

    """
    needs documentation
    """

    PHYSICAL = "PHYSICAL"
    VIRTUAL = "VIRTUAL"
    CONTAINER = "CONTAINER"
    SERVERLESS = "SERVERLESS"


class DATASTORE_TYPE(Enum):

    """
    needs documentation
    """

    UNKNOWN = "UNKNOWN"
    FILE_SYSTEM = "FILE_SYSTEM"
    SQL = "SQL"
    LDAP = "LDAP"
    BUCKET = "BUCKET"
    OTHER = "OTHER"
    NOSQL = "NOSQL"


class Asset(Component):

    """
    As a threat model is built, assets will be assigned threats and controls
    that will provide information on what threats could be considered and what
    controls have been implemented for this component.
    """

    def __init__(
        self,
        name: str,
        open_ports: list[int] = [],
        trust_boundaries: list[Boundary] = [],
        machine: Machine = Machine.PHYSICAL,
        **kwargs
    ):
        if (
            not isinstance(open_ports, list)
            or not all(isinstance(port, int) for port in open_ports)
        ) and open_ports is not None:
            if isinstance(open_ports, int):
                self.open_ports = [open_ports]
            else:
                raise ValueError("Open Ports must be a list of integers")
        self.open_ports = open_ports

        if (
            not isinstance(trust_boundaries, list)
            or not all(
                isinstance(boundary, Boundary) for boundary in trust_boundaries
            )
        ) and trust_boundaries is not None:
            if isinstance(trust_boundaries, Boundary):
                self.boundaries = [trust_boundaries]
            else:
                raise ValueError(
                    "Trust Boundaries must be a list of Boundary objects"
                )
        self.boundaries = trust_boundaries

        if not isinstance(machine, Machine):
            raise ValueError("Machine must be a Machine")
        self.machine = machine

        super().__init__(name, **kwargs)


class ExternalEntity(Asset):

    """
    needs documentation
    """

    def __init__(self, name, physical_access: bool = False, **kwargs):
        if not isinstance(physical_access, bool):
            raise ValueError("Physical Access must be a boolean")
        self.physical_access = physical_access

        super().__init__(name, **kwargs)


class Datastore(Asset):

    """
    needs documentation
    """

    def __init__(
        self, name, ds_type: DATASTORE_TYPE = DATASTORE_TYPE.UNKNOWN, **kwargs
    ):
        if not isinstance(ds_type, DATASTORE_TYPE):
            raise ValueError("DS Type must be a DATASTORE_TYPE object")
        self.ds_type = ds_type
        if ds_type == DATASTORE_TYPE.OTHER and "desc" not in kwargs.keys():
            raise AttributeError(
                "If specifying OTHER for the datastore type please include a description."
            )
        super().__init__(name, **kwargs)


class Process(Asset):

    """
    needs documentation
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
