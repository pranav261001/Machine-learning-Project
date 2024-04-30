# Logging is used to keep track of all the execution thats happens all the information of that execution will be logged in this file 
#  used to record activities that occur within a program

import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # file name
logs_path = os.path.join(os.getcwd(),'log',LOG_FILE) # specifies the path

os.makedirs(logs_path, exist_ok=True) # creates folder at the specified path
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) # joing both
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,    #--|-- line no.
)

# This will create a log file and will get stired in the current working directory with the name 'log'4

# Demo
# if __name__ == "__main__":
#     logging.info("Logging has started")
