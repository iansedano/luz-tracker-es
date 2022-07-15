import requests
from pprint import pp

response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")

pp(response.json())