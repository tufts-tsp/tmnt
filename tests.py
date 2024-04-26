import unittest

from bang_pytm.core.tm import TM
from bang_pytm.core.component import Component
from bang_pytm.core.asset import Asset, ExternalEntity, Datastore, Process
from bang_pytm.core.control import Control, ControlCatalog
from bang_pytm.core.actor import Actor
from bang_pytm.core.flow import DataFlow
from bang_pytm.core.threat import Issue, Threat, Weakness, Vulnerability
from bang_pytm.core.finding import Finding
from bang_pytm.core.element import Element
from bang_pytm.engine.rules import Rules, Rule
from bang_pytm.core.data import Data
from bang_pytm.core.asset import Asset
from bang_pytm.core.asset import ExternalEntity
from bang_pytm.core.asset import Process
from bang_pytm.core.asset import Datastore
from bang_pytm.core.flow import Flow
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

        self.tm.remove_component(component1)
        component_list = self.tm.components

    def tearDown(self):
        self.tm.reset()

class TestElement(unittest.TestCase):

    def setUp(self):
        self.element = Element(
            name="Test Element",
            desc="Description"
        )

    def test_component_init(self):
        self.assertEqual(self.element.name, "Test Element")
        self.assertEqual(self.element.desc, "Description")
        self.assertEqual(len(self.element.children), 0)
        self.assertEqual(len(self.element.parent), 0)
    
    def test_parent_child_assignments(self):

        elem1 = Element("test1")
        elem2 = Element("test2")
        elem3 = Element("test3")

        elem1.parent = elem2
        # no child setter

        # a parent node should not assign itself as a parent
        # with self.assertRaises(ValueError):
        #    elem1.parent = elem1

        # a parent node should not assign its child as a parent
        # with self.assertRaises(ValueError):
        #    elem2.parent = elem1
        
        # a node should not overwrite its parent node without removing it
        # with self.assertRaises(ValueError):
        #    elem1.parent = elem3

        # AttributeError: Element(test2) has children, meaning Element(test3) would be a grandparent
        # with self.assertRaises(AttributeError):
        #    elem2.parent = elem3

        # elem1.remove_parent()

    def test_child_parent_assignments(self):
        #most or all throw the errors from the parent function, not child

        elem1 = Element("test1")
        elem2 = Element("test2")
        elem3 = Element("test3")

        elem1.add_child(elem2)

        # a child node should not assign itself as a child
        # with self.assertRaises(ValueError):
        # ValueError: Element(test1) is self, an element cannot be a parent of itself.
        #    elem1.add_child(elem1)

        # a parent node should not assign its child as a parent
        # with self.assertRaises(ValueError):
        # ValueError: Element(test2) cannot be both a child and parent of Element(test1).
        #    elem2.add_child(elem1)

        # ValueError: No grandparents allowed.
        # with self.assertRaises(ValueError):
        #    elem2.add_child(elem3)

        # AttributeError: A different parent has already been assigned
        #    elem1.add_child(elem2)
    
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

    def test_add_data(self):
        data = Data(name="Test Data")
        self.component.add_data(data)

    def test_remove_control(self):
        control = Control(id="1", title="Test", desc="Description")
        self.component.add_control(control)
        self.component.remove_control(control)

    def test_remove_threat(self):
        threat = Threat(
            name="Test Threat",
            desc="Threat description",
            likelihood="High",
            severity="Critical",
            consequences=[]
        )

        self.component.add_threat(threat)
        self.component.remove_threat(threat)

    def test_remove_data(self):
        data = Data(name="Test Data")
        self.component.add_data(data)
        self.component.remove_data(data)

    def tearDown(self):
        for c in self.component.controls:
            self.component.remove_control(c)
        return super().tearDown()

class TestAsset(unittest.TestCase):
    def setUp(self):
        self.asset = Asset(
            name="Test Asset"
        )

    def test_asset_init(self):
        self.assertEqual(self.asset.name, "Test Asset")
        self.assertEqual(len(self.asset.data), 0)
        self.assertEqual(len(self.asset.open_ports), 0)
        self.assertEqual(len(self.asset.boundaries), 0)
        ##should boundaries and trust boundaries be the same thing

    def test_external_entity(self):
        external_entity = ExternalEntity(name="External Entity Name", physical_access=True)
        self.assertIsInstance(external_entity, ExternalEntity)

    def test_datastore(self):
        datastore = Datastore(name="Datastore Name", ds_type="SQL")
        self.assertIsInstance(datastore, Datastore)


    def test_process(self):
        process = Process(name="Process Name")
        self.assertIsInstance(process, Process)
    
    # no functions

class TestFlow(unittest.TestCase):
    def setUp(self):
        elem1 = Element("test1")
        elem2 = Element("test2")
        self.flow = Flow(
            name="Test Flow",
            src=elem1,
            dst=elem2
        )

    def test_flow_init(self):
        elem1 = Element("test1")
        elem2 = Element("test2")
        self.assertEqual(self.flow.name, "Test Flow")
        # self.assertEqual(self.flow.src, elem1)
        # self.assertEqual(self.flow.dst, elem2)
        self.assertEqual(len(self.flow.path), 2)
        self.assertEqual(self.flow.authentication, None)
        self.assertTrue(self.flow.multifactor_authentication)

class TestSources(unittest.TestCase):
    def test_load_asvs(self):
        asvs = load_owasp_asvs()
        # assertEqual
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
    def test_empty_issue(self):
        print(self.issue.consequences)
        self.assertEqual(len(self.issue.consequences), 0)
    def test_add_remove_consequence(self):
        self.assertEqual(len(self.issue.consequences), 0)
        self.issue.add_consequence("spoofing", "high")
        self.issue.remove_consequence(1)
        self.assertEqual(len(self.issue.consequences), 0)
    def test_add_remove_consequence_multiple(self):
        self.issue.add_consequence("spoofing", "high")
        self.issue.add_consequence("spoofing", "high")
        self.issue.add_consequence("tampering", "low")
        self.issue.add_consequence("invalid value", "high")
        self.assertEqual(len(self.issue.consequences), 4)
        self.issue.remove_consequence(4)
        self.issue.remove_consequence(2)
        self.assertEqual(len(self.issue.consequences), 2)
        self.issue.remove_consequence(1)
        self.issue.remove_consequence(3)
        self.assertEqual(len(self.issue.consequences), 0)
    def tearDown(self) -> None:
        for c in self.issue.consequences:
            self.issue.remove_consequence(c["id"])
        return super().tearDown()

class TestThreat(unittest.TestCase):
    def setUp(self):
        self.threat = Threat("test_threat")
    def test_add_remove_step(self):
        self.threat.add_step(1, "Explore")
        self.threat.remove_step(1)
    def test_add_remove_step_multiple(self):
        self.threat.add_step(1, "Explore")
        self.threat.add_step(2, "Experiment")
        self.assertEqual(len(self.threat.attack_steps), 2)
        self.threat.add_step(2, "Explore")
        self.assertEqual(len(self.threat.attack_steps), 2)
        self.threat.add_step(5, "Exploit")
        self.threat.add_step(4, "invalid value")
        self.threat.remove_step(4)
        self.assertEqual(len(self.threat.attack_steps), 3)
        self.threat.remove_step(3)
        self.assertEqual(len(self.threat.attack_steps), 3)
    def tearDown(self) -> None:
        for s in self.threat.attack_steps:
            self.threat.remove_step(s["order"])
        return super().tearDown()

class TestWeakness(unittest.TestCase):
    def setUp(self):
        self.weakness = Weakness("test_weakness")
    def test_add_introduction(self):
        self.weakness.add_introduction("Policy")
        with self.assertRaises(ValueError):
            self.weakness.add_introduction("invalid value")
    def test_add_detection_method(self):
        self.weakness.add_detection_method("description")
    def tearDown(self) -> None:
        self.weakness = None
        return super().tearDown()

class TestVulnerability(unittest.TestCase):
    def setUp(self):
        self.vulnerability = Vulnerability("test_vulnerability")
    def tearDown(self) -> None:
        return super().tearDown()

class TestFinding(unittest.TestCase):
    def setUp(self):
        self.finding = Finding(affected_components=TestComponent, issues=TestIssue)
        self.finding = Finding(affected_components=Component("test_component"), issues=Issue("test_issue"))
    def tearDown(self) -> None:
        return super().tearDown()

class TestControl(unittest.TestCase):
    def setUp(self):
        self.vulnerability = Control("1", "test_control")
    def tearDown(self) -> None:
        return super().tearDown()

class TestControlCatalog(unittest.TestCase):
    def setUp(self):
        self.control_catalog = ControlCatalog()
    def tearDown(self) -> None:
        return super().tearDown()

class TestActor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor("test_actor")
    def tearDown(self) -> None:
        return super().tearDown()

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
        self.tm_components = [asset1, asset2, process1, process2, datastore1, datastore2, external1, external2, dataflow1, dataflow2]
        for i in range(1,10,2):
            for r in self.rules.threatmap:
                for c in r.controls:
                    if c.title not in [x.title for x in self.tm_components[i].controls]:
                        self.tm_components[i].add_control(c)
    
    def test_findings(self):
        self.findings = get_findings(self.tm_components, self.rules)

    def tearDown(self) -> None:
        for component in self.tm_components:
            for control in component.controls:
                component.remove_control(control)
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()
