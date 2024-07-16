from tmnpy.dsl.element import Element

import unittest


class TestElement(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create_basic_element(self):
        x = Element("Test")
        self.assertEqual(x.name, "Test")
        self.assertIsNone(x.desc)
        self.assertIsNone(x.parent)
        self.assertSetEqual(x.children, set())

    def test_equivalence(self):
        x = Element("Test")
        y = Element("Test1")
        z = Element("Test")
        self.assertEqual(x, x)
        self.assertEqual(x, z)
        self.assertNotEqual(x, y)

    def test_create_complex_element(self):
        x = Element("Test", desc="This is a test element")
        y = Element("Test Parent")
        x.parent = y
        self.assertEqual(x.name, "Test")
        self.assertEqual(x.desc, "This is a test element")
        self.assertEqual(x.parent, y)
        self.assertIsNone(y.parent)
        self.assertSetEqual(x.children, set())
        self.assertSetEqual(y.children, set([x]))

    def test_create_self_parent(self):
        x = Element("Test")
        with self.assertRaises(ValueError) as err:
            x.parent = x
        self.assertTrue("cannot be a parent of itself" in str(err.exception))

    def test_create_self_obbj_parent(self):
        x = Element("Test")
        y = Element("Test")
        with self.assertRaises(ValueError) as err:
            x.parent = y
        self.assertTrue("cannot be a parent of itself" in str(err.exception))

    def test_create_bad_child_parent(self):
        x = Element("Test")
        y = Element("Test Parent")
        x.parent = y
        with self.assertRaises(ValueError) as err:
            y.parent = x
        self.assertTrue("cannot be both" in str(err.exception))

    def test_grandparent(self):
        x = Element("Test")
        y = Element("Test Parent")
        x.parent = y
        z = Element("Test Grandparent")
        y.parent = z
        self.assertEqual(x.parent, y)
        self.assertEqual(y.parent, z)
        self.assertIsNone(z.parent)
        self.assertSetEqual(x.children, set())
        self.assertSetEqual(y.children, set([x]))
        self.assertSetEqual(z.children, set([y]))

    def test_remove_parent(self):
        x = Element("Test")
        y = Element("Test Parent")
        x.parent = y
        del x.parent
        self.assertIsNone(x.parent)
        self.assertSetEqual(y.children, set())

    def test_remove_child(self):
        x = Element("Test")
        y = Element("Test Parent")
        x.parent = y
        y.remove_child(x)
        self.assertIsNone(x.parent)
        self.assertSetEqual(y.children, set())

    def test_remove_grandparent(self):
        x = Element("Test")
        y = Element("Test Parent")
        x.parent = y
        z = Element("Test Grandparent")
        y.parent = z
        del y.parent
        self.assertEqual(x.parent, y)
        self.assertIsNone(y.parent)
        self.assertIsNone(z.parent)
        self.assertSetEqual(x.children, set())
        self.assertSetEqual(y.children, set([x]))
        self.assertSetEqual(z.children, set())

    def test_relationships(self):
        x = Element("Test")
        y = Element("Test Parent")
        z = Element("Test New Parent")

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
