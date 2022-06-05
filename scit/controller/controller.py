from container import Container
from logger import logging
from time import sleep


GRACE_PERIOD_TIME = 15
class Controller:
    '''
    A class that acts as a SCIT controller
    '''

    def __init__(self):
        # State list of controller holding shop app containers
        self.__activate = []
        self.__grace_period = []
        self.__inactivate = []
        self.__live_spare = []
        self.__all_shpp_app = []

        for container in Container.docker_client.containers.list(
            filters={"name":"shopapp*"},all=True):

            con = Container(container=container)
            self.__live_spare.append(con)
            self.__all_shpp_app.append(con)

        # Reference to NGINX Container
        self.__nginx = Container.docker_client.containers.get("scit_nginx_1")

        # Reference to MySQL database Container
        self.__my_sql = Container.docker_client.containers.get("mysql-8_0")

        # Reference to redis Container
        self.__redis = Container.docker_client.containers.get("scit_redis_1")

    def start(self):
        '''
        Method runs the necessary containers and exactly one application.
        Provides SCIT clean state.
        '''
        # Start MySQL, NGINX and REDIS container
        self.__my_sql.start()
        self.__nginx.start()
        self.__redis.start()
        # Start first live spare shop app container
        con = self.__live_spare.pop(0)
        con.start()
        self.__activate.append(con)
        self.logger.info("[CONTROLLER] - Start controller".format())

    def stop(self):
        '''
        Method to stop containers and controller
        '''
        # stop NGINX container
        self.__nginx.start()

        for con in self.__all_shpp_app:
            con.stop()

        # stop MySQL and REDIS container
        self.__redis.start()
        self.__my_sql.start()
        self.logger.info("[CONTROLLER] - Stop controller".format())

    def __activate_state(self):
        '''
        Set first live spare container into active state  
        '''
        self.logger.info("[CONTROLLER] - activate state start".format())
        con = self.__live_spare.pop(0)
        con.start()
        self.__activate.append(con)
        self.logger.info(
                "[CONTROLLER] - activate state for {} completed".format(con))

    def __grace_period_state(self):
        '''
        Set previously running container into grace period state  
        '''
        self.logger.info("[CONTROLLER] - grace period state start".format())
        con = self.__activate.pop(0)
        self.__grace_period.append(con)

        # Send stop signal to docker engine
        con.stop(timeout=GRACE_PERIOD_TIME)
        self.logger.info(
                "[CONTROLLER] - grace period state for {} completed".format(con))

    def __inactivate_state(self):
        '''
        Remove container and push reference to dead state
        '''
        self.logger.info("[CONTROLLER] - inactivate state start".format())
        con = self.__grace_period.pop(0)
        con.remove()
        self.__inactivate.append(con)
        self.logger.info(
                "[CONTROLLER] - inactivate state for {} completed".format(con))

    def __restore_state(self):
        '''
        Try to start all in1activate django containers using docker-compose
        '''
        self.logger.info("[CONTROLLER] - restore state start".format())
        while len(self.__inactivate) != 0:
            con = self.__inactivate.pop(0)
            con.restore()
            self.__live_spare.append(con)
            self.logger.info(
                "[CONTROLLER] - restore state for {} completed".format(con))
        self.logger.info(
            "[CONTROLLER] - restore state all completed")


    def loop(self):
        self.__activate_state()
        sleep(3) # We have to be sure that the HTTP server has launched... :(
        self.logger.info("[CONTROLLER] - sleep 3")
        self.__grace_period_state()
        self.__inactivate_state()
        self.__restore_state()

    @property
    def logger(self):
        return logging.getLogger(__name__)
