import os
import sys

from ratings.exception import RatingsException
from ratings.logger import logging

import numpy as np
import pandas as pd
from pandas import DataFrame

from ratings.entity.config_entity import DataTransformationConfig
from ratings.entity.artifact_entity import (
    DataTransformationArtifact, DataValidationArtifact)
from ratings.constant.training_pipeline import TARGET_COLUMN
from ratings.exception import RatingsException
from ratings.logger import logging
from ratings.utils.main_utils import save_numpy_array_data, save_object

from sklearn.preprocessing import RobustScaler
from catboost import CatBoostClassifier
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector



class DataTransformation:
    def __init__(
        self, 
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig):
    

        try:
            self.data_validation_artifact = data_validation_artifact

            self.data_transformation_config = data_transformation_config
        
        except Exception as e:
            raise RatingsException(e, sys)

    @staticmethod
    def read_data(filepath)-> DataFrame:
        try:
            return pd.read_csv(filepath)
    
        except Exception as e:
            raise RatingsException(e, sys)
    
    @classmethod
    def get_data_transformer_object(cls)-> Pipeline:
        """
        :return: Pipeline object to transform dataset
        """
        logging.info(
             "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Got numerical cols from schema config")

            robust_scaler = RobustScaler()

            numerical_transformer = Pipeline(
                steps=[
                    ('imp_num', IterativeImputer(initial_strategy='median')),
                    ('RobustScaler', robust_scaler)
                    ]
                )

            categorical_transformer = OneHotEncoder(handle_unknown="ignore")

            logging.info("Initialized RobustScaler, Iterative Imputer")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numerical_transformer, selector(dtype_exclude="category")),
                    ("cat", categorical_transformer, selector(dtype_include="category"))
                    ])

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor

        except Exception as e:
            raise RatingsException(e, sys)

    # @classmethod
    # def get_num_data_transformer_object(cls)-> Pipeline:
    #     """
    #     :return: Pipeline object to transform dataset
    #     """
    #     logging.info(
    #          "Entered get_data_transformer_object method of DataTransformation class"
    #     )

    #     try:
    #         logging.info("Got numerical cols from schema config")

    #         robust_scaler = RobustScaler()

    #         num_iterative_imputer = IterativeImputer(initial_strategy='median')


    #         logging.info("Initialized RobustScaler, IterativeImputer")

    #         # num_features = df.select_dtypes(exclude="object").columns
    #         # catg_features = df.select_dtypes(include="object").columns


    #         preprocessor_num = Pipeline(
    #             steps=[("imputer", num_iterative_imputer), ("RobustScaler", robust_scaler)]
    #         )

    #         logging.info("Created preprocessor object from ColumnTransformer")

    #         logging.info(
    #             "Exited get_data_transformer_object method of DataTransformation class"
    #         )

    #         return preprocessor_num


    #     except Exception as e:
    #         raise RatingsException(e, sys)

    # @classmethod
    # def get_catg_data_transformer_object(cls)-> Pipeline:
    #     """
    #     :return: Pipeline object to transform dataset
    #     """
    #     logging.info(
    #          "Entered get_data_transformer_object method of DataTransformation class"
    #     )

    #     try:
    #         logging.info("Got numerical cols from schema config")

    #         robust_scaler = RobustScaler()

    #         catg_iterative_imputer = IterativeImputer(initial_strategy='most_frequent')

    #         logging.info("Initialized RobustScaler, IterativeImputer")

    #         preprocessor_catg = Pipeline(
    #             steps=[("imputer", catg_iterative_imputer), ("RobustScaler", robust_scaler)]
    #         )

    #         logging.info("Created preprocessor object from ColumnTransformer")

    #         logging.info(
    #             "Exited get_data_transformer_object method of DataTransformation class"
    #         )

    #         return preprocessor_catg


    #     except Exception as e:
    #         raise RatingsException(e, sys)

    
    def initiate_data_transformation(self)-> DataTransformationArtifact:

        try:
            logging.info("Starting data transformation")

            preprocessor = self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            train_df = DataTransformation.read_data(
                filepath= self.data_validation_artifact.valid_train_file_path
            )

            test_df = DataTransformation.read_data(
                filepath=self.data_validation_artifact.valid_test_file_path
            )

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]

            logging.info("Got input features and target features of Training dataset")

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_df[TARGET_COLUMN]
            
            logging.info("Got input features and target features of test dataset")


            catg_features_train = input_feature_train_df.select_dtypes(include="object").columns

            catg_features_test = input_feature_test_df.select_dtypes(include="object").columns

            logging.info("Got the numerical and categorical columns")

            le=LabelEncoder()

            input_feature_train_df[catg_features_train] = input_feature_train_df[catg_features_train].apply(lambda series: pd.Series(
            le.fit_transform(series[series.notnull()]),
            index=series[series.notnull()].index))

            logging.info("Transformed the train data frame using label encoding")


            input_feature_test_df[catg_features_test] = input_feature_test_df[catg_features_test].apply(lambda series: pd.Series(
            le.fit_transform(series[series.notnull()]),
            index=series[series.notnull()].index))

            logging.info("Transformed the test data frame using label encoding")

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logging.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logging.info("Used the preprocessor object to transform the test features")


            logging.info(
                "Used the preprocessor object to fit transform the train features"
            )
  
            logging.info("Createing train array and test array")

            train_arr = np.c_[
                input_feature_train_arr, target_feature_train_df
            ]

            test_arr = np.c_[
                input_feature_test_arr, target_feature_test_df
            ]

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            logging.info("Saved the preprocessor object")

            logging.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise RatingsException(e, sys)
