import os
import numpy as np
import pandas as pd
import joblib

from config.paths_config import *

#def getAnimeFrame(anime: int | str, path_df):
def getAnimeFrame(anime, path_df):
    """
    Args
        anime: Anime Film ID (int) or Anime Film Name (str)
        path_df
            config/paths_config.py import DF
            path_df = DF
    
    
    getAnimeFrame(anime, path_df)
    """
    try:
        #pd.set_option('display.max_columns', None)
        df = pd.read_csv(path_df)
        if isinstance(anime, int):
            return df[df.anime_id == anime]
        
        if isinstance(anime, str):
            return df[df.eng_version == anime]
    
    except Exception as e:
        print("Error occurred - getAnimeFrame")


def getSynopsis(anime, path_synopsis_df):
    """
    Args
        .
    
    Returns
        .
    
    
    
    Note: Mispelled column ('sypnopsis') inside DataFrame.

    getSynopsis(anime, path_synopsis_df)
    """
    try:
        synopsis_df = pd.read_csv(path_synopsis_df)
        
        if 'sypnopsis' not in synopsis_df.columns:
            raise ValueError("Expected column synopsis = 'sypnopsis' not found in dataset.")
        
        if isinstance(anime, int):
            return synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]
        
        if isinstance(anime, str):
            return synopsis_df[synopsis_df.Name == anime].sypnopsis.values[0]
    except Exception as e:
        print("Error occurred - getAnimeFrame")


# def getSynopsis(anime, path_synopsis_df):
#     """
#     Args
#         path_synopsis = ANIME_SYNOPSIS_CSV
    
#     Returns
#         .
    
    
#     getSynopsis(anime=, path_synopsis_df=)

#     Note: Mispelled column 
#     """
#     try:
#         synopsis_df = pd.read_csv(path_synopsis_df)
    
#     ## Checks whether the column 'sypnopsis' exists inside the dataset
#     if 'sypnopsis' not in synopsis_df.columns:
#         raise ValueError("Expected column synopsis = 'sypnopsis' not found in dataset.")
    
#     if isinstance(anime, int):
#         return synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]
#         #result = synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]
#     if isinstance(anime, str):
#         return synopsis_df[synopsis_df.Name == anime].sypnopsis.values[0]
#         #result = synopsis_df[synopsis_df.Name == anime].sypnopsis.values
#     #else:
#         #raise TypeError("Input must be an integer or a string")
    
#     ## Handle case where not match is found
#     #if result.empty:
#         #raise LookupError(f"No matching anime found for input: {anime}")
    
#     ## Return the synopsis (misspelled column)
#     #return result


def find_similar_animes(name,
                        path_anime_weights,
                        path_anime2anime_encoded,
                        path_anime2anime_decoded,
                        path_anime_df,
                        n=10,
                        return_dist=False,
                        neg=False):
    """
    Args
        .
    
    Returns
        .
    
    find_similar_animes(name,
                        path_anime_weights,
                        path_anime2anime_encoded,
                        path_anime2anime_decoded,
                        path_anime_df,
                        n=10,
                        return_dist=False,
                        neg=False)
    
    Note: changed path_df to path_anime_df due to conflicting issues.
    path_df was conflicting with getAnimeFrame(anime, path_df) which was called inside of this function.
    The interpreter was using it as a method instead of a path.
    """
    try:
        ## Load weights and encoded-decoded mappings
        anime_weights = joblib.load(path_anime_weights)
        anime2anime_encoded = joblib.load(path_anime2anime_encoded)
        anime2anime_decoded = joblib.load(path_anime2anime_decoded)

        ## Get the anime ID for the given name
        ## Note: Directly pass the path_df (now path_anime_df) into function below
        index = getAnimeFrame(name, path_anime_df).anime_id.values[0]
        encoded_index = anime2anime_encoded.get(index)

        if encoded_index is None:
            raise ValueError(f"Encoded index not found for anime ID: {index}")
        
        ## Compute similarity distance
        weights = anime_weights
        dists = np.dot(weights, weights[encoded_index])## Ensure weights[encoded_index] is a 1D array
        sorted_dists = np.argsort(dists)

        n = n+1

        ## Select closest or farthest based on 'neg' flag
        if neg:
            #closest = sorted_dists[n:]## Error
            closest = sorted_dists[:n]## Solution
        else:
            closest = sorted_dists[-n:]
        
        ## Return distances and closest indices if requested
        if return_dist:
            return dists, closest
        
        ## Build he similarity Array
        SimilarityArr = []
        
        for close in closest:
            decoded_id = anime2anime_decoded.get(close)
            ## Note: Directly pass path_anime_df into function below
            anime_frame = getAnimeFrame(decoded_id, path_anime_df)

            anime_name = anime_frame.eng_version.values[0]
            genre = anime_frame.Genres.values[0]
            similarity = dists[close]

            SimilarityArr.append({
                "anime_id": decoded_id,
                "name": anime_name,
                "similarity": similarity,
                "genre": genre
            })
        
        ## Create DataFrame with results and sort by similarity
        Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
        return Frame[Frame.anime_id != index].drop(['anime_id'], axis=1)
    
    except Exception as e:
        print("Error occurred - find_similar_animes")


def find_similar_users(item_input,
                       path_user_weights,
                       path_user2user_encoded,
                       path_user2user_decoded,
                       n=10,
                       return_dist=False,
                       neg=False):
    """
    Args
        .
    
    Returns
        .
    
    
    find_similar_users(item_input,
                       path_user_weights,
                       path_user2user_encoded,
                       path_user2user_decoded,
                       n=10,
                       return_dist=False,
                       neg=False)
    """
    try:
        user_weights = joblib.load(path_user_weights)
        user2user_encoded = joblib.load(path_user2user_encoded)
        user2user_decoded = joblib.load(path_user2user_decoded)
        
        index = item_input
        encoded_index = user2user_encoded.get(index)
        
        weights = user_weights
        
        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists)
        
        n = n+1
        
        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]
        
        if return_dist:
            return dists, closest
        
        SimilarityArr = []
        
        for close in closest:
            similarity = dists[close]
            
            if isinstance(item_input, int):
                ## Important: use .get()
                decoded_id = user2user_decoded.get(close)
                SimilarityArr.append({
                    "similar_users": decoded_id,
                    "similarity": similarity
                    })
                
                #similar_users = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
                #similar_users = similar_users[similar_users.similar_users != item_input]
                #return similar_users
        similar_users = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
        similar_users = similar_users[similar_users.similar_users != item_input]
        return similar_users
    
    except Exception as e:
        print("Error occurred - find_similar_users", e)


def get_user_preferences(user_id,
                         path_rating_df,
                         path_anime_df):
    """
    Args
        .
    
    Returns
        .
    
    get_user_preferences(user_id,
                         path_rating_df,
                         path_anime_df)
    
    Note: changed path_df to path_anime_df due to conflicting issues
    """
    try:
        rating_df = pd.read_csv(path_rating_df)
        df = pd.read_csv(path_anime_df)
        
        animes_watched_by_user = rating_df[rating_df.user_id == user_id]
        
        #user_rating_percentile = np.percentile(rating_df.rating, 75)## Error
        ## Solution
        user_rating_percentile = np.percentile(animes_watched_by_user.rating, 75)
        
        animes_watched_by_user = animes_watched_by_user[animes_watched_by_user.rating >= user_rating_percentile]
        
        top_animes_user = (
            animes_watched_by_user.sort_values(by="rating", ascending=False).anime_id.values
        )
        
        anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
        anime_df_rows = anime_df_rows[["eng_version", "Genres"]]
        
        return anime_df_rows
    
    except Exception as e:
        print("Error occurred - get_user_preferences", e)


def get_user_recommendations(similar_users,
                             user_pref,
                             path_anime_df,
                             path_synopsis_df,
                             path_rating_df,
                             n=10):
    """
    Args
        .
    
    Returns
        .
    
    
    get_user_recommendations(similar_users,
                             user_pref,
                             path_anime_df,
                             path_synopsis_df,
                             path_rating_df,
                             n=10)
    
    Notes:
    """
    try:
        recommended_animes = []
        anime_list = []
        
        for user_id in similar_users.similar_users.values:
            pref_list = get_user_preferences(int(user_id), path_rating_df, path_anime_df)
            
            pref_list = pref_list[~pref_list.eng_version.isin(user_pref.eng_version.values)]
            
            if not pref_list.empty:
                anime_list.append(pref_list.eng_version.values)
        
        if anime_list:
            anime_list = pd.DataFrame(anime_list)
            sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts()).head(n)
            
            for i, anime_name in enumerate(sorted_list.index):
                n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]
                
                if isinstance(anime_name, str):
                    frame = getAnimeFrame(anime_name, path_anime_df)
                    anime_id = frame.anime_id.values[0]
                    genre = frame.Genres.values[0]
                    synopsis = getSynopsis(int(anime_id), path_synopsis_df)
                    
                    recommended_animes.append({
                        "n" : n_user_pref,
                        "anime_name" : anime_name,
                        "Genres" : genre,
                        "Synopsis": synopsis
                    })
        
        return pd.DataFrame(recommended_animes).head(n)
    
    except Exception as e:
        print("Error occurred - user_recommendations", e)