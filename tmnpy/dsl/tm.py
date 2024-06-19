import random
import logging
from typing import List

from tmnpy.dsl.boundary import Boundary

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

    def __init__(
        self,
        name: str,
        components: List[Component] = [],
        actors: List[Actor] = [],
        boundaries: List[Boundary] = [],
    ):
        self.__assumptions = []
        self.__assets = []
        self.__actors = []
        self.__components = []
        self.__boundaries = []
        self.__flows = []

        self._name = name

        for c in components:
            self.add_component(c)
        for a in actors:
            self.add_actor(a)
        for b in boundaries:
            self.add_boundary(b)

    @property
    def name(self) -> str:
        return self._name

    @property
    def components(self) -> List[Component]:
        return self.__components

    def add_component(self, component: Component):
        if component is None:
            raise ValueError("No component specified to add")
        elif not isinstance(component, Component):
            raise TypeError(
                "Specified component is not of type tmnpy.dsl.Component"
            )

        if component in self.__components:
            print("Component is already in the model")
        else:
            self.__components.append(component)

        if isinstance(component, Asset):
            self.__assets.append(component)
        elif isinstance(component, Flow):
            self.__flows.append(component)

    def remove_component(self, component: Component):
        if component is None:
            raise ValueError("No component specified to remove")
        elif not isinstance(component, Component):
            raise TypeError(
                "Specified component is not of type tmnpy.dsl.Component"
            )

        self.__components.remove(component)

    @property
    def actors(self) -> List[Actor]:
        return self.__actors

    def add_actor(self, actor: Actor):
        if actor is None:
            raise ValueError("No actor specified to add")
        elif not isinstance(actor, Actor):
            raise TypeError("Specified actor is not of type tmnpy.dsl.Actor")

        if actor in self.__actors:
            print("Actor is already in the model")
        else:
            self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor is None:
            raise ValueError("No actor specified to remove")
        elif not isinstance(actor, Actor):
            raise TypeError("Specified actor is not of type tmnpy.dsl.Actor")

        self.__actors.remove(actor)

    @property
    def boundaries(self) -> List[Boundary]:
        return self.__boundaries

    def add_boundary(self, boundary: Boundary):
        if boundary is None:
            raise ValueError("No boundary specified to add")
        elif not isinstance(boundary, Boundary):
            raise TypeError(
                "Specified boundary is not of type tmnpy.dsl.Boundary"
            )

        if boundary in self.__boundaries:
            print("Boundary is already in the model")
        else:
            self.__boundaries.append(boundary)

    def remove_boundary(self, boundary: Boundary):
        if boundary is None:
            raise ValueError("No boundary specified to remove")
        elif not isinstance(boundary, Boundary):
            err = "Specified boundary is not of type tmnpy.dsl.Boundary"
            raise TypeError(err)

        self.__boundaries.remove(boundary)

    @property
    def findings(self) -> List[Finding]:
        return self.findings

    def add_finding(self, finding: Finding):
        if not isinstance(finding, Finding):
            raise ValueError("No finding specified to add")

        if finding in self.findings:
            print("Finding is already in the model")
        else:
            self.findings.append(finding)

    def remove_finding(self, finding: Finding):
        if finding is None:
            raise ValueError("No finding specified to remove")
        elif not isinstance(finding, Finding):
            err = "Specified boundary is not of type tmnpy.dsl.Finding"
            raise TypeError(err)

        self.findings.remove(finding)

    @property
    def assumptions(self):
        return self.__assumptions

    @assumptions.setter
    def assumptions(self, assumption_list: list) -> None:
        if not isinstance(assumption_list, list):
            raise ValueError("Assumptions must be provided as a list")

        for item in assumption_list:
            if not isinstance(item, str):
                raise ValueError("Assumptions must be strings")

        self.__assumptions = assumption_list

    def reset(self):
        self.__components = []
        self.__actors = []
        self.__boundaries = []
        self.__assumptions = []

    def describe_data(self, data: Data):
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
        if kind is None:
            return self.__flows
        flows = []
        for flow in self.__flows:
            if isinstance(flow, kind):
                flows.append(flow)
        return flows

    def enumerate_all_assets(self, kind: Asset) -> List[Asset]:
        ## Give a list of all the assets, able to filter with kind
        if kind is not None:
            return self.__assets
        assets = []
        for asset in self.__assets:
            if isinstance(asset, kind):
                asset_list.append(asset)

    def find_related_attack_vectors(
        self, initial: Component | Actor
    ) -> list[list[Component]]:
        if not isinstance(initial, (Component, Actor)):
            err = "Provided asset is not of type tmnpy.dsl.Component or tmnpy.dsl.Actor"
            raise ValueError(err)

        related_attack_vectors = []

        def trace_backwards(current_asset, path, visited_assets):
            if current_asset in visited_assets:
                return
            visited_assets.add(current_asset)

            for flow in self.__flows:
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
                        (isinstance(floe, Flow) and (floe.src == initial))
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

        trace_backwards(initial, [], set())

        return related_attack_vectors

    def simulate_attack(self, target: Component):
        # print("Analyzing asset:", component)
        if not isinstance(target, (Component | Actor)):
            err = "Provided target is not of type tmnpy.dsl.Component or tmnpy.dsl.Actor"
            raise ValueError(err)

        related_attacks = []

        def trace_forwards(current_component, path, visited_components):
            if current_component in visited_components:
                # print("current component has been revisited in the same path")
                return

            visited_components.add(current_component)
            # print(f"added: {current_component} to visited components")
            for flow in self.__flows:
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
                        (isinstance(floe, Flow) and (floe.dst == target))
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

        trace_forwards(target, [], set())

        return related_attacks
