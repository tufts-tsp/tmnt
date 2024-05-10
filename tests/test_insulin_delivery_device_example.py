import unittest

from tmnt_dsl.core.tm import TM
from tmnt_dsl.core.boundary import Boundary
from tmnt_dsl.core.actor import Actor
from tmnt_dsl.core.asset import (
    Asset,
    Process,
    Datastore,
    ExternalEntity,
    DATASTORE_TYPE,
)
from tmnt_dsl.core.flow import DataFlow


class TestInsulinDeliveryDeviceExample(unittest.TestCase):
    def setUp(self):
        self.tm = TM(name="Insulin Delivery Device TM")
        self.tm.description = "Insulin Delivery Device Threat Model"

        # Actors
        self.mfg = Actor(
            name="Manufacturer",
            actor_type="Organization",
            physical_access=False,
        )
        self.dist = Actor(
            name="Distributor",
            actor_type="Organization",
            physical_access=False,
        )
        self.user = Actor(
            name="End User", actor_type="Individual", physical_access=True
        )

        # Boundaries
        self.phd_idd = Boundary(name="PHD Insulin Delivery Device")
        self.connected_device = Boundary(name="Connected Device")

        # Processes
        self.idd_controller = Process(
            name="Insulin Delivery Device Controller"
        )
        self.phd_idd.add_child(self.idd_controller)

        self.connected_controller = Process(name="Connected Device Controller")
        self.connected_device.add_child(self.connected_controller)

        # External Entities
        self.actuator_pump = ExternalEntity(
            name="Actuator Pump Drive", physical_access=True
        )
        self.phd_idd.add_child(self.actuator_pump)

        self.testAsset = Asset(name="testAsset")

        # Datastores
        self.idd_configuration_db = Datastore(
            name="IDD Configuration Data Store", ds_type=DATASTORE_TYPE.SQL
        )
        self.phd_idd.add_child(self.idd_configuration_db)

        self.idd_therapy_setting_db = Datastore(
            name="IDD Therapy Setting Data Store", ds_type=DATASTORE_TYPE.SQL
        )
        self.phd_idd.add_child(self.idd_therapy_setting_db)

        self.idd_observation_db = Datastore(
            name="IDD Observation Data Store", ds_type=DATASTORE_TYPE.SQL
        )
        self.phd_idd.add_child(self.idd_observation_db)

        self.connected_configuration_db = Datastore(
            name="Connected Device Configuration Data Store",
            ds_type=DATASTORE_TYPE.SQL,
        )
        self.connected_device.add_child(self.connected_configuration_db)

        self.connected_therapy_setting_db = Datastore(
            name="Connected Device Therapy Setting Data Store",
            ds_type=DATASTORE_TYPE.SQL,
        )
        self.connected_device.add_child(self.connected_therapy_setting_db)

        self.connected_observation_db = Datastore(
            name="Connected Device Observation Data Store",
            ds_type=DATASTORE_TYPE.SQL,
        )
        self.connected_device.add_child(self.connected_observation_db)

        # Dataflows
        self.user_to_connected_controller = DataFlow(
            name="User to Connected Device Controller",
            src=self.user,
            dst=self.connected_controller,
        )

        self.connected_device_to_user = DataFlow(
            name="Connected Device Controller to User",
            src=self.connected_controller,
            dst=self.user,
        )

        self.user_to_idd_controller = DataFlow(
            name="User to Insulin Delivery Device Controller",
            src=self.user,
            dst=self.idd_controller,
        )

        self.idd_controller_to_user = DataFlow(
            name="Insulin Delivery Device Controller to User",
            src=self.idd_controller,
            dst=self.user,
        )

        self.pump_to_user = DataFlow(
            name="Actuator Pump Drive to User",
            src=self.actuator_pump,
            dst=self.user,
        )

        self.mfg_to_idd_controller = DataFlow(
            name="Mfg to Insulin Delivery Device Controller",
            src=self.mfg,
            dst=self.idd_controller,
        )

        self.idd_controller_to_mfg = DataFlow(
            name="Insulin Delivery Device Controller to Mfg",
            src=self.idd_controller,
            dst=self.mfg,
        )

        self.idd_controller_to_connected_controller = DataFlow(
            name="Insulin Delivery Device Controller to Connected Device Controller",
            src=self.idd_controller,
            dst=self.connected_controller,
        )

        self.connected_controller_to_idd_controller = DataFlow(
            name="Connected Device Controller to Insulin Delivery Device Controller",
            src=self.connected_controller,
            dst=self.idd_controller,
        )
        self.testFlow = DataFlow(
            name="testFlow", src=self.testAsset, dst=self.phd_idd
        )
        # Populate TM object
        self.tm._boundaries = (
            []
        )  # Clear existing boundaries to prevent duplication during multiple test runs
        self.tm._boundaries.append(self.phd_idd)
        self.tm._boundaries.append(self.connected_device)

        self.tm._actors = []
        self.tm._actors.append(self.mfg)
        self.tm._actors.append(self.dist)
        self.tm._actors.append(self.user)

        self.tm._assets = []
        self.tm._assets.append(self.idd_controller)
        self.tm._assets.append(self.connected_controller)
        self.tm._assets.append(self.actuator_pump)
        self.tm._assets.append(self.idd_configuration_db)
        self.tm._assets.append(self.idd_therapy_setting_db)
        self.tm._assets.append(self.idd_observation_db)
        self.tm._assets.append(self.connected_configuration_db)
        self.tm._assets.append(self.connected_therapy_setting_db)
        self.tm._assets.append(self.connected_observation_db)
        # self.tm._assets.append(self.testAsset)

        self.tm._flows = []
        self.tm._flows.append(self.user_to_connected_controller)
        self.tm._flows.append(self.connected_device_to_user)
        self.tm._flows.append(self.user_to_idd_controller)
        self.tm._flows.append(self.idd_controller_to_user)
        self.tm._flows.append(self.pump_to_user)
        self.tm._flows.append(self.mfg_to_idd_controller)
        self.tm._flows.append(self.idd_controller_to_mfg)
        self.tm._flows.append(self.idd_controller_to_connected_controller)
        self.tm._flows.append(self.connected_controller_to_idd_controller)
        # self.tm._flows.append(self.testFlow)

    def test_actor_assignment(self):
        print("Actors:")
        for actor in self.tm._actors:
            print(actor)
        print("\n")

    def test_boundary_assignment(self):
        for boundary in self.tm._boundaries:
            print(f"Boundary: {boundary}")
            for object in boundary.children:
                print(object)
            print("\n")

    def test_asset_assignment(self):
        print("Assets:")
        for asset in self.tm._assets:
            print(asset)
        print("\n")

    def test_flow_assignment(self):
        print("Flows:")
        for flow in self.tm._flows:
            print(flow)
        print("\n")

    def test_find_related_attack_vectors(self):
        print("Attack Vectors:")
        attack_vectors = self.tm.find_related_attack_vectors(
            self.idd_controller
        )
        for vector in attack_vectors:
            print(vector)
            print("\n")
        print("\n")

    def test_simulate_attack(self):
        print("Simulated Attacks:")
        simulated_attacks = self.tm.simulate_attack(self.idd_controller)
        for attack in simulated_attacks:
            print(attack)
            print("\n")
        print("\n")
