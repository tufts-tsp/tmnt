from typing import List

from .component import Component
from .finding import Finding

from bang_pytm.engine.engine import Engine

class TM(object):
    
    __components: List[Component] = []
    __findings: List[Finding] = []

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
