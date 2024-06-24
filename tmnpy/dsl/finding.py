from typing import List

from .component import Component
from .control import Mitigation
from .threat import Issue
from .requirement import SecurityProperty, SafetyImpact


class Finding:
    """
    A finding consists of a Component(s), the associated Issue(s) and the
    identified Control(s). An Issue may be resolved by one or more Controls, or
    it may be deemed to not have sufficient risk to have a Control assigned, in
    which case the residual risk would be negligible.

    Finding is modeled off of the templates given in Table I-5 and Table I-7 of
    NIST 800-30. Use this document as guidance for filling in your finding.

    Parameters
    ----------
    affected_components : Component or list (required)
    issues : Issue | list (required)
    mitigations : Mitigation | list, default None
    relevance : str, default "Not Evaluated"
    likelihood : str, default "Not Evaluated"
    likelihood_event_occurence : str, default "Not Evaluated"
    likelihood_adverse_event : str, default "Not Evaluated"
    impact : str, default "Not Evaluated"
    technical_impact : SecurityProperty, default SecurityProperty()
    business_impact : str, default "Not Evaluated"
    safety_impact : SafetyImpact, default SafetyImpact()
    predispositions : list, default []
    severity : str, default "Not Evaluated"
    pervasiveness : str, default "Not Evaluated"
    risk : str, default "Not Evaluated"
    residual_risk : str, default "Not Evaluated"
    """

    def __init__(
        self,
        affected_components: List[Component] | Component,
        issues: List[Issue] | Issue,
        mitigations: List[Mitigation] | Mitigation = Mitigation("N/A"),
        relevance: str = "Not Evaluated",
        likelihood: str = "Not Evaluated",
        likelihood_event_occurence: str = "Not Evaluated",
        likelihood_adverse_event: str = "Not Evaluated",
        impact: str = "Not Evaluated",
        technical_impact: SecurityProperty = SecurityProperty(),
        business_impact: str = "Not Evaluated",
        safety_impact: SafetyImpact = SafetyImpact(),
        predispositions: list = [],
        severity: str = "Not Evaluated",
        pervasiveness: str = "Not Evaluated",
        risk: str = "Not Evaluated",
        residual_risk: str = "Not Evaluated",
    ) -> None:
        self.affected_components = affected_components
        self.issues = issues
        self.mitigations = mitigations
        self.relevance = relevance
        self.predispositions = predispositions
        self.severity = severity
        self.pervasiveness = pervasiveness
        self.risk = risk
        self.residual_risk = residual_risk
        self.__impact = {
            "overall": impact,
            "technical": technical_impact,
            "business": business_impact,
            "safety": safety_impact,
        }
        self.__likelihood = {
            "event_occurence": likelihood_event_occurence,
            "adverse_event": likelihood_adverse_event,
            "overall": likelihood,
        }
        pass

    @property
    def impact(self) -> dict:
        return self.__impact

    @impact.setter
    def impact(self, **kwargs):
        for kwarg, val in kwargs.items():
            if kwarg in SecurityProperty.__properties__():
                setattr(self.__impact["technical"], kwarg, val)
            elif kwarg == "business":
                self.__impact["business"] = val
            elif kwarg == "overall":
                self.__impact["overall"] = val
            elif kwarg == "safety":
                raise AttributeError("Please use the safety_impact property.")
            else:
                err = f"{kwarg} is not a valid impact choice."
                raise AttributeError(err)

    @property
    def safety_impact(self) -> SafetyImpact:
        return self.__impact["safety_impact"]

    @safety_impact.setter
    def safety_impact(self, new: SafetyImpact = None, **kwargs) -> None:
        if new != None:
            self.__impact["safety_impact"] = new
        else:
            for kwarg, val in kwargs.items():
                setattr(self.__impact["safety_impact"], kwarg, val)

    @property
    def likelihood(self) -> dict:
        return self.__impact

    @likelihood.setter
    def likelihood(self, **kwargs):
        for kwarg, val in kwargs.items():
            keys = self.__likelihood.keys()
            if kwarg not in keys:
                err = f"{kwarg} not a valid likelihood key. Must be {[keys]}"
                raise ValueError(err)
            self.__likelihood[kwarg] = val
