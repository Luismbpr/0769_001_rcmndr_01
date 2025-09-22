from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input,Embedding,Dot,Flatten,Dense,Activation,BatchNormalization

from src.logger import get_logger
from src.custom_exception import CustomException
# from .logger import get_logger
# from .custom_exception import CustomException

from utils.common_functions import read_yaml

## For testing purposes only
#from config.paths_config import *

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("BaseModel - Loaded configuration from config.yaml")
        except Exception as e:
            raise CustomException("BaseModel - Error loading configuration", e)
    

    ##def RecommenderNet(self):
    def RecommenderNet(self, n_users, n_anime):
        try:
            embedding_size = self.config["model"]["embedding_size"]

            ## Input to get the user ID and the Anime ID, single dimension (int). The brackets are used to define a tuple of integers, in this case shape=(1,)
            user = Input(name="user", shape=[1])

            user_embedding = Embedding(name="user_embedding", input_dim=n_users, output_dim= embedding_size)(user)

            anime  = Input(name="anime", shape=[1])
            anime_embedding = Embedding(name="anime_embedding", input_dim=n_anime, output_dim= embedding_size)(anime)

            ## Each user represented by a point (a vector)
            ## Each anime represented by a point (a vector)
            ## Dot product. Calculates similarity by taking the sum of the element-wise products of the two vectors.
            x = Dot(name="dot_product", normalize=True, axes=2)([user_embedding,anime_embedding])

            x = Flatten()(x)
            
            ## 'he_normal' sets the initial random weights of a nn layer. Particularly useful for ReLU activation or its variantes. Ensures the prevention of vanishing or exploding gradients
            x = Dense(1, kernel_initializer='he_normal')(x)

            x = BatchNormalization()(x)

            ## 0 to 1. Predicting the value that can be interpreted as a probability
            x = Activation("sigmoid")(x)

            model = Model(inputs=[user, anime], outputs=x)

            ## Configures the learning process for the model.
            model.compile(
                loss = self.config["model"]["loss"],
                optimizer = self.config["model"]["optimizer"],
                metrics = self.config["model"]["metrics"]
            )
            ##print(metrics)## Testing purposes only

            logger.info("Model Architecture created successfully")
            
            ## Remember to return model!
            return model
        except Exception as e:
            logger.error(f"Error occurred during model architecture creation: {e}")
            raise CustomException("Failed to create model architecture")

## For testing purposes only
# if __name__ == "__main__":
#     bm = BaseModel(CONFIG_PATH)
#     bm.RecommenderNet()