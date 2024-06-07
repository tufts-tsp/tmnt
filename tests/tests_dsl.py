import unittest

from tmnt.dsl import (
    TM,
    Asset,
    ExternalEntity,
    Datastore,
    Process,
    Control,
    ControlCatalog,
    Actor,
    DataFlow,
    Issue,
    Threat,
    Weakness,
    Vulnerability,
    Finding,
    Data,
    Flow,
)
from tmnt.dsl.component import Component
from tmnt.dsl.element import Element
from tmnt.dsl.asset import DATASTORE_TYPE




class TestTM(unittest.TestCase):
    def setUp(self):
        self.tm = TM("test_tm")
        return super().setUp()

    def test_tm_init(self):
        self.assertEqual(self.tm.name, "test_tm")

    def test_changing_name(self):
        with self.assertRaises(AttributeError):
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
        return super().tearDown()


class TestElement(unittest.TestCase):
    def setUp(self):
        self.element = Element(name="Test Element", desc="Description")
        return super().setUp()

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
        # most or all throw the errors from the parent function, not child

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
    def tearDown(self):
        return super().tearDown()


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.component = Component(name="Test Component", desc="Description")
        return super().setUp()

    def test_component_init(self):
        self.assertEqual(self.component.name, "Test Component")
        self.assertEqual(self.component.desc, "Description")
        self.assertEqual(len(self.component.data), 0)

    def test_data(self):
        data = Data(name="Test Data")
        self.component.add_data(data)
        self.assertEqual(len(self.component.data), 1)
        self.component.remove_data(data)
        self.assertEqual(len(self.component.data), 0)

    def test_control(self):
        control = Control(id="1", title="Test", desc="Description")
        self.component.add_control(control)
        self.assertEqual(len(self.component.controls), 1)
        self.component.remove_control(control)
        self.assertEqual(len(self.component.controls), 0)

    def test_threat(self):
        threat = Threat(
            name="Test Threat",
            desc="Threat description",
            likelihood="High",
            severity="Critical",
            consequences=[],
        )

        self.component.add_threat(threat)
        self.assertEqual(len(self.component.threats), 1)
        self.component.remove_threat(threat)
        self.assertEqual(len(self.component.threats), 0)

    def tearDown(self):
        return super().tearDown()


class TestAsset(unittest.TestCase):
    def setUp(self):
        self.asset = Asset(name="Test Asset")
        return super().setUp()

    def test_asset_init(self):
        self.assertEqual(self.asset.name, "Test Asset")
        self.assertEqual(len(self.asset.data), 0)
        self.assertEqual(len(self.asset.open_ports), 0)
        self.assertEqual(len(self.asset.boundaries), 0)
        ##should boundaries and trust boundaries be the same thing

    def test_external_entity(self):
        external_entity = ExternalEntity(
            name="External Entity Name", physical_access=True
        )
        self.assertIsInstance(external_entity, ExternalEntity)

    def test_datastore(self):
        datastore = Datastore(
            name="Datastore Name", ds_type=DATASTORE_TYPE.SQL
        )
        self.assertIsInstance(datastore, Datastore)

    def test_process(self):
        process = Process(name="Process Name")
        self.assertIsInstance(process, Process)

    def tearDown(self):
        return super().tearDown()


class TestFlow(unittest.TestCase):
    def setUp(self):
        elem1 = Element("test1")
        elem2 = Element("test2")
        self.flow = Flow(name="Test Flow", src=elem1, dst=elem2)
        return super().setUp()

    def test_flow_init(self):
        elem1 = Element("test1")
        elem2 = Element("test2")
        self.assertEqual(self.flow.name, "Test Flow")
        # self.assertEqual(self.flow.src, elem1)
        # self.assertEqual(self.flow.dst, elem2)
        self.assertEqual(len(self.flow.path), 2)
        self.assertEqual(self.flow.authentication, None)
        self.assertTrue(self.flow.multifactor_authentication)

    def tearDown(self):
        return super().tearDown()

class TestIssue(unittest.TestCase):
    def setUp(self):
        self.issue = Issue("test_issue")
        return super().setUp()

    def test_empty_issue(self):
        self.assertEqual(len(self.issue.consequences), 0)

    def test_add_remove_consequence(self):
        init_cnt = len(self.issue.consequences)
        self.issue.add_consequence("spoofing", "high")
        self.issue.remove_consequence(1)
        self.assertEqual(len(self.issue.consequences), init_cnt)

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
        return super().setUp()

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
        return super().tearDown()


class TestWeakness(unittest.TestCase):
    def setUp(self):
        self.weakness = Weakness("test_weakness")
        return super().setUp()

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
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class TestFinding(unittest.TestCase):
    def setUp(self):
        self.finding = Finding(
            affected_components=TestComponent, issues=TestIssue
        )
        self.finding = Finding(
            affected_components=Component("test_component"),
            issues=Issue("test_issue"),
        )
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class TestControl(unittest.TestCase):
    def setUp(self):
        self.vulnerability = Control("1", "test_control")
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class TestControlCatalog(unittest.TestCase):
    def setUp(self):
        self.control_catalog = ControlCatalog()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class TestActor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor("test_actor")
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
