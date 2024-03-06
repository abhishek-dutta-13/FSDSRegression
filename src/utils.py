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
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)
        logger.info("pickle file loaded from: %s" % file_path)
        return obj
    except Exception as e:
        logger.error("Error while loading the pickle file: %s" % file_path)
        raise CustomException(e, sys)
    
def evaluate_model(X_train, y_train, X_test, y_test, models):
    report = {}
    try:
        logger.info("Calculating the performance metrics")
        for i in range(len(models)):
            model = list(models.values())[i]
            model.fit(X_train, y_train)

            #Make Prediction
            y_pred = model.predict(X_test)

            #Metrics:
            test_model_score = r2_score(y_test, y_pred)

            #Storing the model and r2 Score in the report dictionary:
            report[list(models.keys())[i]] = test_model_score
            logger.info("Model: %s, R2 Score: %s" % (list(models.keys())[i], test_model_score))
        logger.info("Calculating the performance metrics ends")
        return report
        
    except Exception as e:
        logger.error("Error while calculating the metrics")
        raise CustomException(e, sys)