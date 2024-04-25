from .engine import Engine
from bang_pytm.core.component import Component
from bang_pytm.core.asset import Asset
from bang_pytm.core.threat import Issue
from typing import List

# (containing a threat and the controls needed to mitigate that threat),
class Rules(Engine):
    pass

class Rule():
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
    def mitigated_threat(self, component:Asset):
        applied_controls = []
        not_applied_controls = []
        for control in self.controls:
            if control[0] in [c.name for c in component.controls]:
                applied_controls.append(control)
            else:
                not_applied_controls.append(control)
        
        # TODO - Currently returns mitigated if any one of the controls is applied, ignoring logical relationships between conditions.
        is_mitigated = True if len(applied_controls) > 0 else False
        
        return {
            'threat':self.issue, 
            'is_mitigated': is_mitigated, 
            'applied_controls': applied_controls,
            'not_applied_controls': not_applied_controls
        }
