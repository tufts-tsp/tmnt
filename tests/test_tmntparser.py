import unittest

from tmnpy.util.parsers import TMNTParser
from tmnpy.dsl.asset import Machine
from tmnpy.dsl.requirement import SecurityProperty, Property




class TestTMNTParser(unittest.TestCase):

    def setUp(self):
        self.parser = TMNTParser(tm_name = "threatmodel_test", yaml = "../examples/parser_examples/presentation_dsl_example.yaml")
        self.TM = self.parser.tm
        return super().setUp()


    def test_parse_actor(self):
        actor_data = [
            a for a in self.TM.actors if a.name == "Surgeon"
        ]
        if len(actor_data) == 1:
            actor = actor_data[0]

        name = actor.name
        actor_type = actor.actor_type
        physical_access = actor.physical_access

        self.assertEqual(name, "Surgeon")
        self.assertEqual(actor_type, "Individual")
        self.assertEqual(physical_access, True)


    def test_parse_asset(self):
        asset_data = [
            a for a in self.TM.components if a.name == "Life Support/Monitoring Equipment"
        ]
        if len(asset_data) == 1:
            asset = asset_data[0]

        name = asset.name
        security_property = asset.security_property
        machine = asset.machine
        data = asset.data

        self.assertEqual(name, "Life Support/Monitoring Equipment")
        self.assertEqual(security_property.confidentiality, Property.HIGH)
        self.assertEqual(security_property.integrity, Property.HIGH)
        self.assertEqual(security_property.availability, Property.HIGH)
        self.assertEqual(machine, Machine.PHYSICAL)
        self.assertEqual(data[0].name, "Patient Monitoring Data")
        self.assertEqual(data.is_pii, True)
        self.assertEqual(data.is_phi, True)
        self.assertEqual(data.format, "Digital")
        self.assertEqual(data.is_credentials, False)
        self.assertEqual(data.desc, "Kept for the duration of the surgery")
        self.assertEqual(data.lifetime, "AUTO")


#     def test_parse_external_entities(self):
#         external_entities_data = self.TM.assets()
        # if len(external_entities_data) == 1:
        #     external_entities = external_entities_data[0]
#         name = external_entities.name
#         security_property = external_entities.security_property
#         physical_access = external_entities.physical_access
#         machine = external_entities.machine
#         data = external_entities.data

#         self.assertEqual(name, "Remote Maintenance Provider")
#         self.assertEqual(security_property.confidentiality, "HIGH")
#         self.assertEqual(security_property.integrity, "HIGH")
#         self.assertEqual(security_property.availability, "HIGH")
#         self.assertEqual(physical_access, False)
#         self.assertEqual(machine, "VIRTUAL")
#         self.assertEqual(data.name, "Robot Maintenance Logs")
#         self.assertEqual(data.is_pii, False)
#         self.assertEqual(data.is_phi, False)
#         self.assertEqual(data.format, "Textual Log Files")
#         self.assertEqual(data.is_credentials, False)
#         self.assertEqual(data.desc, "Retained according to maintenance schedule")
#         self.assertEqual(data.lifetime, "AUTO")


#     def test_parse_dataflow(self):
#         dataflow_data = self.TM.flows()
        # if len(dataflow_data) == 1:
        #     dataflow = dataflow_data[0]

#         name = dataflow.name
#         src = dataflow.src
#         dst = dataflow.dst
#         port = dataflow.port
#         protocol = dataflow.protocol
#         authentication = dataflow.authentication
#         multifactor_authentication = dataflow.multifactor_authentication

#         self.assertEqual(name, "Data Transfer from Life Support to Surgeon Workstation")
#         self.assertEqual(src.name, "Life Support/Monitoring Equipment")
#         self.assertEqual(dst.name, "Surgeon Workstation")
#         self.assertEqual(port, "443")
#         self.assertEqual(protocol, "HTTPS")
#         self.assertEqual(authentication, "TLS")
#         self.assertEqual(multifactor_authentication, False)


#     def test_parse_workflow(self):
#         workflow_data = self.TM.flows()
        # if len(workflow_data) == 1:
        #     workflow = workflow_data[0]
            
#         name = workflow.name
#         src = workflow.src
#         dst = workflow.dst
#         path = workflow.path
#         authentication = workflow.authentication
#         multifactor_authentication = workflow.multifactor_authentication

#         self.assertEqual(name, "Surgical Procedure Execution Flow")
#         self.assertEqual(src.name, "Surgeon Workstation")
#         self.assertEqual(dst.name, "Surgical Robot")
#         self.assertEqual(path.name, "Hospital Network")
#         self.assertEqual(authentication, "Certificate-based")
#         self.assertEqual(multifactor_authentication, True)


#     def tearDown(self) -> None:
#         return super().tearDown()



# class TestTMNTParser1(unittest.TestCase):

#     def setUp(self):
#         self.parser = TMNTParser(tm_name = "threatmodel_test", yaml = "dsl_test_example.yaml")
#         self.TM = self.parser.tm
#         return super().setUp()


#     def test_parse_element(self):
#         element_data = [
#             a for a in self.TM.element if a.name == "element example"
#         ]
        # if len(element_data) == 1:
        #     element = element_data[0]
        
        # name = element.name
        # desc = element.desc
        # parent = element.parent
        # children = element.children
        # security_property  = element.security_property

        # self.assertEqual(name, "element example")
        # self.assertEqual(desc, "element desc")
        # self.assertEqual(parent.name, "parent example")
        # self.assertEqual(children.name, "children example")
#         self.assertEqual(security_property.confidentiality, "HIGH")
#         self.assertEqual(security_property.integrity, "HIGH")
#         self.assertEqual(security_property.availability, "HIGH")



#     def test_parse_boundary(self):
        # boundary_data = [
        #     a for a in self.TM.boundaries if a.name == "boundary example"
        # ]
#         if len(boundary_data) == 1:
#           boundary = boundary_data[0]

#         name = boundary.name
#         boundary_owner = boundary.boundary_owner

#         self.assertEqual(name, "boundary example")
#         self.assertEqual(boundary_owner, "Actor")



#     def test_parse_component(self):
#         component_data = self.TM.components()
#         if len(component_data) == 1:
#           component = component_data[0]

#         name = component.name

#         self.assertEqual(name, "component example")

    
#     def test_parse_process(self):
#         process_data = self.TM.assets()
#         if len(process_data) == 1:
#           process = process_data[0]

#         name = process.name

#         self.assertEqual("process example")


#     def test_parse_datastore(self):
#         datastore_data = self.TM.assets()
#         if len(datastore_data) == 1:
#           datastore = datastore_data[0]

#         name = datastore.name
#         ds_type = datastore.ds_type

#         self.assertEqual("process example")
#         self.assertEqual("UNKNOWN")


#     def tearDown(self) -> None:
#         return super().tearDown()


if __name__ == "__main__":
    unittest.main()




# others: finding, stride, property, safetyimpact, issue, threat, vulnerability, weakness
