import os
import logging
from datetime import datetime

from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #directory will be created for logging the code in current time stamp

logs_path = os.path.join(from_root(), "logs", LOG_FILE)  #path will be created

os.makedirs(logs_path, exist_ok=True) #logs directory is made

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,  #log file name
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)