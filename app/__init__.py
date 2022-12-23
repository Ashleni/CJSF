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
        print(restaurants)
        amenities = api.nearest_Amenities(coords, 100)
        users = db.users_who_searched(request.form['location'])
        img = api.maps(coords)

        return render_template("dashboard.html", centerLat = coords[0], centerLong = coords[1], restaurants=restaurants, \
        amenities=amenities, past_searches=db.past_searches_for_user(session['username'])[::-1], \
        users= users, \
        location = request.form['location'], latitude = api.latitude(request.form['location']), longitude = api.longitude(request.form['location']), map = img )
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
        if db.is_admin(session["username"]):
            return render_template("adminPanel.html")
        else:
            return render_template("requestAdmin.html", hasRequested = db.has_requested_admin(session["username"]))

@app.route("/add", methods=['GET', "POST"])
def add():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        upload_file()
        return "Successfully uploaded"
    else: #get request
        print(db.is_admin(session["username"]))
        return render_template("add.html", isAdmin=db.is_admin(session["username"]))
    

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

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
