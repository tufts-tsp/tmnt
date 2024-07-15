from .component import Component
from .data import Data
from .boundary import Boundary
from .requirement import SecurityProperty

from enum import Enum
from typing import List, Set

class Machine(Enum):

    """
    A `Machine` describes the platform of the `Asset` and how it exists in the
    environment.
    """

    NA = "N/A", "Not Applicable or Unspecified"
    PHYSICAL = "PHYSICAL", "A physical machine such as a workstation"
    VIRTUAL = "VIRTUAL", "A virtual machine"
    CONTAINER = "CONTAINER", "A containerized asset"
    SERVERLESS = "SERVERLESS", "A serverless function, such as AWS Lambda"


class DATASTORE_TYPE(Enum):

    """
    The type of datastore that is being used for the data in question.
    """

    UNKNOWN = "UNKNOWN", "Unknown or Unspecified"
    FILE_SYSTEM = "FILE_SYSTEM", "A local file system"
    SQL = "SQL", "Any SQL database, such as PostgreSQL or MySQL"
    LDAP = "LDAP", "A directory service, such as Active Directory"
    BUCKET = "BUCKET", "File storage hosted in a web service, such as AWS S3"
    OTHER = "OTHER", "A type that is not covered by the other 6"
    NOSQL = "NOSQL", "Any NOSQL style database i.e., non-relational database"


class Asset(Component):

    """
    An `Asset` is a person, structure, facility, information, and records,
    information technology systems and resources, material, process,
    relationships, or reputation that has value[1].

    As a threat model is built, assets will be assigned threats and controls
    that will provide information on what threats could be considered and what
    controls have been implemented for this component.

    Parameters
    ----------
    name : str
    open_ports : List[int]
    machine : Machine or str, default Machine.NA

    Attributes
    ----------
    name : str
        The name of the asset
    open_ports : List[int]
        If there are any open ports associated with this `Asset`, they should
        be listed here. If this `Asset` is associated with a `DataFlow` to a
        specific port, then that port must be in `open_ports`.
    machine : Machine
        The

    Notes
    -----
    .. [1] NICCS CISA. A Glossary of Common Cybersecurity Words and Phrases.

    See Also
    --------
    :func:`tmnpy.dsl.element.Element` : Parent class
    :func:`tmnpy.dsl.ExternalEntity` : A specific type of Asset
    :func:`tmnpy.dsl.Datastore` : A specific type of Asset
    :func:`tmnpy.dsl.Process` : A specific type of Asset
    """

    __open_ports: Set[int]
    __machine: Machine

    def __init__(
        self,
        name: str,
        open_ports: Set[int] | List[int] | int = set(),
        machine: Machine | str = Machine.NA,
        **kwargs
    ):
        self.open_ports = open_ports
        self.machine = machine
        super().__init__(name, **kwargs)

    @property
    def open_ports(self) -> Set[int]:
        return self.__open_ports

    @open_ports.setter
    def open_ports(self, ports: Set[int] | List[int] | int) -> None:
        if (
            (not isinstance(ports, list) and not isinstance(ports, set))
            or not all(isinstance(port, int) for port in ports)
        ):
            if isinstance(ports, int):
                ports = set([ports])
            else:
                raise TypeError("Open Ports must be a list or set of integers")
        self.__open_ports = set(ports)

    @open_ports.deleter
    def open_ports(self) -> None:
        self.__open_ports = set()

    @property
    def machine(self) -> Machine:
        return self.__machine

    @machine.setter
    def machine(self, machine: Machine | str) -> None:
        if isinstance(machine, str):
            machine = Machine[machine]
        if not isinstance(machine, Machine):
            raise TypeError("Machine must be a Machine")
        self.__machine = machine

    @machine.deleter
    def machine(self) -> None:
        self.__machine = Machine.NA

    def add_open_port(self, port: int) -> None:
        if not isinstance(port, int):
            raise TypeError(f"{port} must be an int.")
        self.open_ports.add(port)

    def remove_open_port(self, port: int) -> None:
        if not isinstance(port, int):
            raise TypeError(f"{port} must be an int.")
        self.open_ports.remove(port)


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
