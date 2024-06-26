# All the code related to transformation - encoding, categorial cal to numerical like that
import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # creates a pipelines
from sklearn.impute import SimpleImputer # used to fill missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object




class DataTransformationConfig:
    preprocessor_file_path = os.path.join("artifacts", 'preprocessor.pkl')

class DataTransformation(DataTransformationConfig):

    def get_data_transformation_object(self):
        ''' This function is responsible to perform transformation on different types of data 
        '''
        
        try:
            numerical_features = ["reading_score", "writing_score"]
            categorical_features = [
                "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"
            ]

            num_pipeline = Pipeline(
                steps= [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Numerical & Categorical Pipeline's created")

#           This is used to combine both the pipelines and allocate columns for them 
            preprocessor = ColumnTransformer(
                [("num_pipeline", num_pipeline, numerical_features),
                ("cat_pipeline", cat_pipeline, categorical_features)]

            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train & test sets")

            logging.info("getting the data transformation object")

            preprocessing_obj = self.get_data_transformation_object()

            target_column = ["math_score"]
            numerical_columns = ["reading_score", "writing_score"]

            # training set target and other columns
            input_feature_train_df = train_df.drop(columns=target_column, axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=target_column, axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info("applying preprocessing on training and testing data")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            # input features has been transformed

#         Concatenation of input & target features
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("saving preprocessing object")
            save_object(
                file_path = self.preprocessor_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.preprocessor_file_path
            )




        except Exception as e:
            raise CustomException(e, sys)





        




