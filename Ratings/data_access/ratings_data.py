import sys
from typing import Optional

import numpy as np
import pandas as pd

from ratings.configuration.mongo_db_connection import MongoDBClient
from ratings.constant.database import DATABASE_NAME
from ratings.exception import RatingsException
from ratings.logger import logging


class RatingData:
    """
    This class help to export entire mongoDB record as pandas dataframe   
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise RatingsException(e, sys)
    
    def export_collection_as_dataframe (
        self, collection_name: str, database_name: Optional[str] = None)-> pd.DataFrame:
            try:
                """
                export entire collectin as dataframe:
                return pd.DataFrame of collection
                """
                if database_name is None:
                    collection = self.mongo_client.database[collection_name]

                else:
                    collection = self.mongo_client[database_name][collection_name]

                df = pd.DataFrame(list(collection.find()))

                if "_id" in df.columns.to_list():
                    df=df.drop(columns=["_id"], axis=1)

                logging.info("dropped the column _id created by mongoDB database")
                
                df.replace({"na":np.nan}, inplace=True)

                df.replace({np.nan:0}, inplace=True)

                logging.info("Replaced all the 'na' recorded by 'nan' and 'nan' record by 0")

                df=df.rename(columns={"approx_cost(for two people)":"cost"})

                df["cost"]=df["cost"].astype(str)
                df["cost"]=df["cost"].apply(lambda x: x.replace(",","")).astype(float)

                logging.info("processed the approx_cost(for two people) column and converted the cost column to float")

                df["rate"]=df["rate"].astype(str)
                df["rate"]=df["rate"].apply(lambda x: x.replace("/5", "")).apply(lambda x: x.strip())
                df["rate"]=df["rate"].apply(lambda x: x.replace("NEW", str(np.nan)).replace("-", str(np.nan)))
                df["rate"]=df["rate"].replace("nan", 0.0).astype(float)

                logging.info("processed the rate column and converted to float")

                return df
            except Exception as e:
                raise RatingsException(e, sys)



