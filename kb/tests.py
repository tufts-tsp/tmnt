import unittest

from rules import Rules, Rule
import sources
from tmnt.core import Finding, Asset, Process,Datastore,ExternalEntity,DataFlow
from tmnt.core.element import Element

def get_findings(tm_components, threat_map):
    findings = []
    for component in tm_components:
        mt, umt = threat_map.component_threats(component)
        finding = Finding(affected_components=component, issues=umt)
        findings.append(finding)
    return findings

class TestThreatlib(unittest.TestCase):
    # pytm_rules = Rules()
    # tm_components = [Asset("A"), Asset("B"), Process("C")]
    # findings = get_findings(tm_components, pytm_rules)
    def setUp(self):
        self.rules = Rules()
        asset1 = Asset("A")
        asset2 = Asset("B")
        process1 = Process("C")
        process2 = Process("D")
        datastore1 = Datastore("E")
        datastore2 = Datastore("F")
        external1 = ExternalEntity("G")
        external2 = ExternalEntity("H")
        dataflow1 = DataFlow("I", src=Element("s"), dst=Element("d"))
        dataflow2 = DataFlow("J", src=Element("s"), dst=Element("d"))
        self.tm_components = [
            asset1,
            asset2,
            process1,
            process2,
            datastore1,
            datastore2,
            external1,
            external2,
            dataflow1,
            dataflow2,
        ]
        for i in range(1, 10, 2):
            for r in self.rules.threatmap:
                for c in r.controls:
                    if c.title not in [
                        x.title for x in self.tm_components[i].controls
                    ]:
                        self.tm_components[i].add_control(c)

    def test_findings(self):
        self.findings = get_findings(self.tm_components, self.rules)

    def tearDown(self) -> None:
        for component in self.tm_components:
            for control in component.controls:
                component.remove_control(control)
        return super().tearDown()

class TestSources(unittest.TestCase):
    def test_load_asvs(self):
        asvs = sources.load_owasp_asvs()
        # assertEqual
        for c in asvs:
            self.assertEqual(type(c.id), str)
            self.assertEqual(type(c.title), str)
            self.assertEqual(type(c.desc), str)
            self.assertEqual(type(c.related), list)
            for id in c.related:
                self.assertEqual(type(id), dict)

    def test_load_capec(self):
        capec = sources.load_capec()
        for t in capec:
            self.assertEqual(type(t.name), str)
            self.assertEqual(type(t.desc), str)
            self.assertEqual(type(t.prerequisites), list)
            for p in t.prerequisites:
                self.assertEqual(type(p), str)
            self.assertEqual(type(t.mitigations), list)
            for m in t.mitigations:
                self.assertEqual(type(m), str)
            self.assertEqual(type(t.meta["ref_id"]), str)
            self.assertEqual(type(t.meta["long_desc"]), str)
            self.assertEqual(type(t.meta["likelihood"]), str)
            self.assertEqual(type(t.meta["severity"]), str)
            self.assertEqual(type(t.meta["related"]), list)
            for r in t.meta["related"]:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(t.meta["references"]), list)
            for r in t.meta["references"]:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(t.consequences), list)
            for c in t.consequences:
                self.assertEqual(type(c), dict)
            self.assertEqual(type(t.threat_source["required_skills"]), list)
            for s in t.threat_source["required_skills"]:
                self.assertEqual(type(s), dict)
            self.assertEqual(type(t.threat_source["required_resources"]), list)
            for r in t.threat_source["required_resources"]:
                self.assertEqual(type(r), str)
            self.assertEqual(type(t.examples), list)
            for e in t.examples:
                self.assertEqual(type(e), str)

    def test_load_cwes(self):
        cwes = sources.load_cwes()
        for w in cwes:
            self.assertEqual(type(w.name), str)
            self.assertEqual(type(w.meta["ref_id"]), str)
            self.assertEqual(type(w.alt_name), list)
            for a in w.alt_name:
                self.assertEqual(type(a), str)
            self.assertEqual(type(w.desc), str)
            self.assertEqual(type(w.meta["long_desc"]), str)
            self.assertEqual(type(w.modes_of_introduction), list)
            for m in w.modes_of_introduction:
                self.assertEqual(type(m), str)
            self.assertEqual(type(w.meta["likelihood"]), str)
            self.assertEqual(type(w.consequences), list)
            for c in w.consequences:
                self.assertEqual(type(c), dict)
            self.assertEqual(type(w.meta["related"]), list)
            for r in w.meta["related"]:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(w.mitigations), list)
            for m in w.mitigations:
                self.assertEqual(type(m), dict)
            self.assertEqual(type(w.detection_methods), list)
            for d in w.detection_methods:
                self.assertEqual(type(d), dict)
            self.assertEqual(type(w.meta["references"]), list)
            for r in w.meta["references"]:
                self.assertEqual(type(r), dict)

if __name__ == "__main__":
    unittest.main()
