import unittest
from tmnt.dsl import Asset, Process, Datastore, ExternalEntity, DataFlow
from tmnt.dsl.element import Element
from tmnt.engines.assignment import Assignment, Rule, get_findings


class TestThreatlib(unittest.TestCase):

    def setUp(self):
        self.rules = Assignment()
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
        self.tm_components = [
            asset1,
            asset2,
            process1,
            process2,
            datastore1,
            datastore2,
            external1,
            external2,
            dataflow1,
            dataflow2,
        ]
        for i in range(1, 10, 2):
            for r in self.rules.threatmap:
                for c in r.controls:
                    if c.title not in [
                        x.title for x in self.tm_components[i].controls
                    ]:
                        self.tm_components[i].add_control(c)

    def test_findings(self):
        self.findings = get_findings(self.tm_components, self.rules)

    def tearDown(self) -> None:
        for component in self.tm_components:
            for control in component.controls:
                component.remove_control(control)
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()
