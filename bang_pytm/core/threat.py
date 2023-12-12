import sys

from collections.abc import Iterable

from .var import varString


class Threat:
    """Represents a possible threat"""

    id = varString("", required=True)
    description = varString("")
    condition = varString(
        "",
        doc="""a Python expression that should evaluate
to a boolean True or False""",
    )
    details = varString("")
    severity = varString("")
    mitigations = varString("")
    example = varString("")
    references = varString("")
    target = ()

    def __init__(self, **kwargs):
        self.id = kwargs["SID"]
        self.description = kwargs.get("description", "")
        self.condition = kwargs.get("condition", "True")
        target = kwargs.get("target", "Element")
        if not isinstance(target, str) and isinstance(target, Iterable):
            target = tuple(target)
        else:
            target = (target,)
        self.target = tuple(getattr(sys.modules[__name__], x) for x in target)
        self.details = kwargs.get("details", "")
        self.severity = kwargs.get("severity", "")
        self.mitigations = kwargs.get("mitigations", "")
        self.example = kwargs.get("example", "")
        self.references = kwargs.get("references", "")

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
        return "{0}({1})".format(type(self).__name__, self.id)

    def apply(self, target):
        if not isinstance(target, self.target):
            return None
        return eval(self.condition)
