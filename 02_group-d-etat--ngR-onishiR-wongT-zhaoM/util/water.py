import json
import urllib.request
import sqlite3

from datetime import datetime

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

def convert_measure(measurement, amount):
    '''Converts all liquid measurements to fluid ounces.'''
    # measurement given in cups
    if measurement == 0:
        # fl. oz = cups * 8
        return (amount * 8)
    # measurement given in fl. oz
    elif measurement == 1:
        # no converting necessary
        return amount
    # measurement given in mL
    else:
        # fl. oz = mL / 29.57,  rounded to two decimal places
        #print (str(round((amount / 29.57) , 2)))
        return (round((amount / 29.57) , 2))

def calc_percentage(username):
    '''Calculates percentage of recommended daily water intake user has drank on that day.'''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # find user in database and get user_id
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    # retrieves the amount of water drank on that day
    weekday = datetime.today().isoweekday()
    column = column = "intake_0" + str(weekday)
    #print(column)
    command = "SELECT {} FROM water_log WHERE user_id={}".format(column, user_id)
    #print ("getting user water")
    #print(column)
    c.execute(command)
    data = c.fetchone()[0]
    #print(data)
    db.close()

    # turns retrieved amount into percentage of recommended drank
    return round((data/64.0 * 100), 2)

def get_user_water(username):
    '''Retrieves user's water intake for the day.'''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # gets user_id from username
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    #print(user_id)

    # gets column name based on weekday
    column = "intake_0" + str(datetime.today().isoweekday())
    #print ("setting user water")
    #print(column)
    command = "SELECT {} FROM water_log WHERE user_id={}".format(column, repr(user_id))
    c.execute(command)
    data = c.fetchone()[0]
    total_water = data

    db.close()
    return total_water

def update_user_log(username, input):
    '''Updates the user's water_log with the inputted water.'''

    # checks if input is an empty string or NULL
    if input == '' or input == None:
        return False
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        command = "SELECT id from users WHERE user={}".format(repr(username))
        c.execute(command)
        user_id = c.fetchone()[0]
        #print(user_id)

        # retrieves year, month, day, and the day the week started and stores it into separate variables
        command = "SELECT year, month, day, week_start_day FROM water_log WHERE user_id={}".format(repr(user_id))
        c.execute(command)
        data = c.fetchone()
        #print(data)
        year = data[0]
        month = data[1]
        day = data[2]
        weekday = data[3] + 1

        # takes past water consumption and adds it to new water input
        input = get_user_water(username) + input

        # if within the same week of the same month and year, update the log by adding the input to the correct column
        if datetime.now().year == year and datetime.now().month == month and datetime.now().day - day < 7:
            column = "intake_0" + str(weekday)
            command = "UPDATE water_log SET {} = \"{}\" WHERE user_id = {}".format(column, input, user_id )
            c.execute(command)
        # if not within the week, replace the year, month, and day values so that the current day is the new start day, and the other values reflect this
        else:
            command = "UPDATE water_log SET year=\"{}\", month=\"{}\", day=\"{}\", week_start_day=\"{}\", hours_01=\"{}\" WHERE user_id={}".format(year, month, day, week_start_day, hours, user_id)
            c.execute(command)

    db.commit()
    db.close()
    return True
