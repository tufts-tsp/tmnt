"""import unittest

from bang_pytm.core.tm import TM
from bang_pytm.core.component import Component
from bang_pytm.core.element import Element
from bang_pytm.util.oscal_parser import OSCALParser

class TestControls(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_parse_metadata(self):
        


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
        TM.reset()

class TestElement(unittest.TestCase):
    
    def test_parent_assignments(self):

        elem1 = Element("test1")
        elem2 = Element("test2")
        elem3 = Element("test3")

        # elem1 becomes the child of elem2
        # elem2 becomes the parent of elem1
        elem1.parent = elem2

        # a parent node should not assign itself as a parent
        with self.assertRaises(AttributeError):
            elem1.parent = elem1

        # a parent node should not assign its child as a parent
        with self.assertRaises(AttributeError):
            elem2.parent = elem1
        
        # a node should not overwrite its parent node without removing it
        with self.assertRaises(ValueError):
            elem1.parent = elem3
        
        # grandparents should not be allowed
        with self.assertRaises(AttributeError):
            # elem1 is parent of elem3
            # elem2 is the parent of elem1
            # elem2 is the grandparent of elem3
            elem3.parent = elem1
    
    def test_child_assignments(self):
        
        elem1 = Element("test1")
        elem2 = Element("test2")
        elem3 = Element("test3")
        elem5 = Element("test5")

        # elem2 is now a child of elem1
        elem1.add_child(elem2)

        # if child is self.__parent
        # self.__parent = elem1
        with self.assertRaises(ValueError):
            elem2.add_child(elem1)
        
        # no grandparents/grandchildren allowed
        with self.assertRaises(AttributeError):
            elem3.add_child(elem1)

        # different parent already assigned
        elem3.add_child(elem5)
        with self.assertRaises(AttributeError):
            elem1.add_child(elem5)


if __name__ == '__main__':
    unittest.main()
"""