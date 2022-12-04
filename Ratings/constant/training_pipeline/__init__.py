import os

ARTIFACT_DIR: str = "artifact"

FILE_NAME: str = "ratings.csv"

TRAIN_FILE_NAME: str = "train.csv"

TEST_FILE_NAME: str = "test.csv"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

SCHEMA_DROP_COLS = "drop_columns"

DATA_INGESTION_COLLECTION_NAME: str = "Ratings"

DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_INGESTION_INGESTED_DIR: str = "ingested"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

TARGET_COLUMN = "rate"


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_VALID_DIR: str = "validated"

DATA_VALIDATION_INVALID_DIR: str = "invalid"

DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"

DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "drift_report.yaml"

DATA_VALIDATION_STD_DEV_REPORT_DIR: str = "std_report"

DATA_VALIDATION_STD_DEV_REPORT_FILE_NAME: str = "std_dev_report.yaml"

