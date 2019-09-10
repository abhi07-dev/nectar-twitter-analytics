import json
import sys
sys.path.insert(0, '../aurin')
from FindCoordinate import locateSuburb

filename = "../aurin-data/raw/City_of_Melbourne_CLUE_Bar_Tavern_Pub_Patron_Capacity__Point__2016.json"
write = "../aurin-data/proc/City_of_Melbourne_CLUE_Bar_Tavern_Pub_Patron_Capacity__Point__2016.json"

with open(filename, 'r') as fp:
    data = json.load(fp)
for feature in data["features"]:
    lon = feature["geometry"]["coordinates"][0]
    lat = feature["geometry"]["coordinates"][1]
    feature["suburb"] = locateSuburb(lon, lat).lower()
    
with open(write, 'w') as fp:
    json.dump(data, fp)
