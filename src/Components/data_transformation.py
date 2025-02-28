import sys
import os
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import dill


#from src.exceptions import CustomException
#from src.loggers import logging
#from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    

    def get_data_transformation_obj(self):
        try:
            numerical_columns=['reading_score','writing_score']
            categorical_columns=['gender',
                                 'race_ethnicity',
                                 'parental_level_of_education',
                                 'lunch',
                                 'test_preparation_course'
                                 ]
            
            num_pipeline=Pipeline(
                steps=[
                    ("impute",SimpleImputer(strategy='median')),
                    ("scalar",StandardScaler())
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ('impute',SimpleImputer(strategy='most_frequent')),
                    ('encoder',OneHotEncoder()),
                    ('scalar',StandardScaler())
                ]
            )

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )
            
            return preprocessor

        except Exception as ex:
            raise (ex,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            #logging.info("Read Train and Test data completed")

            #logging.info("obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformation_obj()

            target_column='math_score'

            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]

            #logging.info(f"Applying  preprocessing object on training and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]

            #logging.info(f"Saved preprocessing object.")

            """save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )"""
            def save_object(file_path,obj):
                try:
                    dir_path=os.path.dirname(file_path)
                    os.makedirs(dir_path,exist_ok=True)

                    with open (file_path,'wb') as file_obj:
                        dill.dump(obj,file_obj)
                

                except Exception as ex:
                    raise (ex,sys)

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as ex:
            raise (ex,sys)