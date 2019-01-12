import json
import urllib.request
import sqlite3
from datetime import datetime

#opens if db exist, otherwise create
DB_FILE = "data/health.db"

with open('keys/keys.json', 'r') as f:
    api_dict = json.load(f)

API_KEY = api_dict["USDA_NUTRIENTS_API"]
