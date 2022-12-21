# Clyde 'Thluffy' Sinclair
# SoftDev
# Oct 2022

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session, redirect, url_for
import os                           #facilitate key generation
import db
import api
#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "abcdef"
#app.secret_key = os.urandom(32)


@app.route("/", methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        if db.user_exists(request.form["username"]):

            #if valid -> send to home page
            if db.login_user(request.form["username"], request.form["password"]):
                session["username"] = request.form["username"]
                return redirect(url_for("home"))

            #not valid -> tell them an error message and show fresh form
            else:
                return render_template( 'login.html', error_password="Incorrect password!")
        else:
            return render_template("login.html", error_user="User doesn't exist!")
    else: #get request
            #show login form
        return render_template( 'login.html' )

@app.route('/logout')
def logout():
    # check if the user is logged in
    if 'username' not in session:
        return redirect(url_for("not_logged_in"))

    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        response = db.register_user(request.form["username"], request.form["password"])

        if response == "success":
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error_message=response)
    else: #get request
            #show login form
        return render_template( 'register.html' )

@app.route("/home", methods=['GET'])
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", past_searches=db.past_searches_for_user(session['username'])[::-1], user = session['username'])


@app.route("/dashboard", methods=['POST'])
def dashboard():
    try:

        db.add_past_search(session['username'],request.form['location'])
        coords = api.coords(request.form['location'])
        #print(coords)
        restaurants = api.restaurants(coords)
        #print(restaurants)
        amenities = api.nearest_Amenities(coords, 100)
        users = db.users_who_searched(request.form['location'])
        print(amenities)
        #print(amenities)
        print(users)
        return render_template("dashboard.html", centerLat = coords[0], centerLong = coords[1], restaurants=restaurants, \
        amenities=amenities, past_searches=db.past_searches_for_user(session['username'])[::-1], \
        users= users, \
        location = request.form['location'], latitude = api.latitude(request.form['location']), longitude = api.longitude(request.form['location']) )
    except Exception as e:
        return "An error has occured. Did you use a blank or incorrect key in keys/key_positionstack.txt or in key_yelp.txt?"



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
