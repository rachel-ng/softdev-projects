# Maggie Zhao
# SoftDev1 pd7
# K
# 2018-##-##

import sqlite3

#opens if db exist, otherwise create
db = sqlite3.connect("foo")
#used to traverse db
c = db.cursor() #facilitate db ops

# creates a table. make sure to rm <table> every time it is run, or it will tell you [ table <name> already exists ]
c.execute( "CREATE TABLE roster(name TEXT, userid INTEGER)")

# inserts values into the table. make sure all text is in single quotes (''). If it does not have quotes, it will recognize the text as a column. Double quotes ("") gives you an error for invalid syntax

c.execute("INSERT INTO roster VALUES ('Valerie', 34)")
c.execute("INSERT INTO roster VALUES ('Jemma', 28)")
c.execute("INSERT INTO roster VALUES ('Bob', -3)")

# does not do anything in terminal
# saves as list, need a for loop to navigate through it
# uses unICODE
boo = c.execute("SELECT * FROM roster")
for row in boo:
    print(row)
db.commit() #save changes
db.close()

'''
if the sqlite terminal looks like
sqlite> SELECT * FROM roster
    ...>
you are probably missing the semicolon (;)
'''
