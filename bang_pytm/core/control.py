from .element import Element

#### Based on the OSCAL stuff, is it appropriate to have this Part class here?
######### How would this work for the init?
##### I guess a better question would be is this a good way to set it up if we
##### are parsing an OSCAL catalog??
class Part:
    __part_id: str = None
    __part_name: str = None
    __part_prose: str = None

    def __init__(self, id: str, prose: str) -> None:
        self.__part_id = id
        self.__part_prose = prose

    @property
    def part_name(self) -> str:
        return self.__part_name
    
    @part_name.setter
    def part_name(self, name: str) -> None:
        names = [
            "objective",
            "statement",
            "guidance",
            "item",
            "information"
        ]
        if name not in names:
            err = f"Part name must be from following: {','.join(names)}."
            raise ValueError(err)
        self.__part_name = name

class Control(Element):

    """
    A control is a safegaurd or countermeasure prescribed for an information
    system or an organization to protect the confidentiality, integrity, and
    availability of the system and its information. In OSCAL, a control is a
    requirement or guideline, which when implemented will reduce an aspect of
    risk related to an information system and its information.

    Source: 'KEY CONCEPTS AND TERMS USED IN OSCAL 
        <https://pages.nist.gov/OSCAL/resources/concepts/terminology/>'
    """

    __id: str = None
    __title: str = None

    # properties have a label and a textual context which defines
    # the property's value
    __prop: dict[str, str] = {}

    # in this case, it must have name statement
    __parts: list[Part] = []
    __assumptions: list = []
    __development_phase: list = []

    def __init__(
            self, 
            id: str,
            title: str,
            description: str
    ):
        self.__id = id
        self.__title = title

        
        self.__description = description
    
    @property
    def parts(self) -> list[Part]:
        return self.__parts

    @parts.setter
    def parts(self, parts: list[Part]) -> None:
        if not isinstance(parts, list):
            raise ValueError("Parts must be provided as a list of Part objects.")
        self.__parts = parts

    def add_part(self, part: Part) -> None:
        self.__parts.append(part)
    
    @property
    def prop(self) -> dict:
        return self.__prop

    @prop.setter
    def prop(self, **kwargs):
        for kwarg, val in kwargs.items():
            self.__likelihood[kwarg] = val    

    @property
    def assumptions(self) -> list:
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
    def development_phase(self) -> str:
        """
        What phase in the development cycle does this control apply to. Valid
        `phase` options are: `Policy`, `Requirements`, `Architecture and Design`
        , `Implementation`, `Build and Compilation`, `Testing`, `Documentation`,
        `Bundling`, `Distribution`, `Installation`, `System Configuration`,
        `Operation`, `Patching and Maintenance`, `Porting`, `Integration`,
        `Manufacturing`, and `Decommissioning and End-of-Life`.

        SOURCE: PhaseEnumeration
        `MITRE CWE <https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd>`
        """
        return self.__development_phase

    @development_phase.setter
    def development_phase(self, phase: str) -> None:
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
        self.__development_phase = phase

    
class ControlCatalog(Element):
    """
    A Control Catalog is a set of controls that are from some standardized set
    of controls. Examples are OWASP ASVS and NIST800-53.

    Source: `OSCAL CATALOG <https://pages.nist.gov/OSCAL/resources/concepts/layer/control/catalog/>`
    """
            
    class Metadata:
        """
        The metadata section of the control catalog contains data about the
        catalog document. This section has identical structure which is used
        consistently across all OSCAL models.

        Source: 'CREATING A CONTROL CATALOG <https://pages.nist.gov/OSCAL/learn/tutorials/control/basic-catalog/>'
        """
        __title: str = None

        # RFC 3339 format for date/time
        __published: str = None
        __last_modified: str = None

        __version: str = None
        __oscal_version: str = None

        def __init__(self,
                     title: str, 
                     published: str, 
                     last_modified: str, 
                     version: str, 
                     oscal_version: str) -> None:
            
            self.__title = title
            self.__published = published
            self.__last_modified = last_modified
            self.__version = version
            self.__oscal_version = version
        
    class Group:
        """
        An OSCAL catalog allows for the organization of related controls
        using groups. A catalog group can represent families of controls
        or other organizational structures, such as sections in a control
        catalog.

        Source: 'CREATING A CONTROL CATALOG <https://pages.nist.gov/OSCAL/learn/tutorials/control/basic-catalog/>'
        """
        __id: str = None
        __title: str = None

        # properties have a label and a textual context which defines
        # the property's value
        ######### how to init this?????
        __prop: dict[str, str] = {}

        # list of other Group objects
        __subgroups: list = []
        __subgroup_part: Part = None
        __controls: list[Control] = None

        def __init__(self, 
                     id: str, 
                     title: str, 
                     subgroups: list, 
                     subgroup_part: Part, 
                     controls: list[Control]) -> None:
            
            self.__id = id
            self.__title = title
            self.__subgroups = subgroups
            self.__subgroup_part = subgroup_part
            self.__controls = controls
                
        @property
        def prop(self) -> dict:
            return self.__prop

        @prop.setter
        def prop(self, **kwargs):
            for kwarg, val in kwargs.items():
                self.__likelihood[kwarg] = val      

    __metadata: Metadata = None
    __groups: list[Group] = []
    __controls: list[Control] = []

    def __init__(self, 
                 metadata: Metadata,
                 groups: list[Group],
                 controls: list[Control]
                 ):
        
        self.__metadata = metadata
        self.__groups = groups
        self.__controls = controls
