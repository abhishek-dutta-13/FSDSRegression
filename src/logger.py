import logging
import os
from datetime import datetime

#Create a log file
#LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H:%M:%S')}.log"
LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}.log"
logs_path=os.path.join("../src","logs")
os.makedirs(logs_path,exist_ok=True)


LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

#Custom Logger 
logger = logging.getLogger("Regression")
logger.setLevel(logging.DEBUG)

#Create Handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(LOG_FILE_PATH)

c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

#Create formatter and add to handler
c_format = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
f_format = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

#Add handler
logger.addHandler(c_handler)
logger.addHandler(f_handler)
