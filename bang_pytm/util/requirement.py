from enum import Enum

class StrideToProperty(Enum):
    SPOOFING="AUTHENTICITY"
    TAMPERING="INTEGRITY"
    REPUDIATION="NON_REPUDIATION"
    INFORMATION_DISCLOSURE="CONFIDENTIALITY"
    DENIAL_OF_SERVICE="AVAILABILITY"
    ELEVATION_OF_PRIVILEGE="AUTHORIZATION"

class PropertyToStride(Enum):
    AUTHENTICITY="SPOOFING"
    INTEGRITY="TAMPERING"
    NON_REPUDIATION="REPUDIATION"
    CONFIDENTIALITY="INFORMATION_DISCLOSURE"
    AVAILABILITY="DENIAL_OF_SERVICE"
    AUTHORIZATION="ELEVATION_OF_PRIVILEGE"

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

    __spoofing = False
    __tampering = False
    __repudiation = False
    __information_disclosure = False
    __denial_of_service = False
    __elevation_of_privilege = False

    def __init__(
        self,
        spoofing: bool = False,
        tampering: bool = False,
        repudiation: bool = False,
        information_disclosure: bool = False,
        denial_of_service: bool = False,
        elevation_of_privilege: bool = False,
    ) -> None:
        self.spoofing = spoofing
        self.tampering = tampering
        self.repudiation = repudiation
        self.information_disclosure = information_disclosure
        self.denial_of_service = denial_of_service
        self.elevation_of_privilege = elevation_of_privilege

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

    To Do
    -----
    1. Add forced type checking
    """

    class Property(Enum):
        HIGH = "HIGH"
        LOW = "LOW"
        NONE = "NONE"

    __confidentiality = Property.NONE
    __integrity = Property.NONE
    __availability = Property.NONE
    __authenticity = Property.NONE
    __non_repudiation = Property.NONE
    __authorization = Property.NONE

    def __init__(
        self,
        confidentiality: str = None,
        integrity: str = None,
        availability: str = None,
        authenticity: str = None,
        non_repudiation: str = None,
        authorization: str = None,
    ):
        self.confidentiality = confidentiality
        self.integrity = integrity
        self.availability = availability
        self.authenticity = authenticity
        self.non_repudiation = non_repudiation
        self.authorization = authorization

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
    def confidentiality(self, val: str) -> None:
        if val:
            self.__confidentiality = self.Property[c.upper()]

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
    def integrity(self, i: str) -> None:
        if i:
            self.__integrity = self.Property[i.upper()]
        
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
    def availability(self, a: str) -> None:
        if a:
            self.__availability = self.Property[a.upper()]
        
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
    def authenticity(self, a: str) -> None:
        if a:
            self.__authenticity = self.Property[a.upper()]

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
    def non_repudiation(self, nr: str) -> None:
        if nr:
            self.__non_repudiation = self.Property[nr.upper()]

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
    def authorization(self, a: str) -> None:
        if a:
            self.__authorization = self.Property[a.upper()]
        