import time


from container import Container
from logger import logging


GRACE_PERIOD_TIME = 30

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

    def state_one(self):
        '''
        Set first live spare container into active state  
        '''
        self.logger.info("[CONTROLLER] - State one start".format())
        con = self.__live_spare.pop(0)
        con.start()
        self.__activate.append(con)
        self.logger.info(
                "[CONTROLLER] - State one for {} completed".format(con))

    def state_two(self):
        '''
        Set previously running container into grace period state  
        '''
        self.logger.info("[CONTROLLER] - State two start".format())
        con = self.__activate.pop(0)
        self.__grace_period.append(con)

        # Send stop signal to docker engine
        con.stop(timeout=GRACE_PERIOD_TIME)
        self.logger.info(
                "[CONTROLLER] - State two for {} completed".format(con))

    def state_three(self):
        '''
        Remove container and push reference to dead state
        '''
        self.logger.info("[CONTROLLER] - State three start".format())
        con = self.__grace_period.pop(0)
        con.remove()
        self.__inactivate.append(con)
        self.logger.info(
                "[CONTROLLER] - State three for {} completed".format(con))

    def state_four(self):
        '''
        Try to start all in1activate django containers using docker-compose
        '''
        self.logger.info("[CONTROLLER] - State four start".format())
        while len(self.__inactivate) != 0:
            con = self.__inactivate.pop(0)
            con.restore()
            self.__live_spare.append(con)
            self.logger.info(
                "[CONTROLLER] - State four for {} completed".format(con))
        self.logger.info(
            "[CONTROLLER] - State four all completed".format())
    @property
    def logger(self):
        return logging.getLogger(__name__)

if __name__=="__main__":
   a =  Controller()
   a.start()
   a.state_one()
   time.sleep(2)
   a.state_two()       
   time.sleep(2)
   a.state_three()
   time.sleep(2)
   a.state_four()
   time.sleep(2)
   print("Koniec 1")
   time.sleep(30)

   a.state_one()
   time.sleep(2)
   a.state_two()       
   time.sleep(2)
   a.state_three()
   time.sleep(2)
   a.state_four()
   time.sleep(2)

   print("Koniec 2")

   time.sleep(35)

   a.state_one()
   time.sleep(2)
   a.state_two()       
   time.sleep(2)
   a.state_three()
   time.sleep(2)
   a.state_four()
   print("Koniec 3")
   time.sleep(35)
   a.stop()
