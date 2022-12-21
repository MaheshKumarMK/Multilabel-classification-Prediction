
import sys, os
import pandas as pd

from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder

from ratings.exception import RatingsException
from ratings.logger import logging
from ratings.constant.training_pipeline import *


class RatingsModel:
    def __init__(self, preprocessing_object, trained_model_object: object):
        
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def model_predict(self, dataframe: DataFrame) -> DataFrame:
        logging.info("Entered predict method of RatingsModel class")

        try:
            logging.info("Using the trained model to get predictions")

            catg_features = dataframe.select_dtypes(include="object").columns

            le=LabelEncoder()

            dataframe[catg_features] = dataframe[catg_features].apply(lambda series: pd.Series(
            le.fit_transform(series[series.notnull()]),
            index=series[series.notnull()].index))

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise RatingsException(e, sys) from e


class ModelResolver:

    def __init__(self, model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise e

    def get_best_model_path(self,)->str:
        try:
            timestamps = list(map(int, os.listdir(self.model_dir)))

            latest_timestamp = max(timestamps)

            latest_model_path = os.path.join(self.model_dir, f"{latest_timestamp}", MODEL_FILE_NAME)

            return latest_model_path

        except Exception as e:
            raise e

    def is_model_exists(self)->bool:
        try:
            if not os.path.exists(self.model_dir):
                return False
            
            timestamps = os.listdir(self.model_dir)

            if len(timestamps) == 0:
                return False

            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False

            return True

        except Exception as e:
            raise e

        
