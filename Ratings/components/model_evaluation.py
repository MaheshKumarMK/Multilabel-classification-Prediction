from ratings.exception import RatingsException
from ratings.logger import logging

import os,sys
import pandas as pd
from sklearn import model_selection

from ratings.entity.config_entity import ModelEvaluationConfig
from ratings.entity.artifact_entity import (
    DataValidationArtifact, ModelTrainerArtifact,ModelEvaluationArtifact
    )
from ratings.constant.training_pipeline import *
from ratings.ml.model.estimator import ModelResolver
from ratings.utils.main_utils import load_object, write_yaml_file
from ratings.ml.metric.classification_metric import get_classification_score



class ModelEvaluation:
    def __init__(
        self, model_eval_config: ModelEvaluationConfig,

        data_validation_artifact: DataValidationArtifact,

        model_training_artifact: ModelTrainerArtifact
    ):
        try:
            self.model_eval_config = model_eval_config

            self.data_validation_artifact = data_validation_artifact

            self.model_training_artifact = model_training_artifact

        except Exception as e:
            raise RatingsException(e,sys)

    def initiate_model_evaluation(self)-> ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path

            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            train_df = pd.read_csv(valid_train_file_path)

            test_df = pd.read_csv(valid_test_file_path)

            logging.info("Got the train df and test df")

            df = pd.concat([train_df, test_df])

            logging.info("Combined train df and test df")

            y_true = df[TARGET_COLUMN]

            df = df.drop(TARGET_COLUMN, axis=1)

            logging.info("Got the y_true and df dataframe")


            train_model_file_path = self.model_training_artifact.trained_model_filepath

            model_resolver = ModelResolver()

            is_model_accepted = True


            if not model_resolver.is_model_exists():

                model_evaluation_artifact = ModelEvaluationArtifact(

                    is_model_accepted=is_model_accepted,

                    improved_accuracy=None,

                    best_model_path=None, 

                    trained_model_path=train_model_file_path, 

                    train_model_metric_artifact=self.model_training_artifact.train_metric_artifact,

                    best_model_metric_artifact=None
                )

                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")

                return model_evaluation_artifact
            
            latest_model_path = model_resolver.get_best_model_path()

            latest_model = load_object(file_path=latest_model_path)

            train_model = load_object(file_path=train_model_file_path)


            y_trained_pred = train_model.predict(df)

            y_latest_pred = latest_model.predict(df)


            trained_metric = get_classification_score(y_true, y_trained_pred)

            latest_metric = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score

            if self.model_eval_config.change_threshold_score < improved_accuracy:
                is_model_accepted = True
            
            else:
                is_model_accepted =False

            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=improved_accuracy, 
                    best_model_path=latest_model_path, 
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=trained_metric, 
                    best_model_metric_artifact=latest_metric)

            model_eval_report = model_evaluation_artifact.__dict__

            #save the report

            write_yaml_file(
                file_path=self.model_eval_config.report_file_path,
                content=model_eval_report
                )
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise RatingsException(e,sys)


