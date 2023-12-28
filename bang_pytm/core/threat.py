from .element import Element

from bang_pytm.util.requirement import STRIDE


class Vulnerability(object):
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

    pass


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
    desc : str, default None
        A short description of the weakness to help understand it's
        applicability.


    stride : list, default None

    """

    __long_desc: str = None
    __stride = STRIDE()

    def __init__(
        self,
        name: str,
        ref_id: int = -1,
        alt_name: str = None,
        desc: str = None,
        long_desc: str = None,
        mode_introduction: list = None,
        exploitable: str = None,
        consequences: list = None,
        relationships: dict = None,
        conditions: list = None,
        mitigations: list = None,
        detection_methods: list = None,
        related_cves: list = None,
        related_threats: list = None
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

    @property
    def long_desc(self) -> str:
        return self.__long_desc

    @long_desc.setter
    def long_desc(self, val: str) -> None:
        self.__long_desc = val

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

    """
    def __init__(self, name: str, desc: str = None) -> None:
        super().__init__(name, desc)
        pass
