from enum import Enum
from uuid import uuid4, UUID
import time

class Engine(object):
    def __init__(
        self,
        name: str,
        desc: str = "N/A",
    ):
        self.__id = uuid4()
        if not isinstance(name, str):
            raise ValueError("Engine Name must be a string")
        self.__name = name
        if desc == None:
            desc = "N/A"
        if not isinstance(desc, str):
            raise ValueError("Engine Description must be a string")
        self.__desc = desc

    @property
    def eid(self) -> UUID:
        """Unique ID for the Element"""
        return self.__id

    @property
    def name(self) -> str:
        """Name of the Element"""
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        self.__name = val

    @property
    def desc(self) -> str:
        """Description of the Element"""
        return self.__desc

    @desc.setter
    def desc(self, val: str) -> None:
        self.__desc = val

class EventType(Enum):

    """
    needs documentation
    """

    ASSET = "ASSET"
    WORKFLOW = "WORKFLOW"
    THREAT = "THREAT"
    MITIGATION = "MITIGATION"

class NaturalEngine(Engine):

    """
    NatrualEngine is the system that tracks
    """

    def __init__(
        self, name: str, currentFocus: str = "None", desc: str = None,
    ):
        self.currentFocus = currentFocus
        self.previous_events = []
        self.lastevent = time.time()
        super().__init__(name,desc)

    def event(self, event_type: str):
    # Get the event and check what type it is, then plug into markov model to predict new focus.  Update list of previous events to include this.
        self.previous_events.append(event_type)
        self.lastevent = time.time()
        return
