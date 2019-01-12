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
    query = food.replace(' ','%20')
    # print(food)
    url = ('https://api.nal.usda.gov/ndb/search/?format=json&q='+query+'&sort=r&max=10&offset=0&api_key='+API_KEY)
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    # print(raw_json)
    for item in raw_json["list"]['item']:
        # print(item['group'])
        if item['group'] != "Branded Food Products Database":
            requirements = food.split(' ')
            # print(requirements)
            if all(requirement.upper() in item['name'].upper() for requirement in requirements):
                # print(item['ndbno'])
                return item['ndbno']
    return -1

def get_food_calories(ndbno):
    info = []
    if ndbno == -1:
        return False
    else:
        url = ('https://api.nal.usda.gov/ndb/V2/reports?ndbno='+ndbno+'&type=f&format=json&api_key='+API_KEY)
        response = urllib.request.urlopen(url)
        raw_json = json.loads(response.read())
        calories = 0
        for row in raw_json['foods'][0]['food']['nutrients']:
            # print(row['unit'])
            if(row['unit'] == 'kcal'):
                print(row['value'])
                calories = row['value']
        return calories

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
    # print(repr(amount))
    try:
        calories = convert_calories(meal, amount)
    except:
        calories = 0
        return False
    print(calories)
    params = (user_id, year, month, day, hour, minute, meal, amount, calories)
    c.execute("INSERT INTO food_log (user_id, year, month, day, hour, minute, meal, amount, calories) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
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
    db.close()
    return today_food

def convert_calories(meal, amount):
    calories = get_food_calories(get_food_ndbno(meal))
    print(calories)
    calories = calories * float(amount) / 100
    print(calories)
    return calories

def get_total_calories(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    command = "SELECT calories FROM food_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
    c.execute(command)
    data = c.fetchall()
    db.close()
    total = 0
    # print(data)
    for row in data:
        if row[0] != None:
            # print (row[0])
            total += row[0]
    # print(data)
    return total

# print(get_food_ndbno("pork cured"))
# print(add_food("banana", 118.0, "test"))
# print(get_total_calories('test'))
