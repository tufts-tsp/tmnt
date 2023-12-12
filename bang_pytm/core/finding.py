from .var import var, varString, varElement
from .element import Element


class Finding:
    """Represents a Finding - the element in question
    and a description of the finding"""

    element = varElement(
        None, required=True, doc="Element this finding applies to"
    )
    target = varString("", doc="Name of the element this finding applies to")
    description = varString("", required=True, doc="Threat description")
    details = varString("", required=True, doc="Threat details")
    severity = varString("", required=True, doc="Threat severity")
    mitigations = varString("", required=True, doc="Threat mitigations")
    example = varString("", required=True, doc="Threat example")
    id = varString("", required=True, doc="Finding ID")
    threat_id = varString("", required=True, doc="Threat ID")
    references = varString("", required=True, doc="Threat references")
    condition = varString("", required=True, doc="Threat condition")
    response = varString(
        "",
        required=False,
        doc="""Describes how this threat matching this particular asset or dataflow is being handled.
Can be one of:
* mitigated - there were changes made in the modeled system to reduce the probability of this threat ocurring or the impact when it does,
* transferred - users of the system are required to mitigate this threat,
* avoided - this asset or dataflow is removed from the system,
* accepted - no action is taken as the probability and/or impact is very low
""",
    )
    cvss = varString("", required=False, doc="The CVSS score and/or vector")

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        if args:
            element = args[0]
        else:
            element = kwargs.pop("element", Element("invalid"))

        self.target = element.name
        self.element = element
        attrs = [
            "description",
            "details",
            "severity",
            "mitigations",
            "example",
            "references",
            "condition",
        ]
        threat = kwargs.pop("threat", None)
        if threat:
            kwargs["threat_id"] = getattr(threat, "id")
            for a in attrs:
                # copy threat attrs into kwargs to allow to override them in next step
                kwargs[a] = getattr(threat, a)

        threat_id = kwargs.get("threat_id", None)
        for f in element.overrides:
            if f.threat_id != threat_id:
                continue
            for i in dir(f.__class__):
                attr = getattr(f.__class__, i)
                if (
                    i in ("element", "target")
                    or i.startswith("_")
                    or callable(attr)
                    or not isinstance(attr, var)
                ):
                    continue
                if f in attr.data:
                    kwargs[i] = attr.data[f]
            break

        for k, v in kwargs.items():
            setattr(self, k, v)

    def _safeset(self, attr, value):
        try:
            setattr(self, attr, value)
        except ValueError:
            pass

    def __repr__(self):
        return "<{0}.{1}({2}) at {3}>".format(
            self.__module__, type(self).__name__, self.id, hex(id(self))
        )

    def __str__(self):
        return f"'{self.target}': {self.description}\n{self.details}\n{self.severity}"
