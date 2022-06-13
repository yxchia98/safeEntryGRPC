import pymongo
from pymongo import MongoClient


class MongoDatabase():
    def __init__(self) -> None:
        pass

    def connect(self):
        self.client = MongoClient(
            "mongodb+srv://<user>:<password>@secluster.25zbo.mongodb.net/?retryWrites=true&w=majority")

    def connect_database(self, dbname):
        return self.client[dbname]

    def disconnect(self):
        self.client.close()
