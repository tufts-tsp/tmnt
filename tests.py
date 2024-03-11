import unittest

from bang_pytm.core.tm import TM
from bang_pytm.core.element import Element

class TestTM(unittest.TestCase):

    def setUp(self):
        self.tm = TM("test_tm")

    def test_tm_init(self):
        self.assertEqual(self.tm.name, "test_tm")

    def test_changing_name(self):
        with self.assertRaises(ValueError):
            self.tm.name = "test2_tm"
    
    def test_parent_child_assignments(self):

        elem1 = Element("test1")
        elem2 = Element("test2")
        elem3 = Element("test3")

        elem1.parent = elem2

        # a parent node should not assign itself as a parent
        with self.assertRaises(ValueError):
            elem1.parent = elem1

        # a parent node should not assign its child as a parent
        with self.assertRaises(ValueError):
            elem2.parent = elem1
        
        # a node should not overwrite its parent node without removing it
        with self.assertRaises(ValueError):
            elem1.parent = elem3

        # 

        elem1.add_child(elem2)

    def tearDown(self):
        TM.reset()


if __name__ == '__main__':
    unittest.main()
