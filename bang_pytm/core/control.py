from .element import Element


class Control(Element):

    __id: str = None
    __title: str = None
    __desc: str = None
    __assumptions: list = []
    __development_phase: list = []
    __related: list = []

    def __init__(
            self, 
            id: str,
            title: str,
            desc: str=None,
            related: list=[]
    ):
        self.__id = id
        self.__title = title
        self.__desc = desc
        self.__related = related

    @property
    def id(self) -> str:
        """ID of the Control"""
        return self.__id

    @id.setter
    def id(self, val: str) -> None:
        self.__id = val

    @property
    def title(self) -> str:
        """Title of the Control"""
        return self.__title

    @title.setter
    def title(self, val: str) -> None:
        self.__title = val

    @property
    def desc(self) -> str:
        """Description of the Control"""
        return self.__desc

    @desc.setter
    def desc(self, val: str) -> None:
        self.__desc = val

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

    @property
    def related(self) -> list:
        """Issues related to the Control"""
        return self.__related

    @related.setter
    def related(self, val: list) -> None:
        self.__related = val

class ControlCatalog(Element):
    """
    A Control Catalog is a set of controls that are from some standardized set
    of controls. Examples are OWASP ASVS and NIST800-53.

    Source: `OSCAL CATALOG <https://pages.nist.gov/OSCAL/resources/concepts/layer/control/catalog/>`
    """

    def __init__(self):
        pass
