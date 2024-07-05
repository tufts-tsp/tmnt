from typing import Optional
from .element import Element


class Mitigation(Element):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Part(object):
    """
    needs documentation
    """

    def __init__(self, id: Optional[str] = None, prose: Optional[str] = None) -> None:
        if not isinstance(id, str):
            raise ValueError("Part ID must be a string")
        self.__part_id = id

        if not isinstance(prose, str):
            raise ValueError("Part Prose must be a string")
        self.__part_prose = prose

        self.__part_name = None

    @property
    def part_id(self) -> str:
        return self.__part_id

    @property
    def part_prose(self) -> str:
        return self.__part_prose

    @property
    def part_name(self) -> str:
        return self.__part_name

    @part_name.setter
    def part_name(self, name: str) -> None:
        names = ["objective", "statement", "guidance", "item", "information"]
        if name not in names:
            err = f"Part name must be from following: {','.join(names)}."
            raise ValueError(err)
        self.__part_name = name


class Control(Mitigation):

    """
    A control is a safegaurd or countermeasure prescribed for an information
    system or an organization to protect the confidentiality, integrity, and
    availability of the system and its information. In OSCAL, a control is a
    requirement or guideline, which when implemented will reduce an aspect of
    risk related to an information system and its information.

    Source: 'KEY CONCEPTS AND TERMS USED IN OSCAL
        <https://pages.nist.gov/OSCAL/resources/concepts/terminology/>'
    """

    def __init__(
        self, cid: str, name: str, desc: Optional[str] = None, related: list = []
    ):
        if not isinstance(cid, str):
            raise ValueError("Control ID must be a string")
        self.__cid = cid
        self.__related = related
        super().__init__(name=name, desc=desc)

    @property
    def cid(self) -> str:
        return self.__cid

    @property
    def parts(self) -> list[Part]:
        return self.__parts

    @parts.setter
    def parts(self, parts: list[Part]) -> None:
        if not isinstance(parts, list):
            raise ValueError(
                "Parts must be provided as a list of Part objects."
            )
        self.__parts = parts

    def add_part(self, part: Part) -> None:
        self.__parts.append(part)

    @property
    def prop(self) -> dict:
        return self.__prop

    @prop.setter
    def prop(self, **kwargs):
        for kwarg, val in kwargs.items():
            label = kwarg
            context = val
            if not isinstance(label, str) and not isinstance(context, str):
                raise ValueError("Property label and context must be strings")
            self.__prop[label] = context

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
    def related(self):
        return self.__related


class Metadata:
    """
    The metadata section of the control catalog contains data about the
    catalog document. This section has identical structure which is used
    consistently across all OSCAL models.

    Source: 'CREATING A CONTROL CATALOG <https://pages.nist.gov/OSCAL/learn/tutorials/control/basic-catalog/>'
    """

    def __init__(
        self,
        title: str,
        published: str,
        last_modified: str,
        version: str,
        oscal_version: str,
    ) -> None:
        if not isinstance(title, str):
            raise ValueError("Metadata title must be a string")
        self.__title = title

        if not isinstance(published, str):
            raise ValueError("Metadata publish date must be a string")
        self.__published = published

        if not isinstance(last_modified, str):
            raise ValueError("Metadata last modified date must be a string")
        self.__last_modified = last_modified

        if not isinstance(version, str):
            raise ValueError("Metadata version must be a string")
        self.__version = version

        if not isinstance(oscal_version, str):
            raise ValueError("Metadata OSCAL version must be a string")
        self.__oscal_version = oscal_version

    @property
    def title(self) -> str:
        return self.__title

    @property
    def published(self) -> str:
        return self.__published

    @property
    def last_modified(self) -> str:
        return self.__last_modified

    @property
    def version(self) -> str:
        return self.__version

    @property
    def oscal_version(self) -> str:
        return self.__oscal_version


class Group:
    """
    An OSCAL catalog allows for the organization of related controls
    using groups. A catalog group can represent families of controls
    or other organizational structures, such as sections in a control
    catalog.

    Source: 'CREATING A CONTROL CATALOG <https://pages.nist.gov/OSCAL/learn/tutorials/control/basic-catalog/>'
    """

    def __init__(
        self,
        id: str,
        title: str,
        subgroups: list["Group"],
        controls: list[Control],
    ) -> None:
        if not isinstance(id, str):
            raise ValueError("Group ID must be a string")
        self.__id = id

        if not isinstance(title, str):
            raise ValueError("Group title must be a string")
        self.__title = title

        if not isinstance(subgroups, list) or not all(
            isinstance(subgroup, Group) for subgroup in subgroups
        ):
            if isinstance(subgroups, Group):
                self.__subgroups = [subgroups]
            else:
                raise ValueError("Subgroups must be a list of Group objects")
        self.__subgroups = subgroups

        if not isinstance(controls, list) or not all(
            isinstance(control, Control) for control in controls
        ):
            if isinstance(controls, Control):
                self.__controls = [controls]
            else:
                raise ValueError("Controls must be a list of Control Objects")
        self.__controls = controls

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def subgroups(self) -> list:
        return self.__subgroups

    @property
    def controls(self) -> list[Control]:
        return self.__controls

    @property
    def parts(self) -> list[Part]:
        return self.__parts

    @parts.setter
    def parts(self, parts: list[Part]) -> None:
        if not isinstance(parts, list) or not all(
            isinstance(part, Part) for part in parts
        ):
            if isinstance(parts, Group):
                self.__parts = [parts]
            else:
                raise ValueError("Parts must be a list of Part objects")
        self.__parts = parts

    def add_part(self, part: Part) -> None:
        if not isinstance(part, Part):
            raise ValueError("Part must be a Part object")
        self.__parts.append(part)

    @property
    def prop(self) -> dict:
        return self.__prop

    @prop.setter
    def prop(self, **kwargs):
        for kwarg, val in kwargs.items():
            label = kwarg
            context = val
            if not isinstance(label, str) and not isinstance(context, str):
                raise ValueError("Property label and context must be strings")
            self.__prop[label] = context


class ControlCatalog(Element):
    """
    A Control Catalog is a set of controls that are from some standardized set
    of controls. Examples are OWASP ASVS and NIST800-53.

    Source: `OSCAL CATALOG <https://pages.nist.gov/OSCAL/resources/concepts/layer/control/catalog/>`
    """

    def __init__(
        self, metadata: Metadata, groups: list[Group], controls: list[Control]
    ):
        if not isinstance(metadata, Metadata):
            raise ValueError("Metadata must be a Metadata object")
        self.__metadata = metadata

        if not isinstance(groups, list) or not all(
            isinstance(group, Group) for group in groups
        ):
            if isinstance(groups, Group):
                self.__groups = [groups]
            else:
                raise ValueError("Controls must be a list of Control Objects")
        self.__groups = groups

        if not isinstance(controls, list) or not all(
            isinstance(control, Control) for control in controls
        ):
            if isinstance(controls, Control):
                self.__controls = [controls]
            else:
                raise ValueError("Controls must be a list of Control Objects")
        self.__controls = controls

    @property
    def metadata(self) -> Metadata:
        return self.__metadata

    @property
    def groups(self) -> list[Group]:
        return self.__groups

    @property
    def controls(self) -> list[Control]:
        return self.__controls

    @groups.setter
    def groups(self, group: Group):
        if not isinstance(group, Group):
            raise ValueError("Group must be a Group object")
        self.__groups.append(group)
