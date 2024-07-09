from enum import Enum

from .component import Component
from .data import Data
from .boundary import Boundary
from .requirement import SecurityProperty


class Machine(Enum):

    """
    needs documentation
    """

    NA = "N/A"
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

    open_ports: list[int]
    trust_boundaries: list[Boundary]
    machine: Machine

    def __init__(
        self,
        name: str,
        open_ports: list[int] = [],
        machine: Machine | str = Machine.NA,
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

        if isinstance(machine, str):
            machine = Machine[machine]

        if not isinstance(machine, Machine):
            raise ValueError("Machine must be a Machine")
        self.machine = machine

        super().__init__(name, **kwargs)


class ExternalEntity(Asset):

    """
    needs documentation
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Datastore(Asset):

    """
    needs documentation
    """

    def __init__(
        self,
        name,
        # machine: Machine | str = Machine.NA,
        ds_type: DATASTORE_TYPE | str = DATASTORE_TYPE.UNKNOWN,
        **kwargs
    ):
        if isinstance(ds_type, str):
            ds_type = DATASTORE_TYPE[ds_type]

        if not isinstance(ds_type, DATASTORE_TYPE):
            raise ValueError("DATASTORE_TYPE must be a DATASTORE_TYPE")
        self.ds_type = ds_type

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
