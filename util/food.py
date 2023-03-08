import json
import urllib.request
import sqlite3
from datetime import datetime

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

with open('keys/usda_nutrients_api.json', 'r') as f:
    api_dict = json.load(f)

API_KEY = api_dict["USDA_NUTRIENTS_API_KEY"]

def get_food_ndbno(food):
    '''This function gets the food's ndbno, which is the food's id in the API. It is necessary for getting all the nutrition information on the food.'''
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
    '''This function gets the total calories of the food by getting the json from the USDA Nutrients API.'''
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

def get_food_carbs(ndbno):
    '''This function gets the total carbohydrates of the food by getting the json from the USDA Nutrients API.'''
    info = []
    if ndbno == -1:
        return False
    else:
        url = ('https://api.nal.usda.gov/ndb/V2/reports?ndbno='+ndbno+'&type=f&format=json&api_key='+API_KEY)
        response = urllib.request.urlopen(url)
        raw_json = json.loads(response.read())
        carbs = 0
        for row in raw_json['foods'][0]['food']['nutrients']:
            # print(row['unit'])
            if(row['name'] == 'Carbohydrate, by difference'):
                print(row['value'])
                carbs = row['value']
        return carbs

def get_food_protein(ndbno):
    '''This function gets the total protein of the food by getting the json from the USDA Nutrients API.'''
    info = []
    if ndbno == -1:
        return False
    else:
        url = ('https://api.nal.usda.gov/ndb/V2/reports?ndbno='+ndbno+'&type=f&format=json&api_key='+API_KEY)
        response = urllib.request.urlopen(url)
        raw_json = json.loads(response.read())
        protein = 0
        for row in raw_json['foods'][0]['food']['nutrients']:
            # print(row['unit'])
            if(row['name'] == 'Protein'):
                print(row['value'])
                protein = row['value']
        return protein

def get_food_fat(ndbno):
    '''This function iterates through the json file, adding each kind of fat to the total amount of fat the food has after getting the json from the USDA Nutrients API.'''
    info = []
    if ndbno == -1:
        return False
    else:
        url = ('https://api.nal.usda.gov/ndb/V2/reports?ndbno='+ndbno+'&type=f&format=json&api_key='+API_KEY)
        response = urllib.request.urlopen(url)
        raw_json = json.loads(response.read())
        fat = 0
        for row in raw_json['foods'][0]['food']['nutrients']:
            # print(row['unit'])
            if('Fatty acids' in row['name']):
                print(row['value'])
                fat += row['value']
        return fat

def add_food(meal, amount, username):
    '''This function adds all the information about the food that the user has eaten into the database.'''
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
        carbs = convert_carbs(meal, amount)
        protein = convert_protein(meal, amount)
        fat = convert_fat(meal, amount)
    except:
        calories = 0
        carbs = 0
        protein = 0
        fat = 0
        return False
    print(calories)
    params = (user_id, year, month, day, hour, minute, meal, amount, calories, carbs, protein, fat)
    c.execute("INSERT INTO food_log (user_id, year, month, day, hour, minute, meal, amount, calories, carbs, protein, fat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
    db.commit()
    db.close()
    return True

def get_user_food(username):
    '''This function retrieves the meal, amount, and the time it was eaten about all the food the user has eaten today and returns it as a list.'''
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
    '''This function converts the amount of calories consumed by the user based on the proportion given by the USDA Nutrients API.'''
    calories = get_food_calories(get_food_ndbno(meal))
    # print(calories)
    calories = calories * float(amount) / 100
    # print(calories)
    return calories

def convert_carbs(meal, amount):
    '''This function converts the amount of carbohydrates consumed by the user based on the proportion given by the USDA Nutrients API.'''
    carbs = get_food_carbs(get_food_ndbno(meal))
    # print(carbs)
    carbs = carbs * float(amount) / 100
    # print(carbs)
    return carbs

def convert_protein(meal, amount):
    '''This function converts the amount of protein consumed by the user based on the proportion given by the USDA Nutrients API.'''
    protein = get_food_protein(get_food_ndbno(meal))
    # print(protein)
    protein = protein * float(amount) / 100
    # print(protein)
    return protein

def convert_fat(meal, amount):
    '''This function converts the amount of fat consumed by the user based on the proportion given by the USDA Nutrients API.'''
    fat = get_food_fat(get_food_ndbno(meal))
    # print(fat)
    fat = fat * float(amount) / 100
    # print(fat)
    return fat

def get_total_calories(username):
    '''This function retrieves the total amount of calories based on all the food the user has eaten today.'''
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

def get_total_carbs(username):
    '''This function retrieves the total amount of carbohydrates based on all the food the user has eaten today.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    command = "SELECT carbs FROM food_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
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

def get_total_protein(username):
    '''This function retrieves the total amount of protein based on all the food the user has eaten today.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    command = "SELECT protein FROM food_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
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

def get_total_fat(username):
    '''This function retrieves the total amount of fat based on all the food the user has eaten today.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    command = "SELECT fat FROM food_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
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

# print(get_food_ndbno("beef"))
# print(convert_carbs("beef", 100))
# print(convert_fat("beef", 100))
# print(add_food("beef", 100.0, "test"))
# print(get_total_calories('test'))
