from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission
from pprint import pprint

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
#def nameAndOperator(longitude, latitude):
def nameAndOperator(coords):
    latitude = coords[0]
    longitude = coords[1]
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
def nearest_Amenities(coords, magnitude):
    longitude = coords[1]
    latitude = coords[0]
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];way(around:""" + str(magnitude) + """,""" + latitude + """,""" + longitude + """);out;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    print(response.url)
    data = response.json()
    #pprint(data)
    place_list = []
    for x in range(len(data["elements"])):
        if  "tags" in data["elements"][x] and "name" in data["elements"][x]["tags"] and data["elements"][x]["tags"]["name"] not in place_list:
            place_list.append(str(data["elements"][x]["tags"]["name"]))
    return place_list



#yelp!
def restaurants(coords):
    latitude = coords[0]
    longitude = coords[1]
    url = "https://api.yelp.com/v3/businesses/search?latitude=" + latitude + "&longitude=" + longitude + "&term=restaurant&sort_by=best_match&limit=20"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer 3j_qPIkE1w9a0hDM1adjkt4P3yVUkqShLfwy-vJb3ZRGf157342vujvG0rLHQsZ2yjZtXKPFojNdnjZUvE3v3E7H9JY_6DOO0rI6GN8aw0KfKS-NGzpw9OBgWoOTY3Yx"
    }
    r = requests.get(url, headers=headers)
    data  =  r.json()
    #pprint(data)
    place_dict = {}
    for x in range(len(data["businesses"])):
        if "name" in data["businesses"][x] and data["businesses"][x]["name"] not in place_dict:
            coords = [str(data["businesses"][x]["coordinates"]["latitude"]), str(data["businesses"][x]["coordinates"]["longitude"])]
            place_dict[str(data["businesses"][x]["name"])] = coords
    return place_dict

    ''' #returns list of only restaurant names
    place_list = []
    for x in range(len(data["businesses"])):
        if "name"  in data["businesses"][x] and data["businesses"][x]["name"] not in place_list:
            place_list.append(str(data["businesses"][x]["name"]))
    return place_list
    '''



    # FIX IT AT HOME MAKE LONGITIUDW AND LATITUDE THE SAME 
longitude = longitude(" 345 Chambers, NY, NY ")
latitude = latitude(" 345 Chambers, NY, NY  ")
print(str(latitude) + "," + str(longitude))
#print(nearest_Amenities(latitude, longitude, 50))
print(restaurants(latitude, longitude))
