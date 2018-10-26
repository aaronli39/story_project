import sqlite3

#open("../data/info.db","w").close() #Resets Database

db = sqlite3.connect("../data/info.db")

c = db.cursor()

#Setting up tables
'''creates table to store user information'''
c.execute("CREATE TABLE IF NOT EXISTS userInfo(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, pass TEXT)")

'''creates table to store story information'''
c.execute("CREATE TABLE IF NOT EXISTS stories(name TEXT, username TEXT, contrib TEXT)")

db.commit()
db.close()

