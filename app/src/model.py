from .utils import read_pickle
from pathlib import Path
import scipy as sp
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

PROJECT_ROOT_PATH = Path(__file__).parent.parent
DATA_DIRNAME = 'data'
EMBEDDINGS_FILENAME = 'product_embeddings'
EMBEDDINGS_FILEFORMAT = 'npz'
MOST_POPULAR_PRODUCTS_FILENAME = 'most_popular_products'
MOST_POPULAR_PRODUCTS_FILEFORMAT = 'pickle'
PRODUCT_TO_MATRIX_MAPPING_FILENAME = 'product_to_matrix_mapping'
PRODUCT_TO_MATRIX_MAPPING_FILEFORMAT = 'pickle'

CUSTOMER_PRODUCT_IDS_FILENAME = 'customer_product_ids'
CUSTOMER_PRODUCT_IDS_FILEFORMAT = 'pickle'

EMBEDDINGS_PATH = os.path.join(PROJECT_ROOT_PATH, DATA_DIRNAME, (EMBEDDINGS_FILENAME + '.' + EMBEDDINGS_FILEFORMAT))
MOST_POPULAR_PRODUCTS_PATH = os.path.join(PROJECT_ROOT_PATH, DATA_DIRNAME, (MOST_POPULAR_PRODUCTS_FILENAME + '.' + MOST_POPULAR_PRODUCTS_FILEFORMAT))
PRODUCT_TO_MATRIX_MAPPING_PATH = os.path.join(PROJECT_ROOT_PATH, DATA_DIRNAME, (PRODUCT_TO_MATRIX_MAPPING_FILENAME + '.' + PRODUCT_TO_MATRIX_MAPPING_FILEFORMAT))
CUSTOMER_PRODUCT_IDS_PATH = os.path.join(PROJECT_ROOT_PATH, DATA_DIRNAME, (CUSTOMER_PRODUCT_IDS_FILENAME + '.' + CUSTOMER_PRODUCT_IDS_FILEFORMAT))



class ContentBasedFiltering:
    def __init__(self) -> None:
        self.embeddings = sp.sparse.load_npz(EMBEDDINGS_PATH)
        self.dict_product_to_embedding_ids = read_pickle(PRODUCT_TO_MATRIX_MAPPING_PATH)
        self.dict_embedding_to_product_ids = {v: k for k, v in self.dict_product_to_embedding_ids.items()}
        self.most_popular_products = read_pickle(MOST_POPULAR_PRODUCTS_PATH)
        self.dict_customer_product_ids = read_pickle(CUSTOMER_PRODUCT_IDS_PATH)

    def recommend_by_product(self, customer_id, similarity_threshold=0.6, n_recommendations=20):
        customer_product_ids = self.dict_customer_product_ids[customer_id]

        dict_product_recommendations = {}
        for product_id in customer_product_ids:
            similarity_matrix = cosine_similarity(self.embeddings, self.embeddings[self.dict_product_to_embedding_ids[product_id], :], dense_output=False)
            recommendations_indices = np.argsort(similarity_matrix.toarray().flatten())[::-1][1:n_recommendations+1]
            recommendations_scores = np.sort(similarity_matrix.toarray().flatten())[::-1][1:n_recommendations+1]
            recommendations_ids = np.array([self.dict_embedding_to_product_ids[idx] for idx in recommendations_indices])
            recommendations_ids = recommendations_ids[recommendations_scores>similarity_threshold].tolist()
            recommendations_scores = recommendations_scores[recommendations_scores>similarity_threshold].tolist()
            dict_product_recommendations[product_id] = list(zip(recommendations_ids, recommendations_scores))
        return dict_product_recommendations
    

    def recommend(self, customer_id, similarity_threshold=0.6, n_recommendations=10):
        dict_product_recommendations = self.recommend_by_product(customer_id, similarity_threshold=similarity_threshold, n_recommendations=20)
        sorted_product_ids = sorted(dict_product_recommendations, key=lambda k: len(dict_product_recommendations[k]))

        i = 0
        recommendations = []
        for product_id in sorted_product_ids:
            product_recommendations = [x[0] for x in dict_product_recommendations[product_id]]
            recommendations = recommendations + product_recommendations
            i += len(product_recommendations)

        if i < 20:
            recommendations = recommendations + self.most_popular_products[:n_recommendations-i]
        else:
            recommendations = recommendations[:n_recommendations]
            
        return recommendations