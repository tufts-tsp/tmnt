import unittest

from tmnt import kb


class TestASVS(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_load_asvs(self):
        asvs = kb.load_owasp_asvs()
        # assertEqual
        for c in asvs:
            self.assertEqual(type(c.id), str)
            self.assertEqual(type(c.title), str)
            self.assertEqual(type(c.desc), str)
            self.assertEqual(type(c.related), list)
            for id in c.related:
                self.assertEqual(type(id), dict)

    def tearDown(self):
        return super().tearDown()


class TestCAPEC(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_load_capec(self):
        capec = kb.load_capec()
        for t in capec:
            self.assertEqual(type(t.name), str)
            self.assertEqual(type(t.desc), str)
            self.assertEqual(type(t.prerequisites), list)
            for p in t.prerequisites:
                self.assertEqual(type(p), str)
            self.assertEqual(type(t.mitigations), list)
            for m in t.mitigations:
                self.assertEqual(type(m), str)
            self.assertEqual(type(t.meta["ref_id"]), str)
            self.assertEqual(type(t.meta["long_desc"]), str)
            self.assertEqual(type(t.meta["likelihood"]), str)
            self.assertEqual(type(t.meta["severity"]), str)
            self.assertEqual(type(t.meta["related"]), list)
            for r in t.meta["related"]:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(t.meta["references"]), list)
            for r in t.meta["references"]:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(t.consequences), list)
            for c in t.consequences:
                self.assertEqual(type(c), dict)
            self.assertEqual(type(t.threat_source["required_skills"]), list)
            for s in t.threat_source["required_skills"]:
                self.assertEqual(type(s), dict)
            self.assertEqual(type(t.threat_source["required_resources"]), list)
            for r in t.threat_source["required_resources"]:
                self.assertEqual(type(r), str)
            self.assertEqual(type(t.examples), list)
            for e in t.examples:
                self.assertEqual(type(e), str)

    def tearDown(self):
        return super().tearDown()


class TestCWES(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_load_cwes(self):
        cwes = kb.load_cwes()
        for w in cwes:
            self.assertEqual(type(w.name), str)
            self.assertEqual(type(w.meta["ref_id"]), str)
            self.assertEqual(type(w.alt_name), list)
            for a in w.alt_name:
                self.assertEqual(type(a), str)
            self.assertEqual(type(w.desc), str)
            self.assertEqual(type(w.meta["long_desc"]), str)
            self.assertEqual(type(w.modes_of_introduction), list)
            for m in w.modes_of_introduction:
                self.assertEqual(type(m), str)
            self.assertEqual(type(w.meta["likelihood"]), str)
            self.assertEqual(type(w.consequences), list)
            for c in w.consequences:
                self.assertEqual(type(c), dict)
            self.assertEqual(type(w.meta["related"]), list)
            for r in w.meta["related"]:
                self.assertEqual(type(r), dict)
            self.assertEqual(type(w.mitigations), list)
            for m in w.mitigations:
                self.assertEqual(type(m), dict)
            self.assertEqual(type(w.detection_methods), list)
            for d in w.detection_methods:
                self.assertEqual(type(d), dict)
            self.assertEqual(type(w.meta["references"]), list)
            for r in w.meta["references"]:
                self.assertEqual(type(r), dict)

    def tearDown(self):
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
