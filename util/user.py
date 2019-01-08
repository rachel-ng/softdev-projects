#code to create user table in database.db
import sqlite3
from passlib.hash import sha256_crypt

#opens if db exist, otherwise create
DB_FILE = "health.db"

def create_table():
    ''' This function creates a Users table in database with column names username and password.'''
    db = sqlite3.connect(DB_FILE)

    #used to traverse db
    c = db.cursor() #facilitate db ops

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS basic_info (user_id INTEGER, height REAL, weight REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS water (user_id INTEGER, current_intake REAL, expected_intake REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS sleep (user_id INTEGER, current_intake REAL, expected_intake REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS diet (user_id INTEGER, allergies TEXT, carbs REAL, protein REAL, fat REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS expected_diet (user_id INTEGER, expected_carbs REAL, expected_protein REAL, expected_fat REAL)")

    db.commit() #save changes
    db.close()

# create_table()
