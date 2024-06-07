import random
import logging
from typing import List

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
    description: str
    findings: list[Finding] = []
    assumptions: list = []

    def __init__(self, name: str, components: List[Component] = []):
        self._name = name
        self.__components = components

    @property
    def name(self) -> str:
        return self._name

    @property
    def components(self) -> List[Component]:
        return self.__components

    @property
    def findings(self) -> List[Finding]:
        return self.findings

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

    @property
    def assumptions(self):
        return self.assumptions

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

    def remove_component(self, component: Component = None):
        if component is None:
            raise ValueError("No component specified to remove")

        self.__components.remove(component)

    def reset(self):
        for c in self.__components:
            self.remove_component(c)

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

    def find_related_attack_vectors(self, asset: Asset) -> list[list[Element]]:
        if not isinstance(asset, (Asset)):
            raise ValueError(
                "Provided asset is not of type 'Asset' or 'Actor'"
            )

        related_attack_vectors = []

        def trace_backwards(current_asset, path, visited_assets):
            if current_asset in visited_assets:
                return
            visited_assets.add(current_asset)

            for flow in self._flows:
                # go one step upstream from asset
                if flow.dst == current_asset:
                    new_path = [flow] + path

                    # prevent oscillations
                    if len(new_path) > 1:
                        if isinstance(new_path[0], Flow) and isinstance(
                            new_path[1], Flow
                        ):
                            if new_path[0].src == new_path[1].dst:
                                continue

                    # Prevent the entire path from looping back to the asset
                    if not any(
                        (isinstance(floe, Flow) and (floe.src == asset))
                        for floe in new_path
                    ):
                        related_attack_vectors.append(new_path)
                        trace_backwards(
                            flow.src, new_path, visited_assets.copy()
                        )

            # Trace through the parent of the current asset if it exists
            if (
                current_asset.parent
                and current_asset.parent not in visited_assets
            ):
                parent_path = [
                    current_asset.parent
                ] + path  # Include parent in the path
                related_attack_vectors.append(parent_path)
                trace_backwards(
                    current_asset.parent, parent_path, visited_assets.copy()
                )

        trace_backwards(asset, [], set())

        return related_attack_vectors

    def simulate_attack(self, component: Component):
        # print("Analyzing asset:", component)
        if not isinstance(component, (Asset)):
            raise ValueError(
                "Provided asset is not of type 'Asset' or 'Actor'"
            )

        related_attacks = []

        def trace_forwards(current_component, path, visited_components):
            if current_component in visited_components:
                # print("current component has been revisited in the same path")
                return

            visited_components.add(current_component)
            # print(f"added: {current_component} to visited components")
            for flow in self._flows:
                # print(f"analyzing flow with src: {flow.src} and dst: {flow.dst}")
                if flow.src == current_component:
                    # print(f"we matched component: {current_component}, with src: {flow.src}")
                    new_path = path + [flow]

                    # prevent oscillations
                    if len(new_path) > 1:
                        if isinstance(new_path[-1], Flow) and isinstance(
                            new_path[-2], Flow
                        ):
                            if new_path[-1].dst == new_path[-2].src:
                                # print("Skipping due to immediate return to previous node.")
                                continue

                    # Prevent the entire path from looping back to the asset
                    if not any(
                        (isinstance(floe, Flow) and (floe.dst == component))
                        for floe in new_path
                    ):
                        related_attacks.append(new_path)
                        trace_forwards(
                            flow.dst, new_path, visited_components.copy()
                        )

            if hasattr(current_component, "children"):
                for child in current_component.children:
                    if child not in visited_components:
                        child_path = path + ["Child: " + child.name]
                        related_attacks.append(child_path)
                        trace_forwards(
                            child, child_path, visited_components.copy()
                        )

        trace_forwards(component, [], set())

        return related_attacks
