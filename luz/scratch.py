
import requests
from datetime import datetime

from pprint import pp

from functools import reduce

def get_timestamp(date, hour):
    day, month, year = date.split("-")
    hour, _ = hour.split("-")

    dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))
    return int(dt.timestamp())


response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")

price_json = response.json()

def reducer(acc: list, keyval):
    acc.append((keyval[0], keyval[1]["price"]))
    return acc
    
pp(reduce(reducer, price_json.items(), []))