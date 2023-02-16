# Clyde 'Thluffy' Sinclair
# SoftDev
# Oct 2022

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session, redirect, url_for, flash
import os                           #facilitate key generation
import db
import api
import traceback
from werkzeug.utils import secure_filename
from math import cos, asin, sqrt, pi
#the conventional way:
#from flask import Flask, render_template, request

UPLOAD_FOLDER = 'app/static/imgs'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    #print(db.get_all_requested_admins())
    #print(db.get_all_requested_amenities())
    #print(db.get_all_requested_restaurants())
    #print(db.get_all_approved_amenities())
    #print(db.get_all_approved_restaurants())
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", past_searches=db.past_searches_for_user(session['username'])[::-1], user = session['username'])


@app.route("/dashboard", methods=['POST'])
def dashboard():
    try:

        db.add_past_search(session['username'],request.form['location'])
        coords = api.coords(request.form['location'])
        if coords == "invalid":
            return render_template("home.html", error = "Invalid input, no results found.", past_searches=db.past_searches_for_user(session['username'])[::-1], user = session['username'])
        else:
            #print(coords)
            restaurants = api.restaurants(coords)
            #print(restaurants)
            amenities = api.nearest_Amenities(coords, 100)
            users = db.users_who_searched(request.form['location'])
            img = api.maps(coords)

            user_restaurants = db.get_all_approved_restaurants()
            user_amenities = db.get_all_approved_amenities()
            #print(user_amenities)
            user_restaurants_dict = {}
            restaurants_too_far = 0
            for i in user_restaurants:
                name = i[1]
                dist = round(distance(i[4], i[5], coords[0], coords[1]) * 1000)
                user_restaurants_dict[name] = [i[2], i[3], i[4], i[5], dist]
                if dist > 5000:
                    restaurants_too_far += 1

            user_amenities_dict = {}
            for i in user_amenities:
                name = i[1]
                user_amenities_dict[name] = [i[2], i[3], round(distance(i[2], i[3], coords[0], coords[1]) * 1000)]

            print(user_amenities)
            return render_template("dashboard.html",
                centerLat = coords[0],
                centerLong = coords[1],
                restaurants=restaurants,
                amenities=amenities,
                past_searches=db.past_searches_for_user(session['username'])[::-1],
                users= users,
                location = request.form['location'],
                latitude = api.latitude(request.form['location']),
                longitude = api.longitude(request.form['location']),
                map = img,
                user_restaurants = user_restaurants_dict,
                user_amenities = user_amenities_dict,
                restaurants_too_far = restaurants_too_far
            )
    except Exception as e:
        print(traceback.format_exc())
        return "An error has occured. Did you use a blank or incorrect key in keys/key_positionstack.txt or in key_yelp.txt?"

@app.route("/admin", methods=['GET', "POST"])
def admin():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        db.request_admin(session["username"])
        return render_template("requestAdmin.html", hasRequested = db.has_requested_admin(session["username"]), success = True)
    else: #get request
        if db.is_admin(session["username"]): # for admins only
            requested_admins = db.get_all_requested_admins()
            requested_amenities = db.get_all_requested_amenities()
            requested_restaurants = db.get_all_requested_restaurants()
            return render_template("adminPanel.html", requested_admins = requested_admins, requested_amenities = requested_amenities, requested_restaurants = requested_restaurants)
        else:
            return render_template("requestAdmin.html", hasRequested = db.has_requested_admin(session["username"]), banned = db.has_rejected_admin(session["username"]))

@app.route("/add", methods=['GET'])
def add():
    if "username" not in session:
        return redirect(url_for("login"))

    isAdmin = db.is_admin(session["username"])
    return render_template("add.html", isAdmin=isAdmin, amenitysuccess=request.args.get('amenitysuccess'), restaurantsuccess=request.args.get('restaurantsuccess'))
    
@app.route("/addamenity", methods=['POST'])
def addamenity():

    isAdmin = db.is_admin(session["username"])
    if isAdmin:
        db.create_new_amenity(request.form["name"], request.form["latitude"], request.form["longitude"], session["username"])
    else:
        db.suggest_new_amenity(request.form["name"], request.form["latitude"], request.form["longitude"], session["username"])
    return redirect(url_for("add", amenitysuccess = True))

@app.route("/addrestaurant", methods=['POST'])
def addrestaurant():

    isAdmin = db.is_admin(session["username"])
    filename = upload_file()
    if isAdmin:
        #name, stars, imgname, latitude, longitude, proposer
        db.create_new_restaurant(request.form["name"], request.form["rating"], filename, request.form["latitude"], request.form["longitude"], session["username"])
    else:
        db.suggest_new_restaurant(request.form["name"], request.form["rating"], filename, request.form["latitude"], request.form["longitude"], session["username"])
    return redirect(url_for("add", restaurantsuccess = True))

@app.route("/approve-admins", methods=["POST"])
def approve_admins():
    if request.form["approval"] == "reject":
        db.reject_admin(request.form["username"])
    else: # approve
        db.approve_admin(request.form["username"])
    return redirect(url_for("admin"))

@app.route("/approve-amenity", methods=["POST"])
def approve_amenity():
    if request.form["approval"] == "reject":
        db.reject_amenity(request.form["id"])
    else: # approve
        db.approve_amenity(request.form["id"], session["username"])
    return redirect(url_for("admin"))

@app.route("/approve-restaurant", methods=["POST"])
def approve_restaurant():
    if request.form["approval"] == "reject":
        db.reject_restaurant(request.form["id"])
    else: # approve
        db.approve_restaurant(request.form["id"], session["username"])
    return redirect(url_for("admin"))




def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename


def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.run()
