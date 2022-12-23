from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission
from pprint import pprint

app = Flask(__name__)    #create Flask object


#==========================================================
#position stack!

# returns list, latitude first, longitude second, both ints
def coords(location):
    try:
        key = open("app/keys/key_positionstack.txt", "r").read()
        key = key.strip()
        query = location
        link = 'http://api.positionstack.com/v1/forward?access_key=' + key + '&query=' + query
        r = requests.get(link) 
        #pprint(link)
        info = r.json()
        if not info['data']:
            print("EMPTY LIST")
        else:
            latitude = info['data'][0]['latitude']
            longitude = info['data'][0]['longitude']
        return [latitude, longitude]
    except Exception as e:
        return "invalid"

# returns latitude as int of location
# location should be string with any amt of info needed
def latitude(location):
    key = open("app/keys/key_positionstack.txt", "r").read()
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
    key = open("app/keys/key_positionstack.txt", "r").read()
    key = key.strip()
    query = location
    link = 'http://api.positionstack.com/v1/forward?access_key=' + key + '&query=' + query
    #region = '&region=Rio+de+Janeiro&limit=1'
    #print(link)
    r = requests.get(link) 
    info = r.json()
    return info['data'][0]['longitude']
    

#==========================================================
# overpass api!
# returns dictionary of nearest amenities, key is amenity name and value is coord list (latitude, longitude). ALL STRINGS
def nearest_Amenities(coords, magnitude):
    longitude = str(coords[1])
    latitude = str(coords[0])
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (way(around:{magnitude},{latitude},{longitude});
    );
    out geom;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    #pprint(data)
    #pprint(data)
    place_dict = {}
    for x in range(len(data["elements"])):
        if  "tags" in data["elements"][x] and "name" in data["elements"][x]["tags"] and data["elements"][x]["tags"]["name"] not in place_dict:
            coords = [str(data["elements"][x]["geometry"][0]["lat"]), str(data["elements"][x]["geometry"][0]["lon"])]
            place_dict[str(data["elements"][x]["tags"]["name"])] = coords
    return place_dict


#==========================================================
#yelp!

# returns dictionary of restaurants, key is restaurant name and value is coord list (latitude, longitude). ALL STRINGS
def restaurants(coords):
    latitude = str(coords[0])
    longitude = str(coords[1])
    key = open("app/keys/key_yelp.txt", "r").read()
    key = key.strip()
    url = "https://api.yelp.com/v3/businesses/search?latitude=" + latitude + "&longitude=" + longitude + "&term=restaurant&sort_by=best_match&limit=20"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + key
    }
    r = requests.get(url, headers=headers)
    data  =  r.json()
    #pprint(data)
    place_dict = {}

    for x in range(len(data["businesses"])):
        if "name" in data["businesses"][x] and data["businesses"][x]["name"] not in place_dict:
            coords = [str(data["businesses"][x]["coordinates"]["latitude"]), str(data["businesses"][x]["coordinates"]["longitude"])]
            address = ""
            for y in range(len(data["businesses"][x]["location"]["display_address"])):
                address += str(data["businesses"][x]["location"]["display_address"][y]) + " " 
            categories = []
            for y in range(len(data["businesses"][x]["categories"])):
                categories += [str(data["businesses"][x]["categories"][y]["title"])]
            rating = str(data["businesses"][x]["rating"])
            phone = str(data["businesses"][x]["phone"])
            img_url = str(data["businesses"][x]["image_url"])
            distance = str(round(data["businesses"][x]["distance"]))
            if data["businesses"][x]["is_closed"]:
                closed_open = "Currently open"
            else:
                closed_open = "Currently closed"
            place_dict[str(data["businesses"][x]["name"])] = [coords, address, categories, rating, phone, img_url, distance, closed_open]
    return place_dict
    
# returns dictionary of restaurants, key is restaurant name and value is address. ALL STRINGS
def restaurantsAddress(coords):
    latitude = str(coords[0])
    longitude = str(coords[1])
    key = open("app/keys/key_yelp.txt", "r").read()
    key = key.strip()
    url = "https://api.yelp.com/v3/businesses/search?latitude=" + latitude + "&longitude=" + longitude + "&term=restaurant&sort_by=best_match&limit=20"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + key
    }
    r = requests.get(url, headers=headers)
    data  =  r.json()
    #pprint(data)
    place_dict = {}
    
    for x in range(len(data["businesses"])):
        if "name" in data["businesses"][x] and data["businesses"][x]["name"] not in place_dict:
            address = str(data["businesses"][x]["location"]["display_address"][0]) + ", " + str(data["businesses"][x]["location"]["display_address"][1])
            place_dict[str(data["businesses"][x]["name"])] = address
    return place_dict
    
def restaurantInfo(coords):
    latitude = str(coords[0])
    longitude = str(coords[1])
    key = open("app/keys/key_yelp.txt", "r").read()
    key = key.strip()
    url = "https://api.yelp.com/v3/businesses/search?latitude=" + latitude + "&longitude=" + longitude + "&term=restaurant&sort_by=best_match&limit=20"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + key
    }
    r = requests.get(url, headers=headers)
    data  =  r.json()
    #pprint(data)
    place_dict = {}
    for x in range(len(data["businesses"])):
        if "name" in data["businesses"][x] and data["businesses"][x]["name"] not in place_dict:
            address = ""
            for y in range(len(data["businesses"][x]["location"]["display_address"])):
                address += str(data["businesses"][x]["location"]["display_address"][y]) + " " 
            categories = []
            for y in range(len(data["businesses"][x]["categories"])):
                categories += [str(data["businesses"][x]["categories"][y]["title"])]
            rating = str(data["businesses"][x]["rating"])
            phone = str(data["businesses"][x]["display_phone"])
            img_url = str(data["businesses"][x]["image_url"])
            distance = str(data["businesses"][x]["distance"])
            if data["businesses"][x]["is_closed"]:
                closed_open = "Currently open"
            else:
                closed_open = "Currently closed"
            place_dict[str(data["businesses"][x]["name"])] = [address, categories, rating, phone, img_url, distance, closed_open]
    return place_dict


#==========================================================
# geoapify!
# returns link to a generated image of a map.
def maps(coords):
    latitude = str(coords[0])
    longitude = str(coords[1])
    key = open("app/keys/key_geoapify.txt", "r").read()
    key = key.strip()
    #url = "https://api.yelp.com/v3/businesses/search?latitude=" + latitude + "&longitude=" + longitude + "&term=restaurant&sort_by=best_match&limit=20"
    #url = "https://maps.geoapify.com/v1/staticmap?style=osm-bright-smooth&width=600&height=400&center=lonlat%3A-122.29009844646316%2C47.54607447032754&zoom=14.3497&marker=lonlat%3A-122.29188334609739%2C47.54403990655936%3Btype%3Aawesome%3Bcolor%3A%23bb3f73%3Bsize%3Ax-large%3Bicon%3Apaw%7Clonlat%3A-122.29282631194182%2C47.549609195001494%3Btype%3Amaterial%3Bcolor%3A%234c905a%3Bicon%3Atree%3Bicontype%3Aawesome%7Clonlat%3A-122.28726954893025%2C47.541766557545884%3Btype%3Amaterial%3Bcolor%3A%234c905a%3Bicon%3Atree%3Bicontype%3Aawesome&apiKey=ccbf1f8595484e5f8216653ae249b4b4
    url = "https://maps.geoapify.com/v1/staticmap?style=osm-bright-smooth&width=600&height=400&center=lonlat:" + longitude + "," + latitude + "&zoom=13.7401&apiKey=" + key
    return url
    
    
    
#==========================================================    

#test commands!
#longitude = longitude(" 345 Chambers, NY, NY ")
#latitude = latitude(" 345 Chambers, NY, NY  ")
#print(str(latitude) + "," + str(longitude))
#print(nearest_Amenities(latitude, longitude, 50))
#print(restaurantInfo(coords("345 chambers")))
#print(coords("ajsgdfsuihdsfuirehdsifu esguiesi dfugh df"))
#print(maps(coords("345 chambers")))



