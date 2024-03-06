# Basic Import
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet
from src.exception import CustomException
from src.logger import logger

from src.utils import save_objects
from src.utils import evaluate_model

from dataclasses import dataclass
import sys
import os

#First we need to get the model trainer path

@dataclass
class ModelTrainerConfig:

    # Get the directory path of the current script
    current_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    # Define the logs directory path relative to the main directory
    logs_directory = os.path.join(current_directory, "artifacts")

    trained_model_path_file = os.path.join(logs_directory, "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, train_array, test_array):
        try:
            logger.info('Splitting Dependent and Independent variables from train and test data')
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
            'LinearRegression':LinearRegression(),
            'Lasso':Lasso(),
            'Ridge':Ridge(),
            'Elasticnet':ElasticNet()
        }
            
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models) # In the form of dictionary

            logger.info('\n====================================================================================\n')
            logger.info(f'Model Report : {model_report}')
            logger.info('\n====================================================================================\n')

            #To get the best model score from dictionary

            best_model_score = max(sorted(model_report.values()))
            #best_model_name = [k for k,v in model_report.items() if v == best_model_score][0]
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]


            logger.info('\n====================================================================================\n')
            logger.info(f'Best Model: {best_model_name} ## Best Model Score : {best_model_score}')
            logger.info('\n====================================================================================\n')

            best_model = models[best_model_name]

            #To save the model
            save_objects(file_path = self.model_trainer_config.trained_model_path_file, 
                        obj = best_model)

        except Exception as e:
            logger.error("Error while initiating the model training")
            raise CustomException(e, sys)

