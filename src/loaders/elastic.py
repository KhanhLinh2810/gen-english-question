from elasticsearch import Elasticsearch
from env import config

class Elastic:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = Elasticsearch(
                config["elastic"]["url"],
                api_key=config["elastic"]["api_key"]
            )
        return cls._instance
