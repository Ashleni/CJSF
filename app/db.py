#Crazy Joe Speaks Frogs:: Kevin Wang & Shreya Roy & Faiyaz Rafee & Justin Mohabir
#SoftDev  
#P01
#2022-12-05

import sqlite3   #enable control of an sqlite database
DB_FILE="database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
#===========================MOCK STATIC DATABASE TO POPULATE ROUTES W/ DATA=============================== 
def wipeDB():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    c.execute("DROP TABLE if exists authentication") #drop so no need to delete database each time the code changes
    c.execute("DROP TABLE if exists pastSearches")
    c.execute("DROP TABLE if exists isAdmin")
    c.executescript(""" 
        CREATE TABLE authentication (username TEXT PRIMARY KEY, password TEXT NOT NULL);
        CREATE TABLE pastSearches (username TEXT NOT NULL, pastSearch TEXT NOT NULL);
        CREATE TABLE isAdmin (username TEXT PRIMARY KEY, admin INTEGER NOT NULL);
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
        CREATE TABLE IF NOT EXISTS isAdmin (username TEXT PRIMARY KEY, admin INTEGER NOT NULL, isRequested INTEGER NOT NULL);
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
    register_user("admin", "adminadmin")

    make_admin("admin")

    past_searches = [
        ("faiyaz", "345 Chambers St"),
        ("kevin", "29 Fort Greene Pl")
    ]
    c.executemany("INSERT INTO pastSearches VALUES(?, ?)", past_searches)
    db.commit() #save changes
    db.close()
    return True

#==========================================================
def make_admin(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    c.execute("REPLACE INTO isAdmin VALUES(?, ?)", (username, 1))
    db.commit() #save changes
    db.close()
    return True

#==========================================================
def make_regular_user(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    c.execute("INSERT INTO isAdmin VALUES(?, ?)", (username, 0))
    db.commit() #save changes
    db.close()
    return True

#==========================================================
def is_admin(username): #determines if user is admin
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT admin FROM isAdmin WHERE username = ?", (username,)).fetchall() #needs to be in ' ', ? notation doesnt help with this 
    db.close()

    if len(results) > 0:
        if results[0][0] == 1:
            return True
        else:
            return False
    else: 
        return False
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
    if user_exists(username):
        return "user already exists"
    elif len(username) == 0:
        return "username can't be blank"
    elif len(password) < 8:
        return "password must be greater than 8 digits"
    else:
        db = sqlite3.connect(DB_FILE, check_same_thread=False) 
        c = db.cursor()
        make_regular_user(username)
        c.execute("INSERT INTO authentication VALUES(?, ?);", (username, password))
        db.commit() #save changes
        db.close()
        return "success"

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
def users_who_searched(search): #for printing all users and past searches 
    db = sqlite3.connect(DB_FILE, check_same_thread=False) 
    c = db.cursor()
    results = c.execute("SELECT DISTINCT username FROM pastSearches WHERE pastSearch = ?;", (search, )).fetchall()
    db.close()
    return results
#==========================================================
def reset():
    wipeDB()
    start()
#==========================================================

reset()