# Virtual machine is online and accepts/processes any incoming requests.
ACTIVATE = 'ACTIVATE'
# Virtual machine processes any existing requests, but does not accept any new requests.
GRACE_PERIOD = 'GRACE PERIOD'
# Virtual machine is offline.
INACTIVATE = 'INACTIVATE'
# Virtual machine has been restored to pristine state and is ready to come on-line.
LIVE_SPARE = 'LIVE SPARE'


ALL_STATES = frozenset({ACTIVATE, GRACE_PERIOD, INACTIVATE, LIVE_SPARE})
class Container:
    '''
    A class that stores information about a container.
    '''
    def __init__(self, name, image, compose_name):
        # Container Name
        self.name = name

        # Image Name
        self.image = image

        # Name in docker-compose file
        self.compose_name = compose_name

        # Status
        self.__status = LIVE_SPARE

    def __str__(self):
        return "Container: {} Status: {}".format(self.name, self.__status)

    def next_status(self):
        if self.__status == ACTIVATE:
            self.__status = GRACE_PERIOD
        elif self.__status == GRACE_PERIOD:
            self.__status = INACTIVATE
        elif self.__status == INACTIVATE:
            self.__status = LIVE_SPARE
        elif self.__status == LIVE_SPARE:
            self.__status = ACTIVATE
