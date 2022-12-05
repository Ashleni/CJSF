
from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

key = 
link = 'http://api.positionstack.com/v1/forward?access_key=5e990e9a2a02b3952708f993eaeb5c44&query=Copacabana&region=Rio+de+Janeiro&limit=1'
print(link)
r = requests.get(link) #new line at end of key file
print(r.json())
    


