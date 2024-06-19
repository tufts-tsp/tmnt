from threading import Lock, Thread
import time

from concurrent import futures

import grpc

from controller_pb2 import (
    Machine,
    Datastore_Type,
    Empty,
    Status,
    Status_Code,
    Actor,
    GetActorsResponses,
    Boundary,
    GetBoundariesResponses,
    AssetResponse,
    GetAssetsResponses,
    ExternalAssetResponse,
    GetExternalAssetsResponses,
    DatastoreResponse,
    GetDatastoreResponses,
    ProcessResponse,
    GetProcessResponses,
)
import controller_pb2_grpc


from tmnpy.dsl import TM, Actor, Boundary
from tmnpy.dsl.asset import ExternalEntity, Datastore, Machine, DATASTORE_TYPE
from tmnpy.engines import Engine


class TMNTControllerMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class TMNTController(metaclass=TMNTControllerMeta):

    """
    TMNTController is what starts a TMNT threat modeling session. Your
    initialized threat model will be empty by default, or you can specify a
    file path for your YAML configuration file
    (see `examples.parser_examples`).
    You can initialize with a set of Engines or you can add them
    later, by default it uses just the basic Assignment engine. Additionally,
    if you have any reference threat models that you want to compare against,
    you can add them with `references`.
    """

    def __init__(
        self,
        name: str,
        config_file: str = "",
        engines: Engine | list[Engine] = Engine(),
        references: None | TM | list[TM] = None,
    ):
        self.created = time.time()
        self.lastmodified = time.time()
        self.tm = TM(name)
        if config_file != "":
            # parse config and add to `self.tm`
            pass
        self.engines = engines
        self.references = references


class ControllerService(controller_pb2_grpc.ControllerServicer):
    def __init__(
        self,
        control: TMNTController,
    ):
        self.controller = control

    def AddExternalAsset(self, request, context):
        # check first to see if the actor or boundary already exist. If no, create a new ones.
        actor = Actor(
            request.trust_boundary[0].boundary_owner.name,
            request.trust_boundary[0].boundary_owner.actor_type,
            request.trust_boundary[0].boundary_owner.physical_access,
        )
        boundary = Boundary(request.trust_boundary[0].name, actor)
        open_ports = []
        for port in request.open_port:
            open_ports.append(port)
        trust_boundaries = [boundary]

        machine = Machine.PHYSICAL
        if request.machine == 1:
            machine = Machine.VIRTUAL
        elif request.machine == 2:
            machine = Machine.CONTAINER
        elif request.machine == 3:
            machine = Machine.SERVERLESS

        asset = ExternalEntity(
            name=request.name,
            physical_access=request.physical_access,
            open_ports=open_ports,
            trust_boundaries=trust_boundaries,
            machine=machine,
        )
        self.controller.tm.add_component(asset)
        status = Status(code=Status_Code.SUCCESS)
        return status

    def AddDatastore(self, request, context):
        # check first to see if the actor or boundary already exist. If no, create a new ones.
        actor = Actor(
            request.trust_boundary[0].boundary_owner.name,
            request.trust_boundary[0].boundary_owner.actor_type,
            request.trust_boundary[0].boundary_owner.physical_access,
        )
        boundary = Boundary(request.trust_boundary[0].name, actor)
        open_ports = []
        for port in request.open_port:
            open_ports.append(port)
        trust_boundaries = [boundary]

        machine = Machine.PHYSICAL
        if request.machine == 1:
            machine = Machine.VIRTUAL
        elif request.machine == 2:
            machine = Machine.CONTAINER
        elif request.machine == 3:
            machine = Machine.SERVERLESS

        datastore_type = DATASTORE_TYPE.UNKNOWN
        if request.ds_type == 1:
            datastore_type = DATASTORE_TYPE.FILE_SYSTEM
        elif request.ds_type == 2:
            datastore_type = DATASTORE_TYPE.SQL
        elif request.ds_type == 3:
            datastore_type = DATASTORE_TYPE.LDAP
        elif request.ds_type == 4:
            datastore_type = DATASTORE_TYPE.BUCKET
        elif request.ds_type == 5:
            datastore_type = DATASTORE_TYPE.OTHER
        elif request.ds_type == 6:
            datastore_type = DATASTORE_TYPE.NOSQL

        asset = Datastore(
            name=request.name,
            open_ports=open_ports,
            trust_boundaries=trust_boundaries,
            machine=machine,
            ds_type=datastore_type,
        )
        self.controller.tm.add_component(asset)
        status = Status(code=Status_Code.SUCCESS)
        return status

    def AddActor(self, request, context):
        actor = Actor(
            request.name, request.actor_type, request.physical_access
        )
        self.controller.tm.add_actor(actor)
        status = Status(code=Status_Code.SUCCESS)
        return status

    def AddBoundary(self, request, context):
        actor = Actor(
            request.trust_boundary.boundary_owner.name,
            request.trust_boundary.boundary_owner.actor_type,
            request.trust_boundary.boundary_owner.physical_access,
        )
        boundary = Boundary(request.trust_boundary.name, actor)
        self.controller.tm.add_component(boundary)
        status = Status(code=Status_Code.SUCCESS)
        return status

    def Import(self, request, context):
        # call the parser function on request.input_file to install a new threat model from a yaml file
        status = Status(Status_Code.SUCCESS)
        return status

    def Export(self, request, context):
        # save the current threat model object to a yaml file with the file name given by request.output_file
        status = Status(Status_Code.SUCCESS)
        return status


def serve():
    controller = TMNTController("default", "", None, None)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    controller_pb2_grpc.add_ControllerServicer_to_server(
        ControllerService(controller), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
