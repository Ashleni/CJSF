#Crazy Joe Speaks Frogs:: Kevin Wang & Shreya Roy & Faiyaz Rafee & Justin Mohabir
#SoftDev  
#P01
#2022-12-05

import sqlite3   #enable control of an sqlite database
DB_FILE="gabagoo.db"
#===========================MOCK STATIC DATABASE TO POPULATE ROUTES W/ DATA=============================== 
def wipeDB():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    c.execute("DROP TABLE if exists users") #drop so no need to delete database each time the code changes
    c.execute("DROP TABLE if exists pastSearches")
    c.executescript(""" 
        CREATE TABLE authentication (username TEXT PRIMARY KEY, password TEXT NOT NULL);
        CREATE TABLE pastSearches (username TEXT NOT NULL, pastSearch TEXT NOT NULL);
    """
    ) #Primary key is implicityly NOT NULL
    db.commit() #save changes
    db.close()  #close database
    return True
#==========================================================
def start():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()
    c.executescript(""" 
        CREATE TABLE IF NOT EXISTS authentication (username TEXT PRIMARY KEY, password TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS pastSearches (username TEXT NOT NULL, pastSearch TEXT NOT NULL);
    """
    )
    if len(c.execute("SELECT * FROM authentication").fetchall()) == 0:
        sample()
    db.commit() #save changes
    db.close()  #close database
    return True
#==========================================================
def sample(): #adds sample data
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    register_user("kevin", "abcdefgh")
    register_user("faiyaz", "12345678")
    date = c.execute("SELECT DATETIME('now');").fetchall()
    past_searches = [
        ("faiyaz", "345 Chambers St"),
        ("kevin", "29 Fort Greene Pl")
    ]
    c.executemany("INSERT INTO pastSearches VALUES(?, ?)", past_searches)
    db.commit() #save changes
    db.close()
    return True
#==========================================================
def add_past_search(username, search):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    c.execute("INSERT INTO pastSearches VALUES(?, ?)", (username, search))
    db.commit() #save changes
    db.close()
    return True


#==========================================================
def user_exists(a): #determines if user exists
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT username, password FROM authentication WHERE username = ?", (a,)).fetchall() #needs to be in ' ', ? notation doesnt help with this 
    db.close()
    if len(results) > 0:
        return True
    else: 
        return False
#==========================================================
def register_user(username, password): #determines if input is valid to register, adds to users table if so
    if user_exists(username) or len(username) == 0 or len(password) < 8:
        return False
    else:
        db = sqlite3.connect(DB_FILE, check_same_thread=False) 
        c = db.cursor()
        inserter = [(username, password)]
        c.executemany("INSERT INTO authentication VALUES(?, ?);", inserter)
        db.commit() #save changes
        db.close()
        return True

#==========================================================
def login_user(username, password): 
    if user_exists(username):
        db = sqlite3.connect(DB_FILE, check_same_thread=False) 
        c = db.cursor()
        results = c.execute("SELECT password FROM authentication WHERE username = ?", (username,)).fetchall()
        db.close()
        return password == results[0][0]
    return False
#==========================================================
def all_users(): #for printing all users and past searches 
    db = sqlite3.connect(DB_FILE, check_same_thread=False) 
    c = db.cursor()
    results = c.execute("SELECT * FROM pastSearches;").fetchall()
    db.close()
    return results
#==========================================================
def past_searches_for_user(username): #for printing all users and past searches 
    db = sqlite3.connect(DB_FILE, check_same_thread=False) 
    c = db.cursor()
    results = c.execute("SELECT * FROM pastSearches WHERE username = ?;", (username, )).fetchall()
    db.close()
    return results
#==========================================================
def reset():
    start()
    sample()
#==========================================================