from .component import Component
from .data import Data
from .boundary import Boundary

from typing import List
from enum import Enum

class Machine(Enum):

    PHYSICAL="PHYSICAL"
    VIRTUAL="VIRTUAL"
    CONTAINER="CONTAINER"
    SERVERLESS="SERVERLESS"

class DATASTORE_TYPE(Enum):

    UNKNOWN="UNKNOWN"
    FILE_SYSTEM="FILE_SYSTEM"
    SQL="SQL"
    LDAP="LDAP"
    BUCKET="BUCKET"
    OTHER="OTHER"

class Asset(Component):
    """
    As a threat model is built, assets will be assigned threats and controls
    that will provide information on what threats could be considered and what
    controls have been implemented for this component.
    """

    def __init__(
        self,
        name,
        open_ports: list = [],
        trust_boundaries: List[Boundary] = [],
        machine: Machine = Machine.PHYSICAL,
        **kwargs
    ):
        self.open_ports = open_ports
        self.boundaries = trust_boundaries
        self.machine = machine
        super().__init__(name, **kwargs)

class ExternalEntity(Asset):
    def __init__(self, name, physical_access: bool = False, **kwargs):
        self.physical_access = physical_access
        super().__init__(name, **kwargs)

class Datastore(Asset):
    def __init__(self, name, ds_type: DATASTORE_TYPE = DATASTORE_TYPE.UNKNOWN,  **kwargs):
        """
        If other then fill in description
        """
        self.ds_type = ds_type
        if ds_type == DATASTORE_TYPE.OTHER and 'desc' not in kwargs.keys():
            raise AttributeError("If specifying OTHER for the datastore type please include a description.")
        super().__init__(name, **kwargs)

class Process(Asset):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)