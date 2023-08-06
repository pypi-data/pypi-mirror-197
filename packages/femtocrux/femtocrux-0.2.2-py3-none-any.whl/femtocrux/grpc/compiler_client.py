from collections.abc import Iterable
from dataclasses import dataclass
import docker
from enum import Enum
import grpc
import logging
import numpy as np
import os
import pickle
import queue
import socket
import sys
from getpass import getpass
from typing import Any, List

from fmot.fqir import GraphProto
import femtocrux

from utils import numpy_to_ndarray, ndarray_to_numpy

# GRPC artifacts
import compiler_service_pb2 as cs_pb2
import compiler_service_pb2_grpc as cs_pb2_grpc

class Model:
    def get_message(self) -> cs_pb2.model:
        """
            Subclass overrides this to implement the model's grpc message.
        """
        raise NotImplementedError("Must be defined by subclass")

@dataclass
class FQIRModel(Model):
    graph_proto: GraphProto = None
    batch_dim: int = None
    sequence_dim: int = None

    def get_message(self) -> cs_pb2.model:
        # Serialize FQIR via pickle
        model = pickle.dumps(self.graph_proto)

        # Send the serialized model
        return cs_pb2.model(
            fqir = cs_pb2.fqir(
                model = model,
                batch_dim = self.batch_dim,
                sequence_dim = self.sequence_dim,
            )
        )

@dataclass
class TFLiteModel(Model):
    flatbuffer: bytes = None
    signature_name: str = None

    def get_message(self) -> cs_pb2.model:
        return cs_pb2.model(
            tflite = cs_pb2.tflite(
                model = self.flatbuffer,
                signature_name = self.signature_name
            )
        )

class Simulator():
    def __init__(self, client: "CompilerClient", model: Model):
        self.client = client
        self.model = model

        # Create an event stream fed by a queue
        self.request_queue = queue.SimpleQueue()
        request_iterator = iter(
            self.request_queue.get, 
            self.__request_sentinel__
        ) 
        self.response_iterator = client.__simulate__(request_iterator)
 
        # Compile the model with the first message
        model_msg = model.get_message()
        simulation_start_msg = cs_pb2.simulation_input(
            model = model_msg
        )
        self.__send_request__(simulation_start_msg)

        # Check compilation status
        self.__get_response__()

    def __del__(self):
        """ Close any open streams. """
        self.__send_request__(self.__request_sentinel__)

    def __send_request__(self, msg):
        self.request_queue.put(msg)

    def __get_response__(self):
        response = next(self.response_iterator)
        self.client.__check_status__(response.status)
        return response

    @property
    def __request_sentinel__(self) -> Any:
        """ Sentinel value to close the request queue. """
        return None

    def simulate(self, inputs: List[np.array], quantize_inputs: bool = False, dequantize_outputs: bool = False) -> List[np.array]:
        #TODO how to handle multiple inputs? What's the proper form for FASMIR? Map inputs to FASMIR indices as in CompilerFrontend?
        simulation_request = cs_pb2.simulation_input(
            data = cs_pb2.simulation_data(
                data = [numpy_to_ndarray(x) for x in inputs],
                quantize_inputs = quantize_inputs,
                dequantize_outputs = dequantize_outputs
            )
        )
        self.__send_request__(simulation_request)
        response = self.__get_response__()

        return [ndarray_to_numpy(x) for x in response.data]

class CompilerClientImpl:
    """ 
    Internal implementation of CompilerClient, with extra testing options. 

    Allows substituting your own gRPC channel and stub.
    """
    def __init__(self, channel, stub, wait_for_ready: bool = False, 
            fake_server: bool = False):
        self.channel = channel
        self.stub = stub

        self.rpc_kwargs = {}
        if wait_for_ready:
            # 'wait_for_ready' is not recognized by 'pytest --grpc-fake-server'
            self.rpc_kwargs['wait_for_ready'] = wait_for_ready

    def __check_status__(self, status):
        """ Check a status response, raising an exception if unsuccessful. """
        if not status.success:
            raise RuntimeError("Client received error from compiler server:\n%s" % status.msg)

    def compile(self, model: Model) -> bytes: 
        response = self.stub.compile(
            model.get_message(), 
            **self.rpc_kwargs
        )
        self.__check_status__(response.status)
        return response.bitfile

    def __simulate__(self, in_stream: Iterable) -> Iterable:
        """ Calls the 'simulator' bidirectional streaming RPC. """
        return self.stub.simulate(
            in_stream, 
            **self.rpc_kwargs
        )

    def simulate(self, model: Model) -> Simulator:
        return Simulator(client = self, model = model)

class CompilerClient(CompilerClientImpl):
    """
    User-facing compiler client class.
    Configures the client and server for production use.
    """
    def __init__(self, start_server: bool = True):
        self.container = None
        self.sock = None
        # Optionally, start a new docker server
        if start_server:
            self.container = self.__create_docker_server__()
            self.__init_channel_info_container__(self.container)
        else:
            # Debugging mode: open a socket to localhost.
            # Does not start a server.
            self.sock = self.__init_channel_info_socket__()

        # Set the maximum message size
        megabyte_size = 2 ** 20
        max_message_size = 32 * megabyte_size

        # Open a gRPC channel to the docker
        sock_name = '%s:%s' % (self.channel_addr, self.channel_port)
        self.channel = grpc.insecure_channel(
            sock_name,
            options = [
                  ('grpc.max_send_message_length', max_message_size),
                  ('grpc.max_receive_message_length', max_message_size)
            ],
        )
        logging.info("Created gRPC channel at %s" % sock_name)

        # Initialize the client on this channel.
        # Note: this blocks RPCs until ready.
        self.stub = cs_pb2_grpc.CompileStub(self.channel)
        super().__init__(self.channel, self.stub, wait_for_ready=True)

    def __del__(self):
        """ Reclaim system resources. """
        if self.container is not None:
            self.container.kill()
            self.container = None

    def __del__(self):
        """ Reclaim system resources. """
        if self.container is not None:
            self.container.kill()
            self.container = None

    def __get_docker_api_client__(self):
        """ Get a client to the Docker daemon. """
        return docker.from_env()

    def __init_channel_info_socket__(self):
        """
        For local connections only.

        Opens a socket to communicate with localhost.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        self.__channel_addr__, self.__channel_port__ = sock.getsockname()
        self.sock = sock
        return sock

    def __init_channel_info_container__(self, container):
        """
        For local connections only.

        Gets the IP address and port of the container.
        """
        self.__channel_port__ = self.container_port

        # Get the network info
        network_name = 'bridge'
        client = self.__get_docker_api_client__()
        network = client.networks.get(network_name)

        # Search for this container in the network
        network_containers = network.attrs['Containers']
        try:
            container_info = network_containers[container.id]
        except KeyError:
            raise OSError(
                "Failed to find container '%s' on network '%s'.\nFound options:\n\t%s" % (
                container.id, network_name, container_info
                )
            )

        # Extract the IP address of this container
        container_ip = container_info['IPv4Address'].split('/')[0]
        self.__channel_addr__ = container_ip

    @property
    def __docker_image_name__(self) -> str:
        """
        Returns the docker image name. For testing, override with the
        FEMTOCRUX_SERVER_IMAGE_NAME environment variable.
        """
        try:
            return os.environ["FEMTOCRUX_SERVER_IMAGE_NAME"]
        except KeyError:
            return "femtocrux:" + femtocrux.__version__

    @property
    def channel_addr(self) -> str:
        return self.__channel_addr__

    @property
    def channel_port(self) -> int:
        """
        Port used for the gRPC channel, whether container or local socket.
        """
        return self.__channel_port__

    @property
    def container_port(self) -> int:
        """ Port used for containers. """
        return 50051

    @property
    def __container_label__(self) -> str:
        """ Label attached to identify containers started by this client. """
        return 'femtocrux_server'

    def __get_unused_container_name__(self) -> str:
        """ Get an unused container name. """
        basename = 'femtocrux_server_'

        # Search for an unused name
        client = self.__get_docker_api_client__()
        container_idx = 0
        while True:
            name = 'femtocrux_server_%d' % container_idx
            try:
                client.containers.get(name)
            except docker.errors.NotFound:
                # If no collision, use this name
                return name

            container_idx += 1

    def __create_docker_server__(self) -> docker.models.containers.Container:
        """
        Starts the server in a new Docker container.
        """
        # Get a client for the Docker daemon
        client = self.__get_docker_api_client__()

        # Pull the image, if not available
        existing_image_names = [tag for image in client.images.list() for tag in image.tags]
        if self.__docker_image_name__ not in existing_image_names:
            logging.info('Failed to find the docker image %s locally.', self.__docker_image_name__)
            fetching = True
            while fetching:
                try:
                    REGISTRY = "ghcr.io"
                    ORG = "femtosense"
                    logging.info('Attempting to download %s from remote.', self.__docker_image_name__)
                    if "GH_PACKAGE_KEY" in os.environ:
                        password = os.environ["GH_PACKAGE_KEY"]
                    else:
                        password = getpass("Please enter your Femtosense-provided key:")
                    resp = client.login("femtodaemon", password, registry="https://" + REGISTRY)
                    logging.info(resp['Status'])
                    logging.info("Downloading image")
                    image = client.images.pull(REGISTRY + '/' + ORG + '/' + self.__docker_image_name__)
                    image.tag("femtocrux", femtocrux.__version__)
                    fetching = False
                except KeyboardInterrupt:
                    logging.info("Password entry interrupted")
                    raise
                except docker.errors.ImageNotFound as exc:
                    logging.warn("Docker image not found. Please notify your Femtosense representative.")
                    raise RuntimeError("Docker image not found. Please notify your Femtosense representative.") from exc
                except docker.errors.APIError as exc:
                    if exc.explanation == "manifest unknown":
                        logging.warn("Docker image %s not found on the remote. Check if it is published.", self.__docker_image_name__)
                        raise RuntimeError("Docker image {} not found. Please notify your Femtosense representative.".format(self.__docker_image_name__))
                    elif 'denied' in exc.explanation:
                        logging.warn("Docker authetication failed. Try again.")

        # Start a container running the server
        command = "--port %s" % self.container_port
        container = client.containers.run(
            self.__docker_image_name__,
            command=command, # Appends entrypoint with args 
            detach=True,
            labels=[self.__container_label__],
            stderr=True,
            stdout=True,
            name=self.__get_unused_container_name__(),
            auto_remove=True,
        )

        # Check if the container is running
        try:
            top = container.top()
        except:
            raise RuntimeError("Failed to start docker container (status: %s)" % container.status)
        assert len(top['Processes']) > 0, "Docker container is idle"

        return container

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    client = CompilerClient()
    logging.info('Client started successfully.')
