import unittest

from tmnt.dsl import (
    TM,
    Boundary,
    Actor,
    Asset,
    Process,
    Datastore,
    ExternalEntity,
    DataFlow,
)
from tmnt.dsl.asset import (
    DATASTORE_TYPE,
    Machine,
)


class TestHotelBookingWebsiteExample(unittest.TestCase):
    def setUp(self):
        self.tm = TM(name="Hotel Booking TM")
        self.tm.description = "Hotel Booking Website Threat Model"

        # Actors
        self.users = Actor(name="Users", actor_type="Individual")
        self.system_admin = Actor(
            name="System Admin", actor_type="Administrator"
        )
        self.developer = Actor(name="Developer", actor_type="Organization")

        # Core Systems
        self.main_load_balancer = Process(
            name="Main Load Balancer", machine=Machine.SERVERLESS
        )
        self.secondary_load_balancer = Process(
            name="Secondary Load Balancer", machine=Machine.SERVERLESS
        )

        # Microservices
        # Manage bookings (create, update, handle)
        self.booking_service = Process(
            name="Booking Service", machine=Machine.CONTAINER
        )
        # Manage users (register, authenticate, profiles)
        self.user_service = Process(
            name="User Service", machine=Machine.CONTAINER
        )
        # Manage payments (process transactions)
        self.payment_service = Process(
            name="Payment Sertice", machine=Machine.CONTAINER
        )
        # Manage searches (search pricing, location, availibility)
        self.search_service = Process(
            name="Search Service", machine=Machine.CONTAINER
        )

        # Security and Monitoring
        self.splunk_monitoring = Process(
            name="Splunk Monitoring Service", machine=Machine.VIRTUAL
        )

        # API Gateway
        self.api_gateway = Process(
            name="Amazon API Gateway", machine=Machine.SERVERLESS
        )

        # Databases
        self.postgres_database = Datastore(
            name="PostgreSQL Database Server", ds_type=DATASTORE_TYPE.SQL
        )
        self.mongodb_database = Datastore(
            name="MongoDB Database", ds_type=DATASTORE_TYPE.NOSQL
        )

        # Cache
        self.redis_cache = Datastore(
            name="Redis Cache Server",
            ds_type=DATASTORE_TYPE.OTHER,
            desc="https://redis.io/docs/latest/",
        )

        # Message Queue
        self.rabbitmq = Datastore(
            name="RabbitMQ Message Queue",
            ds_type=DATASTORE_TYPE.OTHER,
            desc="https://www.rabbitmq.com/docs",
        )

        # CDN
        self.cloudfront_cdn = ExternalEntity(
            name="Amazon Cloudfront CDN", machine=Machine.SERVERLESS
        )

        # Payment Gateway
        self.stripe_payment_gateway = ExternalEntity(
            name="Stripe Payment Gateway", machine=Machine.SERVERLESS
        )

        # Email Service
        self.sendgrid_email_service = ExternalEntity(
            name="SendGrid Email Service", machine=Machine.SERVERLESS
        )

        # Dataflows
        # API gateway
        self.users_to_api_gateway = DataFlow(
            name="Users to API Gateway",
            src=self.users,
            dst=self.api_gateway,
            port=443,
            protocol="HTTPS",
        )
        self.api_gateway_to_booking_service = DataFlow(
            name="API Gateway to Booking Service",
            src=self.api_gateway,
            dst=self.booking_service,
            port=8080,
            protocol="HTTP",
        )
        self.api_gateway_to_user_service = DataFlow(
            name="API Gateway to User Service",
            src=self.api_gateway,
            dst=self.user_service,
            port=8080,
            protocol="HTTP",
        )
        self.api_gateway_to_payment_service = DataFlow(
            name="API Gateway to Payment Service",
            src=self.api_gateway,
            dst=self.payment_service,
            port=8080,
            protocol="HTTP",
        )
        self.api_gateway_to_search_service = DataFlow(
            name="API Gateway to Search Service",
            src=self.api_gateway,
            dst=self.search_service,
            port=8080,
            protocol="HTTP",
        )
        # services to database
        self.booking_service_to_postgres_db = DataFlow(
            name="Booking Service to PostgreSQL Database",
            src=self.booking_service,
            dst=self.postgres_database,
            port=5432,
            protocol="SQL",
        )
        self.booking_service_to_mongodb_db = DataFlow(
            name="Booking Service to MongoDB Database",
            src=self.booking_service,
            dst=self.mongodb_database,
            port=27017,
            protocol="MongoDB",
        )
        self.user_service_to_postgres_db = DataFlow(
            name="User Service to PostgreSQL Database",
            src=self.user_service,
            dst=self.postgres_database,
            port=5432,
            protocol="SQL",
        )
        self.payment_service_to_postgres_db = DataFlow(
            name="Payment Service to PostgreSQL Database",
            src=self.payment_service,
            dst=self.postgres_database,
            port=5432,
            protocol="SQL",
        )
        self.search_service_to_postgres_db = DataFlow(
            name="Search Service to PostgreSQL Database",
            src=self.search_service,
            dst=self.postgres_database,
            port=5432,
            protocol="SQL",
        )
        self.user_service_to_mongodb_db = DataFlow(
            name="User Service to MongoDB Database",
            src=self.user_service,
            dst=self.mongodb_database,
            port=27017,
            protocol="MongoDB",
        )
        # services to cache
        self.booking_service_to_cache = DataFlow(
            name="Booking Service to Redis Cache",
            src=self.booking_service,
            dst=self.redis_cache,
            port=6379,
            protocol="Redis",
        )
        self.user_service_to_cache = DataFlow(
            name="User Service to Redis Cache",
            src=self.user_service,
            dst=self.redis_cache,
            port=6379,
            protocol="Redis",
        )
        self.payment_service_to_cache = DataFlow(
            name="Payment Service to Redis Cache",
            src=self.payment_service,
            dst=self.redis_cache,
            port=6379,
            protocol="Redis",
        )
        self.search_service_to_cache = DataFlow(
            name="Search Service to Redis Cache",
            src=self.search_service,
            dst=self.redis_cache,
            port=6379,
            protocol="Redis",
        )
        # services to payment gateway
        self.payment_service_to_payment_gateway = DataFlow(
            name="Payment Service to Payment Gateway",
            src=self.payment_service,
            dst=self.stripe_payment_gateway,
            port=443,
            protocol="HTTPS",
        )
        # services to email service
        self.user_service_to_email_service = DataFlow(
            name="User Service to Email Service",
            src=self.user_service,
            dst=self.sendgrid_email_service,
            port=587,
            protocol="SMTP",
        )
        # services to message queue
        self.booking_service_to_mq = DataFlow(
            name="Booking Service to RabbitMQ Message Queue",
            src=self.booking_service,
            dst=self.rabbitmq,
            port=5672,
            protocol="AMQP",
        )
        self.user_service_to_mq = DataFlow(
            name="User Service to RabbitMQ Message Queue",
            src=self.user_service,
            dst=self.rabbitmq,
            port=5672,
            protocol="AMQP",
        )
        self.payment_service_to_mq = DataFlow(
            name="Payment Service to RabbitMQ Message Queue",
            src=self.payment_service,
            dst=self.rabbitmq,
            port=5672,
            protocol="AMQP",
        )
        self.search_service_to_mq = DataFlow(
            name="Search Service to RabbitMQ Message Queue",
            src=self.search_service,
            dst=self.rabbitmq,
            port=5672,
            protocol="AMQP",
        )
        # services to monitoring
        self.booking_service_to_monitoring = DataFlow(
            name="Booking Service to Splunk Monitoring",
            src=self.booking_service,
            dst=self.splunk_monitoring,
            port=8089,
            protocol="HTTPS",
        )
        self.user_service_to_monitoring = DataFlow(
            name="User Service to Splunk Monitoring",
            src=self.user_service,
            dst=self.splunk_monitoring,
            port=8089,
            protocol="HTTPS",
        )
        self.payment_service_to_monitoring = DataFlow(
            name="Payment Service to Splunk Monitoring",
            src=self.payment_service,
            dst=self.splunk_monitoring,
            port=8089,
            protocol="HTTPS",
        )
        self.search_service_to_monitoring = DataFlow(
            name="Search Service to Splunk Monitoring",
            src=self.search_service,
            dst=self.splunk_monitoring,
            port=8089,
            protocol="HTTPS",
        )
        # system admin and developer to API gateway
        self.system_admin_to_api_gateway = DataFlow(
            name="System Admin to API Gateway",
            src=self.system_admin,
            dst=self.api_gateway,
            port=443,
            protocol="HTTPS",
        )
        self.developer_to_api_gateway = DataFlow(
            name="Developer to API Gateway",
            src=self.developer,
            dst=self.api_gateway,
            port=443,
            protocol="HTTPS",
        )
        # dataflows for load balancers
        self.api_gateway_to_main_lb = DataFlow(
            name="API Gateway to Main Load Balancer",
            src=self.api_gateway,
            dst=self.main_load_balancer,
            port=80,
            protocol="HTTP",
        )
        self.main_lb_to_booking_service = DataFlow(
            name="Main Load Balancer to Booking Service",
            src=self.main_load_balancer,
            dst=self.booking_service,
            port=8080,
            protocol="HTTP",
        )
        self.main_lb_to_user_service = DataFlow(
            name="Main Load Balancer to User Service",
            src=self.main_load_balancer,
            dst=self.user_service,
            port=8080,
            protocol="HTTP",
        )
        self.main_lb_to_payment_service = DataFlow(
            name="Main Load Balancer to Payment Service",
            src=self.main_load_balancer,
            dst=self.payment_service,
            port=8080,
            protocol="HTTP",
        )
        self.main_lb_to_search_service = DataFlow(
            name="Main Load Balancer to Search Service",
            src=self.main_load_balancer,
            dst=self.search_service,
            port=8080,
            protocol="HTTP",
        )
        self.api_gateway_to_secondary_lb = DataFlow(
            name="API Gateway to Secondary Load Balancer",
            src=self.api_gateway,
            dst=self.secondary_load_balancer,
            port=80,
            protocol="HTTP",
        )
        self.secondary_lb_to_booking_service = DataFlow(
            name="Secondary Load Balancer to Booking Service",
            src=self.secondary_load_balancer,
            dst=self.booking_service,
            port=8080,
            protocol="HTTP",
        )
        self.secondary_lb_to_user_service = DataFlow(
            name="Secondary Load Balancer to User Service",
            src=self.secondary_load_balancer,
            dst=self.user_service,
            port=8080,
            protocol="HTTP",
        )
        self.secondary_lb_to_payment_service = DataFlow(
            name="Secondary Load Balancer to Payment Service",
            src=self.secondary_load_balancer,
            dst=self.payment_service,
            port=8080,
            protocol="HTTP",
        )
        self.secondary_lb_to_search_service = DataFlow(
            name="Secondary Load Balancer to Search Service",
            src=self.secondary_load_balancer,
            dst=self.search_service,
            port=8080,
            protocol="HTTP",
        )
        # dataflows for cloudfront CDN
        self.users_to_cdn = DataFlow(
            name="Users to CloudFront CDN",
            src=self.users,
            dst=self.cloudfront_cdn,
            port=443,
            protocol="HTTPS",
        )
        self.cdn_to_api_gateway = DataFlow(
            name="CDN to API Gateway",
            src=self.cloudfront_cdn,
            dst=self.api_gateway,
            port=443,
            protocol="HTTPS",
        )
        self.api_gateway_to_cdn = DataFlow(
            name="API Gateway to CDN",
            src=self.api_gateway,
            dst=self.cloudfront_cdn,
            port=443,
            protocol="HTTPS",
        )
        self.cdn_to_users = DataFlow(
            name="CDN to Users",
            src=self.cloudfront_cdn,
            dst=self.users,
            port=443,
            protocol="HTTPS",
        )

        # Populate TM object
        self.tm._actors = []
        self.tm._actors.append(self.users)
        self.tm._actors.append(self.system_admin)
        self.tm._actors.append(self.developer)

        self.tm._assets = []
        self.tm._assets.append(self.main_load_balancer)
        self.tm._assets.append(self.secondary_load_balancer)
        self.tm._assets.append(self.booking_service)
        self.tm._assets.append(self.user_service)
        self.tm._assets.append(self.payment_service)
        self.tm._assets.append(self.search_service)
        self.tm._assets.append(self.splunk_monitoring)
        self.tm._assets.append(self.api_gateway)
        self.tm._assets.append(self.postgres_database)
        self.tm._assets.append(self.mongodb_database)
        self.tm._assets.append(self.redis_cache)
        self.tm._assets.append(self.rabbitmq)
        self.tm._assets.append(self.cloudfront_cdn)
        self.tm._assets.append(self.stripe_payment_gateway)
        self.tm._assets.append(self.sendgrid_email_service)

        self.tm._flows = []
        self.tm._flows.append(self.users_to_api_gateway)
        self.tm._flows.append(self.api_gateway_to_booking_service)
        self.tm._flows.append(self.api_gateway_to_user_service)
        self.tm._flows.append(self.api_gateway_to_payment_service)
        self.tm._flows.append(self.api_gateway_to_search_service)
        self.tm._flows.append(self.booking_service_to_postgres_db)
        self.tm._flows.append(self.booking_service_to_mongodb_db)
        self.tm._flows.append(self.user_service_to_postgres_db)
        self.tm._flows.append(self.payment_service_to_postgres_db)
        self.tm._flows.append(self.search_service_to_postgres_db)
        self.tm._flows.append(self.user_service_to_mongodb_db)
        self.tm._flows.append(self.booking_service_to_cache)
        self.tm._flows.append(self.user_service_to_cache)
        self.tm._flows.append(self.payment_service_to_cache)
        self.tm._flows.append(self.search_service_to_cache)
        self.tm._flows.append(self.payment_service_to_payment_gateway)
        self.tm._flows.append(self.user_service_to_email_service)
        self.tm._flows.append(self.booking_service_to_mq)
        self.tm._flows.append(self.user_service_to_mq)
        self.tm._flows.append(self.payment_service_to_mq)
        self.tm._flows.append(self.search_service_to_mq)
        self.tm._flows.append(self.booking_service_to_monitoring)
        self.tm._flows.append(self.user_service_to_monitoring)
        self.tm._flows.append(self.payment_service_to_monitoring)
        self.tm._flows.append(self.search_service_to_monitoring)
        self.tm._flows.append(self.system_admin_to_api_gateway)
        self.tm._flows.append(self.developer_to_api_gateway)
        self.tm._flows.append(self.api_gateway_to_main_lb)
        self.tm._flows.append(self.main_lb_to_booking_service)
        self.tm._flows.append(self.main_lb_to_user_service)
        self.tm._flows.append(self.main_lb_to_payment_service)
        self.tm._flows.append(self.main_lb_to_search_service)
        self.tm._flows.append(self.api_gateway_to_secondary_lb)
        self.tm._flows.append(self.secondary_lb_to_booking_service)
        self.tm._flows.append(self.secondary_lb_to_user_service)
        self.tm._flows.append(self.secondary_lb_to_payment_service)
        self.tm._flows.append(self.secondary_lb_to_search_service)
        self.tm._flows.append(self.users_to_cdn)
        self.tm._flows.append(self.cdn_to_api_gateway)
        self.tm._flows.append(self.api_gateway_to_cdn)
        self.tm._flows.append(self.cdn_to_users)
        return super().setUp()

    def test_actor_assignment(self):
        print("Actors:")
        for actor in self.tm._actors:
            print(actor)
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
            self.postgres_database
        )
        for vector in attack_vectors:
            print(vector)
            print("\n")
        print("\n")

    def test_simulate_attack(self):
        print("Simulated Attacks:")
        simulated_attacks = self.tm.simulate_attack(self.main_load_balancer)
        for attack in simulated_attacks:
            print(attack)
            print("\n")
        print("\n")

    def tearDown(self) -> None:
        return super().tearDown()


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
        return super().setUp()

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

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
