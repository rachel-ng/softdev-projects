import sqlite3
from datetime import datetime
from passlib.hash import sha256_crypt

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

def create_table():
    ''' This function creates all the tables in the database if they do not exist.'''
    db = sqlite3.connect(DB_FILE)

    #used to traverse db
    c = db.cursor() #facilitate db ops

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS basic_info (user_id INTEGER, goal TEXT, age INTEGER, height REAL, weight REAL, allergies TEXT, dietary_restrictions TEXT, expected_calories INTEGER, expected_carbs INTEGER, expected_protein INTEGER, expected_fat INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS water_log (user_id INTEGER, year INTEGER, month INTEGER, day INTEGER, week_start_day INTEGER, intake_01 REAL, intake_02 REAL, intake_03 REAL, intake_04 REAL, intake_05 REAL, intake_06 REAL, intake_07 REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS exercise_log (user_id INTEGER, year INTEGER, month INTEGER, day INTEGER, week_start_day INTEGER, hours_01 INTEGER, hours_02 INTEGER, hours_03 INTEGER, hours_04 INTEGER, hours_05 INTEGER, hours_06 INTEGER, hours_07 INTEGER, target_muscle_group_01 TEXT, target_muscle_group_02 TEXT, target_muscle_group_03 TEXT, target_muscle_group_04 TEXT, target_muscle_group_05 TEXT, target_muscle_group_06 TEXT, target_muscle_group_07 TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS sleep_log (user_id INTEGER, year INTEGER, month INTEGER, day INTEGER, week_start_day INTEGER, hours_01 REAL, start_01 REAL, hours_02 REAL, start_02 REAL, hours_03 REAL, start_03 REAL, hours_04 REAL, start_04 REAL, hours_05 REAL, start_05 REAL, hours_06 REAL, start_06 REAL, hours_07 REAL, start_07 REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS food_log (user_id INTEGER, year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minute INTEGER, meal TEXT, amount REAL, calories INTEGER, carbs INTEGER, protein INTEGER, fat INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS weekly_diet (user_id INTEGER, year INTEGER, month INTEGER, week_start_day INTEGER, calories_01 INTEGER, carbs_01 INTEGER, protein_01 INTEGER, fat_01 INTEGER, calories_02 INTEGER, carbs_02 INTEGER, protein_02 INTEGER, fat_02 INTEGER, calories_03 INTEGER, carbs_03 INTEGER, protein_03 INTEGER, fat_03 INTEGER, calories_04 INTEGER, carbs_04 INTEGER, protein_04 INTEGER, fat_04 INTEGER, calories_05 INTEGER, carbs_05 INTEGER, protein_05 INTEGER, fat_05 INTEGER, calories_06 INTEGER, carbs_06 INTEGER, protein_06 INTEGER, fat_06 INTEGER, calories_07 INTEGER, carbs_07 INTEGER, protein_07 INTEGER, fat_07 INTEGER)")

    db.commit() #save changes
    db.close()

def register(username, password):
    '''This function adds the user to the database.
    If username already exists, returns false. Otherwise, the function inserts a row in users and returns true.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users;")
    for row in data:
        if username == row[1]:
            return False
    params = (username, sha256_crypt.hash(password))
    c.execute("INSERT INTO users (user, password) VALUES (?, ?)", params)
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    params = (user_id, 2000, 275, 60, 51)
    c.execute("INSERT INTO basic_info (user_id, expected_calories, expected_carbs, expected_protein, expected_fat) VALUES(?, ?, ?, ?, ?)", params)
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    current_weekday = datetime.now().weekday()

    params = (user_id, current_year, current_month, current_day, current_weekday, 0, 0, 0, 0, 0, 0, 0)
    c.execute("INSERT INTO exercise_log (user_id, year, month, day, week_start_day, hours_01, hours_02, hours_03, hours_04, hours_05, hours_06, hours_07) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

    c.execute("INSERT INTO water_log (user_id, year, month, day, week_start_day, intake_01, intake_02, intake_03, intake_04, intake_05, intake_06, intake_07) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

    params = (user_id, current_year, current_month, current_day, current_weekday, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    c.execute("INSERT INTO sleep_log (user_id, year, month, day, week_start_day, hours_01, start_01, hours_02, start_02, hours_03, start_03, hours_04, start_04, hours_05, start_05, hours_06, start_06, hours_07, start_07) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

    db.commit()
    db.close()
    return True

def authenticate(username, password):
    '''This function checks user login. If username and encrypted password match, the function returns true. The function returns false otherwise.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users")
    for row in data:
        if row[1] == username and sha256_crypt.verify(password, row[2]):
            db.close()
            return True
    db.close()
    return False

def add_info(age, height, weight, allergies, dietary_restrictions, username):
    '''This function adds the basic information (height, age, weight, allergies, dietary restrictions) for each user to the database by taking the user's username as a parameter.'''
    if height == '' or weight == '':
        return False
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    command = "SELECT user_id FROM basic_info WHERE user_id={}".format(user_id)
    c.execute(command)

    if c.fetchone() == None: # if user has not yet added their info
        params = (user_id, age, height, weight, allergies, dietary_restrictions)
        c.execute("INSERT INTO basic_info (user_id, age, height, weight) VALUES (?, ?, ?, ?, ?, ?)", params)
    else:
        command = "UPDATE basic_info SET age=\"{}\", height=\"{}\", weight=\"{}\", allergies=\"{}\", dietary_restrictions=\"{}\" WHERE user_id={}".format(age, height, weight, allergies, dietary_restrictions, user_id)
        c.execute(command)
    db.commit()
    db.close()
    return True

def get_info(username):
    '''This function gets all the basic information of the user to be presented on the profile page.'''
    info = []
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    command = "SELECT age, height, weight, allergies, dietary_restrictions FROM basic_info WHERE user_id={}".format(user_id)
    c.execute(command)
    data = c.fetchone()
    for item in data:
        if item == None:
            info.append('')
        else:
            info.append(item)
    db.close()
    return info

def get_user_goal(username):
    '''This function gets the user's daily goal from the database to show on the page.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    command = "SELECT goal FROM basic_info WHERE user_id={}".format(user_id)
    c.execute(command)
    goal = c.fetchone()[0]
    return goal

def update_user_goal(username, goal):
    '''This function updates the user's existing daily goal with a new one in the database.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]

    command = "SELECT goal FROM basic_info WHERE user_id={}".format(user_id)
    c.execute(command)

    if c.fetchone() == None: # if user has not yet added their info
        params = (user_id, goal)
        c.execute("INSERT INTO basic_info (user_id, goal) VALUES (?, ?)", params)
    else:
        command = "UPDATE basic_info SET goal=\"{}\" WHERE user_id={}".format(goal, user_id)
        c.execute(command)
    db.commit()
    db.close()
    return True

create_table()
# register("a", "a")
