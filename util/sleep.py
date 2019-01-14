import json
import urllib.request
import sqlite3
from datetime import datetime, timedelta
#opens if db exist, otherwise create
#remember to change route!
DB_FILE = "data/health.db"

#with open('data/keys.json', 'r') as f:
#    api_dict = json.load(f)

def get_user_sleep(username):
    print(str(datetime.today().isoweekday()))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    #print(user_id)
    column = "hours_0" + str(datetime.today().isoweekday())
    print("getting user sleep")
    print(column)
    command = "SELECT {} FROM sleep_log WHERE user_id={}".format(column, repr(user_id))
    c.execute(command)
    data = c.fetchone()[0]
    total_sleep = data

    db.close()
    return total_sleep

def update_user_log(username, input):
    if input == '':
        return False
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        command = "SELECT id from users WHERE user={}".format(repr(username))
        c.execute(command)
        user_id = c.fetchone()[0]
        #print(user_id)
        command = "SELECT year, month, day, week_start_day FROM sleep_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
        data = c.fetchone()
        print(data)
        year = data[0]
        month = data[1]
        day = data[2]
        weekday = data[3]

        if datetime.now().year == year and datetime.now().month == month and datetime.now().day - day < 7:
            column = "hours_0" + str(weekday + 1)
            print("putting in user sleep")
            print(column)

            command = "UPDATE sleep_log SET {} = \"{}\" WHERE user_id = {}".format(column, input, user_id )
            print(command)
            c.execute(command)
        else:
            command = "UPDATE sleep_log SET year=\"{}\", month=\"{}\", day=\"{}\", week_start_day=\"{}\", hours_01=\"{}\" WHERE user_id={}".format(year, month, day, week_start_day, hours, user_id)
            c.execute(command)

    db.commit()
    db.close()
    return True

def get_diff(start, end):
    FMT = '%H:%M'
    tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
    if tdelta.days < 0:
        tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    print (tdelta)
    return tdelta

def convert(hour, min, time):
    if hour == 12 and time == 0:
        hour = 0
    elif hour == 12 and time == 1:
        hour = 12
    else:
        hour = (time * 12) + hour
    final = str(hour) + ":" + "{:02d}".format(min)
    print (final)
    return final


get_user_sleep("a");
