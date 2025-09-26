from config.paths_config import *
from utils.helpers import *
#from src.custom_exception import CustomException
#from src.logger import get_logger

#logger = get_logger(__name__)

def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    """
    Hybrid Recommendation System

    Args
        .
    
    Returns
        .
    
    hybrid_recommendation(user_id=, user_weight=0.5, content_weight=0.5)
    """
    try:
        #logger.info("prediction_pipeline.py - hybrid_recommendation Started")
        ##User Recommendation
        similar_users = find_similar_users(item_input=user_id,
                                           path_user_weights=USER_WEIGHTS_PATH,
                                           path_user2user_encoded=USER2USER_ENCODED,
                                           path_user2user_decoded=USER2USER_DECODED,
                                           n=10, return_dist=False, neg=False)
        
        user_pref = get_user_preferences(user_id,
                                         path_rating_df=RATING_DF,
                                         path_anime_df=DF)
        
        user_recommended_animes = get_user_recommendations(similar_users=similar_users,
                                                           user_pref=user_pref,
                                                           path_anime_df=DF,
                                                           path_synopsis_df=SYNOPSIS_DF,
                                                           path_rating_df=RATING_DF,
                                                           n=10)
        
        user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()

        ##Content Recommendation
        content_recommended_animes = []

        for anime in user_recommended_anime_list:
            similar_animes = find_similar_animes(name=anime,
                                                 path_anime_weights=ANIME_WEIGHTS_PATH,
                                                 path_anime2anime_encoded=ANIME2ANIME_ENCODED,
                                                 path_anime2anime_decoded=ANIME2ANIME_DECODED,
                                                 path_anime_df=DF,
                                                 n=10,
                                                 return_dist=False,
                                                 neg=False)
            
            if similar_animes is not None and not similar_animes.empty:
                content_recommended_animes.extend(similar_animes["name"].tolist())
            else:
                print(f"No similar anime foind {anime}")
            
        combined_scores = {}

        for anime in user_recommended_anime_list:
            combined_scores[anime] = combined_scores.get(anime, 0) + user_weight
        
        for anime in content_recommended_animes:
            combined_scores[anime] = combined_scores.get(anime, 0) + content_weight
        
        sorted_animes = sorted(combined_scores.items(), key= lambda x:x[1], reverse=True)
        
        #logger.info("prediction_pipeline.py - hybrid_recommendation Completed Successfully")
        #logger.info(f"sorted_animes:\n{print([anime for anime, score in sorted_animes in sorted_animes[:10]])}")
        
        return [anime for anime, score in sorted_animes in sorted_animes[:10]]
    
    except Exception as e:
        #logger.info("Error occurred - prediction_pipeline.py - hybrid_recommendation", e)
        print("Error occurred - prediction_pipeline.py - hybrid_recommendation", e)