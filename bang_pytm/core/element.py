import inspect
import random
import uuid
import logging

from hashlib import sha224

from .aux import Classification, TLSVersion
from .controls import Controls
from .tm import TM
from .var import (
    var,
    varString,
    varBoundary,
    varBool,
    varClassification,
    varControls,
    varInts,
    varTLSVersion,
    varFindings,
    varStrings,
    varInt,
)


logger = logging.getLogger(__name__)


class Element:
    """A generic element"""

    name = varString("", required=True)
    description = varString("")
    inBoundary = varBoundary(None, doc="Trust boundary this element exists in")
    inScope = varBool(True, doc="Is the element in scope of the threat model")
    maxClassification = varClassification(
        Classification.UNKNOWN,
        required=False,
        doc="Maximum data classification this element can handle.",
    )
    minTLSVersion = varTLSVersion(
        TLSVersion.NONE,
        required=False,
        doc="""Minimum TLS version required.""",
    )
    findings = varFindings([], doc="Threats that apply to this element")
    overrides = varFindings(
        [],
        doc="""Overrides to findings, allowing to set
a custom response, CVSS score or override other attributes.""",
    )
    levels = varInts(
        {0}, doc="List of levels (0, 1, 2, ...) to be drawn in the model."
    )
    sourceFiles = varStrings(
        [],
        required=False,
        doc="Location of the source code that describes this element relative to the directory of the model script.",
    )
    controls = varControls(None)

    def __init__(self, name, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.name = name
        self.controls = Controls()
        self.uuid = uuid.UUID(int=random.getrandbits(128))
        self._is_drawn = False
        TM._elements.append(self)

    def __repr__(self):
        return "<{0}.{1}({2}) at {3}>".format(
            self.__module__, type(self).__name__, self.name, hex(id(self))
        )

    def __str__(self):
        return "{0}({1})".format(type(self).__name__, self.name)

    def _uniq_name(self):
        """transform name and uuid into a unique string"""
        h = sha224(str(self.uuid).encode("utf-8")).hexdigest()
        name = "".join(x for x in self.name if x.isalpha())
        return "{0}_{1}_{2}".format(type(self).__name__.lower(), name, h[:10])

    def check(self):
        return True

    def display_name(self):
        return self.name

    def _safeset(self, attr, value):
        try:
            setattr(self, attr, value)
        except ValueError:
            pass

    def oneOf(self, *elements):
        """Is self one of a list of Elements"""
        for element in elements:
            if inspect.isclass(element):
                if isinstance(self, element):
                    return True
            elif self is element:
                return True
        return False

    def crosses(self, *boundaries):
        """Does self (dataflow) cross any of the list of boundaries"""
        if self.source.inBoundary is self.sink.inBoundary:
            return False
        for boundary in boundaries:
            if inspect.isclass(boundary):
                if (
                    (
                        isinstance(self.source.inBoundary, boundary)
                        and not isinstance(self.sink.inBoundary, boundary)
                    )
                    or (
                        not isinstance(self.source.inBoundary, boundary)
                        and isinstance(self.sink.inBoundary, boundary)
                    )
                    or self.source.inBoundary is not self.sink.inBoundary
                ):
                    return True
            elif (
                self.source.inside(boundary) and not self.sink.inside(boundary)
            ) or (
                not self.source.inside(boundary) and self.sink.inside(boundary)
            ):
                return True
        return False

    def enters(self, *boundaries):
        """does self (dataflow) enter into one of the list of boundaries"""
        return self.source.inBoundary is None and self.sink.inside(*boundaries)

    def exits(self, *boundaries):
        """does self (dataflow) exit one of the list of boundaries"""
        return self.source.inside(*boundaries) and self.sink.inBoundary is None

    def inside(self, *boundaries):
        """is self inside of one of the list of boundaries"""
        for boundary in boundaries:
            if inspect.isclass(boundary):
                if isinstance(self.inBoundary, boundary):
                    return True
            elif self.inBoundary is boundary:
                return True
        return False

    def _attr_values(self):
        klass = self.__class__
        result = {}
        for i in dir(klass):
            if i.startswith("_") or callable(getattr(klass, i)):
                continue
            attr = getattr(klass, i, {})
            if isinstance(attr, var):
                value = attr.data.get(self, attr.default)
            else:
                value = getattr(self, i)
            result[i] = value
        return result

    def checkTLSVersion(self, flows):
        return any(f.tlsVersion < self.minTLSVersion for f in flows)


class Asset(Element):
    """An asset with outgoing or incoming dataflows"""

    from .var import varElements, varData

    port = varInt(-1, doc="Default TCP port for incoming data flows")
    protocol = varString(
        "", doc="Default network protocol for incoming data flows"
    )
    data = varData([], doc="pytm.Data object(s) in incoming data flows")
    inputs = varElements([], doc="incoming Dataflows")
    outputs = varElements([], doc="outgoing Dataflows")
    onAWS = varBool(False)
    handlesResources = varBool(False)
    usesEnvironmentVariables = varBool(False)
    OS = varString("")

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        TM._assets.append(self)


class Lambda(Asset):
    """A lambda function running in a Function-as-a-Service (FaaS) environment"""

    onAWS = varBool(True)
    environment = varString("")
    implementsAPI = varBool(False)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Server(Asset):
    """An entity processing data"""

    usesSessionTokens = varBool(False)
    usesCache = varBool(False)
    usesVPN = varBool(False)
    usesXMLParser = varBool(False)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class ExternalEntity(Asset):
    hasPhysicalAccess = varBool(False)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Datastore(Asset):
    """An entity storing data"""

    from .var import varDatastoreType
    from .aux import DatastoreType

    onRDS = varBool(False)
    storesLogData = varBool(False)
    storesPII = varBool(
        False,
        doc="""Personally Identifiable Information
is any information relating to an identifiable person.""",
    )
    storesSensitiveData = varBool(False)
    isSQL = varBool(True)
    isShared = varBool(False)
    hasWriteAccess = varBool(False)
    type = varDatastoreType(
        DatastoreType.UNKNOWN,
        doc="""The  type of Datastore, values may be one of:
* UNKNOWN - unknown applicable
* FILE_SYSTEM - files on a file system
* SQL - A SQL Database
* LDAP - An LDAP Server
* AWS_S3 - An S3 Bucket within AWS""",
    )

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Actor(Element):
    """An entity usually initiating actions"""

    from .var import varData, varElements

    port = varInt(-1, doc="Default TCP port for outgoing data flows")
    protocol = varString(
        "", doc="Default network protocol for outgoing data flows"
    )
    data = varData([], doc="pytm.Data object(s) in outgoing data flows")
    inputs = varElements([], doc="incoming Dataflows")
    outputs = varElements([], doc="outgoing Dataflows")
    isAdmin = varBool(False)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        TM._actors.append(self)


class Process(Asset):
    """An entity processing data"""

    codeType = varString("Unmanaged")
    implementsCommunicationProtocol = varBool(False)
    tracksExecutionFlow = varBool(False)
    implementsAPI = varBool(False)
    environment = varString("")
    allowsClientSideScripting = varBool(False)

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class SetOfProcesses(Process):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Dataflow(Element):
    """A data flow from a source to a sink"""

    from .var import varElement, varData

    source = varElement(None, required=True)
    sink = varElement(None, required=True)
    isResponse = varBool(False, doc="Is a response to another data flow")
    response = varElement(
        None, doc="Another data flow that is a response to this one"
    )
    responseTo = varElement(None, doc="Is a response to this data flow")
    srcPort = varInt(-1, doc="Source TCP port")
    dstPort = varInt(-1, doc="Destination TCP port")
    tlsVersion = varTLSVersion(
        TLSVersion.NONE,
        required=True,
        doc="TLS version used.",
    )
    protocol = varString("", doc="Protocol used in this data flow")
    data = varData([], doc="pytm.Data object(s) in incoming data flows")
    order = varInt(-1, doc="Number of this data flow in the threat model")
    implementsCommunicationProtocol = varBool(False)
    note = varString("")
    usesVPN = varBool(False)
    usesSessionTokens = varBool(False)

    def __init__(self, source, sink, name, **kwargs):
        self.source = source
        self.sink = sink
        super().__init__(name, **kwargs)
        TM._flows.append(self)

    def display_name(self):
        if self.order == -1:
            return self.name
        return "({}) {}".format(self.order, self.name)

    def hasDataLeaks(self):
        return any(
            d.classification > self.source.maxClassification
            or d.classification > self.sink.maxClassification
            or d.classification > self.maxClassification
            for d in self.data
        )


class Boundary(Element):
    """Trust boundary groups elements and data with the same trust level."""

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        if name not in TM._boundaries:
            TM._boundaries.append(self)

    def parents(self):
        result = []
        parent = self.inBoundary
        while parent is not None:
            result.append(parent)
            parent = parent.inBoundary
        return result
