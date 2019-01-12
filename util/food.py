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
    # print(calories)

def add_food(meal, amount, username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour = datetime.now().hour
    minute = datetime.now().minute
    params = (user_id, year, month, day, hour, minute, meal, amount)
    c.execute("INSERT INTO food_log (user_id, year, month, day, hour, minute, meal, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", params)
    db.commit()
    db.close()
    return True

def get_user_food(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    today_food = []
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    command = "SELECT hour, minute, meal, amount FROM food_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
    c.execute(command)
    data = c.fetchall()
    # print(data)
    for row in data:
        today_food.append(row)
        # print(row[0])
    return today_food
# print(get_food_ndbno("milk"))
# get_food_nutrients(get_food_ndbno('milk'))
