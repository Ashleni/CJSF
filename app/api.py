from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object






#position stack!

# returns latitude as int of location
# string detailing location with any amt of info needed
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
    
   
# returns longitude as int of location
# string detailing location with any amt of info needed
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



#open street map!

#brokcen :'(
def nameAndOperator(longitude, latitude):
    link = "https://overpass-api.de/api/interpreter?[out:json];way(around:50," + latitude + "," + longitude + ");out;"
    #print(link)
    link2 = 'https://overpass-api.de/api/interpreter'
    query = """
    [out:json];
    way(around:50,40.755884,-73.978504);
    out;
    """
    
    #info = r.json()
    r = requests.get(link2, params={'data': query})
    print(r.url)
    return r.json()
    
    
# returns list of nearest places, roads, buildings, etc. 
# latitude, longitude, and magnitude (all ints) needed.
def nearest_Amenities(latitude, longitude, magnitude):
    longitude = str(longitude)
    latitude = str(latitude)
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];way(around:""" + str(magnitude) + """,""" + latitude + """,""" + longitude + """);out;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    print(response.url)
    data = response.json()
    place_list = []
    for x in range(len(data["elements"])):
        if  "tags" in data["elements"][x] and "name" in data["elements"][x]["tags"] and data["elements"][x]["tags"]["name"] not in place_list:
            place_list.append(str(data["elements"][x]["tags"]["name"]))
    return place_list


longitude = longitude(" Antarctica ")
latitude = latitude(" Antarctica")
print(str(latitude) + "," + str(longitude))
print(nearest_Amenities(latitude, longitude, 300))