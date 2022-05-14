import logging
import sys

#Creating and Configuring Logger

Log_Format = "[%(asctime)s] [%(levelname)s] %(message)s"

file_handler = logging.FileHandler(filename='controller.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(format = Log_Format, 
                    level = logging.INFO,
                    handlers=handlers
)
