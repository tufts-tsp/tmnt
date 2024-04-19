import unittest

from bang_pytm.core.tm import TM
from bang_pytm.core.component import Component
from bang_pytm.core.element import Element
from bang_pytm.core.data import Data
from bang_pytm.core.asset import Asset
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

    # no functions
    # children?


if __name__ == '__main__':
    unittest.main()
