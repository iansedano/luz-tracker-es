import sqlalchemy
from luz.luz_db import connect_to_luz
from luz.mongo import get_prices_collection
import requests
from datetime import datetime

from pprint import pp

from functools import reduce

def get_timestamp(date, hour):
    day, month, year = date.split("-")
    hour, _ = hour.split("-")

    dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))
    return int(dt.timestamp())
    
def get_datetime(date, hour):
    day, month, year = date.split("-")
    hour, _ = hour.split("-")

    return datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))

    
def pprint_api_data(price_json):
    def reducer(acc: list, keyval):
        acc.append((keyval[0], keyval[1]["price"]))
        return acc
        
    pp(reduce(reducer, price_json.items(), []))

def get_data_from_api():
    response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")

    price_json = response.json()

    pprint_api_data(price_json)

    return [
            {"date": get_datetime(obj["date"], obj["hour"]), "price": obj["price"]}
            for obj in price_json.values()
        ]

def send_data_to_mysql(api_data):
    engine, connection, metadata = connect_to_luz()

    table = sqlalchemy.Table("price", metadata, autoload=True, autoload_with=engine)

    query = sqlalchemy.insert(table)
    result_proxy = connection.execute(query, [
            {"date": int(record["date"].timestamp()), "price": record["price"]}
            for record in api_data
        ])

def send_data_to_mongo(api_data):
    collection = get_prices_collection()
    collection.insert_many(api_data)

send_data_to_mongo(get_data_from_api())