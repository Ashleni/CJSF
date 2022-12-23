Googol maps by Crazy Joe Speaking Frogs
==

Project Manager : Kevin Wang 
<br>
Devos : Shreya Roy & Faiyaz Rafee & Justin Mohabir
--
Project Description:  
Create boot-leg Google Maps. An address inputted from the client is then converted into coordinates to be passed into the yelp restaurants API and overpass API. Returns nearest restaurants and amenities within 5000 meters of the client’s inputted address. Also allows users to update the maps with their own amenities and restaurants, and an admin portal to approve it!

Apis Used:
<br> [Position Stack](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_PositionStack.md)
<br> [Yelp API](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Yelp.md)
<br> [OpenStreetMap Overpass API](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_OpenStreetMap_overpass-api.md)
<br> [Geoapify Static Maps API](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_geoapify_static_maps.md)

Launch Codes:   
* git clone https://github.com/kev1n/CJSF.git
* cd CJSF
* python3 -m venv venv
* source venv/bin/activate
* Run ```pip install -r requirements.txt```
* Run ```python3 app/__init__.py```  
* Open "localhost:5000" in your favorite browser

