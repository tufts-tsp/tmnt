import json
import re
from .engine import Engine
from bang_pytm.core.asset import Asset, ExternalEntity, Datastore, Process
from bang_pytm.core.finding import Finding
from bang_pytm.core.control import Control
from bang_pytm.core.flow import DataFlow
from bang_pytm.util import sources
from bang_pytm.core.tm import TM
from bang_pytm.core.component import Component
from bang_pytm.core.threat import Issue

# from typing import List


class Rules(Engine):
    """
    Rules represent a list of rules. The default ruleset is the pytm threatlib.
    """

    __threatmap: list  # list of Rules

    def __init__(self, threatmap: list = None) -> None:
        if threatmap == None:
            self.__threatmap = self.parse_pytm_threatlib()
        else:
            self.__threatmap = threatmap

    @property
    def threatmap(self) -> type:
        return self.__threatmap

    @threatmap.setter
    def threatmap(self, x):
        self.__threatmap = x

    # Given Rules and a Component, return the unmitigated and mitigated threats for that Component
    def component_threats(self, component):
        mitigated_threats = []
        unmitigated_threats = []
        applicable_rules = [
            t for t in self.__threatmap if type(component) == t.component
        ]
        for r in applicable_rules:
            result = r.mitigated_threat(component)
            if result["is_mitigated"]:
                mitigated_threats.append(result["threat"])
            else:
                unmitigated_threats.append(result["threat"])
        return mitigated_threats, unmitigated_threats

    # Parses the rules found in the threats.json file of pytm, stores it as a list of Rules
    def parse_pytm_threatlib(self):
        with open(
            "bang_pytm/util/pytm_threatlib.json", "r", encoding="utf8"
        ) as f:
            data = json.load(f)
        capec = sources.load_capec()
        pytm_rules = []

        for d in data:
            # get CAPEC ID
            capec_ref = re.search(
                "capec\.mitre\.org\/data\/definitions\/(\d*)\.html",
                d["references"],
            )
            if capec_ref:
                capec_id = capec_ref.group(1)
                for c in capec:
                    if c.meta["ref_id"] == "CAPEC-" + capec_id:
                        threat = c
            else:
                threat = Issue(d["description"])

            # get controls
            controls_strs = re.findall(
                "target\.controls\.(\w*) is (True|False)", d["condition"]
            )  # pretty sure it's always False
            controls_list_2 = re.findall(
                "target\.controls\.(\w*)", d["condition"]
            )

            controls_list = []
            for i, c in enumerate(controls_strs):
                controls_list.append(Control(id=i, title=c[0]))

            # TODO - Currently stores controls as a regular list, ignoring logical relationships
            # EXAMPLE EXPRESSION: s = "(target.hasDataLeaks() or any(d.isCredentials or d.isPII for d in target.data)) and (not target.controls.isEncrypted or (not target.isResponse and any(d.isStored and d.isDestEncryptedAtRest for d in target.data)) or (target.isResponse and any(d.isStored and d.isSourceEncryptedAtRest for d in target.data)))"
            # "condition": "target.usesEnvironmentVariables is True and target.controls.sanitizesInput is False and target.controls.checksInputBounds is False"
            # control_conditions = re.findall('(and|or)', d["condition"])
            # filtered_control_conditions = []
            # for i in range(len(controls_list) - 1):
            #     if control_conditions[i] in ['and', 'or']:
            #         filtered_control_conditions.append(control_conditions[i])

            # create separate rules object for each target
            for t in d["target"]:
                if t in ["Process", "Datastore", "ExternalEntity"]:
                    pytm_rules.append(
                        Rule(globals()[t], threat, controls_list)
                    )
                elif t == "Dataflow":
                    pytm_rules.append(Rule(DataFlow, threat, controls_list))
                elif t in ["Server", "Lambda"]:
                    pytm_rules.append(Rule(Asset, threat, controls_list))
                else:
                    raise Exception("Unknown Asset type")
        return pytm_rules


class Rule:
    """
    A Rule represents a potential Issue for a type of Component, and the Controls necessary to mitigate this Issue.
    """

    __component: type
    __issue: Issue
    __controls: list

    def __init__(
        self,
        component: type,
        issue: Issue,
        controls: list = None,
    ) -> None:
        self.__component = component
        self.__issue = issue
        self.__controls = controls

    @property
    def component(self) -> type:
        return self.__component

    @component.setter
    def component(self, x):
        self.__component = x

    @property
    def issue(self) -> Issue:
        return self.__issue

    @issue.setter
    def issue(self, x):
        self.__issue = x

    @property
    def controls(self) -> list:
        return self.__controls

    @controls.setter
    def controls(self, x):
        self.__controls = x

    # Given a Rule and an Asset with some Controls, use the Rule to determine whether the Threat applies on this Asset. Return the Threat, True iff it was mitigated, and the Controls that were found to apply/not apply.
    def mitigated_threat(self, component: Asset):
        applied_controls = []
        not_applied_controls = []
        for control in self.controls:
            if control.title in [x.title for x in component.controls]:
                applied_controls.append(control)
            else:
                not_applied_controls.append(control)

        # TODO - Currently returns mitigated if any one of the controls is applied, ignoring logical relationships between conditions.
        is_mitigated = True if len(applied_controls) > 0 else False

        return {
            "threat": self.issue,
            "is_mitigated": is_mitigated,
            "applied_controls": applied_controls,
            "not_applied_controls": not_applied_controls,
        }
