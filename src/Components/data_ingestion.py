import os
import sys
from src.exceptions import CustomException
from src.loggers import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path:str = os.path.join('artifacts','raw_data.csv')
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path:str = os.path.join('artifacts','test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data ingestion method or component")
        try:
            df=pd.read_csv('src/Notebook/Data/stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train Test split initiated")
            train_data,test_data=train_test_split(df,test_size=0.2,random_state=123)

            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_data.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")  

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            ) 

        except Exception as ex:
            raise CustomException(ex,sys)


if __name__== "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()

