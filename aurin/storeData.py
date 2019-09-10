import json
import sys
import couchdb
import requests

from FindCoordinate import locateSuburb

if len(sys.argv) != 4:
    print("Usage: python storeData.py [couchdbuser] [password] [host]")

json_file = "data_economic_prosperity.json"

json_data = open(json_file).read()

data = json.loads(json_data)

GOOGLE_MAPS_API = "https://maps.googleapis.com/maps/api/geocode/json"

user = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]

couchserver = couchdb.Server("http://%s:%s@%s/" % (user, password, host)) 

dbname = "aurin"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

params = {
    'region': 'aus'
}

for f in data["features"]:
    if (not f["properties"]["SA2_Name_2011"]
       or not f["properties"]["Median_age"]
       or not f["properties"]["Employment_rate"]
       or not f["properties"]["Average_government_benefits"]
       or not f["properties"]["Median_household_income"]):
        continue

    params['address'] = f["properties"]["SA2_Name_2011"]

    res = requests.get(GOOGLE_MAPS_API, params=params)
    while 'error_message' in res.json():
        print("Error from google")    
        res = requests.get(GOOGLE_MAPS_API, params=params)
       
    res = res.json()
    lat = res["results"][0]["geometry"]["location"]["lat"]
    lng = res["results"][0]["geometry"]["location"]["lng"]
    
    suburb = locateSuburb(lng, lat).lower()
    if suburb == "not available":
        continue

    doc = {}
    doc["_id"] = suburb
    doc["suburb"] = suburb
    doc["median_age"] = f["properties"]["Median_age"]
    doc["employment_rate"] = f["properties"]["Employment_rate"]
    doc["avg_government_benefits"] = f["properties"]["Average_government_benefits"]
    doc["median_household_income"] = f["properties"]["Median_household_income"]
    if suburb in db:
        doc2 = db[suburb]
        doc["median_age"] = (doc["median_age"] + doc2["median_age"]) / 2.0
        doc["employment_rate"] = (doc["employment_rate"] + doc2["employment_rate"]) / 2.0
        doc["avg_government_benefits"] = (doc["avg_government_benefits"] + doc2["avg_government_benefits"]) / 2.0
        doc["median_household_income"] = (doc["median_household_income"] + doc2["median_household_income"]) / 2.0
    
    print("saving/updating", suburb, "to db")
    sys.stdout.flush()
    db.update([doc])
