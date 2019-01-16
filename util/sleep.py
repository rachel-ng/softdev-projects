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
    command = "SELECT week_start_day FROM sleep_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    start = c.fetchone()[0]
    current_weekday = int(datetime.now().weekday())
    difference = int(start) - current_weekday
    column = "hours_0" + str(difference+1)
    command = "SELECT {} FROM sleep_log WHERE user_id={}".format(column, repr(user_id))
    c.execute(command)
    data = c.fetchone()[0]
    total_sleep = data
    db.close()
    return total_sleep

def update_user_log(username, delta, start):
    if delta == '' or start == '':
        return False
    else:
        print(delta)
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        command = "SELECT id from users WHERE user={}".format(repr(username))
        c.execute(command)
        user_id = c.fetchone()[0]
        #print(user_id)
        command = "SELECT year, month, day, week_start_day FROM sleep_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
        data = c.fetchone()
        year = data[0]
        month = data[1]
        day = data[2]
        weekday = data[3]
        current_weekday = datetime.now().weekday()
        current_hours = 0
        if datetime.now().year == year and datetime.now().month == month and datetime.now().day - day < 7:
            if current_weekday == weekday:
                command = "SELECT hours_01 from sleep_log WHERE user_id={}".format(repr(user_id))
                c.execute(command)
                current_hours = c.fetchone()[0]
                delta = float(delta)
                delta += float(current_hours)
                command = "UPDATE sleep_log SET hours_01=\"{}\", start_01=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)
            elif current_weekday == weekday + 1:
                command = "UPDATE sleep_log SET hours_02=\"{}\", start_02=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)

            elif current_weekday == weekday + 2:
                command = "UPDATE sleep_log SET hours_03=\"{}\", start_03=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)

            elif current_weekday == weekday + 3:
                command = "UPDATE sleep_log SET hours_04=\"{}\", start_04=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)

            elif current_weekday == weekday + 4:
                command = "UPDATE sleep_log SET hours_05=\"{}\", start_05=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)

            elif current_weekday == weekday + 5:
                command = "UPDATE sleep_log SET hours_06=\"{}\", start_06=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)

            elif current_weekday == weekday + 6:
                command = "UPDATE sleep_log SET hours_07=\"{}\", start_07=\"{}\" WHERE user_id={}".format(delta, start, user_id)
                c.execute(command)

        else:
            command = "UPDATE sleep_log SET year=\"{}\", month=\"{}\", day=\"{}\", week_start_day=\"{}\", hours_01=\"{}\", start_01 WHERE user_id={}".format(year, month, day, week_start_day, delta, start, user_id)
            c.execute(command)
        db.commit()
        db.close()
        return True

def get_diff(start, end):
    FMT = '%H:%M'
    tdelta = (datetime.strptime(end, FMT) - datetime.strptime(start, FMT))
    # print(type(tdelta))
    tdelta = tdelta / timedelta(hours=1)
    # print(tdelta)
    # print(tdelta.minutes)
    # if tdelta.days < 0:
    #     tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    return tdelta

def convert(hour, min, time):
    if hour == 12 and time == 0:
        hour = 0
    elif hour == 12 and time == 1:
        hour = 12
    else:
        hour = (time * 12) + hour
    final = str(hour) + ":" + "{:02d}".format(min)
    # print (final)
    return final


# get_user_sleep("a");
# print(convzert())
