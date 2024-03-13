import random
import logging
from typing import List

from bang_pytm.engine import Engine

from .descriptors import varString, varFindings, varStrings
from .data import Data
from .component import Component
from .finding import Finding
from .flow import Flow
from .asset import Asset
from .element import Element

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
        
        if component is None:
            raise ValueError("No component specified to add")
        
        if not isinstance(component, Component):
            raise TypeError("Specified component is not of type 'Component")
        
        if component in self.__components:
            print("Component is already in the model")
        else:
            self.__components.append(component)

        
        self.__components.append(component)


    def remove_component(self, component: Component = None):
        
        if component is None:
            raise ValueError("No component specified to remove")
        
        self.__components.remove(component)


    def describe_data(self, data: Data = None):
        # Provide user with the components that process, send, receive, store
        # this data

        if data is None:
            raise ValueError("Data object must be provided")
        
        associated_components = []

        for component in self.__components:
            if data in component.data:
                associated_components.append(data)
        
        return associated_components


    def enumerate_all_flows(self, kind: Flow) -> List[Flow]:
        # Give a list of all the flows, able to filter with kind
        
        flow_list = []
        
        if kind is not None:
            for flow in self._flows:
                if isinstance(flow, kind):
                    flow_list.append(flow)
        else:
            return self._flows.copy()

    def enumerate_all_assets(self, kind: Asset) -> List[Asset]:
        ## Give a list of all the assets, able to filter with kind
        
        asset_list = []

        if kind is not None:
            for asset in self._assets:
                if isinstance(asset, kind):
                    asset_list.append(asset)
        else:
            return self._assets.copy()

    def find_related_attack_vectors(self, asset: Asset):
        # Find all the flows where the asset is the destination, then grab 
        # assets and then recurse 
        pass

    def simulate_attack(self, component: Component):
        # If someone were to attack and breach, what things could they hop to
        # or otherwise get access to - reverse of find_related_attack_vectors, 
        # i.e. start with initial attack surface how far they can go
        pass