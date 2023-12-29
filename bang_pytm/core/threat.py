from .element import Element

from bang_pytm.util.requirement import STRIDE


class Vulnerability(Element):
    """
    A vulnerability is a previously known weakness in a piece of software,
    generally associated with a CVE. This is used in the context of a threat
    model to provide specific examples related to the weaknesses identified in
    the system as well as the related threats.

    Definition
    -----------
    A characteristic or specific weakness that renders an organization or asset
    (such as information or an information system) open to exploitation by a
    given threat or susceptible to a given hazard.

    SOURCE : NICCS CISA
    """

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)


class Weakness(Element):
    """
    A weakness is a potential issue in the design of the system in question.
    The basic attributes of a weakness are based in part on the Common Weakness
    Enumeration List maintained by MITRE.

    Definition
    -----------
    A shortcoming or imperfection in software code, design, architecture, or
    deployment that, under proper conditions, could become a vulnerability or
    contribute to the introduction of vulnerabilities.

    SOURCE : NICCS CISA

    Parameters
    ----------
    name : str
        Name of the weakness, can be a short hand.
    ref_id : str, default None
        Alternative ID to reference, such as CWE-XX.
    desc : str, default None
        A short description of the weakness to help understand it's
        applicability.
    long_desc : str, default None
        A longer descripiton about the weakness
    mode_introduction : list, default None
        What development phase this weakness is introduced. Valid options are:
        `Policy`, `Requirements`, `Architecture and Design`, `Implementation`,
        `Build and Compilation`, `Testing`, `Documentation`, `Bundling`,
        `Distribution`, `Installation`, `System Configuration`, `Operation`,
        `Patching and Maintenance`, `Porting`, `Integration`, `Manufacturing`,
        `Decommissioning and End-of-Life`.

        SOURCE: PhaseEnumeration
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
    exploitable : str, default "Unknown"
        Likelihood of this weakness being exploited. Valid options are: `High`,
        `Medium`, `Low`, `Unknown`.

        SOURCE: LikelihoodEnumeration
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
    consequences : list, default None
        Consequences refers to the potential impact of a weakness. A consequence
        should (although it is not enforced) be a dict that can include the
        following keys: `scope`, `impact`, `likelihood`, `note`. Scope
        identifies the security property that is violated. Impact describes the
        technical impact that arises if an adversary succeeds in exploiting this
        weakness. Likelihood identifies how likely the specific consequence is
        expected to be seen relative to the other consequences. Note provides
        additional commentary about a consequence.

        SOURCE: CommonConsequencesType
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
    relationships : dict, default None
        To Do - Should be removed and instead we use parent/children
    conditions : list, default None
        To Do
    mitigations : list, default None
        To Do
    detection_methods : list, default None
        To Do
    related_cves : list, default None
        To Do
    related_threats : list, default None
        To Do
    references : list, default None
        To Do
    """

    __stride = STRIDE()

    def __init__(
        self,
        name: str,
        ref_id: str = None,
        alt_name: str = None,
        desc: str = None,
        long_desc: str = None,
        mode_introduction: list = None,
        exploitable: str = "Unknown",
        consequences: list = None,
        relationships: list = None,
        conditions: list = None,
        mitigations: list = None,
        detection_methods: list = None,
        related_cves: list = None,
        related_threats: list = None,
        references: list = None,
    ) -> None:
        super().__init__(name, desc)
        self.long_desc = long_desc
        self.ref_id = ref_id
        self.alt_name = alt_name
        self.mode_introduction = mode_introduction
        self.exploitable = exploitable
        self.consequences = consequences
        self.relationships = relationships
        self.conditions = conditions
        self.mitigations = mitigations
        self.detection_methods = detection_methods
        self.related_cves = related_cves
        self.related_threats = related_threats
        self.references = references

    @property
    def stride(self) -> STRIDE:
        """
        Parts of STRIDE that are applicable to this threat. To set the values,
        pass a dictionary {`category`:bool} for the applicable STRIDE categories.
        Valid keys are: `spoofing`, `tampering`, `repudiation`,
        `information_disclosure`, `denial_of_service`, `elevation_of_privilege`.
        See :func:`~bang_pytm.util.STRIDE` for more information.
        """
        return self.__stride

    @stride.setter
    def stride(self, vals: dict) -> None:
        for category, val in vals.items():
            self.__stride.__setattr__(category, val)

    @stride.deleter
    def stride(self) -> None:
        self.__stride = STRIDE()


class Threat(Element):
    """
    A threat is an instance of a weakness (or set of weaknesses) in the system
    that the threat model is for, that has been determined to apply. A threat is
    evaluated both on it's own, such as the potential worst-case severity of the
    threat, as well as in conjunction with the

    Definition
    -----------
    A circumstance or event that has or indicates the potential to exploit
    vulnerabilities and to adversely impact (create adverse consequences for)
    organizational operations, organizational assets (including information and
    information systems), individuals, other organizations, or society.

    SOURCE : NICCS CISA

    Parameters
    ----------
    name : str
        Name of the threat, can be a short hand.
    desc : str, default None
        A short description of the threat to help understand it's
        applicability.
    TO FINISH
    """

    def __init__(
        self,
        name: str,
        ref_id: str = None,
        desc: str = None,
        long_desc: str = None,
        conditions: list = None,
        likelihood: str = "Unknown",
        severity: str = None,
        consequences: list = None,
        required_skills: str = "Unknown",
        required_resources: str = "Unknown",
        mitigations: list = None,
        examples: list = None,
        steps: list = None,
        relationships: list = None,
        related_weaknesses: list = None,
        references: list = None,
    ) -> None:
        super().__init__(name, desc)
        self.long_desc = long_desc
        self.ref_id = ref_id
        self.conditions = conditions
        self.likelihood = likelihood
        self.severity = severity
        self.consequences = consequences
        self.required_skills = required_skills
        self.required_resources = required_resources
        self.mitigations = mitigations
        self.examples = examples
        self.steps = steps
        self.relationships = relationships
        self.related_weaknesses = related_weaknesses
        self.references = references
