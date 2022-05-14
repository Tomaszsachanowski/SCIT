import time
import asyncio

from logger import logging
from controller import Controller


logger = logging.getLogger(__name__)
LOOP_TIME = 30


async def controller_job(controller):
    '''
    Async Controller Job pushing need to change running containers 
    and providing pass through whole running-dead-awaiting loop
    '''
    logger.info("[MAIN] - Started Controller Job")
    start = time.perf_counter()
    controller.loop()
    stop = time.perf_counter()
    logger.info("[MAIN] - Finished Controller Job")

    logger.info(
        "[MAIN] - Finished Controller Job in {}".format(stop -start))


async def controller_loop(controller):
    '''
    Async Controller Loop pushing Controller Jobs 
    '''
    loop = asyncio.get_event_loop()
    while True:
        await asyncio.sleep(LOOP_TIME)
        loop.create_task(controller_job(controller))


if __name__=="__main__":
    controller = Controller()
    controller.start()

    loop = asyncio.get_event_loop()

    asyncio.ensure_future(controller_loop(controller))
    loop.run_forever()
