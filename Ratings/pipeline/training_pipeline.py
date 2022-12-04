import os, sys
from ratings.components.data_ingestion import DataIngestion

from ratings.exception import RatingsException
from ratings.logger import logging

from ratings.entity.config_entity import (
    TrainingPipelineConfig, 
    DataIngestionConfig,
    DataValidationConfig
)
from ratings.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)
from ratings.components.data_ingestion import DataIngestion
from ratings.components.data_validation import DataValidation

from ratings.constant.training_pipeline import *

class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

        self.data_ingestion_config=DataIngestionConfig()

        self.data_validation_config= DataValidationConfig()


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


    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise RatingsException(e, sys) from e

    def run_pipeline(self):


        try:
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)

        except Exception as e:
    
            raise RatingsException(e, sys)
