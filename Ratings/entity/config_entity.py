import os
from dataclasses import dataclass, field
from datetime import datetime

from ratings.constant.training_pipeline import *

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig():
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)

    timestamp: str = TIMESTAMP

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        TrainingPipelineConfig.artifact_dir, DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
    )

    training_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
    )

    testing_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
    )

    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

    collection_name: str = DATA_INGESTION_COLLECTION_NAME


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
        )
    
    valid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_VALID_DIR)

    invalid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_INVALID_DIR)

    valid_train_file_path: str = os.path.join(valid_data_dir, TRAIN_FILE_NAME)

    valid_test_file_path: str = os.path.join(valid_data_dir, TEST_FILE_NAME)

    invalid_train_file_path: str = os.path.join(invalid_data_dir, TRAIN_FILE_NAME)

    invalid_test_file_path: str = os.path.join(invalid_data_dir, TEST_FILE_NAME)

    
    std_dev_report_file_path: str = os.path.join(
        data_validation_dir,
        DATA_VALIDATION_STD_DEV_REPORT_DIR,
        DATA_VALIDATION_STD_DEV_REPORT_FILE_NAME

    )

    drift_report_file_path: str = os.path.join(
        data_validation_dir,
        DATA_VALIDATION_DRIFT_REPORT_DIR,
        DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
    )


@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
        )

    transformed_train_file_path: str = os.path.join(
        data_transformation_dir, 
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TRAIN_FILE_NAME.replace("csv", "npy")
        )
    
    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TEST_FILE_NAME.replace("csv", "npy")
    )

    transformed_object_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        PREPROCSSING_OBJECT_FILE_NAME
   )



@dataclass
class ModelTrainingConfig:
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME
    )

    trained_model_file_path:str = os.path.join(
        model_trainer_dir,MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_TRAINER_TRAINED_MODEL_NAME
    )

    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE

    #model_config_file_path = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH

    overfitting_underfitting_threshold = MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD


@dataclass
class ModelEvaluationConfig:
    model_evaluation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_EVALUATION_DIR_NAME
    )

    report_file_path = os.path.join(
        model_evaluation_dir, MODEL_EVALUATION_REPORT_NAME
    )

    change_threshold_score = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE


@dataclass
class ModelPusherConfig:
    model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,MODEL_PUSHER_DIR_NAME
    )

    model_file_path = os.path.join(model_evaluation_dir,MODEL_FILE_NAME)

    timestamp = round(datetime.now().timestamp())

    saved_model_path=os.path.join(
        SAVED_MODEL_DIR,f"{timestamp}",MODEL_FILE_NAME
    )

