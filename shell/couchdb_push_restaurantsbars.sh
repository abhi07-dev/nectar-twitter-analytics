#!/usr/bin/env bash

curl -XPUT "http://${user}:${pass}@${masternode}:5984/restaurantsbars"
curl -XPOST "http://${user}:${pass}@${masternode}:5984/restaurantsbars/_bulk_docs " --header "Content-Type: application/json" \
  --data @./aurin-data/proc/City_of_Melbourne_CLUE_Bar_Tavern_Pub_Patron_Capacity__Point__2016.json
curl -XPOST "http://${user}:${pass}@${masternode}:5984/restaurantsbars/_bulk_docs " --header "Content-Type: application/json" \
  --data @./aurin-data/proc/City_of_Melbourne_CLUE_Cafe_Restaurant_Bistro_Seats__Point__2016_.json