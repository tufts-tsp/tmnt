import random
import logging
from typing import List

from bang_pytm.engine import Engine

from .data import Data
from .component import Component
from .finding import Finding
from .flow import Flow
from .asset import Asset
from .element import Element
from .actor import Actor

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
    name : str
    description : str
    findings : list[Finding] = []
    assumptions : list = []

    def __init__(self, name: str, components: List[Component] = []):
        self.name = name
        self.__components = components

    @property
    def components(self) -> List[Component]:
        return self.__components
    
    @property
    def findings(self) -> List[Finding]:
        return self.findings
    
    def generate_threats(self, engine: Engine):
        pass

    def add_finding(self, finding: Finding = None):
        if not isinstance(finding, Finding):
            raise ValueError("No finding specified to add")
        
        if finding in self.findings:
            print("Finding is already in the model")
        else:
            self.findings.append(finding)

    def remove_finding(self, finding: Finding = None):
        if finding is None:
            raise ValueError("No finding specified to remove")
        
        self.findings.remove(finding)

    @assumptions.setter
    def assumptions(self, assumption_list: list) -> None:

        if not isinstance(assumption_list, list):
            raise ValueError("Assumptions must be provided as a list")
        
        for item in assumption_list:
            if not isinstance(item, str):
                raise ValueError("Assumptions must be strings")
        
        self.assumptions = assumption_list

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

        # type checking
        if not isinstance(asset, (Asset, Actor)):
            raise ValueError("Provided asset is not of type 'Element' or 'Actor'")
        
        related_attack_vectors = []
        processed_assets = set()
        path = []

        def helper(asset, path):
            if asset in processed_assets:
                return
            processed_assets.add(asset)

            for flow in self._flows:
                # find flows incident to this asset
                if flow.dst == asset:
                    new_path = path + [flow]
                    related_attack_vectors.append(new_path)
                    # chainnnnnnn
                    if flow.src in self._elements:
                        helper(flow.src, new_path)
            
            if asset.parent in self._elements:
                new_path = path + [asset.parent]
                related_attack_vectors.append(new_path)
                helper(asset.parent, new_path)
        
        helper(asset, path)
        return related_attack_vectors


    def simulate_attack(self, component: Component):

        # type checking
        if not isinstance(component, (Component, Actor)):
            raise ValueError("Provided asset is not of type 'Element' or 'Actor'")
        
        related_paths = []
        processed_components = set()
        path = []

        def helper(component, path):
            if component in processed_components:
                return
            processed_components.add(component)

            for flow in self._flows:

                if flow.src == component:
                    new_path = path + [flow]
                    related_paths.append(new_path)

                    if flow.dst in self._elements:
                        helper(flow.dst, new_path)
            
            if component.child in self._elements:
                new_path = path + [component.child]
                related_paths.append(new_path)
                helper(component.child, new_path)
        
        helper(component, path)
        return related_paths

