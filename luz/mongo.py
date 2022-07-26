import os

import pymongo


def get_prices_collection():
    client = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}"
        f"@platorimo.2wuzf.mongodb.net/?authSource=admin"
    )

    return client.get_database("luz").get_collection("prices")
