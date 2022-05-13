import asyncio
import functools
from traceback import print_tb
import requests
import signal
import subprocess
import sys
import time

import docker

from container import Container


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
        for container in self.docker_client.containers.list(
            filters={"name":"shopapp*"}, all=True):
            self.__live_spare.append(Container(container=container))

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

if __name__=="__main__":
   a =  Controller()
   a.start()