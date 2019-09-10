#!/usr/bin/env bash

curl -XPUT "http://${user}:${pass}@${masternode}:5984/twitter"
curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_bulk_docs " --header "Content-Type: application/json" \
  --data @./couchdb/twitter/data.json