import sqlalchemy
from luz.luz_db import connect_to_luz
import requests
from datetime import datetime

from pprint import pp

from functools import reduce

def get_timestamp(date, hour):
    day, month, year = date.split("-")
    hour, _ = hour.split("-")

    dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))
    return int(dt.timestamp())

# Connect to local database
engine, connection, metadata = connect_to_luz()

table = sqlalchemy.Table("price", metadata, autoload=True, autoload_with=engine)

response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")

price_json = response.json()

def reducer(acc: list, keyval):
    acc.append((keyval[0], keyval[1]["price"]))
    return acc
    
pp(reduce(reducer, price_json.items(), []))

prices = [
        {"date": get_timestamp(obj["date"], obj["hour"]), "price": obj["price"]}
        for obj in price_json.values()
    ]

query = sqlalchemy.insert(table)
result_proxy = connection.execute(query, prices)
