from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object






#position stack!

def latitude(location):
    key = open("keys/key_positionstack.txt", "r").read()
    key = key.strip()
    query = location
    link = 'http://api.positionstack.com/v1/forward?access_key=' + key + '&query=' + query
    #region = '&region=Rio+de+Janeiro&limit=1'
    #print(link)
    r = requests.get(link) 
    info = r.json()
    return info['data'][0]['latitude']
    
    
def longitude(location):
    key = open("keys/key_positionstack.txt", "r").read()
    key = key.strip()
    query = location
    link = 'http://api.positionstack.com/v1/forward?access_key=' + key + '&query=' + query
    #region = '&region=Rio+de+Janeiro&limit=1'
    #print(link)
    r = requests.get(link) 
    info = r.json()
    return info['data'][0]['longitude']
    

    
#print(longitude("new york city"))
#print(latitude("new york city"))



#city bikes!

def nearest_bikes(longitude, latitude):
    link = "https://api.citybik.es/v2/networks"
    r = requests.get(link)
    info = r.json()
    for row in info['networks']:
        print(row['location']['city'] +": " + row['name'])

#nearest_bikes()


#open street map!

def nameAndOperator(longitude, latitude):
    link = "https://overpass-api.de/api/interpreter?[out:json];way(around:50," + latitude + "," + longitude + ");out;"
    print(link)
    #link = "https://overpass-api.de/api/interpreter?[out:json];way(around:50,40.755884,-73.978504);out;"
    r = requests.get(link)
    #info = r.json()
    return r.text


longitude = str(longitude("Stuyvesant High School"))
latitude = str(latitude("Stuyvesant High School"))
print(nameAndOperator(longitude, latitude))
