# Clyde 'Thluffy' Sinclair
# SoftDev
# Oct 2022

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session, redirect, url_for
import db
#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['GET', 'POST'])
def login():
    if "username" in session:
        redirect(url_for("home"))
        
    if request.method == "POST":
        if db.user_exists(request.form["username"]):

            #if valid -> send to home page
            if db.login_user(request.form["username"], request.form["password"]):
                session["username"] = request.form["username"]
                return redirect(url_for("home"))
            
            #not valid -> tell them an error message and show fresh form
            else:
                return render_template( 'login.html', error_message="Incorrect password!")
        else:
            return render_template("login.html", error_message="User doesn't exist!")        
    else: #get request
            #show login form
        return render_template( 'login.html' )

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/register")
def register():
    if "username" in session:
        redirect(url_for("home"))
        
    if request.method == "POST":
        response = db.register_user(request.form["username"], request.form["password"])
        if response == "success":
            redirect(url_for("login"))
        else:
            render_template("register.html", error_message="response")
    else: #get request
            #show login form
        return render_template( 'register.html' )

@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
        
    return render_template("home.html")

    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()