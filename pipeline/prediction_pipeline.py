from config.paths_config import *
from utils.helpers import *
#from src.custom_exception import CustomException
#from src.logger import get_logger

#logger = get_logger(__name__)

def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    """
    Prediction Pipeline using a Hybrid Recommendation System

    Hybrid Recommendation System
    Finds Similar Users
    Finds Similar Users

    Args
        .
    
    Returns
        .
    
    hybrid_recommendation(user_id=, user_weight=0.5, content_weight=0.5)
    """
    try:
        #logger.info("prediction_pipeline.py - hybrid_recommendation Started")
        ##User Recommendation
        similar_users = find_similar_users(user_id, USER_WEIGHTS_PATH,
                                           USER2USER_ENCODED, USER2USER_DECODED,
                                           n=10, return_dist=False, neg=False)
        
        user_pref = get_user_preferences(user_id, RATING_DF, DF)
        
        user_recommended_animes = get_user_recommendations(similar_users, user_pref, DF,
                                                           SYNOPSIS_DF, RATING_DF,
                                                           n=10)
        
        user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()

        ##Content Recommendation
        content_recommended_animes = []

        for anime in user_recommended_anime_list:
            similar_animes = find_similar_animes(anime, ANIME_WEIGHTS_PATH,
                                                 ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED,
                                                 DF,
                                                 n=10, return_dist=False, neg=False)
            
            if similar_animes is not None and not similar_animes.empty:
                content_recommended_animes.extend(similar_animes["name"].tolist())
            else:
                print(f"No similar anime found {anime}")
            
        combined_scores = {}

        for anime in user_recommended_anime_list:
            combined_scores[anime] = combined_scores.get(anime, 0) + user_weight
        
        for anime in content_recommended_animes:
            combined_scores[anime] = combined_scores.get(anime, 0) + content_weight
        
        sorted_animes = sorted(combined_scores.items(), key= lambda x:x[1], reverse=True)
        
        #logger.info("prediction_pipeline.py - hybrid_recommendation Completed Successfully")
        #logger.info(f"sorted_animes:\n{print([anime for anime, score in sorted_animes in sorted_animes[:10]])}")
        
        return [anime for anime, score in sorted_animes[:10]]
    
    except Exception as e:
        print("Error occurred - prediction_pipeline.py - hybrid_recommendation", e)