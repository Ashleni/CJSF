from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission
from pprint import pprint

app = Flask(__name__)    #create Flask object

#position stack!

# returns list, latitude first, longitude second, both ints
def coords(location):
    key = open("app/keys/key_positionstack.txt", "r").read()
    key = key.strip()
    query = location
    link = 'http://api.positionstack.com/v1/forward?access_key=' + key + '&query=' + query
    r = requests.get(link) 
    info = r.json()
    latitude = info['data'][0]['latitude']
    longitude = info['data'][0]['longitude']
    return [latitude, longitude]

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
    place_dict = {}
    for x in range(len(data["elements"])):
        if  "tags" in data["elements"][x] and "name" in data["elements"][x]["tags"] and data["elements"][x]["tags"]["name"] not in place_dict:
            coords = [str(data["elements"][x]["geometry"][0]["lat"]), str(data["elements"][x]["geometry"][0]["lon"])]
            place_dict[str(data["elements"][x]["tags"]["name"])] = coords
    return place_dict

'''
#open street map
def near(coords, magnitude):
    longitude = str(coords[1])
    latitude = str(coords[0])
    url = "https://www.openstreetmap.org/#map=" + str(magnitude) + "/" + latitude + "/" + longitude
    r = requests.get(url)
    print(url)
    data = r.json()
    pprint(data)
'''


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
            place_dict[str(data["businesses"][x]["name"])] = coords
    return place_dict

    ''' #returns list of only restaurant names
    place_list = []
    for x in range(len(data["businesses"])):
        if "name"  in data["businesses"][x] and data["businesses"][x]["name"] not in place_list:
            place_list.append(str(data["businesses"][x]["name"]))
    return place_list
    '''
    
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


#test commands!
#longitude = longitude(" 345 Chambers, NY, NY ")
#latitude = latitude(" 345 Chambers, NY, NY  ")
#print(str(latitude) + "," + str(longitude))
#print(nearest_Amenities(latitude, longitude, 50))
#print(restaurants(coords("345 Chambers, NY, NY")))
#print(coords("345 Chambers, NY, NY"))
print(restaurantsAddress(coords("345 Chambers, NY, NY")))



#open street map!

'''
#brokcen :'(
def nameAndOperator(coords):
    latitude = str(coords[0])
    longitude = str(coords[1])
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
''' 

'''
#city bikes!
# not being used anymore :'(
def nearest_bikes(longitude, latitude):
    link = "https://api.citybik.es/v2/networks"
    r = requests.get(link)
    info = r.json()
    for row in info['networks']:
        print(row['location']['city'] +": " + row['name'])
'''