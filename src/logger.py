import logging
import os
from datetime import datetime

"""#Create a log file
#LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H:%M:%S')}.log"
LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}.log"
logs_path=os.path.join("logs")
os.makedirs(logs_path,exist_ok=True)


LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)"""

# Get the directory path of the current script
current_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Define the logs directory path relative to the main directory
logs_directory = os.path.join(current_directory, "logs")

# Create the logs directory if it doesn't exist
os.makedirs(logs_directory, exist_ok=True)

# Define the log file path
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y %H:%M:%S')}.log"
LOG_FILE_PATH = os.path.join(logs_directory, LOG_FILE)

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
