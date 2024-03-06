import os # We use os to create path...
import sys
from src.logger import logger
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass  # dtaclass, we create directly create variable names, we dont need to write __init__ method


## Initialize the Data Ingetion Configuration
# --init__ is used when we are creating functions. However, here we will just initialize the variables

@dataclass
class DataIngetionconfig:
        # Get the directory path of the current script
    current_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    # Define the logs directory path relative to the main directory
    logs_directory = os.path.join(current_directory, "artifacts")


    train_data_path:str = os.path.join(logs_directory, "train.csv")
    test_data_path:str = os.path.join(logs_directory, "test.csv")
    raw_data_path:str = os.path.join(logs_directory, "raw.csv")

# Create a class for Data Ingetion
class DataIngetion:
    def __init__(self):
        self.ingetion_config = DataIngetionconfig() #Tuple of three
    
    def initiate_data_ingetion(self):
        logger.info("Data Ingetion methods starts")
        try:
            #read data
            #df = pd.read_csv("/Users/abhishek/Desktop/iNeuron/Machine Learning/Linear Regression/Linear_Regression_End_to_End/notebooks/gemstone.csv")
            
            df = pd.read_csv(os.path.join("/Users/abhishek/Desktop/iNeuron/Machine Learning/Linear Regression/Linear_Regression_End_to_End/notebooks", "gemstone.csv")) #reading the data from the data directory
            logger.info("Dataset read successfully")

            #make my directory
            #os.makedirs is used to create a directory
            #exist_ok -> If the directory is present then dont create else create
            os.makedirs(os.path.dirname(self.ingetion_config.raw_data_path), exist_ok=True) 
            
            df.to_csv(self.ingetion_config.raw_data_path, index=False) #index = False -> not to create a seprate index

            #train test split
            logger.info("Train test split starts")
            train_set, test_set = train_test_split(df, test_size=0.3, random_state=42)
            logger.info("Train test split ends")

            #Inserting the train and test data into artifacts directory
            logger.info("Inserting the train and test data into artifacts directory")
            train_set.to_csv(self.ingetion_config.train_data_path, header=True, index=False)
            test_set.to_csv(self.ingetion_config.test_data_path, header=True, index=False)
            logger.info("Inserting the train and test data into artifacts directory ends")

            logger.info("Data Ingetion methods ends")

            return (
                self.ingetion_config.train_data_path,
                self.ingetion_config.test_data_path
            )

        except Exception as e:
            logger.info("Exception occured in Data Ingetion methods")
            raise CustomException(e, sys)
