from locust import HttpUser, task, between
import random

from pathlib import Path

from utils import read_pickle
import os

PROJECT_ROOT_PATH = Path(__file__).parent
DATA_DIRNAME = 'data'
CUSTOMER_PRODUCT_IDS_FILENAME = 'customer_product_ids'
CUSTOMER_PRODUCT_IDS_FILEFORMAT = 'pickle'

CUSTOMER_PRODUCT_IDS_PATH = os.path.join(PROJECT_ROOT_PATH, DATA_DIRNAME, (CUSTOMER_PRODUCT_IDS_FILENAME + '.' + CUSTOMER_PRODUCT_IDS_FILEFORMAT))

customer_ids = list(read_pickle(CUSTOMER_PRODUCT_IDS_PATH).keys())


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # simulate a user wait time between 1 to 5 seconds

    def on_start(self):
        # This function is called when a new user (locust instance) is started
        self.customer_id = random.choice(customer_ids)  # randomly select a customer_id for each user

    @task
    def explore_website(self):
        self.client.get(f"/recommend/{self.customer_id}", timeout=20)  # simulate hitting the recommendation endpoint

    # @task
    # def explore_products(self):
    #     self.client.get(f"/recommend_by_product/{self.customer_id}")  # simulate hitting the recommend_by_product endpoint
