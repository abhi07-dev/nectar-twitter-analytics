cd ~/nectar-twitter-analytics/cdb-grunt

sudo docker pull couchdb:2.1.1

#export declare -a nodes=(172.17.0.2 172.17.0.3 172.17.0.4)
#export masternode=`echo ${nodes} | cut -f1 -d' '`
#export size=${#nodes[@]}
#export user=admin
#export pass=admin

#for i in ${!nodes[@]}; do docker run -d --rm -v /database/node$i:/opt/couchdb/data couchdb:2.1.1 --ip=${nodes[$i]}; done

#docker run -d --rm -v /database/node0:/opt/couchdb/data couchdb:2.1.1 --ip=172.17.0.2

#for i in ${!nodes[@]}; do docker create -v /database/node$i:/opt/couchdb/data couchdb:2.1.1 -–ip=${nodes[$i]}; done

#for i in ${!nodes[@]}; do docker create couchdb:2.1.1 -–ip=${nodes[$i]}; done

docker create -v /database/node1:/opt/couchdb/data couchdb:2.1.1 -–ip=172.17.0.2
docker create -v /database/node2:/opt/couchdb/data couchdb:2.1.1 -–ip=172.17.0.3
docker create -v /database/node0:/opt/couchdb/data --network host couchdb:2.1.1
export declare nodes=(127.0.0.1 172.17.0.2 172.17.0.3)
export masternode=127.0.0.1
export size=${#nodes[@]}
export user=admin
export pass=admin

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

for cont in "${conts[@]}"; do docker start ${cont}; done
sleep 3

for (( i=0; i<${size}; i++ )); do
    docker exec ${conts[${i}]} \
      bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
    docker exec ${conts[${i}]} \
      bash -c "echo \"-name couchdb@${nodes[${i}]}\" >> /opt/couchdb/etc/vm.args"
done

for cont in "${conts[@]}"; do docker restart ${cont}; done
sleep 6

for node in "${nodes[@]}"; do     
    curl -XPUT "http://${node}:5984/_node/_local/_config/admins/${user}" --data "\"${pass}\""    
    curl -XPUT "http://${user}:${pass}@${node}:5984/_node/couchdb@${node}/_config/chttpd/bind_address" --data '"0.0.0.0"'
done

for node in "${nodes[@]}"; do     
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \
        \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\", \
        \"remote_node\": \"${node}\", \
        \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done

for node in "${nodes[@]}"; do     
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"add_node\", \"host\":\"${node}\", \
        \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done

curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

	
rev=`curl -XGET "http://127.0.0.1:5986/_nodes/nonode@nohost" --user "${user}:${pass}" | sed -e 's/[{}"]//g' | cut -f3 -d:`

curl -X DELETE "http://127.0.0.1:5986/_nodes/nonode@nohost?rev=${rev}"  --user "${user}:${pass}"

curl -XPUT "http://${user}:${pass}@${masternode}:5984/twitter"
curl -XPUT "http://${user}:${pass}@${masternode}:5984/aurin"
curl -XPUT "http://${user}:${pass}@${masternode}:5984/restaurantsbars"