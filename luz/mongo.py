import pymongo
from luz.secret import mongo_pass, mongo_user



def get_prices_collection():
    client = pymongo.MongoClient(
    f"mongodb+srv://{mongo_user}:{mongo_pass}@platorimo.2wuzf.mongodb.net/?authSource=admin")
    
    return client.get_database('luz').get_collection("prices")

