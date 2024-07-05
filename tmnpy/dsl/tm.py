from .actor import Actor, Actors
from .asset import Asset
from .boundary import Boundary, Boundaries
from .component import Component, Components
from .data import Data
from .element import Element
from .finding import Finding, Findings
from .flow import Flow

import logging
import random
from typing import List, Optional
import uuid

logger = logging.getLogger(__name__)


class TM:
    """
    Describes the threat model administratively, and holds all details during
    a run.

    Parameters
    ----------
    name : str
    components : List[Component], default []
    actors : List[Actor], default []
    boundaries : List[Boundary], default []

    Attributes
    ----------
    name : str
    components : List[Component], default Components()
    actors : List[Actor], default Actors()
    boundaries : List[Boundary], default Boundaries()
    findings : List[Finding], default Findings()
    assumptions : List[str], default []


    Methods
    -------

    """

    __actors: Actors
    __assumptions: list
    __boundaries: Boundaries
    __components: Components

    def __init__(
        self,
        name: str,
        components: Optional[List[Component]] = None,
        actors: Optional[List[Actor]] = None,
        boundaries: Optional[List[Boundary]] = None,
    ):
        self.__assumptions = []
        self.__actors = Actors()
        self.__components = Components()
        self.__boundaries = Boundaries()
        self.__findings = Findings()

        self.__name = name
        if components:
            self.components = components
        if actors:
            self.actors = actors
        if boundaries:
            self.boundaries = boundaries

    @property
    def actors(self) -> Actors:
        return self.__actors

    @actors.setter
    def actors(self, actors: List[Actor]) -> None:
        self.__actors = Actors()
        if not isinstance(actors, list):
            raise TypeError("Must use a list of type tmnpy.dsl.Actor")
        for actor in actors:
            self.__actors.append(actor)

    @actors.deleter
    def actors(self) -> None:
        self.__actors = Actors()

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

    @property
    def boundaries(self) -> Boundaries:
        return self.__boundaries

    @boundaries.setter
    def boundaries(self, boundaries: List[Boundary]) -> None:
        self.__boundaries = Boundaries()
        if not isinstance(boundaries, list):
            raise TypeError("Must use a list of type tmnpy.dsl.Boundary")
        for boundary in boundaries:
            self.__boundaries.append(boundary)

    @boundaries.deleter
    def boundaries(self) -> None:
        self.__boundaries = Boundaries()

    @property
    def components(self) -> Components:
        return self.__components

    @components.setter
    def components(self, components: List[Component]) -> None:
        self.__components = Components()
        if not isinstance(components, list):
            raise TypeError("Must use a list of type tmnpy.dsl.Component")
        for component in components:
            self.__components.append(component)

    @components.deleter
    def components(self) -> None:
        self.__components = Components()

    @property
    def findings(self) -> Findings:
        return self.__findings

    @findings.setter
    def findings(self, findings: List[Finding]) -> None:
        self.__findings = Findings()
        if not isinstance(findings, list):
            raise TypeError("Must use a list of type tmnpy.dsl.Finding")
        for finding in findings:
            self.__findings.append(finding)

    @findings.deleter
    def findings(self) -> None:
        self.__findings = Findings()

    @property
    def name(self) -> str:
        return self.__name

    def reset(self):
        self.__components = Components()
        self.__actors = Actors()
        self.__boundaries = Boundaries()
        self.__assumptions = []
        self.__findings = Findings()

    def describe_data(self, data: Data):
        # Provide user with the components that process, send, receive, store
        # this data

        if not isinstance(data, Data):
            raise ValueError("Must provide a tmnpy.Data object")
        associated_components = []

        for component in self.__components:
            if data in component.data:
                associated_components.append(data)

        return associated_components

    def enumerate_flows(self, kind: type[Flow] = Flow) -> Components:
        # Give a list of all the flows, able to filter with kind
        return self.components.subset(kind)

    def enumerate_assets(self, kind: type[Asset] = Asset) -> Components:
        ## Give a list of all the assets, able to filter with kind
        return self.components.subset(kind)

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

            for flow in self.enumerate_flows():
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
            for flow in self.enumerate_flows():
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
