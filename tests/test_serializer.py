from tmnpy.dsl import Asset, Actor, Boundary, Data, DataFlow, ExternalEntity, Process, WorkFlow
from tmnpy.dsl.asset import Machine
from tmnpy.dsl.requirement import Property
from tmnpy.dsl.data import Lifetime
from tmnpy.util.serializer import TMNTSerializer

import unittest


class TestSerializerName(unittest.TestCase):
    def setUp(self):
        self.serializer = TMNTSerializer()
        return super().setUp()

    def test_asset_name(self):
        a = Asset("test")
        serealized = self.serializer.serialize(a, 0, {})

        test_dict = {"name": "test"}
        self.assertEqual(test_dict.items() <= serealized.items(), True)
        self.assertEqual(serealized["name"], "test")
        self.assertEqual(serealized["type"], "Asset")

    def test_externalentity_name(self):
        e = ExternalEntity("test")
        serealized = self.serializer.serialize(e, 0, {})

        test_dict = {"name": "test"}
        self.assertEqual(test_dict.items() <= serealized.items(), True)
        self.assertEqual(serealized["name"], "test")
        self.assertEqual(serealized["type"], "ExternalEntity")

    def test_process_name(self):
        p = Process("test")
        serealized = self.serializer.serialize(p, 0, {})

        test_dict = {"name": "test"}
        self.assertEqual(test_dict.items() <= serealized.items(), True)
        self.assertEqual(serealized["name"], "test")
        self.assertEqual(serealized["type"], "Process")

    def test_actor_name(self):
        a = Actor("test")
        serealized = self.serializer.serialize(a, 0, {})
        
        test_dict = {"name": "test"}
        self.assertEqual(test_dict.items() <= serealized.items(), True)
        self.assertEqual(serealized["name"], "test")
        self.assertEqual(serealized["type"], "Actor")

    def test_boundary_name(self):
        b = Boundary("test")
        serealized = self.serializer.serialize(b, 0, {})
        
        test_dict = {"name": "test"}
        self.assertEqual(test_dict.items() <= serealized.items(), True)
        self.assertEqual(serealized["name"], "test")

    def test_dataflow_name(self):
        d = DataFlow("test", src = Asset("src"), dst = Asset("dst"))
        serealized = self.serializer.serialize(d, 0, {})
        
        self.assertEqual(serealized["name"], "test")
        self.assertEqual(serealized["src"]["name"], "src")
        self.assertEqual(serealized["dst"]["name"], "dst")
        self.assertEqual(serealized["type"], "DataFlow")

    def test_workflow_name(self):
        w = WorkFlow("test", src = Asset("src"), dst = Asset("dst"))
        serealized = self.serializer.serialize(w, 0, {})
        
        self.assertEqual(serealized["name"], "test")
        self.assertEqual(serealized["src"]["name"], "src")
        self.assertEqual(serealized["dst"]["name"], "dst")
        self.assertEqual(serealized["type"], "WorkFlow")

    def tearDown(self) -> None:
        return super().tearDown()


class TestSerializerElements(unittest.TestCase):
    def setUp(self):
        self.serializer = TMNTSerializer()
        return super().setUp()

    def test_asset(self):
        a = Asset("Life Support/Monitoring Equipment")
        a.machine = "PHYSICAL"
        a.open_port = [9999]
        a.security_property.confidentiality = "HIGH"
        a.security_property.integrity = "HIGH"
        a.security_property.availability = "HIGH"
        data_elem = Data("Patient Monitoring Data")
        data_elem.is_pii = True
        data_elem.is_phi = True
        data_elem.format = "Digital"
        data_elem.is_credentials = False
        data_elem.desc = "Kept for the duration of the surgery"
        data_elem.lifetime = "NONE"
        a.data.append(data_elem)
        serealized = self.serializer.serialize(a, 0, {})

        self.assertEqual(serealized["name"], "Life Support/Monitoring Equipment")
        self.assertEqual(serealized["type"], "Asset")
        self.assertEqual(serealized["machine"], Machine.PHYSICAL)
        self.assertEqual(serealized["open_port"], [9999])
        self.assertEqual(serealized["security_property"]["confidentiality"], Property.HIGH)
        self.assertEqual(serealized["security_property"]["integrity"], Property.HIGH)
        self.assertEqual(serealized["security_property"]["availability"], Property.HIGH)
        self.assertEqual(serealized["data"][0]["name"], "Patient Monitoring Data")
        self.assertEqual(serealized["data"][0]["is_pii"], True)
        self.assertEqual(serealized["data"][0]["is_phi"], True)
        self.assertEqual(serealized["data"][0]["format"], "Digital")
        self.assertEqual(serealized["data"][0]["is_credentials"], False)
        self.assertEqual(serealized["data"][0]["desc"], "Kept for the duration of the surgery")
        # self.assertEqual(serealized["data"][0]["lifetime"], Lifetime.NONE)

    def test_actor(self):
        a = Actor("Surgeon")
        a.actor_type = "Individual"
        a.internal = False
        serealized = self.serializer.serialize(a, 0, {})

        self.assertEqual(serealized["name"], "Surgeon")
        self.assertEqual(serealized["type"], "Actor")
        self.assertEqual(serealized["actor_type"], "Individual")
        self.assertEqual(serealized["internal"], False)

    def test_dataflow(self):
        asset1 = Asset("Life Support/Monitoring Equipment")
        asset2 = Asset("Surgeon Workstation")
        d = DataFlow("Data Transfer from Life Support to Surgeon Workstation", src = asset1, dst = asset2)
        d.port = "443"
        d.protocol = "HTTPS"
        d.authentication = "TLS"
        d.multifactor_authentication = False
        serealized = self.serializer.serialize(d, 0, {})

        self.assertEqual(serealized["name"], "Data Transfer from Life Support to Surgeon Workstation")
        self.assertEqual(serealized["type"], "DataFlow")
        self.assertEqual(serealized["src"]["name"], "Life Support/Monitoring Equipment")
        self.assertEqual(serealized["dst"]["name"], "Surgeon Workstation")
        self.assertEqual(serealized["port"], "443")
        self.assertEqual(serealized["protocol"], "HTTPS")
        self.assertEqual(serealized["authentication"], "TLS")
        self.assertEqual(serealized["multifactor"], False)

    def test_workflow(self):
        asset1 = Asset("Surgeon Workstation")
        asset2 = Asset("Surgical Robot")
        asset3 = Asset("Hospital Network")
        w = WorkFlow("Surgical Procedure Execution Flow", src = asset1, dst = asset2)
        w.path = [asset3]
        serealized = self.serializer.serialize(w, 0, {})

        self.assertEqual(serealized["name"], "Surgical Procedure Execution Flow")
        self.assertEqual(serealized["type"], "WorkFlow")
        self.assertEqual(serealized["src"]["name"], "Surgeon Workstation")
        self.assertEqual(serealized["dst"]["name"], "Surgical Robot")
        self.assertEqual(serealized["path"][1]["name"], "Hospital Network")

    def tearDown(self) -> None:
        return super().tearDown()


class TestSerializerElementLists(unittest.TestCase):
    def setUp(self):
        self.serializer = TMNTSerializer()
        return super().setUp()

    def test_asset_list(self):
        a1 = Asset("asset1")
        a2 = Asset("asset2")
        a3 = Asset("asset3")
        serealized = self.serializer.serialize_list([a1, a2, a3], {})

        self.assertEqual("assets" in serealized, True)
        self.assertEqual(serealized["assets"][0]["name"], "asset1")
        self.assertEqual(serealized["assets"][1]["name"], "asset2")
        self.assertEqual(serealized["assets"][2]["name"], "asset3")

    def test_boundary_list(self):
        b1 = Boundary("boundary1")
        b2 = Boundary("boundary2")
        b3 = Boundary("boundary3")
        serealized = self.serializer.serialize_list([b1, b2, b3], {})

        self.assertEqual("boundaries" in serealized, True)
        self.assertEqual(serealized["boundaries"][0]["name"], "boundary1")
        self.assertEqual(serealized["boundaries"][1]["name"], "boundary2")
        self.assertEqual(serealized["boundaries"][2]["name"], "boundary3")

    def test_flow_list(self):
        f1 = DataFlow("flow1", src = Asset("src1"), dst = Asset("dst1"))
        f2 = WorkFlow("flow2", src = Asset("src2"), dst = Asset("dst2"))
        f3 = DataFlow("flow3", src = Asset("src3"), dst = Asset("dst3"))
        serealized = self.serializer.serialize_list([f1, f2, f3], {})

        self.assertEqual("flows" in serealized, True)
        self.assertEqual(serealized["flows"][0]["name"], "flow1")
        self.assertEqual(serealized["flows"][0]["src"]["name"], "src1")
        self.assertEqual(serealized["flows"][0]["dst"]["name"], "dst1")
        self.assertEqual(serealized["flows"][1]["name"], "flow2")
        self.assertEqual(serealized["flows"][1]["src"]["name"], "src2")
        self.assertEqual(serealized["flows"][1]["dst"]["name"], "dst2")
        self.assertEqual(serealized["flows"][2]["name"], "flow3")
        self.assertEqual(serealized["flows"][2]["src"]["name"], "src3")
        self.assertEqual(serealized["flows"][2]["dst"]["name"], "dst3")

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()




