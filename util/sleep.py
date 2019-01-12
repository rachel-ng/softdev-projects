import json
import urllib.request
import sqlite3

#opens if db exist, otherwise create
#remember to change route!
DB_FILE = "../data/health.db"

#with open('data/keys.json', 'r') as f:
#    api_dict = json.load(f)

def get_user_sleep(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id from users WHERE user={}".format(repr(username))
    c.execute(command)
    user_id = c.fetchone()[0]
    #print(user_id)
    command = "SELECT * FROM sleep_log WHERE user_id={}".format(repr(user_id))
    c.execute(command)
    data = c.fetchall()
    print(data)
    total_sleep = -1
    # print(data)
    for row in data:
        print(row)
        total_sleep = row[4] + row[5] + row[6] + row[7] + row[8] + row[9] + row[10]
    db.close()

    return total_sleep

def update_user_log(username):
    return True

get_user_sleep("f");
