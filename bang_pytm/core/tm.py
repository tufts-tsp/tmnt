import random
import logging


from bang_pytm.core.descriptors import varString, varFindings, varStrings

logger = logging.getLogger(__name__)


class TM:
    """Describes the threat model administratively,
    and holds all details during a run"""

    _flows = []
    _elements = []
    _actors = []
    _assets = []
    _threats = []
    _boundaries = []
    _data = []
    name = varString("", required=True, doc="Model name")
    description = varString("", required=True, doc="Model description")
    findings = varFindings([], doc="threats found for elements of this model")
    assumptions = varStrings(
        [],
        required=False,
        doc="A list of assumptions about the design/model.",
    )

    def __init__(self, name, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.name = name
        self._init_threats()
        random.seed(0)

    @classmethod
    def reset(cls):
        cls._flows = []
        cls._elements = []
        cls._actors = []
        cls._assets = []
        cls._threats = []
        cls._boundaries = []
        cls._data = []

    def _init_threats(self):
        # TO BE IMPLEMENTED
        pass

    def report(self):
        # TO BE IMPLEMENTED
        pass
