from typing import Union

from fastapi import FastAPI

from .model import ContentBasedFiltering

app = FastAPI()

recommender = ContentBasedFiltering()


@app.get("/")
def read_root():
    return 'Selal Product Recommender System API'


@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):
    return recommender.recommend(customer_id)


@app.get("/recommend_by_product/{customer_id}")
def recommend(customer_id: int):
    return recommender.recommend_by_product(customer_id)