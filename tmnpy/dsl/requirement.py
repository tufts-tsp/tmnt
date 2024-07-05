"""
Requirements and other properties relevant for threat modeling.

StrideToProperty : Mapping of STRIDE category to Security Property

PropertyToStride : Mapping of Security Property to STRIDE category

STRIDE : Specify which parts of STRIDE apply to a threat

SecurityProperty : Specify what security properties are relevant

SafetyRequirement : Specify the severity of harm that is possible
"""

from enum import Enum, IntEnum


class StrideToProperty(Enum):
    SPOOFING = "AUTHENTICITY"
    TAMPERING = "INTEGRITY"
    REPUDIATION = "NON_REPUDIATION"
    INFORMATION_DISCLOSURE = "CONFIDENTIALITY"
    DENIAL_OF_SERVICE = "AVAILABILITY"
    ELEVATION_OF_PRIVILEGE = "AUTHORIZATION"


class PropertyToStride(Enum):
    AUTHENTICITY = "SPOOFING"
    INTEGRITY = "TAMPERING"
    NON_REPUDIATION = "REPUDIATION"
    CONFIDENTIALITY = "INFORMATION_DISCLOSURE"
    AVAILABILITY = "DENIAL_OF_SERVICE"
    AUTHORIZATION = "ELEVATION_OF_PRIVILEGE"


class STRIDE(object):
    """
    A STRIDE object is assigned to a threat, whereby the user determines, which
    aspects of STRIDE apply to this particular threat.

    STRIDE has a 1-1 match with SecurityProperty. See each property for more
    information.

    Parameters
    ----------
    spoofing : bool, default False
        If Spoofing applies
    tampering : bool, default False
        If Tampering applies
    repudiation : bool, default False
        If Repudiation applies
    information_disclosure : bool, default False
        If Information Disclosure applies
    denial_of_service : bool, default False
        If Denial of Service applies
    elevation_of_privilege : bool, default False
        If Elevation of Privilege applies
    """

    def __init__(
        self,
        spoofing: bool = False,
        tampering: bool = False,
        repudiation: bool = False,
        information_disclosure: bool = False,
        denial_of_service: bool = False,
        elevation_of_privilege: bool = False,
    ) -> None:
        self.__spoofing = spoofing
        self.__tampering = tampering
        self.__repudiation = repudiation
        self.__information_disclosure = information_disclosure
        self.__denial_of_service = denial_of_service
        self.__elevation_of_privilege = elevation_of_privilege
        self.__information = None

    @property
    def spoofing(self) -> bool:
        """
        Spoofing requirement. Maps to
        :func:`~bang_pytm.util.requirement.SecurityProperty.authenticity`

        Definition
        ----------
        Breaching the user's authentication information. In this case, the
        hacker has obtained the user's personal information or something that
        enables him to replay the authentication procedure. Spoofing threats are
        associated with a wily hacker being able to impersonate a valid system
        user or resource to get access to the system and thereby compromise
        system security.

        SOURCE: Loren Kohnfelder and Praerit Garg. The threats to our products.
        Microsoft. April 1999.
        """
        return self.__spoofing

    @spoofing.setter
    def spoofing(self, val: bool) -> None:
        self.__spoofing = val

    @property
    def tampering(self) -> bool:
        """
        Tampering threat. Maps to
        :func:`~bang_pytm.util.requirement.SecurityProperty.integrity`

        Definition
        ----------
        Modifying system or user data with or without detection. An unauthorized
        change to stored or in-transit information, formatting of a hard disk, a
        malicious intruder introducing an undetectable network packet in a
        communication, and making an undetectable change to a sensitive file are
        all tampering threats.

        SOURCE: Loren Kohnfelder and Praerit Garg. The threats to our products.
        Microsoft. April 1999.
        """
        return self.__tampering

    @tampering.setter
    def tampering(self, val: bool) -> None:
        self.__tampering = val

    @property
    def repudiation(self) -> bool:
        """
        Repudiation threat. Maps to
        :func:`~bang_pytm.util.requirement.SecurityProperty.non_repudiation`

        Definition
        ----------
        An untrusted user performing an illegal operation without the ability to
        be traced. Repudiability threats are associated with users (malicious or
        otherwise) who can deny a wrongdoing without any way to prove otherwise.

        SOURCE: Loren Kohnfelder and Praerit Garg. The threats to our products.
        Microsoft. April 1999.
        """
        return self.__repudiation

    @repudiation.setter
    def repudiation(self, val: bool) -> None:
        self.__repudiation = val

    @property
    def information_disclosure(self) -> bool:
        """
        Information Disclosure threat. Maps to
        :func:`~bang_pytm.util.requirement.SecurityProperty.confidentiality`

        Definition
        ----------
        Compromising the user's private or business-critical information.
        Information disclosure threats expose information to individuals who are
        not supposed to see it. A user's ability to read a file that she or he
        was not granted access to, as well as an intruder's ability to read the
        data while in transit between two computers, are both disclosure
        threats. Note that this threat differs from a spoofing threat in that
        here the perpetrator gets access to the information directly rather than
        by having to spoof a legitimate user.

        SOURCE: Loren Kohnfelder and Praerit Garg. The threats to our products.
        Microsoft. April 1999.
        """
        return self.__information_disclosure

    @information_disclosure.setter
    def information_disclosure(self, val: bool) -> None:
        self.__information_disclosure = val

    @property
    def denial_of_service(self) -> bool:
        """
        Denial of Service threat. Maps to
        :func:`~bang_pytm.util.requirement.SecurityProperty.availability`

        Definition
        ----------
        Making the system temporarily unavailable or unusable, such as those
        attacks that could force a reboot or restart of the user's machine. When
        an attacker can temporarily make the system resources (processing time,
        storage, etc.) unavailable or unusable, we have a denial of service
        threat. We must protect against certain types of D.o.S. threats for
        improved system availability and reliability. However, some types of
        D.o.S. threats are very hard to protect against, so at a minimum, we
        must identify and rationalize such threats.

        SOURCE: Loren Kohnfelder and Praerit Garg. The threats to our products.
        Microsoft. April 1999.
        """
        return self.__denial_of_service

    @denial_of_service.setter
    def denial_of_service(self, val: bool) -> None:
        self.__denial_of_service = val

    @property
    def elevation_of_privilege(self) -> bool:
        """
        Elevation of Privilege threat. Maps to
        :func:`~bang_pytm.util.requirement.SecurityProperty.authorization`

        Definition
        ----------
        An unprivileged user gains privileged access and thereby has sufficient
        access to completely compromise or destroy the entire system. The more
        dangerous aspect of such threats is compromising the system in
        undetectable ways whereby the user is able to take advantage of the
        privileges without the knowledge of system administrators. Elevation of
        privilege threats include those situations where an attacker is allowed
        more privilege than should properly be granted, completely compromising
        the security of the entire system and causing extreme system damage.
        Here the attacker has effectively penetrated all system defenses and
        become part of the trusted system itself and can do anything.

        SOURCE: Loren Kohnfelder and Praerit Garg. The threats to our products.
        Microsoft. April 1999.
        """
        return self.__elevation_of_privilege

    @elevation_of_privilege.setter
    def elevation_of_privilege(self, val: bool) -> None:
        self.__elevation_of_privilege = val

    @property
    def info(self) -> str:
        return self.__information

    @info.setter
    def info(self, val: str) -> None:
        self.__information = val


class Property(Enum):
    HIGH = "HIGH"
    LOW = "LOW"
    NONE = "NONE"


class SecurityProperty(object):
    """
    Determine what are the security properties associated with an element,
    specifically Confidentiality, Integrity, Availability, Authenticity,
    Non-Repudiation, and Authorization. This helps set prioritization
    of elements in a threat model as well as provides more granularity on
    evaluating threats.

    SecurityProperty has a 1-1 match with STRIDE. See each property for more
    information.

    Parameters
    ----------
    confidentiality : str, default None
        Confidentiality requirement for the element. Valid value are: `NONE`,
        `LOW`, `HIGH`. Case-insensitive.
    integrity : str, default None
        Integrity requirement for the element. Valid value are: `NONE`, `LOW`,
        `HIGH`. Case-insensitive.
    availability : str, default None
        Availability requirement for the element. Valid value are: `NONE`,
        `LOW`, `HIGH`. Case-insensitive.
    authenticity : str, default None
        Authenticity requirement for the element. Valid value are: `NONE`,
        `LOW`, `HIGH`. Case-insensitive.
    non_repudiation : str, default None
        Non-Repudiation requirement for the element. Valid value are: `NONE`,
        `LOW`, `HIGH`. Case-insensitive.
    authorization : str, default None
        Authorization requirement for the element. Valid value are: `NONE`,
        `LOW`, `HIGH`. Case-insensitive.
    """

    def __init__(
        self,
        confidentiality: Property = Property.NONE,
        integrity: Property = Property.NONE,
        availability: Property = Property.NONE,
        authenticity: Property = Property.NONE,
        non_repudiation: Property = Property.NONE,
        authorization: Property = Property.NONE,
    ) -> None:
        self.confidentiality = confidentiality
        self.integrity = integrity
        self.availability = availability
        self.authenticity = authenticity
        self.non_repudiation = non_repudiation
        self.authorization = authorization
        self.information = None

    @classmethod
    def __properties__(cls):
        return [
            k
            for k in vars(cls).keys()
            if k.startswith("_") == False and k != "Property"
        ]

    @property
    def confidentiality(self) -> Property:
        """
        Confidentiality requirement. Maps to
        :func:`~bang_pytm.util.requirement.STRIDE.information_disclosure`

        Definition
        ----------
        A property that information is not disclosed to users, processes, or
        devices unless they have been authorized to access the information.

        SOURCE: NICCS CISA
        """
        return self.__confidentiality

    @confidentiality.setter
    def confidentiality(self, val: str | Property) -> None:
        if isinstance(val, str):
            self.__confidentiality = Property[val.upper()]
        elif isinstance(val, Property):
            self.__confidentiality = val

    @property
    def integrity(self) -> Property:
        """
        Integrity requirement. Maps to
        :func:`~bang_pytm.util.requirement.STRIDE.tampering`

        Definition
        ----------
        The property whereby information, an information system, or a component
        of a system has not been modified or destroyed in an unauthorized
        manner.

        SOURCE: NICCS CISA
        """
        return self.__integrity

    @integrity.setter
    def integrity(self, i: str | Property) -> None:
        if isinstance(i, str):
            self.__integrity = Property[i.upper()]
        elif isinstance(i, Property):
            self.__integrity = i

    @property
    def availability(self) -> Property:
        """
        Availability requirement. Maps to
        :func:`~bang_pytm.util.requirement.STRIDE.denial_of_service`

        Definition
        ----------
        The property of being accessible and usable upon demand.

        SOURCE: NICCS CISA
        """
        return self.__availability

    @availability.setter
    def availability(self, a: str | Property) -> None:
        if isinstance(a, str):
            self.__availability = Property[a.upper()]
        elif isinstance(a, Property):
            self.__availability = a

    @property
    def authenticity(self) -> Property:
        """
        Authenticity requirement. Maps to
        :func:`~bang_pytm.util.requirement.STRIDE.spoofing`

        Definition
        ----------
        A property achieved through cryptographic methods of being genuine and
        being able to be verified and trusted, resulting in confidence in the
        validity of a transmission, information or a message, or sender of
        information or a message.

        SOURCE: NICCS CISA
        """
        return self.__authenticity

    @authenticity.setter
    def authenticity(self, a: str | Property) -> None:
        if isinstance(a, str):
            self.__authenticity = Property[a.upper()]
        elif isinstance(a, Property):
            self.__authenticity = a

    @property
    def non_repudiation(self) -> Property:
        """
        Non-Repudiation requirement. Maps to
        :func:`~bang_pytm.util.requirement.STRIDE.repudiation`

        Definition
        ----------
        A property achieved through cryptographic methods to protect against an
        individual or entity falsely denying having performed a particular
        action related to data.

        SOURCE: NICCS CISA
        """
        return self.__non_repudiation

    @non_repudiation.setter
    def non_repudiation(self, nr: str | Property) -> None:
        if isinstance(nr, str):
            self.__non_repudiation = Property[nr.upper()]
        elif isinstance(nr, Property):
            self.__non_repudiation = nr

    @property
    def authorization(self) -> Property:
        """
        Authorization requirement. Maps to
        :func:`~bang_pytm.util.requirement.STRIDE.elevation_of_privilege`

        Definition
        ----------
        A process of determining, by evaluating applicable access control
        information, whether a subject is allowed to have the specified types of
        access to a particular resource.

        SOURCE: NICCS CISA
        """
        return self.__authorization

    @authorization.setter
    def authorization(self, a: str | Property) -> None:
        if isinstance(a, str):
            self.__authorization = Property[a.upper()]
        elif isinstance(a, Property):
            self.__authorization = a

    @property
    def info(self) -> str:
        return self.__information

    @info.setter
    def info(self, val: str) -> None:
        self.__information = val


class PatientHarm(IntEnum):
    """
    `PatientHarm` is for systems that need to evaluate safety as part of
    the threat model. These are ranked in order of potential severity. For each
    option, you can also see a description of these categories by calling
    `description` for an instance of `PatientHarm`.

    SOURCE: ANSI/AAMI/ISO 14971: 2007/(R)2010: Medical Devices - Application of
    Risk Management to Medical Devices.
    """

    NEGLIGIBLE = 1
    MINOR = 2
    SERIOUS = 3
    CRITICAL = 4
    CATASTROPHIC = 5

    def description(self):
        """A description of the severity of harm"""
        if self.value == 1:
            return """Inconvenience or temporary discomfort"""
        elif self.value == 2:
            return """Results in temporary injury or impairment not requiring
            professional medical intervention"""
        elif self.value == 3:
            return """Results in injury or impairment requiring professional
            medical intervention"""
        elif self.value == 4:
            return """Results in permanent impairment or life-threatening
            injury"""
        elif self.value == 5:
            return """Results in patient death"""
        else:
            raise AttributeError


class SafetyImpact(object):
    def __init__(
        self,
        harm: PatientHarm = PatientHarm.CATASTROPHIC,
        exploitability: str = None,
        **kwargs,
    ) -> None:
        if harm:
            self.__harm = harm
        if exploitability:
            self.__exploitability = exploitability
        self.__meta = {
            "assessed_by": None,
            "assessment_date": None,
            "additional_info": None,
        }  # (**kwargs)
        __risk = False

    @property
    def meta(self) -> dict:
        """
        meta is the meta data for this SafetyImpact analysis.

        Parameters
        ----------
        assessed_by : str
            Who conducted the impact assessment
        assessment_date : str
            When this impact assessment was done
        additional_info : str
            Any other relevant information related to this assessment

        To Do
        -----
        1. Have assessment_date be a dt object (should still accept a string)
        """
        return self.__meta

    @meta.setter
    def meta(
        self,
        assessed_by: str = None,
        assessment_date: str = None,
        additional_info: str = None,
    ) -> None:
        if assessed_by:
            self.__meta["assessed_by"] = assessed_by
        if assessment_date:
            self.__meta["assessment_date"] = assessment_date
        if additional_info:
            self.__meta["additional_info"] = additional_info

    @property
    def harm(self) -> PatientHarm:
        return self.__harm

    @harm.setter
    def harm(self, val: str) -> None:
        self.__harm = getattr(PatientHarm, val.upper())

    @property
    def exploitability(self) -> str:
        return self.__exploitability

    @exploitability.setter
    def exploitability(self, val: str) -> None:
        val = val.upper()
        options = ["HIGH", "MEDIUM", "LOW", "UNKNOWN"]
        if val not in options:
            err = f"""Exploitability must be one of the following:
            {[o for o in options]}"""
            raise AttributeError()
        self.__exploitability = val

    @property
    def controlled_risk(self) -> bool:
        """
        Definition
        ----------
        A key purpose of conducting the cyber-vulnerability risk assessment is
        to evaluate whether the risk of patient harm is controlled (acceptable)
        or uncontrolled (unacceptable). One method of assessing the
        acceptability of risk involves using a matrix with combinations of
        "exploitability" and "severity of patient harm" to determine whether the
        risk of patient harm is controlled or uncontrolled. A manufacturer can
        then conduct assessments of the exploitability and severity of patient
        harm and then use such a matrix to assess the risk of patient harm for
        the identified cybersecurity vulnerabilities.

        For risks that remain uncontrolled, additional remediation should be
        implemented.

        Source: FDA. Postmarket Management of Cybersecurity in Medical Devices.
        2016. pp 17-18.
        """
        ### CONTROLLED RISK AS RECOMMENDED BY FDA GUIDANCE
        if self.exploitability == "LOW" and (
            self.harm == PatientHarm.NEGLIGIBLE
            or self.harm == PatientHarm.MINOR
        ):
            return True
        elif (
            self.exploitability == "MEDIUM"
            and self.harm == PatientHarm.NEGLIGIBLE
        ):
            return True

        ### UNCONTROLLED RISK AS RECOMMENDED BY FDA GUIDANCE
        elif self.exploitability == "HIGH" and (
            self.harm == PatientHarm.CATASTROPHIC
            or self.harm == PatientHarm.CRITICAL
            or self.harm == PatientHarm.SERIOUS
        ):
            return False
        elif self.exploitability == "MEDIUM" and (
            self.harm == PatientHarm.CATASTROPHIC
            or self.harm == PatientHarm.CRITICAL
        ):
            return False
        elif self.exploitability == "LOW" and (
            self.harm == PatientHarm.CATASTROPHIC
        ):
            return False

        ### RECOMMENDATION UNCLEAR FROM FDA GUIDANCE
        else:
            print("Please evaluate the risk.")
            return False

    @controlled_risk.setter
    def controlled_risk(self, val: bool) -> None:
        self.__risk = val
