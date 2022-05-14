import subprocess
import docker

from logger import logging


# Virtual machine is online and accepts/processes any incoming requests.
ACTIVATE = 'ACTIVATE'
# Virtual machine processes any existing requests, but does not accept any new requests.
GRACE_PERIOD = 'GRACE PERIOD'
# Virtual machine is offline.
INACTIVATE = 'INACTIVATE'
# Virtual machine has been restored to pristine state and is ready to come on-line.
LIVE_SPARE = 'LIVE SPARE'


ALL_STATES = frozenset({ACTIVATE, GRACE_PERIOD, INACTIVATE, LIVE_SPARE})

DOCKER_COMPSE_FILE = "../docker-compose.yaml"

class Container:
    '''
    A class that stores information about a container.
    '''
    # Connect to docker engine
    docker_client =  docker.from_env()


    def __init__(self, container):

        # Container Name
        self.__name = container.name

        # Name in docker-compose file
        self.__compose_name = container.name.split('_')[1]

        container.stop()# Stop shop app container. To be sure

        # Status
        self.__status = LIVE_SPARE
        self.logger.info("[CONTAINER] Init {}".format(self))

    def __str__(self):
        return "Container: {} Status: {}".format(self.__name, self.__status)

    @property
    def container(self):
        return Container.docker_client.containers.get(self.__name)

    def start(self):
        self.container.start()
        self.__status = ACTIVATE
        self.logger.info("[CONTAINER] Start {}".format(self))


    def stop(self, timeout=None):
        self.container.stop(timeout=timeout)
        self.__status = GRACE_PERIOD
        self.logger.info("[CONTAINER] Stop {}".format(self))


    def remove(self):
        self.container.remove(v=True)
        self.__status = INACTIVATE
        self.logger.info("[CONTAINER] Remove {}".format(self))

    def restore(self):
        # Use docker-compose as it has defined all important data to run image
        subprocess.run(["docker-compose",  "-f", DOCKER_COMPSE_FILE,
                        "create", "--build", self.__compose_name])
        self.__status = LIVE_SPARE
        self.logger.info("[CONTAINER] Restore {}".format(self))

    @property
    def logger(self):
        return logging.getLogger(__name__)

