#This program will prompt for a location, contact a web service and retrieve JSON for the web service and parse that data, and retrieve the first place_id from the JSON. 
#A place ID is a textual identifier that uniquely identifies a place as within Google Maps.


import urllib
import urllib.request
import json

serviceURL = "https://maps.googleapis.com/maps/api/geocode/json?"
##regular Google API

##serviceURL = 'http://python-data.dr-chuck.net/geojson?'
##prepared API for the course results 

while True:
    address = input("Enter location: ")
    ##for example enter: South Federal University
    ##for Assignment solution: Universidade Federal do Rio Grande do Sul
    
    if len(address) < 1 : break


    url = serviceURL + urllib.parse.urlencode({"sensor" : "false", "address" : address})
    #urllib library has diffrent method in Python 3.x - see above (added "parse" in the middle)
    print ("Retrieving"), url
    open_url = urllib.request.urlopen(url)
    data = open_url.read()
    print ("Retrieved", len(data), "characters")

    js = json.loads(data)
    try: js = json.loads(data)
    except: js = None
    if "status" not in js or js["status"] != "OK":
        print ("===== Failure To Retrieve =====")
        print (data)
        continue

    print (json.dumps(js, indent = 4)) ##pretty printing with indentation

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    #entering each value - it's dictionary with list within dictionaries, etc.
    print ("Latitude: ", lat, "Longitude: ", lng)
    location = js["results"][0]["formatted_address"]
    place_ID = js["results"][0]["place_id"]
    print ("Place ID: ", place_ID)
    print ("Location: ", location)
    


    
    
