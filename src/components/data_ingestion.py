# All the code that is related to reading the data

import os
import pandas as pd
import sys

from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation



@dataclass #-decorator - using this instead of __init__ - dataclass can be used to directly define the class variables
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", 'train.csv')
    test_data_path: str = os.path.join("artifacts", 'test.csv')
    raw_data_path: str = os.path.join("artifacts", 'data.csv')

class DataIngestion(DataIngestionConfig):

    # def __init__(self):
    #     self.ingestion_config = DataIngestionConfig() # this variable will store the class
# ----------Instead why not use inheritance -----------

    def initiate_data_ingestion(self): #used to read data from databases - mongodb
        logging.info("Entered data ingestion component")

        try:
            df = pd.read_csv("notebook\data\stud.csv")
            logging.info("reading the dataset")

            os.makedirs(os.path.dirname(self.train_data_path), exist_ok= True)
            df.to_csv(self.raw_data_path,  index= False, header= True)

            logging.info("Train test split initiated")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.train_data_path, index= False, header= True)
            test_set.to_csv(self.test_data_path, index= False, header= True)

            logging.info("data ingestion withinn separate files is completed")

            return (
                self.train_data_path,
                self.test_data_path
            )


        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":

    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
