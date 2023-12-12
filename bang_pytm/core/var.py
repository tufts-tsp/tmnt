import logging
import sys

from weakref import WeakKeyDictionary
from collections.abc import Iterable

logger = logging.getLogger(__name__)


class var(object):
    """A descriptor that allows setting a value only once"""

    def __init__(self, default, required=False, doc="", onSet=None):
        self.default = default
        self.required = required
        self.doc = doc
        self.data = WeakKeyDictionary()
        self.onSet = onSet

    def __get__(self, instance, owner):
        # when x.d is called we get here
        # instance = x
        # owner = type(x)
        if instance is None:
            return self
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        # called when x.d = val
        # instance = x
        # value = val
        if instance in self.data:
            raise ValueError(
                "cannot overwrite {}.{} value with {}, already set to {}".format(
                    instance,
                    self.__class__.__name__,
                    value,
                    self.data[instance],
                )
            )
        self.data[instance] = value
        if self.onSet is not None:
            self.onSet(instance, value)


class varString(var):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(
                "expecting a String value, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varStrings(var):
    def __set__(self, instance, value):
        if not isinstance(value, Iterable) or isinstance(value, str):
            value = [value]
        for i, e in enumerate(value):
            if not isinstance(e, str):
                raise ValueError(
                    f"expecting a list of str, item number {i} is a {type(e)}"
                )
        super().__set__(instance, set(value))


class varBoundary(var):
    def __set__(self, instance, value):
        from .element import Boundary  # TO DO

        if not isinstance(value, Boundary):
            raise ValueError(
                "expecting a Boundary value, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varBool(var):
    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError(
                "expecting a boolean value, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varInt(var):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(
                "expecting an integer value, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varInts(var):
    def __set__(self, instance, value):
        if not isinstance(value, Iterable):
            value = [value]
        for i, e in enumerate(value):
            if not isinstance(e, int):
                raise ValueError(
                    f"expecting a list of int, item number {i} is a {type(e)}"
                )
        super().__set__(instance, set(value))


class varElement(var):
    def __set__(self, instance, value):
        from .element import Element  # TO DO

        if not isinstance(value, Element):
            raise ValueError(
                "expecting an Element (or inherited) "
                "value, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varElements(var):
    def __set__(self, instance, value):
        from .element import Element  # TO DO

        for i, e in enumerate(value):
            if not isinstance(e, Element):
                raise ValueError(
                    "expecting a list of Elements, item number {} is a {}".format(
                        i, type(e)
                    )
                )
        super().__set__(instance, list(value))


class varFindings(var):
    def __set__(self, instance, value):
        from .finding import Finding  # TO DO

        for i, e in enumerate(value):
            if not isinstance(e, Finding):
                raise ValueError(
                    "expecting a list of Findings, item number {} is a {}".format(
                        i, type(e)
                    )
                )
        super().__set__(instance, list(value))


class varAction(var):
    def __set__(self, instance, value):
        from .aux import Action

        if not isinstance(value, Action):
            raise ValueError(
                "expecting an Action, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varClassification(var):
    def __set__(self, instance, value):
        from .aux import Classification

        if not isinstance(value, Classification):
            raise ValueError(
                "expecting a Classification, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varLifetime(var):
    def __set__(self, instance, value):
        from .aux import Lifetime

        if not isinstance(value, Lifetime):
            raise ValueError(
                "expecting a Lifetime, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varDatastoreType(var):
    def __set__(self, instance, value):
        from .aux import DatastoreType

        if not isinstance(value, DatastoreType):
            raise ValueError(
                "expecting a DatastoreType, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varTLSVersion(var):
    def __set__(self, instance, value):
        from .aux import TLSVersion

        if not isinstance(value, TLSVersion):
            raise ValueError(
                "expecting a TLSVersion, got a {}".format(type(value))
            )
        super().__set__(instance, value)


class varData(var):
    def __set__(self, instance, value):
        from .data import Data, DataSet  # TO DO
        from .aux import Classification

        if isinstance(value, str):
            value = [
                Data(
                    name="undefined",
                    description=value,
                    classification=Classification.UNKNOWN,
                )
            ]
            sys.stderr.write(
                "FIXME: a dataflow is using a string as the Data attribute. This has been deprecated and Data objects should be created instead.\n"
            )

        if not isinstance(value, Iterable):
            value = [value]
        for i, e in enumerate(value):
            if not isinstance(e, Data):
                raise ValueError(
                    "expecting a list of pytm.Data, item number {} is a {}".format(
                        i, type(e)
                    )
                )
        super().__set__(instance, DataSet(value))


class varControls(var):
    def __set__(self, instance, value):
        from .controls import Controls

        if not isinstance(value, Controls):
            raise ValueError(
                "expecting an Controls " "value, got a {}".format(type(value))
            )
        super().__set__(instance, value)
