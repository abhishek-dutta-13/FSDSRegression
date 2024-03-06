import os # We use os to create path...
import sys
from src.logger import logger
from src.exception import CustomException
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer ## HAndling Missing Values
from sklearn.preprocessing import StandardScaler # HAndling Feature Scaling
from sklearn.preprocessing import OrdinalEncoder # Ordinal Encoding for categorical variables
## pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer #Group everything together
from dataclasses import dataclass
from src.utils import save_objects

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join("../src","artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()  # Creating object of DataTransformationConfig class

    def get_data_transformation_objects(self):
        try:
            logger.info("Data Transformation methods starts")

            #Getting numerical columns:
            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']

            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logger.info("Pipeline Initiated")

            ##Numerical Pipeline
            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")), #Handle Null Values
                    ("scaler", StandardScaler()), #Handle Feature Scaling
                ]
            )
            ##Categorical Pipeline
            cat_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")), #null values with most frequent
                    ("ordinalencoder", OrdinalEncoder(categories=[cut_categories, color_categories, clarity_categories])), #Handle Categorical Variables
                    ("scaler", StandardScaler()), #Handle Feature Scaling (z-Score)
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols)
                ]
            )
            logger.info("Pipeline methods creation ends")
            return preprocessor
    
        except Exception as e:
            logger.info("Error occured in get_data_transformation_objects method")
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            logger.info("Data Transformation methods starts")
            df_train = pd.read_csv(train_path)
            df_test = pd.read_csv(test_path)
            logger.info("Data Read successfully")
            logger.info(f"Train Data Frame Head: \n{df_train.head().to_string()}")
            logger.info(f"Test Data Frame Head: \n{df_test.head().to_string()}")

            target_column_name = "price"
            drop_columns = [target_column_name, "id"]

            logger.info("Input and Output Feature distribution to start")

            preprocessing_obj = self.get_data_transformation_objects()
            # Input feature for train and test
            input_feature_train_df = df_train.drop(drop_columns, axis=1)
            input_feature_test_df = df_test.drop(drop_columns, axis=1)

            # Target feature for train and test
            target_feature_train_df = df_train[target_column_name]
            target_feature_test_df = df_test[target_column_name]

            logger.info("Input and Output Feature distribution Successfulll")


            logger.info("Applying preprocessing object on training and test data")

            

            #transformation using preprocessing object
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            logger.info("Data TPreprocessing Successfulll")

            # This step is used to reduce time as it will read via array:
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logger.info("train and test array created Successfullly")

            # We can apply ML Algo in numpy array as well and it is super fast with comparison to Pandas df

            ## We need to save the pickle file preprocessing_obj to be used in future. This is done in utils.py ##

            save_objects(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj

                )
            logger.info("saved the pickle file preprocessing_obj to: %s" % self.data_transformation_config.preprocessor_obj_file_path)
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        
        except Exception as e:
            logger.info("Error occured in initiate_data_transformation method")
            raise CustomException(e, sys)