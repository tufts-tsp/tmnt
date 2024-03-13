from .element import Element

from bang_pytm.util.requirement import STRIDE, SecurityProperty, SafetyImpact
from bang_pytm.util.cvss import CVSS
from typing import Union

class Issue(Element):
    """
    Parent of all different types of issues that have a potential negaitve
    impact that should be accounted for in the threat model.

    Parameters
    ----------
    name : str
        Name of the weakness, can be a short hand.
    desc : str, default None
        A short description of the weakness to help understand it's
        applicability.
    prerequisites : list, default None

    mitigations : list, default None

    ref_id : str, default None
        Alternative ID to reference, such as CWE-XX.
    long_desc : str, default None
        A longer descripiton about the weakness
    likelihood : str, default "Unknown"
        Likelihood of this weakness being exploited. Recommended values to
        use: `High`,`Medium`, `Low`, `Unknown`. While the options are not
        validated against a specific list, this was inspired by MITRE's
        Likelihood variable that is part of both CWE and CAPEC (see source
        for details).

        SOURCE: LikelihoodEnumeration
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
    severity : str, default None
        Severity is the typical severity of this type of issue. Recommended
        values to use: `Very High`, `High`,`Medium`, `Low`, `Very Low`.
        While the options are not validated against a specific list, this
        was inspired by MITRE's Severity variable that is part of CAPEC (see
        source for details).

        SOURCE: SeverityEnumeration
        `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`
    related : list, default []
        Related is a catchall for related Issues, which can be Issue objects
        (incl child objects) or strings referencing another schema.
        Recommend using the child/parent parameters of Issue when possible.
    references : list, default []
        References that are useful to look at for this Issue
    consequences : list, default []
        Consequences associated with this issue. If a consequence is added it
        must be a list of dictionaries. The following keys are required: `scope`
        `impact`. And the following are optional: `likelihood` and `note`. See
        :func:`~bang_pytm.core.Issue.consequences` for more information.
    """

    __meta_data: dict = {}
    __cvss: CVSS = CVSS()
    __consequences = []

    def __init__(
        self,
        name: str,
        desc: str = None,
        prerequisites: list = None,
        mitigations: list = None,
        ref_id: str = None,
        long_desc: str = None,
        likelihood: str = "Unknown",
        severity: str = None,
        related: list = [],
        references: list = [],
        consequences: list = [],
    ) -> None:
        super().__init__(name, desc)
        self.prerequisites = prerequisites
        self.mitigations = mitigations
        self.__meta_data = {
            "ref_id": ref_id,
            "long_desc": long_desc,
            "likelihood": likelihood,
            "severity": severity,
            "related": related,
            "references": references,
        }
        for c in consequences:
            like = c["likelihood"] if "likelihood" in c.keys() else None
            note = c["note"] if "impact" in c.keys() else None
            self.add_consequence(c["scope"], c["impact"], like, note)

    @property
    def meta(self) -> dict:
        """
        meta consists of the meta data associated with an Issue. In particular,
        it has the following attributes: `ref_id`, `long_desc`, `likelihood`,
        `severity`, `related`, and `references`.

        Parameters
        ----------
        ref_id : str, default None
            Alternative ID to reference, such as CWE-XX.
        long_desc : str, default None
            A longer descripiton about the weakness
        likelihood : str, default "Unknown"
            Likelihood of this weakness being exploited. Recommended values to
            use: `High`,`Medium`, `Low`, `Unknown`. While the options are not
            validated against a specific list, this was inspired by MITRE's
            Likelihood variable that is part of both CWE and CAPEC (see source
            for details).

            SOURCE: LikelihoodEnumeration
            `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
        severity : str, default None
            Severity is the typical severity of this type of issue. Recommended
            values to use: `Very High`, `High`,`Medium`, `Low`, `Very Low`.
            While the options are not validated against a specific list, this
            was inspired by MITRE's Severity variable that is part of CAPEC (see
            source for details).

            SOURCE: SeverityEnumeration
            `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`
        related : list, default []
            Related is a catchall for related Issues, which can be Issue objects
            (incl child objects) or strings referencing another schema.
            Recommend using the child/parent parameters of Issue when possible.
        references : list, default []
            References that are useful to look at for this Issue.
        """
        return self.__meta_data

    @meta.setter
    def meta(self, **kwargs) -> None:
        for kwarg, val in kwargs.items():
            self.__check_kwarg("meta", kwarg, self.__meta_data.keys())
            if kwarg in ["related", "references"]:
                self.__meta_data[kwarg].append(val)
            else:
                self.__meta_data[kwarg] = val

    @property
    def cvss(self) -> CVSS:
        return self.__cvss

    @cvss.setter
    def cvss(self) -> None:
        # TO DO
        pass

    @property
    def consequences(self) -> list:
        """
        Consquences refers to the potential impact of an issue. A consequence is
        a dict that can include the following keys: `scope`, `impact`,
        `likelihood`, `note`. It is based on the ConsequenceType used in both
        MITRE CAPEC and CWE.

        SOURCE: CommonConsequencesType
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`

        Parameters
        ----------
        scope : str or list
            The scope refers to which aspect of STRIDE applies, i.e. the
            associated threat type for the security property that is violated.
            In this case specifying which parts of STRIDE apply for the
            specified consequence. This assignment will be applied to a
            `bang_pytm.util.STRIDE` object. Valid values are: `spoofing`,
            `tampering`, `repudiation`, `information_disclosure`,
            `denial_of_service`, `elevation_of_privilege`. See
            :func:`~bang_pytm.util.STRIDE` for more information.
        impact : str
            A description of the impact/outcome from this consequence, i.e. when
            the specified STRIDE categories apply. Impact describes the
            technical impact that arises if an adversary succeeds in exploiting
            this issue.
        likelihood : str, default None
            This is the likelihood of this consequence occuring compared to the
            other consequences associated with this issue. If there is only one
            consequence then this should be left as `None`.
        note : str, default None
            Note provides additional commentary about a consequence

        Methods
        -------
        add_consequence
            Add a consequence to the issue, where an user will specify each
            parameter as described above.
        remove_conseqeunce
            Remove a consequence from the issue. This is done by passing the id
            associated with the consequence that is to be removed.

        Note: You cannot edit a consequence, instead you must remove the old one
        and then add the edited version back.
        """
        return self.__consequences

    def add_consequence(
        self,
        scope: Union[str, list],
        impact: str,
        likelihood: str = None,
        note: str = None,
    ) -> None:
        """Adding a consequence to an issue."""
        cid = 1
        if len(self.__consequences) >= 1:
            cid = max([c["id"] for c in self.__consequences]) + 1
        self.__consequences.append(
            {
                "id": cid,
                "scope": scope,
                "impact": impact,
                "likelihood": likelihood,
                "note": note,
            }
        )

    def remove_consequence(self, cid: int) -> None:
        """Removing a consequence from an issue."""
        for i in range(len(self.__consequences)):
            if self.__consequences[i]["id"] == cid:
                del self.__consequences[i]
                break

    def __check_kwarg(self, nm, kwarg, keys) -> None:
        if kwarg not in keys:
            err = f"{nm} must be from the following: {[k for k in keys]}"
            raise AttributeError(err)


class Vulnerability(Issue):
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


class Weakness(Issue):
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
    mode_introduction : list, default None
        What development phase this weakness is introduced. Each value should
        consist of a dictionary with a `phase`, which is required, and a `notes`,
        which is optional to give more context. Valid `phase` options are:
        `Policy`, `Requirements`, `Architecture and Design`, `Implementation`,
        `Build and Compilation`, `Testing`, `Documentation`, `Bundling`,
        `Distribution`, `Installation`, `System Configuration`, `Operation`,
        `Patching and Maintenance`, `Porting`, `Integration`, `Manufacturing`,
        `Decommissioning and End-of-Life`.

        SOURCE: PhaseEnumeration
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
    detection_methods : list, default None
        Detection methods are used to identify methods that may be employed to
        detect this weakness, including their strengths and limitations. Each
        method consists of `desc`, `effectiveness`, and `notes`. The required
        `desc` is intended to provide some context of how this method can be
        applied to a specific weakness. The optional `effectiveness` explains
        how effective the detection method may be in detecting the associated
        weakness. This assumes the use of best-of-breed tools, analysts, and
        methods. There is limited consideration for financial costs, labor, or
        time. The optional `notes` provides additional discussion of the
        strengths and shortcomings of this detection method.

        Source: DetectionMethodsType
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
    **kwargs
        See :func:`~bang_pytm.core.Issue`.
    """

    __mode_introduction: list = []
    __detection_methods: list = []

    def __init__(
        self,
        name: str,
        alt_name: str = None,
        desc: str = None,
        mode_introduction: list = None,
        detection_methods: list = None,
        **kwargs,
    ) -> None:
        super().__init__(name, desc, **kwargs)
        self.alt_name = alt_name
        self.__mode_introduction = mode_introduction
        self.__detection_methods = detection_methods

    @property
    def modes_of_introduction(self) -> list:
        return self.__mode_introduction

    @modes_of_introduction.setter
    def modes_of_introduction(self, modes) -> None:
        for m in modes:
            notes = m["note"] if "notes" in m.keys() else None
            self.add_introduction(m["phase"], notes)

    def add_introduction(self, phase: str, notes: str = None) -> None:
        phases = [
            "Policy",
            "Requirements",
            "Architecture and Design",
            "Implementation",
            "Build and Compilation",
            "Testing",
            "Documentation",
            "Bundling",
            "Distribution",
            "Installation",
            "System Configuration",
            "Operation",
            "Patching and Maintenance",
            "Porting",
            "Integration",
            "Manufacturing",
            "Decommissioning and End-of-Life",
        ]
        if phase not in phases:
            err = f"Phase must be from following: {','.join(phases)}."
            raise ValueError(err)
        self.__mode_introduction.append({"phase": phase, "notes": notes})

    @property
    def detection_methods(self) -> list:
        return self.__detection_methods

    @detection_methods.setter
    def detection_methods(self, methods) -> None:
        for m in methods:
            self.add_detection_method(m["desc"], m["effectivess"], m["notes"])

    def add_detection_method(
        self, desc: str, effectiveness: str = None, notes: str = None
    ) -> None:
        self.__detection_methods.append(
            {"desc": desc, "effectiveness": effectiveness, "notes": notes}
        )


class Threat(Issue):
    """
    A threat is an instance of a weakness (or set of weaknesses) in the system
    that the threat model is for, that has been determined to apply. A threat is
    evaluated on it's own, such as the potential worst-case severity of the
    threat.

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
    examples : list, default None
        Any examples of this threat.
    threat_source_desc : str, default None
        A description about the threat source, for example `APT` or
        `Insider Threat` that provides some information about who the threat
        could be from. NIST 800-30 provides detailed examples of threat sources
        that can be used in Appendix D.
    required_skills : str, default "Unknown"
        The level of skills or specific knowledge needed by an adversary to
        execute this type of attack. Options are: `High`, `Medium`, `Low`, and
        `Unknown`.

        Source: SkillLevelEnumeration
        `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`
    required_resources : str, default "Unknown"
        The resources (e.g., CPU cycles, IP addresses, tools) required by an
        adversary to effectively execute this type of attack.

        Source: RequiredResourcesType
        `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`
    avenue : str, default "Unknown
        The avenue is the area or place from which an attack must occur. Each
        separate avenue represents varying levels of implied trust and attack
        surface. Options are: `Remote`, `Limited Remote`, `Local`, `Physical`.
        More information on these options, as well as additional options can be
        found in See :func:`~bang_pytm.core.Threat.threat_source`.

        Source: NIST Vulnerability Data Ontology
    attack_steps : list, default []
        List of steps associated with the threat, this generally only applies to
        attack patterns, such as those given in MITRE CAPEC.
    **kwargs
        See :func:`~bang_pytm.core.Issue`.
    """

    __threat_source: dict = {}
    __atack_steps: list = []

    def __init__(
        self,
        name: str,
        desc: str = None,
        examples: list = None,
        threat_source_desc: str = None,
        required_skills: str = "Unknown",
        required_resources: str = "Unknown",
        avenue: str = "Unknown",
        attack_steps: list = [],
        **kwargs,
    ) -> None:
        super().__init__(name, desc, **kwargs)
        self.__threat_source = {
            "desc": threat_source_desc,
            "required_skills": required_skills,
            "required_resources": required_resources,
            "avenue": avenue,
        }
        self.examples = examples
        self.attack_steps = attack_steps

    @property
    def threat_source(self) -> dict:
        """
        A description of the threat source as well as the required resources,
        skills, and how the attack surface can be accessed.

        Parameters
        ----------
        desc : str, default None
            A description about the threat source, for example `APT` or
            `Insider Threat` that provides some information about who the threat
            could be from.
        required_skills : str, default "Unknown"
            The level of skills or specific knowledge needed by an adversary to
            execute this type of attack. Options are: `High`, `Medium`, `Low`,
            and `Unknown`.

            Source: SkillLevelEnumeration
            `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`
        required_resources : str, default "Unknown"
            The resources (e.g., CPU cycles, IP addresses, tools) required by an
            adversary to effectively execute this type of attack.

            Source: RequiredResourcesType
            `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`
        avenue : str, default "Unknown
            The avenue is the area or place from which an attack must occur.
            Each separate avenue represents varying levels of implied trust and
            attack surface.

            Options
            -------
            `Remote`
                The exploit scenario requires that the attack occurs over
                the network stack; normally external to the target's internal
                network such as from the Internet. Common targets in the remote
                theater are public websites, Domain Name System (DNS) services,
                or web-browsers.
            `Remote:Internet`
                An attack is able to originate over the internet.
            `Remote:Intranet`
                The attack must be launched from within an organizations
                internal network that is shielded from direct access of the
                Internet. (Ex: A router is configured by default to only allow
                connections from the Intranet ports and not the WAN ports.) This
                also represents broadcast domains.
            `Remote:Local network`
                An attacker must have access to a physical interface to the
                network, or collision domain.
            `Limited Remote`
                The exploit scenario requires that the attack can occur over
                layer 2 or layer 3 technologies, but a limitation exists either
                by the nature of the network communication or by range
                constraints.
            `Limited Remote:Bluetooth`
                The attack must be launched relying on a Bluetooth communication
                channel.
            `Limited Remote:Cellular`
                The attack must be launched from a cellular network.
            `Limited Remote:Infrared`
                The attack must be launched relying on an Infrared communication
                channel.
            `Limited Remote:Line of Sight`
                The attack must be launched using a Line-of-Sight system such as
                ocular.
            `Limited Remote:Satellite`
                The attack must be launched using Satellite communication
                channels.
            `Limited Remote:Wireless`
                The attack must be launched from a wireless (802.11x) network.
            `Local`
                The exploit scenario requires that the attack can only occur
                after the adversary has logical local access to a device such as
                through a console, Remote Desktop Protocol (RDP), Secure Shell
                (SSH), or Telnet login.
            `Physical`
                The exploit scenario requires the attacker's physical presence
                at the target.

        Source: NIST Vulnerability Data Ontology
        """
        return self.__threat_source

    @threat_source.setter
    def threat_source(self, **kwargs) -> None:
        for kwarg, val in kwargs.items():
            self.__check_kwarg(
                "threat_source", kwarg, self.__threat_source.keys()
            )
            self.__threat_source[kwarg] = val

    @property
    def attack_steps(self) -> list:
        """
        Attack steps provides a detailed step by step flow of a threat,
        specifically an attack pattern. It lists the steps typically performed
        by an adversary when leveraging the given technique. This is only
        applicable to attack patterns (a specific class of threats) with an
        abstraction level of detailed.

        Source: ExecutionFlowType
        `MITRE CAPEC <https://capec.mitre.org/data/xsd/ap_schema_latest.xsd>`

        Step
        ----
        A step consists of the following:

        order : int
            Where in the order this step occurs. This should be unique among the
            various steps, i.e. step 1, step 2, step 3...step n.
        phase : str
            What phase within the attack this step occurs. Options are:
            `Explore`, `Experiment`, `Exploit`.
        desc : str
            A short description about this threat
        technique : str
            The techniques involved with this step.
        """
        return self.__atack_steps

    @attack_steps.setter
    def attack_steps(self, steps: list) -> None:
        for step in steps:
            self.add_step(
                step["order"], step["phase"], step["desc"], step["technique"]
            )

    def add_step(
        self, order: int, phase: str, desc: str = None, technique: str = None
    ) -> None:
        """
        Add a step to the attack steps. If a step already exists, identified by
        the order, then the old one will be replaced with the new one.

        Parameters
        ----------
        order : int (required)
            Where in the order this step occurs. This should be unique among the
            various steps, i.e. step 1, step 2, step 3...step n.
        phase : str (required)
            What phase within the attack this step occurs. Options are:
            `Explore`, `Experiment`, `Exploit`.
        desc : str, default None
            A short description about this threat
        technique : str, default None
            The techniques involved with this step.
        """
        self.remove_step(order)
        self.__atack_steps.append(
            {
                "order": order,
                "phase": phase,
                "desc": desc,
                "technique": technique,
            }
        )

    def remove_step(self, order: int) -> None:
        for i in range(len(self.__atack_steps)):
            if self.__atack_steps[i]["order"] == order:
                del self.__atack_steps[i]
