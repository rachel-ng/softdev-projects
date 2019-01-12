import json
import urllib.request
import sqlite3
from datetime import datetime
#opens if db exist, otherwise create
#remember to change route!
DB_FILE = "data/health.db"

#with open('data/keys.json', 'r') as f:
#    api_dict = json.load(f)

def convert_measure(measurement, amount):
    '''Converts all liquid measurements to fluid ounces.'''

    if measurement == 0:
        return (amount * 8)
    elif measurement == 1:
        return amount
    else:
        return (round(amount / 29.57) , 2)

def calc_percentage(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    weekday = datetime.today().weekday()
    column = column = "intake_0" + str(weekday)
    #print(column)
    command = "SELECT {} FROM water_log WHERE user_id={}".format(column, user_id)
    c.execute(command)
    data = c.fetchone()[0]
    #print(data)
    db.close()
    return round((data/64.0 * 100), 2)

def get_user_water(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    #print(user_id)
    column = "intake_0" + str(datetime.today().isoweekday())
    command = "SELECT {} FROM water_log WHERE user_id={}".format(column, repr(user_id))
    c.execute(command)
    data = c.fetchone()[0]
    total_water = data

    db.close()
    return total_water

def update_user_log(username, input):
    if input == '' or input == None:
        return False
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        command = "SELECT id from users WHERE user={}".format(repr(username))
        c.execute(command)
        user_id = c.fetchone()[0]
        #print(user_id)
        command = "SELECT year, month, day, week_start_day FROM water_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
        data = c.fetchone()
        #print(data)
        year = data[0]
        month = data[1]
        day = data[2]
        weekday = data[3]

        input = get_user_water(username) + input
        if datetime.now().year == year and datetime.now().month == month and datetime.now().day - day < 7:
            column = "intake_0" + str(weekday)
            command = "UPDATE water_log SET {} = \"{}\" WHERE user_id = {}".format(column, input, user_id )
            c.execute(command)
        else:
            command = "UPDATE water_log SET year=\"{}\", month=\"{}\", day=\"{}\", week_start_day=\"{}\", hours_01=\"{}\" WHERE user_id={}".format(year, month, day, week_start_day, hours, user_id)
            c.execute(command)

    db.commit()
    db.close()
    return True
