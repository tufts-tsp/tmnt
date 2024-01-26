import unittest

from bang_pytm.core.tm import TM

class TestActor(unittest.TestCase):

    def create_actor(self):

        tm = TM("test_tm")
        tm.description("this is a test tm")

if __name__ == '__main__':
    unittest.main()