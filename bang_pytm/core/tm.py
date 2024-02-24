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

    def __init__(self, name: str, components: List[Component] = []):
        self.name = name
        self.__components = components

    @property
    def components(self) -> List[Component]:
        return self.__components
    
    @property
    def findings(self) -> List[Finding]:
        return self.__findings
    
    def generate_threats(self, engine: Engine):
        pass

    def add_finding(self, finding: Finding = None):
        pass

    def remove_finding(self, finding: Finding = None):
        pass

    def add_component(self, component: Component = None):
        pass

    def remove_component(self, component: Component = None):
        pass
