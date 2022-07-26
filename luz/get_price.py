from datetime import datetime
from functools import reduce
from pprint import pp

import requests

from luz.mongo import get_prices_collection


def get_timestamp(date, hour):
    day, month, year = date.split("-")
    hour, _ = hour.split("-")

    dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))
    return int(dt.timestamp())


def get_datetime(date, hour):
    day, month, year = date.split("-")
    hour, _ = hour.split("-")

    return datetime(year=int(year), month=int(month), day=int(day), hour=int(hour))


def pprint_api_data(price_json) -> None:
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


def send_data_to_mongo(api_data) -> None:
    collection = get_prices_collection()
    collection.insert_many(api_data)


if __name__ == "__main__":
    send_data_to_mongo(get_data_from_api())
