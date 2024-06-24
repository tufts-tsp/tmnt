import unittest

from tmnpy.util.tmntparser import TMNTParser
from tmnpy.dsl import *



class TestTMNTParser(unittest.TestCase):

    def __init__(self):
        self.parser = TMNTParser(name="threatmodel_test", "../examples/parser_examples/presentation_dsl_example.yaml")
        self.TM = self.parser.tm
        return super().setUp()


    #parse workflow
    def test_parse_workflow(self):


    #parse dataflow
    def test_parse_dataflow(self):


    def test_parse_flow(self):
        flow_data = self.example_data["flow"]
        flow = self.parser.parse_flow(flow_data)

        name = flow.name
        authentication = flow.authentication
        multifactor_authentication = flow.multifactor_authentication

        self.assertEqual(name, "Data Transfer from Life Support to Surgeon Workstation")
        self.assertEqual(authentication, "TLS")
        self.assertEqual(multifactor_authentication, false)



    #process
    def test_parse_process(self):


    #datastore
    def test_parse_datastore(self):


    def test_parse_asset(self):
        asset_data = self.example_data["assets"]
        asset = self.parser.parse_asset(asset_data)

        name = asset_data.name
        machine = asset_data.machine

        self.assertEqual(name, "Life Support/Monitoring Equipment")
        self.assertEqual(machine, "PHYSICAL")


    def test_parse_external_entities(self):
        ee_data = self.example_data["external_entitie"]
        external_entities = self.parser.pparse_external_entitie(ee_data)

        name = external_entities.name
        physical_access = external_entities.physical_access

        self.assertEqual(name, "Remote Maintenance Provider")
        self.assertEqual(physical_access, false)


    #weakness
    def test_parse_weakness(self):


    #vulnerability
    def test_parse_vulnerability(self):


    #threat
    def test_parse_threat(self):


    #issue
    def test_parse_issue(self):


    def test_parse_data(self):
        for item in self.example_data:
            print(item)
            for obj in self.example_data[item]:
                print(obj)


        data = self.parser.parse_data(d_data)

        name = data.name
        is_pii = data.is_pii
        is_phi = data.is_phi
        format = data.format
        is_credentials = data.is_credentials
        lifetime = data.lifetime


        self.assertEqual(name, "Patient Monitoring Data")
        self.assertEqual(is_pii, true)
        self.assertEqual(is_phi, true)
        self.assertEqual(format, "Digital")
        self.assertEqual(is_credentials, false)
        self.assertEqual(lifetime, "For the duration of the surgery")



    #component
    def test_parse_component(self):


    def test_parse_actor(self):
        actor_data = self.example_data["actor"]
        actor = self.parser.parse_actor(actor_data)

        name = actor.name
        actor_type = actor.actor_type
        physical_access = actor.physical_access

        self.assertEqual(name, "Surgeon")
        self.assertEqual(actor_type, "Individual")
        self.assertEqual(physical_access, true)


    #boundary
    def test_parse_boundary(self):


    #element
    def test_parse_element(self):


    #safetyimpact
    def test_parse_safetyimpact(self):


    def test_parse_security_property(self):
        security_property_data = self.TM.components()
        #["security_property"]
        security_property = self.parser.parse_security_property(security_property_data)

        confidentiality = security_property.confidentiality
        integrity = security_property.integrity
        availability = security_property.availability

        self.assertEqual(confidentiality, "HIGH")
        self.assertEqual(integrity, "HIGH")
        self.assertEqual(availability, "HIGH")



    #stride
    def test_parse_stride(self):


    #finding
    def test_parse_finding(self):


    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":

    parser = TestTMNTParser()
    parser.test_parse_data()
