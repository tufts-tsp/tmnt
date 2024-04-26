import unittest

from bang_pytm.core.tm import TM
from bang_pytm.core.component import Component
from bang_pytm.core.asset import Asset, ExternalEntity, Datastore, Process
from bang_pytm.core.threat import Issue, Threat, Weakness, Vulnerability
from bang_pytm.core.finding import Finding
from bang_pytm.core.element import Element
from bang_pytm.engine.rules import Rules, Rule
from bang_pytm.util.sources import *
from bang_pytm.util.get_findings import *

class TestTM(unittest.TestCase):

    def setUp(self):
        self.tm = TM("test_tm")

    def test_tm_init(self):
        self.assertEqual(self.tm.name, "test_tm")

    def test_changing_name(self):
        with self.assertRaises(ValueError):
            self.tm.name = "test2_tm"
    
    def test_adding_removing_component(self):
        
        component_list = []
        
        component1 = Component("test1")

        self.tm.add_component(component1)
        component_list = self.tm.components
        print(component_list)

        self.tm.remove_component(component1)
        component_list = self.tm.components
        print(component_list) 

    def tearDown(self):
        self.tm.reset()

class TestElement(unittest.TestCase):
    
    def test_parent_child_assignments(self):

        elem1 = Element("test1")
        elem2 = Element("test2")
        elem3 = Element("test3")

        elem1.parent = elem2

        # a parent node should not assign itself as a parent
        # with self.assertRaises(ValueError):
        #    elem1.parent = elem1

        # a parent node should not assign its child as a parent
        # with self.assertRaises(ValueError):
        #    elem2.parent = elem1
        
        # a node should not overwrite its parent node without removing it
        # with self.assertRaises(ValueError):
        #    elem1.parent = elem3

class TestComponent(unittest.TestCase):
    def setUp(self):
        self.component = Component(
            name="Test Component",
            desc="Description",
            data = []
        )

    def test_component_init(self):
        self.assertEqual(self.component.name, "Test Component")
        self.assertEqual(self.component.desc, "Description")
        self.assertEqual(len(self.component.data), 0)
        
    def test_add_control(self):
        control = Control(id="1", title="Test", desc="Description")
        self.component.add_control(control)

    def test_add_threat(self):
        threat = Threat(
            name="Test Threat",
            desc="Threat description",
            likelihood="High",
            severity="Critical",
            consequences=[]
        )

        self.component.add_threat(threat)

    def tearDown(self):
        return super().tearDown()

class TestSources(unittest.TestCase):
    def test_load_asvs(self):
        asvs = load_owasp_asvs()
        for c in asvs:
            self.assertEqual(type(c.id), str)
            self.assertEqual(type(c.title), str)
            self.assertEqual(type(c.desc), str)
            self.assertEqual(type(c.related), list)
            for id in c.related:
                self.assertEqual(type(id), dict)
    def test_load_capec(self):
        capec = load_capec()
        for t in capec:
            self.assertEqual(type(t.name), str)
            self.assertEqual(type(t.desc), str)
            self.assertEqual(type(t.prerequisites), list)
            for p in t.prerequisites:
                self.assertEqual(type(p), str)
            self.assertEqual(type(t.mitigations), list)
            for m in t.mitigations:
                self.assertEqual(type(m), str)
            self.assertEqual(type(t.meta['ref_id']), str)
            self.assertEqual(type(t.meta['long_desc']), str)
            self.assertEqual(type(t.meta['likelihood']), str)
            self.assertEqual(type(t.meta['severity']), str)
            self.assertEqual(type(t.meta['related']), list)
            for r in t.meta['related']:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(t.meta['references']), list)
            for r in t.meta['references']:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(t.consequences), list)
            for c in t.consequences:
                self.assertEqual(type(c), dict)
            self.assertEqual(type(t.threat_source['required_skills']), list)
            for s in t.threat_source['required_skills']:
                self.assertEqual(type(s), dict)
            self.assertEqual(type(t.threat_source['required_resources']), list)
            for r in t.threat_source['required_resources']:
                self.assertEqual(type(r), str)
            self.assertEqual(type(t.examples), list)
            for e in t.examples:
                self.assertEqual(type(e), str)
    def test_load_cwes(self):
        cwes = load_cwes()
        for w in cwes:
            self.assertEqual(type(w.name), str)
            self.assertEqual(type(w.meta['ref_id']), str)
            self.assertEqual(type(w.alt_name), list)
            for a in w.alt_name:
                self.assertEqual(type(a), str)
            self.assertEqual(type(w.desc), str)
            self.assertEqual(type(w.meta['long_desc']), str)
            self.assertEqual(type(w.modes_of_introduction), list)
            for m in w.modes_of_introduction:
                self.assertEqual(type(m), str)
            self.assertEqual(type(w.meta['likelihood']), str)
            self.assertEqual(type(w.consequences), list)
            for c in w.consequences:
                self.assertEqual(type(c), dict)
            self.assertEqual(type(w.meta['related']), list)
            for r in w.meta['related']:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(w.mitigations), list)
            for m in w.mitigations:
                self.assertEqual(type(m), dict)
            self.assertEqual(type(w.detection_methods), list)
            for d in w.detection_methods:
                self.assertEqual(type(d), dict)
            self.assertEqual(type(w.meta['references']), list)
            for r in w.meta['references']:
                self.assertEqual(type(r), dict)

class TestIssue(unittest.TestCase):
    def setUp(self):
        self.issue = Issue("test_issue")
    def tearDown(self) -> None:
        return super().tearDown()

class TestThreat(unittest.TestCase):
    def setUp(self):
        self.threat = Threat("test_threat")
    def tearDown(self) -> None:
        return super().tearDown()

class TestWeakness(unittest.TestCase):
    def setUp(self):
        self.weakness = Weakness("test_weakness")
    def tearDown(self) -> None:
        return super().tearDown()

class TestVulnerability(unittest.TestCase):
    def setUp(self):
        self.vulnerability = Vulnerability("test_vulnerability")
    def tearDown(self) -> None:
        return super().tearDown()

class TestFinding(unittest.TestCase):
    def setUp(self):
        self.finding = Finding(affected_components=TestComponent, issues=TestIssue)
    def tearDown(self) -> None:
        return super().tearDown()

class TestThreatlib(unittest.TestCase):
    pytm_rules = Rules()
    tm_components = [Asset("A"), Asset("B"), Process("C")]
    findings = get_findings(tm_components, pytm_rules)

if __name__ == '__main__':
    unittest.main()
