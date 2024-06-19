from threading import Lock, Thread
import time

from concurrent import futures

import grpc

import naturalengine_pb2_grpc


from tmnpy.dsl import TM, Actor, Boundary
from tmnpy.dsl.asset import ExternalEntity, Datastore, Machine, DATASTORE_TYPE
from tmnpy.engines import Engine


class NaturalEngineMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class NaturalEngine(metaclass=NaturalEngineMeta):

    """
    NatrualEngine is the system that tracks
    """

    def __init__(
        self,
        currentFocus: "None",
    ):
        self.currentFocus = currentFocus
        self.previous_events = []
        self.lastevent = time.time()


class NaturalEngineService(naturalengine_pb2_grpc.NaturalEngineServicer):
    def __init__(
        self,
        engine: NaturalEngine,
    ):
        self.naturalengine = engine

    def NewEvent(self, request, context):
        # Get the event and check what type it is, then plug into markov model to predict new focus.  Update list of previous events to include this.
        event = request.event_type


def serve():
    engine = NaturalEngine("None")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    naturalengine_pb2_grpc.add_NaturalEngineServicer_to_server(
        NaturalEngineService(engine), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
