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
    c.execute("CREATE TABLE IF NOT EXISTS basic_info (user_id INTEGER, height REAL, weight REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS water (user_id INTEGER, current_intake REAL, expected_intake REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS diet (user_id INTEGER, allergies TEXT, carbs REAL, protein REAL, fat REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS expected_diet (user_id INTEGER, expected_carbs REAL, expected_protein REAL, expected_fat REAL)")

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

create_table()
