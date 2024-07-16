from tmnpy.dsl import Asset, Actor, Boundary, DataFlow, Datastore, ExternalEntity, Process, WorkFlow
from tmnpy.dsl.asset import Machine, DATASTORE_TYPE
from tmnpy.dsl.data import Lifetime
from tmnpy.util.parsers import TMNTParser
from tmnpy.dsl.requirement import SecurityProperty, Property

import unittest
import os


class TestTMNTParser(unittest.TestCase):
    def setUp(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        self.parser = TMNTParser(
            tm_name="threatmodel_test",
            yaml=f"{directory}/dsl_parser_test.yaml",
        )
        self.tm = self.parser.tm
        return super().setUp()

    def test_parse_actor(self):
        actor_data = [a for a in self.tm.actors if a.name == "Surgeon"]
        self.assertEqual(len(actor_data), 1)
        actor = actor_data[0]
        self.assertIsInstance(actor, Actor)

        name = actor.name
        actor_type = actor.actor_type

        self.assertEqual(name, "Surgeon")
        self.assertEqual(actor_type, "Individual")

    def test_parse_asset(self):
        asset_data = [
            a
            for a in self.tm.enumerate_assets(Asset)
            if a.name == "Life Support/Monitoring Equipment"
        ]
        self.assertEqual(len(asset_data), 1)
        asset = asset_data[0]
        self.assertIsInstance(asset, Asset)
        name = asset.name
        security_property = asset.security_property
        machine = asset.machine
        self.assertEqual(len(asset.data), 1)
        data = asset.data[0]

        self.assertEqual(name, "Life Support/Monitoring Equipment")
        self.assertEqual(security_property.confidentiality, Property.HIGH)
        self.assertEqual(security_property.integrity, Property.HIGH)
        self.assertEqual(security_property.availability, Property.HIGH)
        self.assertEqual(machine, Machine.PHYSICAL)
        self.assertEqual(data.name, "Patient Monitoring Data")
        self.assertEqual(data.is_pii, True)
        self.assertEqual(data.is_phi, True)
        self.assertEqual(data.format, "Digital")
        self.assertEqual(data.is_credentials, False)
        self.assertEqual(data.desc, "Kept for the duration of the surgery")
        self.assertEqual(data.lifetime, Lifetime.AUTO)

    def test_parse_external_entities(self):
        external_entities_data = self.tm.enumerate_assets(ExternalEntity)
        self.assertEqual(len(external_entities_data), 0)

    def test_parse_dataflow(self):
        dataflow_data = [
            a
            for a in self.tm.enumerate_flows(DataFlow)
            if a.name == "Data Transfer from Life Support to Surgeon Workstation"
        ]
        self.assertEqual(len(dataflow_data), 1)
        dataflow = dataflow_data[0]
        self.assertIsInstance(dataflow, DataFlow)
        name = dataflow.name
        src = dataflow.src
        dst = dataflow.dst
        port = dataflow.port
        protocol = dataflow.protocol
        authentication = dataflow.authentication
        multifactor_authentication = dataflow.multifactor_authentication

        self.assertEqual(
            name, "Data Transfer from Life Support to Surgeon Workstation"
        )
        self.assertIsInstance(src, Asset)
        self.assertEqual(src.name, "Life Support/Monitoring Equipment")
        self.assertIsInstance(dst, Asset)
        self.assertEqual(dst.name, "Surgeon Workstation")
        self.assertEqual(port, "443")
        self.assertEqual(protocol, "HTTPS")
        self.assertEqual(authentication, "TLS")
        self.assertEqual(multifactor_authentication, False)

    def test_parse_workflow(self):
        workflow_data = [
            a
            for a in self.tm.enumerate_flows(WorkFlow)
            if a.name == "Surgical Procedure Execution Flow"
        ]
        self.assertEqual(len(workflow_data), 1)
        workflow = workflow_data[0]
        self.assertIsInstance(workflow, WorkFlow)

        name = workflow.name
        src = workflow.src
        dst = workflow.dst
        path = workflow.path
        self.assertEqual(len(path), 3)

        self.assertEqual(name, "Surgical Procedure Execution Flow")
        self.assertEqual(src.name, "Surgeon Workstation")
        self.assertEqual(dst.name, "Surgical Robot")
        self.assertEqual(path[0].name, "Surgeon Workstation")
        self.assertEqual(path[1].name, "Hospital Network")
        self.assertEqual(path[2].name, "Surgical Robot")

    def tearDown(self) -> None:
        return super().tearDown()


class TestTMNTParser1(unittest.TestCase):

    def setUp(self):
        self.parser = TMNTParser(
            tm_name = "threatmodel_test", 
            yaml = "dsl_test_example.yaml",
        )
        self.tm = self.parser.tm
        return super().setUp()

    def test_parse_process(self):
        process_data = [
            p 
            for p in self.tm.enumerate_assets(Process) 
            if p.name == "process example"
        ]
        self.assertEqual(len(process_data), 1)
        process = process_data[0]
        self.assertIsInstance(process, Process)

        name = process.name

        self.assertEqual(name, "process example")

    def test_parse_datastore(self):
        datastore_data = [
            d 
            for d in self.tm.enumerate_assets(Datastore) 
            if d.name == "datastore example"
        ]
        self.assertEqual(len(datastore_data), 1)
        datastore = datastore_data[0]
        self.assertIsInstance(datastore, Datastore)

        name = datastore.name
        ds_type = datastore.ds_type

        self.assertEqual(name, "datastore example")
        self.assertEqual(ds_type, DATASTORE_TYPE.UNKNOWN)

    def test_parse_boundary(self):
        boundary_data = [
            b for b in self.tm.boundaries if b.name == "boundary example"
        ]
        self.assertEqual(len(boundary_data), 1)
        boundary = boundary_data[0]
        self.assertIsInstance(boundary, Boundary)

        name = boundary.name
        elements = boundary.elements
        actors = boundary.actors
        # print(actors)

        self.assertEqual(name, "boundary example")
        self.assertEqual(elements[0].name, "asset example")
        self.assertEqual(elements[1].name, "process example")
        self.assertEqual(elements[2].name, "datastore example")
        self.assertEqual(len(actors), 1)
        self.assertEqual(actors[0].name, "actor example")
        self.assertEqual(actors[0].physical_access, True)
 
    def tearDown(self) -> None:
        return super().tearDown()


class TestMockDeviceDiagram(unittest.TestCase):

    def setUp(self):
        self.parser = TMNTParser(
            tm_name = "mock_device_diagram_test", 
            yaml = "test_mock_device_diagram.yaml",
        )
        self.tm = self.parser.tm
        return super().setUp()

    def test_parse_asset(self):
        asset_data = [
            a
            for a in self.tm.enumerate_assets(Asset)
            if a.name == "Hospital Infrastructure"
        ]
        self.assertEqual(len(asset_data), 1)
        asset = asset_data[0]
        self.assertIsInstance(asset, Asset)

        name = asset.name
        machine = asset.machine
        open_ports = asset.open_ports

        self.assertEqual(name, "Hospital Infrastructure")
        self.assertEqual(machine, Machine.PHYSICAL)
        self.assertEqual(open_ports, [22])
        self.assertEqual(open_ports[0], 22)

    def test_parse_datastore(self):
        datastore_data = [
            d 
            for d in self.tm.enumerate_assets(Datastore) 
            if d.name == "EHR Datastore"
        ]
        self.assertEqual(len(datastore_data), 1)
        datastore = datastore_data[0]
        self.assertIsInstance(datastore, Datastore)

        name = datastore.name
        machine = datastore.machine
        open_ports = datastore.open_ports
        ds_type = datastore.ds_type
        desc = datastore.desc
        data = datastore.data[0]
        data1 = datastore.data[4]

        self.assertEqual(name, "EHR Datastore")
        self.assertEqual(machine, Machine.VIRTUAL)
        self.assertEqual(open_ports, [443])
        self.assertEqual(open_ports[0], 443)
        self.assertEqual(ds_type, DATASTORE_TYPE.OTHER)
        self.assertEqual(desc, "include later")
        self.assertEqual(data.name, "Patient Vitals")
        self.assertEqual(data.is_pii, True)
        self.assertEqual(data.is_phi, True)
        self.assertEqual(data.format, "log")
        self.assertEqual(data.is_credentials, False)
        self.assertEqual(data.lifetime, Lifetime.LONG)
        self.assertEqual(data1.name, "Password")
        self.assertEqual(data1.is_pii, False)
        self.assertEqual(data1.is_phi, False)
        self.assertEqual(data1.format, "String")
        self.assertEqual(data1.is_credentials, True)
        self.assertEqual(data1.lifetime, Lifetime.LONG)    

    def test_parse_process(self):
        process_data = [
            p
            for p in self.tm.enumerate_assets(Process) 
            if p.name == "Life Support/Monitoring Equipment"
        ]
        self.assertEqual(len(process_data), 1)
        process = process_data[0]
        self.assertIsInstance(process, Process)

        name = process.name
        machine = process.machine
        open_ports = process.open_ports
        data = process.data[0]
        data1 = process.data[1]

        self.assertEqual(name, "Life Support/Monitoring Equipment")
        self.assertEqual(machine, Machine.PHYSICAL)
        self.assertEqual(open_ports, [9999])
        self.assertEqual(open_ports[0], 9999)
        self.assertEqual(data.name, "Patient Vitals")
        self.assertEqual(data.is_pii, True)
        self.assertEqual(data.is_phi, True)
        self.assertEqual(data.format, "log")
        self.assertEqual(data.is_credentials, False)
        self.assertEqual(data.lifetime, Lifetime.LONG)
        self.assertEqual(data1.name, "Encryption Keys")
        self.assertEqual(data1.is_pii, False)
        self.assertEqual(data1.is_phi, False)
        self.assertEqual(data1.format, "RSA")
        self.assertEqual(data1.is_credentials, True)
        self.assertEqual(data1.lifetime, Lifetime.MANUAL)    

    def test_parse_actors(self):
        self.assertEqual(len(self.tm.actors), 10)
        actor_data = [a for a in self.tm.actors if a.name == "Observer"]
        self.assertEqual(len(actor_data), 1)
        actor = actor_data[0]
        self.assertIsInstance(actor, Actor)

        name = actor.name
        actor_type = actor.actor_type
        internal = actor.internal

        self.assertEqual(name, "Observer")
        self.assertEqual(actor_type, "Individual")
        self.assertEqual(internal, False)

        actor_data1 = [a for a in self.tm.actors if a.name == "Manufacturer Techs"]
        self.assertEqual(len(actor_data1), 1)
        actor1 = actor_data1[0]
        self.assertIsInstance(actor1, Actor)

        name1 = actor1.name
        actor_type1 = actor1.actor_type
        internal1 = actor1.internal

        self.assertEqual(name1, "Manufacturer Techs")
        self.assertEqual(actor_type1, "Consultants")
        self.assertEqual(internal1, True)

    def test_parse_boundary(self):
        self.assertEqual(len(self.tm.boundaries), 7)
        boundary_data = [
            b for b in self.tm.boundaries if b.name == "Cloud (Datastore)"
        ]
        self.assertEqual(len(boundary_data), 1)
        boundary = boundary_data[0]
        self.assertIsInstance(boundary, Boundary)

        name = boundary.name
        elements = boundary.elements
        actors = boundary.actors
        # physical_access = boundary.physical_access

        self.assertEqual(name, "Cloud (Datastore)")
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].name, "EHR Datastore")
        self.assertEqual(len(actors), 3)
        self.assertEqual(actors[0].name, "Cloud Provider")
        self.assertEqual(actors[0].physical_access, True)
        self.assertEqual(actors[0].name, "Hospital 1 IT")
        self.assertEqual(actors[0].name, "upport Consultants")

    def test_parse_workflow(self):
        workflow_data = [
            a
            for a in self.tm.enumerate_flows(WorkFlow)
            if a.name == "Surgeon - Surgical Robot (internal)"
        ]
        self.assertEqual(len(workflow_data), 1)
        workflow = workflow_data[0]
        self.assertIsInstance(workflow, WorkFlow)

        name = workflow.name
        src = workflow.src
        dst = workflow.dst
        path = workflow.path
        self.assertEqual(len(path), 3)

        self.assertEqual(name, "Surgeon - Surgical Robot (internal)")
        self.assertEqual(src.name, "Surgeon Workstation (internal)")
        self.assertEqual(dst.name, "Hospital Infrastructure")
        self.assertEqual(path[0].name, "Surgeon Workstation (internal)")
        self.assertEqual(path[1].name, "Surgical Robot")
        self.assertEqual(path[2].name, "Hospital Infrastructure")

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()