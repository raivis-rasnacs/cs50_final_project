import sqlite3

# Connect db
con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()