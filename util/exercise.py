import json
import urllib.request
import sqlite3

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

with open('data/keys.json', 'r') as f:
    api_dict = json.load(f)

API_KEY = api_dict["WORKOUT_MANAGER_API"]

def get_category_id(category):
    url = ('https://wger.de/api/v2/exercisecategory/?format=json')
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    for exercise in raw_json["results"]:
        if exercise["name"] == category:
            return exercise["id"]
    return -1

def list_category_exercises(id):
    url = ('https://wger.de/api/v2/exercise/?format=json&language=2&category='+str(id))
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    exercises = []
    for exercise in raw_json["results"]:
        if exercise["name"] != "" and exercise['name'] != "Awesome":
            exercises.append(exercise["name"])
        else:
            # exercises.append(exercise["name"])
            pass
    return exercises

def get_all_categories():
    url = ('https://wger.de/api/v2/exercisecategory/?format=json')
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    categories = []
    for category in raw_json["results"]:
        if category["name"] != '':
            categories.append(category["name"])
    return categories

def get_user_exercise(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    print(user_id)
    command = "SELECT * FROM exercise_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    data = c.fetchall()
    total_exercise = -1
    # print(data)
    for row in data:
        # print(row)
        total_exercise = row[4] + row[5] + row[6] + row[7] + row[8] + row[9] + row[10]
    db.close()

    return total_exercise

def update_user_log(username):
    return True
# print(list_category_exercises(get_category_id("Arms")))
