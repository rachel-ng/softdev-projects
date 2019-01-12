import json
import urllib.request
import sqlite3
from datetime import datetime

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

with open('keys/keys.json', 'r') as f:
    api_dict = json.load(f)

API_KEY = api_dict["USDA_NUTRIENTS_API"]

def get_food_ndbno(food):
    url = ('https://api.nal.usda.gov/ndb/search/?format=json&q='+food+'&sort=r&max=25&offset=0&api_key='+API_KEY)
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    for item in raw_json["list"]['item']:
        if food in item['name'] or food.upper() in item['name']:
            return item['ndbno']
    return -1

def get_food_nutrients(ndbno):
    info = []
    url = ('https://api.nal.usda.gov/ndb/V2/reports?ndbno='+ndbno+'&type=f&format=json&api_key='+API_KEY)
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())

    calories = raw_json['foods'][0]['food']['nutrients'][0]['value']
    print(calories)
# print(get_food_ndbno("milk"))
get_food_nutrients(get_food_ndbno('milk'))
