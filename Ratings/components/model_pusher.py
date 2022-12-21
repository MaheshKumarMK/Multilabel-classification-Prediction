from ratings.exception import RatingsException
from ratings.logger import logging

from ratings.entity.config_entity import ModelPusherConfig
from ratings.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact

import os,sys
import shutil

class ModelPusher:

    def __init__(
        self,
        model_pusher_config: ModelPusherConfig,
        model_evaluation_artifact: ModelEvaluationArtifact
    ):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_evaluation_artifact
        except  Exception as e:
            raise RatingsException(e, sys)

    def initiate_model_pusher(self)-> ModelPusherArtifact:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path


            logging.info("Creating model pusher dir to save model")

            model_file_path = self.model_pusher_config.model_file_path

            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)

            shutil.copy(src=trained_model_path, dst=model_file_path)

            logging.info("Created model pusher dir to save model")


            logging.info("saving model direcctory")

            saved_model_path = self.model_pusher_config.saved_model_path
            
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)

            shutil.copy(src=trained_model_path, dst=saved_model_path)

            logging.info("saved model direcctory")


            logging.info("Preparing artifact")

            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path=saved_model_path, 
                model_file_path=model_file_path)

            return model_pusher_artifact

        except  Exception as e:
            raise RatingsException(e, sys)







