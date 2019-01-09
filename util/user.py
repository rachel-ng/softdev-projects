import sqlite3
from passlib.hash import sha256_crypt

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

def create_table():
    ''' This function creates a Users table in database with column names username and password.'''
    db = sqlite3.connect(DB_FILE)

    #used to traverse db
    c = db.cursor() #facilitate db ops

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS basic_info (user_id INTEGER, height REAL, weight REAL, allergies TEXT, dietary_restrictions TEXT, expected_calories INTEGER, expected_carbs INTEGER, expected_protein INTEGER, expected_fat INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS water_log (user_id INTEGER, year INTEGER, month INTEGER, week_start_day INTEGER, intake_01 REAL, intake_02 REAL, intake_03 REAL, intake_04 REAL, intake_05 REAL, intake_06 REAL, intake_07 REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS exercise_log (user_id INTEGER, year INTEGER, month INTEGER, week_start_day INTEGER, hours_01 REAL, hours_02 REAL, hours_03 REAL, hours_04 REAL, hours_05 REAL, hours_06 REAL, hours_07 REAL, target_muscle_group_01 TEXT, target_muscle_group_02 TEXT, target_muscle_group_03 TEXT, target_muscle_group_04 TEXT, target_muscle_group_05 TEXT, target_muscle_group_06 TEXT, target_muscle_group_07 TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS sleep_log (user_id INTEGER, year INTEGER, month INTEGER, week_start_day INTEGER, hours_01 REAL, hours_02 REAL, hours_03 REAL, hours_04 REAL, hours_05 REAL, hours_06 REAL, hours_07 REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS food_log (user_id INTEGER, year INTEGER, month INTEGER, day INTEGER, time INTEGER, meal TEXT, calories INTEGER, carbs INTEGER, protein INTEGER, fat INTEGER)")
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

def add_info(height, weight, username):
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
        params = (user_id, height, weight)
        c.execute("INSERT INTO basic_info (user_id, height, weight) VALUES (?, ?, ?)", params)
    else:
        command = "UPDATE basic_info SET height=\"{}\", weight=\"{}\" WHERE user_id={}".format(height, weight, user_id)
        c.execute(command)
    db.commit()
    db.close()
    return True

create_table()
