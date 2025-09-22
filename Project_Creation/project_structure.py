import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


PROJECT_PATH = "/Users/luis/Documents/Programming/dev/0769_Beginner_Advanced_MLOPS_GCP_CICD/venv_0769_Beginner_Advanced_MLOPS_GCP_CICD/0769_03_Hybrid_Recommender_System/Project02/"


project_structure_files = {
f"{PROJECT_PATH}/application.py",
f"{PROJECT_PATH}/config/__init__.py",
f"{PROJECT_PATH}/config/config.yaml",
f"{PROJECT_PATH}/config/paths_config.py",
f"{PROJECT_PATH}/custom_jenkins/Dockerfile",
f"{PROJECT_PATH}/deployment.yaml",
f"{PROJECT_PATH}/Dockerfile",
f"{PROJECT_PATH}/Jenkinsfile",
f"{PROJECT_PATH}/notebook/anime.ipynb",
f"{PROJECT_PATH}/notebook/NB_001.ipynb",
f"{PROJECT_PATH}/notebook/NB_002.ipynb",
f"{PROJECT_PATH}/notebook/NB_003.ipynb",
f"{PROJECT_PATH}/notebook/NB_004.ipynb",
f"{PROJECT_PATH}/notebook/NB_005.ipynb",
f"{PROJECT_PATH}/notebook/NB_006.ipynb",
f"{PROJECT_PATH}/notebook/NB_007.ipynb",
f"{PROJECT_PATH}/notebook/NB_008.ipynb",
f"{PROJECT_PATH}/pipeline/__init__.py",
f"{PROJECT_PATH}/pipeline/prediction_pipeline.py",
f"{PROJECT_PATH}/pipeline/training_pipeline.py",
f"{PROJECT_PATH}/project_creation/project_structure.py",
f"{PROJECT_PATH}/project_creation/project_structure.ipynb",
#f"{PROJECT_PATH}/requirements.txt",
f"{PROJECT_PATH}/setup.py",
f"{PROJECT_PATH}/src/__init__.py",
f"{PROJECT_PATH}/src/base_model.py",
f"{PROJECT_PATH}/src/custom_exception.py",
f"{PROJECT_PATH}/src/data_ingestion.py",
f"{PROJECT_PATH}/src/data_processing.py",
f"{PROJECT_PATH}/src/logger.py",
f"{PROJECT_PATH}/src/model_training.py",
f"{PROJECT_PATH}/static/style.css",
f"{PROJECT_PATH}/templates/index.html",
f"{PROJECT_PATH}/tester.py",
f"{PROJECT_PATH}/utils/__init__.py",
f"{PROJECT_PATH}/utils/common_functions.py",
f"{PROJECT_PATH}/utils/helpers.py",
}

for filepath in project_structure_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    print(f"filedir:\n{filedir}")
    print(f"filename:\n{filename}")
    print("")

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:\n{filedir} for the file: {filename}")

        ## If filepath does not exist, get the size of the filepath. If it is 0 then open filepath in write mode and create that file
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w") as f:
                pass
                logging.info(f"Creating empty file: {filepath}")
        else:
            
            logging.info(f"{filename} already exists")