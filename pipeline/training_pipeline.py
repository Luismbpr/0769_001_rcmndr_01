import os
import sys
from src.logger import get_logger
from src.custom_exception import CustomException

from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
##from src.base_model import BaseModel
from src.model_training import ModelTraining

from utils.common_functions import read_yaml
from config.paths_config import *

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Training Pipeline Initialized - training_pipeline.py")
    
    #data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    #data_ingestion.run()

    data_processor = DataProcessor(input_file=ANIMELIST_CSV, output_dir=PROCESSED_DIR)
    data_processor.run()
    
    ## BaseModel Already in ModelTraining
    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()

    logger.info("Training Pipeline Finalized - training_pipeline.py")