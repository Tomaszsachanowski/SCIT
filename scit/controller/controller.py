import asyncio
import functools
from traceback import print_tb
import requests
import signal
import subprocess
import sys
import time

import docker

from container import GRACE_PERIOD, Container


GRACE_PERIOD_TIME = 10

class Controller:
    '''
    A class that acts as a SCIT controller
    '''

    def __init__(self):
        # Connect to docker engine
        self.docker_client = docker.from_env()
        # State list of controller holding shop app containers
        self.__activate = []
        self.__grace_period = []
        self.__inactivate = []
        self.__live_spare = []
        self.__all_shpp_app = []
        for container in self.docker_client.containers.list(filters={"name":"shopapp*"},
                                                            all=True):
            con = Container(container=container)
            self.__live_spare.append(con)
            self.__all_shpp_app.append(con)

        # Reference to NGINX Container
        self.__nginx = self.docker_client.containers.get("scit_nginx_1")
        print(self.__nginx.name)

        # Reference to MySQL database Container
        self.__my_sql = self.docker_client.containers.get("mysql-8_0")
        print(self.__my_sql.name)

        # Reference to redis Container
        self.__redis = self.docker_client.containers.get("scit_redis_1")
        print(self.__redis.name)

    def start(self):
        '''
        Method runs the necessary containers and exactly one application.
        Provides SCIT clean state.
        '''
        # Start MySQL, NGINX and REDIS container
        self.__my_sql.start()
        self.__nginx.start()
        self.__redis.start()
        print("SSS", self.__live_spare, self.__activate)
        # Start first live spare shop app container
        con = self.__live_spare.pop(0)
        con.start()
        self.__activate.append(con)

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

    def state_one(self):
        '''
        Set first live spare container into active state  
        '''
        print("[Controller] - State one for start")
        con = self.__live_spare.pop(0)
        con.start()
        self.__activate.append(con)
        print("[Controller] - State one for {} completed".format(con))

    def state_two(self):
        '''
        Set previously running container into grace period state  
        '''
        print("[Controller] - State two for start")

        con = self.__activate.pop(0)
        self.__grace_period.append(con)

        # Send stop signal to docker engine
        con.stop(timeout=GRACE_PERIOD_TIME)
        print("[Controller] - State two for {} completed".format(con))

    def state_three(self):
        '''
        Remove container and push reference to dead state
        '''
        print("[Controller] - State three for start")

        con = self.__grace_period.pop(0)
        con.remove()
        self.__inactivate.append(con)
        print("[Controller] - State tree for {} completed".format(con))

    def state_four(self):
        '''
        Try to start all in1activate django containers using docker-compose
        '''
        print("[Controller] - State four for start")

        while len(self.__inactivate) != 0:
            con = self.__inactivate.pop(0)
            con.restore()
            self.__live_spare.append(con)
        print("[Controller] - State four for {} completed".format(con))

if __name__=="__main__":
   a =  Controller()
   a.start()
   a.state_one()
   time.sleep(12)
   a.state_two()       
   time.sleep(12)
   a.state_three()
   time.sleep(12)
   a.state_four()
   time.sleep(12)
   print("Koniec 1")
   time.sleep(30)

   a.state_one()
   time.sleep(12)
   a.state_two()       
   time.sleep(12)
   a.state_three()
   time.sleep(12)
   a.state_four()
   time.sleep(12)

   print("Koniec 2")

   time.sleep(30)

   a.state_one()
   time.sleep(12)
   a.state_two()       
   time.sleep(12)
   a.state_three()
   time.sleep(12)
   a.state_four()
   print("Koniec 3")
   time.sleep(30)
   a.stop()
