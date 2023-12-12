import os
import random
import json
import logging
import html
import copy

from collections import Counter, defaultdict
from itertools import combinations

from .aux import Action
from .var import varString, varBool, varFindings, varAction, varStrings

logger = logging.getLogger(__name__)


class TM:
    """Describes the threat model administratively,
    and holds all details during a run"""

    _flows = []
    _elements = []
    _actors = []
    _assets = []
    _threats = []
    _boundaries = []
    _data = []
    _threatsExcluded = []
    _duplicate_ignored_attrs = (
        "name",
        "note",
        "order",
        "response",
        "responseTo",
        "controls",
    )
    name = varString("", required=True, doc="Model name")
    description = varString("", required=True, doc="Model description")
    threatsFile = varString("",
        onSet=lambda i, v: i._init_threats(),
        doc="JSON file with custom threats",
    )
    isOrdered = varBool(False, doc="Automatically order all Dataflows")
    mergeResponses = varBool(False, doc="Merge response edges in DFDs")
    ignoreUnused = varBool(
        False, doc="Ignore elements not used in any Dataflow"
    )
    findings = varFindings([], doc="threats found for elements of this model")
    onDuplicates = varAction(
        Action.NO_ACTION,
        doc="""How to handle duplicate Dataflow
with same properties, except name and notes""",
    )
    assumptions = varStrings(
        [],
        required=False,
        doc="A list of assumptions about the design/model.",
    )

    def __init__(self, name, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.name = name
        self._add_threats()
        # make sure generated diagrams do not change, makes sense if they're commited
        random.seed(0)

    @classmethod
    def reset(cls):
        cls._flows = []
        cls._elements = []
        cls._actors = []
        cls._assets = []
        cls._threats = []
        cls._boundaries = []
        cls._data = []
        cls._threatsExcluded = []

    def _init_threats(self):
        TM._threats = []
        self._add_threats()

    def _add_threats(self):
        from .threat import Threat

        # with open(self.threatsFile, "r", encoding="utf8") as threat_file:
        #     threats_json = json.load(threat_file)

        # for i in threats_json:
        #     TM._threats.append(Threat(**i))

    def resolve(self):
        from .finding import Finding
        finding_count = 0
        findings = []
        elements = defaultdict(list)
        for e in TM._elements:
            if not e.inScope:
                continue

            override_ids = set(f.threat_id for f in e.overrides)
            # if element is a dataflow filter out overrides from source and sink
            # because they will be always applied there anyway
            try:
                override_ids -= set(
                    f.threat_id for f in e.source.overrides + e.sink.overrides
                )
            except AttributeError:
                pass

            for t in TM._threats:
                if not t.apply(e) and t.id not in override_ids:
                    continue

                if t.id in TM._threatsExcluded:
                    continue

                finding_count += 1
                f = Finding(e, id=str(finding_count), threat=t)
                logger.debug(f"new finding: {f}")
                findings.append(f)
                elements[e].append(f)
        self.findings = findings
        for e, findings in elements.items():
            e.findings = findings

    def check(self):
        if self.description is None:
            raise ValueError(
                """Every threat model should have at least
a brief description of the system being modeled."""
            )

        TM._flows = self._match_responses(
            self._sort(TM._flows, self.isOrdered)
        )

        self._check_duplicates(TM._flows)

        self._apply_defaults(TM._flows, TM._data)

        for e in TM._elements:
            top = Counter(f.threat_id for f in e.overrides).most_common(1)
            if not top:
                continue
            threat_id, count = top[0]
            if count != 1:
                raise ValueError(
                    f"Finding {threat_id} have more than one override in {e}"
                )

        if self.ignoreUnused:
            TM._elements, TM._boundaries = self._get_elements_and_boundaries(
                TM._flows
            )

        result = True
        for e in TM._elements:
            if not e.check():
                result = False

        if self.ignoreUnused:
            # cannot rely on user defined order if assets are re-used in multiple models
            TM._elements = self._sort_elem(TM._elements)

        return result

    def _match_responses(self, flows):
        """Ensure that responses are pointing to requests"""
        index = defaultdict(list)
        for e in flows:
            key = (e.source, e.sink)
            index[key].append(e)
        for e in flows:
            if e.responseTo is not None:
                if not e.isResponse:
                    e.isResponse = True
                if e.responseTo.response is None:
                    e.responseTo.response = e
            if e.response is not None:
                if not e.response.isResponse:
                    e.response.isResponse = True
                if e.response.responseTo is None:
                    e.response.responseTo = e

        for e in flows:
            if not e.isResponse or e.responseTo is not None:
                continue
            key = (e.sink, e.source)
            if len(index[key]) == 1:
                e.responseTo = index[key][0]
                index[key][0].response = e

        return flows

    def _sort(self, flows, addOrder=False):
        ordered = sorted(flows, key=lambda flow: flow.order)
        if not addOrder:
            return ordered
        for i, flow in enumerate(ordered):
            if flow.order != -1:
                break
            ordered[i].order = i + 1
        return ordered

    def _sort_elem(self, elements):
        if len(elements) == 0:
            return elements
        orders = {}
        for e in elements:
            try:
                order = e.order
            except AttributeError:
                continue
            if e.source not in orders or orders[e.source] > order:
                orders[e.source] = order
        m = max(orders.values()) + 1
        return sorted(
            elements,
            key=lambda e: (
                orders.get(e, m),
                e.__class__.__name__,
                getattr(e, "order", 0),
                str(e),
            ),
        )

    def _check_duplicates(self, flows):
        if self.onDuplicates == Action.NO_ACTION:
            return

        index = defaultdict(list)
        for e in flows:
            key = (e.source, e.sink)
            index[key].append(e)

        for flows in index.values():
            for left, right in combinations(flows, 2):
                left_attrs = left._attr_values()
                right_attrs = right._attr_values()
                for a in self._duplicate_ignored_attrs:
                    del left_attrs[a], right_attrs[a]
                if left_attrs != right_attrs:
                    continue
                if self.onDuplicates == Action.IGNORE:
                    right._is_drawn = True
                    continue

                left_controls_attrs = left.controls._attr_values()
                right_controls_attrs = right.controls._attr_values()
                # for a in self._duplicate_ignored_attrs:
                #    del left_controls_attrs[a], right_controls_attrs[a]
                if left_controls_attrs != right_controls_attrs:
                    continue
                if self.onDuplicates == Action.IGNORE:
                    right._is_drawn = True
                    continue

                raise ValueError(
                    "Duplicate Dataflow found between {} and {}: "
                    "{} is same as {}".format(
                        left.source,
                        left.sink,
                        left,
                        right,
                    )
                )

    def report(self, template_path):
        with open(template_path) as file:
            template = file.read()

        threats = self.encode_threat_data(TM._threats)
        findings = self.encode_threat_data(self.findings)

        elements = self.encode_element_threat_data(TM._elements)
        assets = self.encode_element_threat_data(TM._assets)
        actors = self.encode_element_threat_data(TM._actors)
        boundaries = self.encode_element_threat_data(TM._boundaries)
        flows = self.encode_element_threat_data(TM._flows)

        data = {
            "tm": self,
            "dataflows": flows,
            "threats": threats,
            "findings": findings,
            "elements": elements,
            "assets": assets,
            "actors": actors,
            "boundaries": boundaries,
            "data": TM._data,
        }

        return data

    def encode_element_threat_data(self, obj):
        """Used to html encode threat data from a list of Elements"""
        encoded_elements = []
        if type(obj) is not list:
            raise ValueError(
                "expecting a list value, got a {}".format(type(obj))
            )

        for o in obj:
            c = copy.deepcopy(o)
            for a in o._attr_values():
                if a == "findings":
                    encoded_findings = self.encode_threat_data(o.findings)
                    c._safeset("findings", encoded_findings)
                else:
                    v = getattr(o, a)
                    if type(v) is not list or (
                        type(v) is list and len(v) != 0
                    ):
                        c._safeset(a, v)
            encoded_elements.append(c)

        return encoded_elements

    def encode_threat_data(self, obj):
        from .finding import Finding
        """Used to html encode threat data from a list of threats or findings"""
        encoded_threat_data = []

        attrs = [
            "description",
            "details",
            "severity",
            "mitigations",
            "example",
            "id",
            "threat_id",
            "references",
            "condition",
        ]

        if type(obj) is Finding or (len(obj) != 0 and type(obj[0]) is Finding):
            attrs.append("target")

        for e in obj:
            t = copy.deepcopy(e)

            for a in attrs:
                try:
                    v = getattr(e, a)
                except AttributeError:
                    # ignore missing attributes, since this can be called
                    # on both a Finding and a Threat
                    continue
                setattr(t, a, html.escape(v))

            encoded_threat_data.append(t)

        return encoded_threat_data
