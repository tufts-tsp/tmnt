import unittest

from bang_pytm.core.tm import TM
from bang_pytm.core.component import Component
from bang_pytm.core.element import Element
from bang_pytm.core.data import Data
from bang_pytm.core.asset import Asset
from bang_pytm.core.asset import ExternalEntity
from bang_pytm.core.asset import Process
from bang_pytm.core.asset import Datastore
from bang_pytm.core.flow import Flow
from bang_pytm.util.sources import *

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

    
class TestSources(unittest.TestCase):
    def test_load_asvs(self):
        asvs = load_owasp_asvs()
        # assertEqual
    def test_load_capec(self):
        capec = load_capec()
    def test_load_cwes(self):
        cwes = load_cwes()

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

    # def tearDown(self):
    #     self.component.reset()
    # AttributeError: 'Component' object has no attribute 'reset'
    # is there supposed to be a reset function

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



if __name__ == '__main__':
    unittest.main()
