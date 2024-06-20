import unittest

from tmnt.util.oscalparser2 import OSCALParser2
from tmnt.dsl import *



class TestOSCALParser2(unittest.TestCase):
    
    def __init__(self):
        self.parser = OSCALParser2()
        self.TM = TM(name = "threatmodel")
        file_path = "../examples/parser_examples/presentation_dsl_example.yaml"
        self.TM = self.parser.parse(file_path, TM)
        return super().setUp()


    def test_parse_security_property(self):
        security_property_data = self.TM["assets"]["security_property"]
        security_property = self.parser.parse_security_property(security_property_data)
        
        confidentiality = security_property.confidentiality
        integrity = security_property.integrity
        availability = security_property.availability

        self.assertEqual(confidentiality, "HIGH")
        self.assertEqual(integrity, "HIGH")
        self.assertEqual(availability, "HIGH")

    
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


    def test_parse_asset(self):
        asset_data = self.example_data["assets"]
        asset = self.parser.parse_asset(asset_data)

        name = asset_data.name
        machine = asset_data.machine

        self.assertEqual(name, "Life Support/Monitoring Equipment")
        self.assertEqual(machine, "PHYSICAL")

    def test_parse_actor(self):
        actor_data = self.example_data["actor"]
        actor = self.parser.parse_actor(actor_data)

        name = actor.name
        actor_type = actor.actor_type
        physical_access = actor.physical_access

        self.assertEqual(name, "Surgeon")
        self.assertEqual(actor_type, "Individual")
        self.assertEqual(physical_access, true)


    def test_parse_flow(self):
        flow_data = self.example_data["flow"]
        flow = self.parser.parse_flow(flow_data)

        name = flow.name
        authentication = flow.authentication
        multifactor_authentication = flow.multifactor_authentication

        self.assertEqual(name, "Data Transfer from Life Support to Surgeon Workstation")
        self.assertEqual(authentication, "TLS")
        self.assertEqual(multifactor_authentication, false)


    def test_parse_external_entities(self):
        ee_data = self.example_data["external_entitie"]
        external_entities = self.parser.pparse_external_entitie(ee_data)

        name = external_entities.name
        physical_access = external_entities.physical_access

        self.assertEqual(name, "Remote Maintenance Provider")
        self.assertEqual(physical_access, false)


    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":

    parser = TestOSCALParser2()
    parser.test_parse_data()

