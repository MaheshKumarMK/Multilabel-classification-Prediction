import sys
from typing import Optional

import numpy as np
import pandas as pd
import re

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

                df=df.rename(columns={"approx_cost(for two people)":"cost"})

                df["cost"]=df["cost"].astype(str)
                df["cost"]=df["cost"].apply(lambda x: x.replace(",","")).astype(float)
                df["cost"]=df["cost"].replace({np.nan:0})
                # df["cost"]=df["cost"].replace({'':0})
                

                logging.info("processed the approx_cost(for two people) column and converted the cost column to float")

                df["rate"]=df["rate"].astype(str)
                df["rate"]=df["rate"].apply(lambda x: x.replace("/5", "")).apply(lambda x: x.strip())
                df["rate"]=df["rate"].apply(lambda x: x.replace("NEW", str(np.nan)).replace("-", str(np.nan)))
                df["rate"]=df["rate"].replace('nan', 0.0).astype(float)

                logging.info("processed the rate column and converted to float")

                df["reviews_list"]=df["reviews_list"].replace('[]',0.0)
                df["str_reviews_list"]=df["reviews_list"].apply(lambda x : re.findall(r'Rated *\d+\.\d+', str(x))).apply(lambda x : re.findall(r'\d+\.\d+', str(x)))

                logging.info("processed the review list column and created a new column str review list")

                df["mean_reviews_list"]=df["str_reviews_list"].apply(lambda x : re.findall(r'\d+\.\d+', str(x))).apply(lambda x: list(map(float,x)))
                df["mean_reviews_list"]=df["mean_reviews_list"].apply(lambda x : round(np.mean(x),1))
                df["mean_reviews_list"].replace(np.nan,0, inplace=True)

                logging.info("processed the str review list column and created a new column mean review list")

                df["rate"] =round((df["rate"] + df["mean_reviews_list"])/2,1)

                logging.info("Took a mean of rate column and mean review list column to get the final rate feature")

                def ratings(value):
                    if (value >= 0.0 and value <= 0.5): 
                        return 0.0
                    elif (value > 0.5 and value <= 1.4): 
                        return 1.0
                    elif (value > 1.4 and value <= 2.4): 
                        return 2.0
                    elif (value > 2.4 and value <= 3.4):
                        return 3.0
                    elif (value > 3.4 and value <= 4.4):
                        return 4.0
                    else:
                        return 5.0

                logging.info("converted the rate column to fall in range of ratings 1 to 5")

                df["rate"]=df["rate"].apply(ratings)

                logging.info("Applied the function to convert final rate column to fall under ratings 1 to 5")

                df=df[df['rate']>0].reset_index().drop(columns='index')

                logging.info("Deleted the records with rates =0 and took it for prediction")

                return df
            except Exception as e:
                raise RatingsException(e, sys)



