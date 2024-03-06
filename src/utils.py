import os
import sys
import pandas as pd 
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from src.exception import CustomException
from src.logger import logger
import pickle

def save_objects(file_path, obj):
    try:
        # To make the directory, if it is not available:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        # To save the object as a pickle file:
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logger.info("pickle file saved to: %s" % file_path)
    except Exception as e:
        logger.error("Error while saving the pickle file: %s" % file_path)
        raise CustomException(e)