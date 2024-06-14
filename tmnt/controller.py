from threading import Lock, Thread
import time

from .dsl import TM
from .engines import Engine

class TMNTControllerMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class TMNTController(metaclass=TMNTControllerMeta):

    """
    TMNTController is what starts a TMNT threat modeling session. Your
    initialized threat model will be empty by default, or you can specify a
    file path for your YAML configuration file
    (see `examples.parser_examples`).
    You can initialize with a set of Engines or you can add them
    later, by default it uses just the basic Assignment engine. Additionally,
    if you have any reference threat models that you want to compare against,
    you can add them with `references`.
    """

    def __init__(
        self,
        name: str,
        config_file: str = "",
        engines: Engine | list[Engine] = Engine(),
        references: None | TM | list[TM] = None,
    ):
        self.created = time.time()
        self.lastmodified = time.time()
        self.tm = TM(name)
        if config_file != "":
            #parse config and add to `self.tm`
            pass
        self.engines = engines
        self.references = references
