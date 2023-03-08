import json
import urllib.request
import sqlite3
from datetime import datetime

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

def get_category_id(category):
    '''This function takes in the category and gets the id that the category is in the Workout Manager API.'''
    url = ('https://wger.de/api/v2/exercisecategory/?format=json')
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    for exercise in raw_json["results"]:
        if exercise["name"] == category:
            return exercise["id"]
    return -1

def list_category_exercises(id):
    '''This function lists all the exercises that are in the category selected to show as recommendations for the user.'''
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
    '''This function gets all the available muscle group categories to allow the user to select which category to search for recommendations or select as the muscle group they worked out.'''
    url = ('https://wger.de/api/v2/exercisecategory/?format=json')
    response = urllib.request.urlopen(url)
    raw_json = json.loads(response.read())
    categories = []
    for category in raw_json["results"]:
        if category["name"] != '':
            categories.append(category["name"])
    return categories

def get_user_exercise(username):
    '''This function gets the total hours of exercise the user has done this week.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    # print(user_id)
    command = "SELECT * FROM exercise_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    data = c.fetchall()
    total_exercise = -1
    # print(data)
    for row in data:
        # print(row[5])
        total_exercise = row[5] + row[6] + row[7] + row[8] + row[9] + row[10] + row[11]
    db.close()

    return total_exercise

def update_user_log(hours, category, username):
    '''This function updates the exercise log in the database based on the user's input on the hours exercised and the category.'''
    if hours == '' or category == '':
        return False
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        command = "SELECT id from users WHERE user={}".format(repr(username))
        c.execute(command)
        user_id = c.fetchone()[0]
        # print(user_id)
        current_weekday = datetime.now().weekday()
        # print(current_weekday)
        command = "SELECT year, month, day, week_start_day FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
        data = c.fetchone()
        year = data[0]
        month = data[1]
        day = data[2]
        weekday = data[3]
        current_hours = 0
        if datetime.now().year == year and datetime.now().month == month and datetime.now().day - day < 7:
            if current_weekday == weekday:
                command = "SELECT hours_01 from exercise_log WHERE user_id={}".format(repr(user_id))
                c.execute(command)
                current_hours = c.fetchone()[0]
                print(current_hours)
                # print(hours)
                hours = int(hours)
                hours += int(current_hours)
                # print(hours)
                command = "UPDATE exercise_log SET hours_01=\"{}\", target_muscle_group_01=\"{}\" WHERE user_id={}".format(repr(hours), category, user_id)
                c.execute(command)
            elif current_weekday == weekday + 1:
                command = "UPDATE exercise_log SET hours_02=\"{}\", target_muscle_group_02=\"{}\" WHERE user_id={}".format(hours, category, user_id)
                c.execute(command)
            elif current_weekday == weekday + 2:
                command = "UPDATE exercise_log SET hours_03=\"{}\", target_muscle_group_03=\"{}\" WHERE user_id={}".format(hours, category, user_id)
                c.execute(command)
            elif current_weekday == weekday + 3:
                command = "UPDATE exercise_log SET hours_04=\"{}\", target_muscle_group_04=\"{}\" WHERE user_id={}".format(hours, category, user_id)
                c.execute(command)
            elif current_weekday == weekday + 4:
                command = "UPDATE exercise_log SET hours_05=\"{}\", target_muscle_group_05=\"{}\" WHERE user_id={}".format(hours, category, user_id)
                c.execute(command)
            elif current_weekday == weekday + 5:
                command = "UPDATE exercise_log SET hours_06=\"{}\", target_muscle_group_06=\"{}\" WHERE user_id={}".format(hours, category, user_id)
                c.execute(command)
            elif current_weekday == weekday + 6:
                command = "UPDATE exercise_log SET hours_07=\"{}\", target_muscle_group_07=\"{}\"WHERE user_id={}".format(hours, category, user_id)
                c.execute(command)
        else:
            command = "UPDATE exercise_log SET year=\"{}\", month=\"{}\", day=\"{}\", week_start_day=\"{}\", hours_01=\"{}\" WHERE user_id={}".format(year, month, day, week_start_day, hours, user_id)
            c.execute(command)
        db.commit()
        db.close()
    return True

def get_user_category(username):
    '''This function gets the muscle group category that the user has last worked out today.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    # print(user_id)
    current_weekday = datetime.now().weekday()
    command = "SELECT week_start_day FROM exercise_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    weekday = c.fetchone()[0]
    if current_weekday == weekday:
        command = "SELECT target_muscle_group_01 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    elif current_weekday == weekday + 1:
        command = "SELECT target_muscle_group_02 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    elif current_weekday == weekday + 2:
        command = "SELECT target_muscle_group_03 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    elif current_weekday == weekday + 3:
        command = "SELECT target_muscle_group_04 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    elif current_weekday == weekday + 4:
        command = "SELECT target_muscle_group_05 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    elif current_weekday == weekday + 5:
        command = "SELECT target_muscle_group_06 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    elif current_weekday == weekday + 6:
        command = "SELECT target_muscle_group_07 FROM exercise_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
    category = c.fetchone()[0]
    db.close()
    return category
# print(list_category_exercises(get_category_id("Arms")))
