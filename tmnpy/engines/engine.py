from enum import Enum
from uuid import uuid4, UUID
import time
class Engine(object):
    def __init__(
        self,
        name: str,
        desc: str = "N/A",
    ):
        self.__id = uuid.uuid4()
        if not isinstance(name, str):
            raise ValueError("Engine Name must be a string")
        self.__name = name
        if desc == None:
            desc = "N/A"
        if not isinstance(desc, str):
            raise ValueError("Engine Description must be a string")
        self.__desc = desc

class Event_Type(Enum):
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
