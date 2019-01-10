import json
import urllib.request

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

# print(list_category_exercises(get_category_id("Arms")))
