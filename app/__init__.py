# Clyde 'Thluffy' Sinclair
# SoftDev
# Oct 2022

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session, redirect, url_for 
#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object


@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if "username" in session:
        redirect(url_for("home"))
    
if request.method == "POST":
    print("hi")
    if user_exists(request.form["username"]):

        #if valid -> send to home page
        if login_user(request.form["username"], request.form["password"]):
            redirect(url_for("home"))
        
        #not valid -> tell them an error message and show fresh form
        else:
            return render_template( 'login.html', error_message="Incorrect password!")
    else:
        return render_template("login.html", error_message="User doesn't exist!")        
else: #get request
        #show login form
    return render_template( 'login.html' )


@app.route("/auth") # , methods=['GET', 'POST'])
def authenticate():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.args ***")
    print(request.args)
    #print("***DIAG: request.args['username']  ***")
    #print(request.args['username'])
    print("***DIAG: request.headers ***")
    print(request.headers)
    return "Waaaa hooo HAAAH"  #response to a form submission

@app.route("/home") # , methods=['GET', 'POST'])
def home():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.args ***")
    print(request.args)
    #print("***DIAG: request.args['username']  ***")
    #print(request.args['username'])
    print("***DIAG: request.headers ***")
    print(request.headers)
    return "Waaaa hooo HAAAH"  #response to a form submission


    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()