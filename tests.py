import unittest

from bang_pytm.core.tm import TM

class TestTM(unittest.TestCase):

    def setUp(self):
        self.tm = TM("test_tm")

    def test_tm_init(self):
        self.assertEqual(self.tm.name, "test_tm")
    
    def tearDown(self):
        TM.reset()


if __name__ == '__main__':
    unittest.main()
