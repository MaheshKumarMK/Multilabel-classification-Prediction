import os, sys
from ratings.components.data_ingestion import DataIngestion

from ratings.exception import RatingsException
from ratings.logger import logging

from ratings.entity.config_entity import TrainingPipelineConfig
from ratings.entity.config_entity import DataIngestionConfig
from ratings.entity.artifact_entity import DataIngestionArtifact
from ratings.components.data_ingestion import DataIngestion

from ratings.constant.training_pipeline import *

class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

        self.data_ingestion_config=DataIngestionConfig()


    def start_data_ingestion(self)->DataIngestionArtifact: #this function should return train and test file path as mentioned in artifact
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )

            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(
                data_ingestion_config = self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
            logging.info("Got the train_set and test_set from mongodb")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
                )
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise RatingsException(e, sys)

    def run_pipeline(self):

        TrainPipeline.is_pipeline_running=True

        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            TrainPipeline.is_pipeline_running=False
            raise RatingsException(e, sys)
