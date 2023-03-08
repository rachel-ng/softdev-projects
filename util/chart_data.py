import sqlite3
from datetime import datetime

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

def get_user_water (username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))

    c.execute(command)
    user_id = c.fetchone()[0]
    current_weekday = datetime.now().weekday()
    command = "SELECT year, month, day, week_start_day FROM water_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    data = c.fetchone()
    year = data[0]
    month = data[1]
    day = data[2]
    weekday = data[3]

    command = "SELECT intake_01, intake_02, intake_03, intake_04, intake_05, intake_06, intake_07 FROM water_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
    c.execute(command)
    data = c.fetchall()

    water_data = []

    for row in data:
        water_data = row

    db.close()
    return (water_data)

def get_user_sleep (username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))

    c.execute(command)
    user_id = c.fetchone()[0]
    current_weekday = datetime.now().weekday()
    command = "SELECT year, month, day, week_start_day FROM sleep_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    data = c.fetchone()
    year = data[0]
    month = data[1]
    day = data[2]
    weekday = data[3]

    command = "SELECT hours_01, start_01, hours_02, start_02, hours_03, start_03, hours_04, start_04, hours_05, start_05, hours_06, start_06, hours_07, start_07 FROM sleep_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
    c.execute(command)
    data = c.fetchall()

    sleep_data = []

    for row in data:
        sleep_data = row

    db.close()
    return (sleep_data)

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
    command = "SELECT hour, minute, meal, calories FROM food_log WHERE user_id={} AND year={} AND month={} AND day={}".format(repr(user_id), repr(year), repr(month), repr(day))
    c.execute(command)
    data = c.fetchall()
    for row in data:
        today_food.append(row)
    db.close()
    return today_food

def get_user_exercise(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    command = "SELECT hours_01, hours_02, hours_03, hours_04, hours_05, hours_06, hours_07 FROM exercise_log WHERE user_id={} AND year={} AND month={}".format(repr(user_id), repr(year), repr(month))
    c.execute(command)
    data = c.fetchall()
    print(data)

    exercise_data = []
    for row in data:
        exercise_data = row

    db.close()
    return (exercise_data)
